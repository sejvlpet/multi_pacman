import pygame

# Those constants shall be in main
EMPTY = 0
PILL = 1
STOP_PILL = 2
WALL = 3
GHOST = 4
PACMAN = 5
GHOST_AND_PILL = 6
GHOST_AND_STOP_PILL = 7


class Grid(object):
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	GREEN = (0, 255, 0)
	RED = (255, 0, 0)
	GREY = (220, 220, 220)
	BLUE = (30, 144, 255)

	WIDTH = 25
	HEIGHT = 25
 
	MARGIN = 1

	def __init__(self, maze):
		pygame.init()
		windowSize = [len(maze[0]) * (self.HEIGHT + self.MARGIN),
						   len(maze) * (self.WIDTH + self.MARGIN)]
		self.screen = pygame.display.set_mode(windowSize)
		self.clock = pygame.time.Clock()
		
	def draw(self, maze):
		while True:
			self.screen.fill(self.GREY)
			rowIterator = 0
			for row in maze:
				colIterator = 0
				for cell in row:
					if cell == EMPTY:
						color = self.WHITE
					elif cell == WALL:
						color = self.BLACK
					elif cell == PILL:
						color = self.GREEN
					elif cell == STOP_PILL:
						color = self.BLUE
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
			self.clock.tick(60)
			pygame.display.flip()

	def quit():
		pygame.quit()