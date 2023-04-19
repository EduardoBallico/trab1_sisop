class Process():
    def __init__(self, processName):
        self.code = []
        self.data = {}
        self.labels = {}

        self.pc: int = 0
        self.acc: int = 0

        self.processName = processName
        self.read_process()

        self.terminate = False
        self.priority = 2

        self.quantum = 4

        self.waitingTime = 0
        self.runningTime = 0
        self.startTime = 0
        self.turnaroundTime = 0

        self.arrivalTime = 0

# ------ Round Robin ------
        self.shouldBeBlocked = False
        self.blockedUntil = 0

# ------ SJF ------
        self.execTime = 0

    def read_process(self):
        isCode = False
        isData = False
        codeLine = 0
        with open(self.processName, 'r') as file:
            for l in file:
                if l[0:8] == '.enddata':
                    isData = False
                if l[0:8] == '.endcode':
                    isCode = False

                if isData:
                    l_split = l.strip().split()
                    #self.data[l_split[0]] = int(l_split[1])
                    self.data[l_split[0]] = l_split[1]
                if isCode:
                    l_split = l.strip().split()
                    if l_split[0][len(l_split[0]) - 1] == ':':
                        self.code.append(("label", l_split[0][0:-1]))
                        self.labels[l_split[0][0:-1]] = codeLine
                    else:
                        self.code.append((l_split[0], l_split[1]))
                    codeLine += 1

                if l[0:5] == '.code':
                    isCode = True
                if l[0:5] == '.data':
                    isData = True


process = Process("ex_pgms_tp1/prog2.txt")

# process.read_process('ex_pgms_tp1/prog2.txt')

# print(process.data)
print(process.code)
print("\n")
print(process.labels)
