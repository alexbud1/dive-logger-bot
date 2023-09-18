import json

def get_phrase(language, key):
    # Load phrases from a JSON file
    with open(f"assets/{language}.json", "r", encoding="utf-8") as json_file:
        phrases = json.load(json_file)

    # Check if the language exists in the loaded phrases
    if key in phrases.keys(): 
        return phrases[key]
    else:
        raise Exception("Key not found in phrases")


