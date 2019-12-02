import rummi4
hash = 105

def printTafel(tafel):
    if tafel == False:
        print("false")
        return
    for j in tafel:
        print(j)
    print('\n')

l = []
j = 0
for c in range(colors):
    t = []
    for i in range(n):
        value = ((cijfer & (3 << j))>>j) #3 = 0b11 oftewel het masker
        t.append(value)
        j += 2
    l.append(t)
printTafel(l)
