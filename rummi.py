from rummi_output import *
from rummi_util import *
import multiprocessing as mp
from timeit import default_timer

stones = "stones"
colors = "colors"
copies = "copies"
minimal_size = "minimal_size"

#Returns all possible runs that can be layed on the table given table size, handsize and minimal run size
#Not all options returned are necessarily allowed, this is determined by placeRun()
def determinePossibleRuns(cfg, remaining_hand, run_size): #456
    options = []
    if (remaining_hand-run_size) >= cfg[minimal_size]:
        options.append(run_size)
        options += determinePossibleRuns(cfg, remaining_hand, run_size+1)
    else:
        options.append(remaining_hand)
    return options

#Places the given run on the table; returns false when it fails
def placeRun(cfg, table, i, row, run_size):
    for each in range(run_size):
        if table[row][each + i] == cfg[copies]:
            return False
        else:
            table[row][each + i] += 1
    return table

#Returns all possible group combinations that are allowed to be put on the table; returns false when it fails
def determinePossibleGroups(cfg, table, col, group_size): #444
    group_list = [0,1,2,3]
    for i in range(cfg[colors]):
        if table[i][col] == cfg[copies]:
            group_list.remove(i)
    if len(group_list) < cfg[minimal_size]:
        return False
    else:
        group_list = findSubsets(group_list, group_size)
        return group_list

#Places group on the table. No checks are done in this function, this is all done in determinePossibleGroups()
def placeGroup(table, col, group):
    for i in group:
        table[i][col] += 1
    return table

#i: index for where to continue looping in the table
#on_row: index for what row on the table; when negative we are looping on columns with i as index
def recursiveCount(args):
    on_row, i, remaining_hand, table, solutions, cfg = args
    if table == False:
        return solutions
    elif remaining_hand == 0:
        solutions.add(hashTable(table))
        return solutions
    else:
        options = determinePossibleRuns(cfg, remaining_hand, cfg[minimal_size])
        i_backup = i
        on_row_backup = on_row
        for allowed_option in options:
            i = i_backup
            on_row = on_row_backup
            #Looping over the rows
            while on_row > - 1:
                while (cfg[stones] - i) >= allowed_option: 
                    solutions = recursiveCount(
                        [on_row, 
                        i, 
                        remaining_hand - allowed_option, 
                        placeRun(cfg, copyTable(table), i, on_row, allowed_option), 
                        solutions,
                        cfg])
                    i += 1
                if on_row < (cfg[colors] - 1): on_row += 1
                else: on_row = -1
                i = 0
            #Looping over the colums
            if allowed_option >= cfg[minimal_size] and allowed_option <= cfg[colors]:
                while i != cfg[stones]:
                    group_options = determinePossibleGroups(cfg, table, i, allowed_option)
                    if group_options != False:
                        for g in group_options:
                            solutions = recursiveCount(
                                [on_row, 
                                i, 
                                remaining_hand - allowed_option, 
                                placeGroup(copyTable(table), i, g), 
                                solutions,
                                cfg])
                    i += 1
        return solutions

# Lists all recursive function calls for the first level of recursion. 
# This can be easily return 
def createTaskList(cfg, hand_size):
    table = initTable(cfg[colors], cfg[stones])
    options = determinePossibleRuns(cfg, hand_size, cfg[minimal_size])
    on_rows = list(range(0,cfg[colors]))
    on_rows.append(-1)
    tasks = []
    for option in options:
        for on_row in on_rows:
            #Task list for rows
            if on_row == -1 and option <= cfg[colors] :
                for i in range(0, cfg[stones]):
                    for g in determinePossibleGroups(cfg, table, i, option):
                        tasks.append([on_row, i, hand_size-option, (placeGroup(copyTable(table), i, g)), set() , cfg])
            #Tasklist for columns
            elif on_row != -1 and option <= 5:
                for i in range(0,cfg[stones]-option+1):
                    tasks.append([on_row, i, hand_size-option, placeRun(cfg, copyTable(table), i, on_row, option), set(),cfg])
    return tasks

# Wrapper for the recursive calls
# Support for multicoreprocessing
def perfCallRecCount(hand_size, nmax, k , m, cores):
    #initializing vars
    config = {stones:nmax, colors:k, copies:m, minimal_size:3}
    pool = mp.Pool(cores)
    tasks = createTaskList(config, hand_size)
    peak_memory = 0
    memory = 0
    task_count = 0
    imapsol = set()
    printTaskList(hand_size, len(tasks), cores)
    #Calculation start
    start = default_timer()
    for ip in pool.imap_unordered(recursiveCount, tasks):
        for i in ip:
            imapsol.add(i)
        memory = memoryUsage()
        if  memory > peak_memory:
            peak_memory = memory
        printCurrentTask(memory, peak_memory, len(tasks), task_count)
        task_count += 1
    stop = default_timer()
    pool.close()
    pool.join()
    # Returns: Lengt of the solution set, time taken to calculate en storage size of the solution list
    return [len(imapsol), round(stop - start,2), memory, peak_memory]

# Wrapper for the recursive calls
# No support for multicoreprocessing
def callRecCount(hand_size, nmax, k , m):
    config = {stones:nmax, colors:k, copies:m, minimal_size:3}
    table = initTable(colors, stones)
    solutions = set()
    start = default_timer()
    solutions = recursiveCount([0,0, hand_size, table, solutions, config])
    stop = default_timer()
    return (len(solutions), round(stop - start,2))