import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

computers = set[str]()
connections = dict[str, list[str]]()

for line in file:
    a,b = line.split("-")
    computers.add(a)
    computers.add(b)
    if(a not in connections):
        connections[a] = [b]
    else:
        connections[a].append(b)
    if(b not in connections):
        connections[b] = [a]
    else:
        connections[b].append(a)

conMap = dict[str, set[str]]()
def findConnections(computer:str, connected:set[str]):
    if(computer in conMap):
        return conMap[computer]
    for con in connected:
        if(con not in connections[computer]):
            return connected
    best = set[str]()
    for con in connections[computer]:
        if(con in connected):
            continue
        result = findConnections(con, connected | {computer})
        if(len(result) > len(best)):
            best = result
    conMap[computer] = best
    return best


connectionSet = set[str]()
for i, c in enumerate(computers):
    conMap.clear()
    print("checking", i, "/", len(computers) )
    r = findConnections(c, set[str]())
    if(len(r) > len(connectionSet)):
        connectionSet = r

print("--- %s seconds ---" % (time.time() - start_time))
print("result", len(connectionSet), str.join(",", sorted(list(connectionSet))))