from rummi_settings import print_to_console, print_to_file

def outputTable(table,output):
    if print_to_console or print_to_file:
        printTable(table, output)

def printTable(table, output):
    if table == False:
        print("false")
        return
    for j in table:
        if print_to_console: print(j)
        if print_to_file:
            for i in j:
                output.write(str(i))
                output.write(' ')
            output.write('\n')
    if print_to_console: print('\n')
    if print_to_file: output.write('\n')

def writeSolutions(s):
    f = open("output_hashed.txt", "w")
    for l in list(s):
        f.writelines(str(l)+ "\n")
    f.close()