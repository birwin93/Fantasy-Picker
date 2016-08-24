import nfldb
import score
import time

def get_game_query(years, weeks):
	db = nfldb.connect()
	q = nfldb.Query(db).game(season_year=years, season_type="Regular")
	if weeks:
		q.game(week=weeks)
	return q

def get_team_scores(years, weeks=None, top=None):
	q = get_game_query(years, weeks)
	scorer = score.Score(score.DRAFT_KINGS_SCORING, score.DRAFT_KINGS_BONUS)
	scores = {}
	for game in q.as_games():
		team_pps = {}
		team_pps[game.home_team] = []
		team_pps[game.away_team] = []
		for pp in game.play_players:
			if pp.team in team_pps:
				team_pps[pp.team].append(pp)
		home_score = scorer.get_defense_score(team_pps[game.home_team], game.away_score)
		away_score = scorer.get_defense_score(team_pps[game.away_team], game.home_score)		
		scores[game.home_team] = scores.get(game.home_team, 0) + home_score
		scores[game.away_team] = scores.get(game.away_team, 0) + away_score
	scores_arr = []
	for k in scores:
		scores_arr.append((k, scores[k]))
	return score.PositionScore("D", scores_arr, False, top)

def get_defense_team_stats(years, weeks=None):
	q = get_game_query(years, weeks)
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


def sort_for_position(position):
	if position == "QB":
		return "passing_yds"
	elif position == "RB":
		return "rushing_yds"
	else:
		return "receiving_yds"

def get_player_scores(position, years, weeks=None, top=None):
	q = get_game_query(years, weeks)
	if position != "ALL":
		q.player(position=position)
	scores = []
	scorer = score.Score(score.DRAFT_KINGS_SCORING, score.DRAFT_KINGS_BONUS)
	for pp in q.sort(sort_for_position(position)).as_aggregate():
		scores.append((pp.player, scorer.get_offense_score([pp])))
	return score.PositionScore(position, scores, True, top)

def get_position_scores(positions, years, weeks=None, top=None):
	valid_positions = True
	position_scores = []
	for pos in positions:
		if pos in {"QB", "RB", "WR", "TE", "D", "ALL"}:
			start = time.time()
			pos_score = []
			if pos == "D":
				pos_score = get_team_scores(years, weeks, top)
			else:
				pos_score = get_player_scores(pos, years, weeks, top)
			position_scores.append(pos_score)
			print "Time to calculate {}: {} seconds".format(pos, time.time()-start)
		else:
			print "ERROR ", pos, " is not a position"
	start = time.time()
	all_scores = get_player_scores("ALL", years, weeks, top)
	print "Time to calculate {}: {} seconds".format("ALL", time.time()-start)
	return position_scores, all_scores 


def print_query(pos, years, weeks=None, top=None):
	pos_scores, all_scores = get_position_scores(pos, years, weeks, top)
	for pos_score in pos_scores:
		print pos_score
		print ""
	print all_scores


#start = time.time()
#print_query(["QB", "RB", "WR", "TE", "D"], 2015, None, 15)
#end = time.time()
#print ""
#print "Time to calculate: {} seconds".format(end - start)

defenses = get_defense_team_stats(2015)
defenses.sort(key=lambda tup: tup.receiving_yds_allowed)
for d in defenses:
	print d

