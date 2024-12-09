import pandas as pd
import numpy as np
import calendar
import tabulate
import urllib.request, json 
from datetime import datetime
from tabulate import tabulate
from nba_api.stats.endpoints import leagueleaders, leaguestandings
from nba_api.stats.static import players

def perGame(): 
    data = leagueleaders.LeagueLeaders() 
    df = data.league_leaders.get_data_frame()
    was, stats = df[df.TEAM == 'WAS'], ['PTS', 'REB', 'AST', 'STL']
    wash_per = was[stats].div(was['GP'], axis=0).round(1)
    wash_per = pd.concat([was['PLAYER'], wash_per], axis=1)
    wash_per.PLAYER = wash_per.PLAYER.str.split(n=1).str[1]
    wash_per = wash_per.sort_values(by='PTS', ascending=False)
    wash_per = wash_per.set_index('PLAYER').head(15)
    if wash_per.empty:
        return ''
    return tabulate(wash_per, tablefmt='pipe', headers='keys',
        colalign=("left","center","center","center","center"), floatfmt=".1f")

perGame = perGame()

def homeWon(time, wiz, opp, schedule):
    schedule['score'] = '' if not wiz or not opp else wiz + "-" + opp
    if time == 'Final':
        result = 'W' if float(wiz) > float(opp) else 'L'
        schedule['score'] = result + ' ' + schedule['score']

def schedule():
    curr_month = calendar.month_name[datetime.now().month]
    url_str = "http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2024/league/00_full_schedule.json"
    with urllib.request.urlopen(url_str) as url:
        data = json.loads(url.read().decode())
    curr_month_games = [s['mscd']['g'] for s in data['lscd'] if s['mscd']['mon'] == curr_month]
    lst = []
    for game in curr_month_games[0]:
        if 'WAS' in (game['gcode']):
            schedule = {}
            if 'WAS' == game['h']['ta']:
                homeWon(game['stt'], game['h']['s'], game['v']['s'], schedule)
                schedule['team'] = "vs " + game['v']['ta']
            else:
                homeWon(game['stt'], game['v']['s'], game['h']['s'], schedule)
                schedule['team'] = "@ " + game['h']['ta']
            schedule['date'] = pd.to_datetime(game['gdte'])
            schedule['time'] = game['stt']
            lst.append(schedule)
    df = pd.DataFrame(lst)[['date', 'time', 'team', 'score']]
    df.columns = map(str.title, df.columns)
    # reformat date and time
    df.Date = df.Date.dt.strftime('%b %d')
    # add logo
    df.Team = df.Team + ' [](/' + df.Team.str[-3:] + ')' 
    return df.set_index('Date').to_markdown()

schedule = schedule()


def standings():
    sta = leaguestandings.LeagueStandings() 
    df = sta.standings.get_data_frame()
    df = df[df.Conference == 'East'][['TeamCity', 'WINS', 'LOSSES', 'WinPCT', 'L10']] # L10 removed
    df.columns = ['Team', 'W', 'L', 'PCT', 'L10']
    df.PCT = df.PCT.round(2)
    df = df.set_index('Team').reset_index()
    df.index.name = '#'
    df.index = range(1,len(df)+1)

    # games behind col
    df['W-L'] = df.W.astype(str) + ' - ' + df.L.astype(str) 
    df['WLDiff'] = df['W'] - df['L']
    df['GB'] = 0
    pos = df.columns.get_loc('WLDiff')
    df['GB'] =  (df.iat[0, pos] - df.iloc[1:, pos]) / 2

    df = df[['Team', 'W-L', 'GB', 'L10']].replace(np.nan, 0, regex=True)
    return tabulate(df, tablefmt='pipe', headers='keys',
        colalign=("center", "left", "center", "center", "center"))

standings = standings()
