import time
import numpy as np
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

def parseValues(lines: list[str]) -> tuple[float]:
    a = tuple([int(x.split("+")[1]) for x in (lines[0].split(": ")[1].split(", "))])
    b =  tuple([int(x.split("+")[1]) for x in (lines[1].split(": ")[1].split(", "))])
    r = tuple([int(x.split("=")[1]) + 10000000000000 for x in (lines[2].split(": ")[1].split(", "))])
    return a,b,r


def solve_for_A_and_B(RX:int, RY:int, X1:int, X2:int, Y1:int, Y2:int):
    c_matrix = np.array([[X1, X2], [Y1, Y2]])
    constants = np.array([RX, RY])
    A, B = np.linalg.solve(c_matrix, constants)

    return round(A,2), round(B,2) 

sum = 0
for i in range(0,len(file), 4):
    a,b,r  = parseValues(file[i:i+3])
    A,B = solve_for_A_and_B(r[0], r[1], a[0], b[0], a[1], b[1])

    print(f"A: {A}, B: {B}")
    if(A > 0 and B > 0 and A.is_integer() and B.is_integer()):
        sum += A*3 + B*1
   

print("--- %s seconds ---" % (time.time() - start_time))
print("result", int(sum))