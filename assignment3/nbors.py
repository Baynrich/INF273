def oneopt_operator_nborhood(cur_sol):
    nbors = []
    for i in range(len(cur_sol)):
        currentlist = []
        workable = cur_sol.copy()
        item_to_insert = workable.pop(i)
        for j in range(len(cur_sol)):
            if i == j or cur_sol[i] == cur_sol[j]:
                continue
            insertable = workable.copy()
            insertable.insert(j, item_to_insert)
            if insertable != cur_sol and solution_sanity(insertable):
                currentlist.append(insertable)
        nbors = nbors + currentlist
    retval = []
    for nbor in nbors:
        if nbor not in retval:
            retval.append(nbor)
    return retval

def twoopt_operator_nborhood(cur_sol):
    nbors = []
    for i in range(len(cur_sol)):
        for j in range(len(cur_sol)):
            if i == j or cur_sol[i] == cur_sol[j]:
                continue
            insertable = cur_sol.copy()
            i_val = insertable[i]
            insertable[i] = insertable[j]
            insertable[j] = i_val
            if insertable != cur_sol and solution_sanity(insertable):
                nbors.append(insertable)
    retval = []
    for nbor in nbors:
        if nbor not in retval:
            retval.append(nbor)
    return retval

def threeopt_operator_nborhood(cur_sol):
    nbors = []
    for i in range(len(cur_sol)):
        for j in range(len(cur_sol)):
            for k in range(len(cur_sol)):
                if (i == j or j == k or i == k) or (cur_sol[i] == cur_sol[j] and cur_sol[j] == cur_sol[k]):
                    continue
                insertable = cur_sol.copy()
                i_val = insertable[i]
                j_val = insertable[j]
                k_val = insertable[k]
                insertable[i] = k_val
                insertable[j] = i_val
                insertable[k] = j_val
                if insertable != cur_sol and solution_sanity(insertable):
                    nbors.append(insertable)
    retval = []
    for nbor in nbors:
        if nbor not in retval:
            retval.append(nbor)
    return retval


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