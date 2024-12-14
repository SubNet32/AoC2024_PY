import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

def parseInput(line:str):
    return [int(x) for x in line.replace(" ",",").replace("p=","").replace("v=","").split(",")]


maxX = 101 if len(file) > 100 else 11
maxY = 103 if len(file) > 100 else 7

def move(pos: tuple[int, int], dir: tuple[int, int]):
    newPos = ((pos[0] + dir[0]) % (maxX), (pos[1] + dir[1]) % (maxY))
    if(newPos[0] < 0): newPos[0] += maxX+1
    if(newPos[1] < 0): newPos[1] += maxY+1
    return newPos

def getQuadrant(pos: tuple[int, int]):
    lx = (maxX-1)/2
    ly = (maxY-1)/2
    if(pos[0] < lx and pos[1] < ly):
        return 0
    elif(pos[0] > lx and pos[1] < ly):
        return 1
    elif(pos[0] < lx and pos[1] > ly):
        return 2
    elif(pos[0] > lx and pos[1] > ly):
        return 3
    else:
        return -1

def moveRobot(robot:list[int], steps:int):
    pos = (robot[0], robot[1])
    dir = (robot[2], robot[3])
    startPos = pos

    for _ in range(steps):
        pos = move(pos, dir)
    return pos

def printRobots(robots:set):
    for y in range(0, maxY):
        line = ""
        if(y == (maxY-1)/2):
            print()
            continue
        for x in range(0, maxX):
            if(x == (maxX-1)/2):
                line += " "
            elif((x,y) in robots):
                line += str(robots[(x,y)])
            else:
                line += "."
        print(line)


quadrants = [0,0,0,0]
robots = {}
for line in file:
    robot = parseInput(line)
    finalPos = moveRobot(robot, 100)
    if(finalPos in robots):
        robots[finalPos] += 1
    else:
        robots[finalPos] = 1
    finalQuadrant = getQuadrant(finalPos)

    if(finalQuadrant != -1):
        quadrants[finalQuadrant] += 1

printRobots(robots)
print(quadrants)

print("--- %s seconds ---" % (time.time() - start_time))
print("result", int(quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]))