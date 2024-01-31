import random

class Dice():

    def __init__(self, values: list, seed: int|None = None) -> None:
        self.values = values
        self.EV = 0
        self.caculate_EV()
        self.seed = seed
        self.set_seed()

    def set_seed(self) -> None:
        random.seed(self.seed)

    def caculate_EV(self):
        self.EV = sum(self.values)/len(self.values)

    def roll_n_dice(self, n):
        total = 0
        for _ in range(n):
            total += random.choice(self.values)
        return total
