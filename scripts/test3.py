import json


file_path = './scripts/reference.json'

# Reading the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)


# Update scores
# s = data['events'][0]["competitions"][0]["situation"]["lastPlay"]["probability"]
espn_event = data['events'][0]["competitions"][0]
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