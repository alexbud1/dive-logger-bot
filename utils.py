import json
import geopy
from geopy.geocoders import Nominatim
from deep_translator import GoogleTranslator
import certifi
import ssl
from assets.countries import countries_en, countries_uk
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

# .env adjustments
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def get_phrase(language: str, key: str) -> str:
    # Load phrases from a JSON file
    with open(f"assets/{language}.json", "r", encoding="utf-8") as json_file:
        phrases = json.load(json_file)

    # Check if the language exists in the loaded phrases
    if key in phrases.keys(): 
        return phrases[key]
    else:
        raise Exception("Key not found in phrases")
    
# This function is used to check if the user's input is a valid country name by two files in assets/
def is_valid_country_name(input_string: str) -> bool:
    return input_string.capitalize() in countries_en + countries_uk

# This function is used to get a country by coordinates using the Nominatim geocoder
def get_country_from_coordinates(latitude: float, longitude: float) -> str:
    # Create the SSL context, without it an exception is thrown
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx

    # Initialize the Nominatim geocoder
    geolocator = Nominatim(scheme='http', user_agent="dive-logger-bot")

    try:
        # Get the location information based on the coordinates
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        
        # Extract the country from the location information
        country = location.raw.get("address", {}).get("country", "Unknown")
        
        return translate_to_en(country)
    except Exception as e:
        print(f"Error retrieving country from coordinates: {e}")
        return "Unknown"
    
def translate_to_en(phrase: str) -> str:
    translation = GoogleTranslator(source='auto', target='en').translate(phrase)
    return translation

def create_profile_api(user_profile_data: dict) -> dict | None | requests.exceptions.RequestException:
    # Define the URL of your endpoint
    url = "http://127.0.0.1:8000/user_profile/"

    # Define the headers with the token
    headers = {
        "token": os.getenv("DIVE_LOGGER_API_TOKEN"),
        "Content-Type": "application/json",  # Set the content type as JSON
    }

    try:
        # Send a POST request to the endpoint with the headers and JSON data
        response = requests.post(url, headers=headers, json=user_profile_data)

        # Check the response status code
        if response.status_code == 201:
            # Request was successful, you can parse the JSON response
            data = response.json()
            return data
        else:
            # Request failed, handle the error as needed
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            return None

    except requests.exceptions.RequestException as e:
        # Handle exceptions like connection errors, timeouts, etc.
        print(f"Request error: {e}")
        return None