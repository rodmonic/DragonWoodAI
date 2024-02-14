from dataclasses import dataclass, field
from typing import Callable

from tqdm import tqdm
from more_itertools import powerset

import pandas as pd

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
    card_mask: list[list[str]] = None
    powerset_card_mask: bool = False
    shuffle_players: bool = True
    attack_selection_fuction: Callable|None = None

    def Run(self):
        decisions = []
        player_details = []
        games = []

        if not self.card_mask:
            self.card_mask = [[]]

        if self.powerset_card_mask:
            self.card_mask = powerset(self.card_mask[0])

        for i in tqdm(self.range_of_risk_level):
            for j in tqdm(self.range_of_risk_adjustement):
                for mask in self.card_mask:
                    for _ in tqdm(range(self.number_of_iterations)):
                        adventurer_deck = Adventurer_Deck(self.adventurer_suits, self.adventurer_values)
                        dragonwood_deck = Dragonwood_Deck(self.creature_filepath, self.enhancement_filepath)
                        dice = Dice(self.dice_values)

                        players=[]

                        players.append(Player(
                                i,
                                j,
                                "player 0",
                                mask
                                )
                            )

                        for k in range(1,self.number_of_players):
                            players.append(Player(
                                0,
                                0,
                                f"player {k}",
                                []
                                ))
                        
                        game = Game(adventurer_deck, dragonwood_deck, players, dice, self.shuffle_players)
                        result = game.play()
                        decisions.extend(result["decisions"])
                        player_details.extend(result["players_details"])
                        games.append({
                                "game_uuid": result["game_uuid"],
                                "winner": result["winner"],
                                "turns": result["turns"],
                                "mask": mask
                            })
                
        return Results(games, decisions, player_details)


@dataclass
class Results():
    games: list[dict]
    decisions: list[dict]
    player_details: list[dict]

    def export(self, filepath: str, include_mask: list[str] = [])-> None:

        attributes = ["games", "decisions", "player_details"]
        
        for attribute in [x for x in attributes if x not in include_mask]:
            df = pd.DataFrame.from_dict(getattr(self, attribute))
            df.to_csv(f'{filepath}/\{attribute}.csv')



