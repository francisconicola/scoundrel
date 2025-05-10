from collections.abc import Callable
from enum import Enum

import readchar
from rich.console import RenderableType
from rich.live import Live


def select_input(
    *,
    start: int = 0,
    option_count: int,
    live: Live,
    refresher: Callable[[int], RenderableType],
) -> int:
    selection = start
    live.update(refresher(start), refresh=True)
    while True:
        char = readchar.readkey()
        if char in [readchar.key.UP, readchar.key.LEFT]:
            selection = (selection - 1) % option_count
        elif char in [readchar.key.DOWN, readchar.key.RIGHT]:
            selection = (selection + 1) % option_count
        elif char in [readchar.key.ENTER, readchar.key.SPACE]:
            return selection
        else:
            continue
        live.update(refresher(selection), refresh=True)
