from functools import cache
from hashlib import new
import heapq as hq
from itertools import combinations
from operator import truediv
import sys
import copy
import time
from turtle import back

def read_and_parse(path):
    f = open(path, 'r')
    contents = f.readlines()
    row_constraints = []
    col_constraints = []
    f.close()
    for i in range(len(contents[0]) - 1):
        row_constraints.append(int(contents[0][i]))
        col_constraints.append(int(contents[1][i]))

    subs = int(contents[2][0])
    destroyers = 0 
    cruisers = 0
    battleships = 0

    if contents[2][1] != '\n':
        destroyers = int(contents[2][1])
        if contents[2][2] != '\n':
            cruisers = int(contents[2][2])
            if contents[2][3] != '\n':
                battleships = int(contents[2][3])
    grid = []

    for i in range(3, len(contents)):

        if contents[i][-1] == '\n':

            s = contents[i][:-1]
        else:
            s = contents[i]
        
        grid.append(s)

    return grid, row_constraints, col_constraints, subs, destroyers, cruisers, battleships

def output_format(grid):
    r = ""
    for i in range(len(grid)):
        # for n in range(len(grid[i])):
        r = r + grid[i]
        r = r + '\n'
    return r[:-1]

def find_combinations(dom, trues_left):
    
    if trues_left == 0:
        for i in range(len(dom)):
            if dom[i] is None: # != bool or type(dom[i]) != str:
                dom[i] = False
        return [dom]
    
    if len(dom) == 1 and dom[0] is None and trues_left == 1: # (type(dom[0]) != bool or type(dom[0]) != str)
        return [[True]]

    elif len(dom) == 1:
        return []
    
    else:
        if dom[0] is None:
            opt1 = []
            opt2 = []
            for c in find_combinations(dom[1:], trues_left - 1):
                opt1.append([True] + c)
            for c in find_combinations(dom[1:], trues_left):
                opt2.append([False] + c)
            
            return opt1 + opt2
        else:
            res = []
            for c in find_combinations(dom[1:], trues_left):
                res.append([dom[0]] + c)

            return res



def domain_create(grid, row_constraints, col_constraints):
    
    col_counts = [0] * len(grid)
    counts = [0] * len(grid)
    final = []
    domains = []
    for i in range(len(grid)):
        domains.append([None] * len(grid))

    for j in range(len(grid)):
        
        row = grid[j]
        dom = domains[j]
        

        for i in range(len(row)):

            # if row_constraints[j] == counts[j]:
            #     dom[i] = False

            # if col_constraints[i] == col_counts[i]:
            #     dom[i] = False
            
            if row[i] == 'W':
                dom[i] = False
            if row[i] == 'S':
                counts[j] += 1
                col_counts[i] += 1
                dom[i] = 'S' # True
                if j + 1 < len(grid):
                    domains[j + 1][i] = False
                if j - 1 >= 0:
                    domains[j - 1][i] = False

                if i + 1 < len(row):
                    dom[i+1] = False
                    if j + 1 < len(grid):
                        domains[j + 1][i + 1] = False
                    if j - 1 >= 0:
                        assert(domains[j - 1][i + 1] == None or not domains[j - 1][i + 1])
                        domains[j - 1][i + 1] = False
                if i - 1 >= 0:
                    dom[i-1] = False
                    if j + 1 < len(grid):
                        domains[j + 1][i - 1] = False
                    if j - 1 >= 0:
                        assert(domains[j - 1][i - 1] == None or not domains[j - 1][i - 1])
                        domains[j - 1][i - 1] = False
                
            if row[i] == 'L':
                counts[j] += 1
                col_counts[i] += 1
                dom[i] = 'L' # True
                assert(i + 1 < len(row))
                counts[j] += 1
                col_counts[i + 1] += 1
                dom[i + 1] = True

                if j + 1 < len(grid):
                    domains[j + 1][i] = False
                if j - 1 >= 0:
                    domains[j - 1][i] = False

                if i - 1 >= 0:
                    dom[i-1] = False
                    if j + 1 < len(grid):
                        domains[j + 1][i - 1] = False
                    if j - 1 >= 0:
                        assert(domains[j - 1][i - 1] == None or not domains[j - 1][i - 1])
                        domains[j - 1][i - 1] = False
                if i + 1 < len(row):
                    if j + 1 < len(grid):
                        domains[j + 1][i + 1] = False
                    if j - 1 >= 0:
                        assert(domains[j - 1][i + 1] == None or not domains[j - 1][i + 1])
                        domains[j - 1][i + 1] = False

                if i + 2 < len(grid):
                    if j + 1 < len(grid):
                        domains[j + 1][i + 2] = False
                    if j - 1 >= 0:
                        domains[j - 1][i + 2] = False

            if row[i] == 'R':
                dom[i] = 'R' # True
                counts[j] += 1
                col_counts[i] += 1
                assert(i - 1 >= 0)
                dom[i - 1] = True
                counts[j] += 1
                col_counts[i - 1] += 1

                if j + 1 < len(grid):
                    domains[j + 1][i] = False
                if j - 1 >= 0:
                    domains[j - 1][i] = False

                if i - 1 >= 0:
                    if j + 1 < len(grid):
                        domains[j + 1][i - 1] = False
                    if j - 1 >= 0:
                        assert(domains[j - 1][i - 1] == None or not domains[j - 1][i - 1])
                        domains[j - 1][i - 1] = False
                if i + 1 < len(row):
                    dom[i + 1] = False
                    if j + 1 < len(grid):
                        domains[j + 1][i + 1] = False
                    if j - 1 >= 0:
                        assert(domains[j - 1][i + 1] == None or not domains[j - 1][i + 1])
                        domains[j - 1][i + 1] = False

                if i - 2 >= 0:
                    if j + 1 < len(grid):
                        domains[j + 1][i - 2] = False
                    if j - 1 >= 0:
                        domains[j - 1][i - 2] = False

            if row[i] == 'M':
                dom[i] = 'M' # True
                counts[j] += 1
                col_counts[i] += 1
                if i - 1 >= 0:
                    if j + 1 < len(grid):
                        domains[j + 1][i - 1] = False
                    if j - 1 >= 0:
                        assert(domains[j - 1][i - 1] == None or not domains[j - 1][i - 1])
                        domains[j - 1][i - 1] = False
                if i + 1 < len(row):
                    if j + 1 < len(grid):
                        domains[j + 1][i + 1] = False
                    if j - 1 >= 0:
                        assert(domains[j - 1][i + 1] == None or not domains[j - 1][i + 1])
                        domains[j - 1][i + 1] = False

            if row[i] == 'B':
                dom[i] = 'B' # True
                counts[j] += 1
                col_counts[i] += 1
                if j + 1 < len(grid):
                    domains[j + 1][i] = False
                if j - 1 >= 0:
                    domains[j - 1][i] = True
                    counts[j - 1] += 1
                    col_counts[i] += 1
                if i - 1 >= 0:
                    dom[i - 1] = False
                    if j + 1 < len(grid):
                        domains[j + 1][i - 1] = False
                    if j - 1 >= 0:
                        assert(domains[j - 1][i - 1] == None or not domains[j - 1][i - 1])
                        domains[j - 1][i - 1] = False
                if i + 1 < len(row):
                    dom[i + 1] = False
                    if j + 1 < len(grid):
                        domains[j + 1][i + 1] = False
                    if j - 1 >= 0:
                        assert(domains[j - 1][i + 1] == None or not domains[j - 1][i + 1])
                        domains[j - 1][i + 1] = False
                if j - 2 >= 0:
                    if i + 1 < len(grid):
                        domains[j - 2][i + 1] = False
                    if i - 1 < len(grid):
                        domains[j - 2][i - 1] = False
                

            if row[i] == 'T':
                dom[i] = 'T' # True
                counts[j] += 1
                col_counts[i] += 1
                if j + 1 < len(grid):
                    domains[j + 1][i] = True
                    counts[j + 1] += 1
                    col_counts[i] += 1
                if j - 1 >= 0:
                    domains[j - 1][i] = False
                if i - 1 >= 0:
                    dom[i - 1] = False
                    if j + 1 < len(grid):
                        domains[j + 1][i - 1] = False
                    if j - 1 >= 0:
                        assert(domains[j - 1][i - 1] == None or not domains[j - 1][i - 1])
                        domains[j - 1][i - 1] = False
                if i + 1 < len(row):
                    dom[i + 1] = False
                    if j + 1 < len(grid):
                        domains[j + 1][i + 1] = False
                    if j - 1 >= 0:
                        assert(domains[j - 1][i + 1] == None or not domains[j - 1][i + 1])
                        domains[j - 1][i + 1] = False
                if j + 2 < len(grid):
                    if i + 1 < len(grid):
                        domains[j + 2][i + 1] = False
                    if i - 1 < len(grid):
                        domains[j + 2][i - 1] = False
                
                

        assert(counts[j] <= row_constraints[j])
    
    
    for j in range(len(domains)):
        for i in range(len(domains[i])):
            if row_constraints[j] == counts[j] and not domains[j][i]:
                domains[j][i] = False

            if col_constraints[i] == col_counts[i] and not domains[j][i]:
                domains[j][i] = False

    
    
    
    for i in range(len(grid)):
        
        final.append(find_combinations(domains[i], row_constraints[i] - counts[i]))

   
    return final

def verify_column(grid, col_constraints):

    
    for i in range(len(grid)):
        count = 0
        for n in range(len(grid)):
             if grid[n][i]:
                count += 1
        if count != col_constraints[i]:
            return False
    
    return True

def verify_column1(value, col_constraints):

   
    count = [0] * len(value)
    for i in range(len(value)):
        for n in range(len(value)):
             if value[i][n]:
                count[n] += 1
        if count[i] > col_constraints[i]:
            return False
    for i in range(len(value)):
        if count[i] != col_constraints[i]:
            return False
    
    return True

def convert_to_grid(grid):

    res = []
    
    for i in range(len(grid)):
        s = ""
        for n in range(len(grid[i])):
            if not grid[i][n]:
                s = s + 'W'
            else:

                if i + 1 < len(grid):
                        if n + 1 < len(grid):
                            if grid[i + 1][n + 1]:
                                return False
                        if n - 1 >= 0:
                            if grid[i + 1][n - 1]:
                                return False
                if i - 1 >= 0:
                    if n + 1 < len(grid):
                        if grid[i - 1][n + 1]:
                            return False
                    if n - 1 >= 0:
                        if grid[i - 1][n - 1]:
                            return False

                saturated = False

                if grid[i][n] == 'S' and (((i + 1 < len(grid) and not grid[i + 1][n]) or (i + 1 >= len(grid))) and 
                ((i - 1 >= 0 and not grid[i - 1][n]) or i - 1 < 0) and ((n + 1 < len(grid) 
                and not grid[i][n + 1]) or (n + 1 >= len(grid))) and 
                ((n - 1 >= 0 and not grid[i][n - 1]) or n - 1 < 0)):
                    s = s + 'S'
                    saturated = True

                
                if grid[i][n] == 'T' and (not ((i + 1 < len(grid) and not grid[i + 1][n]) or (i + 1 >= len(grid))) and 
                ((i - 1 >= 0 and not grid[i - 1][n]) or i - 1 < 0) and ((n + 1 < len(grid) 
                and not grid[i][n + 1]) or (n + 1 >= len(grid))) and 
                ((n - 1 >= 0 and not grid[i][n - 1]) or n - 1 < 0)):
                    s = s + 'T'
                    saturated = True
                
                if grid[i][n] == 'B' and (((i + 1 < len(grid) and not grid[i + 1][n]) or (i + 1 >= len(grid))) and 
                not ((i - 1 >= 0 and not grid[i - 1][n]) or i - 1 < 0) and ((n + 1 < len(grid) 
                and not grid[i][n + 1]) or (n + 1 >= len(grid))) and 
                ((n - 1 >= 0 and not grid[i][n - 1]) or n - 1 < 0)):
                    s = s + 'B'
                    saturated = True
                
                if grid[i][n] == 'R' and (((i + 1 < len(grid) and not grid[i + 1][n]) or (i + 1 >= len(grid))) and 
                ((i - 1 >= 0 and not grid[i - 1][n]) or i - 1 < 0) and ((n + 1 < len(grid) 
                and not grid[i][n + 1]) or (n + 1 >= len(grid))) and 
                not ((n - 1 >= 0 and not grid[i][n - 1]) or n - 1 < 0)):
                        s = s + 'R'
                        saturated = True
                    
                if grid[i][n] == 'L' and (((i + 1 < len(grid) and not grid[i + 1][n]) or (i + 1 >= len(grid))) and 
                ((i - 1 >= 0 and not grid[i - 1][n]) or i - 1 < 0) and not ((n + 1 < len(grid) 
                and not grid[i][n + 1]) or (n + 1 >= len(grid))) and 
                ((n - 1 >= 0 and not grid[i][n - 1]) or n - 1 < 0)):
                    s = s + 'L'
                    saturated = True
                
                if grid[i][n] == 'M' and (not ((i + 1 < len(grid) and not grid[i + 1][n]) or (i + 1 >= len(grid))) and 
                not ((i - 1 >= 0 and not grid[i - 1][n]) or i - 1 < 0) and ((n + 1 < len(grid) 
                and not grid[i][n + 1]) or (n + 1 >= len(grid))) and 
                ((n - 1 >= 0 and not grid[i][n - 1]) or n - 1 < 0)):
                    s = s + 'M'
                    saturated = True
                
                if grid[i][n] == 'M' and (((i + 1 < len(grid) and not grid[i + 1][n]) or (i + 1 >= len(grid))) and 
                ((i - 1 >= 0 and not grid[i - 1][n]) or i - 1 < 0) and not ((n + 1 < len(grid) 
                and not grid[i][n + 1]) or (n + 1 >= len(grid))) and 
                not ((n - 1 >= 0 and not grid[i][n - 1]) or n - 1 < 0)):
                    s = s + 'M'
                    saturated = True

                if type(grid[i][n]) == str and not saturated:
                    return False

                if not saturated:

                    # if it is a S
                    if (((i + 1 < len(grid) and not grid[i + 1][n]) or (i + 1 >= len(grid))) and 
                    ((i - 1 >= 0 and not grid[i - 1][n]) or i - 1 < 0) and ((n + 1 < len(grid) 
                    and not grid[i][n + 1]) or (n + 1 >= len(grid))) and 
                    ((n - 1 >= 0 and not grid[i][n - 1]) or n - 1 < 0)):
                        s = s + 'S'

                    # if it is a L
                    elif (not ((i + 1 < len(grid) and not grid[i + 1][n]) or (i + 1 >= len(grid))) and 
                    ((i - 1 >= 0 and not grid[i - 1][n]) or i - 1 < 0) and ((n + 1 < len(grid) 
                    and not grid[i][n + 1]) or (n + 1 >= len(grid))) and 
                    ((n - 1 >= 0 and not grid[i][n - 1]) or n - 1 < 0)):
                        s = s + 'T'

                    # if it a R
                    elif (((i + 1 < len(grid) and not grid[i + 1][n]) or (i + 1 >= len(grid))) and 
                    not ((i - 1 >= 0 and not grid[i - 1][n]) or i - 1 < 0) and ((n + 1 < len(grid) 
                    and not grid[i][n + 1]) or (n + 1 >= len(grid))) and 
                    ((n - 1 >= 0 and not grid[i][n - 1]) or n - 1 < 0)):
                        s = s + 'B'

                    
                    # if it a T
                    elif (((i + 1 < len(grid) and not grid[i + 1][n]) or (i + 1 >= len(grid))) and 
                    ((i - 1 >= 0 and not grid[i - 1][n]) or i - 1 < 0) and not ((n + 1 < len(grid) 
                    and not grid[i][n + 1]) or (n + 1 >= len(grid))) and 
                    ((n - 1 >= 0 and not grid[i][n - 1]) or n - 1 < 0)):
                        s = s + 'L'
                    
                    # if it is a B
                    elif (((i + 1 < len(grid) and not grid[i + 1][n]) or (i + 1 >= len(grid))) and 
                    ((i - 1 >= 0 and not grid[i - 1][n]) or i - 1 < 0) and ((n + 1 < len(grid) 
                    and not grid[i][n + 1]) or (n + 1 >= len(grid))) and 
                    not ((n - 1 >= 0 and not grid[i][n - 1]) or n - 1 < 0)):
                            s = s + 'R'
                    
                    elif (not ((i + 1 < len(grid) and not grid[i + 1][n]) or (i + 1 >= len(grid))) and 
                    not ((i - 1 >= 0 and not grid[i - 1][n]) or i - 1 < 0) and ((n + 1 < len(grid) 
                    and not grid[i][n + 1]) or (n + 1 >= len(grid))) and 
                    ((n - 1 >= 0 and not grid[i][n - 1]) or n - 1 < 0)):
                        s = s + 'M'
                    
                    elif (((i + 1 < len(grid) and not grid[i + 1][n]) or (i + 1 >= len(grid))) and 
                    ((i - 1 >= 0 and not grid[i - 1][n]) or i - 1 < 0) and not ((n + 1 < len(grid) 
                    and not grid[i][n + 1]) or (n + 1 >= len(grid))) and 
                    not ((n - 1 >= 0 and not grid[i][n - 1]) or n - 1 < 0)):
                        s = s + 'M'

                    else:
                        return False
                            
        res.append(s)
    
    return res
                        
                
               


def verify_num_ships(grid, subs, destroyers, cruisers, battleships):
    sub_count = 0
    dest_count = 0
    cruiser_count = 0
    bat_count = 0

    new_grid = convert_to_grid(grid)
    if not new_grid:
        return False
    for i in range(len(grid)):
        for n in range(len(grid)):
            if new_grid[i][n] == 'S':
                sub_count += 1
                if sub_count > subs:
                    return False
                # may need to verify the other constraint (diagonals especially)
            elif new_grid[i][n] == 'T':
                if new_grid[i + 1][n] == 'M':
                    if new_grid[i + 2][n] == 'M':
                        bat_count += 1
                        if bat_count > battleships or (len(new_grid) > i + 3 and new_grid[i + 3][n] == 'M'):
                            return False
                        
                    else:
                        cruiser_count += 1
                        if cruiser_count > cruisers:
                            return False
                else:
                    dest_count += 1
                    if dest_count > destroyers:
                        return False
            
            elif new_grid[i][n] == 'L':
                if new_grid[i][n + 1] == 'M':
                    if new_grid[i][n + 2] == 'M':
                        bat_count += 1
                        if bat_count > battleships:
                            return False
                    else:
                        cruiser_count += 1
                        if cruiser_count > cruisers:
                            return False
                else:
                    dest_count += 1
                    if dest_count > destroyers:
                        return False

    if subs != sub_count:
        return False
    if cruisers != cruiser_count:
        return False
    if dest_count != destroyers:
        return False
    if cruiser_count != cruisers:
        return False

    return True



def before(n):
    assigned = {}
    for i in range(n):
        assigned[i] = False
    return assigned

def backtrack(grid, row_constraints, col_constraints, subs, destroyers, cruisers, battleships, value, assigned, domains, cache1, path):

    unassigned = []
    count = 0
    for key in assigned:
        if assigned[key]:
            count +=1
        else:
            hq.heappush(unassigned, (len(domains[key]), key))
            # unassigned.append(key)
    if count == len(grid): #if all vars assigned
        # newgrid = []
        # for i in range(len(grid)):
        #     print(value[i])
        #     newgrid.append(value[i])
        final = output_format(convert_to_grid(value))
        print(final)
        f = open(path, "w")
        f.write(final)
        f.close()
        print("--- %s seconds ---" % (time.time() - start_time))
        exit()

    val, v = hq.heappop(unassigned)
    #  v = unassigned.pop()
    assigned[v] = True

    for d in domains[v]:
        value[v] = d
        constraintsok = True
        if unassigned == []:
            # newgrid = []
            # for i in range(len(grid)):
            #     newgrid.append(value[i])
            if not verify_column(value, col_constraints) or not verify_num_ships(value, subs, destroyers, cruisers, battleships):
            # if not verify_num_ships(newgrid, subs, destroyers, cruisers, battleships):
                constraintsok = False
        if constraintsok == True:
            # flag = False
            backtrack(grid, row_constraints, col_constraints, subs, destroyers, cruisers, battleships, value, assigned, domains, cache1, path)
            # if str(value) not in cache1:
            #     temp = str(value)
            #     backtrack(grid, row_constraints, col_constraints, subs, destroyers, cruisers, battleships, value, assigned, domains, cache1)
            #     cache1[temp] = value, assigned
            # else:
            #     value, assigned = cache1[str(value)]


            
            # if (str(value), str(assigned)) in cache1:
            #     flag = True
            # # for n in range(len(cache1)):
            # #     if cache1[n] == (str(value), str(assigned)):
            # #         flag = True
            # #         break
            # if not flag:
            #     temp = (str(value), str(assigned))
            #     backtrack(grid, row_constraints, col_constraints, subs, destroyers, cruisers, battleships, value, assigned, domains, cache1)
            #     cache1[temp] = (value, assigned)
            # #     cache2.append((value, assigned))
            # else:
                
            #     value, assigned = cache1[str(value), str(assigned)]

    assigned[v] = False
    return value

def FCCheck1(grid, row_dom, col_constraints, unassigned, pruned):

    # print(row_dom)
    i = 0
    count = 0
    while i < len(row_dom):
        grid[unassigned] = row_dom[i]
        # print(row_dom[i])
        # print(grid)
        if not verify_column(grid, col_constraints):
            if unassigned in pruned:
                pruned[unassigned] = pruned[unassigned] + [row_dom[i]]
            else:
                pruned[unassigned] = [row_dom[i]]
            row_dom.pop(i)
            i -= 1
        i += 1
        count += 1
    # print(count)
    # print(len(pruned))
    # print(i)
    # assert(count - i == len(pruned))
    if row_dom == []:
        return False # DWO
    else:
        return True

def FCCheck2(grid, row_dom, subs, destroyers, cruisers, battleships, unassigned, pruned):

    i = 0
    while i < len(row_dom):
        grid[unassigned] = row_dom[i]
        
        if not verify_num_ships(grid, subs, destroyers, cruisers, battleships):
            # pruned[unassigned] = row_dom[i]
            if unassigned in pruned:
                pruned[unassigned] = pruned[unassigned] + [row_dom[i]]
            else:
                pruned[unassigned] = [row_dom[i]]
            row_dom.pop(i)
            i -= 1
        i += 1
    if row_dom == []:
        return False # DWO
    else:
        return True
    

def forwardchecking(grid, row_constraints, col_constraints, subs, destroyers, cruisers, battleships, value, assigned, domains):

    unassigned = []
    count = 0
    for key in assigned:
        if assigned[key]:
            count +=1
        else:
            hq.heappush(unassigned, (len(domains[key]), key))
            # unassigned.append(key)
    if count == len(grid): #if all vars assigned
        newgrid = []
        for i in range(len(grid)):
            print(value[i])
            newgrid.append(value[i])
        print(output_format(convert_to_grid(newgrid)))
        print("--- %s seconds ---" % (time.time() - start_time))
        exit()

    # MRV make unassigned a heapq len(domains[unasigned])
    val, v = hq.heappop(unassigned)
    print(v)
    # v = unassigned.pop(0)
    assigned[v] = True
    pruned = {}
    for d in domains[v]:
        value[v] = d
        DWO = False
        if len(unassigned) == 1:
            newgrid = []
            # print(unassigned)
            for i in range(len(grid)):
                if i != unassigned[0][1]:
                    newgrid.append(value[i])
                if i == unassigned[0][1]:
                    newgrid.append([0] * len(grid))
           
            check = FCCheck1(newgrid, domains[unassigned[0][1]], col_constraints, unassigned[0][1], pruned)
            
            if not check:
                DWO = True
            else:
                check2 = FCCheck2(newgrid, domains[unassigned[0][1]], subs, destroyers, cruisers, battleships, unassigned[0][1], pruned)
                if not check2:
                    DWO = True
                    

        if not DWO:
            print(value)
            forwardchecking(grid, row_constraints, col_constraints, subs, destroyers, cruisers, battleships, value, assigned, domains)

        for key in pruned:
            # print(pruned)
            domains[key] = domains[key] + pruned[key]
        
    assigned[v] = False

    return value



def findA(c, domains, iandn):

    i, n = iandn
    final_assignment = []
    remainingVars = domains[:i] + domains[i + 1:]
    

    if remainingVars == []: # remaining vars is domains[:i] + domains[i:]
        
        c = 1
        #check if C satisfied

    var = remainingVars.pop()

    for val in var.curDomain():
        
        final_assignment.append((var, val))

    #some c's can be false w.o. full assignment, e.g., a sum

        if c: # C not already falsified:

            if findA(remainingVars, final_assignment):

                return True

        final_assignment.pop() #(var,val) didn't work

    remainingVars.append(var)

    return False

# findA(C.scope()-V, (V,d)) #V,d from your pseudocode

def gac_enforce(gac_queue, grid, row_constraints, col_constraints):

    domains = domain_create(grid, row_constraints,col_constraints)

    while gac_queue != []:
        c = gac_queue.pop()
        for i in range(len(grid)):
            for n in range(len(domains[i])):
                new_grid = []
                domains[i][n] # one assignment for variable i


                findA(c, domains, (i, n)) 


                # find combos of domain one by one
                # while flag:
                # l = 0
                # tried = {}
                # for j in range(len(domains)):
                    
                #     if j != i:
                #             l = 0
                #             while l < len(domains[j]):
                #                 if (j,l) not in tried:
                #                     tried[(j,l)] = 1
                #                     new_grid.append(domains[j][l])
                #                     break
                #                 else:
                #                     if tried[(j,l)] < len(grid) - 2:
                #                         new_grid.append(domains[j][l])
                #                         tried[(j,l)] += 1
                #                     else:
                #                         if l < len(domains[j]):
                #                             l += 1

                #     else:
                #         new_grid.append(domains[i][n])
                # # l += 1

                # if c == 1:
                #     verify_column(new_grid, col_constraints)
            


        



if __name__ == "__main__":
    start_time = time.time()
    # "C:\\Users\\nitin\\Downloads\\bat_test.txt"
    grid, row_constraints, col_constraints, subs, destroyers, cruisers, battleships = read_and_parse(sys.argv[1])
    
    # print(output_format(grid))

    # print(domain_create(grid, row_constraints))
    
    domains = domain_create(grid, row_constraints, col_constraints)
    # print(domains)
    assigned = before(len(grid))
    value = backtrack(grid, row_constraints, col_constraints, subs, destroyers, cruisers, battleships, {}, assigned, domains, {}, sys.argv[2])
    # value = forwardchecking(grid, row_constraints, col_constraints, subs, destroyers, cruisers, battleships, {}, assigned, domains)
   
    # newgrid = []
    # for i in range(len(grid)):
    #     print(value[i])
    #     newgrid.append(value[i])
    # print(output_format(convert_to_grid(newgrid)))
        
    print("--- %s seconds ---" % (time.time() - start_time))
