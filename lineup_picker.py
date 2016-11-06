from lineup import Lineup, LineupPlayer, LineupRules
from progressbar import ProgressBar, ETA, Bar
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
    print "Choosing best lineup from {} players for {} salary cap".format(len(players), rules.salary_cap)
    pbar = ProgressBar(widgets=[Bar()])
    all_lineups = {}
    for current_salary in range(0, rules.salary_cap+1, rules.salary_step_size):
        all_lineups[current_salary] = Lineup(rules)

    # remove players whose projected scores are too low
    filtered_players = [player for player in players if player.score > min_score]

    for current_salary in pbar(range(0, rules.salary_cap+1, rules.salary_step_size)):
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
    return max_lineup

def update_lineup(all_lineups, lineup, rules):
    if lineup.is_valid() and all_lineups[lineup.salary].score < lineup.score:
        all_lineups[lineup.salary] = lineup.deepcopy()
