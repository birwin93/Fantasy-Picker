
DRAFT_KINGS_SCORING = {
    "offense": {
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
    },
    "defense": {
        "defense_frec": 2,
        "defense_int": 2,
        "defense_puntblk": 0,
        "defense_safe": 2,
        "defense_sk": 1,
        "defense_xpblk": 2,
        "defense_frec_tds": 6,
        "defense_int_tds": 6,
        "defense_fgblk": 2,
    },
}

DRAFT_KINGS_BONUS = {
    "offense_bonus_points": 3,
    "offense": {
        "passing_yds": 300,
        "receiving_yds": 100,
        "rushing_yds": 100,
    },
    "defense_bonus_points": 0,
    "defense": {
        "ranges": [
            {
                "points_scored": [0],
                "added_points": 10,
            },
            {
                "points_scored": [1, 2, 3, 4, 5, 6],
                "added_points": 7,
            },
            {
                "points_scored": [7, 8, 9, 10, 11, 12, 13],
                "added_points": 4,
            },
            {
                "points_scored": [14, 15, 16, 17, 18, 19, 20],
                "added_points": 1,
            },
            {
                "points_scored": [21, 22, 23, 24, 25, 26, 27],
                "added_points": 0,
            },
            {
                "points_scored": [28, 29, 30, 31, 32, 33, 34],
                "added_points": -1,
            },
        ],
        "max_points_given_points": -4,
    },
}

class PositionScore(object):
	def __init__(self, position, scores, sort=False, top=None):
		if sort:
			scores.sort(key=lambda tup: tup[1], reverse=True)
		if top:
			scores = scores[:top]
		self.position = position
		self.scores = scores
		self.median = scores[len(scores)/2][1]
		self.mean = sum(s for p,s in scores) / len(scores)
	
	def __str__(self):
		ret_str = ""
		for p, s in self.scores:
			ret_str = ret_str + "{} {}\n".format(p, s)
		ret_str = ret_str + "mean: {}\n".format(self.mean)
		ret_str = ret_str + "median: {}\n".format(self.median)
		return ret_str

		

class Score(object):
    TYPE_OFFENSE = "offense"
    TYPE_DEFENSE = "defense"

    def __init__(self,  scoring, bonus):
        self.scoring = scoring
        self.bonus = bonus

    def get_offense_score(self, aggregate):
        return self.get_offense_score([aggregate])
    
    def get_offense_score(self, aggregate_list):
        score = 0
        score_type = self.TYPE_OFFENSE
        for aggregate in aggregate_list:
            score += self._get_standard_score(aggregate, score_type) + self._get_bonus_score(aggregate, score_type)
        return score

    def get_defense_score(self, aggregate_list, points_allowed):
        score = self._get_defensive_starting_score(points_allowed)
        score_type = self.TYPE_DEFENSE
        for aggregate in aggregate_list:
            score += self._get_standard_score(aggregate, score_type) + self._get_bonus_score(aggregate, score_type)
        return score

    def _get_standard_score(self, aggregate, score_type):
        s = 0
        scoring = self.scoring[score_type]
        for name, score in scoring.iteritems():
            s += getattr(aggregate, name, 0) * score
        return s

    def _get_bonus_score(self, aggregate, score_type):
        b = 0
        for name, minimum in self.bonus.iteritems():
            if getattr(aggregate, name, 0) >= minimum:
                b += self._number_of_bonus_points(score_type)
        return b

    def _get_defensive_starting_score(self, points_allowed):
         ranges = self.bonus["defense"]["ranges"]
         for r in ranges:
             if points_allowed in r["points_scored"]:
                 return r["added_points"]
         return self.bonus["defense"]["max_points_given_points"]

    def _number_of_bonus_points(self, score_type):
        if score_type == self.TYPE_OFFENSE:
            return self.bonus["offense_bonus_points"]
        elif score_type == self.TYPE_DEFENSE:
            return self.bonus["defense_bonus_points"]
        return 0




