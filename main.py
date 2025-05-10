from src.console import console
from src.game_menu import GameMenu


def main():
    try:
        GameMenu().run()
    except KeyboardInterrupt:
        console.system_print("Bye!")


if __name__ == "__main__":
    main()
