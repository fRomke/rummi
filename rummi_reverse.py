from rummi_util import initTable, copyTable
from rummi_output import printTableToConsole
from itertools import groupby, combinations
import c_rummikub

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

def deCall():
    #Generating and sorting situations
    table = initTable(4, 6, 2)
    tablefrank = formatForFrank(table)
    subsets_raw = findSubsets(tablefrank, len(tablefrank)-1)
    subsets_unique = list(subsets_raw for subsets_raw,_ in groupby(subsets_raw))

    #Parsing situations
    cR = c_rummikub.cRummikub()
    tempcount = 0
    for each in subsets_unique:
        summed, parsed = parseForFrank(each)
        cR.appendGame(summed, parsed)
        # if(tempcount == 50):
        #     break
        # else:
        #     tempcount += 1
    #Running situations
    #cR.build("in/1.in", cR.inlist)
    cR.buildMP()
    #cR.run("in/1.in")
    print("Matchlist", cR.matchlist)
    print("Output", cR.outlist)
    #print(cR.isWinning())
    # f = open("temp.txt", 'w')
    # for each in subsets_unique:
    #     f.write(str(each) + '\n')
    # f.close()

deCall()
