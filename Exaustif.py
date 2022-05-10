from pylab import *
import matplotlib.pyplot as plt
import random
import numpy as np
from queryParser import *
import psycopg2
import time

FACT="lineorder"
def solution_space(len):
    
    return 2*math.factorial(len)

def get_random_state(Relations):
    #Create a new random individual
    point=random.sample(Relations, len(Relations))
    p=np.random.randint(2)
    point.insert(p,FACT)
    return point

def get_all(Relations):
    all=set()
    card=solution_space(len(Relations))
    while(len(all)<card):
        point=get_random_state(Relations)
        all.add(tuple(point))
    return all
          
def Exaustif(input,cursor):
    state=()
    solution=()
    all=()
    solution_space=[]
    joinedTables ,parsed_query,alias=queryParser(input)
    print("joined tables",joinedTables)
    joinedTables.remove(FACT)
    all=get_all(joinedTables)
    all=list(all) 
    i=0
    for s in all:
          print(i)
          query=listToQuery(s,get_indice(s),parsed_query)
          state=(query,get_cost(query,cursor),s)
          solution_space.append(state)
             
    solution_space=sorted(solution_space, key=lambda x: x[1], reverse=False)
    solution=solution_space[0]
   
        
    return solution
            
    
    
    



   
