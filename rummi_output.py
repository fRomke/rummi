print_to_console = False
print_to_file = False
def outputTable(table,output):
    if print_to_console: 
        printTableToConsole(table)
    if print_to_file:
        printTableToFile(table, output)

def printTableToConsole(table):
    if table == False:
        print("false")
        return
    for j in table:
        print(j)
    print('\n')

def printTableToFile(table, file):
    if table == False:
        print("false")
        return
    for j in table:
        for i in j:
            file.write(str(i))
            file.write(' ')
        file.write('\n')
    file.write('\n')

def writeSolutions(s):
    f = open("output_hashed.txt", "w")
    for l in list(s):
        f.writelines(str(l)+ "\n")
    f.close()

def writeResult(i, stones, colors, copies, cores, r):
    from time import time, localtime, strftime
    from rummi_util import placeValue
    t = time()
    line = strftime('%Y-%m-%d %H:%M', localtime(t)) + " - "
    line += "n" + str(stones) + "k" + str(colors) + "m" + str(copies) + "c" + str(cores) + "h - " + str(i) + " - "
    line += str(r[0]) + " - " + str(r[1]) + " - " + placeValue(r[2]) + " - " + placeValue(r[3])
    out = open('results.txt', 'a')
    out.write(line + '\n')
    out.close()
    return line