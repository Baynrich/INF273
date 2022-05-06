import random
import numpy as np
from utils import cost_function, feasibility_check, handle_init_costs



def reassign_call(sol, costs, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost):
    # Reassigns call with currently highest associated cost and reassigns it to a new vehicle
    actives = costs[costs[:, 1] == 0]
    if len(actives) < 1:
        # No calls are active, return initial solution
        return sol, costs
    actives = actives[np.argsort(actives[:, 0])][::-1]
    sol = sol[sol != actives[0, 2]]
    target_v = random.randint(0, n_vehicles - 1)
    ZeroIndexes = np.array(np.where(sol == 0)[0], dtype=int)
    sidx = 0 if target_v == 0 else ZeroIndexes[target_v - 1] + 1
    eidx = ZeroIndexes[target_v]
    for i in range(2):
        insertpos = random.randint(sidx, eidx + i)
        sol = np.insert(sol, insertpos, int(actives[0, 2]))
        # Update inserted call's associated cost
    updatedCostSol = sol[np.logical_or(sol != 0, sol != actives[0, 2])]
    costs[int(actives[0, 2] - 1)][0] = cost_function(updatedCostSol, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost)
    return sol, costs



def reorder_vehicle_calls(sol):
    """ Reinsert a call within the schedule of a vehicle """
    # Do not allow selecting retired calls on this occasion
    ZeroIndex = np.array(np.where(sol == 0)[0], dtype=int)
    reorderables = []
    for i, idx in enumerate(ZeroIndex):
        if i == 0 and idx < 4:
            continue
        if idx - ZeroIndex[i-1] < 4:
            continue
        reorderables.append([i, idx])
    # No vehicles can be reordered - return original solution. 
    
    if len(reorderables) < 1:
        return sol
    e = random.choice(reorderables)
    eidx = e[1]
    sidx = 0 if e[0] == 0 else ZeroIndex[e[0]-1] + 1
    to_reorder = random.randint(sidx, eidx-1)
    to_target = random.choice([sidx + i for i in range(eidx-sidx) if sol[sidx + i] != sol[to_reorder]])
    target = sol[to_target]
    sol[to_target] = sol[to_reorder]
    sol[to_reorder] = target
    return sol

    
def assign_retireds(sol, costs, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost):
    retireds = costs[costs[:, 1] == 1]
    if len(retireds) < 1:
        return sol, costs

    retireds = retireds[np.argsort(retireds[:, 0])][::-1]
    n_to_assign = 1 if len(retireds) < 2 else random.randint(1, int(np.sqrt(len(retireds) - 1)))
    for i in range(n_to_assign):
        sol = sol[sol != retireds[i, 2]]
        retiredIndex = np.array(np.where(sol == 0)[0], dtype=int)[-1]
        insertIdx = random.randint(0, retiredIndex)
        sol = np.insert(sol, insertIdx, int(retireds[i][2]))
        sol = np.insert(sol, insertIdx, int(retireds[i][2]))
        
        # Update inserted call's associated cost
        updatedCostSol = sol[np.logical_or(sol != 0, sol != retireds[i, 2])]
        costs[int(retireds[i, 2] - 1)][0] = cost_function(updatedCostSol, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost)
        costs[int(retireds[i, 2] - 1)][1] = 0
    return sol, costs
            

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

    
def reassign_all(n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost):
    all_calls = [i+1 for i in range(n_calls)]
    r_sol = np.array([0 for i in range(n_vehicles)])
    while(len(all_calls) > 0):
        cur_call = random.choice(all_calls)
        all_calls.remove(cur_call)
        ZeroIndex = np.array(np.where(r_sol == 0)[0], dtype=int)
        inserted = False
        for index in ZeroIndex:
            cand_sol = r_sol.copy()
            cand_sol = np.insert(cand_sol, index, cur_call)
            cand_sol = np.insert(cand_sol, index, cur_call)
            if(feasibility_check(cand_sol, n_vehicles, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo)):
                r_sol = cand_sol
                inserted = True
                break
        if not inserted:
            r_sol = np.append(r_sol, cur_call)
            r_sol = np.append(r_sol, cur_call)
    costs = handle_init_costs(r_sol, n_vehicles, n_calls, Cargo, TravelCost, FirstTravelCost, PortCost)
    return r_sol, costs
