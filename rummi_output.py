from rummi_settings import printtoconsole, printtofile

def writeOffTafel(tafel,output):
    if printtoconsole or printtofile:
        printTafel(tafel, output)

def printTafel(tafel, output):
    if tafel == False:
        print("false")
        return
    for j in tafel:
        if printtoconsole: print(j)
        if printtofile:
            for i in j:
                output.write(str(i))
                output.write(' ')
            output.write('\n')
    if printtoconsole: print('\n')
    if printtofile: output.write('\n')

def writeSolutions(s):
    f = open("output_hashed.txt", "w")
    for l in list(s):
        f.writelines(str(l)+ "\n")
    f.close()