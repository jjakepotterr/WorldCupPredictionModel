##The kitchen (handles our logic)

from flask import Flask, request, jsonify
import pickle
import json

app = Flask(__name__) 

with open('model.pkl', 'rb') as f: # deserializes and opens our model pickle as a binary f = file
    model = pickle.load(f) # loads the file here

with open('label_encoder.pkl', 'rb') as f: # same thing but with label encoder which shows team name rather than team rep #
    le = pickle.load(f) # le means label encoder

with open('team_list.json', 'r') as f: # same thing with team list of names & data. rather than rb its r bc we are reading text not binary #
    team_list = json.load(f)

@app.route('/predict', methods = ['POST']) 
def predict(): # flask calls on this function whenever someone requests a prediction
    data = request.get_json() # gets data from json file via request
    team_name = data['team']
    if team_name not in team_list: # checks if team does not exist
        return jsonify({'error': 'Team not found'}), 404 # returns error message & asks for reinput

    team_enc = le.transform([team_name])[0]    # encodes the team_name into a number that represents it
    
    input_data = [[team_enc, team_enc, 0]]    # building input: teams (win/loss, Home/Away) vs average opponent on a neutral ground
    
    proba = model.predict_proba(input_data)[0]    # gets probabilities for [home win, draw, away win]
    
    win_prob = round(float(proba[0]) * 100, 1)     # win probability is index 0 (home win)

    return jsonify({
        'team': team_name,
        'win_probability': win_prob,    # calls upon format correctly using json schema
    }), 200


if __name__ == '__main__': # main backend code/doorway for flask when we call on backend we wish to run this file.
    app.run(debug=True) 