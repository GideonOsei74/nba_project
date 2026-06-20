import pandas as pd
from pathlib import Path


def clean_finals_games():
    raw_path = Path("data/raw/finals_series_tracker_raw.csv")
    output_path = Path("data/processed/finals_games_clean.csv")

    df = pd.read_csv(raw_path)

    df = df.drop_duplicates()
    df["GAME_ID"] = df["GAME_ID"].astype(str)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    return df


def clean_player_stats():
    raw_path = Path("data/raw/finals_player_stats_raw.csv")
    output_path = Path("data/processed/finals_player_stats_clean.csv")

    df = pd.read_csv(raw_path)

    df = df.drop_duplicates()
    df["GAME_ID"] = df["GAME_ID"].astype(str)

    # Keep useful columns only
    columns_to_keep = [
        "GAME_ID",
        "TEAM_ID",
        "TEAM_ABBREVIATION",
        "PLAYER_ID",
        "PLAYER_NAME",
        "START_POSITION",
        "MIN",
        "PTS",
        "REB",
        "AST",
        "STL",
        "BLK",
        "TO",
        "FGM",
        "FGA",
        "FG_PCT",
        "FG3M",
        "FG3A",
        "FG3_PCT",
        "FTM",
        "FTA",
        "FT_PCT",
        "OREB",
        "DREB",
        "PF",
        "PLUS_MINUS"
    ]

    existing_columns = [col for col in columns_to_keep if col in df.columns]
    df = df[existing_columns]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    return df