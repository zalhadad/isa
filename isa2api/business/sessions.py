import pandas as pd
import numpy as np
import json

from isa2api.database import db, where, select


class Sessions():

    def __init__(self, params):
        params.setdefault('offset', (params.page - 1) * params.per_page)
        sql = "SELECT * FROM sessions" + where(params)
        sql += ' ORDER BY ' + params.get('sort') + ' ' + params.get(
            'order') + ' LIMIT %(per_page)s OFFSET %(offset)s '
        sql2 = "SELECT count(*) FROM sessions" + where(params)
        self.total = select(sql2, params)[0]['count']
        self.data = pd.read_sql(sql, db, params=params)

    def get(self):
        return json.loads(self.data.to_json(orient='records', date_format='iso'))

    def __repr__(self):
        return self.data.to_json(orient='records')


class History():

    def __init__(self, id, info):
        self.id = id
        sql = "SELECT timestamp,node,info FROM sessions_history WHERE session=%(id)s AND (node <> '' "
        if info:
            sql += "OR (info <> '' AND info <> 'endOfWavFile')"
        sql += " )  ORDER BY timestamp"
        history = pd.read_sql(sql, db, params={'id': self.id})
        self.edges = []
        self.nodes = []
        if history.size > 0:
            history = pd.melt(history, id_vars='timestamp', value_vars=[
                'node', 'info'], var_name='type', value_name='node').replace('', np.nan).dropna()
            history.set_index(history.groupby(history.timestamp.values.astype('datetime64[ms]')).cumcount(
            ) + history.timestamp.values.astype('datetime64[ms]').astype('datetime64[us]'), inplace=True)
            history.sort_index(inplace=True)
            history.reset_index(inplace=True)
            history.drop('timestamp', 1, inplace=True)
            history.columns = ['timestamp', 'group', 'label']
            history['id'] = history['timestamp'].apply(
                lambda x: pd.to_datetime(x).isoformat()).values
            self.nodes = history[['id', 'label', 'group']
                                 ].to_dict(orient='records')
            sources = history['id'][0:-1].values
            targets = history['id'][1:].values
            durations = history['timestamp'].diff()[1::]
            edgesList = list(zip(sources, targets, durations))
            self.edges = [dict(
                {'from': x[0], 'to': x[1], 'label': x[2].to_pytimedelta()}) for x in edgesList]

    def get(self):
        return {'id': self.id,  'nodes': self.nodes, 'edges': self.edges}
