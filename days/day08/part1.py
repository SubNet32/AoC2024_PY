import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

antennas = {}
maxY = len(file)-1
maxX = len(file[0])-1
for y in range(len(file)):
    for x in range(len(file[y])):
        c = file[y][x]
        if(c == "."): continue
        if(c not in antennas): antennas[c] = [(x,y)]
        else: antennas[c].append((x,y))

def subtractPoints(a:tuple, b:tuple):
    return (a[0]-b[0], a[1]-b[1])

def addPoints(a:tuple, b:tuple):
    return (a[0]+b[0], a[1]+b[1])

def checkInBounds(a:tuple):
    return a[0] >= 0 and a[0] <= maxX and a[1] >= 0 and a[1] <= maxY

def calcAntiNodesFor(a:tuple, b:tuple):
    result = [addPoints(a, subtractPoints(a,b)), addPoints(b, subtractPoints(b,a))]
    return [p for p in result if checkInBounds(p)]
    

result = {}
for a in antennas:
    for i in range(len(antennas[a])-1):
        for j in range(i+1, len(antennas[a])):
            antiNodes = calcAntiNodesFor(antennas[a][i], antennas[a][j])
            for p in antiNodes:
                result[p] = True


print("--- %s seconds ---" % (time.time() - start_time))
print("result", len(result))