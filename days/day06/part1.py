import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

field = []
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
visited = {}
dir = 0
x = -1
y = -1
for line in file:
    field.append([c for c in line])
    if(x > -1): continue
    gStart = line.find("^")
    if(gStart != -1):
        x = gStart
        y = len(field) - 1

def printField(pos: tuple):
    for y in range(len(field)):
        line = ""
        for x in range(len(field[y])):
            if(x == pos[0] and y == pos[1]):
                line += "X"
            else:
                line += field[y][x]
        print(line)
    print()

while(True):
    if(len(field) < 20):
        printField((x, y))
    nextX = x + directions[dir][0]
    nextY = y + directions[dir][1]
    if(nextX < 0 or nextX >= len(field[0]) or nextY < 0 or nextY >= len(field)):
        break
    if(field[nextY][nextX] == "#"):
        dir += 1
        if(dir == 4): dir = 0
        continue
    x = nextX
    y = nextY
    visited[x,y] = True

print("--- %s seconds ---" % (time.time() - start_time))
print("result", len(visited))