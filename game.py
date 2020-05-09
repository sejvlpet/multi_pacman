import ghost
import grid
import math
import MCTS


def getDistance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


# return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) # works weirdly with that


def valid(row, col, maze):
    return row < len(maze) and col < len(maze[0]) and row >= 0 and col >= 0 and maze[row][col] != grid.WALL


def play(gameGrid, real=True):
    pacmans = gameGrid.pacmans
    ghosts = gameGrid.ghosts
    maze = gameGrid.maze
    gameStats = gameGrid.gameStats

    for i in range(len(pacmans)):
        pos = pacmans[i].getCord()
        maze[pos[0]][pos[1]].remove("pacman")

        pos = pacmans[i].move(gameGrid, real)
        maze[pos[0]][pos[1]].place("pacman", gameStats)
        pacmans[i].cord = pos
    mcts = MCTS.MCTS(grid.copyGrid(gameGrid))
    mcts.play()

    for i in range(len(ghosts)):
        pos = ghosts[i].getCord()
        maze[pos[0]][pos[1]].removeGhost()

        pos = ghosts[i].move(maze, pacmans)
        maze[pos[0]][pos[1]].placeGhost(pacmans, pos, gameStats)
        ghosts[i].cord = pos

    return gameStats["pacmanCount"] <= 0 or gameStats["pillCount"] <= 0
