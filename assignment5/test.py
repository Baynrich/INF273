from utils import load_problem
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

def feas_new(solution, n_vehicles, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo):
    """
    :rtype: tuple
    :param solution: The input solution of order of calls for each vehicle to the problem
    :param problem: The pickup and delivery problem object
    :return: whether the problem is feasible and the reason for probable infeasibility
    """
    solution = np.append(solution, [0])
    ZeroIndex = np.where(solution == 0)[0]
    ZeroIndex = ZeroIndex.astype('int64')
    feasibility = True
    tempidx = 0
    for i in range(n_vehicles): 
        currentVPlan = solution[tempidx:ZeroIndex[i]]
        currentVPlan = currentVPlan - 1
        NoDoubleCallOnVehicle = len(currentVPlan)
        tempidx = ZeroIndex[i] + 1
        if NoDoubleCallOnVehicle > 0:
            allcand = np.zeros(currentVPlan.size)
            for j in range(len(currentVPlan)):
                currentv = currentVPlan[j]
                allcand[j] = VesselCargo[i, currentv]

            if not np.all(allcand):
                return False
            
            sortRout = np.sort(currentVPlan)
            I = np.argsort(currentVPlan, kind='quicksort')
            Indx = np.argsort(I, kind='quicksort')

            LoadSize = np.zeros(sortRout.size)
            for j in range(len(sortRout)):
                LoadSize[j] = (-1) * Cargo[j, 2]

            for j in range(int(len(LoadSize) / 2)):
                LoadSize[j*2] = abs(LoadSize[j*2])
            LoadSize = LoadSize[Indx]
            if np.any(VesselCapacity[i] - np.cumsum(LoadSize) < 0):
                return False

            Timewindows = np.zeros((2, NoDoubleCallOnVehicle))
            Timewindows[0] = Cargo[sortRout, 6]
            Timewindows[0, ::2] = Cargo[sortRout[::2], 4]
            Timewindows[1] = Cargo[sortRout, 7]
            Timewindows[1, ::2] = Cargo[sortRout[::2], 5]

            Timewindows = Timewindows[:, Indx]
            PortIndex = Cargo[sortRout, 1].astype("int")
            PortIndex[::2] = Cargo[sortRout[::2], 0]
            PortIndex = PortIndex[Indx] - 1
            LU_Time = np.zeros(sortRout.size)
            for j in range(len(LU_Time)):
                if np.mod(j, 2) == 0:
                    LU_Time[j] = LoadingTime[i, sortRout[j]]
                else:
                    LU_Time[j] = UnloadingTime[i, sortRout[j]]
            
            LU_Time = LU_Time[Indx]

            Diag = np.zeros(PortIndex.size - 1)
            for j in range(len(PortIndex) - 1):
                Diag[j] = TravelTime[i, PortIndex[j], PortIndex[j+1]]
            FirstVisitTime = np.atleast_1d(np.array(FirstTravelTime[i, int(Cargo[currentVPlan[0], 0] - 1)]))
            RouteTravelTime = np.concatenate((FirstVisitTime, Diag))
            ArriveTime = np.zeros(NoDoubleCallOnVehicle)

            currentTime = 0
            for j in range(NoDoubleCallOnVehicle):
                ArriveTime[j] = max(currentTime + RouteTravelTime[j], Timewindows[0, j])
                if ArriveTime[j] > Timewindows[1, j]:
                    return False
                currentTime = ArriveTime[j] + LU_Time[j]

    return feasibility



n_nodes, n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost = load_problem('./Call_18_Vehicle_5.txt')


foundsol = [17, 17, 13, 13,  0,  5, 12, 11, 12,  7,  5, 11,  7,  0, 16, 18, 16,  6, 18,  6,  0, 10, 14, 14, 10,  0,  1,  1,  3,  3,  0,  4,  4, 15, 15,  2,  2,  9,  9,  8,  8]
print(feas_old(np.array(foundsol), n_vehicles, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo))
print(feas_new(np.array(foundsol), n_vehicles, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo))