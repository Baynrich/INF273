from multiprocessing.dummy import current_process
import random
import numpy as np



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
        return reassign_call(sol, n_vehicles, n_calls)

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

    
def assign_retireds(sol, n_vehicles, n_calls, prob):

    """ This operator is intended to move us far from our current solution in the solution space.
        Moves many calls, where other operators move only one. """
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
        return(reorder_vehicle_calls(sol, n_vehicles, n_calls))


    # Un-retire random amount of calls. Start by un-retiring calls with highest cost of not transporting.
    retireds = list(set(retireds))
    retireds = [(call, prob["Cargo"][call-1][3]) for call in retireds]
    retireds.sort(key = lambda tuple: tuple[1], reverse=True)
    n_to_assign = random.randint(1, len(retireds) - 1)

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
        if (i < len(vehicles) - 1):
            flattened += [0]
    return flattened
            

