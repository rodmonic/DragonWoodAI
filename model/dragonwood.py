from typing import List
import ast
import itertools
from collections import Counter
import csv
import logging
logging.basicConfig(filename='dragonwood.log', encoding='utf-8', level=logging.DEBUG, )
import random



class Dice():

    def __init__(self, values: list):
        self.values = values
        self.EV = 0
        self.caculate_EV()

    def caculate_EV(self):
        self.EV = sum(self.values)/len(self.values)

    def roll_n_dice(self, n):
        total = 0
        for _ in range(n):
            total += random.choice(self.values)
        return total


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
                self.discard = []
                self.shuffle()

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
    def __init__(self, points: int, strike: int, stomp: int, scream: int, name: str) -> None:
        Card.__init__(self, strike, stomp, scream, name)
        self.points = points

    def __repr__(self):
        return f'C:{self.name}:{self.points}({self.strike},{self.stomp},{self.scream})'


class Enhancement(Card):
    def __init__(self, strike: int, stomp: int, scream: int, name: str, modifications: list[object], modifier: int, permanent: bool) -> None:
        Card.__init__(self, strike, stomp, scream, name)
        self.modifications = modifications
        self.modifier = modifier
        self.permanent = permanent

    def __repr__(self):
        return f'E:{self.name}({self.strike},{self.stomp},{self.scream})'


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
                            scream=int(creature[4])
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

    def __repr__(self):
        return f'Adventurer({self.suit}:{self.value})'


class Adventurer_Deck(Deck):
    def __init__(self, suits: int, values: int):
        Deck.__init__(self)
        self.generate_adventurer_deck(suits, values)
        self.suits = max(self.cards, key=lambda card: card.suit)
        self.shuffle()

    def generate_adventurer_deck(self, suits, values):
        # adverenturer cards
        self.cards = [
            Adventurer(i, j)
            for i in range(0, suits)
            for j in range(0, values)
            ]
        # # lucky ladybird cards
        # for _ in range(0,4):
        #     self.cards.append(Adventurer(0,0))


class Player():

    def __init__(self, risk_level: float, dice: Dice, name: str):
        self.hand = []
        self.choices = []
        self.name = name
        self.adjusted_EV = risk_level + dice.EV
        self.dice = dice
        self.points = 0
        self.dw_cards = []
        self.strike_modifier = 0
        self.stomp_modifier = 0
        self.scream_modifier = 0

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

        self.choices = self.find_choices()

        options = []

        for index, card in enumerate(landscape):
            # Extracting strike, stomp, and scream values from the current card
            values = card.strike, card.stomp, card.scream
            names = "strike", "stomp", "scream"

            for i, choice in enumerate(self.choices):
                pre_options = []
                for option in choice:
                    threshold = len(option) * self.adjusted_EV + getattr(self, f'{names[i]}_modifier')
                    if threshold > values[i]:
                        pre_options.append([names[i], card, option, threshold - values[i], index])

                if pre_options:
                    options.append(min([x for x in pre_options if x[3] >=0], key=lambda x: x[3]))          

        if options:
            # Use key=lambda x: x[3] to get the element with the smallest positive difference
            max_element = max(options, key=lambda x: x[3])
            decision["decision"] = max_element[0]  # strike/stomp/scream
            decision["card"] = max_element[4]  # the card index within the landscape
            decision["adventurers"] = max_element[2]  # the adventurers used

        else:
            decision["decision"] = "reload"

        return decision

    def discard_card(self, adventurer_deck):

        adventurer_deck.discard.append(self.hand[0])
        del self.hand[0]


class Game():
    def __init__(self, adventurer_deck: Adventurer_Deck, dragonwood_deck: Dragonwood_Deck, players: List[Player]):
        self.adventurer_deck = adventurer_deck
        self.dragonwood_deck = dragonwood_deck
        self.players = players
        self.turns = 0
        self.winner = ''
        self.landscape = []
        self.initial_deal_adventurer()
        self.initial_deal_landscape()
        random.seed()

    def report(self):
        scores = [self.winner]
        for player in self.players:
            scores.extend([
                player.name, 
                player.points, 
                player.adjusted_EV, 
                player.scream_modifier, 
                player.strike_modifier,
                player.stomp_modifier
                ])
        return scores

    def __repr__(self) -> str:
        return f'Game({len(self.players)} players)'

    def initial_deal_adventurer(self):
        for _ in range(5):
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

    def failure(self, player, decision):
        player.discard_card(self.adventurer_deck)

    def play(self, seed: int=None):
        
        logging.debug('start')

        while self.landscape:
            self.turns += 1
            for player in self.players:
                decision = player.decide(self.landscape)

                if decision["decision"] == "reload":
                    player.hand.extend(self.adventurer_deck.deal(1))
                else:
                    dice_roll = player.dice.roll_n_dice(len(decision["adventurers"]))
                    modifiers = getattr(player, decision["decision"] + "_modifier")

                    if (dice_roll + modifiers) >= getattr(self.landscape[decision["card"]], decision["decision"]):
                        logging.debug(f'Turn {self.turns} {player.name} {decision["decision"]}-{dice_roll}-{decision["adventurers"]}-{self.landscape[decision["card"]]}-SUCCESS')
                        self.success(player, decision)
                    else:
                        logging.debug(f'Turn {self.turns} {player.name} {decision["decision"]}-{dice_roll}-{decision["adventurers"]}-{self.landscape[decision["card"]]}-FAILURE')
                        self.failure(player, decision)
        
        players_scores =[(player.name, player.points) for player in self.players]
        
        self.winner, _ = max(players_scores, key=lambda x: x[1])

        return self.report()


