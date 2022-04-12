from operator import indexOf
from utils import *
from nbors import *
from methods import *
import time

def run_problem(problem, initial_solution):
    best_sol, best_sol_cost = annealing(initial_solution, problem)
    return best_sol, best_sol_cost

problem = load_problem('./Call_18_Vehicle_5.txt')
init_sol = [0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18]

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

