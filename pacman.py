import game
import grid

class Pacman:

	def __init__(self, cord):
		self.cord = cord

	def getCord(self):
		return self.cord

	def move(self, maze, ghosts):		
		cord = self.__nearestGhost(ghosts)

		self.cord = self.__moveGready(cord, maze)
		return self.cord

	# private
	def __moveGready(self, cord, maze):
		moves = self.__validMoves(self.__getMoves(maze), maze)

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

	def  __validMoves(self, moves, maze):
		i = 0
		while i < len(moves):
			if(game.isGhost(moves[i], maze) or game.isPacman(moves[i], maze)):
				del moves[i]
				i -= 1
			i += 1
		return moves

	def __getMoves(self, maze):
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

