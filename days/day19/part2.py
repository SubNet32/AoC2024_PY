import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

patterns = [x for x in file[0].split(", ")]

results = dict[str, int]()
def checkValid(value:str):
    if(value in results):
        return results[value]
    result = 0
    if(len(value) == 0):
        return 1
    for pattern in patterns:
        if(value.startswith(pattern)):
            checkResult = checkValid(value[len(pattern):])
            if(checkResult > 0):
                result += checkResult
    results[value] = result
    return result

result = 0
for line in file[2:]:
    results.clear()
    result += checkValid(line)

print("--- %s seconds ---" % (time.time() - start_time))
print("result", result)