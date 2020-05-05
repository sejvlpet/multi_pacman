import game
import random

class Ghost:

	def __init__(self, cord, radius):
		self.cord = cord
		self.radius = radius

	def getCord(self):
		return self.cord
		# or perhaps
		# return self.cord[0], self.cord[1]

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
			dist = game.getDistance(self.cord, pacman) 
			if dist < self.radius and dist < minDistance:
				nearby = True
				minDistance = dist
				cord = pacman

		return nearby, cord

	def __moveGready(self, cord, maze):
		moves = game.getMoves(self.cord, maze)

		minDistance = game.getDistance(moves[0], cord)
		finalMove = moves[0]
		for move in moves:
			dist = game.getDistance(move, cord)
			if dist < minDistance:
				minDistance = dist
				finalMove = move
		return finalMove

	def __randomMove(self, maze):
		# sometimes they get unlogically stuck
		moves = game.getMoves(self.cord, maze)

		return moves[random.randint(0, len(moves) - 1)] # fixme not sure if should there be -1, but I think yees


