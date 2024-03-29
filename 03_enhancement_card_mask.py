
from Dragonwood.GameConfig import GameConfig
from Dragonwood.SharedRandom import set_seed

set_seed()


def main():

    model_games()


def model_games():

    range_of_risk_level = [0]
    range_of_risk_adjustement = [0]

    config = {
        "adventurer_suits": 5,
        "adventurer_values": 12,
        "dice_values": [1, 2, 2, 3, 3, 4],
        "number_of_players": 4,
        "card_mask": [["Bucket of Spinach", "Ghost Disguise", "Cloak of Darkness", "Magical Unicorn", "Silver Sword"]],
        "powerset_card_mask": True,
        "shuffle_players": True,
        "number_of_iterations": 10000,
        "range_of_risk_level": range_of_risk_level,
        "range_of_risk_adjustement": range_of_risk_adjustement,
        "creature_filepath": "./cards/creatures.csv",
        "enhancement_filepath": "./cards/enhancements.csv"
    }

    gameconfig = GameConfig(**config)
    results = gameconfig.Run()
    results.export("./data/enhancement_card_mask/", ["decisions"])


if __name__ == "__main__":
    main()
