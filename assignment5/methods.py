from nbors import assign_all_retireds, reassign_call, reorder_vehicle_calls
from utils import *
from tqdm import tqdm
import random
import numpy as np

n = 25000
n_operators = 3
new_sol_score = 0.001
improvement_score = 0.1
best_score = 0.25



def alns(init_sol, prob):
    best_sol = init_sol
    best_sol_cost = cost_function(best_sol, prob)
    global_best_sol = init_sol
    global_best_cost = best_sol_cost
    delta_es = [0]

    visited = []
    operator_scores = [1 / n_operators] * n_operators
    cooldown = np.linspace(0.8, 0.05, num=(n))
    feasibles = 0
    
    for i in tqdm(range(n)):
        operator, nbor = select_nbor_op(best_sol, prob, operator_scores)
        nbor_cost = cost_function(nbor, prob)
        delta_e = nbor_cost - best_sol_cost


        if not nbor in visited:
            operator_scores[operator] += new_sol_score
            visited.append(nbor)

        if feasibility_check(nbor, prob):
            feasibles += 1
            if delta_e > 0:
                best_sol = nbor
                best_sol_cost = nbor_cost
                operator_scores[operator] += improvement_score
                if best_sol_cost < global_best_cost:
                    global_best_cost = best_sol_cost
                    global_best_sol = best_sol
                    operator_scores[operator] += best_score
            else:
                delta_es.append(delta_e)
                randval = random.random()
                if randval < cooldown[i]:
                    best_sol_cost = nbor_cost
                    best_sol = nbor
        # Regularize operator scores
        for j in range(len(operator_scores)):
            operator_scores[j] = operator_scores[j] / sum(operator_scores)
    print(operator_scores)
    print("feasibles", feasibles)
    return global_best_sol, global_best_cost


def select_nbor_op(sol, prob, operator_scores):
    choice = random.random()
    if choice < operator_scores[0] / sum(operator_scores):
        operator = 0
        nbor = reassign_call(sol, prob)
    elif choice >= operator_scores[0]  and choice < ( operator_scores[0] + operator_scores[1]):
        operator = 1
        nbor = reorder_vehicle_calls(sol, prob)
    else:
        operator = 2
        nbor = assign_all_retireds(sol, prob)
    return operator, nbor