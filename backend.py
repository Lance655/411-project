import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOMORROWIO_API_KEY = os.getenv("Kf6jEI6LHSzOUU4a7QE6PzrFw6PZy4Ea")  # Remember .env file!

def get_weather(location, api_key):
    url = "https://api.tomorrow.io/v4/weather/forecast?location=new%20york&apikey=Kf6jEI6LHSzOUU4a7QE6PzrFw6PZy4Ea&timesteps=daily"
    params = {
        "location": location,
        "fields": "temperature",
        "units": "imperial",  # You can adjust units as needed (e.g., "metric")
        "apikey": api_key,
    }
    response = requests.get(url, params=params)
    return response.json()

# Replace 'latitude,longitude' with the actual coordinates of your location
location = "latitude,longitude"
weather_data = get_weather(location, TOMORROWIO_API_KEY)
print(weather_data)
print()
print()
print("sup bro")
print(weather_data['timelines']['daily'][2])

# Specify the target date in the format 'YYYY-MM-DD'
target_date = "2023-11-04"

# Iterate through the daily timelines to find the one that matches the target date
target_timeline = None
for daily_timeline in weather_data['timelines']['daily']:
    if daily_timeline['time'] == target_date:
        target_timeline = daily_timeline
        break




