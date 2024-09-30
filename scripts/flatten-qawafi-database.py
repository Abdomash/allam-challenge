import os
import json

def combine_json_files(directory, output_file):
    combined_data = {'data': []}

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    # Load the JSON data from the file
                    file_data = json.load(f)

                    # Extract names and add them to the combined data
                    for item in file_data.get('data', []):
                        text = item['name'].replace(" ", "")
                        if (text):
                            if (len(text) > 2 and text[0:2] == "ال"):
                                text = text[2:]
                            combined_data['data'].append(text)

                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {filename}")
            
            print(f"Processed file {filename}...")

    combined_data['data'].sort(key=lambda name: name[::-1])

    # Write the combined data to the output file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        json.dump(combined_data, out_file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    output_file = 'combined_output.json'

    combine_json_files("original-qawafi-database", output_file)
    print(f"Combined JSON file created: {output_file}")
