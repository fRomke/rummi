from rummi_settings import print_to_console, print_to_file

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