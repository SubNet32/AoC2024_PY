import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

def move(pos: tuple[int], direction: tuple[int]):
    return (pos[0] + direction[0], pos[1] + direction[1])

directions =[(1, 0), (0, 1), (-1, 0), (0, -1)]
positions = set[tuple[int]]()
start = (0, 0)
end = (0,0)
for y, line in enumerate(file):
    for x, char in enumerate(line):
        if char == "." or char == "S" or char == "E":
            positions.add((x, y))
        if char == "S":
            start = (x, y)
        if char == "E":
            end = (x, y)

maxX = len(file[0])
maxY = len(file)

path = dict[tuple[int], int]()
pos = start
t = 0
path[pos] = t

while pos != end:
    t += 1
    for d in directions:
        p1 = move(pos,d)
        if p1 in positions and p1 not in path:
            pos = p1
            path[pos] = t
            break

tMax = 20
def getAllCheats(pos: tuple[int]):
    cheats = dict[int, int]()
    for dx in range(max(0, pos[0]-tMax), min(pos[0]+tMax+1, maxX)):
        dxt = abs(dx - pos[0])
        for dy in range(max(0, pos[1] - tMax + abs(dxt)), min(pos[1] + tMax + 1 - abs(dxt), maxY)):
            dyt = abs(dy - pos[1])
            pm = (dx, dy)
            if(pm == pos):
                continue
            if(pm in path):
                save = path[pm] - path[pos] - dxt - dyt
                if(save >= 100):
                    if(save not in cheats):
                        cheats[save] = 1
                    else:
                        cheats[save] += 1
    return cheats
          
   

saved = dict[int, int]()
total = 0
for pos in path:
    cheats = getAllCheats(pos)
    for c in cheats:
        if(c not in saved):
            saved[c] = cheats[c]
        else:
            saved[c] += cheats[c]
        total += cheats[c]

print("--- %s seconds ---" % (time.time() - start_time))
print("result", total)
