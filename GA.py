import random
import numpy as np
from queryParser import *
import psycopg2
from moz_sql_parser import parse
from moz_sql_parser import format


# Enter here the percent of top-grated individuals to be retained for the next generation (range 0-1)
GRADED_RETAIN_PERCENT = 0.5
 
# Enter here the chance for a non top-grated individual to be retained for the next generation (range 0-1)
CHANCE_RETAIN_NONGRATED = 0.2
 
# Number of individual in the population
POPULATION_COUNT = 10
 
# Maximum number of generation before stopping the script
GENERATION_COUNT_MAX = 3
 
#Number of top-grated individuals to be retained for the next generation
GRADED_INDIVIDUAL_RETAIN_COUNT = int(POPULATION_COUNT * GRADED_RETAIN_PERCENT)
instructions=0
def set_generations(val):
    global GENERATION_COUNT_MAX
    GENERATION_COUNT_MAX=val



def get_random_population(Relations):
    """ Create a new random population, made of `POPULATION_COUNT` individual. """
    return [get_random_state(Relations) for _ in range(POPULATION_COUNT)]

 
"""""def average_population_cost(population,parsed_query):
   Return the average fitness of all individual in the population
    total = 0
    for individual in population:
        total += get_cost(individual,mode,parsed_query)
    return total / POPULATION_COUNT"""
  
def grade_population(population,cursor,parsed_query):
    """ Grade the population. Return a list of tuple (individual, fitness) sorted from most graded to less graded. """
    global instructions
    graded_individual = []
    for individual in population:
        instructions+=1
        graded_individual.append((individual, get_energy(listToQuery(individual,get_indice(individual),parsed_query),cursor)))
    return sorted(graded_individual, key=lambda x: x[1], reverse=False)



def get_local_min(sorted_population):
    min=100000000
    for state,cost in sorted_population:
        if cost<min :
            min=cost
            
    return min    



def evolve_population(sorted_population):
    """ Make the given population evolving to his next generation. """
  
    # Get individuals sorted by grade (top first), the average cost 
    #average_cost = 0
    graded_population = []
    for individual, fitness in sorted_population:
        #average_cost += fitness
        graded_population.append(individual)
    #average_cost /= POPULATION_COUNT
        
    # Filter the top graded individuals
    parents = graded_population[:GRADED_INDIVIDUAL_RETAIN_COUNT]
   
 
    # Randomly add other individuals to promote genetic diversity
    for individual in graded_population[GRADED_INDIVIDUAL_RETAIN_COUNT:]:
        if random.uniform(0, 1) < CHANCE_RETAIN_NONGRATED:
            parents.append(individual)
    
   
    # Crossover parents to create children
    ind_len=len(parents[1])
    parents_len = len(parents)
    desired_len = POPULATION_COUNT - parents_len
    children = []
    while len(children) < desired_len:
        parent=random.sample(parents, 1)[0]
        child=move(parent)
        children.append(child)
    
    # The next generation is ready
    parents.extend(children)

    return parents

def Genetic_algorithm(input,cursor):
    global instructions
    joinedTables ,parsed_query,alias=queryParser(input)
    joinedTables.remove(FACT)
    #generate the initial population
    population = get_random_population(joinedTables)
    #population=[['lineorder', 'part', 'customer', 'date', 'supplier'], ['lineorder', 'customer', 'supplier', 'part', 'date'], ['lineorder', 'date', 'supplier', 'part', 'customer'], ['supplier', 'lineorder', 'customer', 'part', 'date'], ['lineorder', 'date', 'customer', 'supplier', 'part']]
    #print('Initial population',population)
    
    i = 0
    #costs_avg = []
    #locals_min=[]
    #Average cost of the initial population
    #average_cost = average_population_cost(population,mode,parsed_query)
    #costs_avg.append(average_cost)

    # Make the population evolve
    while  i < GENERATION_COUNT_MAX:
        # grade population
        sorted_population=grade_population(population,cursor,parsed_query)
        #local_min_state=get_local_min(sorted_population)
        #locals_min.append(local_min_state)
        population = evolve_population(sorted_population)
        #costs_avg.append(average_cost)
        i += 1

    min_state=grade_population(population,cursor,parsed_query)[0]
            
    return min_state,instructions

 

   
