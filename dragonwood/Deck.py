import random
import csv
from Dragonwood.Card import Creature, Enhancement, Adventurer_Card, Dragonwood_Card
import ast
from typing import List

class Deck:
    def __init__(self, seed: int|None = None):
        self.cards = []
        self.discard = []
        self.set_seed(seed)

    def set_seed(self, seed) -> None:
        random.seed(seed)

    def shuffle(self) -> None:
        random.shuffle(self.cards)

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
        Deck.__init__(self, seed)
        self.import_creatures(creatures_file_path)
        self.import_enhancements(enchantments_file_path)
        self.shuffle()

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
                
class Adventurer_Deck(Deck):
    def __init__(self, suits: int, values: int, hand_size: int, seed: int|None = None):
        Deck.__init__(self, seed)
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