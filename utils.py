import json
import geopy
from geopy.geocoders import Nominatim
from deep_translator import GoogleTranslator
from caching.cache_language import LanguageCache
from aiogram import types
from aiogram.types import Message
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

async def send_error_message(message: Message, phrase: str) -> None:
    await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), phrase))

async def send_error_callback(callback: types.CallbackQuery, phrase: str) -> None:
    await callback.message.answer(get_phrase(await LanguageCache.get_user_language(callback.from_user.id), phrase))

async def create_profile_api(user_profile_data: dict, message: Message = None, callback: types.CallbackQuery = None) -> dict | None | requests.exceptions.RequestException:
    # URL of my endpoint
    url = "http://127.0.0.1:8000/user_profile/"

    # Define the headers with the token
    headers = {
        "token": os.getenv("DIVE_LOGGER_API_TOKEN"), # access token, which I give manually for apps.
        "Content-Type": "application/json",
    }

    # remove all None values from the dictionary
    user_profile_data = {key : value for key, value in user_profile_data.items() if value is not None}
    
    try:
        response = requests.post(url, headers=headers, json=user_profile_data)

        # Check the response status code
        if response.status_code == 201:
            data = response.json()
            return data
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            return None

    except requests.exceptions.RequestException as e:
        # Handle exceptions like connection errors, timeouts, etc.
        print(f"Request error: {e}")
        if message:
            await send_error_message(message, "server_error")
        elif callback:
            await send_error_callback(callback, "server_error")
        return None
    
    except Exception as e:
        # Handle any other exceptions
        print(f"Error: {e}")
        if message:
            await send_error_message(message, "server_error")
        elif callback:
            await send_error_callback(callback, "server_error")
        return None
    


async def get_profile_api(telegram_id: int, message: Message = None, callback: types.CallbackQuery = None) -> dict | None | str:
    # Define the API endpoint URL
    url = f"http://127.0.0.1:8000/user_profile/{telegram_id}"

    # Define the headers with the token
    headers = {
        "token": os.getenv("DIVE_LOGGER_API_TOKEN"), # access token, which I give manually for apps.
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            user_profile_data = response.json()
            return user_profile_data
        elif response.status_code == 404:
            print(f"User profile with telegram_id {telegram_id} not found")
            return "not_found"
        else:
            # Handle errors, raise an exception, or return None as needed
            print(f"Error: {response.status_code} - {response.text}")

            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        if message:
            await send_error_message(message, "server_error")
        elif callback:
            await send_error_callback(callback, "server_error")
        return None
    
async def update_profile_api(telegram_id: int, key: str, value: any, message: Message = None, callback: types.CallbackQuery = None) -> dict | None | requests.exceptions.RequestException:
    # Define the API endpoint URL
    url = f"http://127.0.0.1:8000/user_profile/{telegram_id}"

    # Define the headers with the token
    headers = {
        "token": os.getenv("DIVE_LOGGER_API_TOKEN"), # access token, which I give manually for apps.
        "Content-Type": "application/json",
    }

    # Define the data to be sent
    data = {
        key: value
    }

    try:
        response = requests.patch(url, headers=headers, json=data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            user_profile_data = response.json()
            return user_profile_data
        elif response.status_code == 404:
            print(f"User profile with telegram_id {telegram_id} not found")
            return "not_found"
        else:
            # Handle errors, raise an exception, or return None as needed
            print(f"Error: {response.status_code} - {response.text}")

            return None
        
    except requests.exceptions.RequestException as e:
        # Handle exceptions like connection errors, timeouts, etc.
        print(f"Request error: {e}")
        if message:
            await send_error_message(message, "server_error")
        elif callback:
            await send_error_callback(callback, "server_error")
        return None