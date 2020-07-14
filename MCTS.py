import time
import random
import game
import grid
import stats

"""
    initializes root and searech monte carlo tree
"""
class MCTS:

    def __init__(self, gameGrid, mtcs):
        self.grid = gameGrid
        self.root = Node(gameGrid.gameStats)
        self.root.initiliaze(gameGrid, 0)
        self = mtcs
    """
        searech for best move for a given amount of time
    """
    def play(self):
        target = time.time() + 0.33
        playedGames = 0
        while time.time() < target:
            playedGames += 1
            self.root.findMove()

        if len(self.root.movesCounts) > 0:
            best = self.root.getInitialBest(True)
            self.root.getBestMove(0, self.root.children, [], best, True)
            res, moves = self.root.getNodeAndMoves(best["cords"])

            # print("games from root: ", playedGames, " possible games from root: ", self.root.multiply())
            game.pacmansInWave(self.grid, moves)
            print(playedGames)
            return best["mtcs"]


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
            return
        self.__initiliazeChildren(0, self.children)
        self.stats = stats.Stats(self.grid.gameStats)
        self.level = level
        self.initiliazed = True

    """
        selects child to play, initilazes if not , calls its play method and saves result
    """
    def findMove(self):
        if len(self.movesCounts) == 0:
            return self.grid.gameStats
        best = self.getInitialBest(False)
        self.getBestMove(0, self.children, [], best, False)
        res, moves = self.getNodeAndMoves(best["cords"])

        if not res.initiliazed:
            newGrid = grid.copyGrid(self.grid)
            game.pacmansInWave(newGrid, moves)
            game.playGhosts(newGrid.maze, newGrid.ghosts, newGrid.pacmans, newGrid.gameStats)
            res.initiliaze(newGrid, self.level + 1)
            if not res.initiliazed:
                return self.grid.gameStats
            stats = res.__playRandomGame()
        else:
            stats = res.findMove()

        self.stats.saveVisit(stats)
        return stats

    """
        passes children of root and choose the best move
    """
    def getBestMove(self, depth, children, cords, best, final):
        if depth == len(self.movesCounts) - 1:
            # compare results
            i = 0
            for node in children:
                score = node.stats.getScore() if final else node.stats.getRandomMetric()
                if score > best["score"]:
                    best["score"] = score
                    tmp = cords[:]
                    tmp += [i]
                    best["cords"] = tmp
                    best["mtcs"] = node
                i += 1
        else:
            for i in range(self.movesCounts[depth]):
                cords += [i]
                self.getBestMove(depth + 1, children[i], cords, best, final)
                cords.pop()

    """
        return score of node at all 0
    """
    def getInitialBest(self, final):
        cords = [0 for i in range(len(self.movesCounts))]
        best = {
            "cords": cords,
            "score": self.__getStatsAt(cords).getScore() if final else self.__getStatsAt(cords).getRandomMetric(),
            "mtcs": self
        }
        return best

    """
        gets count of possible moves
    """
    def multiply(self):
        res = 1
        for c in self.movesCounts:
            res *= c
        return res

    """
        return score of node on indexes
    """
    def __getStatsAt(self, indexes):
        res, moves = self.getNodeAndMoves(indexes)
        if isinstance(res, list):
            return self.stats
        return res.stats

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
            moves += [self.childrenMoves[i][r]]
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
                self.childrenMoves += [moves[:]]

"""
    selects random list from list of move counts
"""
def selectRandoms(movesCounts):
    res = []
    for c in movesCounts:
        res += [random.randint(0, c - 1)]
    return res
