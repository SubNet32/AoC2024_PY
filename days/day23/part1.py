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
    if(a.startswith("t")):
        computers.add(a)
    if(b.startswith("t")):
        computers.add(b)
    if(a not in connections):
        connections[a] = [b]
    else:
        connections[a].append(b)
    if(b not in connections):
        connections[b] = [a]
    else:
        connections[b].append(a)


connectionSets = set[tuple[str,str,str]]()
for c in computers:
    if(len(connections[c]) < 2):
        continue
    for c2 in connections[c]:
        for c3 in connections[c]:
            if(c2 == c3):
                continue
            if(c2 in connections[c3] and c3 in connections[c2]):
                connectionSets.add(tuple(sorted([c,c2,c3])))

print("--- %s seconds ---" % (time.time() - start_time))
print("result", len(connectionSets))