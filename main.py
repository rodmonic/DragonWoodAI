import model.dragonwood as dw


adventurer_deck = dw.Adventurer_Deck(5, 12)
dragonwood_deck = dw.Dragonwood_Deck('./cards/creatures.csv', './cards/enhancements.csv')
dice = dw.Dice([1, 2, 2, 3, 3, 4])
players = [dw.Player(1.5, dice, "Player 1"),
           dw.Player(0.5, dice, "Player 2")]


game = dw.Game(adventurer_deck, dragonwood_deck, players)


def main():

    game.play()


if __name__ == "__main__":
    main()
