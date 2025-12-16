from flask import jsonify, render_template, send_from_directory
from data_processing import get_all_active_players
from player import Player

def register_routes(app):
    
    @app.route("/static/js/<path:filename>")
    def serve_js(filename):
        return send_from_directory("/static/js", filename, mimetype="application/javascript")

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

    @app.route("/player/<int:player_id>", methods=['GET'])
    def get_player_page(player_id):
        return render_template("player.html", player_id=player_id)