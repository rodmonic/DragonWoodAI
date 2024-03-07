from importlib.machinery import WindowsRegistryFinder
from typing import List
import itertools
import logging
import time
from uu import encode
import shortuuid
from Dragonwood.Deck import Adventurer_Deck, Dragonwood_Deck, Adventurer_Card
from Dragonwood.Player import Player
from Dragonwood.Card import Creature, Dragonwood_Card, Enhancement
from Dragonwood.Dice import Dice
from neat.nn import FeedForwardNetwork
from Dragonwood.SharedRandom import shared_random

logging.basicConfig(filename=f'./data/logging/{time.strftime("%Y%m%d-%H%M%S")}.log', encoding='utf-8', level=logging.DEBUG)


class Game():
    def __init__(self, adventurer_deck: Adventurer_Deck, dragonwood_deck: Dragonwood_Deck, players: List[Player], dice: Dice, shuffle_players: bool = True):
        self.adventurer_deck = adventurer_deck
        self.dragonwood_deck = dragonwood_deck
        self.dice = dice
        self.players = players if not shuffle_players else shared_random.sample(players, len(players))
        self.uuid = shortuuid.uuid()[:8]
        self.turns = 1
        self.landscape = []
        self.winner = ''
        self.initialise_game()

    def __repr__(self) -> str:
        return f'Game({len(self.players)} players)'

    def initialise_game(self):
        """Handles the initial setup for the game."""
        self.adventurer_deck.shuffle()
        self.dragonwood_deck.shuffle()
        self.initial_deal_adventurer()
        self.initial_deal_landscape()
        self.dragonwood_deck.initial_config(len(self.players))


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
            player.hand = self.adventurer_deck.deal(5)

    def initial_deal_landscape(self):
        self.landscape = self.dragonwood_deck.deal(5)

    def success(self, player: Player, decision: dict):
        dw_card = decision["card"]
        player.dragonwood_cards.append(dw_card)
        player.points += getattr(dw_card, "points", 0)

        if isinstance(dw_card, Enhancement):
            for modification in dw_card.modifications:
                setattr(player, modification, getattr(player, modification) + dw_card.modifier)


        self.landscape.remove(decision["card"])
        self.landscape.extend(self.dragonwood_deck.deal(1))
        
        player.hand = [card for card in player.hand if card not in decision["adventurers"]]
        self.adventurer_deck.discard.extend(decision["adventurers"])

    def failure(self, player:Player):
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
            if player.is_robot:
                # logging.debug(f'Turn {self.turns} {player.name} {decision["decision"]}-{player.hand}-{[str(x) for x in self.landscape]}-RELOAD')
                logging.debug(f'RELOAD |Turn {self.turns:0>2d}|{player.name}|{player.points}|{player.fitness}|{decision["decision"]}|||{self.landscape}||{player.hand}')
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
                if player.is_robot:
                    # logging.debug(f'Turn {self.turns} {player.name} {decision["decision"]}-{dice_roll + modifiers}-{decision["adventurers"]}-{[str(x) for x in self.landscape]}-{decision["card"]}-SUCCESS')
                    logging.debug(f'SUCCESS|Turn {self.turns:0>2d}|{player.name}|{player.points}|{player.fitness}|{decision["decision"]}|{dice_roll + modifiers}|{decision["card"]}|{self.landscape}|{decision["adventurers"]}|{player.hand}')
                decision_detail["outcome"] = "SUCCESS"
                self.success(player, decision)
            else:
                if player.is_robot:
                    # logging.debug(f'Turn {self.turns} {player.name} {decision["decision"]}-{dice_roll + modifiers}-{decision["adventurers"]}-{[str(x) for x in self.landscape]}-{decision["card"]}-FAILURE')
                    logging.debug(f'FAILURE|Turn {self.turns:0>2d}|{player.name}|{player.points}|{player.fitness}|{decision["decision"]}|{dice_roll + modifiers}|{decision["card"]}|{self.landscape}|{decision["adventurers"]}|{player.hand}')
                decision_detail["outcome"] = "FAILURE"
                self.failure(player)

        return decision_detail

    def get_number_of_games_enders(self) -> int:

        # check if all the game ending cards have been captured 
        remaining_DW_cards = itertools.chain(self.dragonwood_deck.cards, self.landscape)
        game_ending_cards = sum([x.game_ender for x in remaining_DW_cards if type(x) is Creature])

        return game_ending_cards

    def play(self, net: FeedForwardNetwork=None, debug: bool = False):

        if not debug:
            logging.disable()
        logging.debug('start')

        decisions = []

        while True:

            for player in self.players:

                if not player.hand:
                    decision = {"decision": "reload"}
                else:
                    attack_options = player.find_attack_options()
                    if player.is_robot:
                        decision = self.decide_by_nn(attack_options, net, player)

                    elif player.is_random:
                        decision = self.decide_by_random(attack_options)
                    else:
                        decision = player.decide_by_rules(self.landscape, self.dice.EV, attack_options)

                decisions.append(self.enact_decision(decision, player))

                if self.get_number_of_games_enders() == 0:
                    break

                if len(player.hand) > 9:
                    player.discard_card(self.adventurer_deck)
                    

            self.turns += 1

            if self.adventurer_deck.number_of_deals > 2 or self.get_number_of_games_enders() == 0:
                break

        self.winner = self.get_winner()

        for player in self.players:
            logging.debug(f"{player.name}|{player.points}|{player.fitness}")

        for robot_player in [x for x in self.players if x.is_robot]:
            if robot_player.uuid == self.winner:
                robot_player.fitness += 10.0

        return {
            "game_uuid": self.uuid,
            "winner": self.winner,
            "turns": self.turns,
            "decisions": decisions,
            "players_details": self.get_players_details()
        }

    def get_attack_option_game_state(self, attack_option: list[Adventurer_Card], dragonwood_card: Dragonwood_Card, hand: list[Adventurer_Card]) -> list[float]:

        encoded_attack_option= self.get_encoded_attack_option(attack_option, hand)
        encoded_landscape = self.get_encoded_landscape(dragonwood_card)
        player_points = [x.points/50 for x in sorted(self.players, key=lambda obj: obj.name)]
        number_of_game_enders = [self.get_number_of_games_enders()/2]

        state = list(
            itertools.chain(
                encoded_attack_option,
                encoded_landscape,
                player_points,
                number_of_game_enders
            )
            )

        return state

    def get_encoded_attack_option(self, attack_option: list[Adventurer_Card], hand: list[Adventurer_Card]) -> list[int]:

        suits = self.adventurer_deck.suits
        values = self.adventurer_deck.values
        attack_option_encoded = [0.0] * (suits * values)

        cards = list(itertools.chain(attack_option, hand))
        
        for card in cards:
            attack_option_encoded[values*card.suit + card.value] += 0.5

        return attack_option_encoded

    def get_encoded_landscape(self, dragonwood_card: Dragonwood_Card ) -> list[int]:
        landscape_encoded = [0.0] * len(self.dragonwood_deck.lookup)

        for card in set(self.landscape):
            landscape_encoded[self.dragonwood_deck.lookup[card.name]] = 0.5

        landscape_encoded[self.dragonwood_deck.lookup[dragonwood_card.name]] = 1.0

        return landscape_encoded

    def decide_by_nn(self, attack_options: list[list[Adventurer_Card]], net: FeedForwardNetwork, player: Player) -> dict:
        
        index_of_highest_score = 0
        highest_score = float('-inf')
        selected_card = 0

        for card in self.landscape:
            for index, attack_option in enumerate(attack_options):

                modifiers = getattr(player, attack_option[0] + "_modifier")
                # check if it is a "bad descision" (i.e. impossible for the AI to win that card) 
                # and skip that card
                if (len(attack_option[1])*4 + modifiers) < (getattr(card, attack_option[0])):
                    continue

                encoded_option = self.get_attack_option_game_state(attack_option[1], card, player.hand)
                option_score = net.activate(encoded_option)[0]
                if option_score > highest_score:
                    highest_score = option_score
                    index_of_highest_score = index
                    selected_card = card

        if highest_score <= 0.33:
            selected_decision = {"decision": "reload"}

        else:
            selected_decision = {
            "decision": attack_options[index_of_highest_score][0],      # strike/stomp/scream
            "card": selected_card,                                      # the card  within the landscape
            "adventurers":  attack_options[index_of_highest_score][1],  # the adventurers used
        }
        
        return selected_decision
    
    def decide_by_random(self, attack_options: list[list[Adventurer_Card]]) -> dict:

        attack_options.extend([])

        selected_option = shared_random.choice(attack_options)
        selected_card = shared_random.choice(self.landscape)

        if selected_option:
            selected_decision = {
            "decision": selected_option[0],      # strike/stomp/scream
            "card": selected_card,               # the card  within the landscape
            "adventurers":  selected_option[1],  # the adventurers used
        }
        else:
            selected_decision = {"decision": "reload"}
        
        return selected_decision

