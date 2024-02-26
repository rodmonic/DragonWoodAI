import neat
import os

import multiprocessing

from numpy import average


from Dragonwood.Game import Game
from Dragonwood.Deck import Adventurer_Deck, Dragonwood_Deck
from Dragonwood.Player import Player
from Dragonwood.Dice import Dice
import Dragonwood.SharedRandom as sr

sr.set_seed()

generations = 1000
iterations = 2000

def eval_genome(genome, config):

    net = neat.nn.FeedForwardNetwork.create(genome, config)
    fitness = 0
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
        
        game.play(
            net=net,
            debug=False
        )

        # Determine the fitness score based on the outcome of the game
        fitness_of_players_that_are_robots = [x.fitness for x in players if x.is_robot]
        fitness += average(fitness_of_players_that_are_robots)

    return fitness/iterations
    



def run_neat(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-2')
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    checkpointer = neat.Checkpointer(1)
    p.add_reporter(checkpointer)
    # Run for up to 300 generations.
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = p.run(pe.evaluate, generations)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "./NEAT/config-feedforward.txt")
    run_neat(config_path)
