#import rummi_winning
from rummi_util import initTable, copyTable
from rummi_output import printTableToConsole
import c_rummikub

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
# def deLoop(table, remaining=1, cR=c_rummikub.cRummikub(), outlist=[], max_row=13, max_col=4):
#     j, i = 0, 0
#     while j < max_col:
#         while i < max_row:
#             if table[j][i] != 0:
#                 newtable = copyTable(table)
#                 newtable[j][i] -= 1
#                 if remaining-1 == 0:
#                     summed, parsed = parseWithFrank(newtable)
#                     cR.appendGame(parsed)
#                     outlist.append(summed)
#                 else:
#                     deLoop(newtable, remaining - 1, cR, outlist)
#             i += 1
#         j += 1
#         i = 0
#     printTableToConsole(table)
#     return cR, outlist

import itertools
def findSubsets(inlist, size): 
    return list(map(list, itertools.combinations(inlist, size)))

def deCall():
    #Generating and sorting situations
    table = initTable(4, 6, 2)
    tablefrank = formatForFrank(table)
    subsets_raw = findSubsets(tablefrank, len(tablefrank)-1)
    subsets_unique = list(subsets_raw for subsets_raw,_ in itertools.groupby(subsets_raw))

    #Parsing situations
    cR = c_rummikub.cRummikub()
    tempcount = 0
    for each in subsets_unique:
        summed, parsed = parseForFrank(each)
        cR.appendGame(summed, parsed)
        if(tempcount == 50):
            break
        else:
            tempcount += 1
    #Running situations
    cR.build("in/2.in", cR.inlist)
    #cR.run("in/1.in")
    print("Matchlist", cR.matchlist)
    print("Output", cR.outlist)
    #print(cR.isWinning())
    # f = open("temp.txt", 'w')
    # for each in subsets_unique:
    #     f.write(str(each) + '\n')
    # f.close()

deCall()
