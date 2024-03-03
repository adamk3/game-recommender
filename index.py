# First, We're going to use a few inputs from the user to try and recommend these games.
# The user is required to input their steam web API key, and their steam ID (or the steam ID of any public profile)

# We want to use the Steam Web API to extract some data from the user, as well as the year-in-review ((IF POSSIBLE))
# The year-in-review data will be the best way to recommend data based on user interactions

# the URL for the year-in-review site is this: https://store.steampowered.com/yearinreview/(steam_id_here)/2023

# To start we will dump the data gained from the user into a JSON file.
# using Steam Web API: https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_.28v0001.29

import pandas as pd
import requests
import json
import csv
import os

# Get the directory where index.py is located
script_directory = os.path.dirname(os.path.realpath(__file__))

# Change the current working directory to the directory where index.py is located
os.chdir(script_directory)

def save_json_data(url, file_path):
    """
    Function to download JSON data from the given URL and save it to the specified file path.
    """
    response = requests.get(url)
    if response.status_code == 200:
        json_content = response.json()
        with open(file_path, 'w', encoding='utf-8') as local_file:
            json.dump(json_content, local_file, ensure_ascii=False, indent=2)
        print(f"Successfully downloaded and saved JSON content to {file_path}")
    else:
        print(f"Failed to download JSON content from {url}. Status Code: {response.status_code}")

# Example steamID
steamID = '76561198297963461'

# Get user input
key = input("Enter your steam API key: ")

# List of URLs to attain user data
recentlyPlayedUrl = f'https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={steamID}&format=json'
ownedGamesUrl = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamID}&format=json'

# Save recent data
save_json_data(recentlyPlayedUrl, 'recent_data.json')

# Save owned games data
save_json_data(ownedGamesUrl, 'owned_games.json')

# Load JSON data for owned games from the file
with open('owned_games.json', 'r') as file:
    owned_games_data = json.load(file)

# Extract games
owned_games = owned_games_data["response"]["games"]

# Load JSON data for all games from the file
with open('games.json', 'r', encoding='utf-8') as file:
    all_games_data = json.load(file)

# CSV file path
csv_file_path = "games_data.csv"

# Write CSV header with additional columns for developer and genre
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["appid", "playtime", "developer", "genre", "description"])

# Write game data to CSV
with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for game in owned_games:
        app_id = game["appid"]
        playtime = game["playtime_forever"]
        developer = "Not Found"  # Default value if developer is not found
        genre = "Not Found"  # Default value if genre is not found
        description = "Description Not Found" # Default value if description is not found
        if str(app_id) in all_games_data:
            developer = all_games_data[str(app_id)]['developers'][0] if all_games_data[str(app_id)]['developers'] else "Unknown"
            genre = ', '.join(all_games_data[str(app_id)]['genres']) if all_games_data[str(app_id)]['genres'] else "Unknown"
            description = all_games_data[str(app_id)].get('detailed_description', 'Description Not Found')
        writer.writerow([app_id, playtime, developer, genre, description])

# Now we have a nice CSV file, parse it into a dataframe for the training data
df = pd.read_csv('games_data.csv')