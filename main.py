from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import boxscoretraditionalv2
from nba_api.stats.endpoints import leaguegamefinder
import numpy as np

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

career = playercareerstats.PlayerCareerStats(player_id='203999') 

# pandas data frames (optional: pip install pandas)
df = pd.DataFrame(career.get_data_frames()[0])
ud = df[["PLAYER_ID", "TEAM_ID", "GP", "GS", "FGM", "FG3M", "FTM", "MIN", "REB", "AST", "STL", "BLK", "TOV", "PTS"]]
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


games = leaguegamefinder.LeagueGameFinder(player_or_team_abbreviation='P', player_id_nullable=203999)  # Jokic
df = games.get_data_frames()[0]
indGames = df[["PLAYER_ID", 'GAME_DATE', 'MATCHUP', "TEAM_ID", "FGM", "FG3M", "FTM", "MIN", "REB", "AST", "STL", "BLK", "TOV", "PTS"]]
print(indGames)

newDF = indGames
newDF = newDF.copy()
newDF["PTC"] = newDF["FGM"] + newDF["FTM"]
newDF["G(X)"] = newDF["PTC"] + newDF["REB"] + newDF["AST"] + newDF["STL"]
newDF["G(X)/MIN"] = round(newDF["G(X)"] / newDF["MIN"], 2)
newDF["AST:TOV"] = np.where(
    newDF["TOV"] == 0,       # if turnovers are zero
    np.nan,               # or you could use np.inf, 0, etc.
    round(newDF["AST"] / newDF["TOV"], 2)
)
print(newDF)
# newDF["PTC"]

