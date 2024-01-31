
import dragonwood.dice as dw

dice = dw.Dice([1,2,3,4,5,6], 100)
    
def test_card_EV_creation():

    assert dice.EV == 3.5

def test_roll_n_dice():

    assert dice.roll_n_dice(5) == 18

