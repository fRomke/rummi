#algo2.0
from rummi_output import *
from rummi_util import *
import multiprocessing as mp
from timeit import default_timer
import rummi as rummi

stones = "stones"
colors = "colors"
copies = "copies"
minimal_size = "minimal_size"

#Returns all possible runs that can be layed on the table given table size, handsize and minimal run size
#Not all options returned are necessarily allowed, this is determined by placeRun()
def determinePossibleRuns(cfg, remaining_hand, run_size): #456
    # TODO Merge with the group version
    # TODO Variable 5, bugged for remaininghand = 6 or 7
    options = []
    if (remaining_hand-run_size) >= cfg[minimal_size]:
        options.append(run_size)
        if (run_size == 5):
            return options
        options += determinePossibleRuns(cfg, remaining_hand, run_size+1)
    elif run_size <= 5:
        options.append(remaining_hand)
    return options

def determinePossibleRunsForGroups(cfg, remaining_hand, run_size): #456
    # TODO Merge with the group version
    # TODO Variable 5, bugged for remaininghand = 6
    options = []
    if (remaining_hand-run_size) >= cfg[minimal_size]:
        options.append(run_size)
        if (run_size == min(cfg[colors], 5)):
            return options
        options += determinePossibleRunsForGroups(cfg, remaining_hand, run_size+1)
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
    return True

#Returns all possible group combinations that are allowed to be put on the table; returns false when it fails
def determinePossibleGroups2(cfg, table, col, remaining_hand): #444
    # TODO Remaining hand support
    group_list = list(range(cfg[colors]))
    for color in range(cfg[colors]):
        if table[color][col] == cfg[copies]:
            group_list.remove(color)
    if min(remaining_hand, len(group_list)) < cfg[minimal_size]:
        return False
    else:
        partitions = determinePossibleRunsForGroups(cfg, remaining_hand, cfg[minimal_size])
        possible_groups = []
        for part in partitions:
            possible_groups += findSubsets(group_list, part)
        return(possible_groups)      

#Places group on the table. No checks are done in this function, this is all done in determinePossibleGroups()
def placeGroup(table, col, group):
    for i in group:
        table[i][col] += 1
    return table

#Determines if there is even enough space to lay all the tiles on table from the given position
#The odds of this functions returning True will be bigger towards the end of the algorithm
def countFit(cfg, table, row, col, remaining_hand):
    table2 = list(chain(*table))
    i = row * cfg[stones] + col
    count = 0
    for k in range(i, len(table2)):
        if table2[k] == 1:
            count = count + 1
        elif table2[k] == 0:
            count = count + 2
    if remaining_hand > count:
        #print(remaining_hand, count, True, k)
        return False
    else:
        #print(remaining_hand, count, False, k)
        return True

#i: index for where to continue looping in the table
#on_row: index for what row on the table; when negative we are looping on columns with i as index
def recursiveCount(args):
    bak_row_index, bak_column_index, remaining_hand, table, solutions, cfg = args
    if table == False:
        return solutions
    elif remaining_hand == 0:
        solutions.add(hashTable(table))
        #printTableToFile(table, "table2.txt")
        return solutions
    else:
        #Columns
        row_index = bak_row_index
        column_index = bak_column_index
        if row_index == -1:
            while column_index != cfg[stones]:
                options = determinePossibleGroups2(cfg, table, column_index, remaining_hand)
                if options != False:
                    for option in options:
                        solutions = recursiveCount(
                                        [row_index, 
                                        column_index, 
                                        remaining_hand - len(option), 
                                        placeGroup(copyTable(table), column_index, option), 
                                        solutions,
                                        cfg])
                column_index += 1
            bak_row_index = 0
            bak_column_index = 0
        #Rows
        options = determinePossibleRuns(cfg, remaining_hand, cfg[minimal_size])
        for option in options:#for all options
            row_index = bak_row_index
            column_index = bak_column_index
            while row_index < cfg[colors]: #for all rows
                while (cfg[stones] - column_index) >= option: #option fits on current row
                    counted_fit = countFit(cfg, table, row_index, column_index, remaining_hand)
                    placed_run_table = copyTable(table)
                    placed_run = placeRun(cfg, placed_run_table, column_index, row_index, option)
                    if (counted_fit & placed_run):
                        #printTableToFile(table, "table2.txt")
                        solutions = recursiveCount(
                                    [row_index, 
                                    column_index, 
                                    remaining_hand - option, 
                                    placed_run_table, 
                                    solutions,
                                    cfg])
                    column_index += 1
                column_index = 0
                row_index += 1
        return solutions