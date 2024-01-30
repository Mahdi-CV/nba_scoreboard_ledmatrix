import json

# File path of the JSON file
file_path = './espn_event_data.json'

# Reading the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)

# Pretty-printing the JSON data
pretty_json = json.dumps(data, indent=4)

# Writing the pretty-printed JSON back to the file
with open(file_path, 'w') as file:
    file.write(pretty_json)

print(f"Pretty-printed JSON has been saved to {file_path}")
