import os
import json
import glob

# Folder containing the JSON files
input_folder = 'dbench-gpt4'  # Change this to your folder name
output_file = 'dbench-gpt4.json'

# Get a list of all JSON files in the input folder
json_files = glob.glob(os.path.join(input_folder, '*.json'))

# List to hold all combined data
combined_data = []

# Iterate through each file and read its content
for file in json_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ensure that each file contains an array of items and extend the combined data
            if isinstance(data, list):
                combined_data.extend([{
                    "heuristic": d["heuristic"],
                    "type": d["dataset"][0]["bug_type"]
                } for d in data])
            else:
                combined_data.append({
                    "heuristic": data["heuristic"],
                    "type": data["dataset"][0]["bug_type"]
                })
    except Exception as e:
        print(f"Error reading {file}: {e}")

# Write all combined data into a single JSON file
try:
    with open(output_file, 'w', encoding='utf-8') as out_file:
        json.dump(combined_data, out_file, indent=4)
    print(f"Combined data written to {output_file}")
except Exception as e:
    print(f"Error writing to output file: {e}")
