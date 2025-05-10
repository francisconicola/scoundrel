import random
from abc import ABC, abstractmethod

from src.cards import Card, Suit


class DeckShuffler(ABC):
    @abstractmethod
    def create_shuffled_deck(self) -> list[Card]:
        pass


class TrueRandomDeckShuffler(DeckShuffler):
    def create_shuffled_deck(self) -> list[Card]:
        deck: list[Card] = []
        for suit in Suit:
            for rank in range(2, 15):
                if suit in [Suit.HEARTS, Suit.DIAMONDS] and rank in [11, 12, 13, 14]:
                    continue
                deck.append(Card(suit, rank))
        random.shuffle(deck)
        return deck


class ControlledDeckShuffler(DeckShuffler):
    def create_shuffled_deck(self) -> list[Card]:
        utility_cards = [
            Card(suit, rank)
            for suit in [Suit.HEARTS, Suit.DIAMONDS]
            for rank in range(2, 11)
        ]
        enemy_cards = [
            Card(suit, rank)
            for suit in [Suit.CLUBS, Suit.SPADES]
            for rank in range(2, 15)
        ]
        random.shuffle(utility_cards)
        random.shuffle(enemy_cards)

        def pick_controlled(utility: int, enemy: int) -> list[Card]:
            pile = [utility_cards.pop() for _ in range(utility - 1)] + [
                enemy_cards.pop() for _ in range(enemy - 1)
            ]
            random.shuffle(pile)
            return pile

        first_pile = pick_controlled(5, 6)
        second_pile = pick_controlled(4, 7)
        remaining_pile = utility_cards + enemy_cards
        random.shuffle(remaining_pile)
        return first_pile + second_pile + remaining_pile
