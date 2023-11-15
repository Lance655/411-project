import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# ------------------------------------ WEATHER API ----------------------------------------- #

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
# print(weather_data)

def get_weather_for_date(api_key, city, target_date):
   
    url = "https://api.tomorrow.io/v4/weather/forecast?location={city}&apikey=Kf6jEI6LHSzOUU4a7QE6PzrFw6PZy4Ea&timesteps=daily"
    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = response.json()
        daily_timelines = weather_data.get('timelines', {}).get('daily', [])

        for daily_data in daily_timelines:
            # Parse the date from the "time" string
            date_from_api = datetime.strptime(daily_data.get('time'), "%Y-%m-%dT%H:%M:%SZ").date()
            
            # Parse the target date
            target_date_parsed = datetime.strptime(target_date, "%Y-%m-%d").date()

            # Compare only the date part
            if date_from_api == target_date_parsed:
                return daily_data.get('values', {})

    return None

weather_vals = get_weather_for_date(TOMORROWIO_API_KEY, "new york", "2023-11-17")
print(weather_vals)



# ------------------------------------ EVENTS API ----------------------------------------- #



url = "https://real-time-events-search.p.rapidapi.com/search-events"

querystring = {"query":"Concerts in San-Francisco","start":"0"}

headers = {
	"X-RapidAPI-Key": "6319ba4d96mshf4bc1f385f347ddp133906jsnfea5e88cf1ab",
	"X-RapidAPI-Host": "real-time-events-search.p.rapidapi.com"
}

# Commented out the API call below. Only use sparingly --> don't go over limit
# response = requests.get(url, headers=headers, params=querystring)
#
# print(response.json())

