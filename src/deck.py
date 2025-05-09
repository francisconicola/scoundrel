import random
from typing import Iterable

from src.cards import Card, Suit


class Deck:
    def __init__(self):
        self.cards = self._create_deck()
        random.shuffle(self.cards)

    def _create_deck(self):
        deck = []
        for suit in Suit:
            for rank in range(2, 15):
                # Remove red face cards and red aces
                if suit in [Suit.HEARTS, Suit.DIAMONDS] and rank in [11, 12, 13, 14]:
                    continue
                deck.append(Card(suit, rank))
        return deck

    def draw(self, count=1) -> list[Card]:
        return [self.cards.pop(0) for _ in range(min(count, len(self.cards)))]

    def put_back(self, cards: Iterable[Card]) -> None:
        self.cards.extend(cards)

    def __len__(self):
        return len(self.cards)
