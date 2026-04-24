import pandas as pd

def load_data():
    df = pd.read_csv("data/future_match_probabilities_baseline.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df


def find_team_in_query(user_input, df):
    user_input = user_input.lower()

    teams = set(df['home_team']).union(set(df['away_team']))

    for team in teams:
        if str(team).lower() in user_input:
            return team

    return None