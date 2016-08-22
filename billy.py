import nfldb
import score

def get_game_query(years, weeks):
	db = nfldb.connect()
	q = nfldb.Query(db).game(season_year=years)
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

def get_player_scores(position, years, weeks=None, top=None):
	q = get_game_query(years, weeks)
	if position != "ALL":
		q.player(position=position)
	scores = []
	scorer = score.Score(score.DRAFT_KINGS_SCORING, score.DRAFT_KINGS_BONUS)
	for pp in q.as_aggregate():
		scores.append((pp.player, scorer.get_offense_score([pp])))
	return score.PositionScore(position, scores, True, top)

def get_position_scores(positions, years, weeks=None, top=None):
	valid_positions = True
	position_scores = []
	for pos in positions:
		if pos in {"QB", "RB", "WR", "TE", "D", "ALL"}:
			pos_score = []
			if pos == "D":
				pos_score = get_team_scores(years, weeks, top)
			else:
				pos_score = get_player_scores(pos, years, weeks, top)
			position_scores.append(pos_score)
		else:
			print "ERROR ", pos, " is not a position"
	all_scores = get_player_scores("ALL", years, weeks, top)
	return position_scores, all_scores 


def print_query(pos, years, weeks=None, top=None):
	pos_scores, all_scores = get_position_scores(pos, years, weeks, top)
	for pos_score in pos_scores:
		print pos_score
		print ""
	print all_scores


print_query(["QB", "RB", "WR", "TE", "D"], 2015, None, 15)




