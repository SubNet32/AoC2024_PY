import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

directions = [(0,1), (0,-1), (1,0), (-1,0)]
walls: set[tuple[int]] = set()
start = (0,0)
end = (0,0)

class Position:
    pos: tuple[int]
    dir: tuple[int]
    cost: int
    prev: tuple[int] | None
    def __init__(self, cost: int, pos: tuple[int], dir: tuple[int], prev: tuple[int] | None):
        self.pos = pos
        self.dir = dir
        self.cost = cost
        self.prev = prev

for y, line in enumerate(file):
    for x, char in enumerate(line):
        if(char == "#"):
            walls.add((x,y))
        elif(char == "S"):
            start = (x,y)
        elif(char == "E"):
            end = (x,y)

def move(pos: tuple[int], dir: tuple[int]) -> tuple[int]:
    return pos[0] + dir[0], pos[1] + dir[1]

def inverseDir(dir: tuple[int]) -> tuple[int]:
    return (-dir[0], -dir[1])

def getAdjacentPositions(current: Position) -> list[Position]:
    adjPos: list[list[int, tuple, tuple]] = []
    for dir in directions:
        if(dir == inverseDir(current.dir)):
            continue
        movedPos = move(current.pos, dir)
        if(movedPos in walls):
            continue
        cost = 1 if current.dir == dir else 1001
        adjPos.append(Position(current.cost+cost, movedPos, dir, current.pos))
    return adjPos

def printField(pos: tuple[int]):
    for y in range(len(file)):
        line = ""
        for x in range(len(file[0])):
            if((x,y) in walls):
                line += "#"
            elif((x,y) == pos):
                line += "+"
            else:
                line += " "
        print(line)


current = Position(0, start, (1,0), None)
visited = set[tuple[int]]()
toVisit = dict[tuple[int], Position]()
result = 0
while(current != end):
    # print("Cost", current.cost)
    # printField(current.pos)
    # print()
    visited.add(current.pos)
    adjPositions = getAdjacentPositions(current)
    for adjPos in adjPositions:
        if(adjPos.pos == end):
            result = adjPos.cost
            break
        if(adjPos.pos in visited):
            continue
        if(adjPos.pos in toVisit):
            if(toVisit[adjPos.pos].cost > adjPos.cost):
                toVisit[adjPos.pos] = adjPos
        else:
            toVisit[adjPos.pos] = adjPos
    if(result > 0):
        break
    lowestCost = None
    for pos in toVisit:
        if(lowestCost == None or toVisit[pos].cost < toVisit[lowestCost].cost):
            lowestCost = pos
    current = toVisit.pop(lowestCost)
    
    
print("--- %s seconds ---" % (time.time() - start_time))
print("result", result)