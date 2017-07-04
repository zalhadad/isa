import pandas as pd
import numpy as np
import json

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
        sql += " WHERE s.server = %(server)s AND h.timestamp::date between %(fromDate)s::date AND %(toDate)s::date AND h.timestamp between %(fromDate)s AND %(toDate)s AND (node<> '') "       
        history = pd.read_sql(sql,db.connection,params=params)
        fromNodes = history.groupby('session').apply(lambda x : x[0:-1])
        toNodes = history.groupby('session').apply(lambda x : x[1:])
        edges = pd.DataFrame(list(zip(fromNodes.node.values,toNodes.node.values))).rename(columns={ 0: 'from',1:'to'})
        self.edges = ((edges.groupby(['from','to']).size() / edges.index.size)).reset_index().rename(columns={ 0: 'value'})
        float_formatter = lambda x: "%.2f%%" % x
        self.edges['label'] = (self.edges['value']*100).apply(float_formatter)
        self.edges = json.loads(self.edges.to_json(orient='records'))
        nodes = history.node.unique()
        self.nodes = json.loads(pd.DataFrame({"id" : nodes, "label" : nodes ,"group" : "node"}).to_json(orient='records'))
    def get(self):
        return {'nodes' : self.nodes , 'edges' : self.edges}


    def __repr__(self):
        return self.data.to_json(orient='records')


class Paths():
    
    def __init__(self,params):
        """
        sql="SELECT h.timestamp,h.node,h.session FROM sessions_history h inner join sessions s on h.session = s.id"
        sql += " WHERE s.server = %(server)s AND h.timestamp::date between %(fromDate)s::date AND %(toDate)s::date AND h.timestamp between %(fromDate)s AND %(toDate)s AND (node<> '') "       
        history = pd.read_sql(sql,db.connection,params=params)
        h2 = history.groupby('session').apply(lambda x : x.node.cumsum()).reset_index().set_index('timestamp')
        parcours = pd.DataFrame(history.groupby('session').apply(lambda x :str(list(x.node)))).rename(columns={ 0: 'parcours'})
        n_parcours = parcours.groupby('parcours').size().nlargest(10)

        p = [ast.literal_eval(x) for x in n_parcours.index]
        c = [list(zip(x[0:-1], x[1:])) for x in p ]
        c = [item for sublist in c for item in sublist]



        fromNodes = history.groupby('session').apply(lambda x : x[0:-1])
        toNodes = history.groupby('session').apply(lambda x : x[1:])
        w= pd.DataFrame(list(zip(fromNodes.node.values,toNodes.node.values))).rename(columns={ 0: 'from',1:'to'})


        start = t.time()
        b = history.groupby('session').apply(lambda x : list(zip(x[0:-1].node.values,x[1:].node.values)))
        b = pd.DataFrame([item for sublist in b for item in sublist]).rename(columns={0 : 'from',1:'to'})



        self.edges = (w.merge(a,how='right').groupby(['from','to']).size() / w.index.size).reset_index()

        float_formatter = lambda x: "%.2f%%" % x
        self.edges['label'] = (self.edges['value']*100).apply(float_formatter)
        self.edges = json.loads(self.edges.to_json(orient='records'))
        nodes = history.node.unique()
        self.nodes = json.loads(pd.DataFrame({"id" : nodes, "label" : nodes ,"group" : "node"}).to_json(orient='records'))
        """
    def get(self):

       # return {'nodes' : self.nodes , 'edges' : self.edges}
        import json
        import os
        with open(os.path.join(os.path.dirname(__file__), 'test.json')) as json_data:
            return json.load(json_data)


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