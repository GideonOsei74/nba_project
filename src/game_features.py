import pandas as pd

games = pd.read_csv("data/processed/finals_games_clean.csv")

# Game number
games["GAME_NUMBER"] = range(1, len(games) + 1)

# Score margin
games["POINT_DIFFERENTIAL"] = abs(games["TEAM1_PTS"] - games["TEAM2_PTS"])

# Winner / loser points
games["WINNER_PTS"] = games[["TEAM1_PTS", "TEAM2_PTS"]].max(axis=1)
games["LOSER_PTS"] = games[["TEAM1_PTS", "TEAM2_PTS"]].min(axis=1)

# Close game flag
games["CLOSE_GAME_FLAG"] = games["POINT_DIFFERENTIAL"].apply(
    lambda x: "Close Game" if x <= 5 else "Decisive Game"
)

# Knicks win flag
games["NYK_WIN_FLAG"] = games["WINNER"].apply(lambda x: 1 if x == "NYK" else 0)

# Spurs win flag
games["SAS_WIN_FLAG"] = games["WINNER"].apply(lambda x: 1 if x == "SAS" else 0)

# Cumulative series wins
games["NYK_SERIES_WINS"] = games["NYK_WIN_FLAG"].cumsum()
games["SAS_SERIES_WINS"] = games["SAS_WIN_FLAG"].cumsum()

# Series leader after each game
games["SERIES_LEADER"] = games.apply(
    lambda row: "NYK"
    if row["NYK_SERIES_WINS"] > row["SAS_SERIES_WINS"]
    else "SAS"
    if row["SAS_SERIES_WINS"] > row["NYK_SERIES_WINS"]
    else "Tied",
    axis=1,
)

games.to_csv("data/processed/game_analytics.csv", index=False)

print(games.head())
print("\nGame analytics dataset saved successfully!")