import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import boxscorematchupsv3
from nba_api.stats.endpoints import leaguegamefinder


def get_all_active_players():
    df = pd.DataFrame(players.get_active_players())
    df = df[["id", "full_name"]]
    return df.to_dict(orient="records")

def get_all_teams():
    # may not be used
    df = pd.DataFrame(teams.get_teams())
    print(df)

def get_season_match_data(gameid: str):
    box = boxscorematchupsv3.BoxScoreMatchupsV3(game_id=gameid)
    teams_df = box.get_data_frames()[0]
    # print(teams_df[["TEAM_ID", "GAME_ID", "GAME_DATE", "PTS", "FGA", ]])
    print(teams_df["teamId"].unique())
    """
    Big fix needed here
    Currently function needs the gameid which is irrelevant to the main function of the 
    currently it will be easier to just sum up values of games for a team and compare 
    for upcoming games
    
    however potentially for the future it may make sense to calculate important stats by the dates, to see values as the teams beat each other during the season"""

    for i in teams_df["teamId"].unique():
        team = leaguegamefinder.LeagueGameFinder(player_or_team_abbreviation='T', team_id_nullable=i)
        df = pd.DataFrame(team.get_data_frames()[0])
        # print(df.loc[df['SEASON_ID'] == "22025"])



# under construction
# team = teamgamelog.TeamGameLog(team_id=1610612756)
# team = leaguegamefinder.LeagueGameFinder(player_or_team_abbreviation='T', team_id_nullable=1610612756)
# teamdf = pd.DataFrame(team.get_data_frames()[0])
# print(teamdf.head())  
# get_season_match_data("0022500190")
# get_all_teams()
# graph_utility(igs[:25])