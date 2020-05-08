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
	return row < len(maze) and col < len(maze[0]) and row >= 0 and col >= 0 and maze[row][col] != grid.WALL and not isGhost([row, col], maze)



def play(pacmans, ghosts, maze, gameStats):
	for i in range(len(pacmans)):
		# todo change gameStats

		pos = pacmans[i].getCord()
		maze[pos[0]][pos[1]] = afterPacmamLeave()

		pos = pacmans[i].move(maze, pacmans) # todo add stats
		maze[pos[0]][pos[1]] = onPacmanMove()
		pacmans[i].cord = pos


	for i in range(len(ghosts)):
		pos = ghosts[i].getCord()

		maze[pos[0]][pos[1]] = afterGhostLeave(maze[pos[0]][pos[1]])

		pos = ghosts[i].move(maze, pacmans)
		maze[pos[0]][pos[1]] = onGhostMove(maze, pos, pacmans)
		ghosts[i].cord = pos


def afterPacmamLeave():
	return grid.EMPTY

def onPacmanMove():
	return grid.PACMAN	

def isGhost(pos, maze):
	s = maze[pos[0]][pos[1]]
	return s == grid.GHOST or s == grid.GHOST_AND_PILL or s == grid.GHOST_AND_STOP_PILL

def isPacman(pos, maze):
	s = maze[pos[0]][pos[1]]
	return s == grid.PACMAN



def afterGhostLeave(s):
	if s == grid.GHOST or s == grid.EMPTY:
		return grid.EMPTY
	if s == grid.GHOST_AND_PILL:
		return grid.PILL
	if s == grid.GHOST_AND_STOP_PILL:
		return grid.STOP_PILL
	if s == grid.PILL or s == grid.STOP_PILL or s == grid.PACMAN:
		return s 

def onGhostMove(maze, pos, pacmans):
	s = maze[pos[0]][pos[1]]
	if s == grid.EMPTY:
		return grid.GHOST
	if s == grid.PILL:
		return grid.GHOST_AND_PILL
	if s == grid.STOP_PILL:
		return grid.GHOST_AND_STOP_PILL
	if s == grid.GHOST or s == grid.GHOST_AND_PILL or s == grid.GHOST_AND_STOP_PILL:
		return s
	if s == grid.PACMAN:
		for i in range(len(pacmans)):
			if pacmans[i].getCord() == pos:
				del pacmans[i]
				break
		return grid.GHOST
