from rummi_output import *
from rummi_util import *
from rummi_settings import *
import multiprocessing as mp
from functools import partial
from timeit import default_timer
import time

def determinePossibleRuns(remaining_hand, run_size): #456
    options = []
    if (remaining_hand-run_size) >= minimal_size:
        options.append(run_size)
        options += determinePossibleRuns(remaining_hand, run_size+1)
    else:
        options.append(remaining_hand)
    return options

def placeRun(table, i, row, run_size):
    for each in range(run_size):
        if table[row][each + i] == copies:
            return False
        else:
            table[row][each + i] += 1
    return table

def determinePossibleGroups(table, col, group_size): #444
    group_list = [0,1,2,3]
    for i in range(colors):
        if table[i][col] == copies:
            group_list.remove(i)
    if len(group_list) < minimal_size:
        return False
    else:
        group_list = findSubsets(group_list, group_size)
        return group_list

def placeGroup(table, col, group):
    for i in group:
        table[i][col] += 1
    return table

#i: index for where to continue looping in the table
#on_row: index for what row on the table; when negative we are looping on columns with i as index
def recursiveCount(args):
    on_row, i, remaining_hand, table, solutions = args
    if table == False:
        return solutions
    elif remaining_hand == 0:
        solutions.add(hashTable(table))
        return solutions
    else:
        options = determinePossibleRuns(remaining_hand, minimal_size)
        i_backup = i
        on_row_backup = on_row
        for allowed_option in options: #stones=7 [3,4,7]
            i = i_backup
            on_row = on_row_backup
            while on_row > - 1: #Checking runs for all the rows
                while (stones - i) >= allowed_option: #kolommen in de rij
                    solutions = recursiveCount([on_row, 
                        i, 
                        remaining_hand - allowed_option, 
                        placeRun(copyTable(table), i, on_row, allowed_option), 
                        solutions])
                    i += 1
                if on_row < (colors - 1): on_row += 1
                else: on_row = -1
                i = 0
            if allowed_option >= minimal_size and allowed_option <= colors:
                while i != stones:#kolom
                    group_options = determinePossibleGroups(table, i, allowed_option)
                    if group_options != False:
                        for g in group_options:
                            solutions = recursiveCount([on_row, 
                                i, 
                                remaining_hand - allowed_option, 
                                placeGroup(copyTable(table), i, g), 
                                solutions])
                    i += 1
        return solutions
 

def createTaskList(hand_size):
    table = initTable(colors, stones)
    solutions = set()
    options = determinePossibleRuns(hand_size, minimal_size)
    on_rows = list(range(0,colors))
    on_rows.append(-1)
    tasks = []
    for option in options:
        for on_row in on_rows:
            if on_row == -1 and option <= colors :
                for i in range(0, stones):
                    for g in determinePossibleGroups(table, i, option):
                        tasks.append([on_row, i, hand_size-option, (placeGroup(copyTable(table), i, g)), solutions])
            elif on_row != -1 and option <= 5:
                for i in range(0,stones-option+1):
                    tasks.append([on_row, i, hand_size-option, (placeRun(copyTable(table), i, on_row, option)), solutions])
    return tasks

def perfCallRecCount(hand_size, nmax, k , m):
    #initializing vars
    global stones
    global copies
    global colors
    stones = nmax
    copies = m
    colors = k 
    pool = mp.Pool(mp.cpu_count()-1)  
    
    tasks = createTaskList(hand_size)

    #map unordered
    start = default_timer()
    imapsol = set()
    for ip in pool.imap_unordered(recursiveCount, tasks):
        for i in ip:
            imapsol.add(i)
    stop = default_timer()
    return (len(imapsol), round(stop - start,2))

def callRecCount(hand_size, nmax, k , m):
    #Ugly, needs to be solved
    global stones
    global copies
    global colors
    stones = nmax
    copies = m
    colors = k 

    table = initTable(colors, stones)
    solutions = set()
    start = default_timer()
    solutions = recursiveCount([0,0, hand_size, table, solutions])
    stop = default_timer()
    return (len(solutions), round(stop - start,2))