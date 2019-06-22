from app.constants import SCORE_KEYS


class Player(object):
    """
    To represent instances of each player, storing their name
    and their scoring probabilities
    """

    def __init__(self, name, scoring_probabilities):
        assert name is not None and isinstance(name, str)
        assert isinstance(scoring_probabilities, dict)

        self.name = name.strip()
        self.__scoring_probabilities = scoring_probabilities

        # validation
        self._validate_scoring_probabilities()

    def _validate_scoring_probabilities(self):
        """
        Check if the scoring probabilities provided conform to the expectations
        :return: raise an Exception only if scoring probabilities are invalid
        """

        given_keys = self.__scoring_probabilities.keys()
        given_weights = self.__scoring_probabilities.values()

        if set(given_keys) != set(SCORE_KEYS) or sum(given_weights) != 100:
            raise Exception('Invalid scoring probabilities provided')

    def _get_scoring_probabilities(self):
        return self.__scoring_probabilities

    def __str__(self):
        return self.name

    # sort-of read-only properties
    scoring_probabilities = property(_get_scoring_probabilities)

