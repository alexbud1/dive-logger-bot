import json
import geopy
from geopy.geocoders import Nominatim
from deep_translator import GoogleTranslator
import certifi
import ssl
from assets.countries import countries_en, countries_uk

def get_phrase(language, key):
    # Load phrases from a JSON file
    with open(f"assets/{language}.json", "r", encoding="utf-8") as json_file:
        phrases = json.load(json_file)

    # Check if the language exists in the loaded phrases
    if key in phrases.keys(): 
        return phrases[key]
    else:
        raise Exception("Key not found in phrases")
    

def is_valid_country_name(input_string):
    return input_string.capitalize() in countries_en + countries_uk

def get_country_from_coordinates(latitude, longitude):
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
    
def translate_to_en(phrase):
    translation = GoogleTranslator(source='auto', target='en').translate(phrase)
    return translation