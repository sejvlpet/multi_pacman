import grid
import MCTS
"""
    This file contains methods for game play
"""


def getDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def valid(row, col, maze):
    return row < len(maze) and col < len(maze[0]) and row >= 0 and col >= 0 and maze[row][col] != grid.WALL


def getNeighbors(cord, maze):
    neighbors = []
    if valid(cord[0] + 1, cord[1], maze):
        neighbors += [[cord[0] + 1, cord[1]]]
    if valid(cord[0] - 1, cord[1], maze):
        neighbors += [[cord[0] - 1, cord[1]]]

    if valid(cord[0], cord[1] + 1, maze):
        neighbors += [[cord[0], cord[1] + 1]]

    if valid(cord[0], cord[1] - 1, maze):
        neighbors += [[cord[0], cord[1] - 1]]

    return neighbors[:]

"""
    takes care about play
    returns true if game's over
"""
def play(gameGrid, real=True):
    gameGrid.gameStats["round"] += 1
    pacmans = gameGrid.pacmans
    ghosts = gameGrid.ghosts
    maze = gameGrid.maze
    gameStats = gameGrid.gameStats

    playPacmans(gameGrid, maze, pacmans, gameStats, real)
    playGhosts(maze, ghosts, pacmans, gameStats)

    return gameStats["pacmanCount"] <= 0 or gameStats["pillCount"] <= 0

"""
    takes care about pacmans
"""
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
"""
    takes care about ghosts
"""
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
        if maze[move[0]][move[1]].members["pacman"]:
            i += 1
            continue
        maze[pos[0]][pos[1]].remove("pacman")
        maze[move[0]][move[1]].place("pacman", gameStats)

        pacmans[i].cord = move
        i += 1

"""
    randomly plays and returns stats
"""
def playRandomGame(grid):
    tmp = grid.gameStats["pillCount"]
    maxLength = len(grid.maze) + len(grid.maze[0])
    if grid.gameStats["pillCount"] < 3:
        i = maxLength * 5
    elif grid.gameStats["pillCount"] > 0 and grid.gameStats["pillCount"] < 4:
        i = maxLength / grid.gameStats["pillCount"]
    else:
        i = maxLength / 4
    saved = False
    round = 0
    while not play(grid, False) and i > 0:
        if not saved and tmp != grid.gameStats["pillCount"]:
            grid.gameStats["firstEatenAt"] += i
            saved = True
        i -= 1
        round += 1

    grid.gameStats["round"] += round
    if grid.gameStats["pacmanCount"] == 0:
        grid.gameStats["looses"] = 1
    if grid.gameStats["pillCount"] == 0:
        grid.gameStats["wins"] = 1
    return grid.gameStats