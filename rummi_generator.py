import rummi
import multiprocessing as mp
from functools import partial
from timeit import default_timer

def printListWinningHands(result, t, minhand, stones ,colors ,copies):
    print("For " + str(colors) + " colors with " + str(stones) + " stones and " + str(copies) + " copies of each:")
    for r in result:
        print(str(minhand) + " - " + str(r[0]) + " - " + str(r[1]) + "s")
        minhand += 1
    print("Total time taken: " + str(t)+ "s")

def listWinningHands(minhand, maxhand, stones, colors, copies):
    result = []
    start = default_timer()
    for i in range(minhand,maxhand+1):
        winning = rummi.callRecCount(i, stones, colors, copies)
        result.append(winning)
    stop = default_timer()
    printListWinningHands(result, round(stop - start, 2), minhand, stones, colors, copies)

def perfListWinningHands(minhand, maxhand, stones ,colors ,copies):
    pool  = mp.Pool(mp.cpu_count()-1)
    start = default_timer()
    constargs = partial(rummi.callRecCount, nmax=stones, k=colors, m=copies)
    result = pool.map(constargs, range(minhand,maxhand+1))
    stop = default_timer()
    printListWinningHands(result, round(stop - start, 2), minhand, stones, colors, copies)

if __name__ == '__main__':
    #arg: minhand, maxhand, stones, colors, copies
    perfListWinningHands(3, 26, 6, 4, 2)
    #listWinningHands(3, 16, 6, 4, 2)
    #print(rummi.callRecCount(14, 13, 4, 2))

# Jan
# 7, - 696
# 8, - 467
# 9, - 10872
# 10, - 12816
# 11,10896
# 12,103340
# 13,146760
# 14,144856
# 15,738648
# 16,1150642
# 17,1240616
# 18,4042944
# 19,6433240
# 20,7220872
# 21,16853400

# ListWinningHands()
# For 4 colors with 6 stones and 2 copies of each:
# 3 - 0.0s - 40
# 4 - 0.0s - 18
# 5 - 0.0s - 8
# 6 - 0.0s - 820
# 7 - 0.0s - 696
# 8 - 0.0s - 467
# 9 - 0.05s - 10872
# 10 - 0.07s - 12816
# 11 - 0.06s - 10896
# 12 - 0.57s - 103340
# 13 - 0.96s - 146760
# 14 - 0.98s - 144856
# 15 - 4.87s - 738648
# 16 - 8.88s - 1150642
# 17 - 10.42s - 1240616
# 18 - 33.38s - 4042944
# 19 - 63.37s - 6433240
# 20 - 80.35s - 7220872
# 21 - 186.61s - 16853400
# [Done] exited with code=0 in 390.636 seconds

# perfListWinningHands()
# For 4 colors with 6 stones and 2 copies of each:
# 3 - 40 - 0.0s
# 4 - 18 - 0.0s
# 5 - 8 - 0.0s
# 6 - 820 - 0.0s
# 7 - 696 - 0.0s
# 8 - 467 - 0.0s
# 9 - 10872 - 0.05s
# 10 - 12816 - 0.07s
# 11 - 10896 - 0.06s
# 12 - 103340 - 0.62s
# 13 - 146760 - 1.02s
# 14 - 144856 - 1.08s
# 15 - 738648 - 5.23s
# 16 - 1150642 - 9.51s
# 17 - 1240616 - 11.33s
# 18 - 4042944 - 36.29s
# 19 - 6433240 - 68.16s
# 20 - 7220872 - 88.11s
# 21 - 16853400 - 199.74s
# 22 - 25910748 - 371.19s
# 23 - 29036248 - 486.24s
# 24 - 52234799 - 877.57s
# 25 - 74258224 - 1510.93s
# 26 - 79916256 - 2002.55s
# Total time taken: 2076.47s

# For 4 colors with 13 stones and 2 copies of each:
# 3 - 0.0s - 96
# 4 - 0.0s - 53
# 5 - 0.0s - 36
# 6 - 0.03s - 4656
# 7 - 0.04s - 4980
# 8 - 0.03s - 4731
# 9 - 1.06s - 151728
# 10 - 1.74s - 233412
# 11 - 2.11s - 279108
# 12 - 28.12s - 3753318
# 13 - 58.82s - 7244080

# [Done] exited with code=1 in 149.272 seconds