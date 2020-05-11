import time
import grid
import math
import MCTS


def getDistance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


# return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) # works weirdly with that


def valid(row, col, maze):
    return row < len(maze) and col < len(maze[0]) and row >= 0 and col >= 0 and maze[row][col] != grid.WALL

"""
    takes care about play
    returns true if game's over
"""
def play(gameGrid, real=True):
    pacmans = gameGrid.pacmans
    ghosts = gameGrid.ghosts
    maze = gameGrid.maze
    gameStats = gameGrid.gameStats

    playPacmans(gameGrid, maze, pacmans, gameStats, real)
    playGhosts(maze, ghosts, pacmans, gameStats)

    return gameStats["pacmanCount"] <= 0 or gameStats["pillCount"] <= 0

def playPacmans(gameGrid, maze, pacmans, gameStats, real):
    if not real:
        for i in range(len(pacmans)):
            pos = pacmans[i].getCord()
            maze[pos[0]][pos[1]].remove("pacman")

            pos = pacmans[i].move(gameGrid)
            maze[pos[0]][pos[1]].place("pacman", gameStats)
            pacmans[i].cord = pos
    else:
        mcts = MCTS.MCTS(gameGrid)
        mcts.play()

def playGhosts(maze, ghosts, pacmans, gameStats):
    for i in range(len(ghosts)):
        pos = ghosts[i].getCord()
        maze[pos[0]][pos[1]].removeGhost()

        pos = ghosts[i].move(maze, pacmans)
        maze[pos[0]][pos[1]].placeGhost(pacmans, pos, gameStats)
        ghosts[i].cord = pos

"""
    move pacmans on grid as moves say and let ghosts play
"""
def pacmansInWave(grid, moves):
    i = 0
    maze = grid.maze
    pacmans = grid.pacmans
    gameStats = grid.gameStats
    for move in moves:
        pos = pacmans[i].getCord()
        maze[pos[0]][pos[1]].remove("pacman")
        maze[move[0]][move[1]].place("pacman", gameStats)

        pacmans[i].cord = move
        i += 1

"""
    randomly plays and returns stats
"""
def playRandomGame(grid):
    target = time.time() + 0.01
    round = 0
    while not play(grid, False) and time.time() < target:
        # round += 1
        pass
    # print("finished in ", round, " rounds")
    return grid.gameStats