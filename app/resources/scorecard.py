#!/usr/bin/env python3

from collections import OrderedDict


class Scorecard(object):
    """
    A class to store the player statistics of the game
    """

    def __init__(self, tags=None):
        self._scorecard_registry = OrderedDict()
        self.innings_tags = tags

    @staticmethod
    def _default_factory_scorecard():
        return {
            'runs_scored': 0,
            'balls_faced': 0,
            'not_out': True,
        }

    def add_player(self, batsman_name):
        assert isinstance(batsman_name, str) and batsman_name

        self._scorecard_registry[batsman_name] = (
            Scorecard._default_factory_scorecard()
        )

    def add_runs(self, batsman_name, runs):
        assert isinstance(batsman_name, str)
        assert (isinstance(runs, int) and 0 <= runs <= 6)

        if batsman_name not in self._scorecard_registry:
            self.add_player(batsman_name)

        if self._scorecard_registry[batsman_name]['not_out']:
            self._scorecard_registry[batsman_name]['runs_scored'] += runs
            self._scorecard_registry[batsman_name]['balls_faced'] += 1
        else:
            raise Exception('Invalid operation: Batsmen({}) is already out '
                            'and back in the pavilion'.format(batsman_name))

    def mark_out(self, batsman_name):
        if batsman_name not in self._scorecard_registry:
            self.add_player(batsman_name)

        self._scorecard_registry[batsman_name]['balls_faced'] += 1
        self._scorecard_registry[batsman_name]['not_out'] = False

    def print_scorecard(self):
        for batsmen, game_data in self._scorecard_registry.items():
            print('{} - {}{} ({} ball{})'.\
                  format(batsmen,
                         game_data['runs_scored'],
                         ('*' if game_data['not_out'] else ''),
                         game_data['balls_faced'],
                         ('s' if game_data['balls_faced'] > 1 else '')))

