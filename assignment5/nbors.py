import random


#TODO - update solution representation to only show retired calls once
def reassign_call(sol, prob):
    """ Move a chosen call between vehicles. """
    r_call = random.randint(1, prob["n_calls"])
    r_sol = sol.copy()
    r_sol = [call for call in r_sol if call != r_call]

    currentVehicle = []
    vehicles = []
    for call in r_sol:
        if call == 0:
            vehicles.append(currentVehicle)
            currentVehicle = []
        else:
            currentVehicle.append(call)
    vehicles.append(currentVehicle)

    # Insert
    to_insert = random.randint(0, len(vehicles)-1)
    for i in range(2):
        temp = len(vehicles[to_insert])
        insertpos = random.randint(0, temp)
        vehicles[to_insert].insert(insertpos, r_call)
    # Flatten
    flattened = []
    for i, vehicle in enumerate(vehicles):
        flattened += vehicle
        if (i < len(vehicles) - 1):
            flattened += [0]
    return flattened

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
            

def reassign_all_calls(sol, prob):
    vehicles = [[] * prob["n_vehicles"] + 1]
    for call in range(prob["n_calls"]):
        vehicle = random.randint(0, len(vehicles)-1)
        vehicles[vehicle].insert(random.randint(0, vehicles[vehicle]-1), (call + 1))
    flattened = []
    for i, vehicle in enumerate(vehicles):
        flattened += vehicle
        if (i < len(vehicles) - 1):
            flattened += [0]
    return flattened