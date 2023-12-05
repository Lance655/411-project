import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()



# ------------------------------------ WEATHER API ----------------------------------------- #



TOMORROWIO_API_KEY = os.getenv("Kf6jEI6LHSzOUU4a7QE6PzrFw6PZy4Ea")



# This method takes as input a location and api key and returns the weather values for the next 5 days - (testing method)
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


# This method takes as input the city and target date and returns the weather values for that day - (helper method for calculate_weather_score)
def get_weather_for_date(api_key, city, target_date):

    url = f"https://api.tomorrow.io/v4/weather/forecast?location={city}&apikey=Kf6jEI6LHSzOUU4a7QE6PzrFw6PZy4Ea&timesteps=daily"
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


# This method takes as input the weather_data for a day and calculates the corresponding score
def calculate_weather_score(api_key, city, target_date):
    weather_data = get_weather_for_date(api_key, city, target_date)
    print("weather data is", weather_data)
    # Define weights for each criterion (adjust as needed)
    weights = {
        'temperature_max': -0.5,
        'precipitation_probability_avg': -0.3,
        'wind_speed_max': -0.2,
        'cloud_cover_avg': -0.1,
        'snowAccumulationAvg': -0.3
        # Add more criteria and adjust weights as needed
    }

    # Extract relevant weather data
    temperature_max = weather_data['temperatureMax']
    precipitation_probability_avg = weather_data['precipitationProbabilityAvg']
    wind_speed_max = weather_data['windSpeedMax']
    cloud_cover_avg = weather_data['cloudCoverAvg']
    snow_accumulation_avg = weather_data['snowAccumulationAvg']


    # Calculate the weather score
    weather_score = (
        weights['temperature_max'] * temperature_max +
        weights['precipitation_probability_avg'] * precipitation_probability_avg +
        weights['wind_speed_max'] * wind_speed_max +
        weights['cloud_cover_avg'] * cloud_cover_avg +
        weights['snowAccumulationAvg'] * snow_accumulation_avg
        # Add more terms for other criteria
    )

    print("weather score is ", weather_score)
    #weather_result = interpret_weather_score(weather_score)


    return weather_score


# This method categorizes the weather scores - (helper method for calculate_weather_score)
def interpret_weather_score(weather_score):
    if weather_score < -20.0:
        return "Avoid"
    elif -20.0 <= weather_score < -15.0:
        return "Not Ideal"
    elif -15.0 <= weather_score < -5.0:
        return "Fair"
    elif -5.0 <= weather_score < -3.0:
        return "Good"
    else:
        return "Excellent"




## ---- TESTING -----


#result = calculate_weather_score(TOMORROWIO_API_KEY, "new york", datetime.now().strftime("%Y-%m-%d"))
#print(result)
#print("hello world")
weather_vals = get_weather_for_date(TOMORROWIO_API_KEY, "new york", "2023-11-19")
print(weather_vals)

weather_vals = {'cloudBaseAvg': 1.25, 'cloudBaseMax': 5.08, 'cloudBaseMin': 0, 'cloudCeilingAvg': 2.32, 'cloudCeilingMax': 8.05, 'cloudCeilingMin': 0, 'cloudCoverAvg': 65.12, 'cloudCoverMax': 100, 'cloudCoverMin': 1, 'dewPointAvg': 5.06, 'dewPointMax': 8.86, 'dewPointMin': 2.88, 'evapotranspirationAvg': 0.03, 'evapotranspirationMax': 0.104, 'evapotranspirationMin': 0, 'evapotranspirationSum': 0.689, 'freezingRainIntensityAvg': 0, 'freezingRainIntensityMax': 0, 'freezingRainIntensityMin': 0, 'humidityAvg': 91.71, 'humidityMax': 95, 'humidityMin': 80.29, 'iceAccumulationAvg': 0, 'iceAccumulationLweAvg': 0, 'iceAccumulationLweMax': 0, 'iceAccumulationLweMin': 0, 'iceAccumulationLweSum': 0, 'iceAccumulationMax': 0, 'iceAccumulationMin': 0, 'iceAccumulationSum': 0, 'moonriseTime': '2023-11-17T12:08:14Z', 'moonsetTime': '2023-11-17T19:06:07Z', 'precipitationProbabilityAvg': 16.3, 'precipitationProbabilityMax': 70, 'precipitationProbabilityMin': 0, 'pressureSurfaceLevelAvg': 1018.16, 'pressureSurfaceLevelMax': 1020.04, 'pressureSurfaceLevelMin': 1013.8, 'rainAccumulationAvg': 0.16, 'rainAccumulationLweAvg': 0.16, 'rainAccumulationLweMax': 0.86, 'rainAccumulationLweMin': 0, 'rainAccumulationMax': 0.86, 'rainAccumulationMin': 0, 'rainAccumulationSum': 3.67, 'rainIntensityAvg': 0.14, 'rainIntensityMax': 0.86, 'rainIntensityMin': 0, 'sleetAccumulationAvg': 0, 'sleetAccumulationLweAvg': 0, 'sleetAccumulationLweMax': 0, 'sleetAccumulationLweMin': 0, 'sleetAccumulationLweSum': 0, 'sleetAccumulationMax': 0, 'sleetAccumulationMin': 0, 'sleetIntensityAvg': 0, 'sleetIntensityMax': 0, 'sleetIntensityMin': 0, 'snowAccumulationAvg': 0, 'snowAccumulationLweAvg': 0, 'snowAccumulationLweMax': 0, 'snowAccumulationLweMin': 0, 'snowAccumulationLweSum': 0, 'snowAccumulationMax': 0, 'snowAccumulationMin': 0, 'snowAccumulationSum': 0, 'snowIntensityAvg': 0, 'snowIntensityMax': 0, 'snowIntensityMin': 0, 'sunriseTime': '2023-11-17T07:10:00Z', 'sunsetTime': '2023-11-17T16:20:00Z', 'temperatureApparentAvg': 5.36, 'temperatureApparentMax': 10.34, 'temperatureApparentMin': 0.84, 'temperatureAvg': 6.33, 'temperatureMax': 10.34, 'temperatureMin': 3.63, 'uvHealthConcernAvg': 0, 'uvHealthConcernMax': 0, 'uvHealthConcernMin': 0, 'uvIndexAvg': 0, 'uvIndexMax': 0, 'uvIndexMin': 0, 'visibilityAvg': 12.45, 'visibilityMax': 16, 'visibilityMin': 4.16, 'weatherCodeMax': 1001, 'weatherCodeMin': 1001, 'windDirectionAvg': 212.01, 'windGustAvg': 4.98, 'windGustMax': 10.22, 'windGustMin': 2.79, 'windSpeedAvg': 2.96, 'windSpeedMax': 6.07, 'windSpeedMin': 1.79}


#location = "New York"
#weather_data = get_weather(location, TOMORROWIO_API_KEY)
#print(weather_data)





# ------------------------------------ EVENTS API ----------------------------------------- #

url = "https://real-time-events-search.p.rapidapi.com/search-events"

headers = {
	"X-RapidAPI-Key": "6319ba4d96mshf4bc1f385f347ddp133906jsnfea5e88cf1ab",
	"X-RapidAPI-Host": "real-time-events-search.p.rapidapi.com"
}

#This method calls the API with given location and returns the response call
def get_event(location):
    query = f"Event in {location}"  # Use the location variable to construct the query
    querystring = {"query": query, "start": "0"}  # Construct the querystring with the dynamic query
    return requests.get(url, headers=headers, params=querystring)

#This will return a formatting string listing the events returned by AP
def format_event_response(api_response):
  formatted_response = ""
  events = api_response.get('data', [])

  for i, event in enumerate(events, start=1):
      name = event.get('name', 'No name provided')
      location = event.get('venue', {}).get('full_address', 'No location provided')
      start_time = event.get('start_time', 'No start time provided')
      formatted_response += f"Event {i}\nName: {name}\nLocation: {location}\nTime: {start_time}\n\n"

  return formatted_response

#This returns a list of all the Event Names in order
def get_event_names(api_response):
    events = api_response.get('data', [])
    return [event.get('name', 'No name provided') for event in events]

#This returns a list of all the Event dates in order
def get_event_dates(api_response):
    events = api_response.get('data', [])
    return [event.get('start_time', 'No start time provided').split(' ')[0] for event in events]

#This returns a list of all the Event locations in order
def get_event_locations(api_response):
    events = api_response.get('data', [])
    return [event.get('venue', {}).get('full_address', 'No location provided') for event in events]


## ---- TESTING -----
"""
# Ask user for location
user_location = input("Enter a location to search for events: ")

# Call API to get events for the given location
api_response = get_event(user_location).json()

# Print formatted event details
print("Formatted Event Details:")
formatted_events = format_event_response(api_response)
print(formatted_events)

# Print list of event names
print("Event Names:")
event_names = get_event_names(api_response)
print(event_names)

# Print list of event dates
print("Event Dates:")
event_dates = get_event_dates(api_response)
print(event_dates)

# Print list of event locations
print("Event Locations:")
event_locations = get_event_locations(api_response)
print(event_locations)

"""

