import rummi
import multiprocessing as mp
from functools import partial
from timeit import default_timer

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

# Multicoreprocessing per hand
def paralellBigHands(minhand, maxhand, stones ,colors ,copies):
    r= []
    start = default_timer()
    for i in range(minhand, maxhand+1):
        r.append(rummi.perfCallRecCount(i, stones, colors, copies))
        print(r[-1])
    stop = default_timer()
    printListWinningHands(r, round(stop - start, 2), minhand, stones, colors, copies)


if __name__ == '__main__':
    #arg: minhand, maxhand, stones, colors, copies
    #perfListWinningHands(3, 14, 13, 4, 2)
    #listWinningHands(3, 16, 6, 4, 2)
    #print(rummi.callRecCount(6, 13, 4, 2))
    paralellBigHands(3, 14, 13, 4, 2)