import _pickle as cPickle
import pygame
import random
import game
import ghost
import pacman

EMPTY = 0
PILL = 1
STOP_PILL = 2
WALL = 3
GHOST = 4
PACMAN = 5
GHOST_AND_PILL = 6
GHOST_AND_STOP_PILL = 7

"""
    Holds information about game grid and provides GUI
"""
class Grid:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    GREY = (220, 220, 220)
    BLUE = (30, 144, 255)
    YELLOW = (255, 238, 0)

    WIDTH = 20
    HEIGHT = 20
    MARGIN = 1

    def __del__(self):
        if self.real:
            pygame.quit()

    """
        from given params setups itself for a game
    """
    def createGame(self, colCount, rowCount, pacmansCount, ghostsCount):
        pygame.init()

        self.real = True
        windowSize = [rowCount * (self.HEIGHT + self.MARGIN),
                      colCount * (self.WIDTH + self.MARGIN)]
        self.screen = pygame.display.set_mode(windowSize)
        self.clock = pygame.time.Clock()

        self.colCount = colCount
        self.rowCount = rowCount

        self.__generateMaze(colCount, rowCount)
        pCords, gCords = self.__placeAgents(pacmansCount, ghostsCount)

        self.pacmans = self.__setPacmans(pCords)
        self.ghosts = self.__setGhosts(gCords)

        self.__setGameStats()

    """
        plays previously setuped game
    """
    def play(self):
        step = 0
        over = False
        round = 0
        while not over and round < 300:
            over = game.play(self, True)
            step += 1

            self.__draw()
            self.clock.tick(60)
            pygame.display.flip()
            round += 1
        return self.gameStats

    # private
    """
        sets default game stats dict
    """
    def __setGameStats(self):
        self.gameStats = {
            "pillCount": self.pillCount,
            "pacmanCount": len(self.pacmans),
            "pillsEaten": 0,
            "pacmansEaten": 0,
            "round": 1,
            "wins": 0,
            "looses": 0,
            "firstEatenAt": 0
        }
    """
        randomly places given count of agents and saves their positions
    """
    def __placeAgents(self, pacmanCount, ghostCount):
        pacmans = []
        ghosts = []

        while pacmanCount > 0:
            row, col = self.__getRowCol()
            if self.maze[row][col] == EMPTY:
                self.maze[row][col].place("pacman")
                pacmans += [[row, col]]
                pacmanCount -= 1

        while ghostCount > 0:
            row, col = self.__getRowCol()
            if self.maze[row][col] == EMPTY:
                self.maze[row][col].placeGhost()
                ghosts += [[row, col]]
                ghostCount -= 1

        return pacmans, ghosts

    """
        setups ghost with their cords
    """
    def __setGhosts(self, gCords):
        ghosts = []
        maxLength = len(self.maze) + len(self.maze[0])
        for cord in gCords:
            ghosts += [ghost.Ghost(cord, random.randint(int(maxLength / 6), int(maxLength / 4)))]

        return ghosts
    """
        setups pacmans with their cords
    """
    def __setPacmans(self, pCords):
        pacmans = []
        for cord in pCords:
            pacmans += [pacman.Pacman(cord)]

        return pacmans
    """
        returns random cords as row and col
    """
    def __getRowCol(self):
        row = random.randint(0, len(self.maze) - 1)
        col = random.randint(0, len(self.maze[0]) - 1)
        return row, col

    """
        GUI
    """
    def __draw(self):
        self.screen.fill(self.GREY)
        rowIterator = 0
        for row in self.maze:
            colIterator = 0
            for cell in row:
                # default color is white
                if cell == EMPTY:
                    color = self.WHITE
                elif cell == WALL:
                    color = self.BLACK
                elif cell == PILL:
                    color = self.GREEN
                elif cell == STOP_PILL:
                    color = self.BLUE
                elif cell == PACMAN:
                    color = self.YELLOW
                elif (cell == GHOST or cell == GHOST_AND_PILL
                      or cell == GHOST_AND_STOP_PILL):
                    color = self.RED

                pygame.draw.rect(self.screen,
                                 color,
                                 [(self.MARGIN + self.WIDTH) * colIterator + self.MARGIN,
                                  (self.MARGIN + self.HEIGHT) * rowIterator + self.MARGIN,
                                  self.WIDTH,
                                  self.HEIGHT])
                colIterator += 1
            rowIterator += 1
    """
        add wall on given position
    """
    def __addWalls(self, length, row, col):
        for i in range(length):
            self.maze[row + i][col].place("wall")
    """
        create walls into our grid
    """
    def __createWalls(self):
        rowCount = len(self.maze)
        collCount = len(self.maze[0])
        colIterator = 1
        skip = False
        while colIterator < collCount - 1:
            rowIterator = 1
            while rowIterator < rowCount - 1:
                if (random.random() > 0.05):
                    length = random.randint(1, int((rowCount - rowIterator) / 2))
                    self.__addWalls(length, rowIterator, colIterator)
                    rowIterator += length
                    skip = True
                rowIterator += 1
            if skip:
                colIterator += 1
                skip = False
            colIterator += 1
    """
        adds pills into grid
    """
    def __addPills(self):
        pillCount = 0
        for row in self.maze:
            for collIterator in range(len(row)):
                if row[collIterator] == EMPTY and random.random() > 0.7:
                    row[collIterator].place("pill")
                    pillCount += 1

        return pillCount
    """
        generates maze
    """
    def __generateMaze(self, rowCount, collCount):
        # start with emty maze
        self.maze = [[Cell() for i in range(collCount)] for j in range(rowCount)]

        self.__createWalls()
        self.pillCount = self.__addPills()

"""
    creates deep copy of entire grid object
"""
def copyGrid(other):
    new = Grid()
    new.real = False

    new.colCount = other.colCount
    new.rowCount = other.rowCount

    new.pacmans = cPickle.loads(cPickle.dumps(other.pacmans, -1))
    new.ghosts = cPickle.loads(cPickle.dumps(other.ghosts, -1))

    new.maze = cPickle.loads(cPickle.dumps(other.maze, -1))
    new.gameStats = cPickle.loads(cPickle.dumps(other.gameStats, -1))

    return new

"""
    class having informations and methods for better work with grid
"""
class Cell:
    # default memebers
    def __init__(self):
        self.members = {
            "pacman": False,
            "pill": False,
            "stopPill": False,
            "wall": False,
            "ghostCount": 0
        }

    def __eq__(self, other):
        return self.getStatus() == other

    def placeGhost(self, pacmans=[], pos=[], gameStats={}):
        self.members["ghostCount"] += 1

        if self.members["pacman"]:
            self.remove("pacman")
            gameStats["pacmanCount"] -= 1
            gameStats["pacmansEaten"] += 1
            for i in range(len(pacmans)):
                if pacmans[i].getCord() == pos:
                    del pacmans[i]
                    break

    def removeGhost(self):
        self.members["ghostCount"] -= 1

    def place(self, member, gameStats={}):
        self.members[member] = True

        if member == "pacman" and self.members["pill"]:
            gameStats["pillCount"] -= 1
            gameStats["pillsEaten"] += 1
            self.remove("pill")

    def remove(self, member):
        self.members[member] = False

    def getStatus(self):
        if self.members["wall"]:
            return WALL
        if self.members["ghostCount"] > 0:
            return GHOST
        if self.members["pacman"]:
            return PACMAN
        if self.members["pill"]:
            return PILL
        if self.members["stopPill"]:
            return STOP_PILL
        return EMPTY
