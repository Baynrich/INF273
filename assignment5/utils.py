import numpy as np
from numba import jit

def load_problem(filename):
    """
    :rtype: object
    :param filename: The address to the problem input file
    :return: named tuple object of the problem attributes
    """
    A = []
    B = []
    C = []
    D = []
    E = []
    with open(filename) as f:
        lines = f.readlines()
        n_nodes = int(lines[1])
        n_vehicles = int(lines[3])
        n_calls = int(lines[n_vehicles + 5 + 1])

        for i in range(n_vehicles):
            A.append(lines[1 + 4 + i].split(','))

        for i in range(n_vehicles):
            B.append(lines[1 + 7 + n_vehicles + i].split(','))

        for i in range(n_calls):
            C.append(lines[1 + 8 + n_vehicles * 2 + i].split(','))

        for j in range(n_nodes * n_nodes * n_vehicles):
            D.append(lines[1 + 2 * n_vehicles + n_calls + 9 + j].split(','))

        for i in range(n_vehicles * n_calls):
            E.append(lines[1 + 1 + 2 * n_vehicles + n_calls + 10 + j + i].split(','))
        f.close()

    Cargo = np.array(C, dtype=np.double)[:, 1:]
    D = np.array(D, dtype=np.int)

    TravelTime = np.zeros((n_vehicles + 1, n_nodes + 1, n_nodes + 1))
    TravelCost = np.zeros((n_vehicles + 1, n_nodes + 1, n_nodes + 1))
    for j in range(len(D)):
        TravelTime[D[j, 0]][D[j, 1], D[j, 2]] = D[j, 3]
        TravelCost[D[j, 0]][D[j, 1], D[j, 2]] = D[j, 4]

    VesselCapacity = np.zeros(n_vehicles)
    StartingTime = np.zeros(n_vehicles)
    FirstTravelTime = np.zeros((n_vehicles, n_nodes))
    FirstTravelCost = np.zeros((n_vehicles, n_nodes))
    A = np.array(A, dtype=np.int)
    for i in range(n_vehicles):
        VesselCapacity[i] = A[i, 3]
        StartingTime[i] = A[i, 2]
        for j in range(n_nodes):
            FirstTravelTime[i, j] = TravelTime[i + 1, A[i, 1], j + 1] + A[i, 2]
            FirstTravelCost[i, j] = TravelCost[i + 1, A[i, 1], j + 1]
    TravelTime = TravelTime[1:, 1:, 1:]
    TravelCost = TravelCost[1:, 1:, 1:]
    VesselCargo = np.zeros((n_vehicles, n_calls + 1))
    B = np.array(B, dtype=object)
    for i in range(n_vehicles):
        VesselCargo[i, np.array(B[i][1:], dtype=np.int)] = 1
    VesselCargo = VesselCargo[:, 1:]

    LoadingTime = np.zeros((n_vehicles + 1, n_calls + 1))
    UnloadingTime = np.zeros((n_vehicles + 1, n_calls + 1))
    PortCost = np.zeros((n_vehicles + 1, n_calls + 1))
    E = np.array(E, dtype=np.int)
    for i in range(n_vehicles * n_calls):
        LoadingTime[E[i, 0], E[i, 1]] = E[i, 2]
        UnloadingTime[E[i, 0], E[i, 1]] = E[i, 4]
        PortCost[E[i, 0], E[i, 1]] = E[i, 5] + E[i, 3]

    LoadingTime = LoadingTime[1:, 1:]
    UnloadingTime = UnloadingTime[1:, 1:]
    PortCost = PortCost[1:, 1:]
    return n_nodes, n_vehicles, n_calls, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo, TravelCost, FirstTravelCost, PortCost


@jit(nopython=True)
def get_feasibility_cost(solution, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo):
    NotTransportCost = 0
    RouteTravelCost = np.zeros(n_vehicles)
    CostInPorts = np.zeros(n_vehicles)
    
    solution = np.append(solution, [0])
    ZeroIndex = np.where(solution == 0)[0]
    ZeroIndex = ZeroIndex.astype('int64')
    feasibility = True
    tempidx = 0

    for i in range(n_vehicles + 1): 
        currentVPlan = solution[tempidx:ZeroIndex[i]]
        currentVPlan = currentVPlan - 1
        currentVPlanLength = len(currentVPlan)
        tempidx = ZeroIndex[i] + 1

        if i == n_vehicles:
            # Calculate cost of not transporting
            NotTransportCost = np.sum(Cargo[currentVPlan, 3]) / 2
        else:
            if currentVPlanLength > 0:
                # Test for incompatible vessel and cargo
                allcand = np.zeros(currentVPlan.size)
                for j in range(len(currentVPlan)):
                    currentv = currentVPlan[j]
                    allcand[j] = VesselCargo[i, currentv]
                if not np.all(allcand):
                    return False, 0

                sortRout = np.sort(currentVPlan)
                I = np.argsort(currentVPlan, kind='quicksort')
                Indx = np.argsort(I, kind='quicksort')

                # Test for load size too high
                LoadSize = np.zeros(len(sortRout))
                for j in range(len(sortRout)):
                    LoadSize[j] = (-1) * Cargo[sortRout[j], 2]
                for j in range(int(len(LoadSize) / 2)):
                    LoadSize[j*2] = Cargo[sortRout[j*2], 2]
                LoadSize = LoadSize[Indx]
                if np.any(VesselCapacity[i] - np.cumsum(LoadSize) < 0):
                    return False, 0

                # Test for time windows out of bounds
                Timewindows = np.zeros((2, currentVPlanLength))
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
                ArriveTime = np.zeros(currentVPlanLength)
                currentTime = 0
                for j in range(currentVPlanLength):
                    ArriveTime[j] = max(currentTime + RouteTravelTime[j], Timewindows[0, j])
                    if ArriveTime[j] > Timewindows[1, j]:
                        return False, 0
                    currentTime = ArriveTime[j] + LU_Time[j]

                # Calculate route cost of current vehicle
                PortIndex = Cargo[sortRout, 1]
                PortIndex = PortIndex.astype("int64")
                PortIndex[::2] = Cargo[sortRout[::2], 0]
                PortIndex = PortIndex[Indx] - 1
                Diag = np.zeros(PortIndex.size - 1)
                for j in range(len(PortIndex) - 1):
                    Diag[j] = TravelCost[i, PortIndex[j], PortIndex[j+1]]
                FirstVisitCost = np.atleast_1d(np.array(FirstTravelCost[i, int(Cargo[currentVPlan[0], 0] - 1)]))
                IndividualRouteTravelCost = np.concatenate((FirstVisitCost, Diag))
                RouteTravelCost[i] = np.sum(IndividualRouteTravelCost)

                # Calculate port costs
                insert_elem = np.zeros(currentVPlan.size)
                for j in range(len(currentVPlan)):
                    insert_elem[j] = PortCost[i, currentVPlan[j]]
                CostInPorts[i] = np.sum(insert_elem) / 2
        
    cost = NotTransportCost + sum(RouteTravelCost) + sum(CostInPorts)
    return feasibility, cost
                



@jit(nopython=True)
def feasibility_check(solution, n_vehicles, Cargo, TravelTime, FirstTravelTime, VesselCapacity, LoadingTime, UnloadingTime, VesselCargo):
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
        currentVPlanLength = len(currentVPlan)
        tempidx = ZeroIndex[i] + 1

        if currentVPlanLength > 0:
            allcand = np.zeros(currentVPlan.size)
            for j in range(len(currentVPlan)):
                currentv = currentVPlan[j]
                allcand[j] = VesselCargo[i, currentv]

            if not np.all(allcand):
                return False
            
            sortRout = np.sort(currentVPlan)
            I = np.argsort(currentVPlan, kind='quicksort')
            Indx = np.argsort(I, kind='quicksort')




            LoadSize = np.zeros(len(sortRout))
            for j in range(len(sortRout)):
                LoadSize[j] = (-1) * Cargo[sortRout[j], 2]
            for j in range(int(len(LoadSize) / 2)):
                LoadSize[j*2] = Cargo[sortRout[j*2], 2]
            
            LoadSize = LoadSize[Indx]
            if np.any(VesselCapacity[i] - np.cumsum(LoadSize) < 0):
                return False

            Timewindows = np.zeros((2, currentVPlanLength))
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
            ArriveTime = np.zeros(currentVPlanLength)

            currentTime = 0
            for j in range(currentVPlanLength):
                ArriveTime[j] = max(currentTime + RouteTravelTime[j], Timewindows[0, j])
                if ArriveTime[j] > Timewindows[1, j]:
                    return False
                currentTime = ArriveTime[j] + LU_Time[j]

    return feasibility

@jit(nopython=True)
def cost_function(solution, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost):
    """
    :param solution: the proposed solution for the order of calls in each vehicle
    :return:
    """

    NotTransportCost = 0
    RouteTravelCost = np.zeros(n_vehicles)
    CostInPorts = np.zeros(n_vehicles)

    solution = np.append(solution, [0])
    ZeroIndex = np.where(solution == 0)[0]
    ZeroIndex = ZeroIndex.astype('int64')
    tempidx = 0

    for i in range(n_vehicles + 1):
        currentVPlan = solution[tempidx:ZeroIndex[i]]
        currentVPlan = currentVPlan - 1
        currentVPlanLength = len(currentVPlan)
        tempidx = ZeroIndex[i] + 1

        if i == n_vehicles:
            NotTransportCost = np.sum(Cargo[currentVPlan, 3]) / 2
        else:
            if currentVPlanLength > 0:
                sortRout = np.sort(currentVPlan)
                I = np.argsort(currentVPlan, kind='quicksort')
                Indx = np.argsort(I, kind='quicksort')

                PortIndex = Cargo[sortRout, 1]
                PortIndex = PortIndex.astype("int64")
                PortIndex[::2] = Cargo[sortRout[::2], 0]
                PortIndex = PortIndex[Indx] - 1

                Diag = np.zeros(PortIndex.size - 1)
                for j in range(len(PortIndex) - 1):
                    Diag[j] = TravelCost[i, PortIndex[j], PortIndex[j+1]]

                FirstVisitCost = np.atleast_1d(np.array(FirstTravelCost[i, int(Cargo[currentVPlan[0], 0] - 1)]))
                IndividualRouteTravelCost = np.concatenate((FirstVisitCost, Diag))
                RouteTravelCost[i] = np.sum(IndividualRouteTravelCost)

                insert_elem = np.zeros(currentVPlan.size)
                for j in range(len(currentVPlan)):
                    insert_elem[j] = PortCost[i, currentVPlan[j]]

                CostInPorts[i] = np.sum(insert_elem) / 2

    TotalCost = NotTransportCost + sum(RouteTravelCost) + sum(CostInPorts)
    return TotalCost

@jit(nopython=True)
def handle_init_costs(sol, n_vehicles, n_calls, Cargo, TravelCost, FirstTravelCost, PortCost):
    costs = np.zeros((n_calls, 3), dtype="float64")
    vidx = 0
    for i in range(len(sol)):
        if sol[i] == 0:
            vidx += 1
        else:
            cand_sol = [0] * vidx + [sol[i]] * 2 + [0] * (n_vehicles - vidx)
            cost = cost_function(cand_sol, n_vehicles, Cargo, TravelCost, FirstTravelCost, PortCost)
            costs[sol[i]-1, 0] = cost
            costs[sol[i]-1, 1] = 0 if vidx < (n_vehicles) else 1
            costs[sol[i]-1, 2] = sol[i]
    return costs