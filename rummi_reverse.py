from rummi_util import initTable, copyTable, memoryUsage
from rummi_output import printTableToConsole, writeResult
from itertools import groupby, combinations
import c_rummikub
from sys import argv
from timeit import default_timer

colors = 4
copies = 2

def findSubsets(inlist, size): 
    return list(map(list, combinations(inlist, size)))

def parseForFrank(l):
    s = ""
    summed = 0
    for each in l:
        summed += int(each[:-1])
        s += each + ' '
    return (summed, [len(l), s])

def formatForFrank(tafel):
    l = []
    colors = ['b', 'g', 'r', 'y']
    i_color = 0
    stone = 1
    for each in tafel:
        for i in each:
            for j in range(i):
                l.append(str(stone) + colors[i_color])
            stone += 1
        i_color += 1
        stone = 1
    return l

def reverseCount(hand, stones, cores):
    start = default_timer()
    # Generating a starting table
    table = initTable(colors, stones, copies)
    # Format the table to be readable by frank.cc
    tablefrank = formatForFrank(table)
    # Generating all subset of the table for a given hand
    subsets_raw = findSubsets(tablefrank, hand)
    # Removing all duplicate situations
    import pandas as pd
    df = pd.DataFrame(subsets_raw)
    df = df.drop_duplicates()
    subsets_unique = df.values.tolist()
    print("Unique situations:", len(subsets_unique))
    #Parsing situations into the cR object
    cR = c_rummikub.cRummikub(cores)
    for each in subsets_unique:
        summed, parsed = parseForFrank(each)
        cR.appendGame(summed, parsed)
    #Running situations
    #cR.build("in/1.in", cR.inlist)
    r = cR.buildAndRunMP()
    stop = default_timer()
    memory = memoryUsage()
    print(writeResult(hand, stones, colors, copies, cores, [r.count(True), round(stop - start,2), memory, "botup"]))
    print("Winning hands:", r.count(True))

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