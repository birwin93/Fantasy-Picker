import nfldb
from models import Player, Defense, GameScore
from progressbar import ProgressBar, ETA, Bar
from score import Scorer

class GameDefense(object):
    def __init__(self, team, stats_against, score):
        self.team = team
        self.stats_against = stats_against
        self.score = score

def append_to_arr_dict(arr_dict, k, v):
    if k in arr_dict:
        arr_dict[k].append(v)
    else:
        arr_dict[k] = [v]

def get_all_offensive_player_data(scorer, years, weeks=None):
    print "Loading all data for players"
    pbar = ProgressBar(widgets=[ETA(), Bar()])
    db = nfldb.connect()
    q = nfldb.Query(db).game(season_year=years, season_type="Regular")
    if weeks:
        q.game(week=weeks)
    all_player_data = {}
    all_players = {}
    for game in pbar(q.as_games()):
        game_players = {}
        # go through each play_player in the game
        for pp in game.play_players:
            # record play for player
            append_to_arr_dict(game_players, pp.player_id, pp)
            all_players[pp.player_id] = pp.player

        # now add game stats to each players overall stats
        for player_id in game_players:
            plays_aggregate = nfldb.aggregate(game_players[player_id])
            player = all_players[player_id]
            score = scorer.get_offense_score(plays_aggregate)
            if player.team == game.home_team:
                append_to_arr_dict(all_player_data, player_id, GameScore(score, game.away_team))
            else:
                append_to_arr_dict(all_player_data, player_id, GameScore(score, game.home_team))

    # go through all stats and calculate scores for each game
    processed_players = {}
    for player_id in all_players:
        player = all_players[player_id]
        game_scores = all_player_data[player_id]
        processed_players[player.full_name] = Player(player.full_name, player.position, game_scores)
    return processed_players

def get_all_defensive_data(scorer, years, weeks=None):
    print "Loading all data for defenses"
    pbar = ProgressBar(widgets=[ETA(), Bar()])
    db = nfldb.connect()
    q = nfldb.Query(db).game(season_year=years, season_type="Regular")
    if weeks:
        q.game(week=weeks)
    all_defenses = {}
    for game in pbar(q.as_games()):
        game_defenses = {}
        # go through each play in game
        for pp in game.play_players:
            append_to_arr_dict(game_defenses, pp.team, pp)
        home_team_stats = game_defenses[game.home_team]
        away_team_stats = game_defenses[game.away_team]
        home_score = scorer.get_defense_score(home_team_stats, game.away_score)
        away_score = scorer.get_defense_score(away_team_stats, game.home_score)
        home_team = GameDefense(game.home_team, away_team_stats, GameScore(home_score, game.away_team))
        away_team = GameDefense(game.away_team, home_team_stats, GameScore(away_score, game.home_team))
        append_to_arr_dict(all_defenses, game.home_team, home_team)
        append_to_arr_dict(all_defenses, game.away_team, away_team)

    # calculate score for each defense by game
    defenses = {}
    for team in all_defenses:
        defense_data = all_defenses[team]
        scores = []
        receiving_yds_allowed = 0
        receiving_tds_allowed = 0
        rushing_yds_allowed = 0
        rushing_tds_allowed = 0
        for game_defense in defense_data:
            scores.append(game_defense.score)
            for pp in game_defense.stats_against:
                receiving_yds_allowed += pp.receiving_yds
                receiving_tds_allowed += pp.receiving_tds
                rushing_yds_allowed += pp.rushing_yds
                rushing_tds_allowed += pp.rushing_tds
        defenses[team] = Defense(team, receiving_yds_allowed, receiving_tds_allowed, rushing_yds_allowed, rushing_tds_allowed, scores)
    return defenses

def run_offense(years, weeks=None):
    scorer = Scorer.draft_kings()
    players = get_all_offensive_player_data(scorer, years, weeks)
    for k in players:
        print p.name, k, p.total_score

def run_defense(years, weeks=None):
    scorer = Scorer.draft_kings()
    defenses = get_all_defensive_data(scorer, years, weeks)
    for p in defenses:
        defense = defenses[p]
        print defense.team, defense.total_score, defense.receiving_yds_allowed, defense.receiving_tds_allowed, defense.rushing_yds_allowed, defense.rushing_tds_allowed
