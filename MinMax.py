from pylab import *
import matplotlib.pyplot as plt
import random
import numpy as np
from queryParser import *
import psycopg2
import time

# q1-1="SELECT SUM(l.lo_extendedprice * l.lo_discount) AS revenue FROM lineorder l , date d WHERE l.lo_orderdate = d.d_datekey AND d.d_year = 1993 AND l.lo_discount BETWEEN 1 AND 3 AND l.lo_quantity < 25;"
dimentions={"date":0,"supplier":0,"customer":0,"part":0}
sortedDimentions={}
FACT="lineorder"
def MinMax(input,cursor,f):
    state=[]
    solution={}
    joinedTables ,parsed_query,alias=queryParser(input)
    print("joined tables",joinedTables)
    for t in dimentions:
        query="select count(*) from "+t
        cursor.execute(query)
        dimentions[t]=cursor.fetchall()[0][0]
    sortedDimentions={k: v for k, v in sorted(dimentions.items(), key=lambda item: item[1])}
    for t in sortedDimentions:
        if t in joinedTables:
            state.append(t)
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
            
    
    
    



   
