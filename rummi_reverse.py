from rummi_util import initTable, memoryUsage
from rummi_output import writeResult
from itertools import chain
import c_rummikub
from sys import argv
from timeit import default_timer

colors = 4
copies = 2 # ONLY WORKS FOR 2

def findSubsets(solutions, reference, to_remove, i = 0):
    lenght = len(reference)
    if to_remove > 1:
        remove_options = range(1, copies+1)
    else:
        remove_options = [1]
    while(i<lenght):
        for each in remove_options:
            copy = reference[:]
            copy[i] = copy[i] - each
            if to_remove - each != 0:
                findSubsets(solutions, copy[:], (to_remove - each), i+1)
            else:
                solutions.append(copy)
                if(len(solutions)%1000 == 0):
                    print("Finding subsets milestone ", len(solutions))
        i += 1

def reverseCount(hand, stones, colors, copies, cores):
    # Initialize variables
    maxhand = stones * copies * colors
    to_remove = maxhand - hand
    start = default_timer()
    solutions = list()
    cR = c_rummikub.cRummikub(cores, stones, colors, copies)
    print("Initializing. n", stones, "k", colors, "m", copies, "c", cores, "")
    # Generating a starting table
    table = initTable(colors, stones, copies)
    table = list(chain(*table))
    init = default_timer()
    print("Initialized. Time taken:", round(init - start,2), "\nFinding subsets...")

    # Find unique subsets
    findSubsets(solutions, table, to_remove)
    subset = default_timer()
    print("Found", len(solutions), "possible subsets. Time taken:", round(subset - init,2), "\nExecuting...")

    # Execute the determined situations
    result = None#cR.delegate(solutions)
    execution = default_timer()
    print("Execution done. Time taken:", round(subset - execution,2))

    # Finalizing
    stop = default_timer()
    memory = memoryUsage()
    print(writeResult(hand, stones, colors, copies, cores, [result, round(stop - start,2), memory, "botup"]))
    print("Winning hands:", result)

if __name__ == '__main__':
    stones = 6
    maxhand = 46
    minhand = 46#maxhand - 1
    cores = 4
    if len(argv) == 5:
        maxhand = int(argv[1])
        minhand = int(argv[2])
        stones = int(argv[3])
        cores = int(argv[4])
    elif len(argv)>1 and len(argv) != 5:
        print("Invalid amount of arguments. Must be either none or 4.")
        quit()
    for hand in reversed(range(minhand, maxhand+1)):
        reverseCount(hand, stones, colors, copies, cores)