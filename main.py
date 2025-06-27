"""
The goal of this program is to extract key indicators of NBA championship teams
based on historical data.
Indicators include:
    Regular Season Record

These indicators will be plotted with matplotlib & seaborn to compare analytics

"""

import pandas as pd
import numpy as np
import sqlite3 as sql
from matplotlib import pyplot as plt
import seaborn as sns
from . import scraper, tables

conn = sql.connect('database.db') # create connection object to database
cursor = conn.cursor()

sns.set_theme()

#Displays the number of champions that finished the regular season at each rank
def DisplayChampionRecords():
    getChampionsRecords = '''
                            SELECT COUNT(t.Year), t.Rank
                            FROM (
                                SELECT * FROM
                                TeamRecord r JOIN ChampionsTable c 
                                ON r.Team = c.Champion AND r.Year = c.Year 
                                ) AS t
                            GROUP BY t.Rank
                            ORDER BY CAST(t.Rank AS INT);
                            '''


    championRecords = pd.read_sql_query(getChampionsRecords, conn)

    seed = championRecords.iloc[:, 1]
    num_winners = championRecords.iloc[:, 0]

    plt.grid()
    plt.title('Regular Season Rank to Finals Record')
    plt.xlabel('Seed')
    plt.ylabel('Number of Champions')
    plt.bar(seed, num_winners)
    plt.show()

#Calculates the number of teams that won with the league MVP
def MVPAndChampionCount():
    getMVPChampions = '''
                        SELECT COUNT(m.Season)
                        FROM (
                            SELECT a.Abbreviation AS abr, c.Year
                            FROM ChampionsTable c JOIN Abbreviations a
                            ON c.Champion = a.Team
                            GROUP BY c.Year
                            ORDER BY CAST(c.Year AS INT) DESC
                            ) AS t
                        JOIN MVPs m ON t.abr = m.Team
                        AND CAST(t.Year AS INT) = CAST(SUBSTRING(m.Season, 1, 4) AS INT) + 1;
                        '''
    MVPandChampion = pd.read_sql_query(getMVPChampions, conn).iloc[0, 0]

    return MVPandChampion

def DisplayNumChampsByRating():
    getSRSRating = '''
                        SELECT COUNT(TeamId), SRS
                        FROM ChampionSummary
                        GROUP BY SRS;
                        '''
    SRSRating = pd.read_sql_query(getSRSRating, conn)
    SRSrank = SRSRating.iloc[:, 1]
    SRS_num_winners = SRSRating.iloc[:, 0]

    getOffRating = '''
                        SELECT COUNT(TeamId), OffRtg
                        FROM ChampionSummary
                        GROUP BY OffRtg;
                        '''
    OffRating = pd.read_sql_query(getOffRating, conn)
    Offrank = OffRating.iloc[:, 1]
    Off_num_winners = OffRating.iloc[:, 0]

    getDefRating = '''
                        SELECT COUNT(TeamId), DefRtg
                        FROM ChampionSummary
                        GROUP BY DefRtg;
                        '''
    DefRating = pd.read_sql_query(getDefRating, conn)
    Defrank = DefRating.iloc[:, 1]
    Def_num_winners = DefRating.iloc[:, 0]

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))  # Create 1 row, 3 columns of subplots

    # SRS subplot
    axs[0].set_title('SRS Rank vs Championship Teams')
    axs[0].set_xlabel('SRS Rank')
    axs[0].set_ylabel('Number of Champions')
    axs[0].bar(SRSrank, SRS_num_winners)
    axs[0].set_xlim(0, 10)
    axs[0].set_ylim(0, 40)

    # Off Rating subplot
    axs[1].set_title('Off Rank vs Championship Teams')
    axs[1].set_xlabel('Off Rank')
    axs[1].set_ylabel('Number of Champions')
    axs[1].bar(Offrank, Off_num_winners)
    axs[1].set_xlim(0, 10)
    axs[1].set_ylim(0, 40)

    # Def Rating subplot
    axs[2].set_title('Def Rank vs Championship Teams')
    axs[2].set_xlabel('Def Rank')
    axs[2].set_ylabel('Number of Champions')
    axs[2].bar(Defrank, Def_num_winners)
    axs[2].set_xlim(0, 10)
    axs[2].set_ylim(0, 40)

    plt.tight_layout()
    plt.show()


def DisplayChampRatingsByYear():
    getSRSInfo = '''
                        SELECT TeamId, SRS
                        FROM ChampionSummary;
                        '''
    SRSInfo = pd.read_sql_query(getSRSInfo, conn)
    SRSRating = SRSInfo.iloc[:, 1]

    getOffInfo = '''
                        SELECT TeamId, OffRtg
                        FROM ChampionSummary;
                        '''
    OffInfo = pd.read_sql_query(getOffInfo, conn)
    OffRating = OffInfo.iloc[:, 1]

    getDefInfo = '''
                        SELECT TeamId, DefRtg
                        FROM ChampionSummary;
                        '''
    DefInfo = pd.read_sql_query(getDefInfo, conn)
    DefRating = DefInfo.iloc[:, 1]

    years = np.linspace(1951, 2024, 74, endpoint=True)

    """colors = np.where(year < 1960, 'red',
         np.where(year < 1970, 'orange',
         np.where(year < 1980, 'yellow',
         np.where(year < 1990, 'blue',
         np.where(year < 2000, 'green',        
         np.where(year < 2015, 'indigo'), 'violet')))))"""
    

    fig, axs = plt.subplots(3, 1, figsize=(15, 10), gridspec_kw={'hspace': 0.5}) 

    # SRS subplot
    axs[0].set_title('SRS Rank vs Championship Teams')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('SRS Rank')
    axs[0].scatter(years, SRSRating[::-1])

    # Off Rating subplot
    axs[1].set_title('Off Rank vs Championship Teams')
    axs[1].set_xlabel('Year')
    axs[1].set_ylabel('Off Rank')
    axs[1].scatter(years, OffRating[::-1])

    # Def Rating subplot
    axs[2].set_title('Def Rank vs Championship Teams')
    axs[2].set_xlabel('Year')
    axs[2].set_ylabel('Def Rank')
    axs[2].scatter(years, DefRating[::-1])

    plt.show()

def Display3PStats():
    championThreePointInfo = pd.read_sql_query('''SELECT * FROM 3PChamp;''', conn) 
    leagueThreePointInfo = pd.read_sql_query('''SELECT 3P FROM LeagueAverages;''', conn) 

    years = np.linspace(1979, 2024, 46, endpoint=True)

    fig, axs = plt.subplots(2, 1, figsize=(15, 10), gridspec_kw={'hspace': 0.5}) 

    axs[0].set_title('3PAr of Champions Since 1979')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('3PAr / 3PAr Rank')

    axs[0].plot(years, championThreePointInfo.loc['3PAr'][::-1], label='Champion 3PAr')
    axs[0].plot(years, championThreePointInfo.loc['3PArRank'][::-1], label='Champion 3PAr Rank')

    axs[1].set_title('3P of Champions vs LeagueSince 1979')
    axs[1].set_xlabel('Year')
    axs[1].set_ylabel('3P / 3P Rank')

    axs[1].plot(years, championThreePointInfo.loc['3P'][::-1], label='Champions 3P Averages')
    axs[1].plot(years, championThreePointInfo.loc['3PRank'][::-1], label='Champions 3P Rank')

    axs[1].plot(years, leagueThreePointInfo[::-1], label='League 3P Averages')
    plt.show()

def main():
    scraper.scrape()
    tables.create()

if __name__ == "__main__":
    main()
