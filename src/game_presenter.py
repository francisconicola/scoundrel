from typing import Literal, Optional

import readchar
from rich.console import RenderableType
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from src.action import Action, AttackBarehand, AttackWeapon, Equip, Heal, SkipRoom
from src.cards import Suit
from src.console import console, highlighter
from src.game_state import GameResult, GameState


class GamePresenter:
    def __init__(self):
        self.game = GameState()

    def run(self) -> None:
        console.print("─── Game start!", style="green bold")
        self.game.go_to_next_room()
        current_room = None
        while self.game.game_result == None:
            if current_room != self.game.room_count:
                console.print(
                    f"─── Entering room {self.game.room_count}", style="green bold"
                )
                current_room = self.game.room_count
            action = self.prompt_user_action()
            self.game.apply_action(action)
        if self.game.game_result == GameResult.WIN:
            console.print("─── You win! :3", style="green bold")
            console.print(f"Rooms visited: [b]{self.game.room_count}[/b]")
            console.print(f"Remaining health: [b]{self.game.health}[/b]")
        else:
            console.print("─── You lose...", style="green bold")
            console.print("Better luck next time ;)")
        console.print("Press any key to restart...\n", style="grey42")
        readchar.readchar()

    def prompt_user_action(self) -> Action:
        with Live(
            auto_refresh=False,
            console=console,
        ) as live:
            action: Optional[Action] = None
            main_selection = self.choose_main_selection(live)
            if main_selection == len(self.game.room):
                action = SkipRoom()
            else:
                selected_card = self.game.room[main_selection]
                match selected_card.suit:
                    case Suit.HEARTS:
                        action = Heal(selected_card)
                    case Suit.DIAMONDS:
                        action = Equip(selected_card)
                    case Suit.CLUBS | Suit.SPADES:
                        if (
                            self.game.equipped_weapon == None
                            or not self.game.can_attack_with_weapon(selected_card)
                            or self.choose_attack(live, main_selection) == "barehand"
                        ):
                            action = AttackBarehand(selected_card)
                        else:
                            action = AttackWeapon(selected_card)
            live.update(self.build_room(action_taken=action))
            return action

    def choose_main_selection(self, live: Live) -> int:
        main_selection = 0
        live.update(self.build_room(main_selection=0), refresh=True)
        while True:
            char = readchar.readkey()
            option_count = len(self.game.room) + int(self.game.can_skip_room())
            if char == readchar.key.RIGHT:
                main_selection = (main_selection + 1) % option_count
            elif char == readchar.key.LEFT:
                main_selection = (main_selection - 1) % option_count
            elif char == readchar.key.ENTER:
                live.update(self.build_room(), refresh=True)
                break
            live.update(
                self.build_room(main_selection=main_selection),
                refresh=True,
            )
        return main_selection

    def choose_attack(
        self, live: Live, main_selection: int
    ) -> Literal["barehand", "weapon"]:
        attack_selection = 0
        live.update(
            self.build_room(
                main_selection=main_selection,
                attack_selection=attack_selection,
            ),
            refresh=True,
        )
        while True:
            char = readchar.readkey()
            if char == readchar.key.RIGHT:
                attack_selection = (attack_selection + 1) % 2
            elif char == readchar.key.LEFT:
                attack_selection = (attack_selection - 1) % 2
            elif char == readchar.key.ENTER:
                live.update(self.build_room(), refresh=True)
                break
            live.update(
                self.build_room(
                    main_selection=main_selection,
                    attack_selection=attack_selection,
                ),
                refresh=True,
            )
        return "barehand" if bool(attack_selection) else "weapon"

    def build_room(
        self,
        *,
        main_selection: Optional[int] = None,
        attack_selection: Optional[int] = None,
        action_taken: Optional[Action] = None,
    ) -> RenderableType:
        panel_width = 44
        panel_padding = 1
        main_options = [Text(str(card)) for card in self.game.room] + [
            Text("\u21a9Skip", style="grey30" if not self.game.can_skip_room() else "")
        ]
        if main_selection != None:
            main_options[main_selection].stylize("u")
        attack_options = (
            [Text("Weapon"), Text("Barehand")] if attack_selection != None else []
        )
        if attack_selection != None:
            attack_options[attack_selection].stylize("u")
        content = [Text(" ").join(main_options), Text(" ").join(attack_options)]
        content.append(Text("─" * (panel_width - (panel_padding + 1) * 2)))
        card_placeholder = "[ - ]"
        equipped_weapon = self.game.equipped_weapon or card_placeholder
        weapon_last_slain = self.game.weapon_last_slain or card_placeholder
        content.append(Text(f"Equip: {equipped_weapon} | Slain: {weapon_last_slain}"))
        content.append(
            Text(
                (
                    action_taken.describe()
                    if action_taken
                    else "Please select an option..."
                ),
                style="" if action_taken else "grey42",
            )
        )
        return Panel(
            highlighter(Text("\n").join(content)),
            title=f"[yellow]Room [italic]#{self.game.room_count:02}[/italic][/yellow] "
            + f"| [green]HP:{self.game.health:3}[/green]",
            title_align="left",
            subtitle=f"[yellow]Remaining: [italic]{self.game.remaining:2}[/italic][/yellow]",
            subtitle_align="right",
            highlight=True,
            padding=panel_padding,
            width=panel_width,
        )
