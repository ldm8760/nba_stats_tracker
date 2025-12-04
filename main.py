import time
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import players
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams
from nba_api.stats.endpoints import boxscorematchupsv3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from requests import ReadTimeout
from flask import Flask, request, jsonify, render_template, send_from_directory

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# pd.set_option('display.width', None)

def trim_percentile(values, low=10, high=90):
    values = np.array(values)
    if len(values) == 0:
        return values
    lo = np.percentile(values, low)
    hi = np.percentile(values, high)
    return values[(values >= lo) & (values <= hi)]


def get_all_active_players():
    df = pd.DataFrame(players.get_active_players())
    df = df[["id", "full_name"]]
    return df.to_dict(orient="records")

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

app = Flask(__name__)

@app.route("/static/js/<path:filename>")
def serve_js(filename):
    return send_from_directory("static/js", filename, mimetype="application/javascript")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pull", methods=['GET'])
def send_players():
    actives = get_all_active_players()
    nba_players = []
    limit = 0
    for player in actives:
        p = Player(player["id"], player["full_name"])
        if p.igs.empty:
            nba_players.append({"id": p.id, "name": p.name, "avg_fpts/min": None, "points": None, 
                                "rebounds": None, "assists": None, "steals": None, "blocks": None, 
                                "turnovers": None})
            continue
        avg = p.show_avg_fpts_by_season(22025)

        nba_players.append({"id": p.id, "name": p.name, "avg_fpts/min": avg, "points": round(p.igs["PTS"].mean(), 2), 
                            "rebounds": round(p.igs["REB"].mean(), 2), "assists": round(p.igs["AST"].mean(), 2), 
                            "steals": round(p.igs["STL"].mean(), 2), "blocks": round(p.igs["BLK"].mean(), 2), 
                            "turnovers": round(p.igs["TOV"].mean(), 2)})
        limit += 1
        if limit >= 5:
            break
    return jsonify(nba_players), 200

@app.route("/player-page/<int:player_id>", methods=['GET'])
def get_player_page(player_id):
    return render_template("player.html", player_id=player_id)



if __name__ == "__main__":
    app.run(debug=True)

    # actives = get_all_active_players()
    # nba_players = []
    # for row in actives.itertuples():
    #     p = Player(row.id, row.full_name)
    #     print(p.name, end=" ")

    #     if p.igs.empty:
    #         continue

    #     avg = p.show_avg_fpts_by_season(22025)
    #     trimmed = p.show_avg_fpts_by_season_trimmed(22025)

    #     if avg is None:   # skip players with no games
    #         continue

    #     nba_players.append({
    #         "player": p,
    #         "name": row.full_name,
    #         "avg_fpts_min": avg,
    #         "trimmed_fpts_min": trimmed
    #     })
    # df = pd.DataFrame(nba_players)
    # df = df.sort_values("avg_fpts_min", ascending=False)
    # print(df)

    # print(get_all_active_players())


    # print(f"Average FPTS/MIN: {p.show_avg_fpts_by_season(22025)}")
    # print(f"Average FPTS/MIN: {p.show_avg_fpts_by_season_trimmed(22025)}")
    # p.historical_stats()



    # under construction
    # team = teamgamelog.TeamGameLog(team_id=1610612756)
    # team = leaguegamefinder.LeagueGameFinder(player_or_team_abbreviation='T', team_id_nullable=1610612756)
    # teamdf = pd.DataFrame(team.get_data_frames()[0])
    # print(teamdf.head())  
    # get_season_match_data("0022500190")
    # get_all_teams()
    # graph_utility(igs[:25])




