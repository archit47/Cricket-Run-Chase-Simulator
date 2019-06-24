#!/usr/bin/env python3

from app.constants import MAX_OVERS, TARGET_RUNS
from app.resources.stochastic_schemes import RandomSampling, RouletteSelection
from app.resources import Scorecard, Commentary
from app.models import Player
import six
import traceback


class GamePlay(object):
    """
    A class to emulate or execute a run chase of a cricket game.
    Maintains a scoreboard, and ball-by-ball commentary of the game.
    """

    def __init__(self, batsmen_list, random_gen_class=None):
        assert (batsmen_list and
                isinstance(batsmen_list, list) and
                len(batsmen_list) >= 2 and
                all([isinstance(player, Player) for player in batsmen_list]))
        assert random_gen_class is None or isinstance(random_gen_class, str)

        self.batting_lineup = batsmen_list
        self.commentary = Commentary()
        self.scorecard = Scorecard()
        self.Scoring_Strategy = self._resolve_strategy(random_gen_class)

    @classmethod
    def _resolve_strategy(cls, random_gen_class):
        """
        Resolve which class of Random Score Generator to use
        :param random_gen_class: either None or a string
        :return: a class type object, either RandomSampling or RouletteSelection
        """

        if random_gen_class is None:
            return RandomSampling

        random_technique = str(random_gen_class).lower().strip()
        if random_technique == 'random sampling':
            return RandomSampling
        elif random_technique == 'roulette selection':
            return RouletteSelection
        else:
            raise Exception('Random Number Generator class cannot be resolved '
                            'with the given string: {}'.format(random_gen_class))

    def execute_run_chase(self):
        """
        When called, performs the run-chase in a cricketing sense.
        Builds a probability distribution mapping for generating random scores,
        based on the random generator class provided.
        """

        batsmen = iter(self.batting_lineup)

        striker = next(batsmen)
        non_striker = next(batsmen)

        probabilities_distribution_map = {

            striker.name: self.Scoring_Strategy(
                striker.scoring_probabilities
            ),

            non_striker.name: self.Scoring_Strategy(
                non_striker.scoring_probabilities
            )
        }

        # match trackers
        winner = None
        runs_scored, overs_bowled = 0, 0
        wickets_in_hand = len(self.batting_lineup) - 1

        try:
            ball_count = 0
            self.commentary.before_over_overview(MAX_OVERS - overs_bowled,
                                                 TARGET_RUNS - runs_scored,
                                                 wickets_in_hand)

            while (overs_bowled < MAX_OVERS and
                   wickets_in_hand > 0 and runs_scored < TARGET_RUNS):

                ball_count += 1
                score = probabilities_distribution_map[striker.name].get_score()

                self.commentary.per_ball_commentary(
                    overs_bowled, ball_count,
                    striker.name, score
                )

                if score == 'OUT':
                    # mark the current batsmen out
                    self.scorecard.mark_out(striker.name)

                    # <optional> remove the outgoing batsman from the prop-dist map
                    probabilities_distribution_map.pop(striker.name)

                    wickets_in_hand -= 1

                    # get the next batsman
                    striker = next(batsmen)

                    # add a new batsman on the scorecard
                    self.scorecard.add_player(striker.name)

                    # compute the distributed probabilities for the new batter
                    probabilities_distribution_map[striker.name] = \
                        self.Scoring_Strategy(striker.scoring_probabilities)
                else:
                    score = int(score)
                    runs_scored += score
                    self.scorecard.add_runs(striker.name, score)

                    if score % 2:
                        # swap the strike end
                        striker, non_striker = \
                            non_striker, striker
                    else:
                        # no change required in case of a dot ball or on 2,4,6 runs
                        pass

                if ball_count == 6:
                    # update the game trackers
                    overs_bowled += 1
                    ball_count = 0

                    # batsmen change the batting end; swap the positions
                    striker, non_striker = non_striker, striker

                    if overs_bowled < MAX_OVERS and runs_scored < TARGET_RUNS:
                        # add the summary statement
                        self.commentary.before_over_overview(
                            MAX_OVERS - overs_bowled,
                            TARGET_RUNS - runs_scored,
                            wickets_in_hand
                        )

            else:
                chase_successful = False
                if runs_scored >= TARGET_RUNS:
                    chase_successful = True
                    winner = 'Bengaluru'
                else:
                    winner = 'Chennai'

                self.commentary.match_result_summary(
                    chase_successful, winner,
                    abs(TARGET_RUNS-runs_scored),
                    wickets_in_hand,
                    ((MAX_OVERS-overs_bowled-1) * 6 + (6 - ball_count))
                )
        except StopIteration:
            # Bengaluru lost, no more batsmen left
            winner = 'Chennai'
            self.commentary.match_result_summary(
                False, winner, abs(TARGET_RUNS - runs_scored)
            )

        except Exception as e:
            print('An error occurred while executing the run chase: ', e)
            traceback.print_exc()
            raise e

        # print the match commentary and statistics
        self.scorecard.print_scorecard()
        self.commentary.print_match_commentary()

