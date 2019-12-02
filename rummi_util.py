from itertools import combinations, chain

def initTable(colors, stones):
    col = []
    row = []
    for j in range(colors):
        for i in range(1, stones+1):
            row.append(0)
        col.append(row)
        row = []
    return col

def hashTable(table):
    sum = 0
    for i, c in enumerate(list(chain(*table))):
        sum = sum | (c << (i*2))
    return sum

def copyTable(table):
    new_table = []
    for row in table:
        new_table.append(row.copy())
    return new_table

def findSubsets(s, leg): 
    return list(map(set, combinations(s, leg))) 