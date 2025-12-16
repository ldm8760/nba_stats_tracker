import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask
from api import register_routes

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

def graph_utility(df):
    df = df[::-1]
    plt.scatter(df["GAME_DATE"], df["FPTS"])
    plt.xlabel('Game Date', ha="right")
    plt.ylabel('FPTS')
    plt.title('Grayson Allen')
    plt.tight_layout()
    plt.show()

app = Flask(__name__, template_folder="../templates", static_folder="../frontend/static/js")
register_routes(app)

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



    




