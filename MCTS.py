import time
import random
import game
import grid


class MCTS:

    # todo remember that you work with real grid from the game, if you want to override it, use cpy = game.copyGrid(grid)
    def __init__(self, gameGrid):
        self.grid = gameGrid
        self.root = Node()  # fixme avoid grid overriding
        self.root.initiliaze(gameGrid)
        self.stats = Stats(gameGrid)

    def play(self):
        target = time.time() + 1
        playedGames = 0
        while time.time() < target:
            playedGames += 1
            self.root.findMove()
        print(playedGames)
        # todo choose best serie of moves




"""
    holds game state for particular node, knows it's children and some informations bout their moves
"""
class Node:
    def __init__(self, ):
        self.initiliazed = False

    """
        creates deep copy of game grid with game state coresponding to this node
    """
    def initiliaze(self, gameGrid):
        self.grid = gameGrid
        self.__setMoves()
        self.children = []
        self.__initiliazeChildren(0, self.children)
        self.initiliazed = True

    """
        selects child to play, initilazes if not , calls its play method and saves result
    """
    def findMove(self):
        rand = selectRandoms(self.movesCounts)
        moves = []
        i = 0
        res = self.children
        for r in rand:
            res = res[r]
            moves += [self.childrenMoves[i][r]] # this should choose correct move of pacman on this index
            i += 1
        # todo handle this branch by moves above
        if not res.initiliazed:
            newGrid = grid.copyGrid(self.grid)
            game.pacmansInWave(newGrid, moves)
            res.initiliaze(newGrid)
        stats = game.playRandomGame(grid.copyGrid(res.grid))
        print(stats)
    """
        initialized empty child node
    """
    def __initiliazeChildren(self, depth, addTo):
        if depth == len(self.movesCounts) - 1:
            for i in range(self.movesCounts[depth]):
                # todo initialize with deepCopy of grid and moved pacmans
                addTo += [Node()]

        else:
            for i in range(self.movesCounts[depth]):
                addTo += [[]]
                self.__initiliazeChildren(depth + 1, addTo[i])

    """
        sets all possible moves of children and counts
    """
    def __setMoves(self):
        self.movesCounts = []
        self.childrenMoves = []
        for pacman in self.grid.pacmans:
            moves = pacman.getMoves(self.grid.maze)
            self.movesCounts += [len(moves)]
            self.childrenMoves += [moves[:]]  # fixme check if nothing overrides this

"""
    selects random node from list of move counts
"""
def selectRandoms(movesCounts):
    res = []
    for c in movesCounts:
        # fixme if pacman has no move left, random number from 0 to 0 is beeing selected and rondit fails
        res += [random.randint(1, c) - 1]
    return res


"""
    stats bout game
"""
class Stats:
    def __init__(self, grid):
        # todo intializr stats from grid
        pass