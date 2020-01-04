class cRummikub:
    import subprocess
    import multiprocessing as mp
    def __init__(self):
        self.inlist = []
        self.outlist = []
        self.matchlist = []
        # TODO build frank.cc
    
    def __del__(self):
        #elf.subprocess.call(["ls", "in"])
        #self.subprocess.call(["rm", "in/*.in"])
        pass

    def appendGame(self, summed, l):
        self.inlist.append(l)
        self.matchlist.append(summed)

    def buildAndRunMP(self):
        self.buildMP()
        self.runMP()
        return self.isWinning()

    def buildMP(self):
        from math import ceil
        self.cores = self.mp.cpu_count()-1
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
        import os
        print(os.getpid())
        ifile = "in/" + str(os.getpid()) + ".in"
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
        self.outlist = list(map(int, result.split()))
        return self.outlist

    def isWinning(self):
        i = 0
        resultlist = []
        while i != len(self.matchlist):
            if self.matchlist[i] == self.outlist[i]:
                resultlist.append(True)
            else:
                resultlist.append(False)
                print(i, "Match", self.matchlist[i], "Result", self.outlist[i])
            i += 1
        return resultlist