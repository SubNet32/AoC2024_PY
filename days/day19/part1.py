import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

patterns = [x for x in file[0].split(", ")]

def checkValid(value):
    if(len(value) == 0):
        return True
    for pattern in patterns:
        if(value.startswith(pattern)):
            if(checkValid(value[len(pattern):])):
                return True
    return False

result = 0
for line in file[2:]:
    if(checkValid(line)):
        result += 1


print("--- %s seconds ---" % (time.time() - start_time))
print("result", result)