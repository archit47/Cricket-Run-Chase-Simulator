#!/usr/bin/env python3

import os
from app.models import Player
from app.resources import GamePlay
import optparse


def get_team():
    """
    Initializes the squad: the list of players in the order they are
    expected to bat.
    Uses the Player model to create each batsman with their given
    scoring probabilities.
    """

    batsmen_list = [
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
    ]

    return batsmen_list


def main():
    """
    Lets the game begin!
    """

    batting_lineup = get_team()

    # new Game instance
    game = GamePlay(batting_lineup, 'random sampling')
    game.execute_run_chase()


if __name__ == '__main__':
    main()

