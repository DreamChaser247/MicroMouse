#!/usr/bin/env python3

from typing import List, Tuple  # Import the Tuple type for type hinting
import math

mapSize = 5

map = [[1 for _ in range(mapSize)] for _ in range(mapSize) ]


#kompas jest potrzebny

# DESCRIPTION OF THE MAP
# the numbers represent what walls surround the specyfic cell.
# the numbers are created by multiplying 1 by specyfic numbers that represent a side where the wall is present
# 2 is for the wall below  ; 3 is for the wall to the left |x
# 5 is for the wall above  ; 7 is for the wall to the right x|
# so number 6 = 2 * 3 will represent a cell with walls between it and a cells below and to the left
# and number 70 = 7 * 5 * 2 will represent a cell with walls on all sides exept the one to the left
# number 1 is for cell with no walls around it

# map[0][4] = 7
# map[5][3] = 2
# map[5][4] = 14
# map[1][4] = 2
# map[6][0] = 2
# map[6][1] = 2
# map[6][2] = 2
# map[6][3] = 2
# map[5][0] = 2
# map[5][1] = 2
# map[5][2] = 2
# map[5][3] = 2
map[1][1] = 42
map[2][0] = 2
map[2][1] = 2
map[2][2] = 2
map[0][2] = 7
map[1][2] = 7
map[2][2] = 14

pathMap = [[0 for _ in range(mapSize)] for _ in range(mapSize) ]

pathMap[0][0] = 1


for row in map:
    print(row)

flowQueue: List[Tuple[int, int]] = [(0, 0)]  # Declare flowQueue with type hint

directions =[(1,0,2),(0,-1,3),(-1,0,5),(0,1,7)]

def ifInside (row: int, col: int, dir: int):
    if row + directions[dir][0] > -1 and row + directions[dir][0] < mapSize and col + directions[dir][1] > -1 and col + directions[dir][1] < mapSize:
        return True
    return False
        
    

def flow(startingPoint: Tuple[int,int]):
    col = startingPoint[1]
    row = startingPoint[0]
    for i in range(0,4):
        if ifInside(row, col, i):
            print(f"column {col} row {row} in direction {i} is valid")
            if map[row][col] % directions[i][2] != 0 and pathMap[row + directions[i][0]][col + directions[i][1]] == 0 :
                pathMap[row + directions[i][0]][col + directions[i][1]] = pathMap[row][col] + 1
                flowQueue.append((row + directions[i][0], col + directions[i][1]))


while(len(flowQueue) > 0):
    flow(flowQueue[0])
    flowQueue.pop(0)
    
print("\n pathMap ")
for row in pathMap:
    print(row)