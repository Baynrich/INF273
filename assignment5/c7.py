from operator import indexOf
from utils import *
from nbors import *
from methods import *
from utils import cost_function, feasibility_check 
import time

probnames = ['./Call_7_Vehicle_3.txt', './Call_18_Vehicle_5.txt', './Call_35_Vehicle_7.txt', './Call_80_Vehicle_20.txt', './Call_130_Vehicle_40.txt', './Call_300_Vehicle_90.txt']



def run_problem(probname):
    prob = load_problem(probname)
    init_sol = [0] * prob["n_vehicles"]
    for i in range(prob["n_calls"]):
        init_sol += [(i+1), (i+1)]
    init_sol = np.array(init_sol)
    init_cost = cost_function(init_sol, prob)
    best_best_sol = None
    best_best_cost = float('inf')
    best_costs = []
    st = time.time()
    for i in range(10):
        best_sol, best_sol_cost = alns(init_sol, prob)
        best_costs.append(best_sol_cost)
        if(best_sol_cost < best_best_cost):
            best_best_sol = best_sol
            best_best_cost = best_sol_cost
    runtime = time.time() - st

    average_cost = np.mean(best_costs)
    return best_best_sol, best_best_cost, average_cost, runtime, init_cost



f = open("results.txt", "a")
for probname in probnames:

    bsol, bcost, acost, rt, icost = run_problem(probname)
    f.write(probname + "\n")
    f.write("Average cost: " + str(acost) + "\n")
    f.write("Best cost: " + str(acost) + "\n")
    f.write("Improvement%: " + str((icost-bcost)/icost) + "\n")
    f.write("Runtime: " + str(rt) + "\n")
    f.write("Solution: " + str(bsol) + "\n\n\n")

f.close()

