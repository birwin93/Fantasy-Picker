import nfldb
from score import Scorer
from timer import Timer

def get_all_offensive_player_data(years, weeks=None):
	db = nfldb.connect()
	q = nfldb.Query(db).game(season_year=years, season_type="Regular")
	if weeks:
		q.game(week=weeks)

	all_player_data = {}
	all_players = {}
	for game in q.as_games():

		# go through each play_player in the game
		for pp in game.play_players:

			# record play for player
			if pp.player in game_players:
				game_players[pp.player].append(pp)
			else:
				game_players[pp.player] = [pp]

			# record play against defense
			#if pp.team in game_players:
			#	if pp.team == game.home_team:
			#		game_players[game.away_team].append(pp)
			#	else:
			#		game_players[game.home_team].append(pp)

		# now add game stats to each players overall stats
		for player in game_players:
			plays = game_players[player]
			if player in all_player_data:
				all_player_data[player].append(plays)
			else:
				all_player_data[player] = [plays]
	return all_player_data

def process_all_offensive_player_data(players):
	scorer = Scorer.draft_kings()
	process_players = []
	for player in player:
		all_game_data = player[player]
		scores = []
		for game_data in all_game_data:
			scores.append(scorer.get_offensive_score(game_data))
		

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

all_players, all_player_data = get_all_player_data(2015, 1)
for k in res:
	print k
