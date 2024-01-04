import model.dragonwood as dw
import pandas as pd

def main():

    results = [["winner", 
               "player 1 name","player 1 score", "player 1 EV", "player 1 strike modifier", "player 1 stomp modifier", "player 1 scream modifier",
               "player 2 name","player 2 score", "player 2 EV", "player 2 strike modifier", "player 2 stomp modifier", "player 2 scream modifier",
               "player 3 name","player 3 score", "player 3 EV", "player 3 strike modifier", "player 3 stomp modifier", "player 3 scream modifier",
               "player 4 name","player 4 score", "player 4 EV", "player 4 strike modifier", "player 4 stomp modifier", "player 4 scream modifier"]]

    for _ in range(10):
        adventurer_deck = dw.Adventurer_Deck(5, 12)
        dragonwood_deck = dw.Dragonwood_Deck('./cards/creatures.csv', './cards/enhancements.csv')
        dice = dw.Dice([1, 2, 2, 3, 3, 4])
        players = [dw.Player(0.5, dice, "Player 1"),
                    dw.Player(0.5, dice, "Player 2")]
        game = dw.Game(adventurer_deck, dragonwood_deck, players)
        results.append(game.play())
    
    df_results = pd.DataFrame(results)

    df_results.to_csv('./results.csv')


if __name__ == "__main__":
    main()
