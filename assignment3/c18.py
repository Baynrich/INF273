from nbors import *
from printer import *
from methods import *

problem = load_problem('./Call_18_Vehicle_5.txt')
init_sol = [0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18]
init_cost = cost_function(init_sol, problem)
sols, costs, times = run_problem(problem, init_sol)

printer(costs, sols, init_cost, times, problem)
