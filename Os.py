from Process import Process
import random

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
            self.activeProcess.terminate = True
        elif index == 1:
            self.activeProcess.shouldBeBlocked = True
            print(process.acc)
        elif index == 2:
            self.activeProcess.shouldBeBlocked = True
            self.activeProcess.acc = input("Digite um valor: ")
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

        if process.pc == len(process.code):
            self.activeProcess.terminate = True

    def roundRobin(self):
        self.readyList = self.processList
        self.readyList = sorted(self.readyList, key = lambda p : p.priority)
        # print(self.readyList[0].priority)
        # print(self.readyList[1].priority)
        # print(self.readyList[2].priority)

        while len(self.readyList) != 0:
            if len(self.readyList) != 0:
                self.activeProcess = self.readyList.pop(0)
                print("processo ", self.activeProcess.processName, " entrou")
                for i in range(self.activeProcess.quantum):
                    self.time += 1
                    print("Os time ", str(self.time))
                    #print("executou", str(i))
                    self.executeProcess(self.activeProcess)
                    if self.activeProcess.shouldBeBlocked:
                        break
                    if self.activeProcess.terminate:
                        break

                    if len(self.blockedList) != 0:
                        for process in self.blockedList:
                            if process.blockedUntil == self.time:
                                index = self.blockedList.index(process)
                                self.readyList.append(self.blockedList.pop(index))
                                self.readyList = sorted(self.readyList, key = lambda p : p.priority)

                    if len(self.readyList) != 0:
                        if self.readyList[0].priority < self.activeProcess.priority:
                            print("-----------------trocou----------------------")
                            break


                if self.activeProcess.terminate:
                    self.finishedList.append(self.activeProcess)
                    self.activeProcess.turnaroundTime = self.time - self.activeProcess.startTime 
                elif self.activeProcess.shouldBeBlocked:
                    self.blockedList.append(self.activeProcess)
                    self.activeProcess.blockedUntil = self.time + random.randint(8, 10)
                    print("processo", self.activeProcess.processName, "bloqueado por ", str(self.activeProcess.blockedUntil - self.time))
                    self.activeProcess.shouldBeBlocked = False
                else:
                    self.readyList.append(self.activeProcess)
                    self.readyList = sorted(self.readyList, key = lambda p : p.priority)

            if len(self.readyList) == 0 and len(self.blockedList) > 0:
                while len(self.readyList) == 0:
                    self.time += 1
                    print("tempo acrescentado em bloqueados", str(self.time))
                    for process in self.blockedList:
                            if process.blockedUntil <= self.time:
                                index = self.blockedList.index(process)
                                self.readyList.append(self.blockedList.pop(index))
                                self.readyList = sorted(self.readyList, key = lambda p : p.priority)

                print("processo saiu da lista de bloqueados")



os = Os()
os.loadProcess("ex_pgms_tp1/prog1.txt")
os.processList[0].priority = 1

os.loadProcess("ex_pgms_tp1/prog2.txt")
os.processList[1].priority = 0
os.processList[1].quantum = 7

os.loadProcess("ex_pgms_tp1/prog3.txt")
os.processList[2].priority = 2

os.roundRobin()

# while os.process.terminate == False:
#     os.executeProcess(os.process)

# print(os.process.labels[], '-------------------------------------')

# print(os.process.acc)
