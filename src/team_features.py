import pandas as pd
import numpy as np

# Load advanced player dataset
players = pd.read_csv("data/processed/finals_player_stats_advanced.csv")

# Aggregate to team-by-game level
team = (
    players.groupby(["GAME_ID", "TEAM_ABBREVIATION"])
    .agg(
        TOTAL_POINTS=("PTS", "sum"),
        TOTAL_REBOUNDS=("REB", "sum"),
        TOTAL_ASSISTS=("AST", "sum"),
        TOTAL_STEALS=("STL", "sum"),
        TOTAL_BLOCKS=("BLK", "sum"),
        TOTAL_TURNOVERS=("TO", "sum"),
        TOTAL_FGM=("FGM", "sum"),
        TOTAL_FGA=("FGA", "sum"),
        TOTAL_FG3M=("FG3M", "sum"),
        TOTAL_FG3A=("FG3A", "sum"),
        TOTAL_FTM=("FTM", "sum"),
        TOTAL_FTA=("FTA", "sum"),
        TOTAL_MINUTES=("MIN_DECIMAL", "sum"),
        AVG_PLUS_MINUS=("PLUS_MINUS", "mean"),
    )
    .reset_index()
)

# -----------------------------
# Advanced Team Metrics
# -----------------------------

# Effective FG%
team["TEAM_EFG_PCT"] = (
    team["TOTAL_FGM"] + 0.5 * team["TOTAL_FG3M"]
) / team["TOTAL_FGA"].replace(0, np.nan)

# True Shooting %
team["TEAM_TS_PCT"] = (
    team["TOTAL_POINTS"]
) / (
    2 * (team["TOTAL_FGA"] + 0.44 * team["TOTAL_FTA"])
).replace(0, np.nan)

# Assist-to-Turnover Ratio
team["TEAM_AST_TO_RATIO"] = (
    team["TOTAL_ASSISTS"]
) / team["TOTAL_TURNOVERS"].replace(0, np.nan)

# Three-Point Attempt Rate
team["TEAM_3PT_RATE"] = (
    team["TOTAL_FG3A"]
) / team["TOTAL_FGA"].replace(0, np.nan)

# Free Throw Rate
team["TEAM_FT_RATE"] = (
    team["TOTAL_FTA"]
) / team["TOTAL_FGA"].replace(0, np.nan)

# Points Per Minute
team["TEAM_PTS_PER_MIN"] = (
    team["TOTAL_POINTS"]
) / team["TOTAL_MINUTES"].replace(0, np.nan)

# Stocks
team["TEAM_STOCKS"] = (
    team["TOTAL_STEALS"] + team["TOTAL_BLOCKS"]
)

# Basic Team Efficiency
team["TEAM_EFFICIENCY"] = (
    team["TOTAL_POINTS"]
    + team["TOTAL_REBOUNDS"]
    + team["TOTAL_ASSISTS"]
    + team["TOTAL_STEALS"]
    + team["TOTAL_BLOCKS"]
    - (team["TOTAL_FGA"] - team["TOTAL_FGM"])
    - (team["TOTAL_FTA"] - team["TOTAL_FTM"])
    - team["TOTAL_TURNOVERS"]
)

# Export
team.to_csv("data/processed/team_analytics.csv", index=False)

print(team.head())
print("\nTeam analytics dataset saved successfully!")