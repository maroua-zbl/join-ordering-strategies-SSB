from pylab import *
import matplotlib.pyplot as plt
import random
import numpy as np
from queryParser import *
import psycopg2
import time

# input="SELECT SUM(l.lo_extendedprice * l.lo_discount) AS revenue FROM lineorder l , date d WHERE l.lo_orderdate = d.d_datekey AND d.d_year = 1993 AND l.lo_discount BETWEEN 1 AND 3 AND l.lo_quantity < 25;"
dimentions={"date":0,"supplier":0,"customer":0,"part":0}
tablesWithSel={}
sortedTables=[]
FACT="lineorder"

def init():
    global dimentions
    dimentions={"date":0,"supplier":0,"customer":0,"part":0}
    global tablesWithSel
    tablesWithSel={}
    global sortedTables
    sortedTables=[]
    
def MinSelectivity(input,cursor,f):
    init()
    print("tablesWith",tablesWithSel)
    state=[]
    solution={}
    joinedTables ,parsed_query , alias=queryParser(input)
    joinedTables.remove(FACT)
    tables=get_tableWithSelectivity(parsed_query)
    if 'l'in tables:
        del(tables['l'])
    
    #calculer cardinalités des dimentions
    for t in dimentions:
        query="select count(*) from "+t
        cursor.execute(query)
        dimentions[t]=cursor.fetchall()[0][0]
    
    # calculer selectivités des dimentions
    for key in tables.keys():
        json={'select': {'value': {'count': '*'}},'from':{'value':alias[key],'name':key}}
        if len(tables[key])==1:
            json['where']=tables[key][0]
        else:
            json['where']={'and':tables[key]}
        query=format(json)
        cursor.execute(query)
        tablesWithSel[alias[key]]=cursor.fetchall()[0][0]
        
    # ajouter les tables sans selectivité
    if(len(joinedTables)>len(tablesWithSel)):
        for t in joinedTables:
            print("tt",t)
            if t not in tablesWithSel:
                tablesWithSel[t]=dimentions[t]
    print("gggggggggggg",tablesWithSel)
    sortedTables={k: v for k, v in sorted(tablesWithSel.items(), key=lambda item: item[1])}
    state=list(sortedTables.keys())
    state.insert(1,FACT)
    print("state",state)
    
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