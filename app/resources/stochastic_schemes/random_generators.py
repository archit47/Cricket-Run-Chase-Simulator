#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod
from collections import OrderedDict
import random
import time
import traceback


# system random object
SYSTEM_RANDOM = random.SystemRandom(int(time.time() * 1000))


class GenericRandomNumberGenerator(object):

    __metaclass__ = ABCMeta

    def __init__(self, scoring_probabilities):
        assert isinstance(scoring_probabilities, dict)

        self.scoring_probabilities = scoring_probabilities

        # convert the scoring probabilities of each player
        self.distributed_probabilities = self._compute_distributed_scores()

    @abstractmethod
    def _compute_distributed_scores(self):
        raise NotImplementedError

    @abstractmethod
    def get_score(self):
        raise NotImplementedError


class RandomSampling(GenericRandomNumberGenerator):

    def __init__(self, scoring_probabilities):
        super(RandomSampling, self).__init__(scoring_probabilities)
        self.lower_bound = 0
        self.upper_bound = len(self.distributed_probabilities)

    def _compute_distributed_scores(self):
        try:
            distributed_scores = []

            for score, frequency in self.scoring_probabilities.items():
                distributed_scores.extend([score] * int(frequency))

            return distributed_scores

        except Exception as e:
            print('An error occurred while computing distributed scoring '
                  'probabilities {}: {}'.format(self.scoring_probabilities, e))
            traceback.print_exc()
            raise e

    def get_score(self):
        # randomize the uniform distribution of scoring
        # and yes this still works, because list is shuffled `in-place`!
        random.shuffle(self.distributed_probabilities)

        # generate a random number b/w [0, 100)
        random_index = random.randint(self.lower_bound, self.upper_bound - 1)

        # (hopefully!) random score
        score = self.distributed_probabilities[random_index]

        return score


class RouletteSelection(GenericRandomNumberGenerator):

    def __init__(self, scoring_probabilities):
        super(RouletteSelection, self).__init__(scoring_probabilities)
        self.lower_bound = 0
        # set upper bound to the cumulative sum of the weights
        self.upper_bound = self.distributed_probabilities.values()[-1]

    def _compute_distributed_scores(self):
        try:
            cumulative_probabilities = [0]
            distributed_scores = OrderedDict()

            for score, weights in self.scoring_probabilities.items():
                sum_so_far = cumulative_probabilities[-1]
                current_sum = weights + sum_so_far
                cumulative_probabilities.append(current_sum)
                distributed_scores[score] = current_sum

            return distributed_scores

        except Exception as e:
            print('An error occurred while computing distributed scoring '
                  'probabilities {}: {}'.format(self.scoring_probabilities, e))
            traceback.print_exc()
            raise e

    def get_score(self):

        # generate a random number b/w [0, 100]
        slot = random.randint(self.lower_bound, self.upper_bound)
        score = None

        # find the bucket
        for (score, probability_sum) in self.distributed_probabilities.items():
            if slot <= probability_sum:
                break

        return score

