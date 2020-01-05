class cRummikub:
    import subprocess
    import multiprocessing as mp
    import os
    def __init__(self, c):
        self.inlist = []
        self.outlist = []
        self.matchlist = []
        self.cores = c
        # TODO build frank.cc

    def compileFrank(self):
        MyOut = self.subprocess.Popen(["gcc", "-o", "frank", "frank.cc", "-lstdc++"], 
                    stdout=self.subprocess.PIPE, 
                    stderr=self.subprocess.STDOUT)
        stdout,stderr = MyOut.communicate()
        if stderr != None:
            print(stderr)
            print("Error compiling frank.cc please compile manually: gcc -o frank frank.cc -lstdc++")
            quit()
        else:
            print("frank.cc compiled succesfully!")

    def appendGame(self, summed, l):
        self.inlist.append(l)
        self.matchlist.append(summed)

    def buildAndRunMP(self):
        self.buildMP()
        self.runMP()
        return self.isWinning()

    def buildMP(self):
        from math import ceil
        length = len(self.inlist)
        chunk = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
        self.partsMP = chunk(self.inlist, ceil(length / self.cores))
        
    def runMP(self):
        from itertools import chain
        pool = self.mp.Pool(self.cores)
        result = pool.map(self.buildAndRun, self.partsMP)
        pool.close()
        pool.join()
        self.outlist = list(chain(*result))

    def buildAndRun(self, l):
        print(self.os.getpid())
        ifile = "in/" + str(self.os.getpid()) + ".in"
        self.build(ifile, l)
        return self.run(ifile)

    def build(self, ifile, l):
        f = open(ifile, 'w')
        f.write(str(len(l)) + '\n')
        for each in l:
            f.write(str(each[0]) + '\n')
            f.write(str(each[1]) + '\n')
        f.close

    def run(self, ifile):
        MyOut = self.subprocess.Popen(["./frank", ifile], 
                    stdout=self.subprocess.PIPE, 
                    stderr=self.subprocess.STDOUT)
        stdout,stderr = MyOut.communicate()
        result = stdout.decode("utf-8")
        out = list(map(int, result.split()))
        self.subprocess.call(["rm", ifile])
        return out

    def isWinning(self):
        i = 0
        resultlist = []
        while i != len(self.matchlist):
            if self.matchlist[i] == self.outlist[i]:
                resultlist.append(True)
            else:
                resultlist.append(False)
            i += 1
        return resultlist