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
        self.notStarted = []
        self.finishedList = []

        self.arrivalTimes = set()

        self.time = 0

        self.activeProcess = None



    def loadProcess(self, processName: str, arrivalTime): # inserir processos
        p = Process(processName, arrivalTime) 
        self.notStarted.append(p)
        self.arrivalTimes.add(p.arrivalTime)
        # print("arrival time = ", p.arrivalTime)


    def aritmeticInstructions(self, op1: int, instruction: str, process: Process): #instruções aritméticas
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
            


    def memoryInstructions(self, op1: int or str, instruction: str, process: Process): #insrtuções de memória
        if instruction == "load":
            process.acc = op1
        elif instruction == "store":
            process.data[op1] = process.acc
            process.acc = int(process.acc)


    def jumpInstructions(self, instruction: str, process: Process, posLabel: int): #insrtuções de jump
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


    def systemInstructions(self, process: Process, index: int): #insrtuções de sistema
        if index == 0:
            self.activeProcess.terminate = True
        elif index == 1:
            self.activeProcess.shouldBeBlocked = True
            print("Saida de dados no processo", str(self.activeProcess.processName), ": ", str(process.acc))
        elif index == 2:
            self.activeProcess.shouldBeBlocked = True
            print("Entrada de dados no processo", str(self.activeProcess.processName))
            self.activeProcess.acc = input("Digite um valor: ")
            #precisa ser numero


    def executeProcess(self, process: Process): #executa as instruções
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


    def testArrivalTimeRR(self): #testa se alguma instrução chegou no tempo atual e ordena a lista corretamente com a prioridade dos processos
        for p in self.notStarted:
                if p.arrivalTime == self.time:
                    index = self.notStarted.index(p)
                    self.readyList.append(self.notStarted.pop(index))
                    self.readyList = sorted(self.readyList, key = lambda p : p.priority)

    def testArrivalTimeSJF(self): #testa se alguma instrução chegou no tempo atual e ordena a lista corretamente com o tempo de execução dos processos
        for p in self.notStarted:
                if p.arrivalTime == self.time:
                    index = self.notStarted.index(p)
                    self.readyList.append(self.notStarted.pop(index))
                    self.readyList = sorted(self.readyList, key = lambda p : p.execTime)


    def addWaitingTime(self): #soma 1 no waiting time de cada processo na lista de prontos
        if len(self.readyList) != 0:
            for p in self.readyList:
                p.waitingTime += 1


    def showLists(self):
        print("Tempo = ", str(self.time))

        print("\n----------- Lista de prontos -----------")
        if len(self.readyList) != 0:
            for p in self.readyList:
                print(p.processName)
        else:
            print("Lista vazia")

        print("\n----------- Processo executando -----------")
        if self.activeProcess is not None:
            print(self.activeProcess.processName)
        else:
            print("Nenhum processo executando")

        print("\n----------- Lista de bloqueados -----------")
        if len(self.blockedList) != 0:
            for p in self.blockedList:
                print(p.processName)
        else:
            print("Lista vazia")

        print("\n----------- Lista de finalizados -----------")
        if len(self.finishedList) != 0:
            for p in self.finishedList:
                print(p.processName)
        else:
            print("Lista vazia")

    def isBlocked(self):
        if (len(self.readyList) == 0 and len(self.blockedList) > 0):
            return True
        else:
            return False
        
    def allProcessesNotReady(self):
        if (len(self.notStarted) != 0 and len(self.readyList) == 0 and len(self.blockedList) == 0):
            return True
        else:
            return False

    def roundRobin(self): 
        print("\nExecucao dos processos iniciada com RR\n")

        while len(self.readyList) != 0 or len(self.notStarted) != 0:
            self.testArrivalTimeRR()   

            if len(self.readyList) != 0:
                self.activeProcess = self.readyList.pop(0)
               # print("processo ", self.activeProcess.processName, " entrou")
                for i in range(self.activeProcess.quantum):
                    self.time += 1
                    # print("Os time ", str(self.time))
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

                    
                    self.testArrivalTimeRR()   

                    self.addWaitingTime()

                    self.activeProcess.processingTime += 1

                    if len(self.readyList) != 0:
                        if self.readyList[0].priority < self.activeProcess.priority:
                            # print("-----------------trocou----------------------")
                            break

                    self.showLists()

                    # input('\nPressione ENTER para continuar\n')

            if self.activeProcess is not None:
                if self.activeProcess.terminate:
                    self.finishedList.append(self.activeProcess)
                    self.activeProcess.turnaroundTime = self.time - self.activeProcess.arrivalTime 
                elif self.activeProcess.shouldBeBlocked:
                    self.blockedList.append(self.activeProcess)
                    self.activeProcess.blockedUntil = self.time + random.randint(8, 10)
                    # print("processo", self.activeProcess.processName, "bloqueado por ", str(self.activeProcess.blockedUntil - self.time))
                    self.activeProcess.shouldBeBlocked = False
                else:
                    self.readyList.append(self.activeProcess)
                    self.readyList = sorted(self.readyList, key = lambda p : p.priority)

            if self.isBlocked() or self.allProcessesNotReady():
                while len(self.readyList) == 0:
                    self.time += 1
                    # print("tempo acrescentado em bloqueados", str(self.time))
                    for process in self.blockedList:
                            if process.blockedUntil <= self.time:
                                index = self.blockedList.index(process)
                                self.readyList.append(self.blockedList.pop(index))
                                self.readyList = sorted(self.readyList, key = lambda p : p.priority)

                    
                    self.testArrivalTimeRR()   

                    # input('\nPressione ENTER para continuar\n')
                    
                    self.showLists()
        
        for process in self.finishedList:
            print('Tempo do processo', process.processName, '=', str(process.turnaroundTime))

            



# ------------------------ SJF ---------------------------
    def sjf(self):
        print("\nExecucao dos processos iniciada com SJF\n")
        

        while len(self.readyList) != 0 or len(self.notStarted) != 0:
            self.testArrivalTimeSJF()
            
            if len(self.readyList) != 0:
                self.activeProcess = self.readyList.pop(0)
                # print("processo ", self.activeProcess.processName, " entrou")

                while not self.activeProcess.terminate:
                    self.time += 1
                    # print("Os time ", str(self.time))
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
                                self.readyList = sorted(self.readyList, key = lambda p : p.execTime)

                    self.testArrivalTimeSJF()

                    self.addWaitingTime()

                    self.activeProcess.processingTime += 1

                    if len(self.readyList) != 0:
                        if self.readyList[0].execTime < self.activeProcess.execTime:
                            print("-----------------trocou----------------------")
                            break

                    # input('\nPressione ENTER para continuar\n')
                    
                    self.showLists()

            if self.activeProcess is not None:
                if self.activeProcess.terminate:
                    self.finishedList.append(self.activeProcess)
                    self.activeProcess.turnaroundTime = self.time - self.activeProcess.arrivalTime 
                elif self.activeProcess.shouldBeBlocked:
                    self.blockedList.append(self.activeProcess)
                    self.activeProcess.blockedUntil = self.time + random.randint(8, 10)
                    # print("processo", self.activeProcess.processName, "bloqueado por ", str(self.activeProcess.blockedUntil - self.time))
                    self.activeProcess.shouldBeBlocked = False
                else:
                    self.readyList.append(self.activeProcess)
                    self.readyList = sorted(self.readyList, key = lambda p : p.execTime)

            if self.isBlocked() or self.allProcessesNotReady():
                while len(self.readyList) == 0:
                    self.time += 1
                    # print("tempo acrescentado em bloqueados", str(self.time))
                    for process in self.blockedList:
                            if process.blockedUntil <= self.time:
                                index = self.blockedList.index(process)
                                self.readyList.append(self.blockedList.pop(index))
                                self.readyList = sorted(self.readyList, key = lambda p : p.execTime)

                    self.testArrivalTimeSJF()

                    # input('\nPressione ENTER para continuar\n')

                    self.showLists()
        print("----- Todos os programas terminados -----")
        print("Informaçoes sobre os processos:")
        for process in self.finishedList:
            print("Processo ", process.processName, ':')
            print("Waiting time: ", str(process.waitingTime))
            print("Processing time: ", str(process.processingTime))
            print("Turnaround time: ", str(process.turnaroundTime))



if __name__ == '__main__':
    os = Os()
    scheduler = ''

    while scheduler.upper() != 'RR' and scheduler.upper() != 'SJF':
        scheduler = input('Qual escalonador você deseja utilizar? (RR/SJF) ')

    while True:    
        path = input('Insira o nome (path) do processo: ')
        arrivalTime = int(input('Qual é o tempo de chegada do processo? '))

        os.loadProcess(path, arrivalTime)
        
        if scheduler.upper() == 'RR':
            process_priority = int(input('Insira a prioridade desse processo: '))
            os.notStarted[-1].priority = process_priority
            process_quantum = int(input('Insira o quantum desse processo: '))
            os.notStarted[-1].quantum = process_quantum
            print(os.notStarted[-1].processName)

        elif scheduler.upper() == 'SJF': 
            process_execution_time = int(input('Insira o tempo de execução desse processo: '))
            os.notStarted[-1].execTime = process_execution_time

        add_process = input('Você deseja inserir mais algum processo? (S/N) ')

        if add_process.upper() == 'N':
            break
    
    if scheduler.upper() == 'RR':
        os.roundRobin()
    
    elif scheduler.upper() == 'SJF':
        os.sjf()

    # os.loadProcess("ex_pgms_tp1/prog1.txt")
    # os.notStarted[0].execTime = 3
    # os.notStarted[0].arrivalTime = 0


    # os.loadProcess("ex_pgms_tp1/prog2.txt")
    # os.notStarted[1].execTime = 2
    # os.notStarted[0].arrivalTime = 7

    # os.loadProcess("ex_pgms_tp1/prog3.txt")
    # os.notStarted[2].execTime = 1
    # os.notStarted[0].arrivalTime = 0


    # while os.process.terminate == False:
    #     os.executeProcess(os.process)

    # print(os.process.labels[], '-------------------------------------')

    # print(os.process.acc)
