import file_reader
from lineup import LineupRules
import lineup_picker
from models import LineupPlayer, Player, Defense, Position

def calculate_for_weeks(all_players_data, all_defense_data, selected_week):
    players = file_reader.players_from_file('datasets/{}_2015.txt'.format(selected_week))
    actual_scores = {}
    lineup_players = []
    for p in players:
        actual_scores[p.name] = p.score
        if p.name in all_players_data:
            player = all_players_data[p.name]
            lineup_players.append(LineupPlayer(p.name, p.position, p.salary, player.average_score_in_weeks(1, selected_week)))
        if p.name in all_defense_data:
            defense = all_defense_data[p.name]
            lineup_players.append(LineupPlayer(p.name, p.position, p.salary, defense.average_score_in_weeks(1, selected_week)))

    rules = LineupRules(1, 2, 3, 1, 1, 1, 50000, 100)
    lineup = lineup_picker.choose_lineup(lineup_players, rules, 5)

    best_players = []
    for p in players:
        best_players.append(LineupPlayer(p.name, p.position, p.salary, p.score))
    best_lineup = lineup_picker.choose_lineup(best_players, rules, 5)

    actual_score = 0
    for p in lineup.qbs:
        actual_score += actual_scores[lineup.qbs[p].name]
        #print p
    for p in lineup.rbs:
        actual_score += actual_scores[lineup.rbs[p].name]
        #print p
    for p in lineup.wrs:
        actual_score += actual_scores[lineup.wrs[p].name]
        #print p
    for p in lineup.tes:
        actual_score += actual_scores[lineup.tes[p].name]
        #print p
    for p in lineup.ds:
        actual_score += actual_scores[lineup.ds[p].name]
        #print p
    #print lineup.salary
    print "Week", selected_week
    print "projected score:", lineup.score
    print "actual score:", actual_score
    print "best score:", best_lineup.score
    print ""
    print ""


print "Loading all player and defense data from files"
all_players, all_defenses = file_reader.load_all_players_from_file("data")

print "Organize data into positions"
position_players = { "QB" : [], "RB" : [], "WR" : [], "TE" : [] }
for k in all_players:
    player = all_players[k]
    if player.position in position_players:
        position_players[player.position].append(player)
position_players["DEF"] = all_defenses.values()

positions = {}
for pos in position_players:
    positions[pos] = Position(pos, position_players[pos])

for pos in positions:
    print pos
    print positions[pos].mean(), positions[pos].median()
    print positions[pos].mean(20), positions[pos].median(20)
    print positions[pos].mean(10), positions[pos].median(10)
    print ""
