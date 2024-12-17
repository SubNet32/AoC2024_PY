import time
import math
from termcolor import colored
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
    

program = [int(x) for x in file[4].split(": ")[1].split(",")]
reversedProgram = reversed(program)
initialB =int(file[1].split(": ")[1])
initialC = int(file[2].split(": ")[1])


# 8 = len 2     2^3
# 64 = len 3    2^6
# 512 = len 4   2^9
# 4.096 = len 5
# min 32768
# max 262144
# 117448


initMinV = 2 ** ((len(program)-1) * 3)
minV = initMinV
initMaxV =2 ** ((len(program)) * 3)
maxV = initMaxV

# step = math.floor((maxV-minV) / 1000)

testValue = minV
smoothness = 4096
while(True):   
    testValue = minV
    step = 1 if maxV-minV < 1_000_000 else math.floor((maxV-minV) / smoothness)
    lowestV = 0
    highestV = 0
    bestC = 0
    while(testValue <= maxV):
        data = Data()
        data.A = testValue
        data.B = initialB
        data.C = initialC
        data.Pointer = 0
        data.Out = []
        while(data.Pointer < len(program)):
            code = program[data.Pointer]
            operand = program[data.Pointer + 1]
            noIncrease = runInstruction(data, code, operand)
            if(not noIncrease): data.Pointer += 2
        if(data.Out == program):
            print(testValue, str.join(" ",[colored(str(x), "yellow") if program[i] ==x else str(x) for i, x in enumerate(data.Out)]))
            print("result", testValue)
            print("--- %s seconds ---" % (time.time() - start_time))
            exit()
        # print(testValue, str.join(" ",[colored(str(x), "yellow") if program[i] ==x else str(x) for i, x in enumerate(data.Out)]))

        correctValues = 0
        for i in range(len(program)-1, 0, -1):
            if(data.Out[i] != program[i]):
                break
            correctValues += 1
        if(bestC < correctValues):
            bestC = correctValues
            lowestV = testValue
            highestV = testValue
        elif(correctValues == bestC):
            highestV = testValue
        testValue += step

    newMin = max(minV, lowestV - step)
    newMax = min(maxV, highestV + step)
    if(newMin == minV and newMax == maxV or step == 1):
        minV = initMinV
        maxV = initMaxV
        smoothness = math.floor(smoothness * 1.01) # times 1.01 to introduce some noise to increase the probability of success
        print("Retry with smoothness", smoothness)
    else:
        minV = newMin
        maxV = newMax
        print("new best", bestC, "range", minV, maxV)
        print()

        
            
