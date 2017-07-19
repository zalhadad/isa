import pandas as pd
import numpy as np
import json
import ast

from isa2api.database import db, where
from isa2api.business.graphviz import Graphviz


class GlobalGraph():

    def __init__(self, params):
        sql = "SELECT h.timestamp,h.node,h.session FROM sessions_history h inner join sessions s on h.session = s.id"
        sql += where(params, "h") + \
            " AND (node<> '') ORDER BY h.session,h.timestamp"
        history = pd.read_sql(sql, db, params=params)
        self.edges = []
        self.nodes = []
        if history.size > 0:
            fromNodes = history.groupby('session').apply(
                lambda x: pd.Series(['BEGIN_NODE'] + list(x.node.values)))
            toNodes = history.groupby('session').apply(
                lambda x: pd.Series(list(x.node.values) + ['END_NODE']))
            edges = pd.DataFrame(list(zip(fromNodes.values, toNodes.values))).rename(
                columns={0: 'from', 1: 'to'})
            self.edges = (edges.groupby(['from', 'to']).size(
            ) / history.session.unique().size).reset_index().rename(columns={0: 'value'})

            def float_formatter(x): return "%.2f%%" % x
            self.edges['label'] = (self.edges['value'] *
                                   100).apply(float_formatter)
            self.edges = json.loads(self.edges.to_json(orient='records'))
            nodes = history.node.unique()
            nodes = pd.DataFrame(
                {"id": nodes, "label": nodes, "group": "node"})
            nodes = nodes.append([{"label": "BEGIN", "group": "BEGIN", "id": "BEGIN_NODE"}, {
                "label": "END", "group": "END", "id": "END_NODE"}])
            self.nodes = json.loads(nodes.to_json(orient='records'))

    def get(self):
        return {'nodes': self.nodes, 'edges': self.edges}

    def __repr__(self):
        return self.history.to_json(orient='records')


class Paths():

    def __init__(self, params):

        sql = "SELECT h.timestamp,h.node,h.session FROM sessions_history h inner join sessions s on h.session = s.id"
        sql += where(params, 'h') + \
            " AND (node<> '') ORDER BY h.session,h.timestamp"
        history = pd.read_sql(sql, db, params=params)
        self.edges = []
        self.nodes = []
        if history.size > 0:
            history['nId'] = history['node'] + \
                history.groupby(['node', 'session']).cumcount().astype(str)

            from_nodes = history.groupby('session').apply(
                lambda x: pd.Series(['BEGIN_NODE'] + list(x.nId.values)))
            to_nodes = history.groupby('session').apply(
                lambda x: pd.Series(list(x.nId.values) + ['END_NODE']))
            edges = pd.DataFrame(list(zip(from_nodes.values, to_nodes.values))).rename(
                columns={0: 'from', 1: 'to'})

            parcours = pd.DataFrame(history.groupby('session').apply(lambda x: str(
                ['BEGIN_NODE'] + list(x['nId']) + ['END_NODE']))).rename(columns={0: 'parcours'})
            n_parcours = parcours.groupby(
                'parcours').size().nlargest(params.get('limit'))
            p = [ast.literal_eval(x) for x in n_parcours.index]
            c = [list(zip(x[0:-1], x[1:])) for x in p]
            c = [item for sublist in c for item in sublist]
            b = pd.DataFrame(c).rename(columns={0: 'from', 1: 'to'})

            e = (edges.merge(b.drop_duplicates(), how='right', on=['from', 'to']).groupby(
                ['from', 'to']).size() / history.session.unique().size).reset_index().rename(columns={0: 'value'})

            def float_formatter(x): return "%.2f%%" % x
            e['label'] = (e['value'] * 100).apply(float_formatter)
            self.edges = json.loads(e.to_json(orient='records'))
            nodes = history.merge(pd.DataFrame(pd.melt(b, value_vars=['from', 'to']).value.unique()).rename(
                columns={0: 'nId'}), on='nId', how='inner')[['nId', 'node']].rename(columns={'nId': 'id', 'node': 'label'})
            nodes['group'] = 'node'
            nodes = nodes.append([{"label": "BEGIN", "group": "BEGIN", "id": "BEGIN_NODE"}, {
                "label": "END", "group": "END", "id": "END_NODE"}]).drop_duplicates('id')
            self.nodes = json.loads(nodes.to_json(orient='records'))

    def get(self):
        return {'nodes': self.nodes, 'edges': self.edges}

    def svg(self):
        image = Graphviz({'nodes': self.nodes, 'edges': self.edges})
        return image.svg()
