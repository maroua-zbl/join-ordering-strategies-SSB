from pylab import *
import matplotlib.pyplot as plt
import random
import numpy as np
from queryParser import *
import psycopg2
from moz_sql_parser import parse
from moz_sql_parser import format



TEMPERATURE=7
TEMP_REDUCTION_FACTOR = 0.5
STEPS_TO_EQUILIBRIUM = 10
INSTRUCTIONS=0
def set_temperature(v):
    global TEMPERATURE
    TEMPERATURE=v

def acc_probality(old,new):
    # probality to accept the new state even if new_cost>old_cost
    global TEMPERATURE
    return np.exp( (old - new) /TEMPERATURE )

def is_acceptable(new_cost,old_cost):
    p = random.random()
    if new_cost<old_cost:
        return True
    elif acc_probality(old_cost, new_cost) > p:
        return True
    else:
        return False    
        
def reduce_temperature():
    global TEMPERATURE
    TEMPERATURE *= TEMP_REDUCTION_FACTOR
    
def is_equilibrium():
    global STEPS_TO_EQUILIBRIUM
    if STEPS_TO_EQUILIBRIUM == 0:
        STEPS_TO_EQUILIBRIUM = 10
        return True
    else:
        STEPS_TO_EQUILIBRIUM -= 1
        return False

def is_frozen():
    if TEMPERATURE < 0.1:
        return True
    else:
        return False
     
def simulated_annealing(input,cursor):
    
    #variables initialization
 
    global INSTRUCTIONS
    joinedTables ,parsed_query,alias=queryParser(input)
    joinedTables.remove(FACT)
    
    old_state=get_random_state(joinedTables)
    #print("old state",old_state)
    #old_state=['lineorder', 'part', 'supplier', 'date', 'customer']
    old_cost=get_runTime(listToQuery(old_state,get_indice(old_state),parsed_query),cursor)
    global_min=old_cost
    min_state=(listToQuery(old_state,get_indice(old_state),parsed_query),old_cost)
    
    i=0
    j=0
    
    while not is_frozen() :
        #print("tempeeeeeeeeeeeeeeeeeeeeeeerature" , TEMPERATURE)
        while not is_equilibrium():
                INSTRUCTIONS+=1
                print(STEPS_TO_EQUILIBRIUM)
                #get new state and new cost 
                new_state=move(old_state)
                new_cost= get_runTime(listToQuery(new_state,get_indice(new_state),parsed_query),cursor)
                #print("new state :",new_state, 'with cost :', new_cost)
          
                if (is_acceptable(new_cost,old_cost)):
                    old_state=new_state
                 #update global_min
                    if new_cost<global_min:
                        global_min=new_cost
                        min_state=(listToQuery(new_state,get_indice(new_state),parsed_query),new_cost)
                   
        reduce_temperature()
    
    
    
    
    return min_state,INSTRUCTIONS
    

   
 

   
