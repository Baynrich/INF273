from utils import cost_function, feasibility_check
import random

def oneopt_operator_nborhood(cur_sol, prob):
    nbors = []

    startlook = random.randint(0, len(cur_sol))
    for i in [*range(startlook, len(cur_sol))] + [*range(0, startlook)]:
        currentlist = []
        workable = cur_sol.copy()
        item_to_insert = workable.pop(i)
        if len(nbors) < 1:
            startlook = random.randint(0, len(cur_sol))
            for j in [*range(startlook, len(cur_sol))] + [*range(0, startlook)]:
                if i == j or cur_sol[i] == cur_sol[j]:
                    continue
                insertable = workable.copy()
                insertable.insert(j, item_to_insert)
                
                if insertable != cur_sol and solution_sanity(insertable) and feasibility_check(insertable, prob):
                    currentlist.append(insertable)
                    break
        nbors = nbors + currentlist
    retval = []
    for nbor in nbors:
        if nbor not in retval:
            retval.append(nbor)
    return retval[0]

def twoopt_operator_nborhood(cur_sol, prob):
    nbors = []
    startlook = random.randint(0, len(cur_sol))
    for i in [*range(startlook, len(cur_sol))] + [*range(0, startlook)]:
        if len(nbors) < 1:
            startlook = random.randint(0, len(cur_sol))
            for j in [*range(startlook, len(cur_sol))] + [*range(0, startlook)]:
                if i == j or cur_sol[i] == cur_sol[j]:
                    continue
                insertable = cur_sol.copy()
                i_val = insertable[i]
                insertable[i] = insertable[j]
                insertable[j] = i_val
                if insertable != cur_sol and solution_sanity(insertable) and feasibility_check(insertable, prob):
                    nbors.append(insertable)
                    break
    retval = []
    for nbor in nbors:
        if nbor not in retval:
            retval.append(nbor)
    return retval[0]

def threeopt_operator_nborhood(cur_sol, prob):
    nbors = []
    startlook = random.randint(0, len(cur_sol))
    for i in [*range(startlook, len(cur_sol))] + [*range(0, startlook)]:
        if len(nbors) < 1:
            startlook = random.randint(0, len(cur_sol))
            for j in [*range(startlook, len(cur_sol))] + [*range(0, startlook)]:
                if len(nbors) < 1:
                    startlook = random.randint(0, len(cur_sol))
                    for k in [*range(startlook, len(cur_sol))] + [*range(0, startlook)]:
                        if (i == j or j == k or i == k) or (cur_sol[i] == cur_sol[j] and cur_sol[j] == cur_sol[k]):
                            continue
                        insertable = cur_sol.copy()
                        i_val = insertable[i]
                        j_val = insertable[j]
                        k_val = insertable[k]
                        insertable[i] = k_val
                        insertable[j] = i_val
                        insertable[k] = j_val
                        if insertable != cur_sol and solution_sanity(insertable) and feasibility_check(insertable, prob):
                            nbors.append(insertable)
                            break
    retval = []
    for nbor in nbors:
        if nbor not in retval:
            retval.append(nbor)
    return retval[0]


def solution_sanity(sol):
    """Ensures that any given solution both picks up and delivers its assigned calls"""
    currentcalls = []
    for i in range(len(sol)):
        if sol[i] == 0: 
            if len(currentcalls) > 0:
                return False
        else:
            if sol[i] in currentcalls:
                currentcalls.remove(sol[i])
            else:
                currentcalls.append(sol[i])
    
    for i in range(max(sol)):
        if i not in sol:
            return False
    return True