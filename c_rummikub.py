class cRummikub:
    import subprocess
    def __init__(self):
        self.inlist = []
        self.outlist = []
        self.matchlist = []
        # TODO build frank.cc
    
    def __del__(self):
        self.subprocess.call(["rm", "in/*.in"])

    def appendGame(self, summed, l):
        self.inlist.append(l)
        self.matchlist.append(summed)

    def build(self, ifile, l):
        f = open(ifile, 'w')
        f.write(str(len(l)) + '\n')
        for each in l:
            f.write(str(each[0]) + '\n')
            f.write(str(each[1]) + '\n')
        f.close
    
    def buildMP(self):
        import multiprocessing as mp
        from itertools import chain
        from math import ceil
        length = len(self.inlist)
        chunk = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
        cores = mp.cpu_count()-1
        pool = mp.Pool(cores)
        print(cores)
        parts = chunk(self.inlist, ceil(length / cores))
        result = pool.map(self.buildAndRunMP, parts)
        b= list(chain(*result))
        print(result)

    # TODO seperate buildMP into buildandrun etc

    def buildAndRunMP(self, l):
        import os
        print(os.getpid())
        ifile = "in/" + str(os.getpid()) + ".in"
        self.build(ifile, l)
        return self.run(ifile)

    def buildAndRun(self, option):
        ifile = "in/1.in"
        self.build(ifile, self.inlist)
        return self.run(ifile)

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