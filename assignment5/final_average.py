from utils import *
from nbors import *
from methods import *
from utils import cost_function
import time
import subprocess
import sys
from tqdm import tqdm

subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "numba"])


# Associated times adds up to 895 seconds
# TODO - Change for run session
probnames = [('./Call_7_Vehicle_3.txt', 45), ('./Call_18_Vehicle_5.txt', 75), ('./Call_35_Vehicle_7.txt', 100), ('./Call_80_Vehicle_20.txt', 225), ('./Call_130_Vehicle_40.txt', 450)]

# Compiles JIT functions ahead of time as to not waste running time doing it.
start_init_time = time.time()
n_nodes, n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost = load_problem('./Call_7_Vehicle_3.txt')
init_sol = [0] * n_vehicles
for i in range(n_calls):
    init_sol += [(i+1), (i+1)]
init_sol = np.array(init_sol)
sol, costs = reassign_all(n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost)
reassign_call(init_sol, costs, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo)
reorder_vehicle_calls(init_sol, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo)
assign_retireds(init_sol, costs, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost)
retire_calls(init_sol, costs, Cargo)
handle_set_T_alpha(np.array([1]), 1)
select_nbor_op(sol, np.ones(4), costs, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo)

cooldown = np.zeros(20000)
for i in range(len(cooldown)):
    cooldown[i] = np.exp(-1 * ((i+100) / 2000))

print("Function initialisation finished after", time.time() - start_init_time, "seconds")

def run_problem_average(probname, cooldown):
    print("Running problem:", probname)
    n_nodes, n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost = load_problem(probname)
    init_sol = [0] * n_vehicles
    for i in range(n_calls):
        init_sol += [(i+1), (i+1)]
    init_sol = np.array(init_sol)
    init_cost = cost_function(init_sol, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost)
    best_cost = float('inf')
    best_sol = None

    costs = np.array([])
    st = time.time()
    for i in tqdm(range(10)):
        sol, cost = alns(999999999999, cooldown, n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost) 
        costs = np.append(costs, cost)
        if cost < best_cost:
            best_cost = cost
            best_sol = sol
    runtime = time.time() - st
    return best_sol, best_cost, runtime, np.mean(costs), init_cost


def run_all_average():
    for probname, probtime in probnames:
        sol, cost, rt, acost, icost = run_problem_average(probname, cooldown)
        # Accumulate time not used in previous iterations
        f = open("results.txt", "a")
        f.write(probname + "\n")
        f.write("Best cost: " + str(cost) + "\n")
        f.write("Average cost" + str(acost) + "\n")
        f.write("Improvement% (from all retireds): " + str((icost-cost)/icost) + "\n")
        f.write("Runtime: " + str(rt) + "\n")
        f.write("Solution: " + str(sol) + "\n\n\n")
        f.close()

run_all_average()
