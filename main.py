from tqdm import tqdm
import csv
from more_itertools import powerset

from Dragonwood.GameConfig import GameConfig


def main():

    model_games(1000)
    # model_hands(100000)
    # model_dice(10000)


# def model_hands(iterations: int):
#         fields = ["size", "iteration", "strikes", "stomps", "screams"]
#         hands = []
#         adventurer_deck = dw.Adventurer_Deck(5, 12)
#         dice = dw.Dice([1, 2, 2, 3, 3, 4])
#         player = dw.Player(0.5,0.5, dice, "Alice")

#         for i in tqdm(range(5,10)):
#             for j in tqdm(range(iterations)):
#                 player.hand = adventurer_deck.cards[0:i]
#                 adventurer_deck.shuffle()
#                 choices = player.find_choices()
#                 hand = [
#                     i,
#                     j,
#                     max([len(x) for x in choices[0]], default=0),
#                     max([len(x) for x in choices[1]], default=0),
#                     max([len(x) for x in choices[2]], default=0)
#                 ]
#                 hands.append(hand)

#         with open('hands.csv', 'w', newline='') as f:
     
#             write = csv.writer(f)
#             write.writerow(fields)
#             write.writerows(hands)





# def model_dice(iterations: int) -> None:

#     dice = dw.Dice([1, 2, 2, 3, 3, 4])
#     rolls = []
#     for i in tqdm(range(1,7)):
#         for j in tqdm(range(iterations)):
#             rolls.append(
#                 [
#                     i,
#                     j,
#                     dice.roll_n_dice(i)
#                 ])
            
#     with open('dice.csv', 'w', newline='') as f:
    
#     # using csv.writer method from CSV package
#         write = csv.writer(f)
#         write.writerow(["number of dice", "iteration", "score"])
#         write.writerows(rolls)



def model_games(iterations):

    config = {
        "adventurer_suits": 5,
        "adventurer_values": 13,
        "dice_values": [1,2,2,3,3,4],
        "number_of_players": 4,
        "number_of_iterations": iterations,
        "range_of_risk_level": [0.5],
        "range_of_risk_adjustement": [0.5],
        "seed": 100,
        "creature_filepath": "./cards/creatures.csv", 
        "enhancement_filepath": "./cards/enhancements.csv"
    }

    gameconfig = GameConfig(**config)
    results = gameconfig.Run()
    results.export("./")

if __name__ == "__main__":
    main()
