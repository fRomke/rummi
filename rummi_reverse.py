from rummi_util import initTable, memoryUsage
from rummi_output import writeResult, printTableToConsole
from itertools import chain
import c_rummikub
from sys import argv
from timeit import default_timer

colors = 4
copies = 2 # ONLY WORKS FOR 2

def findSubsets(solutions, reference, to_remove, i = 0):
    lenght = len(reference)
    if to_remove > 0:
        remove_options = range(1, to_remove+1)
    elif to_remove == 0:
        solutions.append(reference)
        return
    while(i<lenght):
        for each in remove_options:
            copy = reference[:]
            copy[i] = copy[i] - each
            if to_remove - each != 0:
                findSubsets(solutions, copy[:], (to_remove - each), i+1)
            else:
                solutions.append(copy)
        i += 1

def removeDups(solutions):
    def twoDimensionize(table):
        chunk = 0
        stones = int(len(table)/colors)
        table_2D = []
        for c in range(colors):
            table_2D.append(table[chunk:(chunk+stones)])
            chunk += stones
        return table_2D
    
    def flipOverY(table):
        newtable_2D = []
        for each in twoDimensionize(table):
            each.reverse()
            newtable_2D.append(each)
        return list(chain(*newtable_2D))

    def flipOverX(table):
        newtable_2D = twoDimensionize(table)
        newtable_2D.reverse()
        return list(chain(*newtable_2D))

    def flipOverXY(table):
        newtable = table[:]
        newtable.reverse()
        return newtable

    def findAndDel(it, count):
        try:
            id = solutions.index(it)
            del solutions[id]
            return 1
        except ValueError:
            return 0
    
    count = 0
    multisol = []
    while(solutions):
        sol = solutions.pop(0)
        multiplier = 1
        multiplier += findAndDel(flipOverX(sol), count)
        multiplier += findAndDel(flipOverXY(sol), count)
        multiplier += findAndDel(flipOverY(sol), count)
        multisol.append((sol, multiplier))
        count += 1
    return multisol

def reverseCount(hand, stones, colors, copies, cores):
    # Initialize variables
    maxhand = stones * copies * colors
    to_remove = maxhand - hand
    start = default_timer()
    solutions = list()
    cR = c_rummikub.cRummikub(cores, stones, colors, copies)
    print("Initializing. n", stones, "k", colors, "m", copies, "c", cores, "h", hand)
    # Generating a starting table
    table = initTable(colors, stones, copies)
    table = list(chain(*table))
    init = default_timer()
    print("Initialized. Time taken:", round(init - start,2), "\nFinding subsets...")

    # Find unique subsets
    findSubsets(solutions, table, to_remove)
    subset = default_timer()
    print("Found", len(solutions), "possible subsets. Time taken:", round(subset - init,2), "\nRemoving duplicates...")

    # Removing duplicates
    solutions = removeDups(solutions)
    dups = default_timer()
    print(len(solutions), "possible subsets left. Time taken:", round(dups - subset,2), "\nExecuting...")

    # Execute the determined situations
    result = cR.delegate(solutions)
    execution = default_timer()
    print("Execution done. Time taken:", round(execution - dups,2))

    # Finalizing
    stop = default_timer()
    memory = memoryUsage()
    print(writeResult(hand, stones, colors, copies, cores, [result, round(stop - start,2), memory, "botup"]))
    print("Winning hands:", result)

if __name__ == '__main__':
    stones = 6
    maxhand = 48
    minhand = 46#maxhand - 1
    cores = 7
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