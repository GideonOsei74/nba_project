from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2
import pandas as pd


# ----------------------------
# STEP 1: GET RAW PLAYOFF DATA
# ----------------------------
def get_playoff_games(season="2023-24"):
    df = leaguegamefinder.LeagueGameFinder(season_nullable=season).get_data_frames()[0]

    df = df[df["GAME_ID"].str.startswith("004")]
    return df


# ----------------------------
# STEP 2: BUILD CLEAN GAME TABLE
# (2 teams per game enforced)
# ----------------------------
def build_games_table(season="2023-24"):
    df = get_playoff_games(season)

    df = df[["GAME_ID", "TEAM_ABBREVIATION", "PTS"]]

    games = []

    for game_id, group in df.groupby("GAME_ID"):
        if len(group) != 2:
            continue

        team1 = group.iloc[0]
        team2 = group.iloc[1]

        games.append({
            "GAME_ID": game_id,
            "TEAM1": team1["TEAM_ABBREVIATION"],
            "TEAM1_PTS": team1["PTS"],
            "TEAM2": team2["TEAM_ABBREVIATION"],
            "TEAM2_PTS": team2["PTS"],
        })

    return pd.DataFrame(games)


# ----------------------------
# STEP 3: BUILD SERIES TRACKER
# ----------------------------
def build_series_tracker(df):
    games = df.copy()

    # create matchup key (order-independent)
    games["MATCHUP"] = games.apply(
        lambda r: " vs ".join(sorted([r["TEAM1"], r["TEAM2"]])),
        axis=1
    )

    results = []

    # process each series separately
    for matchup, group in games.groupby("MATCHUP"):
        group = group.sort_values("GAME_ID").copy()

        team1, team2 = group["TEAM1"].iloc[0], group["TEAM2"].iloc[0]

        t1_wins = 0
        t2_wins = 0

        series_states = []
        winners = []

        for _, row in group.iterrows():
            winner = row["TEAM1"] if row["TEAM1_PTS"] > row["TEAM2_PTS"] else row["TEAM2"]

            if winner == team1:
                t1_wins += 1
            else:
                t2_wins += 1

            winners.append(winner)
            series_states.append(f"{t1_wins}-{t2_wins}")

        group["WINNER"] = winners
        group["SERIES_STATE"] = series_states

        results.append(group)

    return pd.concat(results).sort_values("GAME_ID")


def build_finals_table(season="2023-24"):
    games = build_games_table(season)

    # NBA Finals games are Round 4
    finals = games[games["GAME_ID"].str[5:8] == "004"].copy()

    return finals

def get_finals_player_stats(season="2023-24"):
    finals = build_finals_table(season)

    all_players = []

    for game_id in finals["GAME_ID"]:
        print(f"Fetching box score for game {game_id}...")

        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
        player_stats = boxscore.get_data_frames()[0]

        player_stats["GAME_ID"] = game_id
        all_players.append(player_stats)

    return pd.concat(all_players, ignore_index=True)