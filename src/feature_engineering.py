import pandas as pd
import numpy as np

players = pd.read_csv("data/processed/finals_player_stats_clean.csv")

# ------------------------------------
# Convert MM:SS to decimal minutes
# ------------------------------------

def minutes_to_decimal(min_str):
    if pd.isna(min_str):
        return np.nan

    minutes, seconds = min_str.split(":")
    return int(minutes) + int(seconds) / 60

players["MIN_DECIMAL"] = players["MIN"].apply(minutes_to_decimal)

# ------------------------------------
# Advanced Metrics
# ------------------------------------

# Effective Field Goal Percentage
players["EFG_PCT"] = (
    players["FGM"] + 0.5 * players["FG3M"]
) / players["FGA"].replace(0, np.nan)

# True Shooting Percentage
players["TS_PCT"] = (
    players["PTS"]
) / (2 * (players["FGA"] + 0.44 * players["FTA"]).replace(0, np.nan))

# Assist-to-Turnover Ratio
players["AST_TO_RATIO"] = (
    players["AST"]
) / players["TO"].replace(0, np.nan)

# Three-Point Attempt Rate
players["THREE_POINT_RATE"] = (
    players["FG3A"]
) / players["FGA"].replace(0, np.nan)

# Points Per Minute
players["PTS_PER_MIN"] = (
    players["PTS"]
) / players["MIN_DECIMAL"].replace(0, np.nan)

print(
    players[
        [
            "PLAYER_NAME",
            "MIN",
            "MIN_DECIMAL"
        ]
    ].head(10)
)
# Points Per Minute
players["PTS_PER_MIN"] = (
    players["PTS"]
) / players["MIN_DECIMAL"].replace(0, np.nan)

# Free Throw Rate
players["FREE_THROW_RATE"] = (
    players["FTA"]
) / players["FGA"].replace(0, np.nan)

# Rebounds Per Minute
players["REB_PER_MIN"] = (
    players["REB"]
) / players["MIN_DECIMAL"].replace(0, np.nan)

# Assists Per Minute
players["AST_PER_MIN"] = (
    players["AST"]
) / players["MIN_DECIMAL"].replace(0, np.nan)

# Stocks = Steals + Blocks
players["STOCKS"] = players["STL"] + players["BLK"]

# Basic Player Efficiency
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

print(
    players[
        [
            "PLAYER_NAME",
            "MIN",
            "MIN_DECIMAL",
            "FREE_THROW_RATE",
            "REB_PER_MIN",
            "AST_PER_MIN",
            "STOCKS",
            "EFFICIENCY",
        ]
    ].head(10)
)

# ------------------------------------
# Export Advanced Dataset
# ------------------------------------

players.to_csv(
    "data/processed/finals_player_stats_advanced.csv",
    index=False
)

print("\nAdvanced dataset saved successfully!")