from Dragonwood.GameConfig import GameConfig

def main():

    model_games(100)

def model_games(iterations):

    range_of_risk_level = [x/20 for x in range(-20,20,2)]
    range_of_risk_adjustement = [x/20 for x in range(-20,20,2)]

    config = {
        "adventurer_suits": 5,
        "adventurer_values": 13,
        "dice_values": [1,2,2,3,3,4],
        "number_of_players": 4,
        "number_of_iterations": iterations,
        "range_of_risk_level": range_of_risk_level,
        "range_of_risk_adjustement": range_of_risk_adjustement,
        "seed": 100,
        "creature_filepath": "./cards/creatures.csv", 
        "enhancement_filepath": "./cards/enhancements.csv"
    }

    gameconfig = GameConfig(**config)
    results = gameconfig.Run()
    results.export("./data/ev_sensitivities/")

if __name__ == "__main__":
    main()
