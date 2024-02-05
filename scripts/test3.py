import json


file_path = './scripts/test.json'

# Reading the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)


# Update scores
# s = data['events'][0]["competitions"][0]["situation"]["lastPlay"]["probability"]
espn_event = data['events'][0]["competitions"][0]

for d in data['events']:
    game_data = d["competitions"][0]
    if 'situation' in game_data and 'lastPlay' in game_data['situation'] and 'probability' in game_data['situation']['lastPlay']:
        probabilities = game_data['situation']['lastPlay']['probability']
        home_win_percentage = probabilities.get('homeWinPercentage', None)
        away_win_percentage = probabilities.get('awayWinPercentage', None)
        print(f"Home Win Percentage: {home_win_percentage}")
        print(f"Away Win Percentage: {away_win_percentage}")
    else:
        print("Win percentages not found.")


#print(data['events'][2])
# Update probabilities if available
if ('situation' in espn_event and 
    'lastPlay' in espn_event['situation'] and 
    'probability' in espn_event['situation']['lastPlay']):
    probabilities = espn_event['situation']['lastPlay']['probability']

    # Extract probabilities with defaults
    home_win_probability = int(round(probabilities.get('homeWinPercentage', 0), 2) * 100)
    away_win_probability = int(round(probabilities.get('awayWinPercentage', 0), 2) * 100)
    tie_probability = probabilities.get('tiePercentage', 0)
    print(home_win_probability)
    print(away_win_probability)
# Additional updates and error handling can be added here


#print(s)