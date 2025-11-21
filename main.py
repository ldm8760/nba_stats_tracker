from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import players
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams
from nba_api.stats.endpoints import boxscorematchupsv3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# pd.set_option('display.width', None)




# ud = df[["PLAYER_ID", "TEAM_ID", "GP", "GS", "FGM", "FG3M", "FTM", "MIN", "REB", "AST", "STL", "BLK", "TOV", "PTS"]]
# ud means usefulData

# ud["PTC"] = ud["FGM"] + ud["FTM"]
# ud = ud.copy()
# ud = ud["FGM"] + ud["FTM"]
# print(ud)


# gx = (ud["PTC"] + ud["REB"] + ud["AST"] + ud["STL"]) / ud["MIN"]

# game_id = "0022400001"  # Example: 2024–25 regular season opener

# boxscore = boxscoretraditionalv2.NBAStatsHTTP()
# df = boxscore.get_data_frames()[0]
# print(df.head())

def get_all_active_players():
    df = pd.DataFrame(players.get_active_players())
    df = df[["id", "full_name"]]
    return df

def get_all_teams():
    # may not be used
    df = pd.DataFrame(teams.get_teams())
    print(df)


class Player:
    def __init__(self, player_id, name):
        self.id = player_id
        self.name = name
        self.igs = self.individual_game_stats()

    def show_avg_fpts_by_season(self, season_id):
        s = self.igs["FPTS/MIN"]
        total = s.sum()
        count = s.count()
        return total / count


    def individual_game_stats(self):
        """Data per individual game"""
        games = leaguegamefinder.LeagueGameFinder(player_or_team_abbreviation='P', player_id_nullable=self.id)
        games_df = pd.DataFrame(games.get_data_frames()[0])
        df = games_df[["PLAYER_ID", "SEASON_ID", 'TEAM_ID', 'MATCHUP', "GAME_DATE", "FTA", "FTM", "FGA", "FGM", "FG3A", "FG3M", "MIN", "REB", "AST", "STL", "BLK", "TOV", "PTS"]].copy()
        df["FPTS"] = df["PTS"] + df["REB"] + df["AST"] * 2 + (df["STL"] + df["BLK"]) * 4 - df["TOV"] * 2 + df["FG3M"] + df["FGM"] * 2 + df["FTM"] - df["FTA"] - df["FGA"]
        
        df["FPTS/MIN"] = np.where(
            df["MIN"] == 0,
            np.nan,
            round(df["FPTS"] / df["MIN"], 3)
        )
        
        df["AST:TOV"] = np.where(
            df["TOV"] == 0,       # if turnovers are zero
            np.nan,               # or you could use np.inf, 0, etc.
            round(df["AST"] / df["TOV"], 3)
        )

        df["TS%"] = np.where(
            (df["FGA"] + 0.44 * df["FTA"]) == 0,
            np.nan,
            round(df["PTS"] / (2 * (df["FGA"] + 0.44 * df["FTA"])), 3)
        )
        return df

    def historical_stats(self):
        """Data per season"""
        career = playercareerstats.PlayerCareerStats(player_id=self.id)
        careerdf = pd.DataFrame(career.get_data_frames()[0])
        print(careerdf)

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



def graph_utility(df):
    df = df[::-1]
    plt.scatter(df["GAME_DATE"], df["FPTS"])
    plt.xlabel('Game Date', ha="right")
    plt.ylabel('FPTS')
    plt.title('Grayson Allen')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    actives = get_all_active_players()
    # nba_players = []
    p = Player(203999, "Nikola Jokic")
    print(p.igs.head())
    print(f"Average FPTS/MIN: {p.show_avg_fpts_by_season(1)}")
    p.historical_stats()[:5]



    # under construction
    # team = teamgamelog.TeamGameLog(team_id=1610612756)
    # team = leaguegamefinder.LeagueGameFinder(player_or_team_abbreviation='T', team_id_nullable=1610612756)
    # teamdf = pd.DataFrame(team.get_data_frames()[0])
    # print(teamdf.head())  
    # get_season_match_data("0022500190")
    # get_all_teams()
    # graph_utility(igs[:25])




