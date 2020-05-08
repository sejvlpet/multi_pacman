import game
import random

class Pacman:

	def __init__(self, cord):
		self.cord = cord

	def getCord(self):
		return self.cord

	def move(self, maze, ghosts):		
		cord = self.__nearestGhost(maze, ghosts)

		self.cord = self.__moveGready(cord, maze)
		return self.cord

	# private
	def __moveGready(self, cord, maze):
		moves = self.__validMoves(game.getMoves(self.cord, maze), maze)

		if len(moves) == 0:
			return self.cord # no move left, just die there

		minDistance = game.getDistance(moves[0], cord)
		finalMove = moves[0]
		for move in moves:
			dist = game.getDistance(move, cord)
			if dist > minDistance:
				minDistance = dist
				finalMove = move
		return finalMove

	# def __randomMove(self, maze):
	# 	moves = game.getMoves(self.cord, maze)

	# 	return moves[random.randint(0, len(moves) - 1)]


	def __nearestGhost(self, maze, ghosts):
		cord = ghosts[0].getCord()
		minDistance = game.getDistance(self.cord, ghosts[0].getCord())
		for ghost in ghosts:
			dist = game.getDistance(self.cord, cord) 
			if dist < minDistance:
				minDistance = dist
				cord = ghost.getCord()

		return cord

	def  __validMoves(self, moves, maze):
		i = 0
		while i < len(moves):
			if(game.isGhost(moves[i], maze) or game.isPacman(moves[i], maze)):
				del moves[i]
				i -= 1
			i += 1
		return moves