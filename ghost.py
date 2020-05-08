import game
import random

class Ghost:

	def __init__(self, cord, radius):
		self.cord = cord
		self.radius = radius

	def getCord(self):
		return self.cord

	# pacmans shall be list in shape [[row, col]]
	def move(self, maze, pacmans):
		pacmanNearby, cord = self.__pacmanNearby(maze, pacmans) 
		if pacmanNearby:
			newPos = self.__moveGready(cord, maze)
		else:
			newPos = self.__randomMove(maze)

		self.cord = newPos
		return self.cord

	# private
	def __pacmanNearby(self, maze, pacmans):
		cord = [0, 0]
		nearby = False
		minDistance = len(maze) + len(maze[0]) # such distance is even more than real maximum
		for pacman in pacmans:
			dist = game.getDistance(self.cord, pacman.getCord()) 
			if dist < self.radius and dist < minDistance:
				nearby = True
				minDistance = dist
				cord = pacman.getCord()

		return nearby, cord

	def __moveGready(self, cord, maze):
		moves = game.getMoves(self.cord, maze)
		if len(moves) == 0:
			return self.cord

		minDistance = game.getDistance(moves[0], cord)
		finalMove = moves[0]
		for move in moves:
			dist = game.getDistance(move, cord)
			if dist < minDistance:
				minDistance = dist
				finalMove = move
		return finalMove

	def __randomMove(self, maze):
		moves = game.getMoves(self.cord, maze)
		if len(moves) == 0:
			return self.cord

		return moves[random.randint(0, len(moves) - 1)] 


