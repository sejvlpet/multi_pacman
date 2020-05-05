import ghost
import grid
import math

def getDistance(pos1, pos2):
	return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def getMoves(pos, maze):
	moves = []
	if valid(pos[0] + 1, pos[1], maze):
		moves += [[pos[0] + 1, pos[1]]]
	if valid(pos[0] - 1, pos[1], maze):
		moves += [[pos[0] - 1, pos[1]]]
	if valid(pos[0], pos[1] + 1, maze):
		moves += [[pos[0], pos[1] + 1]]
	if valid(pos[0], pos[1] - 1, maze):
		moves += [[pos[0], pos[1] - 1]]
	return moves


def valid(row, col, maze):

	return row < len(maze) and col < len(maze[0]) and maze[row][col] != grid.WALL



def play(pacmans, ghosts, maze):
	# for pacman in pacmans:
	# 	pass

	for ghost in ghosts:
		# fixme take care of moving over pills
		pos = ghost.getCord()
		maze[pos[0]][pos[1]] = grid.EMPTY
		pos = ghost.move(maze, pacmans)
		maze[pos[0]][pos[1]] = grid.GHOST
