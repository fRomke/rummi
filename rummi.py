from rummi_output import *
from rummi_util import *
from rummi_settings import *
import multiprocessing as mp
from functools import partial
from timeit import default_timer

global_remaining_hand = 0 #temporary help variable, can remove later

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
    if len(args) != 5:
        print(args)
        quit()
    on_row, i, remaining_hand, table, solutions = args
    if table == False:
        return solutions
    elif remaining_hand == 0:
        #outputTable(table, output)
        solutions.add(hashTable(table))
        return solutions
    else:
        options = determinePossibleRuns(remaining_hand, minimal_size)
        #if remaining_hand == global_remaining_hand: print(options)
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
                            new_table = placeGroup(copyTable(table), i, g)
                            solutions = recursiveCount([on_row, 
                                i, 
                                remaining_hand - allowed_option, 
                                new_table, 
                                solutions])
                    i += 1
        return solutions
 

def perfCallRecCount(hand_size, nmax, k , m):
    global stones
    global copies
    global colors
    global output
    global print_to_file
    global global_remaining_hand
    global_remaining_hand = hand_size
    stones = nmax
    copies = m
    colors = k 
    table = initTable(colors, stones)
    solutions = set()
    pool  = mp.Pool(mp.cpu_count()-1)

    options = determinePossibleRuns(hand_size, minimal_size)
    on_rows = list(range(0,colors))
    q = []
    for option in options:
        for on_row in on_rows:
            for i in range(0,stones-option+1):
                q.append([on_row, i, hand_size, (placeRun(copyTable(table), i, on_row, option)), solutions])
    print(len(q))

    
    def collectResult(results):
        answer = set()
        for r in results:
            answer = answer.union(r)
        print(len(answer))

    mappie = pool.map_async(recursiveCount, q, callback=collectResult)
    #s = set(mappie)
    mappie.wait()
    print(len(answer))
    #print(len(mappie[0]))
    #solutions = recursiveCount((0,0), hand_size, table, solutions)

def callRecCount(hand_size, nmax, k , m):
    #Ugly, needs to be solved
    global stones
    global copies
    global colors
    global output
    global print_to_file
    global global_remaining_hand
    global_remaining_hand = hand_size
    stones = nmax
    copies = m
    colors = k 

    table = initTable(colors, stones)
    solutions = set()
    start = default_timer()
    solutions = recursiveCount((0,0), hand_size, table, solutions)
    stop = default_timer()
    if save_hash: 
        output = open('output.txt','w')
        writeSolutions(solutions)
        output.close()
    return (len(solutions), round(stop - start,2))

if __name__ == '__main__':
    perfCallRecCount(7, 13, 4, 2)