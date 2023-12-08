from flask import Flask, render_template, request, jsonify, Response, redirect, session
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os
from backend import get_event, format_event_response, get_weather_for_date, calculate_weather_score, interpret_weather_score
import datetime
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


app = Flask(__name__)
CORS(app)

TOMORROWIO_API_KEY = os.getenv("Kf6jEI6LHSzOUU4a7QE6PzrFw6PZy4Ea")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def events():
    return render_template('events.html')



@app.route('/findEvents', methods=["GET", "POST"])
def find_events():
    try:
        # Extract the JSON data from the request
        data = request.get_json()
        target_date = data.get('date')
        city = data.get('city')
        
        # Retrieve events using the function from backend.py
        api_response = get_event(city)
        if api_response.status_code != 200:
            # If the API call was unsuccessful, return an error message
            return jsonify({'error': 'Failed to retrieve events'}), api_response.status_code
        
        # Format the events response
        events_data = format_event_response(api_response.json())
        
        # Calculate the weather score using the function from backend.py
    
        weather_score = calculate_weather_score(TOMORROWIO_API_KEY, city, target_date)
        
        # Interpret the weather score using the function from backend.py
        weather_interpretation = interpret_weather_score(weather_score)

        # COMMENTED THIS SECTION OUT TO SEE IF THIS WAS THE PROBLEM: 
        
        # Assign a recommendation level to each event based on the weather score
        #print("sup bro")
        #for event in events_data:
        #    event['recommendationLevel'] = weather_interpretation
        #print("elmo")
        
        # Return the data as a JSON response
        return jsonify({
            'events': events_data,
            'weather_score': weather_score,
            'weather_interpretation': weather_interpretation
        })
    except Exception as e:
        # Log the error and return an error message
        print(f"Error occurred: {e}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

@app.route('/get_weather_categorizes', methods=["GET", "POST"])
def get_weather_categorizes():
    if request.method == 'POST':
        data = request.json
        city = data.get('city')
        target_date = data.get('date')
    else:  # GET method
        city = request.args.get('city')
        target_date = request.args.get('date')

    api_key = TOMORROWIO_API_KEY
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 500

    weather_score = calculate_weather_score(api_key, city, target_date)
    weather_categorizes = interpret_weather_score(weather_score)
    return jsonify({'weather_categorization': weather_categorizes})


#MongoDB setup
uri = 'mongodb+srv://user:1234@411project.afvtwb4.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.database
users_collection = db.users

#for OAUTH
@app.route('/oauth2callback')
def oauth2callback():
    # Step 1: Get the authorization code from the callback
    auth_code = request.args.get('code')

    # Step 2: Exchange the authorization code for an access token
    token_request_data = {
        'code': auth_code,
        'client_id': '454906782018-8bvt438shm4f1mvkj1h8ic126pnrhmr9.apps.googleusercontent.com',
        'client_secret': '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',
        'redirect_uri': 'http://127.0.0.1:8080/oauth2callback',
        'grant_type': 'authorization_code'
    }
    token_response = requests.post(
        'https://oauth2.googleapis.com/token',
        data=token_request_data
    )
    token_response_json = token_response.json()
    access_token = token_response_json.get('access_token')

    # Step 3: Use the access token to fetch user data from Google's API
    user_info_response = requests.get(
        'https://www.googleapis.com/oauth2/v2/userinfo',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    user_info = user_info_response.json()
    user_id = user_info.get('id')
    user_name = user_info.get('name')
    #print(user_id, user_name)

    insert_result = users_collection.insert_one(user_info)


    # Redirect to a different page or handle the data as needed
    return redirect('/')

app.secret_key = '1234'


if __name__ == "__main__":
    app.run(port=8080, debug=True)
