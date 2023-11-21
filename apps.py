from flask import Flask, render_template, request, jsonify, Response
import requests
from backend import get_weather_for_date, calculate_weather_score
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/findEvents', methods=["GET", "POST"])
def find_events():
    target_date = request.form.get('event-date')
    city = request.form.get('city')
    weather_info = get_weather_for_date("TODO",  city, target_date)
    weather_score = calculate_weather_score(weather_info)
    return render_template('events.html',weather_score=weather_score)



if __name__ == "__main__":
    app.run(port=8080, debug=True)