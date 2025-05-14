from dotenv import load_dotenv
from flask import Flask, jsonify, request
import requests
import json
import os

app = Flask(__name__)

API_KEY = os.environ.get('WEATHER_API_KEY')

if API_KEY:
    print("API Key loaded successfully!")
else:
    print("API Key not found!")

def display_readable_json(loaded_json):
    print(json.dumps(loaded_json, indent=4))

def get_latitude_longitude(city_name, country_name, loaded_json):
    for entry in loaded_json:

        city = entry["name"]
        country = entry["country"]

        longtiude = entry["lon"]
        latitude = entry["lat"]

        if city_name == city and country_name == country:
            return latitude, longtiude
    return None, None

def between_range(i, j, num):
    return i <= num <= j

@app.route('/weather-sentiment', methods=['POST'])
def get_sentiment():
    #incomes.append(request.get_json())

    data = request.get_json()
    city_name = data.get('city', 'London')
    country_name = data.get('country', 'GB')
    print(city_name)

    
    
    # with the city name and `requests` get the coordinates for the city

    coordinates_response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={API_KEY}")
    #print(coordinates_response.status_code, display_readable_json(coordinates_response.json()))

    lat, lon = get_latitude_longitude(city_name, country_name, coordinates_response.json())
    print(f"found our city located at {lat}, {lon}")

    if lat is None or lon is None:
        return jsonify({"error": "City not found"}), 404

    # use the coordinates to get the weather data
    weather_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}")
    #print(coordinates_response.status_code, display_readable_json(weather_response.json()))

    # TODO: craft more of the response and find all weather condition codes and its done

    weather_json = weather_response.json()
    weather_id = weather_json["weather"][0]["id"]
    print(weather_id)

    weather_sentiment = "neutral"

    # https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
    # thunderstorm
    if between_range(200, 232, weather_id): 
        weather_sentiment = "anxious"
    elif between_range(300, 321, weather_id):
        weather_sentiment = "melancholy"
    elif weather_id == 511: # freezing rain
        weather_sentiment = "miserable"
    elif between_range(520, 531, weather_id):
        weather_sentiment = "moody"
    elif between_range(600, 602, weather_id):
        weather_sentiment = "cozy"
    elif between_range(611, 616, weather_id):
        weather_sentiment = "uncomfortable"
    elif between_range(620, 622, weather_id):
        weather_sentiment = "calm"
    elif between_range(701, 741, weather_id):
        weather_sentiment = "sleepy"
    elif between_range(751, 761, weather_id):
        weather_sentiment = "irritated"
    elif weather_id == 762:
        weather_sentiment = "worried"
    elif weather_id == 771:
        weather_sentiment = "anxious"
    elif weather_id == 781:
        weather_sentiment = "fearful"
    elif weather_id == 800:
        weather_sentiment = "happy"
    elif between_range(801, 802, weather_id):
        weather_sentiment = "neutral"
    elif weather_id == 803:
        weather_sentiment = "indifferent"
    elif weather_id ==  804:
        weather_sentiment = "gloomy"
    
    print(weather_sentiment)

    output = {
        "city":  city_name,
        "country": country_name,
        "sentiment": weather_sentiment,
               }

    return jsonify(output), 200