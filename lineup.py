class LineupRules(object):
	def __init__(self, num_qbs, num_rbs, num_wrs, num_tes, num_ds, num_flex, salary_cap):
		self.num_qbs = num_qbs
		self.num_rbs = num_rbs
		self.num_wrs = num_wrs
		self.num_tes = num_tes
		self.num_ds = num_ds
		self.num_flex = num_flex
		self.salary_cap = salary_cap
		self.positions = { "QB" : num_qbs, "RB" : num_rbs, "WR" : num_wrs, "TE" : num_tes, "D" : num_ds, "FLEX" : num_flex }

class LineupPlayer(object):
	def __init__(self, player_name, position, score, salary):
		self.player_name = player_name
		self.position = position
		self.score = score
		self.salary = salary
		self.player_id = "{}-{}-{}-{}".format(self.player_name, self.position, self.score, self.salary)

	def is_flex(self):
		return self.position == "RB" or self.position == "WR" or self.position == "TE"

	def __str__(self):
		return self.player_id

class Lineup(object):
	def __init__(self, rules):
		self.qbs = {}
		self.rbs = {}
		self.wrs = {}
		self.tes = {}
		self.ds = {}
		self.salary = 0
		self.score = 0
		self.rules = rules
		self.players = { "QB" : self.qbs, "RB" : self.rbs, "WR" : self.wrs, "TE" : self.tes, "D" : self.ds }

	def add_player(self, player):
		if self.is_new_player(player):
			self.players[player.position][player.player_id] = player
			self.salary += player.salary
			self.score += player.score

	def swap_player_for_player(self, in_player, out_player):
		self.players[out_player.position].pop(out_player.player_id)
		self.players[in_player.position][in_player.player_id] = in_player
		self.salary += in_player.salary - out_player.salary
		self.score += in_player.score - out_player.score
		return out_player

	def is_position_open(self, player):
		position_not_full = len(self.players[player.position]) < self.rules.positions[player.position]
		if position_not_full:
			return True
		if player.is_flex():
			num_rbs = len(self.players["RB"])
			num_wrs = len(self.players["WR"])
			num_tes = len(self.players["TE"])
			# if other flex positions aren't using flex, and current position isn't over flex count, add to flex
			if player.position == "RB":
				return num_wrs < self.rules.num_wrs and num_tes < self.rules.num_tes and num_rbs < self.rules.num_rbs + self.rules.num_flex
			if player.position == "WR":
				return num_rbs < self.rules.num_rbs and num_tes < self.rules.num_tes and num_wrs < self.rules.num_wrs + self.rules.num_flex
			if player.position == "TE":
				return num_wrs < self.rules.num_wrs and num_rbs < self.rules.num_rbs and num_tes < self.rules.num_tes + self.rules.num_flex

		return False

	def is_new_player(self, player):
		return player.player_id not in self.players[player.position]

	def can_afford_player(self, player):
		return self.salary + player.salary <= self.rules.salary_cap

	def players_for_position(self, player):
		if player.is_flex() and len(self.players[player.position]) < self.rules.positions[player.position] + self.rules.num_flex:
			return self.players["RB"].values() + self.players["WR"].values() + self.players["TE"].values()
		return self.players[player.position].values()

	def is_valid(self):
		if self.salary > self.rules.salary_cap:
			return False
		elif self.salary < self.rules.salary_cap:
			valid_qbs = len(self.qbs) <= self.rules.num_qbs
			valid_rbs = len(self.rbs) <= self.rules.num_rbs
			valid_wrs = len(self.wrs) <= self.rules.num_wrs
			valid_tes = len(self.tes) <= self.rules.num_tes
			valid_ds = len(self.ds) <= self.rules.num_ds
			valid_flex = True
			if not valid_rbs:
				valid_flex = valid_wrs and valid_tes
			elif not valid_wrs:
				valid_flex = valid_rbs and valid_tes
			elif not valid_tes:
				valid_flex = valid_rbs and valid_wrs
			return valid_qbs and valid_ds and valid_flex
		else:
			valid_qbs = len(self.qbs) == self.rules.num_qbs
			valid_rbs = len(self.rbs) == self.rules.num_rbs
			valid_wrs = len(self.wrs) == self.rules.num_wrs
			valid_tes = len(self.tes) == self.rules.num_tes
			valid_ds = len(self.ds) == self.rules.num_ds
			valid_flex_count = len(self.rbs) + len(self.wrs) + len(self.tes) == self.rules.num_rbs + self.rules.num_wrs + self.rules.num_tes + self.rules.num_flex
			valid_flex = (not valid_rbs and valid_wrs and valid_tes) or (not valid_wrs and valid_rbs and valid_tes) or (not valid_tes and valid_wrs and valid_rbs)
			return valid_qbs and valid_ds and valid_flex

	def deepcopy(self):
		lineup = Lineup(self.rules)
		lineup.qbs.update(self.qbs)
		lineup.rbs.update(self.rbs)
		lineup.wrs.update(self.wrs)
		lineup.tes.update(self.tes)
		lineup.ds.update(self.ds)
		lineup.salary = self.salary
		lineup.score = self.score
		return lineup
