from copy import deepcopy
import datetime
import time
import random


class MCTS:

    def __init__(self, grid):
        self.grid = grid
        self.root = Node(grid) # fixme avoid grid overriding
        self.root.initiliaze()

    def play(self):
        return self.root.findMove()



class Node:
    def __init__(self, grid):
        self.grid = grid

    def initiliaze(self):
        start = datetime.datetime.now()
        self.__setMovesCounts()
        self.children = []
        self.__initiliazeChildren(0, self.children)

    def findMove(self):
        target = time.time() + 1
        foundNodes = 0
        while time.time() < target:
            res = self.children
            rand = selectRandoms(self.movesCounts)
            for r in rand:
                res = res[r]
            # do something
            foundNodes += 1
        # return res
        print("found nodes:", foundNodes)


    def __initiliazeChildren(self, depth, addTo):
        if depth == len(self.movesCounts) - 1:
            for i in range(self.movesCounts[depth]):
                addTo += [Node(self.grid)]

        else:
            for i in range(self.movesCounts[depth]):
                addTo += [[]]
                self.__initiliazeChildren(depth + 1, addTo[i])
                pass

    def __setMovesCounts(self):
        self.movesCounts = []
        for pacman in self.grid.pacmans:
            self.movesCounts += [len(pacman.getMoves(self.grid.maze))]





def selectRandoms(movesCounts):
    res = []
    for c in movesCounts:
        res += [random.randint(0, c - 1)]
    return res

