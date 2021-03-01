import pandas as pd
import calendar
import tabulate
import urllib.request, json 
from datetime import datetime
from nba_api.stats.endpoints import leagueleaders, leaguestandings
from nba_api.stats.static import players

def perGame(): 
    data = leagueleaders.LeagueLeaders() 
    df = data.league_leaders.get_data_frame()
    was, stats = df[df.TEAM == 'WAS'], ['PTS', 'REB', 'AST', 'STL']
    wash_per = was[stats].div(was['GP'], axis=0).round(1)
    wash_per = pd.concat([was['PLAYER'], wash_per], axis=1)
    wash_per.PLAYER = wash_per.PLAYER.str.split(n=1).str[1]
    wash_per = wash_per.set_index('PLAYER')
    return wash_per.to_markdown(floatfmt=".1f")

perGame = perGame()


class GameStat:
    def __init__(self, date, time, team, score, outcome):
        self.date = date
        self.time = time
        self.team = team
        self.score = score
        self.outcome = outcome

def homeWon(wiz, opp, schedule):
    schedule['score'] = wiz + "-" + opp
    if not wiz or not opp:
        schedule['score'] = ''
    elif float(wiz) > float(opp):
        schedule['score'] = 'W ' + schedule['score']
    elif float(wiz) < float(opp):
        schedule['score'] = 'L ' + schedule['score']

def schedule(): 
    curr_month = calendar.month_name[datetime.now().month]
    # curr_month = 'February'
    with urllib.request.urlopen("http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2020/league/00_full_schedule.json") as url:
        data = json.loads(url.read().decode())
    curr_month_games = [s['mscd']['g'] for s in data['lscd'] if s['mscd']['mon'] == curr_month]
    lst = []
    for game in curr_month_games[0]:
        if 'WAS' in (game['gcode']):
            schedule = {}
            home = True if 'WAS' == game['h']['ta'] else False
            if home:
                homeWon(game['h']['s'], game['v']['s'], schedule)
                schedule['team'] = "vs " + game['v']['ta']
            else:
                homeWon(game['v']['s'], game['h']['s'], schedule)
                schedule['team'] = "@ " + game['h']['ta']
            schedule['date'] = pd.to_datetime(game['gdte'])
            schedule['time'] = game['stt']
            lst.append(schedule)
    df = pd.DataFrame(lst)[['date', 'time', 'team', 'score']]
    df.columns = map(str.title, df.columns)
    # reformat date and time
    df.Date = df.Date.dt.strftime('%b %d')
    # df.Time = df.Time.str.slice(stop=-3)
    return df.set_index('Date').to_markdown()

schedule = schedule()


def standings():
    sta = leaguestandings.LeagueStandings() 
    df = sta.standings.get_data_frame()
    df = df[df.Conference == 'East'][['TeamCity', 'WINS', 'LOSSES', 'WinPCT', 'L10']]
    df.columns = ['Team', 'W', 'L', 'PCT', 'L10']
    df.PCT = df.PCT.round(2)
    df = df.set_index('Team').reset_index()
    df.index.name = '#'
    return df.to_markdown()

standings = standings()



# if __name__ == "__main__":
#     print(schedule)
#         # print(game['gcode'][-6:-3], game['gcode'][-3:], game['etm'])

#         curr_month_games = s['mscd']['g'] if s['mscd']['mon'] == curr_month
        
#         for s in data['lscd'] if s['mscd']['mon'] == curr_month][0]


# [s['mscd']['g'] for s in data['lscd'] if s['mscd']['mon'] == curr_month][0]

# reddit = praw.Reddit(
#     client_id="CLIENT_ID",
#     client_secret="CLIENT_SECRET",
#     password="Active8848!",
#     user_agent="USERAGENT",
#     username="windsandtime",
# )

# r = praw.Reddit('r/redsox score bot u/furuta v0.1')
# r.login('username','password') #must be mod of /r/redsox
# r.get_subreddit('redsox').update_settings(description='SIDEBARTEXT');


# https://www.playingnumbers.com/2019/12/how-to-get-nba-data-using-the-nba_api-python-module-beginner/