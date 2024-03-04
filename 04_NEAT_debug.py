import neat
import os
from numpy import average

from tqdm import tqdm

from Dragonwood.Game import Game
from Dragonwood.Deck import Adventurer_Deck, Dragonwood_Deck
from Dragonwood.Player import Player
from Dragonwood.Dice import Dice
import Dragonwood.SharedRandom as sr

sr.set_seed()

generations = 50
iterations = 100

def evaluate_genome(genomes, config):
    player_details = []
    for _, genome in tqdm(genomes):
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
            
            result = game.play(
                net=net,
                debug=True
            )

            player_details.extend(result["players_details"])

            # Determine the fitness score based on the outcome of the game
            list_of_players_that_are_robots = [x.fitness for x in players if x.is_robot]
            fitness += average(list_of_players_that_are_robots)

        genome.fitness = fitness/iterations
    
    # df = pd.DataFrame.from_dict(player_details)
    # df.to_csv(f'./data/NEAT/player_details.csv')


def run_neat(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-69')
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(evaluate_genome, generations)



if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "./NEAT/config-debug.txt")
    run_neat(config_path)
