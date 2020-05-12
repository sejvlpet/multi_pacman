import game
import grid
import random

class Pacman:

	def __init__(self, cord):
		self.cord = cord

	def getCord(self):
		return self.cord

	def move(self, gameGrid):
		maze = gameGrid.maze
		ghosts = gameGrid.ghosts
		r = random.random()
		if r < 0.1:
			cord = self.__nearestGhost(ghosts)
			self.cord = self.__movefromGhost(cord, maze)
		elif r < 0.9:
			cord = self.__nearestPill(maze)
			self.cord = self.__greadyPill(cord, maze)
		else:
			self.cord = self.__randomMove(maze)
		return self.cord


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

		return moves[:]

	def __nearestPill(self, maze):
		neighbors = self.getMoves(maze)
		added = {}
		for neighbor in neighbors:
			row = neighbor[0]
			col = neighbor[1]
			if maze[row][col].members["pill"]:
				return neighbor
			tmp = game.getNeighbors(neighbor, maze)
			for t in tmp:
				if (t[0], t[1]) not in added:
					neighbors += [t]
					added[(t[0], t[1])] = True
		# in case where is path to pill locked by ghost or pacman, nothning can be found
		return self.cord

	def __randomMove(self, maze):
		moves = self.getMoves(maze)

		if len(moves) == 0:
			return self.cord  # no move left, just die there
		return moves[random.randint(0, len(moves) - 1)]

	def __greadyPill(self, cord, maze):
		moves = self.getMoves(maze)

		if len(moves) == 0:
			return self.cord # no move left, just die there

		minDistance = game.getDistance(moves[0], cord)
		finalMove = moves[0]
		for move in moves:
			dist = game.getDistance(move, cord)
			if dist < minDistance:
				minDistance = dist
				finalMove = move
		return finalMove

	def __movefromGhost(self, cord, maze):
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



	def __valid(self, row, col, maze):
		return not (maze[row][col] == grid.GHOST or maze[row][col] == grid.PACMAN)

