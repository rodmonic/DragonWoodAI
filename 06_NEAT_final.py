import neat
import os
from numpy import average

import pickle

import pandas as pd

from Dragonwood.Game import Game
from Dragonwood.Deck import Adventurer_Deck, Dragonwood_Deck
from Dragonwood.Player import Player
from Dragonwood.Dice import Dice
import Dragonwood.SharedRandom as sr

sr.set_seed()

iterations = 10000

def run_genome(net):
    player_details = []

    for _ in range(iterations):
        dragonwood_deck = Dragonwood_Deck("./cards/creatures.csv", "./cards/enhancements.csv")
        adventurer_deck = Adventurer_Deck(5, 12)
        dice = Dice([1, 2, 2, 3, 3, 4])
        players = [
            Player(0, 0, "Alice", [], True),
            Player(0, 0, "Bob", []),
            Player(0, 0, "Charles", []),
            Player(0, 0, "Dylan", [])
        ]

        game = Game(
            adventurer_deck=adventurer_deck,
            dragonwood_deck=dragonwood_deck,
            players=players,
            dice=dice
        )  # Initialize your game with the starting state
        
        result = game.play(
            net=net,
            debug=True
        )

        player_details.extend(result["players_details"])

    
    df = pd.DataFrame.from_dict(player_details)
    df.to_csv(f'./data/NEAT/player_details.csv')


def run_neat(config_file, winner_pickle):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    file = open(winner_pickle,'rb')
    winner = pickle.load(file)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    run_genome(winner_net)

    
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "./NEAT/config-feedforward.txt")
    winner_pickle = os.path.join(local_dir, "winner-feedforward")
    run_neat(config_path, winner_pickle)
