from utils import *
from nbors import *
from printer import *
from methods import *
import json
from utils import *

def print1darray(array):
    liststr = "["
    for i, row in enumerate(array):
        liststr += str(int(row))
        if i != len(array) - 1:
            liststr += ", "
    liststr += "]"
    return liststr

def print2darray(array):
    liststr = "["
    for i, row in enumerate(array):
        liststr += "{"
        for j, elem in enumerate(row):
            liststr += str(int(elem))
            if j != len(row) - 1:
                liststr += ","
        liststr += "}"
    liststr += "]"
    return liststr

def print3darray(array):
    liststr = "["
    for i, a in enumerate(array):
        liststr += "{"
        for j, b in enumerate(a):
            liststr += "("
            for k, c in enumerate(b):
                liststr += str(int(c))
                if k != len(b) - 1:
                    liststr += ", "
            liststr += ")"
        liststr += "}"
    liststr += "]"
    return liststr 



filename = "Call_7_Vehicle_3.txt"
prob = load_problem("./" + filename)

print(cost_function([0, 5, 5, 0, 7, 7, 0, 3, 4, 2, 6, 4, 2, 1, 1, 3, 6], prob))

#print(prob["TravelTime"].shape)
#print(feasibility_check([0, 3, 3, 0, 5, 5, 7, 7, 0, 6, 6, 1, 1, 4, 4, 2, 2], prob))

"""
with open("data" + filename, "w") as f:
    f.write("n_nodes:" + str(prob["n_nodes"]) + "\n")
    f.write("n_vehicles:" + str(prob["n_vehicles"]) + "\n")
    f.write("n_calls:" + str(prob["n_calls"]) + "\n")
    f.write("Cargo:" + print2darray(prob["Cargo"]) + "\n")
    f.write("TravelTime:" + print3darray(prob["TravelTime"]) + "\n")
    f.write("FirstTravelTime:" + print2darray(prob["FirstTravelTime"]) + "\n")
    f.write("VesselCapacity:" + print1darray(prob["VesselCapacity"]) + "\n")
    f.write("LoadingTime:" + print2darray(prob["LoadingTime"]) + "\n")
    f.write("UnloadingTime:" + print2darray(prob["UnloadingTime"]) + "\n")
    f.write("VesselCargo:" + print2darray(prob["VesselCargo"]) + "\n")
    f.write("TravelCost:" + print3darray(prob["TravelCost"]) + "\n")
    f.write("FirstTravelCost:" + print2darray(prob["FirstTravelCost"]) + "\n")
    f.write("PortCost:" + print2darray(prob["PortCost"]) + "\n")
"""

print(str([1, 2, 3]))