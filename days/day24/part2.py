import time
import random
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

O_AND = lambda x,y: x and y
O_OR = lambda x,y: x or y
O_XOR = lambda x,y: x != y

gates = {
    "AND": O_AND,
    "OR": O_OR,
    "XOR": O_XOR,
}

maxR = 0
states = dict[str, bool]()
startWires = set[str]()
endWires = set[str]()
operations = list[list[str]]()
for line in file:
    if(":" in line):
        s,v = line.split(": ")
        states[s] = bool(int(v)) 
        maxR = max(maxR, int(s[1:]))
        startWires.add(s)
        continue
    if("->" in line):
        s1,o,s2,_,t = line.split()
        operations.append([s1,o,s2,t])
        if(t.startswith("z")):
            endWires.add(t)
        continue

operationLevels = list[list[list[str]]]()
reversedOp = dict[str, list[str]]()

def initOperationLevels(initialOperations:list[list[str]]):
    ops = initialOperations.copy()
    operationLevels.clear()
    reversedOp.clear()
    savedOp = set[str](startWires.copy())
    while(ops):
        currentLevel = list[list[str]]()
        opsToRemove = list[list[str]]()
        savedToAdd = set[str]()
        for op in ops:
            s1,o,s2,t = op
            if(s1 in savedOp and s2 in savedOp):
                currentLevel.append(op)
                savedToAdd.add(t)
                opsToRemove.append(op)
                reversedOp[t] = op
        ops = [x for x in ops if x not in opsToRemove]
        savedOp.update(savedToAdd)
        if(len(currentLevel) == 0):
            return False
        operationLevels.append(currentLevel)
    return True

def getRegister(n:int, register:str):
    return register + str(n).rjust(2,"0")

def setState(n:int, register:str):
    for i in range(maxR+1):
        r = getRegister(i, register)
        states[r] = n & (1 << i) > 0

def evaluate():
    for level in operationLevels:
        for op in level:
            s1,o,s2,t = op
            states[t] = gates[o](states[s1],states[s2])
    zStates = ["1" if states[x] else "0" for x in sorted(states) if x.startswith("z")]
    zStateStr = str.join("", reversed(zStates))
    return int(zStateStr,2)

def addNumbers(n1:int, n2:int):
    states.clear()
    setState(n1, "x")
    setState(n2, "y")
    return evaluate()

def getGates(state:str, targetStates:set[str], checkedStates: set[str] = set[str]()):
    s1,_,s2,_ = reversedOp[state]
    # if(s1 in targetStates and s2 in targetStates):
    #     return {state}
    if(s1 in startWires and s2 in startWires):
        if(s1 in targetStates and s2 in targetStates):
            return {state}
        return False

    gates = set[str]()
    if(s1 not in checkedStates):
        r1 = getGates(s1, targetStates, checkedStates | {s1})
        if(r1):
            gates = gates.union(r1)
    if(s2 not in checkedStates):
        r2 = getGates(s2, targetStates, checkedStates | {s2})
        if(r2):
            gates = gates.union(r2)
    return {state} | gates

def testGatesForNumbers(numbers: list[tuple[int,int]], findGates:bool):
    faultyGates = set[str]()
    faultyGatesCount = 0
    for i,i2 in numbers:
        n1 = 1 << i
        n2 = 1 << i2
        r = addNumbers(n1,n2)
        if(r != n1+n2):
            faultyGatesCount += 1
            if(not findGates):
                continue
            zReg = getRegister(i+1, "z")
            zReg2 = getRegister(len(bin(r))-3, "z")
            # print("Found error at",zReg, "bit error", bin(r), zReg2)
            gates = getGates(zReg, set[str]([getRegister(i, "x"), getRegister(i2, "y")]))
            gates2 = getGates(zReg2, set[str]([getRegister(i, "x"), getRegister(i2, "y")]))
            if(gates and len(gates) > 0 and gates2):
                rt3 = addNumbers(n1,0)
                gates3 = gates.copy()
                gates4 = gates.copy()
                zReg3 = ""
                zReg4 = ""
                if(rt3 != n1):
                    zReg3 = getRegister(len(bin(rt3))-3, "z")
                    gates3 = getGates(zReg3, set[str]([getRegister(i, "x"), getRegister(i, "y")]))
                rt4 = addNumbers(0,n2)
                if(rt4 != n2):
                    zReg4 = getRegister(len(bin(rt4))-3, "z")
                    gates4 = getGates(zReg4, set[str]([getRegister(i, "x"), getRegister(i, "y")]))
                  
                faultyGates = faultyGates.union(gates.intersection(gates2.intersection(gates3.intersection(gates4)))) 
                # print("faulty gates", zReg, gates)
                # print("faulty gates2", zReg2, gates2)
                # print("faulty gates3", zReg3, gates3)
                # print("faulty gates4", zReg3, gates4)
                # print("intersection", gates.intersection(gates2.intersection(gates3.intersection(gates4))))
            
       
        
    # print("faulty gates", len(faultyGates), faultyGates)
    # print()
    if(not findGates):
        return faultyGatesCount
    return faultyGates

def testGates(operationsToTest:list[list[str]], findGates:bool):
    # print("----------------------------------------------------------")
    initRes = initOperationLevels(operationsToTest)
    if(not initRes):
        return 1
    remainingGates = testGatesForNumbers([(i,i) for i in range(maxR+1)], True)
    # for _ in range(100000):
    #     values = []
    #     for _ in range(maxR+1):
    #         values.append((random.randint(0, maxR), random.randint(0, maxR)))
    #     gates = testGatesForNumbers(values)
    #     intersection = remainingGates.intersection(gates)
    #     if(len(intersection) == 0):
    #         print("no intersection")
    #         break
    #     remainingGates = intersection
    #     print("remaining gates", len(remainingGates))
    #     if(len(remainingGates) <= 8):
    #         break
    return remainingGates

def swapGates(pairsToSwap = list[tuple[str,str]]):
    resultOperations = []

        # print("swapping", pair[0], " <-> ", pair[1])
    for op in operations:
        for pair in pairsToSwap:
            if(op[3] == pair[0]):
                resultOperations.append(op[:3]+[pair[1]])
                break
            elif(op[3] == pair[1]):
                resultOperations.append(op[:3]+[pair[0]])
                break
        else:
            resultOperations.append(op)
    return resultOperations

errorWires1 = set[str]()
errorWires2 = set[str]()

for op in operations:
        s1,o,s2,t = op
        # all end wires must be XOR or OR in the case of the last wire
        if((t in endWires and o != "XOR" and t != "z45") or (t == "z45" and o != "OR")):
            errorWires1.add(t)
        # wires that are not connected to start or end wires must either be AND or OR
        if(s1 not in startWires and s2 not in startWires and t not in endWires and o == "XOR"):
            errorWires2.add(t)


def findEndGateOfWire(wire:str):
        for op2 in operations:
            s1,o,s2,t = op2
            if(s1 == wire or s2 == wire):
                if(t.startswith("z")):
                    return t
                return findEndGateOfWire(t)

print("errorWires1", errorWires1)
print("errorWires2", errorWires2)
pairsToSwap = list[tuple[str,str]]()
for ew in errorWires2:
    endWire = findEndGateOfWire(ew)
    prevEndWire = "z" + str(int(endWire[1:])-1)
    pairsToSwap.append((ew, prevEndWire))

xV = str.join("", reversed(["1" if states[x] else "0" for x in sorted(states) if x.startswith("x")]))
yV = str.join("", reversed(["1" if states[x] else "0" for x in sorted(states) if x.startswith("y")]))
expectedValue = int(xV,2) + int(yV,2)

newOperations = swapGates(pairsToSwap)
initOperationLevels(newOperations)

newValue = evaluate()
binOverflow =bin(expectedValue ^ newValue)[2:]
overflowErrorAt = len(binOverflow) - binOverflow.index("0")
print(bin(expectedValue ^ newValue))
print(overflowErrorAt)

registerX = getRegister(overflowErrorAt, "x")
registerY = getRegister(overflowErrorAt, "y")
errorWires3 = set[str]()
for op in newOperations:
    s1,o,s2,t = op
    if(s1 == registerX and s2 == registerY or s2 == registerX and s1 == registerY):
        errorWires3.add(t)
        print("found", s1, s2,o, t)
print("errorWires3",errorWires3)

errorWires = list(errorWires1.union(errorWires2).union(errorWires3))

print("--- %s seconds ---" % (time.time() - start_time))
print("result", str.join(",",sorted(errorWires)))
11111110000000000