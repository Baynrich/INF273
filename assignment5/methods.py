from nbors import assign_retireds, reassign_call, reorder_vehicle_calls, retire_calls, reassign_all
from utils import cost_function, feasibility_check 
from tqdm import tqdm
import random
import numpy as np
import time

n = 25000
N_OPERATORS = 4
NEW_SOL_SCORE = 2
NEW_IMPROVEMENT_SCORE = 1
NEW_BEST_SCORE = 6
DECAY_VALUE = 0.1

def handle_set_T_alpha(delta_es):
    T = (sum(delta_es) / len(delta_es)) / np.log(0.8)
    alpha = np.power(0.1 / T, 1 / n)
    return T, alpha


        


def alns(init_sol, prob):
    # Constants
    best_sol = init_sol
    best_sol_cost = cost_function(best_sol, prob)
    global_best_sol = init_sol
    global_best_cost = best_sol_cost
    delta_es = np.array([1])
    T = 0
    alpha = 0

    visited = np.array([])
    operator_probabilities = np.array([1 / N_OPERATORS] * N_OPERATORS)
    operator_scores = np.array([1] * N_OPERATORS)
    operator_decay = np.ones((N_OPERATORS, 3))
    opcounts = np.zeros(N_OPERATORS + 1)
    optimes = np.zeros(N_OPERATORS + 1)


    feasibles = 0
    posdelts = 0

    n_since_last_better = 0
    init_sol, costs = reassign_all(init_sol, prob)
    
    
    for i in tqdm(range(n)):
        
        if i == 100:
            T, alpha = handle_set_T_alpha(delta_es)

        # If we get stuck on the same solution, jump into some new solution and try from there.
        if n_since_last_better >= 25:
            st = time.time()
            best_sol, costs = reassign_all(init_sol, prob)
            et = time.time()
            opcounts[4] += 1
            optimes[4] += (et-st)

            n_since_last_better = 0

        st = time.time()
        operator, nbor, nbor_costs = select_nbor_op(best_sol, prob, operator_probabilities, costs)
        et = time.time()
        opcounts[operator] += 1
        optimes[operator] += (et-st)
        nbor_cost = cost_function(nbor, prob)
        delta_e = nbor_cost - best_sol_cost

        if feasibility_check(nbor, prob):
            if not nbor in visited:
                operator_scores[operator] += (NEW_SOL_SCORE / operator_decay[operator, 0])
                operator_decay[operator, 0] += DECAY_VALUE
                visited = np.append(visited, nbor)

            feasibles += 1
            if delta_e < 0:
                costs = nbor_costs
                posdelts += 1
                n_since_last_better = 0
                best_sol = nbor
                best_sol_cost = nbor_cost
                operator_scores[operator] += (NEW_IMPROVEMENT_SCORE / operator_decay[operator, 1])
                operator_decay[operator, 1] += 0.01

                if best_sol_cost < global_best_cost:
                    global_best_cost = best_sol_cost
                    global_best_sol = best_sol
                    operator_scores[operator] += (NEW_BEST_SCORE /  operator_decay[operator, 2])
                    operator_decay[operator, 2] += 0.01

            else:
                n_since_last_better += 1
                if(i < 100):
                    delta_es = np.append(delta_es, delta_e)
                randval = random.random()

                threshold = 0.8 if i < 100 else np.exp(-delta_e / T)

                if randval < threshold:
                    costs = nbor_costs
                    best_sol_cost = nbor_cost
                    best_sol = nbor
        if i >= 100:
            T = T * alpha
       
        # Update operator probabilities based on achieved scores.
        if i % 200 == 0:
            opsum = sum(operator_scores)
            for j in range(len(operator_probabilities)):
                operator_probabilities[j] = operator_scores[j] / opsum
            operator_scores = np.array([1] * N_OPERATORS)
            operator_decay = np.ones((N_OPERATORS, 3))
    print("n_since_last_better", n_since_last_better)
    print("opcounts", opcounts)
    print("optimes", optimes)

    return global_best_sol, global_best_cost


def select_nbor_op(sol, prob, operator_probabilities, costs):
    choice = random.random()
    if choice < operator_probabilities[0] / sum(operator_probabilities):
        operator = 0
        nbor = reassign_call(sol, prob["n_vehicles"], prob["n_calls"], costs)
    elif choice >= operator_probabilities[0]  and choice < ( operator_probabilities[0] + operator_probabilities[1]):
        operator = 1
        nbor = reorder_vehicle_calls(sol, prob["n_vehicles"], prob["n_calls"], costs)
    elif choice >= operator_probabilities[1] and choice < (operator_probabilities[0] + operator_probabilities[1] + operator_probabilities[2] ):
        operator = 2
        nbor = assign_retireds(sol, prob, costs)
    else:
        operator = 3
        nbor = retire_calls(sol, prob, costs)
    return operator, nbor