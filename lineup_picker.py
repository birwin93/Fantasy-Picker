from lineup import Lineup, LineupPlayer, LineupRules
from timer import Timer

# go through each salary til salary_cap
	# go through each player in players
		# cur_best_team = copy of teams[salary]
		# if cur_best_team has position open
			# add player
		# else
			# try swapping player for each player of same position in cur_best_team
		# if teams[cur_best_team.salary].score < cur_best_team.score
			# teams[cur_best_team.salary] = cur_best_team.score

def choose_lineup(players, rules, min_score):
	print "Began choosing best lineup from {} players for {} salary cap".format(len(players), rules.salary_cap)
	all_lineups = {}
	for current_salary in range(0, rules.salary_cap+1, rules.salary_step_size):
		all_lineups[current_salary] = Lineup(rules)

	# remove players whose projected scores are too low
	filtered_players = [player for player in players if player.score > min_score]
	print "Filtered out {} players whose predicted score was beneath minumum of {}".format(len(players)-len(filtered_players), min_score)

	for current_salary in range(0, rules.salary_cap+1, rules.salary_step_size):
		for player in filtered_players:
			# create deep copy of current best lineup for salary since we edit it below
			best_lineup = all_lineups[current_salary].deepcopy()
			# only try and add player if not already in it
			if best_lineup.is_new_player(player):
				# if lineup has position open and can afford player
				if best_lineup.is_position_open(player) and best_lineup.can_afford_player(player):
					best_lineup.add_player(player)
					update_lineup(all_lineups, best_lineup, rules)
				else:
					# try swapping players of same position (or flex) for player
					for swap_player in best_lineup.players_for_position(player):
						best_lineup.swap_player_for_player(player, swap_player)
						# see if this swap is a better lineup
						update_lineup(all_lineups, best_lineup, rules)
						best_lineup.swap_player_for_player(swap_player, player)
	max_score = 0
	max_lineup = None
	for salaries in all_lineups:
		lineup = all_lineups[salaries]
		if max_score < lineup.score:
			max_score = lineup.score
			max_lineup = lineup
		print salaries, " ", lineup.salary, " ", lineup.score
	return max_lineup

def update_lineup(all_lineups, lineup, rules):
	if lineup.is_valid() and all_lineups[lineup.salary].score < lineup.score:
		all_lineups[lineup.salary] = lineup.deepcopy()


def format_position(position):
	if position == "Def":
		return "D"
	return position

def isint(value):
  try:
    int(value)
    return True
  except:
    return False

# p1 = LineupPlayer("Billy", "QB", 10, 1)
# p2 = LineupPlayer("Ben", "QB", 20, 2)
# p3 = LineupPlayer("Bryan", "QB", 40, 4)
# p4 = LineupPlayer("Biff", "QB", 10, 2)
#
# p5 = LineupPlayer("Jeff", "RB", 25, 2)
# p6 = LineupPlayer("Peter", "RB", 20, 1)
# p7 = LineupPlayer("Craig", "RB", 10, 1)
# p8 = LineupPlayer("Hype", "RB", 15, 1)
# p9 = LineupPlayer("Poop", "RB", 5, 1)
# p10 = LineupPlayer("Max", "RB", 40, 3)
#
# p11 = LineupPlayer("Evan", "WR", 40, 3)
# p12 = LineupPlayer("Matt", "WR", 21, 2)
# p13 = LineupPlayer("Chris", "WR", 30, 1)
# p14 = LineupPlayer("Ted", "WR", 30, 1)
# p15 = LineupPlayer("Tommy", "WR", 20, 1)
# p16 = LineupPlayer("Frank", "WR", 40, 2)
#
# p17 = LineupPlayer("Tyler", "TE", 20, 1)
# p18 = LineupPlayer("Kyle", "TE", 40, 3)
# p19 = LineupPlayer("Joe", "TE", 50, 4)
# p20 = LineupPlayer("Jimmy", "TE", 10, 1)
#
# p21 = LineupPlayer("Mike", "D", 25, 2)
# p22 = LineupPlayer("Nick", "D", 25, 1)
# p23 = LineupPlayer("Lola", "D", 10, 1)
# p24 = LineupPlayer("Luke", "D", 20, 1)
#
# players = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24]
# players = players * 80

players = []
file = open("datasets/2015_12_data.txt")
for line in file.readlines():
	data = line.split(";")
	if isint(data[9]):
		players.append(LineupPlayer(data[3], format_position(data[4]), float(data[8]), int(data[9])))
for player in players:
	print player.player_id

rules = LineupRules(1, 2, 3, 1, 1, 1, 50000, 100)

timer = Timer()
timer.start("Total")
lineup = choose_lineup(players, rules, 0)
timer.end("Total")
print "Done\n\n"
timer.print_times()
print "\n\n"
print lineup.players
print lineup.salary
print lineup.score
