from elote.competitors.base import BaseCompetitor


class EloCompetitor(BaseCompetitor):
    _base_rating = 400
    _k_factor = 32

    def __init__(self, initial_rating=400):
        """
        Elo rating is a rating system based on pairwise comparisons. Ratings are given to competitors based on their
        comparisons (bouts) with peers, in which they can win, lose or tie. The change in a players rating is scaled by
        the rating difference between them and their competitor.

        class vars:

         * _base_rating: defaults to 400.
         * _k_factor: tunes the speed of response to new information, higher is faster response. Default=32

        :param initial_rating: the initial rating to use for a new competitor who has no history.  Default 400
        """
        self.rating = initial_rating

    def __repr__(self):
        return '<EloCompetitor: %s>' % (self.__hash__())

    def __str__(self):
        return '<EloCompetitor>'

    def export_state(self):
        """
        Exports all information needed to re-create this competitor from scratch later on.

        :return: dictionary of kwargs and class-args to re-instantiate this object
        """
        return {
            "initial_rating": self.rating,
            "class_vars": {
                "_k_factor": self._k_factor,
                "_base_rating": self._base_rating
            }
        }

    @property
    def transformed_rating(self):
        return 10 ** (self.rating / self._base_rating)

    def expected_score(self, competitor):
        """
        In Elo rating, a player's expected score is their probability of winning plus half their probability of drawing.
        This is because in Elo rating a draw is not explicitly accounted for, but rather counted as half of a win and
        half of a loss. It can make the expected score a bit difficult to reason about, so be careful.

        :param competitor: another EloCompetitor to compare this competitor to.
        :return: likelihood to beat the passed competitor, as a float 0-1.
        """

        self.verify_competitor_types(competitor)

        return self.transformed_rating / (competitor.transformed_rating + self.transformed_rating)

    def beat(self, competitor):
        """
        takes in a competitor object that lost, updates both's scores.
        """

        self.verify_competitor_types(competitor)

        win_es = self.expected_score(competitor)
        lose_es = competitor.expected_score(self)

        # update the winner's rating
        self.rating = self.rating + self._k_factor * (1 - win_es)

        # update the loser's rating
        competitor.rating = competitor.rating + self._k_factor * (0 - lose_es)

    def tied(self, competitor):
        """

        :param competitor:
        :return:
        """

        self.verify_competitor_types(competitor)

        win_es = self.expected_score(competitor)
        lose_es = competitor.expected_score(self)

        # update the winner's rating
        self.rating = self.rating + self._k_factor * (0.5 - win_es)

        # update the loser's rating
        competitor.rating = competitor.rating + self._k_factor * (0.5 - lose_es)
