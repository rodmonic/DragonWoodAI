from Dragonwood.Deck import Dragonwood_Deck, Adventurer_Deck
import Dragonwood.SharedRandom as sr
sr.set_seed(100)

dragonwood_deck = Dragonwood_Deck("./cards/creatures.csv", "./cards/enhancements.csv")
adventurer_deck = Adventurer_Deck(5,13)


def test_dragonwood_deck_import():

    assert len(dragonwood_deck.cards) == 39
    assert dragonwood_deck.cards[0].name == "Grumpy Troll"


def test_dragonwood_deck_deal_cards():
    cards = dragonwood_deck.deal(5)

    assert len(cards) == 5
    assert [x.name for x in cards] == ['Grumpy Troll', 'Grumpy Troll', "Giggling Goblin", 'Giggling Goblin', 'Hungry Bear']

def test_dragonwood_deck_doesnt_redeal():
    
    cards = dragonwood_deck.deal(50)

    assert len(cards)==34

def test_adventurer_deck_import():

    assert len(adventurer_deck.cards) == 65
    assert adventurer_deck.cards[0].suit == 1
    assert adventurer_deck.cards[0].value == 2
    assert max([x.suit for x in adventurer_deck.cards]) == 4
    assert max([x.value for x in adventurer_deck.cards]) == 12

def test_adventurer_deck_deal_cards():

    cards = adventurer_deck.deal(5)

    assert len(cards) == 5

def test_adventure_deck_redeal():
    
    cards = adventurer_deck.deal(60)
    adventurer_deck.discard = cards
    cards = adventurer_deck.deal(5)

    assert len(adventurer_deck.cards)==55
    assert len(adventurer_deck.discard)==0
    assert adventurer_deck.number_of_deals == 2


