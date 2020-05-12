import time
import random
import math
import game
import grid
import stats
import types



class MCTS:

    def __init__(self, gameGrid):
        self.grid = gameGrid
        self.root = Node(gameGrid.gameStats)  # fixme avoid grid overriding
        self.root.initiliaze(gameGrid, 0)

    def play(self):
        target = time.time() + 0.33
        playedGames = 0
        while time.time() < target:
            playedGames += 1
            self.root.findMove()

        best = self.__getInitialBest()
        self.__getBestMove(0, self.root.children, [], best)
        res, moves = self.root.getNodeAndMoves(best["cords"])

        game.pacmansInWave(self.grid, moves)
        print(best["score"], playedGames)


    """
        passes children of root and choose the best move
    """
    # fixme maybe should be a function isntead
    def __getBestMove(self, depth, children, cords, best):
        if depth == len(self.root.childrenMoves) - 1:
            # compare results
            i = 0
            for node in children:
                score = node.stats.getScore()
                if score > best["score"]:
                    tmp = cords[:]
                    tmp += [i]
                    best["score"] = score
                    best["cords"] = tmp
                i += 1
        else:
            for i in range(self.root.movesCounts[depth]):
                cords += [i]
                self.__getBestMove(depth + 1, children[i], cords, best)
                cords.pop()

    """
        return score of node at all 0
    """
    def __getInitialBest(self):
        cords = [0 for i in range(len(self.root.movesCounts))]
        best = {
            "cords": cords,
            "score": self.root.getScoreAt(cords)
        }
        return best


"""
    holds game state for particular node, knows it's children and some informations bout their moves
"""
class Node:
    def __init__(self, gameStats):
        self.initiliazed = False
        self.movesCounts = []
        self.childrenMoves = []
        self.children = []
        self.stats = stats.Stats(gameStats)
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
        self.stats = stats.Stats(self.grid.gameStats)
        self.level = level
        self.initiliazed = True

    """
        selects child to play, initilazes if not , calls its play method and saves result
    """
    def findMove(self):
        # todo better selection
        # print("playing at level ", self.level)
        rand = selectRandoms(self.movesCounts)
        res, moves = self.getNodeAndMoves(rand)

        if isinstance(res, list):
            # todo handle finished games better
            return self.grid.gameStats
        if not res.initiliazed:
            newGrid = grid.copyGrid(self.grid)
            game.pacmansInWave(newGrid, moves)
            game.playGhosts(newGrid.maze, newGrid.ghosts, newGrid.pacmans, newGrid.gameStats)
            res.initiliaze(newGrid, self.level + 1)
            if not res.initiliazed:
                # todo handle finished games better
                return self.grid.gameStats
            stats = res.__playRandomGame()
        else:
            stats = res.findMove()

        # print(stats)
        self.stats.saveVisit(stats)
        return stats

    """
        return score of node on indexes
    """
    def getScoreAt(self, indexes):
        res, moves = self.getNodeAndMoves(indexes)
        if isinstance(res, list):
            return self.stats.getScore()
        return res.stats.getScore()

    """
        plays random game and saves stats
    """
    def __playRandomGame(self):
        return game.playRandomGame(grid.copyGrid(self.grid))


    """
        finds and return node with its moves
    """
    def getNodeAndMoves(self, indexes):
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
                addTo += [Node(self.grid.gameStats)]
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
