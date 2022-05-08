from utils import load_problem, feasibility_check
import numpy as np

def feas_old(solution, num_vehicles, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo):    

    solution = np.append(solution, [0])
    ZeroIndex = np.array(np.where(solution == 0)[0], dtype=int)
    feasibility = True
    tempidx = 0
    for i in range(num_vehicles): 
        currentVPlan = solution[tempidx:ZeroIndex[i]]
        currentVPlan = currentVPlan - 1
        NoDoubleCallOnVehicle = len(currentVPlan)
        tempidx = ZeroIndex[i] + 1
        if NoDoubleCallOnVehicle > 0:

            if not np.all(VesselCargo[i, currentVPlan]):
                feasibility = False
                break
            else:
                LoadSize = 0
                currentTime = 0
                sortRout = np.sort(currentVPlan, kind='quicksort')
                I = np.argsort(currentVPlan, kind='quicksort')
                Indx = np.argsort(I, kind='quicksort')
                LoadSize -= Cargo[sortRout, 2]
                LoadSize[::2] = Cargo[sortRout[::2], 2]
                LoadSize = LoadSize[Indx]
                if np.any(VesselCapacity[i] - np.cumsum(LoadSize) < 0):
                    feasibility = False
                    break
                Timewindows = np.zeros((2, NoDoubleCallOnVehicle))
                Timewindows[0] = Cargo[sortRout, 6]
                Timewindows[0, ::2] = Cargo[sortRout[::2], 4]
                Timewindows[1] = Cargo[sortRout, 7]
                Timewindows[1, ::2] = Cargo[sortRout[::2], 5]

                Timewindows = Timewindows[:, Indx]

                PortIndex = Cargo[sortRout, 1].astype(int)
                PortIndex[::2] = Cargo[sortRout[::2], 0]
                PortIndex = PortIndex[Indx] - 1

                LU_Time = UnloadingTime[i, sortRout]
                LU_Time[::2] = LoadingTime[i, sortRout[::2]]
                LU_Time = LU_Time[Indx]
                Diag = TravelTime[i, PortIndex[:-1], PortIndex[1:]]
                FirstVisitTime = FirstTravelTime[i, int(Cargo[currentVPlan[0], 0] - 1)]

                RouteTravelTime = np.hstack((FirstVisitTime, Diag.flatten()))

                ArriveTime = np.zeros(NoDoubleCallOnVehicle)
                for j in range(NoDoubleCallOnVehicle):
                    ArriveTime[j] = np.max((currentTime + RouteTravelTime[j], Timewindows[0, j]))
                    if ArriveTime[j] > Timewindows[1, j]:
                        feasibility = False
                        break
                    currentTime = ArriveTime[j] + LU_Time[j]

    return feasibility



n_nodes, n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost = load_problem('./Call_18_Vehicle_5.txt')


foundsol = [4, 4, 1, 1, 0,  8,  8, 17, 17, 13, 13,  0,  6,  6, 11, 11, 12, 12,  0,  7,  7,  5,  5, 14, 14,  0,  9,  9,  0,  2,  2, 16, 16,  3,  3, 10, 10, 18, 18, 15, 15]
print(feas_old(np.array(foundsol), n_vehicles, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo))
print(feasibility_check(np.array(foundsol), n_vehicles, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo))