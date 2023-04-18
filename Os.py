from Process import Process


class Os():
    def __init__(self):
        self.instrucoes = {
            "aritmetic": ["add", "sub", "mult", "div"],
            "memory": ["load", "store"],
            "jump": ["BRANY", "BRPOS", "BRZERO", "BRNEG"],
            "system": ["syscall"]
        }

        self.readyList = []
        self.blockedList = []
        self.processList = []
        self.finishedList = []

        self.time = 0

        self.activeProcess: Process



    def loadProcess(self, processName: str):
        self.processList.append(Process(processName))

    def aritmeticInstructions(self, op1: int, instruction: str, process: Process):
        if instruction == "add":
            process.acc += op1
        elif instruction == "sub":
            process.acc -= op1
        elif instruction == "mult":
            process.acc *= op1
        elif instruction == "div":
            if op1 != 0:
                process.acc /= op1
            else:
                print("Processo ", str(process.processName), "foi terminado por tentar realizar divisao por 0")
                process.terminate = True
            # LIDAR COM DIV POR 0


    def memoryInstructions(self, op1: int or str, instruction: str, process: Process):
        if instruction == "load":
            process.acc = op1
        elif instruction == "store":
            process.data[op1] = process.acc
            process.acc = int(process.acc)


    def jumpInstructions(self, instruction: str, process: Process, posLabel: int):
        if instruction == "BRANY":
            process.pc = posLabel
        elif instruction == "BRPOS":
            if process.acc > 0:
                process.pc = posLabel
        elif instruction == "BRZERO":
            if process.acc == 0:
                process.pc = posLabel
        elif instruction == "BRNEG":
            if process.acc < 0:
                process.pc = posLabel


    def systemInstructions(self, process: Process, index: int):
        if index == 0:
            process.terminate = True
        elif index == 1:
            process.shouldBeBlocked = True
            print(process.acc)
        elif index == 2:
            process.shouldBeBlocked = True
            process.acc = input("Digite um valor")
            #precisa ser numero


    def executeProcess(self, process: Process):
        # print(process.pc)
        instruction = process.code[process.pc]
        print(instruction)
        process.pc += 1

        if instruction[0] in self.instrucoes["aritmetic"]:
            if instruction[1][0] == "#":
                aux = instruction[1].strip("#")
                op = int(aux)
                self.aritmeticInstructions(op, instruction[0], process)
            else:
                op = int(process.data[instruction[1]])
                self.aritmeticInstructions(op, instruction[0], process)

        elif instruction[0] in self.instrucoes["memory"]:
            if instruction[0] == "load":
                if instruction[1][0] == "#":
                    aux = instruction[1].strip("#")
                    op = int(aux)
                    self.memoryInstructions(op, instruction[0], process)
                else:
                    op = int(process.data[instruction[1]])
                    self.memoryInstructions(op, instruction[0], process)
            else:
                self.memoryInstructions(instruction[1], instruction[0], process)
        
        elif instruction[0] in self.instrucoes["jump"]:
            self.jumpInstructions(instruction[0], process, process.labels[instruction[1]])
            
        elif instruction[0] in self.instrucoes["system"]:
            self.systemInstructions(process, int(instruction[1]))

    def roundRobin(self):
        self.readyList = self.processList
        self.readyList = sorted(self.readyList, key = lambda p : p.priority)
        # print(self.readyList[0].priority)
        # print(self.readyList[1].priority)
        # print(self.readyList[2].priority)

        while len(self.readyList) != 0:
            if len(self.readyList) != 0:
                self.activeProcess = self.readyList.pop[0]
                for i in self.activeProcess.quantum:
                    self.executeProcess(self.activeProcess)
                    if self.activeProcess.shouldBeBlocked:
                        break
                    if self.activeProcess.terminate:
                        break
                    self.time += 1

                if self.activeProcess.terminate:
                    self.finishedList.append(self.activeProcess)
                    self.activeProcess.turnaroundTime = self.time - self.activeProcess.startTime 
                elif self.activeProcess.shouldBeBlocked:
                    self.blockedList.append(self.activeProcess)
                else:
                    self.readyList.append(self.activeProcess)
                    self.readyList = sorted(self.readyList, key = lambda p : p.priority)



os = Os()
os.loadProcess("ex_pgms_tp1/prog1.txt")

os.loadProcess("ex_pgms_tp1/prog2.txt")
os.processList[1].priority = 1
os.processList[1].quantum = 7

os.loadProcess("ex_pgms_tp1/prog3.txt")
os.processList[2].priority = 0

os.roundRobin()

# while os.process.terminate == False:
#     os.executeProcess(os.process)

# print(os.process.labels[], '-------------------------------------')

# print(os.process.acc)