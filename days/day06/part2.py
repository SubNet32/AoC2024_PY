import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

field = []
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
pos = (-1, -1)
for line in file:
    field.append([c for c in line])
    if(pos[0] > -1): continue
    gStart = line.find("^")
    if(gStart != -1):
        pos = (gStart, len(field) - 1)

def printField(positions: list, mark = "X", obstacle: tuple = (-1, -1)):
    if(len(field) > 20):
        return
    for y in range(len(field)):
        line = ""
        for x in range(len(field[y])):
            if((x,y) in positions):
                line += mark
            elif((x,y) == obstacle):
                line += "0"
            else:
                line += field[y][x]
        print(line)
    print()


def turnRight(dir):
    dir += 1
    if(dir == 4): dir = 0
    return dir

def posIsObstacle(pos: tuple):
    return field[pos[1]][pos[0]] == "#"

def posIsStart(pos: tuple):
    return field[pos[1]][pos[0]] == "^"

def checkOutOfBounds(pos: tuple):
    return (pos[0] < 0 or pos[0] >= len(field[0]) or pos[1] < 0 or pos[1] >= len(field))

def getNext(pos: tuple, dir: int):
    return (pos[0] + directions[dir][0], pos[1] + directions[dir][1])

def checkForLoop(pos: tuple, dir: int, obstaclePos: tuple,):
    trace = {}
    while(True):
        nextPos = getNext(pos, dir)
        if(checkOutOfBounds(nextPos)):
            return False
        if(posIsObstacle(nextPos) or nextPos == obstaclePos):
            dir = turnRight(dir)
            continue
        if(nextPos in trace and dir in trace[nextPos]):
            return trace
   
        pos = nextPos    
        if(pos in trace):
            trace[pos].append(dir)
        else:
            trace[pos] = [dir]
       
        
        

mainDir = 0
result = {}
visited = {}
while(True):
    nextPos = getNext(pos, mainDir)
    if(checkOutOfBounds(nextPos)):
        break
    if(posIsObstacle(nextPos)):
        mainDir = turnRight(mainDir)
        continue
 
    obstacle = nextPos
    if(not obstacle in result and not posIsStart(obstacle) and not obstacle in visited):
        foundLoop = checkForLoop(pos, turnRight(mainDir), obstacle)
        if(foundLoop != False):
            result[obstacle] = True
    pos = nextPos
    visited[pos] = True
  

print("--- %s seconds ---" % (time.time() - start_time))
print("result", len(result))