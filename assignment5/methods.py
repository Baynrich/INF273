from nbors import assign_all_retireds, reassign_call, reorder_vehicle_calls
from utils import cost_function, feasibility_check 
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
    delta_es = np.array([0])

    visited = np.array([])
    operator_scores = np.array([1 / n_operators] * n_operators)
    cooldown = np.linspace(0.8, 0.05, num=(n))
    feasibles = 0

    n_since_last_better = 0
    last_better_sol = init_sol
    
    for i in tqdm(range(n)):

        # If we get stuck on the same solution, jump into some new solution and try from there.
        if n_since_last_better >= 50:
            last_better_cost = cost_function(last_better_sol, prob)
            # Experiment didnt work, go back to better sol
            if last_better_cost < best_sol_cost:
                best_sol = last_better_sol
                best_sol_cost = last_better_cost
            # Experiment did work but were stuck. Try something new.
            else:
                last_better_sol = best_sol
                best_sol = assign_all_retireds(init_sol)


        operator, nbor = select_nbor_op(best_sol, prob, operator_scores)
        nbor_cost = cost_function(nbor, prob)
        delta_e = nbor_cost - best_sol_cost



        if feasibility_check(nbor, prob):
            if not nbor in visited:
                operator_scores[operator] += new_sol_score
                visited = np.append(visited, nbor)

            feasibles += 1
            if delta_e > 0:
                n_since_last_better = 0
                best_sol = nbor
                best_sol_cost = nbor_cost
                operator_scores[operator] += improvement_score
                if best_sol_cost < global_best_cost:
                    global_best_cost = best_sol_cost
                    global_best_sol = best_sol
                    operator_scores[operator] += best_score
            else:
                n_since_last_better += 1
                delta_es = np.append(delta_es, delta_e)
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
        nbor = reassign_call(sol, prob["n_vehicles"], prob["n_calls"])
    elif choice >= operator_scores[0]  and choice < ( operator_scores[0] + operator_scores[1]):
        operator = 1
        nbor = reorder_vehicle_calls(sol, prob["n_vehicles"], prob["n_calls"])
    else:
        operator = 2
        nbor = assign_all_retireds(sol)
    return operator, nbor