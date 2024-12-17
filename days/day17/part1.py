import time
import math
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

class Data:
    A: int
    B: int
    C: int
    Pointer: int
    Out: list[int]

    def getComboValue(self, combo:int):
        if(combo <= 3):
            return combo
        if(combo == 4):
            return self.A
        if(combo == 5):
            return self.B
        if(combo == 6):
            return self.C
        raise Exception("Invalid combo")

data = Data()
data.A = int(file[0].split(": ")[1])
data.B = int(file[1].split(": ")[1])
data.C = int(file[2].split(": ")[1])
data.Pointer = 0
data.Out = []

program = [int(x) for x in file[4].split(": ")[1].split(",")]

def runInstruction(data:Data, code:int, operand: int):
    if(code == 0):
        data.A = math.floor(data.A / 2 ** data.getComboValue(operand))
        return
    if(code == 1):
        data.B = data.B ^ operand
        return
    if(code == 2):
        data.B = data.getComboValue(operand) % 8
        return
    if(code == 3):
        if(data.A == 0):
            return
        data.Pointer = operand
        return True
    if(code == 4):
        data.B = data.B ^ data.C
        return
    if(code == 5):
        data.Out.append(data.getComboValue(operand) % 8)
        return
    if(code == 6):
        data.B = math.floor(data.A / 2 ** data.getComboValue(operand))
        return
    if(code == 7):
        data.C = math.floor(data.A / 2 ** data.getComboValue(operand))
        return
    raise Exception("Invalid instruction")
    

while(data.Pointer < len(program)):
    code = program[data.Pointer]
    operand = program[data.Pointer + 1]
    noIncrease = runInstruction(data, code, operand)
    if(not noIncrease): data.Pointer += 2



print("--- %s seconds ---" % (time.time() - start_time))
print("result", str.join(",", [str(x) for x in data.Out]))