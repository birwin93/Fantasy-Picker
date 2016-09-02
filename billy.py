import nfldb
from score import Scorer
from timer import Timer

def get_all_player_data(years, weeks=None):
	db = nfldb.connect()
	q = nfldb.Query(db).game(season_year=years, season_type="Regular")
	if weeks:
		q.game(week=weeks)

	all_players = {}

	for game in q.as_games():

		# need to track all stats against defenese to get defensive scores
		game_players = { game.home_team : [], game.away_team : [] }

		# go through each play_player in the game
		for pp in game.play_players:

			# record play for player
			if pp.gsis_id in game_players:
				game_players[pp.gsis_id].append(pp)
			else:
				game_players[pp.gsis_id] = [pp]

			# record play against defense
			if pp.team in game_players:
				if pp.team == game.home_team:
					game_players[game.away_team].append(pp)
				else:
					game_players[game.home_team].append(pp)

		# now add game stats to each players overall stats
		for k in game_players:
			plays = game_players[k]
			if k in all_players:
				all_players[k].append(plays)
			else:
				all_players[k] = [plays]
	return all_players



# def sort_for_position(position):
# 	if position == "QB":
# 		return "passing_yds"
# 	elif position == "RB":
# 		return "rushing_yds"
# 	else:
# 		return "receiving_yds"

# def get_player_scores(position, years, weeks=None, top=None):
# 	q = get_game_query(years, weeks)
# 	if position != "ALL":
# 		q.player(position=position)
# 	scores = []
# 	scorer = score.Score(score.DRAFT_KINGS_SCORING, score.DRAFT_KINGS_BONUS)
# 	for pp in q.sort(sort_for_position(position)).as_aggregate():
# 		scores.append((pp.player, scorer.get_offense_score([pp])))
# 	return score.PositionScore(position, scores, True, top)
#
# def get_position_scores(positions, years, weeks=None, top=None):
# 	valid_positions = True
# 	position_scores = []
# 	for pos in positions:
# 		if pos in {"QB", "RB", "WR", "TE", "D", "ALL"}:
# 			start = time.time()
# 			pos_score = []
# 			if pos == "D":
# 				pos_score = get_team_scores(years, weeks, top)
# 			else:
# 				pos_score = get_player_scores(pos, years, weeks, top)
# 			position_scores.append(pos_score)
# 			print "Time to calculate {}: {} seconds".format(pos, time.time()-start)
# 		else:
# 			print "ERROR ", pos, " is not a position"
# 	start = time.time()
# 	all_scores = get_player_scores("ALL", years, weeks, top)
# 	print "Time to calculate {}: {} seconds".format("ALL", time.time()-start)
# 	return position_scores, all_scores


# defenses = get_defense_team_stats(2015)
# defenses.sort(key=lambda tup: tup.receiving_yds_allowed)
# for d in defenses:
# 	print d

res = get_all_player_data(2015, 1)
for k in res:
	print k, res[k]
