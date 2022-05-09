from operator import indexOf
from utils import *
from nbors import *
from methods import *
from utils import cost_function
import time

# TODO - Change for run session
probnames = [('./Call_7_Vehicle_3.txt', 30), ('./Call_18_Vehicle_5.txt', 10), ('./Call_35_Vehicle_7.txt', 20), ('./Call_80_Vehicle_20.txt', 120), ('./Call_130_Vehicle_40.txt', 300)]

# Compiles JIT functions ahead of time as to not waste running time doing it.
start_init_time = time.time()
n_nodes, n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost = load_problem('./Call_7_Vehicle_3.txt')
init_sol = [0] * n_vehicles
for i in range(n_calls):
    init_sol += [(i+1), (i+1)]
init_sol = np.array(init_sol)
sol, costs = reassign_all(n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost)
reassign_call(init_sol, costs, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost)
reorder_vehicle_calls(init_sol, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo)
assign_retireds(init_sol, costs, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost)
retire_calls(init_sol, costs, Cargo)
print("Function initialisation finished after", time.time() - start_init_time, "seconds")
x = input("Are you ready?")


def run_problem(probname, probtime):
    n_nodes, n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost = load_problem(probname)
    init_sol = [0] * n_vehicles
    for i in range(n_calls):
        init_sol += [(i+1), (i+1)]
    init_sol = np.array(init_sol)
    init_cost = cost_function(init_sol, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost)

    st = time.time()
    sol, cost = alns(probtime, n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost) 
    runtime = time.time() - st

    return sol, cost, runtime, init_cost

f = open("results.txt", "a")
for probname, probtime in probnames:
    sol, cost, rt, icost = run_problem(probname, probtime)
    f = open("results.txt", "a")
    f.write(probname + "\n")
    f.write("Cost: " + str(cost) + "\n")
    f.write("Improvement% (from all retireds): " + str((icost-cost)/icost) + "\n")
    f.write("Runtime: " + str(rt) + "\n")
    f.write("Solution: " + str(sol) + "\n\n\n")
    f.close()
