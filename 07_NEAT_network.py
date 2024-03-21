import neat
import os
import pickle
import visualise


def get_network(config_file, winner_pickle):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    file = open(winner_pickle,'rb')
    winner = pickle.load(file)
    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
    visualise.draw_net(config, winner, prune_unused=True)

    
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "./NEAT/config-feedforward.txt")
    winner_pickle = os.path.join(local_dir, "winner-feedforward")
    get_network(config_path, winner_pickle)
