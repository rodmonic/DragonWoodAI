from Dragonwood.SharedRandom import shared_random

class Dice():

    def __init__(self, values: list) -> None:
        self.values = values
        self.EV = 0
        self.caculate_EV()

    def caculate_EV(self) -> None:
        self.EV = sum(self.values)/len(self.values)

    def roll_n_dice(self, n) -> int:
        total = 0
        for _ in range(n):
            total += shared_random.choice(self.values)
        return total
