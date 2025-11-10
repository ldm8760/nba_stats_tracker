from nba_api.stats.endpoints import playercareerstats
import pandas as pd

career = playercareerstats.PlayerCareerStats(player_id='203999') 

# pandas data frames (optional: pip install pandas)
df = pd.DataFrame(career.get_data_frames()[0])

# json
print(df)