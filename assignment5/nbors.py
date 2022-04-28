from multiprocessing.dummy import current_process
import random
import numpy as np


def reassign_call(sol, prob):
    """ Now works with numpy conversion now """
    target_v = random.randint(0, prob["n_vehicles"])
    target_c = random.randint(1, prob["n_calls"])
    r_sol = np.copy(sol)
    r_sol = r_sol[r_sol != target_c]

    zctr = 0
    sidx = -1
    eidx = -1
    for i in range(len(r_sol)):
        if r_sol[i] == 0:
            zctr += 1
            if  target_v == 0:
                print("Placing in first position")
                sidx = 0
                eidx = i
                break
            if zctr == prob["n_vehicles"] and target_v == prob["n_vehicles"]:
                print("Retiring call")
                sidx = i+1
                eidx = len(r_sol) - 1
                break

            if(target_v != prob["n_vehicles"]):
                if zctr == target_v:
                    sidx = i + 1
                    continue
                if zctr == target_v + 1:
                    eidx = i
                    break

    # Reinsert call  
    for i in range(2):
        insertpos = random.randint(sidx, eidx + i)
        r_sol = np.insert(r_sol, insertpos, target_c)
    return r_sol



def reorder_vehicle_calls(sol, prob):
    """ Reinsert a call within the schedule of a vehicle """

    # Do not allow selecting retired calls on this occasion
    ZeroIndex = np.array(np.where(sol == 0)[0], dtype=int)
    reorderables = [zi for i, zi in enumerate(ZeroIndex) if not(i == 0 and zi < 3 or i > 0 and zi - ZeroIndex[i-1] < 3)]
    
    # No vehicles can be reordered - return same solution.
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

        

    
def assign_all_retireds(sol, prob):
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
    retireds = list(set(retireds))
    for call in retireds:
        assigned_vehicle = random.randint(0, len(vehicles)-1)
        for i in range(2):
            insert_pos = random.randint(0, len(vehicles[assigned_vehicle]))
            vehicles[assigned_vehicle].insert(insert_pos, call)
    
    vehicles.append([])

    # Flatten
    flattened = []
    for i, vehicle in enumerate(vehicles):
        flattened += vehicle
        if (i < len(vehicles) - 1):
            flattened += [0]
    return flattened
            

