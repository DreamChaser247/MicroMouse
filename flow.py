#!/usr/bin/env python3

import math

mapSize = 10

map = [[0 for _ in range(mapSize)] for _ in range(mapSize) ]

map[0][4] = 2

pathMap = [[0 for _ in range(mapSize)] for _ in range(mapSize) ]

for row in map:
    print(row)

def flow(startingPoint: tuple[int,int], map[]):
    if (startingPoint[1] < mapSize-1 and map[startingPoint[0]][startingpoint[1]] % 3 != 0 and pathMap[startingPoint[0]][startingpoint[1]-1] == 0):
        pathMap[startingPoint[0]][startingpoint[1]-1] = pathMap[startingPoint[0]][startingpoint[1]] + 1
    
    if (startingPoint[1] < 0 and map[startingPoint[0]][startingpoint[1]] % 7 != 0 and pathMap[startingPoint[0]][startingpoint[1]+1] == 0):
        pathMap[startingPoint[0]][startingpoint[1]+1] = pathMap[startingPoint[0]][startingpoint[1]] + 1   
    
    if (startingPoint[0] < mapSize-1 and map[startingPoint[0]][startingpoint[1]] % 5 != 0 and pathMap[startingPoint[0]-1][startingpoint[1]] == 0):
        pathMap[startingPoint[0]][startingpoint[1]-1] = pathMap[startingPoint[0]][startingpoint[1]] + 1
    
    if (startingPoint[0] < 0 and map[startingPoint[0]][startingpoint[1]] % 2 != 0 and pathMap[startingPoint[0]+1][startingpoint[1]] == 0):
        pathMap[startingPoint[0]][startingpoint[1]+1] = pathMap[startingPoint[0]][startingpoint[1]] + 1 