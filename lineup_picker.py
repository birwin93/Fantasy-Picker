from lineup import Lineup, LineupPlayer, LineupRules
from timer import Timer

# go through each player in players
	# go through each salary til salary_cap
		# cur_best_team = teams[salary]
		# if cur_best_team has position open
			# add player
		# else
			# try swapping player for each player of same position in cur_best_team
		# if teams[cur_best_team.salary].score < cur_best_team.score
			# teams[cur_best_team.salary] = cur_best_team.score

def choose_lineup(players, rules, timer):
	all_lineups = {}
	timer.start("create empty lineups")
	for current_salary in range(0, rules.salary_cap+1):
		all_lineups[current_salary] = Lineup(rules)
	timer.end("create empty lineups")
	timer.start("find all best lineups")
	for current_salary in range(0, rules.salary_cap+1):
		for player in players:
			for salary in all_lineups:
				best_lineup = all_lineups[salary].deepcopy()
				if not best_lineup.is_new_player(player):
					continue
				if best_lineup.is_position_open(player):
					best_lineup.add_player(player)
					update_lineup(all_lineups, best_lineup, rules)
				else:
					for swap_player in best_lineup.players_for_position(player):
						best_lineup.swap_player_for_player(player, swap_player)
						update_lineup(all_lineups, best_lineup, rules)
						best_lineup.swap_player_for_player(swap_player, player)
			lineup = all_lineups[1]
	timer.end("find all best lineups")
	timer.start("choose best lineup")
	max_score = 0
	max_lineup = None
	print "Done compiling: printing top scores for each:"
	for salaries in all_lineups:
		lineup = all_lineups[salaries]
		if max_score < lineup.score:
			max_score = lineup.score
			max_lineup = lineup
		print salaries, " ", lineup.salary, " ", lineup.score
	timer.end("choose best lineup")
	return max_lineup

def update_lineup(all_lineups, lineup, rules):
	if lineup.is_valid() and all_lineups[lineup.salary].score < lineup.score:
		print "New best score for salary ", lineup.salary, " is ", lineup.score
		all_lineups[lineup.salary] = lineup.deepcopy()

p1 = LineupPlayer("Billy", "QB", 10, 1)
p2 = LineupPlayer("Ben", "QB", 20, 1)
p3 = LineupPlayer("Bryan", "QB", 40, 1)
p4 = LineupPlayer("Biff", "QB", 10, 1)

p5 = LineupPlayer("Jeff", "RB", 25, 1)
p6 = LineupPlayer("Peter", "RB", 20, 1)
p7 = LineupPlayer("Craig", "RB", 10, 1)
p8 = LineupPlayer("Hype", "RB", 15, 1)
p9 = LineupPlayer("Poop", "RB", 5, 1)
p10 = LineupPlayer("Max", "RB", 40, 1)

p11 = LineupPlayer("Evan", "WR", 40, 1)
p12 = LineupPlayer("Matt", "WR", 21, 1)
p13 = LineupPlayer("Chris", "WR", 30, 1)
p14 = LineupPlayer("Ted", "WR", 30, 1)
p15 = LineupPlayer("Tommy", "WR", 20, 1)
p16 = LineupPlayer("Frank", "WR", 40, 1)

p17 = LineupPlayer("Tyler", "TE", 20, 1)
p18 = LineupPlayer("Kyle", "TE", 40, 1)
p19 = LineupPlayer("Joe", "TE", 50, 1)
p20 = LineupPlayer("Jimmy", "TE", 10, 1)

p21 = LineupPlayer("Mike", "D", 40, 4)
p22 = LineupPlayer("Nick", "D", 25, 1)
p23 = LineupPlayer("Lola", "D", 10, 1)
p24 = LineupPlayer("Luke", "D", 20, 1)

players = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24]
rules = LineupRules(1, 2, 2, 1, 1, 1, 8)

timer = Timer()
timer.start("Total")
lineup = choose_lineup(players, rules, timer)
print "Done\n\n"
print lineup.players
print lineup.salary
print lineup.score
timer.end("Total")
timer.print_times()
