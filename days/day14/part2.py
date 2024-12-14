import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

def parseInput(line:str):
    return [int(x) for x in line.replace(" ",",").replace("p=","").replace("v=","").split(",")]


maxX = 101
maxY = 103

def moveRobot(pos: tuple[int, int], dir: tuple[int, int]):
    newPos = ((pos[0] + dir[0]) % (maxX), (pos[1] + dir[1]) % (maxY))
    if(newPos[0] < 0): newPos[0] += maxX+1
    if(newPos[1] < 0): newPos[1] += maxY+1
    return newPos

def printRobots(robots:set):
    for y in range(0, maxY):
        line = ""
        for x in range(0, maxX):
            if((x,y) in robots):
                line += str(robots[(x,y)])
            else:
                line += "."
        print(line)


robots = []
for line in file:
    robot = parseInput(line)
    pos = (robot[0], robot[1])
    dir = (robot[2], robot[3])
    robots.append([pos, dir])

step = 0
while(True):
    step += 1
    robotPositions = {}
    anyOverlap = False
    for robot in robots:
        robot[0] = moveRobot(robot[0], robot[1])
        if(robot[0] in robotPositions):
            robotPositions[robot[0]] += 1
            anyOverlap = True
        else:
            robotPositions[robot[0]] = 1
    if(not anyOverlap):
        printRobots(robotPositions)
        print("step", step)
        print()
        break
   
print("--- %s seconds ---" % (time.time() - start_time))
print("result", step)