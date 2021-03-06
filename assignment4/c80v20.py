from operator import indexOf
from utils import *
from nbors import *
from methods import *
import numpy as np
import time



def run_problem(problem, initial_solution):
    best_sol, best_sol_cost = annealing(initial_solution, problem)
    return best_sol, best_sol_cost

problem = load_problem('./Call_80_Vehicle_20.txt')
init_sol = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29, 30, 30, 31, 31, 32, 32, 33, 33, 34, 34, 35, 35, 36, 36, 37, 37, 38, 38, 39, 39, 40, 40, 41, 41, 42, 42, 43, 43, 44, 44, 45, 45, 46, 46, 47, 47, 48, 48, 49, 49, 50, 50, 51, 51, 52, 52, 53, 53, 54, 54, 55, 55, 56, 56, 57, 57, 58, 58, 59, 59, 60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 65, 65, 66, 66, 67, 67, 68, 68, 69, 69, 70, 70, 71, 71, 72, 72, 73, 73, 74, 74, 75, 75, 76, 76, 77, 77, 78, 78, 79, 79, 80, 80]

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

