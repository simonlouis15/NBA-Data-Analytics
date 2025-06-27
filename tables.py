import pandas as pd
import sqlite3 as sql

def create():
    conn = sql.connect('database.db')
    cursor = conn.cursor()

    df = pd.read_csv('data/champions_index.csv', index_col=0).iloc[:, :5]
    df.columns = ['Year', 'League', 'Champion', 'RunnerUp', 'Finals MVP']

    print(df)
    # insert the first four columns from the DataFrame into the SQLite table
    df.to_sql('ChampionsTable', conn, if_exists='replace', index=False)

    df = pd.read_csv('data/expanded_standings.csv').iloc[:, :6]
    df.columns = ['Year', 'Rank', 'Team', 'Record', 'HomeRecord', 'AwayRecord']

    print(df)
    df.to_sql('TeamRecord', conn, if_exists='replace', index=False)

    df = pd.read_csv('data/nba_teams_all_time.csv')
    df.columns = ['Team', 'Abbreviation']

    print(df)
    df.to_sql('Abbreviations', conn, if_exists='replace', index=False)

    df = pd.read_csv('data/mvp_NBA.csv')
    df.columns = ['Season', 'Lg', 'Player', 'Voting', 'Age', 'Team', 'G', 'MP', 'PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%', '3P%', 'FT%', 'WS', 'WS/48']

    print(df)
    df.to_sql('MVPs', conn, if_exists='replace', index=False)

    df = pd.read_csv('data/champion_summary.csv')
    df.columns = ['TeamId', 'SRS', 'OffRtg', 'DefRtg', 'NetRtg']

    print(df)
    df.to_sql('ChampionSummary', conn, if_exists='replace', index=False)

    df = pd.read_csv('data/3P.csv')
    df.columns = ['Team Id','3P','3PRank','3P%','3P%Rank','3PAr','3PArRank']

    print(df)
    df.to_sql('3PChamp', conn, if_exists='replace', index=False)

    df = pd.read_csv('data/league_averages.csv')
    df.columns = ['Rk','Season','Lg','Age','Ht','Wt','G','MP','FG','FGA','3P','3PA','FT','FTA','ORB','DRB','TRB','AST',
                'STL','BLK','TOV','PF','PTS','FG%','3P%','FT%','Pace','eFG%','TOV%','ORB%','FT/FGA','ORtg','TS%']

    print(df)
    df.to_sql('LeagueAverages', conn, if_exists='replace', index=False)
