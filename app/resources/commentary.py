#!/usr/bin/env python3

from app.constants import SCORE_KEYS, MAX_OVERS, TARGET_RUNS


class Commentary(object):
    """
    To record ball-by-ball description of the match.
    The narration of the match has 3 basic components:
    -> Summary of the chase before every over
    -> Commentary for each and every ball bowled in the over
    -> Post-match summary

    This class provides utility methods for recording each of the 3 types
    of commentaries. It is upto the user of the class' object to call whichever
    methods are required in the process of storing the commentary line,
    and in the order the user deems fit.

    NOTE:
        [1] This Commentary class, in the initial draft, is designed in the
        context of a run-chase.
        [2] No validation-policy: this commentary class is not expected
        to perform data validations. It still performs very minimal though.
    """

    def __init__(self):
        self._match_commentary = list()

    def _add_commentary_line(self, string, append=True):
        if append:
            self._match_commentary.append(string)
        else:
            self._match_commentary.insert(0, string)

    def before_over_overview(self, overs_left,
                             runs_left_to_chase, wickets_in_hand):
        """
        Add a string in match commentary, describing the summary of the run-chase
        :param overs_left: Number of overs remaining
        :param runs_left_to_chase: Amount of runs left to achieve the target
        :param wickets_in_hand: Remaining wickets left with the chasers
        """

        assert isinstance(overs_left, int) and overs_left <= MAX_OVERS
        assert (isinstance(runs_left_to_chase, int) and
                runs_left_to_chase <= TARGET_RUNS)
        assert isinstance(wickets_in_hand, int) and (1 <= wickets_in_hand <= 10)

        self._add_commentary_line(
            '\n{} over(s) left, {} runs to win, {} wickets remaining\n'.\
            format(overs_left, runs_left_to_chase, wickets_in_hand)
        )

    def per_ball_commentary(self, over_number, ball_number, batsman, score):
        """
        Add a string in match commentary, storing the description of a
        happening of an individual ball, like which batsmen scored how many
        runs or got if he OUT.
        :param over_number: Nth over of the inning
        :param ball_number: B/w 1-6, which ball of the over it is
        :param batsman: The player at the crease
        :param score: The runs scored by the batsman or if he got OUT
        """

        assert isinstance(over_number, int) and 0 <= over_number
        assert isinstance(ball_number, int) and 1 <= ball_number <= 6
        assert isinstance(batsman, str) and len(batsman) > 1
        assert isinstance(score, str) and score in SCORE_KEYS

        description = None

        if score == 'OUT':
            description = (
                '{}.{} {} is OUT'.format(over_number, ball_number, batsman)
            )
        elif score == '1':
            description = (
                '{}.{} {} scores 1 run'.\
                format(over_number, ball_number, batsman)
            )
        else:
            description = (
                '{}.{} {} scores {} runs'.\
                format(over_number, ball_number, batsman, score)
            )

        self._add_commentary_line(description)

    def match_result_summary(self, chase_successful, winner_team,
                             runs=None, wickets_at_hand=None, balls_left=None):
        """
        Add a string in match commentary, paraphrasing the outcome of the game
        In case of a `Tie`:
            -> chase_successful is False and winner_team is None

        :param chase_successful: a boolean value expected
        :param winner_team: the name of the team that won the match, str expected
        :param runs: victory margin of the team that won the match
        :param wickets_at_hand: wickets left when the target was chased down
        :param balls_left: (optional) number of balls to spare with the chasers

        :return: (this method does not returns anything)
        """

        assert (chase_successful is not None
                and isinstance(chase_successful, bool))

        description = None

        if chase_successful:
            assert (wickets_at_hand is not None
                    and isinstance(wickets_at_hand, int))
            assert isinstance(winner_team, str)

            wicket_string = ('%d wicket' % wickets_at_hand)
            if wickets_at_hand > 1:
                wicket_string += 's'

            if balls_left:
                balls_left = int(balls_left)

                description = (
                    '{} won by {} and {} balls remaining'.\
                    format(winner_team, wicket_string, balls_left)
                )
            else:
                description = '{} won by {}'.format(winner_team, wicket_string)

        else:
            if winner_team:
                assert runs is not None and isinstance(runs, int)

                runs_string = ('%d run' % runs)
                if runs > 1:
                    runs_string += 's'

                description = '{} won by {}'.format(winner_team, runs_string)

            else:
                description = 'The match has ended in Tie'

        self._add_commentary_line('\n' + description)

    def print_match_commentary(self):
        print('\n'.join(self._match_commentary))

    def get_match_commentary(self):
        return self._match_commentary

