from Process import Process


class Os():
    def __init__(self, process):
        self.instrucoes = {
            "aritmetic": ["ADD", "SUB", "MULT", "DIV"],
            "memory": ["LOAD", "STORE"],
            "jump": ["BRANY", "BRPOS", "BRZERO", "BRNEG"],
            "system": ["SYSCALL"]
        }
        self.process: Process = process

    def aritmeticInstructions(self, op1: int, instruction: str, process: Process):
        if instruction == "ADD":
            process.acc += op1
        elif instruction == "SUB":
            process.acc -= op1
        elif instruction == "MULT":
            process.acc *= op1
        elif instruction == "DIV":
            process.acc /= op1
            # LIDAR COM DIV POR 0


    def memoryInstructions(self, op1: int, instruction: str, process: Process):
        if instruction == "LOAD":
            process.acc = op1
        elif instruction == "STORE":
            process.data[op1] = process.acc


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
            print(process.acc)
        elif index == 2:
            process.acc = input("Digite um valor")
            #precisa ser numero


    def executeProcess(self, process: Process):
        instruction = process.code[process.pc]
        process.pc += 1

        if instruction[0] in self.instrucoes["aritmetic"]:
            if instruction[1][0] == "#":
                aux = instruction[1].strip("#")
                op = int(aux)
                self.aritmeticInstructions(op, instruction[0], process)
            else:
                op = process.data[instruction[1]]
                self.aritmeticInstructions(op, instruction[0], process)

        if instruction[0] in self.instrucoes["memory"]:
            if instruction[1][0] == "#":
                aux = instruction[1].strip("#")
                op = int(aux)
                self.memoryInstructions(op, instruction[0], process)
            else:
                op = process.data[instruction[1]]
                self.memoryInstructions(op, instruction[0], process)
        
        if instruction[0] in self.instrucoes["jump"]:
            self.jumpInstructions(instruction[0], process, process.labels[instruction[1]])

        if instruction[0] in self.instrucoes["system"]:
            self.systemInstructions(process, int(instruction[1]))

