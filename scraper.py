"""
Web Scraper to extract historical NBA data from https://www.basketball-reference.com/


"""
import requests
from bs4 import BeautifulSoup as bs, Comment
import pandas as pd
from io import StringIO
import time
import os

def fetchTable(url, id):
    response = requests.get(url)
    soup = bs(response.content, 'html5lib')
    
    # Find a table by its ID
    table = soup.find('table', id=id)

    i = 0
    while table is None:
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        
        comment_soup = bs(comments[i], 'html5lib')
        table = comment_soup.find('table', id=id)
        i+=1

    df = pd.read_html(StringIO(str(table)))[0]

    return df

def fetchSummary(url, id, ratings, team_id):
    response = requests.get(url)
    soup = bs(response.content, 'html5lib')

    summary = soup.find('div', id=id).text

    for line in summary.splitlines():
        if 'SRS' in line:
            ratings.loc[team_id, 'SRS'] = line
        if 'Off Rtg' in line:
            ratings.loc[team_id, 'Off Rtg'] = line
        if 'Def Rtg' in line:
            ratings.loc[team_id, 'Def Rtg'] = line
        if 'Net Rtg' in line:
            ratings.loc[team_id, 'Net Rtg'] = line
        
    print(ratings.loc[team_id])


def scrape():
    #NBA champions by year
    df = fetchTable('https://www.basketball-reference.com/playoffs/', 'champions_index')
    if os.path.isfile("data/expanded_standings.csv"):
            df.to_csv("data/champions_index.csv", mode='a')
    else:
        df.to_csv("data/champions_index.csv")

    time.sleep()

    #NBA season statistics by year
    for year in range(2025, 1949, -1):
        df = fetchTable('https://www.basketball-reference.com/leagues/NBA_{}_standings.html'.format(year), 'expanded_standings')
        df['year'] = year
        df.set_index('year',inplace=True)
        if os.path.isfile("data/expanded_standings.csv"):
            df.to_csv("data/champion_summary.csv", mode='a')
        else:
            df.to_csv("data/expanded_standings.csv")

        time.sleep(3)


    #NBA MVP by year
    df = fetchTable('https://www.basketball-reference.com/awards/mvp.html', 'mvp_NBA')
    df.to_csv(f"data/mvp_NBA.csv", mode='a', index=False)

    time.sleep()

    #NBA champions statistics by year
    champions = pd.read_csv("data/champions_index.csv").loc[:, ['Champion', 'Year', 'Lg']]
    abbreviations = pd.read_csv("data/nba_teams_all_time.csv")
    ratings = pd.DataFrame(columns=['Team Id', 'SRS', 'Off Rtg', 'Def Rtg', 'Net Rtg']).set_index('Team Id')
    champThreePt = pd.DataFrame(columns=['Team Id', '3P', '3PRank', '3P%', '3P%Rank', '3PAr', '3PArRank']).set_index('Team Id')
    for index, row in champions.iterrows():
        #skips first two rows (col names, curr season), invalid rows and ABA champions
        if index == 0 or row.isna().any() or row.iloc[2] == 'ABA' or row.iloc[1] < 1951:
            continue

        team = row.iloc[0]
        year = row.iloc[1]
        abr = abbreviations.loc[abbreviations['Team'] == team].iloc[0, 1]
        fetchSummary('https://www.basketball-reference.com/teams/{}/{}.html'.format(abr, int(year)), 'meta', ratings, team + '-' + str(year))

        time.sleep(3)

        if year > 1979: #3P shot was introduced in 1979-1980
            table = fetchTable('https://www.basketball-reference.com/teams/{}/{}.html'.format(abr, int(year)), 'team_and_opponent')
            champThreePt.loc[team + '-' + str(year), '3P'] = table['3P'][1] #3 pointers made per game
            champThreePt.loc[team + '-' + str(year), '3PRank'] = table['3P'][2] #Rank of 3 pointers made
            champThreePt.loc[team + '-' + str(year), '3P%'] = table['3P%'][1] #3 point percentage
            champThreePt.loc[team + '-' + str(year), '3P%Rank'] = table['3P%'][2] #Rank of 3 point percentage

            table = fetchTable('https://www.basketball-reference.com/teams/{}/{}.html'.format(abr, int(year)), 'team_misc')
            champThreePt.loc[team + '-' + str(year), '3PAr'] = table[('Advanced', '3PAr')][0] #3-Point Attempt Rate
            champThreePt.loc[team + '-' + str(year), '3PArRank'] = table[('Advanced', '3PAr')][1]#Percentage of field goals taken from the 3-point range

        time.sleep(3)

    champThreePt.to_csv("data/champ_3P.csv")

    #get position in between brackets
    SRS_Ranking = ratings['SRS'].str.extract('(\\(.*\\))')[0].str[1]
    Off_Ranking = ratings['Off Rtg'].str.extract('(\\(.*\\))')[0].str[1]
    Def_Ranking = ratings['Def Rtg'].str.extract('(\\(.*\\))')[0].str[1]
    Net_Ranking = ratings['Net Rtg'].str.extract('(\\(.*\\))')[0].str[1]

    df = pd.DataFrame({'SRS': SRS_Ranking, 'Off': Off_Ranking, 'Def': Def_Ranking, 'Net': Net_Ranking})

    df.to_csv("data/champion_summary.csv")


    #NBA League Averages
    df = fetchTable('https://www.basketball-reference.com/leagues/NBA_stats_per_game.html', 'stats-Regular-Season')
    if os.path.isfile("data/league_averages.csv"):
            df.to_csv("data/league_averages.csv", mode='a')
    else:
        df.to_csv("data/league_averages.csv")




