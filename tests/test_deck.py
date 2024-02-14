from Dragonwood.Deck import Dragonwood_Deck, Adventurer_Deck


dragonwood_deck = Dragonwood_Deck("./cards/creatures.csv", "./cards/enhancements.csv")
adventurer_deck = Adventurer_Deck(5, 13)


def test_dragonwood_deck_import():

    dragonwood_deck.shuffle()
    assert len(dragonwood_deck.cards) == 39


def test_number_of_players_deck_config():
    dragonwood_deck_config = Dragonwood_Deck("./cards/creatures.csv", "./cards/enhancements.csv")

    dragonwood_deck_config.initial_config(2)
    assert len(dragonwood_deck_config.cards) == 27

    dragonwood_deck_config = Dragonwood_Deck("./cards/creatures.csv", "./cards/enhancements.csv")

    dragonwood_deck_config.initial_config(3)
    assert len(dragonwood_deck_config.cards) == 29


def test_dragonwood_deck_deal_cards():

    cards = dragonwood_deck.deal(5)

    assert len(cards) == 5


def test_dragonwood_deck_doesnt_redeal():

    cards = dragonwood_deck.deal(50)
    assert len(cards) == 34


def test_adventurer_deck_import():

    assert len(adventurer_deck.cards) == 65
    assert max([x.suit for x in adventurer_deck.cards]) == 4
    assert max([x.value for x in adventurer_deck.cards]) == 12


def test_adventurer_deck_deal_cards():

    cards = adventurer_deck.deal(5)

    assert len(cards) == 5


def test_adventure_deck_redeal():

    cards = adventurer_deck.deal(60)
    adventurer_deck.discard = cards
    cards = adventurer_deck.deal(5)

    assert len(adventurer_deck.cards) == 55
    assert len(adventurer_deck.discard) == 0
    assert adventurer_deck.number_of_deals == 2


def test_dragonwood_card_lookup():

    dragonwood_deck_lookup = Dragonwood_Deck("./cards/creatures.csv", "./cards/enhancements.csv")
    dw_lookup = dragonwood_deck_lookup.generate_lookup()

    assert len(dw_lookup) == 21
    assert dw_lookup['Giggling Goblin'] == 9
