import random
import numpy as np
from utils import cost_function, feasibility_check



def reassign_call(sol, n_vehicles, n_calls):
    target_v = random.randint(0, n_vehicles)
    target_c = random.randint(1, n_vehicles)
    r_sol = np.copy(sol)
    r_sol = r_sol[r_sol != target_c]

    zctr = 0
    sidx = -1
    eidx = -1
    for i in range(len(r_sol)):
        if r_sol[i] == 0:
            zctr += 1
            if  target_v == 0:
                sidx = 0
                eidx = i
                break
            if zctr == n_vehicles and target_v == n_vehicles:
                sidx = i+1
                eidx = len(r_sol) - 1
                break

            if(target_v != n_vehicles):
                if zctr == target_v:
                    sidx = i + 1
                    continue
                if zctr == target_v + 1:
                    eidx = i
                    break

    # Reinsert call  
    for i in range(2):
        try:
            insertpos = random.randint(sidx, eidx + i)
            r_sol = np.insert(r_sol, insertpos, target_c)
        # Edge case whenever retiring when all other calls are active
        except:
            r_sol = np.insert(r_sol, sidx, target_c)
    return r_sol



def reorder_vehicle_calls(sol, n_vehicles, n_calls):
    """ Reinsert a call within the schedule of a vehicle """
    # Do not allow selecting retired calls on this occasion
    ZeroIndex = np.array(np.where(sol == 0)[0], dtype=int)
    reorderables = []
    for i, idx in enumerate(ZeroIndex):
        if i == 0 and idx < 4:
            continue
        if idx - ZeroIndex[i-1] < 4:
            continue
        reorderables.append(idx)

    # No vehicles can be reordered - reassign instead.
    if len(reorderables) < 1:
        return sol

    eidx = random.choice(reorderables)
    sidx = 0
    for i in range(eidx):
        if sol[eidx - (i+1)] == 0:
            sidx = eidx - (i)
            break

    to_reorder = random.randint(sidx, eidx-1)
    to_target = random.choice([sidx + i for i in range(eidx-sidx) if sol[sidx + i] != sol[to_reorder]])
    target = sol[to_target]
    sol[to_target] = sol[to_reorder]
    sol[to_reorder] = target
    return sol

    
def assign_retireds(sol, prob):
    currentVehicle = []
    vehicles = []
    for call in sol:
        if call == 0:
            vehicles.append(currentVehicle)
            currentVehicle = []
        else:
            currentVehicle.append(call)
    vehicles.append(currentVehicle)

    # Reassign all retired calls to vehicles.
    retireds = vehicles.pop()

    # No retired calls to reassign -> reorder some vehicle call instead.
    if len(retireds) == 0:
        return sol


    # Un-retire random amount of calls. Start by un-retiring calls with highest cost of not transporting.
    retireds = list(set(retireds))
    retireds = [(call, prob["Cargo"][call-1][3]) for call in retireds]
    retireds.sort(key = lambda tuple: tuple[1], reverse=True)
    n_to_assign = 1 if len(retireds) < 2 else random.randint(1, int(np.sqrt(len(retireds) - 1)))

    for call in retireds[0:n_to_assign]:
        assigned_vehicle = random.randint(0, len(vehicles)-1)
        for i in range(2):
            insert_pos = random.randint(0, len(vehicles[assigned_vehicle]))
            vehicles[assigned_vehicle].insert(insert_pos, call[0])
    

    vehicles.append([call[0] for call in retireds[n_to_assign:]])
    vehicles.append([call[0] for call in retireds[n_to_assign:]])
    # Flatten
    flattened = []
    for i, vehicle in enumerate(vehicles):
        flattened += vehicle
        if (i < len(vehicles) - 2):
            flattened += [0]
    return np.array(flattened)
            

def retire_calls(sol, prob):
    ZeroIndex = np.array(np.where(sol == 0)[0], dtype=int)
    r_sol = list(set(sol[:ZeroIndex[-1]]))
    r_sol.remove(0)
    if len(r_sol) < 1:
        return sol
    costs = [[i, 0] for i in r_sol]
    vehicle = 0
    for i in range(len(sol)):
        if not sol[i] in r_sol:
            continue
        if(sol[i] == 0):
            vehicle += 1
            continue
        trialsol = [0] * vehicle + [sol[i], sol[i]] + [0] * (prob["n_vehicles"] - vehicle)
        curcost = cost_function(trialsol, prob)
        for j in range(len(costs)):
            if costs[j][0] == sol[i]:
                costs[j][1] = curcost
                break
    costs.sort(key = lambda tuple: tuple[1], reverse=True)    
    n_to_retire = random.randint(1, min(3, len(r_sol)))
    for i in range(n_to_retire):
        to_retire = costs[i][0]
        sol = sol[sol != to_retire]
        sol = np.append(sol, costs[i][0])
        sol = np.append(sol, costs[i][0])
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
    return r_sol
