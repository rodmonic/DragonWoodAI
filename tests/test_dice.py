from Dragonwood.Dice import Dice
import Dragonwood.SharedRandom as sr

SEED = 100

dice = Dice([1, 2, 3, 4, 5, 6])


def test_card_EV_creation():

    assert dice.EV == 3.5


def test_roll_n_dice():

    sr.set_seed(SEED)

    assert dice.roll_n_dice(5) == 18
