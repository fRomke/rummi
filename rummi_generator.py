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
    perfListWinningHands(3, 14, 13, 4, 2)
    #listWinningHands(3, 16, 6, 4, 2)
    #print(rummi.callRecCount(14, 13, 2, 2))

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

# For 4 colors with 7 stones and 2 copies of each:
# 3 - 48 - 0.0s
# 4 - 23 - 0.0s
# 5 - 12 - 0.0s
# 6 - 1176 - 0.01s
# 7 - 1068 - 0.01s
# 8 - 816 - 0.0s
# 9 - 18912 - 0.1s
# 10 - 24004 - 0.15s
# 11 - 23088 - 0.15s
# 12 - 222549 - 1.48s
# 13 - 342624 - 2.64s
# 14 - 382880 - 3.0s
# 15 - 2023488 - 15.19s
# 16 - 3441477 - 29.46s
# 17 - 4225324 - 38.22s
# 18 - 14567450 - 126.35s
# 19 - 25528004 - 257.2s
# 20 - 32957292 - 357.87s
# 21 - 83299676 - 895.29s
# Total time taken: 903.53s

# For 4 colors with 13 stones and 1 copies of each:
# 3 - 96 - 0.0s
# 4 - 53 - 0.0s
# 5 - 36 - 0.0s
# 6 - 4010 - 0.03s
# 7 - 4100 - 0.03s
# 8 - 3690 - 0.03s
# 9 - 97624 - 0.71s
# 10 - 136694 - 1.1s
# 11 - 147204 - 1.26s
# 12 - 1567624 - 12.14s
# 13 - 2610728 - 22.5s
# 14 - 3152280 - 28.79s
# 15 - 17734816 - 145.86s
# 16 - 31972283 - 294.53s
# 17 - 41233308 - 422.33s
# Total time taken: 425.67s

# For 2 colors with 13 stones and 2 copies of each:
# 3 - 22 - 0.0s
# 4 - 20 - 0.0s
# 5 - 18 - 0.0s
# 6 - 253 - 0.0s
# 7 - 426 - 0.0s
# 8 - 564 - 0.0s
# 9 - 2216 - 0.01s
# 10 - 4621 - 0.03s
# 11 - 7498 - 0.05s
# 12 - 17280 - 0.12s
# 13 - 35082 - 0.29s
# 14 - 61067 - 0.56s
# 15 - 113868 - 1.12s
# 16 - 207577 - 2.26s
# 17 - 352328 - 4.17s
# 18 - 590790 - 7.85s
# 19 - 970294 - 14.59s
# 20 - 1533963 - 26.81s
# 21 - 2358978 - 47.62s
# 22 - 3528600 - 82.76s
# 23 - 5111852 - 141.17s
# 24 - 7182257 - 232.97s
# 25 - 9781466 - 382.83s
# 26 - 12886595 - 611.83s
# Total time taken: 627.03s

# For 4 colors with 13 stones and 2 copies of each:
# 3 - 96 - 0.0s
# 4 - 53 - 0.0s
# 5 - 36 - 0.0s
# 6 - 4656 - 0.03s
# 7 - 4980 - 0.04s
# 8 - 4731 - 0.03s
# 9 - 151728 - 1.1s
# 10 - 233412 - 1.79s
# 11 - 279108 - 2.18s
# 12 - 3753318 - 28.43s
# 13 - 7244080 - 59.58s
# 14 - 10232524 - 87.3s
# Total time taken: 87.78s