import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

directions = [(0,1), (0,-1), (1,0), (-1,0)]

maxX = 70 if len(file) > 1000 else 6
maxY = 70 if len(file) > 1000 else 6
exit = (maxX, maxY)
walls = set[tuple[int]]()
limit = 1024 if len(file) > 1000 else 12
for i, line in enumerate(file):
    if i >= limit:
        break
    x,y = [int(x) for x in line.split(",")]
    walls.add((x,y))


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

printField((0,0))
pos = (0,0)
cost = 0
visited = dict[tuple[int], int]()
toVisit = dict[tuple[int], int]()
while(pos != exit):
    visited[pos] = cost
    adjPositions = getAdjacentPositions(pos)
    for adjPos in adjPositions:
        if(adjPos in visited or adjPos in toVisit):
            continue
        else:
            toVisit[adjPos] = cost + 1
    
    lowestCost = min(toVisit, key = toVisit.get)
    pos = lowestCost
    cost = toVisit.pop(lowestCost)    

print("--- %s seconds ---" % (time.time() - start_time))
print("result", cost)