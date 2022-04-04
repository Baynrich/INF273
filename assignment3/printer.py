import numpy as np

def printer(costs_iter, sols_iter, init_cost):
    """
    best_local_1opt = min([op[0] for op in costs_iter])
    print("Avg Local 1-opt", np.mean([op[0] for op in costs_iter]))
    print("Best Local 1-opt", best_local_1opt)
    print("Improvement%", (init_cost - best_local_1opt) / 100)

    best_local_2opt = min([op[1] for op in costs_iter])
    print("Avg Local 2-opt", np.mean([op[1] for op in costs_iter]))
    print("Best Local 2-opt", best_local_2opt)
    print("Improvement%", (init_cost - best_local_2opt) / 100) 

    best_local_3opt = min([op[2] for op in costs_iter])
    print("Avg Local 3-opt", np.mean([op[2] for op in costs_iter]))
    print("Best Local 3-opt", best_local_3opt)
    print("Improvement%", (init_cost - best_local_3opt) / 100) 


    best_anneal_1opt = min([op[0] for op in costs_iter])
    print("Avg Anneal 1-opt", np.mean([op[0]for op in costs_iter]))
    print("Best Anneal 1-opt", best_anneal_1opt)
    print("Improvement%", (init_cost - best_local_2opt) / 100) 

    best_anneal_2opt = min([op[1] for op in costs_iter])
    print("Avg Anneal 2-opt", np.mean([op[1] for op in costs_iter]))
    print("Best Anneal 2-opt", best_anneal_2opt)
    print("Improvement%", (init_cost - best_local_2opt) / 100) 

    best_anneal_3opt = min([op[2] for op in costs_iter])
    print("Avg Anneal 3-opt", np.mean([op[2] for op in costs_iter]))
    print("Best Anneal 3-opt", best_anneal_3opt)
    print("Improvement%", (init_cost - best_local_3opt) / 100) 
    """
    print(init_cost)
    print(sols_iter)
    print(costs_iter)