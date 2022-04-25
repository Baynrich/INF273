from nbors import *
from printer import *
from methods import *
import time
        


def run_problem(problem, initial_solution):
    methods = [localsearch, annealing]
    operators = [oneopt_operator_nborhood, twoopt_operator_nborhood, threeopt_operator_nborhood]
    sols = []
    costs = []
    times = []
    for method in methods:
        for operator in operators:
            st = time.time()
            best_sol, best_sol_cost = method(initial_solution, operator, problem)
            et = time.time()
            sols.append(best_sol)
            costs.append(best_sol_cost)
            times.append(et - st)
    return sols, costs, times

problem = load_problem('./Call_18_Vehicle_5.txt')
init_sol = [0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18]
init_cost = cost_function(init_sol, problem)
sols_iter = []
costs_iter = []
times_iter = []
for i in range(10):
    sols, costs, times = run_problem(problem, init_sol)
    sols_iter.append(sols)
    costs_iter.append(costs)
    times_iter.append(times)
printer(costs_iter, sols_iter, init_cost, times_iter, problem)
