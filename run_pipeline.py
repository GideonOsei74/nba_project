import subprocess

steps = [
    "python3 -m src.main",
    "python3 -m src.feature_engineering",
    "python3 -m src.game_features",
    "python3 -m src.team_features",
]

for step in steps:
    print(f"\nRunning: {step}")
    subprocess.run(step, shell=True, check=True)

print("\nFull NBA analytics pipeline completed successfully.")