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
        i += 1

def reverseCount(cores = 7, stones = 7, colors = 4, copies = 2):
    # Initialize variables
    maxhand = stones * copies * colors
    to_remove = maxhand - hand
    start = default_timer()
    solutions = list()
    cR = c_rummikub.cRummikub(cores, stones, colors, copies)
    # Generating a starting table
    table = initTable(colors, stones, copies)
    table = list(chain(*table))

    # Find unique subsets
    findSubsets(solutions, table, to_remove)

    # Execute the determined situations
    result = cR.delegate(solutions)

    # Finalizing
    stop = default_timer()
    memory = memoryUsage()
    print(writeResult(hand, stones, colors, copies, cores, [result, round(stop - start,2), memory, "botup"]))
    print("Winning hands:", result)

if __name__ == '__main__':
    stones = 6
    maxhand = stones * colors * copies
    minhand = 47#maxhand - 1
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
        reverseCount(hand, stones, cores)