from nbors import *
from printer import *
from methods import *
        



problem = load_problem('./Call_7_Vehicle_3.txt')
init_sol = [0, 0, 0, 7, 7, 3, 3, 1, 5, 5, 1, 6, 6, 4, 4, 2, 2]
init_cost = cost_function(init_sol, problem)
sols, costs, times = run_problem(problem, init_sol)

print(sols)
print(costs)
print(times)

printer(costs, sols, init_cost, times, problem)