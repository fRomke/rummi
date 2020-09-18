stones = "stones"
colors = "colors"
copies = "copies"
minimal_size = "minimal_size"
config = {stones:6, colors:4, copies:2, minimal_size:3}
hash = 680

def printTafel(tafel):
    if tafel == False:
        print("false")
        return
    for j in tafel:
        print(j)
    print('\n')

l = []
j = 0
for c in range(config[colors]):
    t = []
    for i in range(config[stones]):
        value = ((hash & (3 << j))>>j) #3 = 0b11 oftewel het masker
        t.append(value)
        j += 2
    l.append(t)
printTafel(l)
