import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

addition = lambda a,b: a+b
multiplication = lambda a,b: a*b
concat = lambda a,b: int(str(a) + str(b))
operators = [addition, multiplication, concat]

def evaluate(values: list, testValue: int):
    if(len(values) == 1): 
        return values[0] == testValue
    for op in operators:
        value = op(values[0], values[1])
        if(evaluate([value] + values[2:], testValue)):
            return True
    return False

result = 0
for line in file:
    terms = line.split(":")
    testValue = int(terms[0])
    values = [int(v) for v in terms[1].split()]
    if(evaluate(values, testValue)):
        result += testValue


print("--- %s seconds ---" % (time.time() - start_time))
print("result", result)