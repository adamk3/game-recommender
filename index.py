#First, We're going to use a few inputs from the user to try and recommend these games.
#The user is required to input their steam web API key, and their steam ID (or the steam ID of any public profile)

#We want to use the Steam Web API to extract some data from the user, as well as the year-in-review ((IF POSSIBLE))
#The year-in-review data will be the best way to recommend data based on user interactions

#the URL for the year-in-review site is this: https://store.steampowered.com/yearinreview/(steam_id_here)/2023

#To start we will dump the data gained from the user into a json file.
#using Steam Web API: https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_.28v0001.29

import pandas as pd
import requests
import json
import csv

#example steamID
steamID = '76561198116790116'

#get user input
#i need to ask for your steam API key, because these keys are not to be shared publicly, hence why mine isn't in this repo
#your key will only be stored on the client
key = input("Enter your steam API key: ")

#List of URLs to attain user data
recentlyPlayedUrl = 'https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key='+key+'&steamid='+steamID+'&format=json'

ownedGamesUrl = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='+key+'&steamid='+steamID+'&format=json'

#make a get request to the url
response = requests.get(recentlyPlayedUrl)

#check if the request was successful (status code 200)
if response.status_code == 200:
    #parse the JSON content
    json_content = response.json()

    #save the parsed content to a local file
    local_file_path = 'recent_data.json'
    
    with open(local_file_path, 'w', encoding='utf-8') as local_file:
        json.dump(json_content, local_file, ensure_ascii=False, indent=2)

    print(f"Successfully downloaded and saved JSON content to {local_file_path}")
else:
    print(f"Failed to download JSON content. Status Code: {response.status_code}")
    
    
response = requests.get(ownedGamesUrl)


#check if the request was successful (status code 200)
if response.status_code == 200:
    #parse the JSON content
    json_content = response.json()

    #save the parsed content to a local file
    local_file_path = 'owned_games.json'
    
    with open(local_file_path, 'w', encoding='utf-8') as local_file:
        json.dump(json_content, local_file, ensure_ascii=False, indent=2)

    print(f"Successfully downloaded and saved JSON content to {local_file_path}")
else:
    print(f"Failed to download JSON content. Status Code: {response.status_code}")
 
 
 
#we will now be taking the total playtime as user-interaction data.
#we can attain this from the owned_games.json generated file


# Load JSON data from the file
with open('owned_games.json', 'r') as file:
    data = json.load(file)
    
# Extract games
games = data["response"]["games"]

# CSV file path
csv_file_path = "games_data.csv"

# Write CSV header
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["appid", "playtime"])

# Write game data to CSV
with open(csv_file_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    for game in games:
        writer.writerow([game["appid"], game["playtime_forever"]])
        
#now we have a nice csv file, I want to parse it into a dataframe to be used for the training data

df = pd.read_csv('games_data.csv')