import pandas as pd

def load_placeholder_data():
    data = {
        "team": ["Team A", "Team B"],
        "points": [100, 95]
    }
    return pd.DataFrame(data)