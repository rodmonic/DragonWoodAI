from dataclasses import dataclass, field
from typing import Callable

from tqdm import tqdm

import pandas as pd

from more_itertools import powerset

from Dragonwood.Deck import Adventurer_Deck, Dragonwood_Deck
from Dragonwood.Dice import Dice
from Dragonwood.Player import Player
from Dragonwood.Game import Game

@dataclass
class GameConfig():
    adventurer_suits: int
    adventurer_values: int
    dice_values: list[int]
    number_of_players: int
    number_of_iterations: int
    range_of_risk_level: list[float]
    range_of_risk_adjustement: list[float]            
    creature_filepath: str
    enhancement_filepath: str
    seed: int|None = None
    card_mask: list[str] = field(default_factory=list)
    superset_card_mask: bool = False
    shuffle_players: bool = True
    attack_selection_fuction: Callable|None = None

    def Run(self):
        decisions = []
        player_details = []
        games = []

        for i in tqdm(self.range_of_risk_level):
            for j in tqdm(self.range_of_risk_adjustement):
                for _ in tqdm(range(self.number_of_iterations)):
                    adventurer_deck = Adventurer_Deck(self.adventurer_suits, self.adventurer_values, self.seed)
                    dragonwood_deck = Dragonwood_Deck(self.creature_filepath, self.enhancement_filepath, self.seed)
                    dice = Dice(self.dice_values,self.seed)

                    players=[]
                    for k in range(self.number_of_players):
                        players.append(Player(
                            i,
                            j,
                            f"player{k}",
                            self.card_mask
                            ))
                    
                    game = Game(adventurer_deck, dragonwood_deck, players, dice, self.seed)
                    result = game.play()
                    decisions.extend(result["decisions"])
                    player_details.extend(result["players_details"])
                    games.append({
                            "game_uuid": result["game_uuid"],
                            "winner": result["winner"],
                            "turns": result["turns"]
                        })
                
        return Results(games, decisions, player_details)


@dataclass
class Results():
    games: list[dict]
    decisions: list[dict]
    player_details: list[dict]

    def export(self, filepath: str)-> None:
        
        attributes = ["games", "decisions", "player_details"]
        
        for attribute in attributes:
            df = pd.DataFrame.from_dict(getattr(self, attribute))
            df.to_csv(f'{filepath}/\{attribute}.csv')



