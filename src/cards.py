from enum import Enum


class Suit(Enum):
    HEARTS = "\u2665"
    DIAMONDS = "\u2666"
    CLUBS = "\u2663"
    SPADES = "\u2660"


class Card:
    RANK_TO_CHAR = {11: "J", 12: "Q", 13: "K", 14: "A"}

    def __init__(self, suit: Suit, rank: int):
        assert rank >= 2 and rank <= 14
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        rank_str = Card.RANK_TO_CHAR.get(self.rank, str(self.rank))
        return f"[{self.suit.value} {rank_str}]"
