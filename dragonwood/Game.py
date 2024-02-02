from typing import List
import itertools
import logging
import random
import shortuuid
from Dragonwood.Deck import Adventurer_Deck, Dragonwood_Deck
from Dragonwood.Player import Player
from Dragonwood.Card import Creature, Enhancement
from Dragonwood.Dice import Dice

logging.basicConfig(filename='dragonwood.log', encoding='utf-8', level=logging.DEBUG)

class Game():
    def __init__(self, adventurer_deck: Adventurer_Deck, dragonwood_deck: Dragonwood_Deck, players: List[Player], dice: Dice, seed: int|None = None):
        self.adventurer_deck = adventurer_deck
        self.dragonwood_deck = dragonwood_deck
        self.dice = dice
        self.players = players
        self.uuid = shortuuid.uuid()[:8]
        self.turns = 1
        self.landscape = []
        self.initial_deal_adventurer()
        self.initial_deal_landscape()
        self.winner = ''
        random.seed(seed)

    def get_players_details(self):

        players_details = []

        for player in self.players:
            player_details = player.get_player_details()
            player_details["game_uuid"] = self.uuid
            player_details["winner"] = player.uuid==self.winner
            players_details.append(player_details)

        return players_details
    

    def get_winner(self):

        max_captured_creatures = max([len(x.dragonwood_cards) for x in self.players])
        players_uuids_with_max_creatures = [player.uuid for player in self.players if len(player.dragonwood_cards) == max_captured_creatures]

        if len(players_uuids_with_max_creatures) == 1:
            point_modifier = 3
        else:
            point_modifier = 2
        
        for player in self.players:
            if player.uuid in players_uuids_with_max_creatures:
                player.points+=point_modifier

        max_points = max([x.points for x in self.players])  
        players_with_max_points = [player for player in self.players if player.points == max_points]
        sorted_players_with_max_points = sorted(players_with_max_points, key=lambda x: len(x.dragonwood_cards))

        return sorted_players_with_max_points[0].uuid


    def __repr__(self) -> str:

        return f'Game({len(self.players)} players)'

    def initial_deal_adventurer(self):

        for player in self.players:
            player.hand = []
            player.hand.extend(self.adventurer_deck.deal(5))

    def initial_deal_landscape(self):
        
        self.landscape.extend(self.dragonwood_deck.deal(5))

    def success(self, player, decision):
        dw_card = self.landscape[decision["card_index"]]
        player.dragonwood_cards.append(dw_card)

        if type(dw_card) is Creature:
            player.points += self.landscape[decision["card_index"]].points
            self.landscape.extend(self.dragonwood_deck.deal(1))
        elif type(dw_card) is Enhancement:
            for modification in dw_card.modifications:
                current_value = getattr(player, modification)
                setattr(player, modification, dw_card.modifier + current_value)

        del self.landscape[decision["card_index"]]
        player.hand = [x for x in player.hand if x not in decision["adventurers"]]
        self.adventurer_deck.discard.extend(decision["adventurers"])

    def failure(self, player):
        player.discard_card(self.adventurer_deck)

    def play(self, debug: bool = False):

        # Shuffle players
        random.shuffle(self.players)

        if not debug:
            logging.disable()
        logging.debug('start')

        decisions = []

        while True:

            for player in self.players:
                
                decision_detail = {}
                decision = player.decide(self.landscape, self.dice.EV)

                if decision["decision"] == "reload":
                    decision_detail = {
                        "game uuid": self.uuid,
                        "turn": self.turns,
                        "player uuid": player.uuid,
                        "outcome": "RELOAD",
                        "player points": player.points
                    }

                    player.hand.extend(self.adventurer_deck.deal(1))
                    logging.debug(f'Turn {self.turns} {player.name} {decision["decision"]}-{player.hand}-{[str(x) for x in self.landscape]}-RELOAD')
                else:
                    dice_roll = self.dice.roll_n_dice(len(decision["adventurers"]))
                    modifiers = getattr(player, decision["decision"] + "_modifier")

                    decision_detail = {
                            "game uuid": self.uuid,
                            "turn": self.turns,
                            "player uuid": player.uuid,
                            "selected dragonwood card": self.landscape[decision["card_index"]].name,
                            "decision": decision["decision"],
                            "dice roll": dice_roll,
                            "player points": player.points
                            }


                    if (dice_roll + modifiers) >= getattr(self.landscape[decision["card_index"]], decision["decision"]):
                        logging.debug(f'Turn {self.turns} {player.name} {decision["decision"]}-{dice_roll + modifiers}-{decision["adventurers"]}-{[str(x) for x in self.landscape]}-{self.landscape[decision["card_index"]]}-SUCCESS')
                        decision_detail["outcome"] = "SUCCESS"
                        self.success(player, decision)

                    else:
                        logging.debug(f'Turn {self.turns} {player.name} {decision["decision"]}-{dice_roll + modifiers}-{decision["adventurers"]}-{[str(x) for x in self.landscape]}-{self.landscape[decision["card_index"]]}-FAILURE')
                        decision_detail["outcome"] = "FAILURE"
                        self.failure(player)

                decisions.append(decision_detail)

                

                if len(player.hand) >9:
                    player.discard_card(self.adventurer_deck)

            self.turns += 1

            # check if all the game ending cards have been captured and if so then break while loop
            remaining_DW_cards = itertools.chain(self.dragonwood_deck.cards, self.landscape)
            game_ending_cards = sum([x.game_ender for x in remaining_DW_cards if type(x) is Creature])
            if not game_ending_cards or self.adventurer_deck.number_of_deals > 3:
                break
        
        self.winner = self.get_winner()

        return {
            "game_uuid": self.uuid,
            "winner": self.winner,
            "turns": self.turns,
            "decisions": decisions,
            "players_details": self.get_players_details()
        }
    


