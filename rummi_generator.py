import rummi
import multiprocessing as mp
from functools import partial
from timeit import default_timer
from sys import argv

def printListWinningHands(result, t, minhand, stones ,colors ,copies):
    print("For " + str(colors) + " colors with " + str(stones) + " stones and " + str(copies) + " copies of each:")
    for r in result:
        print(str(minhand) + " - " + str(r[0]) + " - " + str(r[1]) + "s - " + str(r[2]) + " bytes")
        minhand += 1
    print("Total time taken: " + str(t)+ "s")

# No multicoreprocessing
def listWinningHands(minhand, maxhand, stones, colors, copies):
    result = []
    start = default_timer()
    for i in range(minhand,maxhand+1):
        winning = rummi.callRecCount(i, stones, colors, copies)
        result.append(winning)
    stop = default_timer()
    printListWinningHands(result, round(stop - start, 2), minhand, stones, colors, copies)

# Calculates multiple hands at the same time.
def paralellListWinningHands(minhand, maxhand, stones ,colors ,copies):
    pool  = mp.Pool(mp.cpu_count()-1)
    start = default_timer()
    constargs = partial(rummi.callRecCount, nmax=stones, k=colors, m=copies)
    result = pool.map(constargs, range(minhand,maxhand+1))
    stop = default_timer()
    printListWinningHands(result, round(stop - start, 2), minhand, stones, colors, copies)

def writeResult(i, stones, colors, copies, r):
    line = "n" + str(stones) + "k" + str(colors) + "m" + str(copies) + "h - " + str(i) + " - "
    line += str(r[0]) + " - " + str(r[1]) + " - " + str(r[2])
    out = open('results.txt', 'a')
    out.write(line + '\n')
    out.close()
    return line

# Multicoreprocessing per hand
def paralellBigHands(minhand, maxhand, stones ,colors ,copies, cores):
    r= []
    start = default_timer()
    for i in range(minhand, maxhand+1):
        r.append(rummi.perfCallRecCount(i, stones, colors, copies, cores))
        print(writeResult(i, stones, colors, copies, r[-1]))
    stop = default_timer()
    printListWinningHands(r, round(stop - start, 2), minhand, stones, colors, copies)

if __name__ == '__main__':
    minhand = 3
    maxhand = 10
    stones = 13
    colors = 4
    copies = 2
    cores = 4
    if len(argv) == 7:
        minhand = int(argv[1])
        maxhand = int(argv[2])
        stones = int(argv[3])
        colors = int(argv[4])
        copies = int(argv[5])
        cores = int(argv[6])
    elif len(argv)>1 and len(argv) != 7:
        print("Invalid amount of arguments. Must be either none or six.")
        quit()
    paralellBigHands(minhand, maxhand, stones, colors, copies, cores)