import nfldb
import query

class Defenses(object):
    	def __init__(self, years, weeks=None):
        	defenses = get_defense_team_stats(years, weeks)

def get_defense_team_stats(years, weeks=None):
    	q = query.get_game_query(years, weeks)
   	defenses = {}
	for game in q.as_games():
		if game.home_team not in defenses:
			defenses[game.home_team] = []
		if game.away_team not in defenses:
			defenses[game.away_team] = []
		for pp in game.play_players:
			if pp.team == game.home_team:
				defenses[game.away_team].append(pp)
			else:
				defenses[game.home_team].append(pp)
	defenses_arr = []
	for k in defenses:
		defenses_arr.append(score.Defense(k, defenses[k]))
	return defenses_arr



