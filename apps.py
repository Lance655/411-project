from flask import Flask, render_template, request, jsonify, Response
import requests
from backend import get_weather_for_date, calculate_weather_score, interpret_weather_score
import datetime

app = Flask(__name__, static_folder='', template_folder='')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/findEvents', methods=["GET", "POST"])
def find_events():
    target_date = request.form.get('event-date')
    city = request.form.get('city')
    weather_info = get_weather_for_date("TODO api_key",  city, target_date)
    weather_score = calculate_weather_score(weather_info)
    return render_template('events.html',weather_score=weather_score)


@app.route('/get_weather_categorizes', methods=["GET", "POST"])
def get_weather_categorizes():
    city = request.args.get('city')
    target_date = request.args.get('date')
    #eventName = request.args.get('eventName')

    weather_score = calculate_weather_score("TODO api_key", city, target_date)
    weather_categorizes = interpret_weather_score(weather_score)
    return weather_categorizes

if __name__ == "__main__":
    app.run(port=8080, debug=True)
