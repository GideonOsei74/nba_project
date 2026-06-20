import pandas as pd
from pathlib import Path


def create_dimensions():
    players = pd.read_csv("data/processed/finals_player_stats_clean.csv")
    games = pd.read_csv("data/processed/finals_games_clean.csv")

    # -----------------
    # Player Dimension
    # -----------------
    dim_player = (
        players[
            [
                "PLAYER_ID",
                "PLAYER_NAME",
                "TEAM_ID",
                "TEAM_ABBREVIATION",
            ]
        ]
        .drop_duplicates()
        .sort_values("PLAYER_NAME")
    )

    # -----------------
    # Team Dimension
    # -----------------
    dim_team = (
        players[
            [
                "TEAM_ID",
                "TEAM_ABBREVIATION",
            ]
        ]
        .drop_duplicates()
        .sort_values("TEAM_ABBREVIATION")
    )

    # -----------------
    # Game Dimension
    # -----------------
    dim_game = games[
        [
            "GAME_ID",
            "MATCHUP",
            "SERIES_STATE",
            "WINNER",
        ]
    ].drop_duplicates()

    output = Path("data/models")
    output.mkdir(parents=True, exist_ok=True)

    dim_player.to_csv(output / "dim_player.csv", index=False)
    dim_team.to_csv(output / "dim_team.csv", index=False)
    dim_game.to_csv(output / "dim_game.csv", index=False)

    return dim_player, dim_team, dim_game

def create_fact_player_stats():
    players = pd.read_csv("data/processed/finals_player_stats_clean.csv")

    fact_player_stats = players.drop(
        columns=[
            "PLAYER_NAME",
            "TEAM_ABBREVIATION",
            "START_POSITION"
        ],
        errors="ignore"
    )

    output = Path("data/models")
    output.mkdir(parents=True, exist_ok=True)

    fact_player_stats.to_csv(output / "fact_player_stats.csv", index=False)

    return fact_player_stats