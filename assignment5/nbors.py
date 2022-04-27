from multiprocessing.dummy import current_process
import random
import numpy as np


def reassign_call(sol, prob):

    target_v = random.randint(0, prob["n_vehicles"])
    target_c = random.randint(1, prob["n_calls"])
    r_sol = np.copy(sol)
    r_sol = r_sol[r_sol != target_c]

    prevzpos = -1
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

    print("Call", target_c)
    print("Vehicle", target_v)
    print("Into", r_sol)
    print("Starting at", sidx, "Ending at", eidx)
    # Reinsert call  
    for i in range(2):
        insertpos = random.randint(sidx, eidx + i)
        r_sol = np.insert(r_sol, insertpos, target_c)
    
    print("Result", r_sol)

    return r_sol



def reorder_vehicle_calls(sol, prob):
    """ Reinsert a call within the schedule of a vehicle """
    currentVehicle = []
    vehicles = []
    for call in sol:
        if call == 0:
            vehicles.append(currentVehicle)
            currentVehicle = []
        else:
            currentVehicle.append(call)
    vehicles.append(currentVehicle)

    # Do not allow rearranging retired calls
    retireds = vehicles.pop()

    # If no vehicles are rearrangable, do nothing.
    rearrangables = [(idx, vehicle) for idx, vehicle in enumerate(vehicles.copy()) if len(vehicle) > 2]
    if len(rearrangables) > 0:
        to_rearrange = random.choice(rearrangables)
        to_reinsert = to_rearrange[1].pop(random.randint(0, len(to_rearrange[1])-1))
        to_rearrange[1].insert(random.randint(0, len(to_rearrange[1])-1), to_reinsert)
        vehicles[to_rearrange[0]] = to_rearrange[1]

    vehicles.append(retireds)

    # Flatten
    flattened = []
    for i, vehicle in enumerate(vehicles):
        flattened += vehicle
        if (i < len(vehicles) - 1):
            flattened += [0]
    return flattened
    
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
            

