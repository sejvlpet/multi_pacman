import random
import grid

# Those constants shall be in main
EMPTY = 0
PILL = 1
STOP_PILL = 2
WALL = 3
GHOST = 4
PACMAN = 5
GHOST_AND_PILL = 6
GHOST_AND_STOP_PILL = 7

def printMaze(maze):
    for line in maze:
           print(line)

def addWalls(maze, length, row, col):
    for i in range(length):
        maze[row + i][col] = WALL


def createWalls(maze):
    rowCount = len(maze)
    collCount = len(maze[0])
    colIterator = 1
    skip = False
    while colIterator < collCount - 1:
        rowIterator = 1
        while rowIterator < rowCount - 1:
            if(random.random() > 0.33):
                length = random.randint(0, int  ((rowCount - rowIterator) / 4))
                addWalls(maze, length, rowIterator, colIterator)
                rowIterator += length
                skip = True
            rowIterator += 1
        if skip:
            colIterator += 1
            skip = False
        colIterator += 1


def addPills(maze):
    pillsCount = 0
    for row in maze:
        for collIterator in range(len(row)):
            if row[collIterator] == EMPTY and random.random() > 0.5:
                row[collIterator] = PILL
                pillsCount += 1

    return pillsCount


def addStopPill(maze):
    deletedPills = 0
    if maze[0][0] == PILL:
        deletedPills += 1 
    maze[0][0] = STOP_PILL

    if maze[0][len(maze[0]) - 1] == PILL:
        deletedPills += 1 
    maze[0][len(maze[0]) - 1] = STOP_PILL

    if maze[len(maze) - 1][0] == PILL:
        deletedPills += 1 
    maze[len(maze) - 1][0] = STOP_PILL

    if maze[len(maze) - 1][len(maze[0]) - 1] == PILL:
        deletedPills += 1 
    maze[len(maze) - 1][len(maze[0]) - 1] = STOP_PILL

    return deletedPills

def generateMaze(rowCount, collCount):
    # start with emty maze
    maze = [[ 0 for i in range(collCount)] for i in range(rowCount)]
    
    createWalls(maze)
    pillsCount = addPills(maze)
    pillsCount -= addStopPill(maze)

    printMaze(maze)

    myGrid = grid.Grid(maze)
    myGrid.draw(maze)
    return maze, pillsCount




generateMaze(39, 70)
