from flask import Flask, render_template, request, jsonify, Response
import requests
from dotenv import load_dotenv
import os
from backend import get_event, format_event_response, get_weather_for_date, calculate_weather_score, interpret_weather_score
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/findEvents', methods=["GET", "POST"])
def find_events():
    target_date = request.form.get('event-date')
    city = request.form.get('city')
    print(city)
    weather_info = get_weather_for_date("TODO api_key",  city, target_date)
    weather_score = calculate_weather_score("Kf6jEI6LHSzOUU4a7QE6PzrFw6PZy4Ea", city, target_date)
    return render_template('events.html',weather_score=weather_score)

        # Assign a recommendation level to each event based on the weather score
        for event in events_data:
            event['recommendationLevel'] = weather_interpretation
        
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

    api_key = os.getenv('TOMORROWIO_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 500

    weather_score = calculate_weather_score(api_key, city, target_date)
    weather_categorizes = interpret_weather_score(weather_score)
    return weather_score

if __name__ == "__main__":
    app.run(port=8080, debug=True)
