from pathlib import Path
from src.data_loader import build_finals_table, build_series_tracker, get_finals_player_stats
from src.data_cleaner import clean_finals_games, clean_player_stats
from src.data_processor import create_dimensions, create_fact_player_stats

def main():
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    df = build_finals_table()
    series = build_series_tracker(df)

    df.to_csv(raw_dir / "finals_games_raw.csv", index=False)
    series.to_csv(raw_dir / "finals_series_tracker_raw.csv", index=False)

    player_stats = get_finals_player_stats()
    player_stats.to_csv(raw_dir / "finals_player_stats_raw.csv", index=False)

    clean_games = clean_finals_games()
    clean_players = clean_player_stats()
    dim_player, dim_team, dim_game = create_dimensions()
    fact_player_stats = create_fact_player_stats()
    
    print("data/models/fact_player_stats.csv")
    print("Model tables created:")
    print("data/models/dim_player.csv")
    print("data/models/dim_team.csv")
    print("data/models/dim_game.csv")
    print("Cleaned files saved:")
    print("data/processed/finals_games_clean.csv")
    print("data/processed/finals_player_stats_clean.csv")
    print("Saved files:")
    print("data/raw/finals_games_raw.csv")
    print("data/raw/finals_series_tracker_raw.csv")
    print("data/raw/finals_player_stats_raw.csv")

    print(series[[
        "GAME_ID",
        "MATCHUP",
        "TEAM1",
        "TEAM1_PTS",
        "TEAM2",
        "TEAM2_PTS",
        "SERIES_STATE",
        "WINNER"
    ]])


if __name__ == "__main__":
    main()
