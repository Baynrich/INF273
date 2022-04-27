import numpy as np
from utils import cost_function

def printer(costs_iter, sols_iter, init_cost, times_iter, problem):
    print("init_cost", init_cost)



    best_local_1opt = min(costs_iter[0])
    print("Avg Local 1-opt", np.mean(costs_iter[0]))
    print("Best Local 1-opt", best_local_1opt)
    print("Improvement%", (init_cost - best_local_1opt) / init_cost)
    print("Time", sum(times_iter[0]))

    best_local_2opt = min(costs_iter[1])
    print("Avg Local 2-opt", np.mean(costs_iter[1]))
    print("Best Local 2-opt", best_local_2opt)
    print("Improvement%", (init_cost - best_local_2opt) / init_cost) 
    print("Time", sum(times_iter[1]))

    best_local_3opt = min(costs_iter[2])
    print("Avg Local 3-opt", np.mean(costs_iter[2]))
    print("Best Local 3-opt", best_local_3opt)
    print("Improvement%", (init_cost - best_local_3opt) / init_cost) 
    print("Time", sum(times_iter[2]))


    best_anneal_1opt = min(costs_iter[3])
    print("Avg Anneal 1-opt", np.mean(costs_iter[3]))
    print("Best Anneal 1-opt", best_anneal_1opt)
    print("Improvement%", (init_cost - best_local_2opt) / init_cost) 
    print("Time", sum(times_iter[3]))


    best_anneal_2opt = min(costs_iter[4])
    print("Avg Anneal 2-opt", np.mean(costs_iter[4]))
    print("Best Anneal 2-opt", best_anneal_2opt)
    print("Improvement%", (init_cost - best_local_2opt) / init_cost) 
    print("Time", sum(times_iter[4]))


    best_anneal_3opt = min(costs_iter[5])
    print("Avg Anneal 3-opt", np.mean(costs_iter[5]))
    print("Best Anneal 3-opt", best_anneal_3opt)
    print("Improvement%", (init_cost - best_local_3opt) / init_cost)
    print("Time", sum(times_iter[5]))

    bestsol = []
    bestsolcost = float('inf')
    for sols in sols_iter:
        for sol in sols:
            if cost_function(sol, problem) < bestsolcost:
                bestsol = sol
    print(bestsol)