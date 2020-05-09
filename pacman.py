from copy import deepcopy

import game
import grid
import random
import MCTS

class Pacman:

	def __init__(self, cord):
		self.cord = cord

	def getCord(self):
		return self.cord

	def move(self, gameGrid, real):
		maze = gameGrid.maze
		ghosts = gameGrid.ghosts
		gameStats = gameGrid.gameStats
		# cord = self.__nearestGhost(ghosts)
		# self.cord = self.__moveGready(cord, maze)

		if real:
			self.cord = self.__randomMove(maze)
		else:
			pass
			# todo here will be monte carlo move
		# fixme as mcts is for all the pacmans, it cannot be here as move of only one
		# mcts = MCTS.MCTS(grid.copyGrid(gameGrid))
		# mcts.play()

		return self.cord

	# private
	def __randomMove(self, maze):
		moves = self.getMoves(maze)

		if len(moves) == 0:
			return self.cord  # no move left, just die there
		return moves[random.randint(0, len(moves) - 1)]

	def __moveGready(self, cord, maze):
		moves = self.getMoves(maze)

		if len(moves) == 0:
			return self.cord # no move left, just die there

		maxDistance = game.getDistance(moves[0], cord)
		finalMove = moves[0]
		for move in moves:
			dist = game.getDistance(move, cord)
			if dist > maxDistance:
				maxDistance = dist
				finalMove = move
		return finalMove


	def __nearestGhost(self, ghosts):
		cord = ghosts[0].getCord()
		minDistance = game.getDistance(self.cord, ghosts[0].getCord())
		for ghost in ghosts:
			dist = game.getDistance(self.cord, ghost.getCord())
			if dist < minDistance:
				minDistance = dist
				cord = ghost.getCord()

		return cord


	def getMoves(self, maze):
		moves = []
		if game.valid(self.cord[0] + 1, self.cord[1], maze) and self.__valid(self.cord[0] + 1, self.cord[1], maze):
			moves += [[self.cord[0] + 1, self.cord[1]]]

		if game.valid(self.cord[0] - 1, self.cord[1], maze) and self.__valid(self.cord[0] - 1, self.cord[1], maze):
			moves += [[self.cord[0] - 1, self.cord[1]]]

		if game.valid(self.cord[0], self.cord[1] + 1, maze) and self.__valid(self.cord[0], self.cord[1] + 1, maze):
			moves += [[self.cord[0], self.cord[1] + 1]]

		if game.valid(self.cord[0], self.cord[1] - 1, maze) and self.__valid(self.cord[0], self.cord[1] - 1, maze):
			moves += [[self.cord[0], self.cord[1] - 1]]

		return moves

	def __valid(self, row, col, maze):
		return not (maze[row][col] == grid.GHOST or maze[row][col] == grid.PACMAN)

