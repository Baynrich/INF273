from nbors import assign_all_retireds, reassign_call, reorder_vehicle_calls
from utils import *
from tqdm import tqdm
import random
import numpy as np

n = 10000



def annealing(init_sol, prob):
    best_sol = init_sol
    best_sol_cost = cost_function(best_sol, prob)
    global_best_sol = init_sol
    global_best_cost = best_sol_cost
    delta_es = [0]
    for i in tqdm(range(100)):
        choice = random.randint(0, 2)
        if choice == 0:
            nbor = reassign_call(best_sol, prob)
        elif choice == 1:
            nbor = reorder_vehicle_calls(best_sol, prob)
        else:
            nbor = assign_all_retireds(best_sol, prob)

        nbor_cost = cost_function(nbor, prob)
        delta_e = nbor_cost - best_sol_cost

        if feasibility_check(nbor, prob):
            if delta_e > 0:
                best_sol = nbor
                best_sol_cost = nbor_cost
                if best_sol_cost < global_best_cost:
                    global_best_cost = best_sol_cost
                    global_best_sol = best_sol
            else:
                delta_es.append(delta_e)
                randval = random.random()
                if randval < 0.8:
                    best_sol_cost = nbor_cost
                    best_sol = nbor


    T = (sum(delta_es) / len(delta_es)) / np.log(0.8)
    alpha = np.power(0.1 / T, 1 / n)
    
    for i in tqdm(range(n - 100)):
        choice = random.randint(0, 2)
        if choice == 0:
            nbor = reassign_call(best_sol, prob)
        elif choice == 1:
            nbor = reorder_vehicle_calls(best_sol, prob)
        else:
            nbor = assign_all_retireds(best_sol, prob)

        nbor_cost = cost_function(nbor, prob)
        delta_e = nbor_cost - best_sol_cost

        if feasibility_check(nbor, prob):
            if delta_e > 0:
                best_sol = nbor
                best_sol_cost = nbor_cost
                if best_sol_cost < global_best_cost:
                    global_best_cost = best_sol_cost
                    global_best_sol = best_sol
            else:
                delta_es.append(delta_e)
                randval = random.random()
                if randval < np.exp(-delta_e / T):
                    best_sol_cost = nbor_cost
                    best_sol = nbor
        T = T * alpha
    return global_best_sol, global_best_cost