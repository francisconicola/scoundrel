from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.cards import Card


class Action(ABC):
    @abstractmethod
    def describe(self) -> str:
        pass


@dataclass
class Heal(Action):
    target: Card

    def describe(self) -> str:
        return f"You heal with {self.target}."


@dataclass
class Equip(Action):
    target: Card

    def describe(self) -> str:
        return f"You equip {self.target}."


@dataclass
class AttackBarehand(Action):
    target: Card

    def describe(self) -> str:
        return f"You attack {self.target} with your bare hands!"


@dataclass
class AttackWeapon(Action):
    target: Card

    def describe(self) -> str:
        return f"You attack {self.target} with your weapon."


@dataclass
class SkipRoom(Action):
    def describe(self) -> str:
        return "You escape the room."
