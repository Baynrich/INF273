from operator import indexOf
from utils import *
from nbors import *
from methods import *
from utils import cost_function, feasibility_check 

probname = './Call_7_Vehicle_3.txt'
prob = load_problem(probname)
init_sol = [0] * prob["n_vehicles"]
for i in range(prob["n_calls"]):
    init_sol += [(i+1), (i+1)]
init_sol = np.array(init_sol)



def run_problem(init_sol, prob):
    best_best_sol = None
    best_best_cost = float('inf')
    for i in range(10):
        best_sol, best_sol_cost = alns(init_sol, prob)
        if(best_sol_cost < best_best_cost):
            best_best_sol = best_sol
            best_best_cost = best_sol_cost
    print(best_best_sol, best_best_cost)
    return best_best_sol, best_best_cost


#run_problem(init_sol, prob)
print(retire_calls(np.array([1, 1, 0, 2, 2, 0, 3, 3, 0, 4, 4, 5, 5, 6, 6, 7, 7]), prob))

