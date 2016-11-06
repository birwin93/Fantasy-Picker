class BasePlayer(object):
    def __init__(self, game_scores):
        self.game_scores = game_scores
        self.total_score = sum(gs.score for gs in game_scores)
        self.average_score = self.total_score / len(game_scores)
    def scores_in_weeks(self, start, end):
        return self.game_scores[start-1:end-1]
    def average_score_in_weeks(self, start, end):
        scores = []
        for gs in self.scores_in_weeks(start, end):
            scores.append(gs.score)
        return sum(scores) / len(scores)

class Player(BasePlayer):
    def __init__(self, name, position, game_scores):
        super(Player, self).__init__(game_scores)
        self.name = name
        self.position = position

class Defense(BasePlayer):
    def __init__(self, team, rec_yds, rec_tds, rush_yds, rush_tds, game_scores):
        super(Defense, self).__init__(game_scores)
        self.team = team
        self.receiving_yds_allowed = rec_yds
        self.receiving_tds_allowed = rec_tds
        self.rushing_yds_allowed = rush_yds
        self.rushing_tds_allowed = rush_tds

class GameScore(object):
    def __init__(self, score, opponent):
        self.score = score
        self.opponent = opponent

class Position(object):
    def __init__(self, position, players):
        players.sort(key=lambda player: player.total_score, reverse=True)
        self.position = position
        self.players = players

    def mean(self, top=None):
        players = self.top_players(top)
        return sum(p.total_score for p in players) / len(players)

    def median(self, top=None):
        players = self.top_players(top)
        return players[len(players)/2].total_score

    def top_players(self, top):
        if top:
            return self.players[:top]
        else:
            return self.players

class LineupPlayer(object):
    def __init__(self, name, position, salary=None, score=None, opponent=None):
        self.name = name
        self.position = position
        self.score = score
        self.salary = salary
        self.opponent = opponent
        self.player_id = "{} {} {} {} {}".format(self.name, self.position, self.salary, self.score, self.opponent)
    def __str__(self):
        return self.player_id
    def is_flex(self):
        return self.position == "RB" or self.position == "WR" or self.position == "TE"
