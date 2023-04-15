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
            #LIDAR COM DIV POR 0

def memoryInstructions(self, op1: str, instruction: str, process: Process):
        if instruction == "LOAD":
            process.acc = op1
        elif instruction == "STORE":
             process.data[op1] = process.acc


def memoryInstructions(self, instruction: str, process: Process, posLabel: int):
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
        
def memoryInstructions(self, process: Process, index: int):
    if index == 0:
        pass
    elif index == 1:
        pass
    elif index == 2:
        pass