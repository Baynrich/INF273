from math import sqrt
from nbors import assign_retireds, reassign_call, reorder_vehicle_calls
from utils import cost_function, feasibility_check 
from tqdm import tqdm
import random
import numpy as np



n = 25000
n_operators = 3
new_sol_score = 1
improvement_score = 2
best_score = 6


def alns(init_sol, prob):
    best_sol = init_sol
    best_sol_cost = cost_function(best_sol, prob)
    global_best_sol = init_sol
    global_best_cost = best_sol_cost
    delta_es = np.array([1])
    T = 0
    alpha = 0

    visited = np.array([])
    operator_probabilities = np.array([1 / n_operators] * n_operators)
    operator_scores = np.array([1] * n_operators)
    operator_decay = np.ones((3, 3))


    feasibles = 0
    posdelts = 0

    n_since_last_better = 0
    last_better_sol = init_sol


    
    for i in tqdm(range(n)):
        
        if i == 100:
            T = (sum(delta_es) / len(delta_es)) / np.log(0.8)
            alpha = np.power(0.1 / T, 1 / n)

        # If we get stuck on the same solution, jump into some new solution and try from there.
        if n_since_last_better >= 100:
            last_better_cost = cost_function(last_better_sol, prob)
            best_sol = assign_all_retireds(init_sol, prob["n_vehicles"], prob["n_calls"])



        operator, nbor = select_nbor_op(best_sol, prob, operator_probabilities)
        nbor_cost = cost_function(nbor, prob)
        delta_e = nbor_cost - best_sol_cost

        if feasibility_check(nbor, prob):
            if not nbor in visited:
                operator_scores[operator] += (new_sol_score / operator_decay[operator, 0])
                operator_decay[operator, 0] += 0.001
                visited = np.append(visited, nbor)

            feasibles += 1
            if delta_e > 0:
                posdelts += 1
                n_since_last_better = 0
                best_sol = nbor
                best_sol_cost = nbor_cost
                operator_scores[operator] += (improvement_score / operator_decay[operator, 1])
                operator_decay[operator, 1] += 0.001

                if best_sol_cost < global_best_cost:
                    global_best_cost = best_sol_cost
                    global_best_sol = best_sol
                    operator_scores[operator] += (best_score /  operator_decay[operator, 2])
                    operator_decay[operator, 2] += 0.001

            else:
                n_since_last_better += 1
                if(i < 100):
                    delta_es = np.append(delta_es, delta_e)
                randval = random.random()

                threshold = 0.8 if i < 100 else np.exp(-delta_e / T)

                if randval < threshold:
                    best_sol_cost = nbor_cost
                    best_sol = nbor
        if i >= 100:
            T = T * alpha
       
        # Update operator probabilities based on achieved scores.
        if i % 100 == 0:
            opsum = sum(operator_scores)
            for j in range(len(operator_probabilities)):
                operator_probabilities[j] = operator_scores[j] / opsum
            operator_scores = np.array([1] * n_operators)
                
            
    print(operator_probabilities)
    print("feasibles", feasibles)
    print("posdelts", posdelts)
    return global_best_sol, global_best_cost


def select_nbor_op(sol, prob, operator_probabilities):
    choice = random.random()
    if choice < operator_probabilities[0] / sum(operator_probabilities):
        operator = 0
        nbor = reassign_call(sol, prob["n_vehicles"], prob["n_calls"])
    elif choice >= operator_probabilities[0]  and choice < ( operator_probabilities[0] + operator_probabilities[1]):
        operator = 1
        nbor = reorder_vehicle_calls(sol, prob["n_vehicles"], prob["n_calls"])
    else:
        operator = 2
        nbor = assign_retireds(sol, prob["n_vehicles"], prob["n_calls"], prob)
    return operator, nbor