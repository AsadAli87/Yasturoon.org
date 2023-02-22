import requests
import pandas as pd
from bs4 import BeautifulSoup

# specify the URL to scrape
url = "https://cdli.mpiwg-berlin.mpg.de/search?layout=compact&simple-field%5B0%5D=keyword&f%5Batf_translation%5D%5B0%5D=With&limit=1000"

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
        artifact = cols[-1].text.strip()
        genre = cols[2].text.strip()
        period = cols[3].text.strip()
        provenience = cols[4].text.strip()

        data.append([artifact, genre, period, provenience])
# Create a DataFrame from the data list
df = pd.DataFrame(data, columns=['Artifact', 'Genre', 'Period', 'Provenience'])

# Save the DataFrame to an Excel file
df.to_excel("CDLI new.xlsx")
