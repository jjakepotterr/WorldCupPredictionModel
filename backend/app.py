##The kitchen (handles our logic)

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import json

app = Flask(__name__) 
CORS(app, origins=["http://localhost:5173"])

with open('model.pkl', 'rb') as f: # deserializes and opens our model pickle as a binary f = file
    model = pickle.load(f) # loads the file here

with open('label_encoder.pkl', 'rb') as f: # same thing but with label encoder which shows team name rather than team rep #
    le = pickle.load(f) # le means label encoder

with open('team_list.json', 'r') as f: # same thing with team list of names & data. rather than rb its r bc we are reading text not binary #
    team_list = json.load(f)

@app.route('/predict', methods = ['POST']) 
def predict(): # flask calls on this function whenever someone requests a prediction
    data = request.get_json() # gets data from json file via request
    raw_input = data['team'].strip().lower() # .strip() removes extra spaces and .title() capitalizes first letter of each word so "brazil" becomes "Brazil" helps with discovering team in natural language sentence.
    
    # Search through team list to find which team is mentioned
    team_name = None
    for t in team_list:
        if t.lower() in raw_input:
            team_name = t
            break

    if not team_name:
        return jsonify({'error': 'No team found in your message. Try mentioning a country name!'}), 404
    
    team_enc = le.transform([team_name])[0]    # encodes the team_name into a number that represents it
    
    input_data = [[team_enc, team_enc, 0]]    # building input: teams (win/loss, Home/Away) vs average opponent on a neutral ground
    
    proba = model.predict_proba(input_data)[0]    # gets probabilities for [home win, draw, away win]
    
    win_prob = round(float(proba[0]) * 100, 1)     # win probability is index 0 (home win)

    # Generate explanation based on probability
    if win_prob >= 70:
        explanation = f"{team_name} is a dominant force with strong historical performance."
    elif win_prob >= 50:
        explanation = f"{team_name} has a solid chance, consistently performing well internationally."
    elif win_prob >= 35:
        explanation = f"{team_name} is competitive but faces tough opposition."
    else:
        explanation = f"{team_name} is an underdog but upsets are always possible in football."

    all_teams_probs = []                                   # Finds what other team is closest in comparison to the team selected
    for t in team_list:
        try:
            t_enc = le.transform([t])[0]
            t_input = [[t_enc, t_enc, 0]]
            t_proba = model.predict_proba(t_input)[0]
            t_prob = round(float(t_proba[0]) * 100, 1)
            all_teams_probs.append((t, t_prob))
        except:
            continue

   
    all_teams_probs.sort(key=lambda x: abs(x[1] - win_prob)) # Sort by how close they are to our team's probability

    closest = next((t for t in all_teams_probs if t[0] != team_name), None)    # First result is the team itself, second is the closest comparison other team

    return jsonify({                       # returns a json schema structured answer to frontend
        'team': team_name,
        'win_probability': win_prob,
        'explanation': explanation,
        'closest_team': closest[0] if closest else None,
        'closest_prob': closest[1] if closest else None,
    }), 200


if __name__ == '__main__': # main backend code/doorway for flask when we call on backend we wish to run this file.
    app.run(debug=True, port=5001)
