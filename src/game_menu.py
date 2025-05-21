import random
from collections.abc import Callable
from dataclasses import dataclass
from typing import NoReturn, Optional

import readchar
from rich.console import RenderableType
from rich.live import Live
from rich.text import Text

from src.console import console
from src.game_presenter import GamePresenter
from src.input_selector import select_input


@dataclass
class MenuOption:
    label: str
    callback: Callable[[], bool]


class GameMenu:

    def print_title(self) -> None:
        title = """╔═══╗                  ╔╗       ╔╗ 
║╔═╗║                  ║║       ║║ 
║╚══╗╔══╗╔══╗╔╗╔╗╔═╗ ╔═╝║╔═╗╔══╗║║ 
╚══╗║║╔═╝║╔╗║║║║║║╔╗╗║╔╗║║╔╝║╔╗║║║ 
║╚═╝║║╚═╗║╚╝║║╚╝║║║║║║╚╝║║║ ║║═╣║╚╗
╚═══╝╚══╝╚══╝╚══╝╚╝╚╝╚══╝╚╝ ╚══╝╚═╝"""
        console.print(title)

    def run(self) -> None:
        print_title_again = True
        menu_options = [
            MenuOption(label="Start new game", callback=self.start_new_game),
            MenuOption(label="Read manual", callback=self.read_manual),
            MenuOption(label="Quit (Ctrl + C)", callback=self.quit_game),
        ]
        while True:
            if print_title_again:
                self.print_title()
                console.system_print("Welcome!")
            selection_indicator = random.choice(
                [
                    Text("\u2665", style="scoundrel.heart"),
                    Text("\u2666", style="scoundrel.diamond"),
                    Text("\u2663", style="scoundrel.club"),
                    Text("\u2660", style="scoundrel.spade"),
                ]
            )
            menu_selection: Optional[int] = None
            with Live(console=console, auto_refresh=False, transient=True) as live:

                def refresh_main_menu(selection: int) -> RenderableType:
                    return self.build_main_menu(
                        menu_options, selection_indicator, selection
                    )

                menu_selection = select_input(
                    option_count=len(menu_options),
                    live=live,
                    refresher=refresh_main_menu,
                )
            print_title_again = menu_options[menu_selection].callback()
            if print_title_again:
                console.print()

    def build_main_menu(
        self,
        menu_options: list[MenuOption],
        selection_indicator: Text,
        menu_selection: int,
    ) -> RenderableType:
        return Text("\n").join(
            [
                Text(" ").join(
                    [
                        (selection_indicator if index == menu_selection else Text(" ")),
                        Text(
                            option.label,
                            style="u" if index == menu_selection else "",
                        ),
                    ]
                )
                for index, option in enumerate(menu_options)
            ]
        )

    def start_new_game(self) -> bool:
        GamePresenter().run()
        return True

    def read_manual(self) -> bool:
        with Live(console=console, auto_refresh=False, transient=True) as live:
            rules = """- You begin the game with [yellow]20[/yellow] [scoundrel.heart]health[/scoundrel.heart] points.
- Build the deck from a standard 52-card set by removing all red face cards and red Aces.
- On each turn, draw [yellow]4[/yellow] cards to form a [yellow]room[/yellow].
- Choose [yellow]3[/yellow] cards to resolve; [yellow]1[/yellow] stays and carries into the [yellow]next room[/yellow].
- [scoundrel.spade]Spades[/scoundrel.spade] and [scoundrel.club]Clubs[/scoundrel.club] are [scoundrel.spade]mons[/scoundrel.spade][scoundrel.club]ters[/scoundrel.club] — they deal damage based on their [yellow]rank[/yellow].
- [scoundrel.diamond]Diamonds[/scoundrel.diamond] are [scoundrel.diamond]weapons[/scoundrel.diamond] — equip them to reduce damage from [scoundrel.spade]mons[/scoundrel.spade][scoundrel.club]ters[/scoundrel.club].
- [scoundrel.heart]Hearts[/scoundrel.heart] are [scoundrel.heart]potions[/scoundrel.heart] — use them to heal based on its [yellow]rank[/yellow].
- You may only carry one [scoundrel.diamond]weapon[/scoundrel.diamond] at a time; new ones replace the old.
- Equipped [scoundrel.diamond]weapons[/scoundrel.diamond] reduce damage taken when attacking; you only take the difference in [yellow]rank[/yellow].
- After defeating a [scoundrel.spade]mons[/scoundrel.spade][scoundrel.club]ter[/scoundrel.club] with a [scoundrel.diamond]weapon[/scoundrel.diamond], it can only be used again on a [scoundrel.spade]mons[/scoundrel.spade][scoundrel.club]ter[/scoundrel.club] with equal or lower [yellow]rank[/yellow].
- You may always choose to fight [scoundrel.diamond]barehanded[/scoundrel.diamond], taking full [scoundrel.spade]mons[/scoundrel.spade][scoundrel.club]ter[/scoundrel.club] damage.
- You may [yellow]skip[/yellow] a [yellow]room[/yellow]; all [yellow]4[/yellow] cards go to the bottom of the deck.
- You cannot [yellow]skip[/yellow] twice in a row.
- The game ends when your [scoundrel.heart]health[/scoundrel.heart] reaches [yellow]0[/yellow] or the dungeon is empty.
[scoundrel.placeholder]Press any key to return...[/scoundrel.placeholder]
"""
            live.update(rules, refresh=True)
            readchar.readkey()
        return False

    def quit_game(self) -> NoReturn:
        console.system_print("Bye!")
        exit()
