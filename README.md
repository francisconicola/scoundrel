```
╔═══╗                  ╔╗       ╔╗ 
║╔═╗║                  ║║       ║║ 
║╚══╗╔══╗╔══╗╔╗╔╗╔═╗ ╔═╝║╔═╗╔══╗║║ 
╚══╗║║╔═╝║╔╗║║║║║║╔╗╗║╔╗║║╔╝║╔╗║║║ 
║╚═╝║║╚═╗║╚╝║║╚╝║║║║║║╚╝║║║ ║║═╣║╚╗
╚═══╝╚══╝╚══╝╚══╝╚╝╚╝╚══╝╚╝ ╚══╝╚═╝
```

Hi! I made a dungeon crawler solo card game in Python for the terminal. It's fun, you should play it.

Credit to **Zach Gage** and **Kurt Bieg** for the [original rules](http://stfj.net/art/2011/Scoundrel.pdf).

- You begin the game with 20 health points.
- Build the deck from a standard 52-card set by removing all red face cards and red Aces.
- On each turn, draw 4 cards to form a room.
- Choose 3 cards to resolve; 1 stays and carries into the next room.
- Spades and Clubs are monsters — they deal damage based on their rank.
- Diamonds are weapons — equip them to reduce damage from monsters.
- Hearts are potions — use them to heal based on its rank.
- You may only carry one weapon at a time; new ones replace the old.
- After defeating a monster with a weapon, it can only be used again on a monster with equal or lower rank.
- You may always choose to fight barehanded, taking full monster damage.
- You may skip a room; all 4 cards go to the bottom of the deck.
- You cannot skip twice in a row.
- The game ends when your health reaches 0 or the dungeon is empty.

_(Rules are modified from the original version)_

# How to run

## Using `uv`

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/) to be installed.

1. Just run `uv run main.py`.

## Using `pip`

Requires **Python 3.13** to be installed. Other versions may work, but are not tested.

1. Create and activate a virtual environment.

```
python3 -m venv .venv

# On UNIX-like systems
source .venv/bin/activate
# On Windows
source .venv\Scripts\activate
```

2. Install dependencies.

```
pip install -r requirements.txt
```

3. Run the main script.

```
python3 main.py
```
