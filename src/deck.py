from typing import Iterable

from src.cards import Card
from src.shuffler import DeckShuffler


class Deck:
    def __init__(self, shuffler: DeckShuffler):
        self.cards = shuffler.create_shuffled_deck()

    def draw(self, count=1) -> list[Card]:
        return [self.cards.pop(0) for _ in range(min(count, len(self.cards)))]

    def put_back(self, cards: Iterable[Card]) -> None:
        self.cards.extend(cards)

    def __len__(self):
        return len(self.cards)
