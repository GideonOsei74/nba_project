import pandas as pd

games = pd.read_csv("data/processed/finals_games_clean.csv")
players = pd.read_csv("data/processed/finals_player_stats_clean.csv")

# -----------------------
# Game-level features
# -----------------------

games["POINT_DIFF"] = abs(games["TEAM1_PTS"] - games["TEAM2_PTS"])

games["TOTAL_POINTS"] = games["TEAM1_PTS"] + games["TEAM2_PTS"]

games["CLOSE_GAME"] = games["POINT_DIFF"] <= 10

games["WINNER_PTS"] = games.apply(
    lambda row: row["TEAM1_PTS"] if row["WINNER"] == row["TEAM1"] else row["TEAM2_PTS"],
    axis=1
)

games["LOSER_PTS"] = games.apply(
    lambda row: row["TEAM2_PTS"] if row["WINNER"] == row["TEAM1"] else row["TEAM1_PTS"],
    axis=1
)

# -----------------------
# Player-level features
# -----------------------

players["EFFICIENCY"] = (
    players["PTS"]
    + players["REB"]
    + players["AST"]
    + players["STL"]
    + players["BLK"]
    - (players["FGA"] - players["FGM"])
    - (players["FTA"] - players["FTM"])
    - players["TO"]
)

players["TRUE_SHOOTING_PCT"] = players["PTS"] / (
    2 * (players["FGA"] + 0.44 * players["FTA"])
)

players["AST_TO_RATIO"] = players["AST"] / players["TO"].replace(0, pd.NA)

players["THREE_POINT_RATE"] = players["FG3A"] / players["FGA"].replace(0, pd.NA)

players["FREE_THROW_RATE"] = players["FTA"] / players["FGA"].replace(0, pd.NA)

# -----------------------
# Save enhanced files
# -----------------------

games.to_csv("data/processed/finals_games_features.csv", index=False)
players.to_csv("data/processed/finals_player_stats_features.csv", index=False)

print("Feature engineering complete.")
print(games.head())
print(players.head())

# -----------------------
# Summary Tables
# -----------------------

player_summary = players.groupby(["PLAYER_ID", "PLAYER_NAME", "TEAM_ABBREVIATION"]).agg(
    GAMES_PLAYED=("GAME_ID", "nunique"),
    AVG_PTS=("PTS", "mean"),
    AVG_REB=("REB", "mean"),
    AVG_AST=("AST", "mean"),
    AVG_STL=("STL", "mean"),
    AVG_BLK=("BLK", "mean"),
    AVG_PLUS_MINUS=("PLUS_MINUS", "mean"),
    AVG_EFFICIENCY=("EFFICIENCY", "mean"),
    AVG_TRUE_SHOOTING=("TRUE_SHOOTING_PCT", "mean"),
    AVG_AST_TO_RATIO=("AST_TO_RATIO", "mean"),
    AVG_THREE_POINT_RATE=("THREE_POINT_RATE", "mean"),
    AVG_FREE_THROW_RATE=("FREE_THROW_RATE", "mean")
).reset_index()

top_scorers = player_summary.sort_values("AVG_PTS", ascending=False).head(10)

top_rebounders = player_summary.sort_values("AVG_REB", ascending=False).head(10)

top_assist_leaders = player_summary.sort_values("AVG_AST", ascending=False).head(10)

most_efficient_players = player_summary.sort_values("AVG_EFFICIENCY", ascending=False).head(10)

game_summary = games[[
    "GAME_ID",
    "MATCHUP",
    "WINNER",
    "SERIES_STATE",
    "POINT_DIFF",
    "TOTAL_POINTS",
    "CLOSE_GAME",
    "WINNER_PTS",
    "LOSER_PTS"
]]

# -----------------------
# Save Summary Tables
# -----------------------

player_summary.to_csv("data/processed/player_summary.csv", index=False)
top_scorers.to_csv("data/processed/top_scorers.csv", index=False)
top_rebounders.to_csv("data/processed/top_rebounders.csv", index=False)
top_assist_leaders.to_csv("data/processed/top_assist_leaders.csv", index=False)
most_efficient_players.to_csv("data/processed/most_efficient_players.csv", index=False)
game_summary.to_csv("data/processed/game_summary.csv", index=False)

print("Summary tables created.")
print(top_scorers)
print(most_efficient_players)

# -----------------------
# Team Summary
# -----------------------

team_summary = players.groupby("TEAM_ABBREVIATION").agg(
    GAMES_PLAYED=("GAME_ID", "nunique"),
    TOTAL_PTS=("PTS", "sum"),
    TOTAL_REB=("REB", "sum"),
    TOTAL_AST=("AST", "sum"),
    TOTAL_STL=("STL", "sum"),
    TOTAL_BLK=("BLK", "sum"),
    TOTAL_TO=("TO", "sum"),
    AVG_PTS=("PTS", "mean"),
    AVG_REB=("REB", "mean"),
    AVG_AST=("AST", "mean"),
    AVG_PLUS_MINUS=("PLUS_MINUS", "mean"),
    AVG_EFFICIENCY=("EFFICIENCY", "mean")
).reset_index()

team_summary["AST_TO_RATIO"] = team_summary["TOTAL_AST"] / team_summary["TOTAL_TO"]

team_summary.to_csv("data/processed/team_summary.csv", index=False)

print("Team summary created.")
print(team_summary)

print("\n========== SERIES OVERVIEW ==========\n")

print("Games Played:")
print(len(games))

print("\nWinner Counts:")
print(games["WINNER"].value_counts())

print("\nAverage Point Differential:")
print(round(games["POINT_DIFF"].mean(), 2))

print("\nHighest Scoring Game:")
print(games.loc[games["TOTAL_POINTS"].idxmax()])

print("\nLowest Scoring Game:")
print(games.loc[games["TOTAL_POINTS"].idxmin()])

print("\nClose Games:")
print(games["CLOSE_GAME"].value_counts())

print("\n========== PLAYER LEADERS ==========\n")

print("Top Scorers")
print(
    player_summary[
        ["PLAYER_NAME", "TEAM_ABBREVIATION", "AVG_PTS"]
    ].sort_values("AVG_PTS", ascending=False).head(10)
)

print("\nTop Rebounders")
print(
    player_summary[
        ["PLAYER_NAME", "AVG_REB"]
    ].sort_values("AVG_REB", ascending=False).head(10)
)

print("\nTop Assist Leaders")
print(
    player_summary[
        ["PLAYER_NAME", "AVG_AST"]
    ].sort_values("AVG_AST", ascending=False).head(10)
)

print("\nMost Efficient Players")
print(
    player_summary[
        ["PLAYER_NAME", "AVG_EFFICIENCY"]
    ].sort_values("AVG_EFFICIENCY", ascending=False).head(10)
)

print("\n========== TEAM SUMMARY ==========\n")

print(team_summary)