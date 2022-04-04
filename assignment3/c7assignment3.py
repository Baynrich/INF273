from nbors import *
from printer import *
from methods import *

        


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

problem = load_problem('./Call_7_Vehicle_3.txt')
init_sol = [0, 0, 0, 7, 7, 3, 3, 1, 5, 5, 1, 6, 6, 4, 4, 2, 2]
init_cost = cost_function(init_sol, problem)
sols_iter = []
costs_iter = []
for i in range(1):
    sols, costs = run_problem(problem, init_sol)
    sols_iter.append(sols)
    costs_iter.append(costs)

printer(costs_iter, sols_iter, init_cost)
