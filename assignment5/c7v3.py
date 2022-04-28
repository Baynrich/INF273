from operator import indexOf
from utils import *
from nbors import *
from methods import *
import time
from utils import cost_function, feasibility_check 

c7list = [0] * 3 + [i, i]

def run_problem(init_sol, prob):
    best_sol, best_sol_cost = alns(init_sol, prob)
    print(best_sol)
    print(best_sol_cost)
    return best_sol, best_sol_cost

prob = load_problem('./Call_7_Vehicle_3.txt')
init_sol = np.array([0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7])
run_problem(init_sol, prob)
