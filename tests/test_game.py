from sklearn.linear_model import GammaRegressor
from Dragonwood.Game import Game
from Dragonwood.Deck import Adventurer_Deck, Dragonwood_Deck, Creature, Adventurer_Card
from Dragonwood.Player import Player
from Dragonwood.Dice import Dice
import Dragonwood.SharedRandom as sr

dragonwood_deck = Dragonwood_Deck("./cards/creatures.csv", "./cards/enhancements.csv")
adventurer_deck = Adventurer_Deck(5, 12)
dice = Dice([1, 2, 2, 3, 3, 4])
players = [
            Player(0.5, -0.1, dice, "Alice"),
            Player(0.5, -0.1, dice, "Bob"),
            Player(0.5, -0.1, dice, "Charles"),
            Player(0.5, -0.1, dice, "Dylan")
    ]

creatures = [x for x in dragonwood_deck.cards if type(x) is Creature]

four_creatures = creatures[:4]
three_creatures = creatures[:3]
two_creatures = creatures[:2]

game = Game(adventurer_deck, dragonwood_deck, players, dice, True)

# test success


# test get winner
def test_get_clear_winner():

    # test when there is a clear winner
    players[0].points = 20
    players[1].points = 12
    players[2].points = 12
    players[3].points = 12

    assert game.get_winner() == players[0].uuid


def test_person_with_most_creature_cards_gets_2_points():

    players[0].points = 22
    players[1].points = 20
    players[2].points = 12
    players[3].points = 12

    players[0].dragonwood_cards = two_creatures
    players[1].dragonwood_cards = three_creatures

    assert game.get_winner() == players[1].uuid
    assert players[1].points == 23


def test_people_with_most_cards_gets_2_points():

    players[0].points = 21
    players[1].points = 20
    players[2].points = 12
    players[3].points = 12

    players[0].dragonwood_cards = two_creatures
    players[1].dragonwood_cards = three_creatures
    players[2].dragonwood_cards = three_creatures
    players[3].dragonwood_cards = three_creatures

    assert game.get_winner() == players[1].uuid
    assert players[1].points == 22


def test_when_tied_the_person_with_the_most_creatures_wins():

    players[0].points = 10
    players[1].points = 20
    players[2].points = 20
    players[3].points = 20

    players[0].dragonwood_cards = four_creatures
    players[1].dragonwood_cards = three_creatures
    players[2].dragonwood_cards = two_creatures
    players[3].dragonwood_cards = two_creatures

    assert game.get_winner() == players[1].uuid


def test_game_state():
    game = Game(adventurer_deck, dragonwood_deck, players, dice)

    _ = game.play(10)
    
    game_state = game.get_game_state(players[0])

    assert len(game_state) == 86

def test_game_state_adventurer_encoding():

    game = Game(adventurer_deck, dragonwood_deck, players, dice)

    _ = game.play(10)
    
    hand = [Adventurer_Card(0,0), Adventurer_Card(0,1), Adventurer_Card(2,11), Adventurer_Card(4,11)]
    


    players[0].hand = hand

    game_state = game.get_game_state(players[0])

    assert game_state[0] == 1
    assert game_state[1] == 1
    assert game_state[(2*12)+11] == 1
    assert game_state[(4*12)+11] == 1

def test_game_state_creature_ecoding():

    sr.set_seed(100)

    dragonwood_deck = Dragonwood_Deck("./cards/creatures.csv", "./cards/enhancements.csv")

    dragonwood_deck.cards[0]

    game = Game(adventurer_deck, dragonwood_deck, players, dice)

    game_state = game.get_game_state(players[0])

    assert game_state[60+11] == 1
    assert game_state[60+9] == 1
    assert game_state[60+12] == 1


# test failure
