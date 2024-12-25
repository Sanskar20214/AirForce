import requests
from bs4 import BeautifulSoup
import csv

url = "https://en.wikipedia.org/wiki/List_of_active_Indian_military_aircraft"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    html_content = response.text
else:
    raise Exception(f"Failed to retrieve the page. Status code: {response.status_code}")

soup = BeautifulSoup(html_content, 'html.parser')

tables = soup.find('table', {'class': 'wikitable'})
if not tables:
    raise Exception("Could not find the table in the page.")

aircraft_data = []

# Loop through each table
for table in tables:
    # Iterate through rows in the table
    rows = table.find('tr')[1:]  # Skip the header row
    for row in rows:
        columns = row.('td')
        if len(columns) > 1:
            # Extract Aircraft Name (1st column) and Number in Service (2nd column)
            aircraft_name = columns[0].get_text(strip=True)
            number_in_service = columns[1].get_text(strip=True)
            aircraft_data.append([aircraft_name, number_in_service])

# Save the data into a CSV file
csv_file = "indian_military_aircraft.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Aircraft", "Number in Service"])  # Header
    writer.writerows(aircraft_data)

print(f"Data successfully written to {csv_file}")