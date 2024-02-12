from Dragonwood.GameConfig import GameConfig
import Dragonwood.SharedRandom as sr

sr.set_seed(100)

def main():

    model_games()

def model_games():

    range_of_risk_level = [x/8 for x in range(-4,5,1)]
    range_of_risk_adjustement = [x/8 for x in range(-4,5,1)]

    config = {
        "adventurer_suits": 5,
        "adventurer_values": 13,
        "dice_values": [1,2,2,3,3,4],
        "number_of_players": 4,
        "number_of_iterations": 1000,
        "range_of_risk_level": range_of_risk_level,
        "range_of_risk_adjustement": range_of_risk_adjustement,
        "creature_filepath": "./cards/creatures.csv", 
        "enhancement_filepath": "./cards/enhancements.csv"
    }

    gameconfig = GameConfig(**config)
    results = gameconfig.Run()
    results.export("./data/ev_sensitivities/")

if __name__ == "__main__":
    main()
