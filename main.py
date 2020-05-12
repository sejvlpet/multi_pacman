import grid

if __name__ == "__main__":
    won = 0
    lost = 0
    games = 0
    percentageOfPillsEaten = 0
    while True:
        myGrid = grid.Grid()
        myGrid.createGame(13, 13, 5, 5)

        stats = myGrid.play()
        if stats["pillCount"] == 0:
            won += 1
        elif stats["pacmanCount"] == 0:
            lost += 1

        percentageOfPillsEaten += stats["pillsEaten"] / (stats["pillsEaten"] + stats["pillCount"])
        games += 1
        print("games played:",  games, "won: ", won, " lost: ", lost, " mean % of eaten pills: ", percentageOfPillsEaten  / games)