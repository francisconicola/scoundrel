from enum import Enum, auto
from typing import Optional

from src.action import Action, AttackBarehand, AttackWeapon, Equip, Heal, SkipRoom
from src.cards import Card
from src.deck import Deck
from src.shuffler import ControlledDeckShuffler


class GameResult(Enum):
    WIN = auto()
    LOSE = auto()


class GameState:
    MAX_HEALTH = 20
    ROOM_SIZE = 4

    def __init__(self):
        self.deck = Deck(ControlledDeckShuffler())
        self.health = GameState.MAX_HEALTH
        self.equipped_weapon: Optional[Card] = None
        self.weapon_last_slain: Optional[Card] = None
        self.prev_room_skipped = False
        self.room: list[Card] = []
        self.room_count = 0

    @property
    def remaining(self) -> int:
        return len(self.deck) + len(self.room)

    @property
    def game_result(self) -> Optional[GameResult]:
        if self.health <= 0:
            return GameResult.LOSE
        elif self.remaining == 0:
            return GameResult.WIN
        else:
            return None

    def go_to_next_room(self, *, skipped=False) -> None:
        room_len = len(self.room)
        if room_len >= GameState.ROOM_SIZE:
            return
        self.room.extend(self.deck.draw(GameState.ROOM_SIZE - room_len))
        self.room_count += 1
        self.prev_room_skipped = skipped

    def can_attack_with_weapon(self, target: Card) -> bool:
        return self.equipped_weapon != None and (
            self.weapon_last_slain == None or self.weapon_last_slain.rank >= target.rank
        )

    def can_skip_room(self) -> bool:
        return not self.prev_room_skipped and len(self.room) == GameState.ROOM_SIZE

    def apply_action(self, action: Action) -> None:
        match action:
            case Heal(target):
                self.health = min(self.health + target.rank, GameState.MAX_HEALTH)
                self.remove_card_from_room(target)
            case Equip(target):
                self.equipped_weapon = target
                self.weapon_last_slain = None
                self.remove_card_from_room(target)
            case AttackBarehand(target):
                self.health -= target.rank
                self.remove_card_from_room(target)
            case AttackWeapon(target):
                assert self.equipped_weapon
                self.health -= max(target.rank - self.equipped_weapon.rank, 0)
                self.weapon_last_slain = target
                self.remove_card_from_room(target)
            case SkipRoom():
                self.deck.put_back(self.room)
                self.room.clear()
                self.go_to_next_room(skipped=True)
                return
        if len(self.room) <= 1 and len(self.deck) > 0:
            self.go_to_next_room()

    def remove_card_from_room(self, card: Card):
        self.room.remove(card)
