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
	return row < len(maze) and col < len(maze[0]) and row >= 0 and col >= 0 and maze[row][col] != grid.WALL



def play(pacmans, ghosts, maze):
	# for pacman in pacmans:
	# 	pass

	for ghost in ghosts:
		# fixme take care of moving over pills
		pos = ghost.getCord()

		maze[pos[0]][pos[1]] = afterGhostLeave(maze[pos[0]][pos[1]])

		pos = ghost.move(maze, pacmans)
		maze[pos[0]][pos[1]] = onGhostMove(maze[pos[0]][pos[1]])


def afterGhostLeave(s):
	if s == grid.GHOST or s == grid.EMPTY:
		return grid.EMPTY
	if s == grid.GHOST_AND_PILL:
		return grid.PILL
	if s == grid.GHOST_AND_STOP_PILL:
		return grid.STOP_PILL
	if s == grid.PILL or s == grid.STOP_PILL or s == grid.PACMAN:
		return s 

def onGhostMove(s):
	if s == grid.EMPTY:
		return grid.GHOST
	if s == grid.PILL:
		return grid.GHOST_AND_PILL
	if s == grid.STOP_PILL:
		return grid.GHOST_AND_STOP_PILL
	if s == grid.GHOST or s == grid.GHOST_AND_PILL or s == grid.GHOST_AND_STOP_PILL:
		return s
	if s == grid.PACMAN:
		# todo delete pacman
		return grid.GHOST
