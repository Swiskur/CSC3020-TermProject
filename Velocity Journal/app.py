import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os


# Initialize Flask app
app = Flask(__name__)

# Creates file paths for JSON storage for velocity and journal entries
VELOCITY_PATH = 'velocities.json'
JOURNAL_PATH = 'journal_entries.json'

# Helper functions to load and save JSON data
def load_json(file_path):

    # If the file does not exist, it will return empty list
    if not os.path.exists(file_path):
        return []
    
    # When opened it will try to load JSON data, if it fails it will return an empty list
    with open(file_path, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []
        
# Saves the data to JSON file  
def save_json(file_path, data):

    # It will write data to the specified JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Creates a route for the home page
@app.route('/')
def index():

    # returns the index.html template
    return render_template('index.html')

# Creates a route for the velocity tracker page with POST and GET methods
@app.route('/velocity_tracker', methods=['POST', 'GET'])
def velocity_tracker():

    # if the request method is POST it will get the date and velocity from the form entered by the user
    if request.method == 'POST':
        date = request.form.get('date')
        velocity = request.form.get('velocity')

        # if date or velocity is missing it will redirect the user back to the velocity tracker page
        if not date or not velocity:
            return redirect(url_for('velocity_tracker'))
        
        # if both date and velocity are present it will load existing velocities, append  a new entry, and save them back to JSON
        if date and velocity:
            velocities = load_json(VELOCITY_PATH)
            velocities.append({"date": date, "velocity": velocity})
            save_json(VELOCITY_PATH, velocities)
        return redirect(url_for('velocity_tracker'))
 
    # For GET requests it load existing velocities and renders them to the velocity_tracker.html template
    velocity = load_json(VELOCITY_PATH)
    return render_template('velocity_tracker.html', velocity=velocity)

# Creates a route for the journal tracker page with POST and GET methods
@app.route('/journal_tracker', methods=['POST', 'GET'])
def journal_tracker():

    # if the request method is POST it will get the date and user entry from the form
    if request.method == 'POST':
        date = request.form.get('journalDate')
        entry = request.form.get('journalEntry')

        # if date or entry is missing it will redirect user back to the journal entry page
        if not date or not entry:
            return redirect(url_for('journal_tracker'))
        
        # if both date and entry are present it will load the existing journal entries, append a new entry, and save it back to JSON
        if date and entry:
            journal_entries = load_json(JOURNAL_PATH)
            journal_entries.append({"date": date, "entry": entry})
            save_json(JOURNAL_PATH, journal_entries)
        return redirect(url_for('journal_tracker'))

    # For GET requests it loads the existing journal entries and renders the journal.html template
    journal_entries = load_json(JOURNAL_PATH)
    return render_template('journal.html', journal_entries=journal_entries)

# Runs the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)