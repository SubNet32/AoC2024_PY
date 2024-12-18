import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

directions = [(0,1), (0,-1), (1,0), (-1,0)]

maxX = 70 if len(file) > 1000 else 6
maxY = 70 if len(file) > 1000 else 6
end = (maxX, maxY)
walls = set[tuple[int]]()
limit = 1024 if len(file) > 1000 else 12
for i, line in enumerate(file):
    if i >= limit:
        break
    x,y = [int(x) for x in line.split(",")]
    walls.add((x,y))
index = i

def move(pos: tuple[int], dir: tuple[int]) -> tuple[int]:
    return pos[0] + dir[0], pos[1] + dir[1]

def checkOutOfBounds(pos: tuple[int]):
    return (pos[0] < 0 or pos[0] > maxX or pos[1] < 0 or pos[1] > maxY)

def printField(pos: tuple[int]):
    for y in range(maxY+1):
        line = ""
        for x in range(maxX+1):
            if((x,y) in walls):
                line += "#"
            elif((x,y) == pos):
                line += "X"
            else:
                line += "."
        print(line)

def getAdjacentPositions(current: tuple[int]) -> list[tuple[int]]:
    adjPos: list[tuple[int]] = []
    for dir in directions:
        movedPos = move(current, dir)
        if(movedPos in walls or checkOutOfBounds(movedPos)):
            continue
        adjPos.append(movedPos)
    return adjPos

def getDist(pos: tuple[int], pos2: tuple[int]) -> int:
    return abs(pos[0] - pos2[0]) + abs(pos[1] - pos2[1])

def getPath(visited: dict[tuple[int], int], cost :int) -> set[tuple[int]]:
    toCheck = dict[int, list[tuple[int]]]()
    for k,v in visited.items():
        if(v in toCheck):
            toCheck[v].append(k)
        else:
            toCheck[v] = [k]
    pos = end
    path = set[tuple[int]]()
    path.add(pos)
    while(True):
       cost -= 1
       pos = [ x for x in toCheck[cost] if getDist(pos, x) == 1].pop(0)
       if(pos == (0,0)):
           break
       path.add(pos)
    return path

takenPath = None
while(True):
    x,y = [int(x) for x in file[index].split(",")]
    walls.add((x,y))

    if(takenPath != None and (x,y) not in takenPath):
        index += 1
        continue

    # print("index", index)
    # printField((0,0))
    # print()

    pos = (0,0)
    cost = 0
    visited = dict[tuple[int], int]()
    toVisit = dict[tuple[int], int]()
    while(pos != end):
        visited[pos] = cost
        adjPositions = getAdjacentPositions(pos)
        for adjPos in adjPositions:
            if(adjPos in visited or adjPos in toVisit):
                continue
            else:
                toVisit[adjPos] = cost + 1
        if(len(toVisit) == 0):
            print("No path found")
            print("--- %s seconds ---" % (time.time() - start_time))
            print("result", file[index])
            exit()
        lowestCost = min(toVisit, key = toVisit.get)
        pos = lowestCost
        cost = toVisit.pop(lowestCost)    
    takenPath = getPath(visited, cost)
    index += 1

