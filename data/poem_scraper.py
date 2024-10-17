import os
import ast
import json
import requests
from bs4 import BeautifulSoup

def extract_poem(filepath, lim, url):
    """
    This function is designed for https://www.toarab.ws/
    """

    # Fetch the HTML content from the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    html = response.text

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Extract the <tbody>
    tbody = soup.find_all("table", class_="poem")[0]

    if not tbody:
        print("<tbody> not found in the table.")
        return []

    rows = tbody.find_all("tr")  # Get all <tr> elements

    result = []
    
    for row in rows:
        cells = row.find_all('td')  # Get all <td> elements
        cells_text = [cell.get_text(strip=True) for cell in cells]  # Extract text from <td>
        
        # Check if we have 4 cells
        if len(cells_text) == 4:
            result.append(cells_text[1])  # Append the second cell
            result.append(cells_text[3])  # Append the fourth cell

        if len(result) >= lim:
            break

    os.makedirs(os.path.dirname(filepath), exist_ok=True)  # Create the directory if it doesn't exist


    # Save the result to the specified file path
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(f'{result}\n')

    return result


def parse_poem_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read().strip()
        # Safely evaluate the string to convert it into a list
        if content.startswith('[') and content.endswith(']'):
            content = content[1:-1]  # Remove the brackets
            content = content.replace('\'', '').replace('\"', '').replace('  ', ' ').replace('ـ','')
            # Split by commas and clean up each line
            poem_lines = [line.strip() for line in content.split(',')]
            return poem_lines
        else:
            print(f"Invalid format in {file_path}")
            return None

def convert_to_json(folder_path):
    data = {}
    for author in os.listdir(folder_path):
        author_path = os.path.join(folder_path, author)
        if os.path.isdir(author_path):
            data[author] = {}
            for category in os.listdir(author_path):
                category_path = os.path.join(author_path, category)
                if os.path.isdir(category_path):
                    data[author][category] = []  # Change to a list
                    for poem_file in os.listdir(category_path):
                        poem_path = os.path.join(category_path, poem_file)
                        if os.path.isfile(poem_path):
                            poem_lines = parse_poem_file(poem_path)
                            if poem_lines is not None:
                                data[author][category].append(poem_lines)
    return data

def save_to_json(data, output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    folder_path = input("input folder:")
    output_file = input("output filename:")

    poems_data = convert_to_json(folder_path)
    save_to_json(poems_data, output_file)

    print(f"Converted poems to {output_file}")


