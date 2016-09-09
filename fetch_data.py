import nfldb
from score import Scorer
from timer import Timer

class PotentialPlayer(object):
	def __init__(self, player, scores):
		self.player_id = player.player_id
		self.name = player.full_name
		self.position = player.position
		self.scores = scores
		self.total_score = sum(scores)

class GameDefense(object):
	def __init__(self, team, stats_for, stats_against, points_allowed):
		self.team = team
		self.stats_for = stats_for
		self.stats_against = stats_against
		self.points_allowed = points_allowed

class Defense(object):
	def __init__(self, team, scores, stats_against):
		self.team = team
		self.scores = scores
		self.total_score = sum(scores)
		self.receiving_yds_allowed = 0
		self.receiving_tds_allowed = 0
		self.rushing_yds_allowed = 0
		self.rushing_tds_allowed = 0
		for pp in stats_against:
			self.receiving_yds_allowed += pp.receiving_yds
			self.receiving_tds_allowed += pp.receiving_tds
			self.rushing_yds_allowed += pp.rushing_yds
			self.rushing_tds_allowed += pp.rushing_tds

def append_to_arr_dict(arr_dict, k, v):
	if k in arr_dict:
		arr_dict[k].append(v)
	else:
		arr_dict[k] = [v]

def get_all_offensive_player_data(years, weeks=None):
	db = nfldb.connect()
	q = nfldb.Query(db).game(season_year=years, season_type="Regular")
	if weeks:
		q.game(week=weeks)
	all_player_data = {}
	all_players = {}
	total_games = 0
	for game in q.as_games():
		total_games += 1
		if total_games % 10 == 0:
			print "processed", total_games, "games"
		game_players = {}
		# go through each play_player in the game
		for pp in game.play_players:
			# record play for player
			append_to_arr_dict(game_players, pp.player_id, pp)
			all_players[pp.player_id] = pp.player

		# now add game stats to each players overall stats
		for player_id in game_players:
			plays_aggregate = nfldb.aggregate(game_players[player_id])
			append_to_arr_dict(all_player_data, player_id, plays_aggregate)
	return all_players, all_player_data

def process_all_offensive_player_data(players, player_data, scorer):
	processed_players = []
	for player_id in players:
		player = players[player_id]
		data = player_data[player_id]
		scores = []
		for game_data in data:
			scores.append(scorer.get_offense_score(game_data))
		processed_players.append(PotentialPlayer(player, scores))
	return processed_players

def get_all_defensive_data(years, weeks=None):
	db = nfldb.connect()
	q = nfldb.Query(db).game(season_year=years, season_type="Regular")
	if weeks:
		q.game(week=weeks)
	all_defenses = {}
	for game in q.as_games():
		game_defenses = {}
		# go through each play in game
		for pp in game.play_players:
			append_to_arr_dict(game_defenses, pp.team, pp)
		home_team_stats = game_defenses[game.home_team]
		away_team_stats = game_defenses[game.away_team]
		home_team = GameDefense(game.home_team, home_team_stats, away_team_stats, game.away_score)
		away_team = GameDefense(game.home_team, away_team_stats, home_team_stats, game.home_score)
		append_to_arr_dict(all_defenses, game.home_team, home_team)
		append_to_arr_dict(all_defenses, game.away_team, away_team)
	return all_defenses

def process_defenses_data(defenses_data, scorer):
	defenses = {}
	for team in defenses_data:
		defense_data = defenses_data[team]
		scores = []
		all_stats_against = []
		for game_defense in defense_data:
			scores.append(scorer.get_defense_score(game_defense.stats_for, game_defense.points_allowed))
			for pp in game_defense.stats_against:
				all_stats_against.append(pp)
		defenses[team] = Defense(team, scores, all_stats_against)
	return defenses

def get_all_scores(scorer, years, weeks=None):
	all_players, all_player_data = get_all_offensive_player_data(years, weeks)
	all_defense_data = get_all_defensive_data(years, weeks)
	players = process_all_offensive_player_data(all_players, all_player_data, scorer)
	defenses = process_defenses_data(all_defense_data, scorer)
	return players, defenses

def run_offense(years, weeks=None):
	all_players, all_player_data = get_all_offensive_player_data(years, weeks)
	scorer = Scorer.draft_kings()
	players = process_all_offensive_player_data(all_players, all_player_data, scorer)
	players.sort(key=lambda player: player.total_score, reverse=True)
	for p in players[:10]:
		print p.name, p.player_id, p.total_score, p.scores

def run_defense(years, weeks=None):
	all_defense_data = get_all_defensive_data(years, weeks)
	scorer = Scorer.draft_kings()
	defenses = process_defenses_data(all_defense_data, scorer)
	for p in defenses:
		defense = defenses[p]
		print defense.team, defense.total_score, defense.receiving_yds_allowed, defense.receiving_tds_allowed, defense.rushing_yds_allowed, defense.rushing_tds_allowed

run_offense(2015)
run_defense(2015)
