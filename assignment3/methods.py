from utils import *
from tqdm import tqdm
import random
import numpy as np

n = 10000

def localsearch(init_sol, operator, prob):
    best_sol = init_sol
    best_sol_cost = cost_function(best_sol, prob)
    for i in tqdm(range(n)):
        best_nbor = None
        best_nbor_cost = float('inf')
        nbors = operator(best_sol)
        for nbor in nbors:
            feasibility, c = feasibility_check(nbor, prob)
            if feasibility:
                nbor_cost = cost_function(nbor, prob)
                if nbor_cost < best_nbor_cost:
                    best_nbor_cost = nbor_cost
                    best_nbor = nbor
        
        if best_nbor is not None and best_sol_cost > best_nbor_cost:
            best_sol = best_nbor
            best_sol_cost = best_nbor_cost
        if best_nbor is None or best_sol_cost < best_nbor_cost:
            print("Exiting early")
            # We've found local optima. Will not get better.
            break
    return best_sol, best_sol_cost


def annealing(init_sol, operator, prob):
    best_sol = init_sol
    best_sol_cost = cost_function(best_sol, prob)
    delta_es = [0]
    
    for i in tqdm(range(100)):
        best_nbor = None
        best_nbor_cost = float('inf')
        nbors = operator(best_sol)
        for nbor in nbors:
            feasibility, c = feasibility_check(nbor, prob)
            if feasibility:
                nbor_cost = cost_function(nbor, prob)
                if nbor_cost < best_nbor_cost:
                    best_nbor_cost = nbor_cost
                    best_nbor = nbor
                else:
                    randval = random.random()
                    if randval < 0.8:
                        best_nbor_cost = nbor_cost
                        best_nbor = nbor
        
        if best_nbor is not None:
            delta_es.append(best_sol_cost - best_nbor_cost)
            if best_sol_cost > best_nbor_cost:
                best_sol = best_nbor
                best_sol_cost = best_nbor_cost
    T = (sum(delta_es) / len(delta_es)) / np.log(0.8)
    alpha = np.power(0.1 / T, 1 / n)
    
    for i in tqdm(range(n - 100)):
        best_nbor = None
        best_nbor_cost = float('inf')
        nbors = operator(best_sol)
        for nbor in nbors:
            feasibility, c = feasibility_check(nbor, prob)
            if feasibility:
                nbor_cost = cost_function(nbor, prob)
                if nbor_cost < best_nbor_cost:
                    best_nbor_cost = nbor_cost
                    best_nbor = nbor
                else:
                    delta_e = nbor_cost - best_nbor_cost
                    randval = random.random()
                    if randval < np.exp(-delta_e / T):
                        best_nbor_cost = nbor_cost
                        best_nbor = nbor
        
        if best_nbor is not None:
            delta_es.append(best_nbor_cost - best_sol_cost)
            if best_sol_cost > best_nbor_cost:
                best_sol = best_nbor
                best_sol_cost = best_nbor_cost
        T = T * alpha
    return best_sol, best_sol_cost