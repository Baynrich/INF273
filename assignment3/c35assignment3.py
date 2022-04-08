from utils import *
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

problem = load_problem('./Call_35_Vehicle_7.txt')
init_sol = [0, 0, 0, 0, 0, 0, 0, 10, 10, 30, 30, 24, 24, 23, 23, 25, 25, 15, 15, 28, 28, 33, 33, 26, 26, 34, 34, 35, 35, 7, 7, 8, 8, 16, 16, 29, 29, 12, 12, 18, 18, 14, 14, 32, 32, 20, 20, 9, 9, 6, 6, 27, 27, 13, 13, 19, 19, 22, 22, 17, 17, 4, 4, 1, 1, 21, 21, 3, 3, 5, 5, 2, 2, 11, 11, 31, 31]
init_cost = cost_function(init_sol, problem)
sols_iter = []
costs_iter = []
for i in range(2):
    sols, costs = run_problem(problem, init_sol)
    sols_iter.append(sols)
    costs_iter.append(costs)

printer(costs_iter, sols_iter)