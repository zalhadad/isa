import pandas as pd
import numpy as np
import json
import ast

import isa2api.database as db


class Sessions():
    
    def __init__(self,params):
        params.setdefault('offset', (params.page - 1 ) * params.per_page  )
        sql="SELECT * FROM sessions WHERE server = %(server)s AND timestamp::date between %(fromDate)s::date AND %(toDate)s::date AND timestamp between %(fromDate)s AND %(toDate)s "
        if params.id != None:
            sql += ' AND id LIKE %(id)s'        
        if params.caller != None:
            sql += ' AND caller=%(caller)s'        
        if params.called != None:
            sql += ' AND called=%(called)s'           
        sql += ' ORDER BY ' +  params.get('sort') + ' ' + params.get('order') + ' LIMIT %(per_page)s OFFSET %(offset)s ' 
        sql2="SELECT count(*) FROM sessions WHERE server = %(server)s AND timestamp::date between %(fromDate)s::date AND %(toDate)s::date AND timestamp between %(fromDate)s AND %(toDate)s "
        if params.id != None:
            sql2 += ' AND id LIKE %(id)s'        
        if params.caller != None:
            sql2 += ' AND caller=%(caller)s'        
        if params.called != None:
            sql2 += ' AND called=%(called)s'        
        cursor = db.connection.cursor()
        try:
            cursor.execute(sql2,params)
            self.total = cursor.fetchone()['count']
            cursor.close()
        except:
            self.total = 0
            db.connection.rollback()
        self.data = pd.read_sql(sql,db.connection,params=params)
    
    def get(self):
        return json.loads(self.data.to_json(orient='records',date_format='iso'))


    def __repr__(self):
        return self.data.to_json(orient='records')


class GlobalGraph():
    
    def __init__(self,params):
        sql="SELECT h.timestamp,h.node,h.session FROM sessions_history h inner join sessions s on h.session = s.id"
        sql += " WHERE s.server = %(server)s AND s.timestamp::date between %(fromDate)s::date AND %(toDate)s::date AND s.timestamp between %(fromDate)s AND %(toDate)s AND (node<> '') ORDER BY h.session,h.timestamp"       
        history = pd.read_sql(sql,db.connection,params=params)
        fromNodes = history.groupby('session').apply(lambda x : pd.Series(['BEGIN_NODE'] + list(x.node.values)))
        toNodes = history.groupby('session').apply(lambda x : pd.Series(list(x.node.values) + ['END_NODE']))
        edges = pd.DataFrame(list(zip(fromNodes.values,toNodes.values))).rename(columns={ 0: 'from',1:'to'})
        self.edges = (edges.groupby(['from','to']).size() / history.session.unique().size).reset_index().rename(columns={ 0: 'value'})
        float_formatter = lambda x: "%.2f%%" % x
        self.edges['label'] = (self.edges['value']*100).apply(float_formatter)
        self.edges = json.loads(self.edges.to_json(orient='records'))
        nodes = history.node.unique()
        nodes = pd.DataFrame({"id" : nodes, "label" : nodes ,"group" : "node"})
        nodes = nodes.append([{"label" : "BEGIN","group" : "BEGIN","id" : "BEGIN_NODE"}, {"label" : "END","group" : "END","id" : "END_NODE"}])
        self.nodes = json.loads(nodes.to_json(orient='records'))
    def get(self):
        return {'nodes' : self.nodes , 'edges' : self.edges}


    def __repr__(self):
        return self.data.to_json(orient='records')


class Paths():
    
    def __init__(self,params):
        
        sql="SELECT h.timestamp,h.node,h.session FROM sessions_history h inner join sessions s on h.session = s.id"
        sql += " WHERE s.server = %(server)s AND s.timestamp::date between %(fromDate)s::date AND %(toDate)s::date AND s.timestamp between %(fromDate)s AND %(toDate)s AND (node<> '') ORDER BY h.session,h.timestamp"       
        history = pd.read_sql(sql,db.connection,params=params)



        history['nId'] = history['node'] + history.groupby(['node','session']).cumcount().astype(str)

        from_nodes = history.groupby('session').apply(lambda x : pd.Series(['BEGIN_NODE'] + list(x.nId.values)))
        to_nodes = history.groupby('session').apply(lambda x : pd.Series(list(x.nId.values) + ['END_NODE']))
        edges = pd.DataFrame(list(zip(from_nodes.values,to_nodes.values))).rename(columns={ 0: 'from',1:'to'})


        parcours = pd.DataFrame(history.groupby('session').apply(lambda x :str(['BEGIN_NODE'] + list(x['nId']) + ['END_NODE'] ))).rename(columns={ 0: 'parcours'})
        n_parcours = parcours.groupby('parcours').size().nlargest(params.get('limit'))
        p = [ast.literal_eval(x) for x in n_parcours.index]
        c = [list(zip(x[0:-1], x[1:])) for x in p ]
        c = [item for sublist in c for item in sublist]
        b = pd.DataFrame(c).rename(columns={0 : 'from',1:'to'})

        e = (edges.merge(b.drop_duplicates(),how='right',on=['from','to']).groupby(['from','to']).size() / history.session.unique().size).reset_index().rename(columns={ 0: 'value'})

        float_formatter = lambda x: "%.2f%%" % x
        e['label'] = (e['value']*100).apply(float_formatter)
        self.edges = json.loads(e.to_json(orient='records'))
        nodes = history.merge(pd.DataFrame(pd.melt(b,value_vars=['from','to']).value.unique()).rename(columns={0 : 'nId'}),on='nId',how='inner')[['nId','node']].rename(columns={'nId':'id','node':'label'})
        nodes['group'] = 'node'
        nodes = nodes.append([{"label" : "BEGIN","group" : "BEGIN","id" : "BEGIN_NODE"}, {"label" : "END","group" : "END","id" : "END_NODE"}]).drop_duplicates('id')
        self.nodes = json.loads(nodes.to_json(orient='records'))
    
    def get(self):

        return {'nodes' : self.nodes , 'edges' : self.edges}

    def __repr__(self):
        return self.data.to_json(orient='records')


class Session():
    
    def __init__(self,id):
        try:
            sql = 'select * from sessions WHERE id=%(id)s'
            cursor = db.connection.cursor()
            cursor.execute(sql,{'id': id})
            self.session = cursor.fetchone()
            cursor.close()
        except:
            db.connection.rollback()
    def get(self):
        return self.session


class History():
    
    def __init__(self,id,info):
        self.id = id
        sql = "SELECT timestamp,node,info FROM sessions_history WHERE session=%(id)s AND (node <> '' "
        if info:
            sql += "OR (info <> '' AND info <> 'endOfWavFile')"
        sql += " )  ORDER BY timestamp"
        history = pd.read_sql(sql,db.connection,params={'id' : self.id})
        history = pd.melt(history,id_vars='timestamp',value_vars=['node','info'],var_name='type',value_name='node').replace('',np.nan).dropna()
        history.set_index(history.groupby(history.timestamp.values.astype('datetime64[ms]')).cumcount() + history.timestamp.values.astype('datetime64[ms]').astype('datetime64[us]'),inplace=True)
        history.sort_index(inplace=True)
        history.reset_index(inplace=True)
        history.drop('timestamp',1,inplace=True)
        history.columns =['timestamp', 'group', 'label']
        history['id'] = history['timestamp'].apply(lambda x : pd.to_datetime(x).isoformat()).values
        self.nodes = history[['id', 'label', 'group']].to_dict(orient='records')
        sources = history['id'][0:-1].values
        targets = history['id'][1:].values
        durations = history['timestamp'].diff()[1::]
        edgesList = list(zip(sources, targets, durations))
        self.edges = [dict({'from' : x[0], 'to' : x[1], 'label' : x[2].to_pytimedelta()}) for x in edgesList]
    def get(self):
        return { 'id' : self.id,  'nodes' : self.nodes , 'edges' : self.edges}