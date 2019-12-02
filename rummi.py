from rummi_output import *
from rummi_util import *
from rummi_settings import *

globalremaininghand = 0

def determinePossibleLegs(remaininghand, leg): #456
    mogelijkheden = []
    if (remaininghand-leg) >= minimaleleg:
        mogelijkheden.append(leg)
        mogelijkheden += determinePossibleLegs(remaininghand, leg+1)
    else:
        mogelijkheden.append(remaininghand)
    return mogelijkheden

def legZet(tafel, i, row, zet):
    for each in range(zet):
        if tafel[row][each + i] == copien:
            return False
        else:
            tafel[row][each + i] += 1
    return tafel

def determinePossibleGroups(tafel, col, leg): #444
    glist = [0,1,2,3]
    for i in range(colors):
        if tafel[i][col] == copien:
            glist.remove(i)
    if len(glist) < minimaleleg:
        return False
    else:
        glist = findsubsets(glist, leg)
        return glist

def legGroup(tafel, col, group):
    for i in group:
        tafel[i][col] += 1
    return tafel

def recursiveSlice(onrow, remaininghand, tafel, oplossingen, i):
    if remaininghand == 0:
        writeOffTafel(tafel, output)
        oplossingen.add(hashTafel(tafel))
        return oplossingen
    else:
        mogelijkheden = determinePossibleLegs(remaininghand, minimaleleg)
        if remaininghand == globalremaininghand:
            print(mogelijkheden)
        baki = i
        bakonrow = onrow
        for mogeleg in mogelijkheden: #n=7 [3,4,7]
            i = baki
            onrow = bakonrow
            while onrow > - 1: #rij
                while (n - i) >= mogeleg: #kolommen in de rij
                    newtafel = legZet(copyTable(tafel), i, onrow, mogeleg)
                    if newtafel != False:
                        oplossingen = recursiveSlice(onrow, remaininghand - mogeleg, newtafel, oplossingen, i)
                    i += 1
                if onrow < 3:
                    onrow += 1
                    i = 0
                else: 
                    onrow = -1
                    i = 0
            if (mogeleg == 3 or mogeleg == 4) and remaininghand != 5: #remaininghand != 5 wellicht onnodig
                j = i
                while j != n:#kolom
                    gmogelijkheden = determinePossibleGroups(tafel, j, mogeleg)
                    if gmogelijkheden != False:
                        for g in gmogelijkheden:
                            newtafel = legGroup(copyTable(tafel), j, g)
                            oplossingen = recursiveSlice(onrow, remaininghand - mogeleg, newtafel, oplossingen, j)
                    j += 1
        return oplossingen

def callRecSlice(h, nmax, k , m):
    global handsize
    global n
    global copien
    global colors
    global output
    global printtofile
    global globalremaininghand
    output = open('output.txt','w')
    globalremaininghand = h
    handsize = h
    n = nmax
    copien = m
    colors = k 

    tafel = initTafel(colors, n)
    oplossingen = set()
    oplossingen = recursiveSlice(0, handsize, tafel, oplossingen, 0)
    if savehash: writeSolutions(oplossingen)
    output.close()
    return (len(oplossingen))


#callRecSlice(8)




# 14 - 12569104 Unique: 10232524
# [Done] exited with code=0 in 517.619 seconds