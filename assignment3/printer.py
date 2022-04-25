import numpy as np
from utils import cost_function

def printer(costs_iter, sols_iter, init_cost, times_iter, problem):
    best_local_1opt = min([op[0] for op in costs_iter])
    print("Avg Local 1-opt", np.mean([op[0] for op in costs_iter]))
    print("Best Local 1-opt", best_local_1opt)
    print("Improvement%", (init_cost - best_local_1opt) / init_cost)
    print("Time", sum([t[0] for t in times_iter]))

    best_local_2opt = min([op[1] for op in costs_iter])
    print("Avg Local 2-opt", np.mean([op[1] for op in costs_iter]))
    print("Best Local 2-opt", best_local_2opt)
    print("Improvement%", (init_cost - best_local_2opt) / init_cost) 
    print("Time", sum([t[1] for t in times_iter]))

    best_local_3opt = min([op[2] for op in costs_iter])
    print("Avg Local 3-opt", np.mean([op[2] for op in costs_iter]))
    print("Best Local 3-opt", best_local_3opt)
    print("Improvement%", (init_cost - best_local_3opt) / init_cost) 
    print("Time", sum([t[2] for t in times_iter]))


    best_anneal_1opt = min([op[3] for op in costs_iter])
    print("Avg Anneal 1-opt", np.mean([op[3]for op in costs_iter]))
    print("Best Anneal 1-opt", best_anneal_1opt)
    print("Improvement%", (init_cost - best_local_2opt) / init_cost) 
    print("Time", sum([t[3] for t in times_iter]))


    best_anneal_2opt = min([op[4] for op in costs_iter])
    print("Avg Anneal 2-opt", np.mean([op[4] for op in costs_iter]))
    print("Best Anneal 2-opt", best_anneal_2opt)
    print("Improvement%", (init_cost - best_local_2opt) / init_cost) 
    print("Time", sum([t[4] for t in times_iter]))


    best_anneal_3opt = min([op[5] for op in costs_iter])
    print("Avg Anneal 3-opt", np.mean([op[5] for op in costs_iter]))
    print("Best Anneal 3-opt", best_anneal_3opt)
    print("Improvement%", (init_cost - best_local_3opt) / init_cost)
    print("Time", sum([t[5] for t in times_iter]))

    bestsol = []
    bestsolcost = float('inf')
    for sols in sols_iter:
        for sol in sols:
            if cost_function(sol, problem) < bestsolcost:
                bestsol = sol


    print(bestsol)