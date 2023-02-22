import requests
import pandas as pd
from bs4 import BeautifulSoup

# specify the URL to scrape
url = "https://ccp.yale.edu/catalogue?ccp=&museum=&copy=&genre=All&findspot=All&scribe=&rubric=All&edition=All&items_per_page=200&page=4"

# make a request to the URL
response = requests.get(url)

# parse the HTML content of the page
soup = BeautifulSoup(response.content, "html.parser")

# find all the table rows
rows = soup.find_all("tr")

# define a list to store the scraped data
data = []

# loop through all the rows
for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 3:
        ccp_cdli = cols[0].text.strip()
        genre = cols[4].text.strip()
        owner_scribe = cols[5].text.strip()
        link = "https://ccp.yale.edu" + cols[0].find("a").get("href")

        data.append([ccp_cdli, genre, owner_scribe, link])
# Create a DataFrame from the data list
df = pd.DataFrame(data, columns=['CCP & CDLI No', 'Genre', 'Owner and Scribe', 'Link'])

# Save the DataFrame to an Excel file
df.to_excel(".xlsx")# Input file name here
