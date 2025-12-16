import time
import numpy as np # remove soon
import pandas as pd # remove soon
from requests import ReadTimeout
from nba_api.stats.endpoints import leaguegamefinder # remomve soon
from nba_api.stats.endpoints import playercareerstats # remove soon

def trim_percentile(values, low=10, high=90):
    values = np.array(values)
    if len(values) == 0:
        return values
    lo = np.percentile(values, low)
    hi = np.percentile(values, high)
    return values[(values >= lo) & (values <= hi)]

class Player:
    def __init__(self, player_id, name):
        self.id = player_id
        self.name = name
        self.igs = self.individual_game_stats()

    def show_avg_fpts_by_season(self, season_id):
        df = self.igs[self.igs["SEASON_ID"].astype(str) == str(season_id)]
        s = df["FPTS/MIN"]
        return round(s.mean(), 3)
    
    def show_avg_fpts_by_season_trimmed(self, season_id):
        df = self.igs[self.igs["SEASON_ID"].astype(str) == str(season_id)]
        vals = df["FPTS/MIN"].to_numpy()

        trimmed = trim_percentile(vals, low=10, high=90)

        if len(vals) == 0:
            return None

        return trimmed.mean() if len(trimmed) > 0 else None

    def individual_game_stats(self):
        """Fetches data per individual game with retries on timeout"""
        try:
            games = leaguegamefinder.LeagueGameFinder(
                player_or_team_abbreviation='P',
                player_id_nullable=self.id
            )
            df = pd.DataFrame(games.get_data_frames()[0])

            if df.empty:
                return pd.DataFrame()  # player has no games
            
            df = df.copy()

            # Fantasy points
            df["FPTS"] = df["PTS"] + df["REB"] + df["AST"]*2 + (df["STL"]+df["BLK"])*4 \
                            - df["TOV"]*2 + df["FG3M"] + df["FGM"]*2 + df["FTM"] - df["FTA"] - df["FGA"]

            # FPTS per minute
            df["FPTS/MIN"] = np.where(df["MIN"]==0, np.nan, round(df["FPTS"] / df["MIN"], 3))

            # AST:TOV ratio
            df["AST:TOV"] = np.where(df["TOV"]==0, np.nan, round(df["AST"] / df["TOV"], 3))

            # True Shooting %
            df["TS%"] = np.where((df["FGA"] + 0.44 * df["FTA"]) == 0, np.nan,
                                    round(df["PTS"] / (2 * (df["FGA"] + 0.44 * df["FTA"])), 3))
            return df

        except ReadTimeout:
            time.sleep(1)

        # if all retries fail
        print(f"Failed to fetch games for player {self.name} after {3} attempts")
        return pd.DataFrame()


    def historical_stats(self):
        """Data per season"""
        career = playercareerstats.PlayerCareerStats(player_id=self.id)
        careerdf = pd.DataFrame(career.get_data_frames()[0])
        print(careerdf.head())