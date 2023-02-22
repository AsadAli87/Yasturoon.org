import requests
import time
import csv
from bs4 import BeautifulSoup
import pandas as pd

# Load the data into a Pandas DataFrame
df = pd.read_csv("Perseus English Duplicated Removed Translation Links.csv")

# Loop through each row in the DataFrame
for i, row in df.iterrows():
    title = row['Title']
    author = row['Author']
    search_term = title + "+" + author

    # Search for the PDF in archive.org
    archive_search_url = f"https://archive.org/search.php?query={search_term}"
    try:
        response = requests.get(archive_search_url, timeout=2, verify=False)
    except requests.exceptions.Timeout:
        time.sleep(10)
        response = requests.get(archive_search_url, timeout=2, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_link = None

    # Find the first link that contains a PDF
    for a in soup.find_all("a", href=True):
        if a["href"].endswith(".pdf"):
            pdf_link = a["href"]
            break

    if pdf_link:
        pdf_file = title + "_" + author + ".pdf"
        # Save the PDF file
        with open(pdf_file, 'wb') as f:
            f.write(requests.get(pdf_link).content)
        print(f"PDF found and saved: {pdf_file}")
    else:
        print("PDF not found")
