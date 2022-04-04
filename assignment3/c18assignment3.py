from pdp_utils import *
from nbors import *
from printer import *
from methods import *
from tqdm import tqdm
import time
import random
import numpy as np
n = 1000



def run_problem(problem, initial_solution):
    methods = [localsearch, annealing]
    operators = [oneopt_operator_nborhood, twoopt_operator_nborhood, threeopt_operator_nborhood]
    sols = []
    costs = []
    for method in methods:
        for operator in operators:
            best_sol, best_sol_cost = method(initial_solution, operator, problem)
            sols.append(best_sol)
            costs.append(best_sol_cost)
    return sols, costs

problem = load_problem('./Call_18_Vehicle_5.txt')
init_sol = [0, 0, 0, 0, 0, 9, 9, 7, 7, 13, 13, 6, 6, 11, 11, 16, 16, 8, 8, 10, 10, 4, 4, 1, 1, 17, 17, 2, 2, 15, 15, 3, 3, 12, 12, 18, 18, 14, 14, 5, 5]
init_cost = cost_function(init_sol, problem)
sols_iter = []
costs_iter = []
for i in range(2):
    sols, costs = run_problem(problem, init_sol)
    sols_iter.append(sols)
    costs_iter.append(costs)

printer(costs_iter, sols_iter)