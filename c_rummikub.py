class cRummikub:
    def __init__(self):
        self.inlist = []
        self.outlist = []
        self.matchlist = []
        # TODO build frank.cc
    
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

    def run(self, ifile):
        import subprocess
        MyOut = subprocess.Popen(["./frank", ifile], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT)
        stdout,stderr = MyOut.communicate()
        result = stdout.decode("utf-8")
        self.outlist = list(map(int, result.split()))
        return self.outlist

    def buildAndRun(self, option):
        ifile = "in/1.in"
        self.build(ifile, self.inlist)
        return self.run(ifile)

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