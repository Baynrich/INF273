import random
import numpy as np
from utils import cost_function, feasibility_check, handle_init_costs



def reassign_call(sol, n_vehicles, costs, prob):
    # Reassigns call with currently highest associated cost and reassigns it to a new vehicle
    actives = np.where(costs[1] == 0)[0]
    if len(actives) < 1:
        # No calls are active, return initial solution
        return sol

    actives = actives[np.argsort(actives[:, 0])][::-1]
    target_v = random.randint(0, n_vehicles - 1)
    ZeroIndexes = np.array(np.where(sol == 0)[0], dtype=int)
    sidx = 0 if target_v == 0 else ZeroIndexes[target_v - 1] + 1
    eidx = ZeroIndexes[target_v]
    sol = np.array(np.where(sol != actives[0][2]))
    for i in range(2):
        insertpos = random.randint(sidx, eidx + i)
        sol = np.insert(sol, insertpos, actives[0][2])
        # Update inserted call's associated cost
        updatedCostSol = np.where(sol != 0 or sol != actives[i][2])[0]
        costs[actives[i, 2]][0] = cost_function(updatedCostSol, prob)        
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
    eidx = e[0]
    sidx = 0 if e[1] == 0 else reorderables[e[1] - 1][0]
    to_reorder = random.randint(sidx, eidx-1)
    to_target = random.choice([sidx + i for i in range(eidx-sidx) if sol[sidx + i] != sol[to_reorder]])
    target = sol[to_target]
    sol[to_target] = sol[to_reorder]
    sol[to_reorder] = target
    return sol

    
def assign_retireds(sol, prob, costs):
    retireds = np.where(costs[1] == 1)[0]
    if len(retireds) < 1:
        return sol, costs

    retireds = retireds[np.argsort(retireds[:, 0])][::-1]
    n_to_assign = 1 if len(retireds) < 2 else random.randint(1, int(np.sqrt(len(retireds) - 1)))
    for i in range(n_to_assign):
        sol = np.where(sol != retireds[i][2])
        retiredIndex = np.array(np.where(sol == 0)[0], dtype=int)[-1]
        insertIdx = random.randint(0, retiredIndex)
        sol = np.insert(sol, insertIdx, retireds[i][2])
        sol = np.insert(sol, insertIdx, retireds[i][2])
        
        # Update inserted call's associated cost
        updatedCostSol = np.where(sol != 0 or sol != retireds[i][2])[0]
        costs[retireds[i, 2]][0] = cost_function(updatedCostSol, prob)
        costs[retireds[i, 2]][1] = 0
    return sol, costs
            

def retire_calls(sol, prob, costs):
    # TODO - make call selection a weighted probability instead of direct selection to avoid getting stuck.
    # Filter calls currently not retired
    actives = costs[np.where(costs[1] == 0)[0]]
    print(sol)
    print(costs)
    print(actives)
    if len(actives) < 1:
        return sol

    actives = actives[np.argsort(actives[:, 0])][::-1]
    # Starting with most expensive calls, retire.
    n_to_retire = random.randint(1, min(3, len(actives)))
    for i in range(n_to_retire):
        sol = np.where(sol != actives[i][2])
        sol = np.append(sol, actives[i][2])
        sol = np.append(sol, actives[i][2])
        # Update retired call's associated cost
        costs[actives[i][2]][0] = prob["Cargo"][actives[i][2]+1][3]
        costs[actives[i][2]][1] = 1
    return sol

    
def reassign_all(sol, prob):
    all_calls = [i+1 for i in range(prob["n_calls"])]
    r_sol = np.array([0 for i in range(prob["n_vehicles"])])
    while(len(all_calls) > 0):
        cur_call = random.choice(all_calls)
        all_calls.remove(cur_call)
        ZeroIndex = np.array(np.where(r_sol == 0)[0], dtype=int)
        inserted = False
        for index in ZeroIndex:
            cand_sol = r_sol.copy()
            cand_sol = np.insert(cand_sol, index, cur_call)
            cand_sol = np.insert(cand_sol, index, cur_call)
            if(feasibility_check(cand_sol, prob)):
                r_sol = cand_sol
                inserted = True
                break
        if not inserted:
            r_sol = np.append(r_sol, cur_call)
            r_sol = np.append(r_sol, cur_call)
    costs = handle_init_costs(r_sol, prob["n_vehicles"], prob)
    return r_sol, costs
