from models import LineupPlayer, Player, Defense, GameScore
import fetch_data
from score import Scorer

def format_position(position):
    if position == "Def":
        return "DEF"
    return position

def format_name(name):
    parts = name.split(", ")
    return parts[1] + " " + parts[0]

team_mapping = {
    'sfo' : 'SF',
    'sdg' : 'SD',
    'lar' : 'STL',
    'gnb' : 'GB',
    'nor' : 'NO',
    'kan' : 'KC',
    'nwe' : 'NE',
    'tam' : 'TB'
}

def format_team(team):
    if team in team_mapping:
        return team_mapping[team]
    else:
        return team.upper()

def isint(value):
  try:
    int(value)
    return True
  except:
    return False

def players_from_file(filename):
    players = []
    file = open(filename)
    for line in file.readlines():
        data = line.split(";")
        if isint(data[9]):
            position = format_position(data[4])
            if position == "DEF":
                name = format_team(data[5])
            else:
                name = format_name(data[3])
            players.append(LineupPlayer(name, position, int(data[9]), float(data[8]), format_team(data[7])))
    return players

def write_all_data_to_file(filename, scorer, years, weeks=None):
    players = fetch_data.get_all_offensive_player_data(scorer, years, weeks)
    file = open("player_"+filename+".txt", 'w')
    for k in players:
        player = players[k]
        scores = ",".join("{}:{}".format(gs.score, gs.opponent) for gs in player.game_scores)
        player_str = "{},{},{}".format(player.name, player.position, scores)
        file.write(player_str + "\n")
    file.close()

    defenses = fetch_data.get_all_defensive_data(scorer, years, weeks)
    file = open("defense_"+filename+".txt", 'w')
    for k in defenses:
        d = defenses[k]
        scores = ",".join("{}:{}".format(gs.score, gs.opponent) for gs in d.game_scores)
        defense_str = "{},{},{},{},{},{}".format(d.team, d.receiving_yds_allowed, d.receiving_tds_allowed, d.rushing_yds_allowed, d.rushing_tds_allowed, scores)
        file.write(defense_str + "\n")
    file.close()

def load_all_players_from_file(filename):
    players = {}
    file = open("player_"+filename+".txt")
    for line in file.readlines():
        data = line.split(",")
        game_scores = []
        for gs in data[2:]:
            parts = gs.split(":")
            game_scores.append(GameScore(float(parts[0]), parts[1]))
        player = Player(data[0], data[1], game_scores)
        players[player.name] = player
    defenses = {}
    file = open("defense_"+filename+".txt")
    for line in file.readlines():
        data = line.split(",")
        game_scores = []
        for gs in data[5:]:
            parts = gs.split(":")
            game_scores.append(GameScore(float(parts[0]), parts[1]))
            defense = Defense(data[0], data[1], data[2], data[3], data[4], game_scores)
        defenses[defense.team] = defense
    return players, defenses
