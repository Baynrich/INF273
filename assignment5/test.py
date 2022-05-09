from utils import load_problem
from nbors import reorder_vehicle_calls
import numpy as np

n_nodes, n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost = load_problem('./Call_7_Vehicle_3.txt')


init_sol = np.array([4, 4, 7, 7, 0, 0, 0, 2, 2, 3, 3, 5, 5, 6, 6, 7, 7])
print(reorder_vehicle_calls(init_sol, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo))
