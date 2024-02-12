from Dragonwood.SharedRandom import shared_random
import itertools
import csv
from Dragonwood.Card import Creature, Enhancement, Adventurer_Card, Dragonwood_Card
import ast
from typing import List

class Deck:
    def __init__(self):
        self.cards = []
        self.discard = []

    def shuffle(self) -> None:
        shared_random.shuffle(self.cards)

    def deal(self, n: int) -> List[Adventurer_Card|Dragonwood_Card]:
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
    


class Dragonwood_Deck(Deck):
    def __init__(self, creatures_file_path: str, enchantments_file_path: str, seed: int|None = None) -> None:
        Deck.__init__(self)
        self.import_creatures(creatures_file_path)
        self.import_enhancements(enchantments_file_path)

    def import_creatures(self, filepath: str) -> None:

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

    def import_enhancements(self, filepath: str) -> None:

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
    
    def initial_config(self, number_of_players: int) -> None:
        
        self.shuffle()
        # extract game ending cards
        game_enders = [x for x in self.cards if type(x) == Creature and x.game_ender]
        non_game_enders = [x for x in self.cards if x not in game_enders]

        # remove cards based on number of players
        number_cards_to_remove = 12 - ((number_of_players - 2)*2)
        cards = non_game_enders[number_cards_to_remove:]


        # shuffle game ending cards in the bottom of the deck.
        top_cards = cards[:len(cards)//2]
        bottom_cards = list(itertools.chain(cards[len(cards)//2:], game_enders))
        shared_random.shuffle(bottom_cards)

        self.cards = list(itertools.chain(top_cards, bottom_cards))


class Adventurer_Deck(Deck):
    def __init__(self, suits: int, values: int):
        Deck.__init__(self)
        self.generate_adventurer_deck(suits, values)
        self.shuffle()
        self.number_of_deals = 1


    def generate_adventurer_deck(self, suits: int, values: int) -> None:
        # adventurer cards
        self.cards = [
            Adventurer_Card(i, j)
            for i in range(0, suits)
            for j in range(0, values)
            ]