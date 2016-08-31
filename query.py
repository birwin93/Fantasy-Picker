import nfldb
import score
import time

def get_game_query(years, weeks):
	db = nfldb.connect()
	q = nfldb.Query(db).game(season_year=years, season_type="Regular")
	if weeks:
		q.game(week=weeks)
	return q

