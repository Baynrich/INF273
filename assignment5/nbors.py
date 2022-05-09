import random
import numpy as np
from utils import cost_function, feasibility_check, handle_init_costs
from numba import jit, prange

@jit(nopython=True)
def reassign_call(sol, costs, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost):
    # Reassigns call with currently highest associated cost and reassigns it to a new vehicle
    actives = costs[costs[:, 1] == 0]
    if len(actives) < 1:
        # No calls are active, return initial solution
        return sol, costs
    actives = actives[np.argsort(actives[:, 0])][::-1]
    sol = sol[sol != actives[0, 2]]
    
    # Randomly select vehicle to assign removed call to.
    target_v = random.randint(0, n_vehicles - 1)
    ZeroIndexes = np.where(sol == 0)[0]
    ZeroIndexes = ZeroIndexes.astype('int64')
    sidx = 0 if target_v == 0 else ZeroIndexes[target_v - 1] + 1
    eidx = ZeroIndexes[target_v]

    # Reinsert removed call into selected vehicle
    insertIdx = random.randint(sidx, eidx)
    befores = sol[:insertIdx]
    afters = sol[insertIdx:]
    sol = np.concatenate((befores, np.array([int(actives[0, 2])])))
    sol = np.concatenate((sol, afters))
    insertIdx = random.randint(sidx, eidx)
    befores = sol[:insertIdx]
    afters = sol[insertIdx:]
    sol = np.concatenate((befores, np.array([int(actives[0, 2])])))
    sol = np.concatenate((sol, afters))

    # Update inserted call's associated cost
    updatedCostSol = sol[np.logical_or(sol != 0, sol != actives[0, 2])]
    costs[int(actives[0, 2] - 1)][0] = cost_function(updatedCostSol, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost)
    return sol, costs

@jit(nopython=True, parallel=True)
def reorder_vehicle_calls(sol, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo):
    """ Greedily reinsert a call within the schedule of a vehicle """
    # Do not allow selecting retired calls on this occasion
    ZeroIndex = np.where(sol == 0)[0]
    ZeroIndex = ZeroIndex.astype('int64')
    reorderables = []
    for i, idx in enumerate(ZeroIndex):
        if i == 0 and idx < 4:
            continue
        if i > 0 and idx - ZeroIndex[i-1] < 4:
            continue
        reorderables.append([i, idx])
    # No vehicles can be reordered - return original solution. 

    if len(reorderables) < 1:
        return sol
    reorderables = np.array(reorderables)
    e = np.random.randint(len(reorderables))
    e = reorderables[e]
    eidx = e[1]
    sidx = 0 if e[0] == 0 else ZeroIndex[e[0]-1] + 1


    to_reorder = np.random.randint(sidx, eidx)
    top_sol = sol.copy()
    #TODO - we already have this, pass as param rather than calculate
    top_sol_cost = cost_function(top_sol, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost)
    

    for i in prange(sidx, eidx):
        r_sol = sol.copy()
        target = r_sol[i]
        r_sol[i] = r_sol[to_reorder]
        r_sol[to_reorder] = target

        if(feasibility_check(r_sol, n_vehicles, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo)):
            r_sol_cost = cost_function(r_sol, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost)
            if r_sol_cost < top_sol_cost:
                # TODO - Data race may occur here
                top_sol_cost = r_sol_cost
                top_sol = r_sol
    return top_sol

@jit(nopython=True)
def assign_retireds(sol, costs, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost):
    retireds = costs[costs[:, 1] == 1]
    if len(retireds) < 1:
        return sol, costs

    retireds = retireds[np.argsort(retireds[:, 0])][::-1]
    n_to_assign = 1 if len(retireds) < 2 else random.randint(1, int(np.sqrt(len(retireds) - 1)))
    for i in range(n_to_assign):
        sol = sol[sol != retireds[i, 2]]

        retiredIndex = np.where(sol == 0)[0]
        retiredIndex = retiredIndex.astype('int64')
        retiredIndex = retiredIndex[-1]

        insertIdx = random.randint(0, retiredIndex)
        befores = sol[:insertIdx]
        afters = sol[insertIdx:]
        sol = np.concatenate((befores, np.array([int(retireds[i, 2]), int(retireds[i, 2])])))
        sol = np.concatenate((sol, afters))
        # Update inserted call's associated cost
        updatedCostSol = sol[np.logical_or(sol != 0, sol != retireds[i, 2])]
        costs[int(retireds[i, 2] - 1)][0] = cost_function(updatedCostSol, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost)
        costs[int(retireds[i, 2] - 1)][1] = 0
    return sol, costs
            
@jit(nopython=True)
def retire_calls(sol, costs, Cargo):
    # TODO - make call selection a weighted probability instead of direct selection to avoid getting stuck.
    # Filter calls currently not retired
    actives = costs[costs[:, 1] == 0]
    if len(actives) < 1:
        return sol, costs

    actives = actives[np.argsort(actives[:, 0])][::-1]
    # Starting with most expensive calls, retire.
    n_to_retire = random.randint(1, min(3, len(actives)))
    for i in range(n_to_retire):
        sol = sol[sol != actives[i, 2]]
        sol = np.append(sol, int(actives[i][2]))
        sol = np.append(sol, int(actives[i][2]))
        # Update retired call's associated cost
        costs[int(actives[i, 2] - 1)][0] = Cargo[int(actives[i, 2] - 1)][3]
        costs[int(actives[i, 2] - 1)][1] = 1
    return sol, costs

@jit(nopython=True)
def reassign_all(n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost):
    all_calls = np.array([i+1 for i in range(n_calls)])
    r_sol = np.array([0 for i in range(n_vehicles)])
    while(len(all_calls) > 0):
        cur_call = np.random.choice(all_calls)
        all_calls = all_calls[all_calls != cur_call]

        ZeroIndex = np.where(r_sol == 0)[0]
        ZeroIndex = ZeroIndex.astype('int64')

        inserted = False
        for index in ZeroIndex:
            cand_sol = r_sol.copy()

            befores = cand_sol[:index]
            afters = cand_sol[index:]
            cand_sol = np.concatenate((befores, np.array([cur_call, cur_call])))
            cand_sol = np.concatenate((cand_sol, afters))
            if(feasibility_check(cand_sol, n_vehicles, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo)):
                r_sol = cand_sol
                inserted = True
                break
        if not inserted:
            r_sol = np.append(r_sol, cur_call)
            r_sol = np.append(r_sol, cur_call)
    costs = handle_init_costs(r_sol, n_vehicles, n_calls, Cargo, TravelCost, FirstTravelCost, PortCost)
    return r_sol, costs
