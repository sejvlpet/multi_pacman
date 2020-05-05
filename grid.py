import pygame
import game
import random

# Those constants shall be in main
EMPTY = 0
PILL = 1
STOP_PILL = 2
WALL = 3
GHOST = 4
PACMAN = 5
GHOST_AND_PILL = 6
GHOST_AND_STOP_PILL = 7


# handles grid generating, places pacmans and ghosts and has public self.play method, which draws and from game.getMove
# keeps grid uptdated with all the next moves
class Grid(object):
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	GREEN = (0, 255, 0)
	RED = (255, 0, 0)
	GREY = (220, 220, 220)
	BLUE = (30, 144, 255)
	YELLOW = (255, 238, 0)

	WIDTH = 25
	HEIGHT = 25
 
	MARGIN = 1

	def __init__(self, colCount, rowCount):
		pygame.init()

		windowSize = [rowCount * (self.HEIGHT + self.MARGIN),
						   colCount * (self.WIDTH + self.MARGIN)]
		self.screen = pygame.display.set_mode(windowSize)
		self.clock = pygame.time.Clock()

		# generates maze with walls and pills 
		self.maze, self.pillsCount = self.__generateMaze(colCount, rowCount)
		
	def play(self):
		while True:
			self.placeAgents(5, 10)
			self.__draw()

			self.clock.tick(2)
			pygame.display.flip()


	def placeAgents(self, pacmanCount, ghostCount):
		pacmans = [] 
		ghosts = []

		while pacmanCount > 0:
			row, col = self.__getRowCol() 
			if self.maze[row][col] == EMPTY:
				self.maze[row][col] = PACMAN
				pacmans += [[row, col]]
				pacmanCount -= 1

		while ghostCount > 0:
			row, col = self.__getRowCol() 
			if self.maze[row][col] == EMPTY:
				self.maze[row][col] = GHOST
				ghosts += [[row, col]]
				ghostCount -= 1

		return pacmans, ghosts

	def __getRowCol(self):
		row = random.randint(0, len(self.maze) - 1)
		col = random.randint(0, len(self.maze[0]) - 1)
		return row, col


	def __draw(self):
		self.screen.fill(self.GREY)
		rowIterator = 0
		for row in self.maze:
			colIterator = 0
			for cell in row:
				# default color is white
				color = self.WHITE
				if cell == WALL:
					color = self.BLACK
				elif cell == PILL:
					color = self.GREEN
				elif cell == STOP_PILL:
					color = self.BLUE
				elif cell == PACMAN:
					color = self.YELLOW
				elif (cell == GHOST or cell == GHOST_AND_STOP_PILL 
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


	def __del__(self):
		pygame.quit()


	def __printMaze(self, maze):
 		for line in maze:
 			print(line)

	def __addWalls(self, maze, length, row, col):
	    for i in range(length):
	        maze[row + i][col] = WALL


	def __createWalls(self, maze):
	    rowCount = len(maze)
	    collCount = len(maze[0])
	    colIterator = 1
	    skip = False
	    while colIterator < collCount - 1:
	        rowIterator = 1
	        while rowIterator < rowCount - 1:
	            if(random.random() > 0.33):
	                length = random.randint(0, int  ((rowCount - rowIterator) / 4))
	                self.__addWalls(maze, length, rowIterator, colIterator)
	                rowIterator += length
	                skip = True
	            rowIterator += 1
	        if skip:
	            colIterator += 1
	            skip = False
	        colIterator += 1


	def __addPills(self, maze):
	    pillsCount = 0
	    for row in maze:
	        for collIterator in range(len(row)):
	            if row[collIterator] == EMPTY and random.random() > 0.7:
	                row[collIterator] = PILL
	                pillsCount += 1

	    return pillsCount


	def __addStopPill(self, maze):
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

	def __generateMaze(self, rowCount, collCount):
	    # start with emty maze
	    maze = [[ 0 for i in range(collCount)] for i in range(rowCount)]
	    
	    self.__createWalls(maze)
	    pillsCount = self.__addPills(maze)
	    pillsCount -= self.__addStopPill(maze)

	    self.__printMaze(maze)

	    return maze, pillsCount


myGrid = Grid(30, 60)
# randomly places ghost and pacmans
myGrid.placeAgents(5, 10)
myGrid.play()