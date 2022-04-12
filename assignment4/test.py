from utils import *
from nbors import *
from printer import *
from methods import *
from nbors import *


filename = "Call_7_Vehicle_3.txt"
prob = load_problem("./" + filename)
print(assign_all_retireds([1, 1, 0, 2, 2, 0, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7], prob))


