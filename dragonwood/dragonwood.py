from typing import List
import ast
import itertools
from collections import Counter
import csv
import logging
import random
import shortuuid

logging.basicConfig(filename='dragonwood.log', encoding='utf-8', level=logging.DEBUG)


class Deck:
    def __init__(self):
        self.cards = []
        self.discard = []

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, n: int):
        cards_delt = []
        for _ in range(n):

            if not self.cards and type(self) is Adventurer_Deck:
                self.cards = self.discard
                self.discard= []
                self.shuffle()
                self.number_of_deals += 1

            if self.cards:
                cards_delt.extend(self.cards[:1])
                del self.cards[:1]
            else:
                break

        return cards_delt


class Card():
    def __init__(self, strike: int, stomp: int, scream: int, name: str) -> None:
        self.strike = strike
        self.stomp = stomp
        self.scream = scream
        self.name = name



class Creature(Card):
    def __init__(self, points: int, strike: int, stomp: int, scream: int, name: str, game_ender: bool) -> None:
        Card.__init__(self, strike, stomp, scream, name)
        self.points = points
        self.game_ender = game_ender

    def __str__(self):
        return f'C:{self.name}:{self.points}:{self.strike}:{self.stomp}:{self.scream}'

    def __repr__(self) -> str:
        return f'C:{self.name}:{self.points}:{self.strike}:{self.stomp}:{self.scream}'

class Enhancement(Card):
    def __init__(self, strike: int, stomp: int, scream: int, name: str, modifications: list[object], modifier: int, permanent: bool) -> None:
        Card.__init__(self, strike, stomp, scream, name)
        self.modifications = modifications
        self.modifier = modifier
        self.permanent = permanent

    def __str__(self):
        return f'E:{self.name}::{self.strike}:{self.stomp}:{self.scream}'

    def __repr__(self) -> str:
        return f'E:{self.name}::{self.strike}:{self.stomp}:{self.scream}'


class Dragonwood_Deck(Deck):
    def __init__(self, creatures_file_path, enchantments_file_path):
        Deck.__init__(self)
        self.import_creatures(creatures_file_path)
        self.import_enhancements(enchantments_file_path)
        self.shuffle()

    def import_creatures(self, filepath):

        with open(filepath, 'r') as csvfile:
            creatures = csv.reader(csvfile, delimiter=',')

            # skip headers
            next(csvfile)

            for creature in creatures:
                for _ in range(int(creature[5])):
                    self.cards.append(
                        Creature(
                            name=creature[0],
                            points=int(creature[1]),
                            strike=int(creature[2]),
                            stomp=int(creature[3]),
                            scream=int(creature[4]),
                            game_ender=int(creature[6])
                            )
                        )

    def import_enhancements(self, filepath):

        with open(filepath, 'r') as csvfile:
            enhancements = csv.reader(csvfile, delimiter=',')

            # skip headers
            next(csvfile)

            for enhancement in enhancements:

                self.cards.append(
                    Enhancement(
                        name=enhancement[0],
                        strike=int(enhancement[1]),
                        stomp=int(enhancement[2]),
                        scream=int(enhancement[3]),
                        modifications=ast.literal_eval(enhancement[4]),
                        modifier=int(enhancement[5]),
                        permanent=bool(enhancement[6])
                        )
                    )


class Adventurer():
    def __init__(self, suit: int, value: int) -> None:
        self.value = value
        self.suit = suit

    def __str__(self):
        return f'Adventurer({self.suit}:{self.value})'

    def __repr__(self) -> str:
        return f'Adventurer({self.suit}:{self.value})'

class Adventurer_Deck(Deck):
    def __init__(self, suits: int, values: int):
        Deck.__init__(self)
        self.generate_adventurer_deck(suits, values)
        self.suits = max(self.cards, key=lambda card: card.suit)
        self.shuffle()
        self.number_of_deals = 1

    def generate_adventurer_deck(self, suits, values):
        # adventurer cards
        self.cards = [
            Adventurer(i, j)
            for i in range(0, suits)
            for j in range(0, values)
            ]


class Player():

    def __init__(self, risk_level: float, risk_adjustment: float, dice: Dice, name: str, card_mask: list[str]):
        self.hand = []
        self.uuid = shortuuid.uuid()[:8]
        self.name = name
        self.adjusted_EV = risk_level + dice.EV
        self.risk_adjustment = risk_adjustment
        self.dice = dice
        self.points = 0
        self.dw_cards = []
        self.strike_modifier = 0
        self.stomp_modifier = 0
        self.scream_modifier = 0
        self.card_mask = card_mask

    def find_choices(self):

        # strike - finding straights
        strikes = self.find_strikes()
        # stomp - finding duplicate values
        stomps = self.find_stomps()
        # scream - finding duplicate suits
        screams = self.find_screams()

        return strikes, stomps, screams

    def find_strikes(self):
        sorted_hand = sorted(self.hand, key=lambda card: (card.value))
        max_length = 1
        end_index = 0
        count = 0

        consecutive_pairs = zip(sorted_hand, sorted_hand[1:])

        for current_card, next_card in consecutive_pairs:
            if current_card.value + 1 == next_card.value:
                count += 1
                max_length = max(max_length, count)
                end_index = sorted_hand.index(next_card)

            else:
                count = 1
        #if max_length > 1:
                
        adventurers = sorted_hand[end_index-max_length+1: end_index+1]

        # finally return all smaller lists within choices list
        return [adventurers[0:x+1] for x in range(len(adventurers))]

    def find_stomps(self):
        element_counts = Counter(x.value for x in self.hand)
        max_element, max_count = max(element_counts.items(), key=lambda x: x[1])
        adventurers = [x for x in self.hand if x.value == max_element]

        # finally return all smaller lists within choices list
        return [adventurers[0:x+1] for x in range(len(adventurers))]

    def find_screams(self):
        element_counts = Counter(x.suit for x in self.hand)
        max_element, max_count = max(element_counts.items(), key=lambda x: x[0])
        adventurers = [x for x in self.hand if x.suit == max_element]
        
        # finally return all smaller lists within choices list
        return [adventurers[0:x+1] for x in range(len(adventurers))]

    def decide(self, landscape):
        decision = {}

        if not self.hand:
            decision["decision"] = "reload"
            return decision

        choices = self.find_choices()

        names = "strike", "stomp", "scream"
        candidate_decisions = []

        for index, card in enumerate(landscape):

            # skip card if in card_mask
            for en_card in self.card_mask:
                if en_card in [x.name for x in self.dw_cards]:
                    pass

            # Extracting strike, stomp, and scream values from the current card
            values = card.strike, card.stomp, card.scream

            for i, choice in enumerate(choices):
                all_decisions = []
                for option in choice:
                    threshold = len(option) * self.adjusted_EV + getattr(self, f'{names[i]}_modifier') + self.risk_adjustment
                    if threshold > values[i]:
                        all_decisions.append([names[i], card, option, threshold - values[i], index])

                if all_decisions:
                    candidate_decisions.append(min([x for x in all_decisions if x[3] >=0], key=lambda x: x[3]))          

        if candidate_decisions:
            # Use key=lambda x: x[3] to get the element with the smallest positive difference
            logging.debug(f'CANDIDATES {self.strike_modifier}-{self.stomp_modifier}-{self.scream_modifier}-{candidate_decisions}')
            selected_option = min(candidate_decisions, key=lambda x: x[3])
            logging.debug(f'CANDIDATE {selected_option}')
            decision["decision"] = selected_option[0]  # strike/stomp/scream
            decision["card"] = selected_option[4]  # the card index within the landscape
            decision["adventurers"] = selected_option[2]  # the adventurers used

        else:
            decision["decision"] = "reload"

        return decision

    def discard_card(self, adventurer_deck):
        
        self.choices = self.find_choices()
        # find all cards in choices
        choices_cards = set([a for c in self.choices for b in c for a in b])
        potential_cards = [(i, x) for i, x in enumerate(self.hand) if x not in choices_cards]

        if potential_cards:
            logging.debug(f'DISCARD {self.hand} - {self.hand[potential_cards[0][0]]}')
            adventurer_deck.discard.append(potential_cards[0][1])
            del self.hand[potential_cards[0][0]]
        else:
            logging.debug(f'DISCARD {self.hand} - {self.hand[0]}')
            adventurer_deck.discard.append(self.hand[0])
            del self.hand[0]



class Game():
    def __init__(self, adventurer_deck: Adventurer_Deck, dragonwood_deck: Dragonwood_Deck, players: List[Player], hand_length: int):
        self.adventurer_deck = adventurer_deck
        self.dragonwood_deck = dragonwood_deck
        self.uuid = shortuuid.uuid()[:8]
        self.players = players
        self.turns = 0
        self.winner = ''
        self.landscape = []
        self.initial_deal_adventurer(hand_length)
        self.initial_deal_landscape()
        random.seed()
        self.decisions = []
        self.player_details = []

    def report(self):

        player_details = [[
            "game uuid",
            "player uuid",
            "name", 
            "points", 
            "adjusted_ev", 
            "scream_modifier", 
            "strike_modifier",
            "stomp_modifier",
            "winner"
        ]]

        for player in self.players:
            player_details.append([
                self.uuid,
                player.uuid,
                player.name, 
                player.points, 
                player.adjusted_EV, 
                player.scream_modifier, 
                player.strike_modifier,
                player.stomp_modifier,
                player.uuid==self.winner
            ])

        self.player_details = player_details

    def __repr__(self) -> str:
        return f'Game({len(self.players)} players)'

    def initial_deal_adventurer(self, hand_length):

        for player in self.players:
            player.hand = []
        
        for _ in range(hand_length):
            for player in self.players:
                player.hand.extend(self.adventurer_deck.deal(1))

    def initial_deal_landscape(self):
        for _ in range(5):
            self.landscape.extend(self.dragonwood_deck.deal(1))

    def success(self, player, decision):
        dw_card = self.landscape[decision["card"]]
        player.dw_cards.append(dw_card)

        if type(dw_card) is Creature:
            player.points += self.landscape[decision["card"]].points
        elif type(dw_card) is Enhancement:
            for modification in dw_card.modifications:
                current_value = getattr(player, modification)
                setattr(player, modification, dw_card.modifier + current_value)

        del self.landscape[decision["card"]]
        self.landscape.extend(self.dragonwood_deck.deal(1))
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
        
        decisions = [[
            "game uuid",
            "turn",
            "order",
            "player uuid",
            "selected dragonwood card",
            "decision",
            "dice roll",
            "outcome",
            "player points"]
        ]

        while True:

            self.turns += 1
            order = 1
            for player in self.players:

                decision = player.decide(self.landscape)

                if decision["decision"] == "reload":
                    decisions.append([
                        self.uuid,
                        self.turns,
                        order,
                        player.uuid,
                        "",
                        decision["decision"],
                        "",
                        "RELOAD",
                        player.points
                    ])
                    player.hand.extend(self.adventurer_deck.deal(1))
                    logging.debug(f'Turn {self.turns} {player.name} {decision["decision"]}-{player.hand}-{[str(x) for x in self.landscape]}-RELOAD')
                else:
                    dice_roll = player.dice.roll_n_dice(len(decision["adventurers"]))
                    modifiers = getattr(player, decision["decision"] + "_modifier")

                    if (dice_roll + modifiers) >= getattr(self.landscape[decision["card"]], decision["decision"]):
                        logging.debug(f'Turn {self.turns} {player.name} {decision["decision"]}-{dice_roll + modifiers}-{decision["adventurers"]}-{[str(x) for x in self.landscape]}-{self.landscape[decision["card"]]}-SUCCESS')
                        decisions.append([
                            self.uuid,
                            self.turns,
                            order,
                            player.uuid,
                            self.landscape[decision["card"]].name,
                            decision["decision"],
                            dice_roll,
                            "SUCCESS",
                            player.points
                        ])
        
                        self.success(player, decision)
                    else:
                        logging.debug(f'Turn {self.turns} {player.name} {decision["decision"]}-{dice_roll + modifiers}-{decision["adventurers"]}-{[str(x) for x in self.landscape]}-{self.landscape[decision["card"]]}-FAILURE')
                        decisions.append([
                            self.uuid,
                            self.turns,
                            order,
                            player.uuid,
                            self.landscape[decision["card"]].name,
                            decision["decision"],
                            dice_roll,
                            "FAILURE",
                            player.points
                        ])

                        self.failure(player)
                order +=1


                if len(player.hand) >9:
                    player.discard_card(self.adventurer_deck)



            # check if all the game ending cards have been captured and if so then break while loop
            remaining_DW_cards = itertools.chain(self.dragonwood_deck.cards, self.landscape)
            game_ending_cards = sum([x.game_ender for x in remaining_DW_cards if type(x) is Creature])
            if not game_ending_cards or self.adventurer_deck.number_of_deals > 3:
                break
        
        players_scores =[(player.uuid, player.points) for player in self.players]
        self.decisions = decisions
        self.winner, _ = max(players_scores, key=lambda x: x[1])


