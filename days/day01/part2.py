import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = str(cwd) + "\\input.txt"
file = open(path, "r").read().splitlines()

listA = []
listB = []

for line in file:
    a,b  = [int(x) for x in str.split(line, "   ")]
    listA.append(a)
    listB.append(b)

sum = 0
for element in listA:
    sum += element * len(list(filter(lambda x: x == element, listB)))

print("--- %s seconds ---" % (time.time() - start_time))
print("result", sum)
