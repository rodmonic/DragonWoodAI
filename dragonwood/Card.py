
class Dragonwood_Card():
    def __init__(self, strike: int, stomp: int, scream: int, name: str) -> None:
        self.strike = strike
        self.stomp = stomp
        self.scream = scream
        self.name = name

class Creature(Dragonwood_Card):
    def __init__(self, points: int, strike: int, stomp: int, scream: int, name: str, game_ender: bool) -> None:
        Dragonwood_Card.__init__(self, strike, stomp, scream, name)
        self.points = points
        self.game_ender = game_ender

    def __str__(self):
        return f'C:{self.name}:{self.points}:{self.strike}:{self.stomp}:{self.scream}'

    def __repr__(self) -> str:
        return f'C:{self.name}:{self.points}:{self.strike}:{self.stomp}:{self.scream}'

class Enhancement(Dragonwood_Card):
    def __init__(self, strike: int, stomp: int, scream: int, name: str, modifications: list[object], modifier: int, permanent: bool) -> None:
        Dragonwood_Card.__init__(self, strike, stomp, scream, name)
        self.modifications = modifications
        self.modifier = modifier
        self.permanent = permanent

    def __str__(self):
        return f'E:{self.name}::{self.strike}:{self.stomp}:{self.scream}'

    def __repr__(self) -> str:
        return f'E:{self.name}::{self.strike}:{self.stomp}:{self.scream}'
    

class Adventurer_Card():
    def __init__(self, suit: int, value: int) -> None:
        self.value = value
        self.suit = suit

    def __str__(self):
        return f'Adventurer({self.suit}:{self.value})'

    def __repr__(self) -> str:
        return f'Adventurer({self.suit}:{self.value})'
    
    def __key(self):
        return (self.value, self.suit)
    
    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        if isinstance(other, Adventurer_Card):
            return self.__key()==other.__key()
        return False
    


