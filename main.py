import model.dragonwood as dw
import pandas as pd
import numpy as np
from tqdm import tqdm
import json
import csv


column_headers = ["winner", 
            "player 1 name","player 1 score", "player 1 EV", "player 1 strike modifier", "player 1 stomp modifier", "player 1 scream modifier",
            "player 2 name","player 2 score", "player 2 EV", "player 2 strike modifier", "player 2 stomp modifier", "player 2 scream modifier",
            "player 3 name","player 3 score", "player 3 EV", "player 3 strike modifier", "player 3 stomp modifier", "player 3 scream modifier",
            "player 4 name","player 4 score", "player 4 EV", "player 4 strike modifier", "player 4 stomp modifier", "player 4 scream modifier"]

def main():

    model_games(1000)
    # model_hands(100000)
    # model_dice(10000)


def model_hands(iterations: int):
        fields = ["size", "iteration", "strikes", "stomps", "screams"]
        hands = []
        adventurer_deck = dw.Adventurer_Deck(5, 12)
        dice = dw.Dice([1, 2, 2, 3, 3, 4])
        player = dw.Player(0.5, dice, "Alice")


        for i in tqdm(range(5,10)):
            for j in tqdm(range(iterations)):
                player.hand = adventurer_deck.cards[0:i]
                adventurer_deck.shuffle()
                choices = player.find_choices()
                hand = [
                    i,
                    j,
                    max([len(x) for x in choices[0]], default=0),
                    max([len(x) for x in choices[1]], default=0),
                    max([len(x) for x in choices[2]], default=0)
                ]
                hands.append(hand)

        with open('hands.csv', 'w', newline='') as f:
     
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(hands)





def model_dice(iterations: int) -> None:

    dice = dw.Dice([1, 2, 2, 3, 3, 4])
    rolls = []
    for i in tqdm(range(1,7)):
        for j in tqdm(range(iterations)):
            rolls.append(
                [
                    i,
                    j,
                    dice.roll_n_dice(i)
                ])
            
    with open('dice.csv', 'w', newline='') as f:
    
    # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(["number of dice", "iteration", "score"])
        write.writerows(rolls)



def model_games(iterations):

    results = []
        
    for i in tqdm(range(iterations)):

        adventurer_deck = dw.Adventurer_Deck(5, 12)
        dragonwood_deck = dw.Dragonwood_Deck('./cards/creatures.csv', './cards/enhancements.csv')
        dice = dw.Dice([1, 2, 2, 3, 3, 4])
        players = [dw.Player(0, dice, "Alice"),
                    dw.Player(0, dice, "Bob"),
                    dw.Player(0, dice, "Charles"),
                    dw.Player(0, dice, "Dylan")
                    ]
        game = dw.Game(adventurer_deck, dragonwood_deck, players, 5)
        game.play(False)
        report = game.report()
        result = {
            "game": i,
            "winner": report["winner"],
            "turns": report["turns"],
            "game_detail": report["game_detail"],
            "player_detail": report["player_detail"]
        }
        results.append(result)
    
    with open('result.json', 'w') as fp:
        json.dump(results, fp, indent=4)

if __name__ == "__main__":
    main()
