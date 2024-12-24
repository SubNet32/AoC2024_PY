import time
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

states = dict[str, bool]()
operations = list[list[str]]()
for line in file:
    if(":" in line):
        s,v = line.split(": ")
        states[s] = bool(int(v))
        continue
    if("->" in line):
        s1,o,s2,_,t = line.split()
        operations.append([s1,o,s2,t])
        continue

savedOp = set[str](states.keys())
operationLevels = list[list[list[str]]]()
while(operations):
    currentLevel = list[list[str]]()
    opsToRemove = list[list[str]]()
    for op in operations:
        s1,o,s2,t = op
        if(s1 in savedOp and s2 in savedOp):
            currentLevel.append(op)
            savedOp.add(t)
            opsToRemove.append(op)
    operations = [x for x in operations if x not in opsToRemove]
    operationLevels.append(currentLevel)


for level in operationLevels:
    for op in level:
        s1,o,s2,t = op
        states[t] = gates[o](states[s1],states[s2])


zStates = ["1" if states[x] else "0" for x in sorted(states) if x.startswith("z")]
zStateStr = str.join("", reversed(zStates))
result = int(zStateStr,2)


print("--- %s seconds ---" % (time.time() - start_time))
print("result", result)