from utils import *
from nbors import *
from printer import *
from methods import *

n = 5000



testsol = [2, 2, 0, 0, 3, 3]
threeopt_operator_nborhood(testsol)

"""
prob = load_problem('./Call_7_Vehicle_3.txt')
init_sol = [0, 0, 0, 7, 7, 3, 3, 1, 5, 5, 1, 6, 6, 4, 4, 2, 2]
init_cost = cost_function(init_sol, prob) 

best_sol = init_sol
best_sol_cost = cost_function(best_sol, prob) 
print("Initial soution cost: ", best_sol_cost)
for i in tqdm(range(n)):
    best_nbor = None
    best_nbor_cost = float('inf')
    nbors = threeopt_operator_nborhood(best_sol)
    for nbor in nbors:
        feasibility, c = feasibility_check(nbor, prob)
        if feasibility:
            nbor_cost = cost_function(nbor, prob) 
            print("Found feasible nbor with cost", nbor_cost, "")
            if nbor_cost < best_nbor_cost:
                best_nbor_cost = nbor_cost
                best_nbor = nbor
    
    if best_nbor is not None and best_sol_cost > best_nbor_cost:
        best_sol = best_nbor
        best_sol_cost = best_nbor_cost
    if best_nbor is None or best_sol_cost <= best_nbor_cost:
        print("Exiting early")
        # We've found local optima. Will not get better.
        break
        """
