from operator import indexOf
from utils import *
from nbors import *
from methods import *
import numpy as np
import time



def run_problem(problem, initial_solution):
    best_sol, best_sol_cost = annealing(initial_solution, problem)
    return best_sol, best_sol_cost

problem = load_problem('./Call_35_Vehicle_7.txt')
init_sol = [0, 0, 0, 0, 0, 0, 0, 10, 10, 30, 30, 24, 24, 23, 23, 25, 25, 15, 15, 28, 28, 33, 33, 26, 26, 34, 34, 35, 35, 7, 7, 8, 8, 16, 16, 29, 29, 12, 12, 18, 18, 14, 14, 32, 32, 20, 20, 9, 9, 6, 6, 27, 27, 13, 13, 19, 19, 22, 22, 17, 17, 4, 4, 1, 1, 21, 21, 3, 3, 5, 5, 2, 2, 11, 11, 31, 31]

init_cost = cost_function(init_sol, problem)
sols_iter = []
costs_iter = []

start_time = time.time()
for i in range(10):
    sols, costs = run_problem(problem, init_sol)
    sols_iter.append(sols)
    costs_iter.append(costs)
end_time = time.time()

print("Initial objective:", init_cost)
print("Avg objective:", np.mean(costs_iter))
print("Top objective", min(costs_iter))
print("Improvement %:", (min(costs_iter) - init_cost) / init_cost)
print("Time:", end_time - start_time)

print(sols_iter[costs_iter.index(min(costs_iter))])
print(feasibility_check(sols_iter[costs_iter.index(min(costs_iter))], problem))

