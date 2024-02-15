from tqdm import tqdm
from Dragonwood.GameConfig import GameConfig


def main():

    model_games()


def model_games():

    for i in tqdm(range(2, 5)):
        range_of_risk_level = [0]
        range_of_risk_adjustement = [0]

        config = {
            "adventurer_suits": 5,
            "adventurer_values": 12,
            "dice_values": [1, 2, 2, 3, 3, 4],
            "number_of_players": i,
            "shuffle_players": False,
            "number_of_iterations": 10000,
            "range_of_risk_level": range_of_risk_level,
            "range_of_risk_adjustement": range_of_risk_adjustement,
            "seed": 100,
            "creature_filepath": "./cards/creatures.csv",
            "enhancement_filepath": "./cards/enhancements.csv"
        }

        gameconfig = GameConfig(**config)
        results = gameconfig.Run()
        results.export(f"./data/number_of_players/{i}/")


if __name__ == "__main__":
    main()
