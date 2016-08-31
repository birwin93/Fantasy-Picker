import nfldb

db = nfldb.connect()
DRAFT_KINGS_SCORING = {
    "fumbles_lost": -1,
    "fumbles_rec_tds": 6,
    "kicking_rec_tds": 6,
    "kickret_tds": 6,
    "passing_int": -1,
    "passing_tds": 4,
    "passing_twoptm": 2,
    "passing_yds": 0.04,
    "puntret_tds": 6,
    "receiving_rec": 1,
    "receiving_tds": 6,
    "receiving_twoptm": 2, 
    "receiving_yds": 0.1,
    "rushing_tds": 6,
    "rushing_twoptm": 2,
    "rushing_yds": 0.1,
}

DRAFT_KINGS_BONUS = {
    "passing_yds": 300,
    "receiving_yds": 100,
    "rushing_yds": 100,
}

class Score(object):
    BONUS_POINTS = 3

    def __init__(self, aggregate, scoring, bonus):
        self.aggregate = aggregate
        self.scoring = scoring
        self.bonus = bonus

    def get_score(self):
        return self._get_standard_score() + self._get_bonus_score()

    def _get_standard_score(self):
        s = 0
        for name, scoring in self.scoring.iteritems():
            s += getattr(self.aggregate, name, 0) * scoring
        return s

    def _get_bonus_score(self):
        b = 0
        for name, minimum in self.bonus.iteritems():
            if getattr(self.aggregate, name, 0) >= minimum:
                b += self.BONUS_POINTS
        return b


