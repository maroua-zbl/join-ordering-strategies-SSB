from pylab import *
import matplotlib.pyplot as plt
import random
import numpy as np
from queryParser import *
import psycopg2
import time

# input="SELECT SUM(l.lo_extendedprice * l.lo_discount) AS revenue FROM lineorder l , date d WHERE l.lo_orderdate = d.d_datekey AND d.d_year = 1993 AND l.lo_discount BETWEEN 1 AND 3 AND l.lo_quantity < 25;"


tablesWithSel={}
sortedTables=[]
FACT="lineorder"
def init():
    global tablesWithSel
    tablesWithSel={}
    global sortedTables
    sortedTables=[]
def FanOut(input,cursor,f):
    init()
    state=[]
    solution={}
    query="select count(*) from "+FACT
    print("query",query)
    cursor.execute(query)
    factCar=cursor.fetchall()[0][0]
    # calculer les cardinalités des tables
    joinedTables ,parsed_query , alias=queryParser(input)
    print(alias)
    joinedTables.remove(FACT)
    print(joinedTables)
    tables=get_tableWithSelectivity(parsed_query)
    if 'l'in tables:
        del(tables['l'])
    
    for key in tables.keys():
        json={'select': {'value': {'count': '*'}},'from':  [{'value': 'lineorder', 'name': 'l'},{'left join': {'name':key,'value':alias[key]}, 'on': {'eq': get_joinedClause(alias[key])}}]}
        if len(tables[key])==1:
            json['where']=tables[key][0]
        else:
            json['where']={'and':tables[key]}
        query=format(json)
        print("query",query)
        cursor.execute(query)
        tablesWithSel[alias[key]]=cursor.fetchall()[0][0]/factCar
    print("tablewithsel",tablesWithSel)
    if(len(joinedTables)>len(tablesWithSel)):
        for t in joinedTables:
            if t not in tablesWithSel:
                query="select count(*) from lineorder l left join "+t+" as "+get_key(t,alias)+" on "+get_joinedClause(t)[0]+" = "+get_joinedClause(t)[1]
                print("query",query)
                cursor.execute(query)
                tablesWithSel[t]=cursor.fetchall()[0][0]/factCar
                
    
    sortedTables={k: v for k, v in sorted(tablesWithSel.items(), key=lambda item: item[1])}
    state=list(sortedTables.keys())
    state.insert(1,FACT)
    print(state)
    solution["query"]=listToQuery(state,get_indice(state),parsed_query)
    if f==0:
        solution["runTime"]=get_runTime(solution["query"],cursor)
        solution["estimatedCost"]=get_cost(solution["query"],cursor)
        time.sleep(5)
        solution["energy"]=get_energy(solution["query"],cursor)
        
    elif f==1:
        solution["estimatedCost"]=get_cost(solution["query"],cursor)
    elif f==2:
        solution["runTime"]=get_runTime(solution["query"],cursor)
    else:
        time.sleep(5)
        solution["energy"]=get_energy(solution["query"],cursor)
        
    return solution

