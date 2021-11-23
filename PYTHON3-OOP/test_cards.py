from dataclasses import dataclass, field
from typing import Any, List
import math 

@dataclass 
class DataClassCard:
    rank: str 
    suit: str 
 
class RegularCard:
    def __init__(self, rank, suit):
        self.rank = rank 
        self.suit = suit 

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'(rank={self.rank!r}, suit={self.suit!r})') 
    
    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented 
        return (self.rank, self.suit) == (other.rank, other.suit)

@dataclass 
class Position:
    name: str 
    lon: float = 0.0
    lat: float = 0.0

    # adding some functions 

    def distance_to(self, other):
        r = 6371 # earth raduis in kilometer 
        lam_1, lam_2 = math.radians(self.lon), math.radians(other.lon) 
        phi_1, phi_2 = math.radians(self.lat), math.radians(other.lat)
        h = (math.sin((phi_2 - phi_1) / 2) ** 2 \
            + math.cos(phi_1) * math.cos(phi_2) * math.sin((lam_2 - lam_1)/ 2)**2)
        
        return 2*r* math.asin(math.sqrt(h))

@dataclass 
class WithoutExplicitTypes:
    name: Any 
    value: Any = 40

@dataclass  
class PlayingCard:
    rank: str 
    suit: str 

@dataclass 
class Deck:
    cards: List[PlayingCard]

# queen_of_hearts = PlayingCard('Q', 'Hearts')
# ace_of_spades = PlayingCard('A', 'Spades')
# two_cards = Deck([queen_of_hearts, ace_of_spades])


RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
SUITS = '♣ ♢ ♡ ♠'.split()

def make_french_deck():
    return [PlayingCard(r, s) for s in SUITS for r in RANKS]

@dataclass 
class Deck:
    cards: List[PlayingCard] = field(default_factory=make_french_deck) # we use field to handle mutable default value 


# adding metadata paramets to the position class 
@dataclass 
class Position:
    name: str 
    lon: float = field(default=0.0, metadata={'unit':'degrees'})
    lat: float = field(default=0.0, metadata={'unit':'degrees'})