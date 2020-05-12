import grid

if __name__ == "__main__":
    myGrid = grid.Grid()
    myGrid.createGame(13, 13, 5, 5)

    myGrid.play()