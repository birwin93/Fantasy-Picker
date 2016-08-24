import nfldb

class LineupRules(object):
	def __init__(self, num_qbs, num_rbs, num_wrs, num_tes, num_ds, num_flex, salary_cap):
		self.num_qbs = num_qbs
		self.num_rbs = num_rbs
		self.num_wrs = num_wrs
		self.num_tes = num_tes
		self.num_ds = num_ds
		self.num_flex = self.num_flex
		self.salary_cap = salary_cap

class LineupPlayer(object):
	def __init__(self, player, score, salary):
		self.player = player
		self.score = score
		self.salary = salary

class Lineup(object):
	def __init__(self, qbs, rbs, wrs, tes, ds, salary):
		self.qbs = qbs
		self.rbs = rbs
		self.wrs = wrs
		self.tes = tes
		self.ds = ds
		self.salary = salary
	def add_qb(qb):
		self.qbs.append(qb)
		self.salary += qb.salary
	def add_rb(rb):
		self.rbs.append(rb)
		self.salary += rb.salary
	def add_wr(wr):
		self.wrs.append(wr)
		self.salary += wr.salary
	def add_te(te):
		self.tes.append(te)
		self.salary += te.salary
	def add_d(d):
		self.ds.append(d)
		self.salary += d.salary
	def copy():
		return Lineup(list(self.qbs), list(self.rbs), list(self.wrs), list(self.tes), list(self.ds), salary) 
	def empty():
		return Lineup({}, {}, {}, {}, {}, 0)
def choose_lineup(qbs, rbs, wrs, tes, ds, lineup, rules):
	if len(qbs) < rules.num_qbs:
	 	
