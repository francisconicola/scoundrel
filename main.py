from src.console import console
from src.game_presenter import GamePresenter
from src.title import print_title


def main():
    try:
        while True:
            print_title()
            GamePresenter().run()
    except KeyboardInterrupt:
        console.print("Shutting down...")


if __name__ == "__main__":
    main()
