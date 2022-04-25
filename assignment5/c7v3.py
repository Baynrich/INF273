from operator import indexOf
from utils import *
from nbors import *
from methods import *
import time


def run_problem(problem, initial_solution):
    best_sol, best_sol_cost = alns(initial_solution, problem)
    return best_sol, best_sol_cost

problem = load_problem('./Call_7_Vehicle_3.txt')
init_sol = [0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7]

init_cost = cost_function(init_sol, problem)
sols_iter = []
costs_iter = []

start_time = time.time()
for i in range(1):
    sols, costs = run_problem(problem, init_sol)
    sols_iter.append(sols)
    costs_iter.append(costs)
end_time = time.time()

reassign_all_calls(init_sol, )
