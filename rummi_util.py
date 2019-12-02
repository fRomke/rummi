from itertools import combinations, chain

def initTafel(colors, n):
    col = []
    row = []
    for j in range(colors):
        for i in range(1, n+1):
            row.append(0)
        col.append(row)
        row = []
    return col

def hashTafel(table):
    sum = 0
    for i, c in enumerate(list(chain(*table))):
        sum = sum | (c << (i*2))
    return sum

def copyTable(table):
    newtable = []
    for row in table:
        newtable.append(row.copy())
    return newtable

def findsubsets(s, leg): 
    return list(map(set, combinations(s, leg))) 