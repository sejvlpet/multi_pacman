import time
import random
import game
import grid
import types



class MCTS:

    # todo remember that you work with real grid from the game, if you want to override it, use cpy = game.copyGrid(grid)
    def __init__(self, gameGrid):
        self.grid = gameGrid
        self.root = Node()  # fixme avoid grid overriding
        self.root.initiliaze(gameGrid, 0)
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
        self.movesCounts = []
        self.childrenMoves = []
        self.children = []
    """
        takes deep copy of game grid with game state coresponding to this node
    """
    def initiliaze(self, gameGrid, level):
        self.grid = gameGrid
        self.__setMoves()
        if len(self.childrenMoves) == 0:
            # todo handle locked pacmans - loose
            return
        self.__initiliazeChildren(0, self.children)
        self.level = level
        self.initiliazed = True

    """
        selects child to play, initilazes if not , calls its play method and saves result
    """
    def findMove(self):
        # todo better selection
        # print("playing at level ", self.level)
        rand = selectRandoms(self.movesCounts)
        res, moves = self.__getNodeAndMoves(rand)

        if isinstance(res, list):
            # todo handle finished games better
            return
        if not res.initiliazed:
            newGrid = grid.copyGrid(self.grid)
            game.pacmansInWave(newGrid, moves)
            res.initiliaze(newGrid, self.level + 1)
            if not res.initiliazed:
                # todo handle finished games better
                return
            stats = res.__playRandomGame()
        else:
            # self.__playRandomGame()
            stats = res.findMove()

        # print(stats)
        # return stats

    """
        plays random game and saves stats
    """
    def __playRandomGame(self):
        stats = game.playRandomGame(grid.copyGrid(self.grid))
        # todo set stats - for me and res
        return stats


    """
        finds and return node with its moves
    """
    def __getNodeAndMoves(self, indexes):
        moves = []
        i = 0
        res = self.children
        for r in indexes:
            res = res[r]
            moves += [self.childrenMoves[i][r]]  # this should choose correct move of pacman on this index
            i += 1
        return res, moves

    """
        initialized empty child node
    """
    def __initiliazeChildren(self, depth, addTo):
        if depth == len(self.movesCounts) - 1:
            for i in range(self.movesCounts[depth]):
                addTo += [Node()]
        else:
            for i in range(self.movesCounts[depth]):
                addTo += [[]]
                self.__initiliazeChildren(depth + 1, addTo[i])

    """
        sets all possible moves of children and counts
    """
    def __setMoves(self):
        for pacman in self.grid.pacmans:
            moves = pacman.getMoves(self.grid.maze)
            if len(moves) > 0: # ignore pacmans without moves and let them die their death
                self.movesCounts += [len(moves)]
                self.childrenMoves += [moves[:]]  # fixme check if nothing overrides this

"""
    selects random list from list of move counts
"""
def selectRandoms(movesCounts):
    res = []
    for c in movesCounts:
        res += [random.randint(0, c - 1)]
    return res


"""
    stats bout game
"""
class Stats:
    def __init__(self, grid):
        # todo intializr stats from grid
        pass