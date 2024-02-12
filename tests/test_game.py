from Dragonwood.Game import Game
from Dragonwood.Deck import Adventurer_Deck, Dragonwood_Deck
from Dragonwood.Player import Player
from Dragonwood.Dice import Dice
import Dragonwood.SharedRandom as sr
sr.set_seed(100)

dragonwood_deck = Dragonwood_Deck("./cards/creatures.csv", "./cards/enhancements.csv")
adventurer_deck = Adventurer_Deck(5,13)
dice = Dice([1, 2, 2, 3, 3, 4])
players = [Player(0.5, -0.1, dice, "Alice"),
            Player(0.5, -0.1, dice, "Bob"),
            Player(0.5, -0.1, dice, "Charles"),
            Player(0.5, -0.1, dice, "Dylan")
            ] 


game = Game(adventurer_deck, dragonwood_deck,players,dice, True)
