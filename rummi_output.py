from rummi_util import placeValue
from time import time, localtime, strftime
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

def printTableToFile(table, filename):
    file = open(filename, 'a')
    if table == False:
        print("false")
        return
    for j in table:
        for i in j:
            file.write(str(i))
            file.write(' ')
        file.write('\n')
    file.write('\n')
    file.close()

def printListToFile(list, filename):
    file = open(filename, 'a')
    file.writelines(list)
    file.close()

def printTaskList(hand_size, task_len, cores):
    mod = task_len % cores
    print (task_len, "tasks will be mapped to", cores, "cores, for a hand size of", hand_size)
    if mod < (cores/2) and mod != 0:
        if mod == 1:
            end = "core."
        else:
            end = "cores."
        print("Core mapping not optimal, last run wil only use", mod, end)

def printCurrentTask(memory, peak, task_len, task_count):
    t = time()
    curr_time = strftime('%H:%M', localtime(t))
    task = "[" + str(task_count) + "/" + str(task_len) + "]"
    print(task, curr_time, "- Memory usage:", placeValue(memory), "- Peak memory usage:", placeValue(peak))

def writeSolutions(s):
    f = open("output_hashed.txt", "w")
    for l in list(s):
        f.writelines(str(l)+ "\n")
    f.close()

def writeResult(i, stones, colors, copies, cores, r):
    t = time()
    line = strftime('%Y-%m-%d %H:%M', localtime(t)) + " - "
    line += "n" + str(stones) + "k" + str(colors) + "m" + str(copies) + "c" + str(cores) + "h - " + str(i) + " - "
    line += str(r[0]) + " - " + str(r[1]) + " - " + placeValue(r[2]) + " - " + r[3]
    out = open('results.txt', 'a')
    out.write(line + '\n')
    out.close()
    return line