from utils import load_data, find_team_in_query

df = load_data()

def get_team_probability(user_input):
    team = find_team_in_query(user_input, df)

    if not team:
        return {"error": "Team not found. Try another country."}

    # Matches where team is home
    home_games = df[df['home_team'].str.lower() == team.lower()]
    home_win_prob = home_games['p_home_win']

    # Matches where team is away
    away_games = df[df['away_team'].str.lower() == team.lower()]
    away_win_prob = away_games['p_away_win']

    # Combine probabilities
    all_probs = list(home_win_prob) + list(away_win_prob)

    if len(all_probs) == 0:
        return {"error": "No data available for this team."}

    avg_prob = sum(all_probs) / len(all_probs)

    # Categorize
    if avg_prob >= 0.6:
        category = "Strong Contender"
        confidence = "High"
    elif avg_prob >= 0.3:
        category = "Moderate Chance"
        confidence = "Medium"
    else:
        category = "Underdog"
        confidence = "Low"

    return {
        "team": team,
        "win_probability": f"{round(avg_prob * 100)}%",
        "confidence_level": confidence,
        "category": category,
        "explanation": f"{team} has an estimated {round(avg_prob * 100)}% chance of winning based on aggregated match-level probabilities from the dataset."
    }