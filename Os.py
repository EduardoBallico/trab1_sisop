from Process import Process


class Os():
    def __init__(self, processName):
        self.instrucoes = {
            "aritmetic": ["add", "sub", "mult", "div"],
            "memory": ["load", "store"],
            "jump": ["BRANY", "BRPOS", "BRZERO", "BRNEG"],
            "system": ["syscall"]
        }
        self.process: Process = Process(processName)

    def aritmeticInstructions(self, op1: int, instruction: str, process: Process):
        if instruction == "add":
            process.acc += op1
        elif instruction == "sub":
            process.acc -= op1
            print("acc: ", process.acc)
        elif instruction == "mult":
            process.acc *= op1
        elif instruction == "div":
            process.acc /= op1
            # LIDAR COM DIV POR 0


    def memoryInstructions(self, op1: int or str, instruction: str, process: Process):
        if instruction == "load":
            process.acc = op1
            print("acc: ", process.acc)
        elif instruction == "store":
            process.data[op1] = process.acc
            print("acc: ", process.acc)
            print("op1: ", op1)
            print("process.data[op1]: ", process.data[op1])


    def jumpInstructions(self, instruction: str, process: Process, posLabel: int):
        if instruction == "BRANY":
            process.pc = posLabel
        elif instruction == "BRPOS":
            if process.acc > 0:
                process.pc = posLabel
        elif instruction == "BRZERO":
            print("acc: ", process.acc)
            if process.acc == 0:
                process.pc = posLabel
        elif instruction == "BRNEG":
            if process.acc < 0:
                process.pc = posLabel


    def systemInstructions(self, process: Process, index: int):
        if index == 0:
            process.terminate = True
        elif index == 1:
            print(process.acc)
        elif index == 2:
            process.acc = input("Digite um valor")
            #precisa ser numero


    def executeProcess(self, process: Process):
        print(process.pc)
        instruction = process.code[process.pc]
        print(instruction)
        process.pc += 1

        if instruction[0] in self.instrucoes["aritmetic"]:
            if instruction[1][0] == "#":
                aux = instruction[1].strip("#")
                print("aqui" + aux)
                op = int(aux)
                self.aritmeticInstructions(op, instruction[0], process)
            else:
                op = int(process.data[instruction[1]])
                self.aritmeticInstructions(op, instruction[0], process)

        elif instruction[0] in self.instrucoes["memory"]:
            if instruction[1] == "load":
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
            print(int(instruction[1]))
            self.systemInstructions(process, int(instruction[1]))



os = Os("ex_pgms_tp1/prog2.txt")
while os.process.terminate == False:
    os.executeProcess(os.process)

# print(os.process.labels[], '-------------------------------------')

print(os.process.acc)