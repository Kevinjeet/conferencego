import requests
import json
from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY

def get_photo(city, state):
    # Create a dictionary for the headers to use in the request
    # Create the URL for the request with the city and state
    # Make the request
    # Parse the JSON response
    # Return a dictionary that contains a `picture_url` key and
    #   one of the URLs for one of the pictures in the response
    url = "https://api.pexels.com/v1/search"
    params = {
        "per_page": 1,
        "query": city + " " + state}
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, params=params, headers=headers)
    content = json.loads(response.content)
    try:
        return {
        "picture_url": content["photos"][0]["src"]["original"]
        }
    except (KeyError, IndexError):
        return {"picture_url": None}


def get_weather_data(city, state):
    # Create the URL for the geocoding API with the city and state
    # Make the request
    # Parse the JSON response
    # Get the latitude and longitude from the response
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    params_geo = {
        "appid": OPEN_WEATHER_API_KEY,
        "q": f"{city},{state},US",}
    response = requests.get(geo_url, params=params_geo)
    content = json.loads(response.content)
    lat = content[0]["lat"]
    lon = content[0]["lon"]

    # Create the URL for the current weather API with the latitude
    #   and longitude
    # Make the request
    # Parse the JSON response
    # Get the main temperature and the weather's description and put
    #   them in a dictionary
    # Return the dictionary
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    params_weather = {
        "appid": OPEN_WEATHER_API_KEY,
        "lat": lat,
        "lon": lon,
    }
    response1 = requests.get(weather_url, params=params_weather)
    content1 = json.loads(response1.content)
    return {
        "temps": content1["main"]["temp"],
        "description": content1["weather"][0]["description"],
    }
