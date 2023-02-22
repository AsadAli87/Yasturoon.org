import csv
import requests
import time
from bs4 import BeautifulSoup

# Request the first page of the search results
data = []
url = f"https://papyri.info/search?DATE_END_TEXT=0&DATE_END_ERA=CE&DATE_MODE=LOOSE&TRANSL=en&DOCS_PER_PAGE=100&page=10"
try:
    response = requests.get(url, timeout=600)
except requests.exceptions.Timeout:
    time.sleep(10)
    response = requests.get(url, timeout=600)

soup = BeautifulSoup(response.text, "html.parser")

result_records = soup.find_all("tr", class_="result-record")

# Loop through the result records
for record in result_records:
    # Find the text and link for each cell in the row
    cells = record.find_all("td")
    if len(cells) > 0:
        text = [cell.text for cell in cells]
        links = [cell.a["href"] if cell.a else None for cell in cells]
        # Add the text and links to the data list
        data.append(text + links)

# Write the data to a CSV file
with open("papyriinfo 10.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)
