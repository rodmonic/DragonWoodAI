import random

class Dice():

    def __init__(self, values: list, seed: int|None = None) -> None:
        self.values = values
        self.EV = 0
        self.caculate_EV()
        self.set_seed(seed)

    def set_seed(self, seed: int) -> None:
        random.seed(seed)

    def caculate_EV(self) -> None:
        self.EV = sum(self.values)/len(self.values)

    def roll_n_dice(self, n) -> int:
        total = 0
        for _ in range(n):
            total += random.choice(self.values)
        return total
