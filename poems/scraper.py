import os
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

