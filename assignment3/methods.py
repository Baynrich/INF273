from utils import *
from tqdm import tqdm
import random
import numpy as np
from nbors import oneopt_operator_nborhood, twoopt_operator_nborhood, threeopt_operator_nborhood
import time

n = 10000

def run_problem(problem, initial_solution):
    methods = [localsearch, annealing]
    operators = [oneopt_operator_nborhood, twoopt_operator_nborhood, threeopt_operator_nborhood]
    sols = []
    costs = []
    times = []
    for method in methods:
        for operator in operators:
            cur_m_o_sols = []
            cur_m_o_costs = []
            cur_m_o_times = []
            for i in range(10):
                st = time.time()
                best_sol, best_sol_cost = method(initial_solution, operator, problem)
                et = time.time()
                cur_m_o_sols.append(best_sol)
                cur_m_o_costs.append(best_sol_cost)
                cur_m_o_times.append(et - st)
            sols.append(cur_m_o_sols)
            costs.append(cur_m_o_costs)
            times.append(cur_m_o_times)
    return sols, costs, times


def localsearch(init_sol, operator, prob):
    best_sol = init_sol
    best_sol_cost = cost_function(best_sol, prob)
    for i in tqdm(range(n)):
        nbor = operator(best_sol, prob)
        nbor_cost = cost_function(nbor, prob)
        if(nbor_cost < best_sol_cost):
            best_sol_cost = nbor_cost
            best_sol = nbor
    return best_sol, best_sol_cost


def annealing(init_sol, operator, prob):
    best_sol = init_sol
    best_sol_cost = cost_function(best_sol, prob)
    global_best_sol = init_sol
    global_best_cost = best_sol_cost
    delta_es = [0]

    for i in tqdm(range(100)):
        nbor = operator(best_sol, prob)
        nbor_cost = cost_function(nbor, prob)
        delta_e = nbor_cost - best_sol_cost
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
        
        nbor = operator(best_sol, prob)
        nbor_cost = cost_function(nbor, prob)
        delta_e = nbor_cost - best_sol_cost

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