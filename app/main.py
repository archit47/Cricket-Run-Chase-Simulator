import os
from app.models import Player
from app.resources import GamePlay


BATTING_LINEUP = None


def initialize_batting_lineup():
    global BATTING_LINEUP

    BATTING_LINEUP = list()

    BATTING_LINEUP.extend([
        Player('Kirat Boli', {
            '0': 5,
            '1': 30,
            '2': 25,
            '3': 10,
            '4': 15,
            '5': 1,
            '6': 9,
            'OUT': 5,
        }),

        Player('N.S. Nodhi', {
            '0': 10,
            '1': 40,
            '2': 20,
            '3': 5,
            '4': 10,
            '5': 1,
            '6': 4,
            'OUT': 10,
        }),

        Player('R Rumrah', {
            '0': 20,
            '1': 30,
            '2': 15,
            '3': 5,
            '4': 5,
            '5': 1,
            '6': 4,
            'OUT': 20,
        }),

        Player('Shashi Henra', {
            '0': 30,
            '1': 25,
            '2': 5,
            '3': 0,
            '4': 5,
            '5': 1,
            '6': 4,
            'OUT': 30,
        })
    ])


def main():
    initialize_batting_lineup()

    global BATTING_LINEUP  # not really required

    game = GamePlay(BATTING_LINEUP, 'random sampling')
    game.execute_run_chase()


if __name__ == '__main__':
    main()
