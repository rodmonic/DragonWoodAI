from typing import List
import itertools
import logging
import shortuuid
from Dragonwood.Deck import Adventurer_Deck, Dragonwood_Deck
from Dragonwood.Player import Player
from Dragonwood.Card import Creature, Enhancement
from Dragonwood.Dice import Dice
from Dragonwood.SharedRandom import shared_random

logging.basicConfig(filename='dragonwood.log', encoding='utf-8', level=logging.DEBUG)


class Game():
    def __init__(self, adventurer_deck: Adventurer_Deck, dragonwood_deck: Dragonwood_Deck, players: List[Player], dice: Dice, shuffle_players: bool = True):
        self.adventurer_deck = adventurer_deck
        self.dragonwood_deck = dragonwood_deck
        self.dice = dice
        self.players = players
        self.uuid = shortuuid.uuid()[:8]
        self.turns = 1
        self.landscape = []
        self.initial_deal_adventurer()
        self.initial_deal_landscape()
        self.dragonwood_deck.initial_config(len(self.players))
        self.winner = ''
        self.shuffle_players = shuffle_players

    def __repr__(self) -> str:

        return f'Game({len(self.players)} players)'

    def get_players_details(self):

        players_details = []

        for player in self.players:
            player_details = player.get_player_details()
            player_details["game_uuid"] = self.uuid
            player_details["winner"] = player.uuid == self.winner

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
                player.points += point_modifier

        max_points = max([x.points for x in self.players])
        players_with_max_points = [player for player in self.players if player.points == max_points]
        sorted_players_with_max_points = sorted(players_with_max_points, key=lambda x: len(x.dragonwood_cards), reverse=True)

        return sorted_players_with_max_points[0].uuid

    def initial_deal_adventurer(self):

        for player in self.players:
            player.hand = []
            player.hand.extend(self.adventurer_deck.deal(5))

    def initial_deal_landscape(self):

        self.landscape.extend(self.dragonwood_deck.deal(5))

    def success(self, player, decision):
        dw_card = decision["card"]
        player.dragonwood_cards.append(dw_card)

        if type(dw_card) is Creature:
            player.points += decision["card"].points
            self.landscape.extend(self.dragonwood_deck.deal(1))
        elif type(dw_card) is Enhancement:
            for modification in dw_card.modifications:
                current_value = getattr(player, modification)
                setattr(player, modification, dw_card.modifier + current_value)

        self.landscape.remove(decision["card"])

        player.hand = [x for x in player.hand if x not in decision["adventurers"]]
        self.adventurer_deck.discard.extend(decision["adventurers"])

    def failure(self, player):
        player.discard_card(self.adventurer_deck)

    def enact_decision(self, decision: dict, player: Player) -> None:

        decision_detail = {}

        if decision["decision"] == "reload":
            decision_detail = {
                "game_uuid": self.uuid,
                "turn": self.turns,
                "player_uuid": player.uuid,
                "outcome": "RELOAD",
                "player_points": player.points
            }

            player.hand.extend(self.adventurer_deck.deal(1))
            logging.debug(f'Turn {self.turns} {player.name} {decision["decision"]}-{player.hand}-{[str(x) for x in self.landscape]}-RELOAD')
        else:
            dice_roll = self.dice.roll_n_dice(len(decision["adventurers"]))
            modifiers = getattr(player, decision["decision"] + "_modifier")

            decision_detail = {
                    "game_uuid": self.uuid,
                    "turn": self.turns,
                    "player_uuid": player.uuid,
                    "selected dragonwood card": decision["card"].name,
                    "decision": decision["decision"],
                    "dice_roll": dice_roll,
                    "player_points": player.points
                    }

            if (dice_roll + modifiers) >= getattr(decision["card"], decision["decision"]):
                logging.debug(f'Turn {self.turns} {player.name} {decision["decision"]}-{dice_roll + modifiers}-{decision["adventurers"]}-{[str(x) for x in self.landscape]}-{decision["card"]}-SUCCESS')
                decision_detail["outcome"] = "SUCCESS"
                self.success(player, decision)

            else:
                logging.debug(f'Turn {self.turns} {player.name} {decision["decision"]}-{dice_roll + modifiers}-{decision["adventurers"]}-{[str(x) for x in self.landscape]}-{decision["card"]}-FAILURE')
                decision_detail["outcome"] = "FAILURE"
                self.failure(player)

        return decision_detail

    def have_all_game_enders_been_captured(self) -> bool:

        # check if all the game ending cards have been captured and if so then break while loop
        remaining_DW_cards = itertools.chain(self.dragonwood_deck.cards, self.landscape)
        game_ending_cards = sum([x.game_ender for x in remaining_DW_cards if type(x) is Creature])

        return game_ending_cards == 0

    def play(self, debug: bool = False):

        # Shuffle players
        if self.shuffle_players:
            shared_random.shuffle(self.players)

        if not debug:
            logging.disable()
        logging.debug('start')

        decisions = []

        while True:

            for player in self.players:

                decision = player.decide(self.landscape, self.dice.EV)
                decisions.append(self.enact_decision(decision, player))
                if self.have_all_game_enders_been_captured:
                    break

                if len(player.hand) > 9:
                    player.discard_card(self.adventurer_deck)

            self.turns += 1

            if self.adventurer_deck.number_of_deals > 2:
                break

        self.winner = self.get_winner()

        return {
            "game_uuid": self.uuid,
            "winner": self.winner,
            "turns": self.turns,
            "decisions": decisions,
            "players_details": self.get_players_details()
        }
