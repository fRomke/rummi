class cRummikub:
    import subprocess
    import rummi_reverse
    import os
    def __init__(self, c, n, k, m):
        self.cores = c
        self.stones = n
        self.colors = k 
        self.copies = m
        self.checkStructure()

    def checkStructure(self):
        import os.path
        if not os.path.isdir("in"):
            self.subprocess.call(["mkdir", "in"])
        if not os.path.isfile("frank"):
            self.compileFrank()

    def compileFrank(self):
        # TODO Use subprocess.call() maybe?
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

    def delegate(self, input):
        from math import ceil
        print("Total length", len(input))
        chunk = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
        input = chunk(input, ceil(len(input) / self.cores))
        print("Parts", len(input[0]), len(input[-1]))

        import multiprocessing as mp
        pool = mp.Pool(self.cores)
        result = pool.map(self.worker, input)
        pool.close()
        pool.join()
        sum_results = 0
        for a in result:
            sum_results += a
        return sum_results

    def worker(self, input):
        ifile = "in/" + str(self.os.getpid()) + ".in"
        sumlist = []
        # Create input list for own process
        f = open(ifile, 'a')
        f.write(str(len(input)) + '\n')
        for table in input:
            summed, assignment = self.parseForFrank(table)
            sumlist.append(summed)
            f.write(str(assignment[0]) + '\n')
            f.write(str(assignment[1]) + '\n')
        f.close()

        output = self.run(ifile)
        winning = self.isWinning(output, sumlist)
        print(ifile, winning, "/", len(sumlist))
        return winning

    def run(self, ifile):
        # TODO Process results live.
        stdout = self.subprocess.check_output(["./frank", ifile])
        result = stdout.decode("utf-8")
        out = list(map(int, result.split()))
        self.subprocess.call(["rm", ifile])
        return out

    def isWinning(self, output, sumlist):
        # Returns number of results that match the maximum value
        i = 0
        true = 0
        while i != len(sumlist):
            if sumlist[i] == output[i]:
                true += 1
            i += 1
        return true

    def parseForFrank(self, table):
        # Writes table in format that is readable for frank.cc
        # and returns the potential maximum value
        s = ""
        summed = 0
        count = 0
        colors = ['b', 'g', 'r', 'y']
        i_color = 0
        stone = 1
        for tile in table:
            for j in range(tile):
                summed += int(stone)
                s += str(stone) + colors[i_color] + ' '
                count += 1
            if stone == self.stones:
                stone = 1
                i_color += 1
            else:
                stone += 1
        return (summed, [count, s])