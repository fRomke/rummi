class cRummikub:
    def __init__(self):
        self.inlist = []
        # TODO build frank.cc
    
    def appendGame(self, l):
        self.inlist.append(l)
    
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
        return result.split()

    def buildAndRun(self, option):
        ifile = "in/1.in"
        self.build(ifile, self.inlist)
        print(self.run(ifile))