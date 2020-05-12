import grid

if __name__ == "__main__":
    won = 0
    lost = 0
    while True:
        myGrid = grid.Grid()
        myGrid.createGame(13, 13, 5, 5)

        stats = myGrid.play()
        if stats["pillCount"] == 0:
            won += 1
        else:
            lost += 1
        print("won: ", won, " lost: ", lost)