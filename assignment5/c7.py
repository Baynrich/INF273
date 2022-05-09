from operator import indexOf
from utils import *
from nbors import *
from methods import *
from utils import cost_function
import time

probnames = ['./Call_7_Vehicle_3.txt', './Call_18_Vehicle_5.txt', './Call_35_Vehicle_7.txt', './Call_80_Vehicle_20.txt', './Call_130_Vehicle_40.txt']

def run_problem(probname):
    n_nodes, n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost = load_problem(probname)
    init_sol = [0] * n_vehicles
    for i in range(n_calls):
        init_sol += [(i+1), (i+1)]
    init_sol = np.array(init_sol)
    init_cost = cost_function(init_sol, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost)

    st = time.time()
    sol, cost = alns(n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost) 
    runtime = time.time() - st

    return sol, cost, runtime, init_cost

f = open("results.txt", "a")
for probname in probnames:
    sol, cost, rt, icost = run_problem(probname)
    f = open("results.txt", "a")
    f.write(probname + "\n")
    f.write("Cost: " + str(cost) + "\n")
    f.write("Improvement% (from all retireds): " + str((icost-cost)/icost) + "\n")
    f.write("Runtime: " + str(rt) + "\n")
    f.write("Solution: " + str(sol) + "\n\n\n")
    f.close()
