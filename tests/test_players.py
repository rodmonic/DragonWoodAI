from Dragonwood.Player import Player
from Dragonwood.Deck import Dragonwood_Deck, Adventurer_Deck, Adventurer_Card
import Dragonwood.SharedRandom as sr
sr.set_seed(100)


dragonwood_deck = Dragonwood_Deck("./cards/creatures.csv", "./cards/enhancements.csv")
adventurer_deck = Adventurer_Deck(5,13)
player = Player(0, 0, "Alice")

player.hand = adventurer_deck.deal(10)
landscape = dragonwood_deck.deal(5)

def test_find_strikes():

    strikes = player.find_strikes()
    
    assert len(strikes) == 4
    assert str(strikes[0]) == "[Adventurer(4:9)]"

def test_find_stomps():
    
    stomps = player.find_stomps()

    assert len(stomps) == 2
    assert str(stomps[0]) == "[Adventurer(1:2)]"

def test_find_screams():
    
    screams = player.find_screams()

    assert len(screams) == 4
    assert str(screams[0]) == "[Adventurer(4:4)]"


def test_decide_on_landscape():

    decision = player.decide(landscape, 2.5)

    print(player.hand)
    print(landscape)
    print(decision)

    assert decision['decision'] == "strike"
    assert len(decision['adventurers']) == 3


def test_discard_card():
    card = Adventurer_Card(0,1)

    assert card in player.hand
    assert card not in adventurer_deck.discard

    player.discard_card(adventurer_deck)

    assert card not in player.hand
    assert card in adventurer_deck.discard
