import requests
import pandas as pd
from bs4 import BeautifulSoup

# Create the URL
url = f'https://cdli.ucla.edu/search/search_results.php?SearchMode=Line&PrimaryPublication=&MuseumNumber=&Provenience=&Period=&TextSearch=&ObjectID=&requestFrom=Submit&offset=154000'

# Send a request to the website and retrieve the HTML content of the webpage
response = requests.get(url, verify=False)
html_content = response.content

# Use the BeautifulSoup library to parse the HTML and extract the information needed
soup = BeautifulSoup(html_content, 'html.parser')
text_elements = soup.find_all('tr')
output = []
for tr in text_elements:
        td = tr.find_all('td')
        if td:
            td_values = [td_element.text.strip() for td_element in td]
            # Fill up td_values list with empty strings if there are less values than the number of columns
            td_values = td_values + [''] * (7 - len(td_values))
            cdli_no, primary_publication, museum_no, period, dates_referenced, provenience, genre = td_values

            # Construct the link to the Object ID page
            item_link = f"https://cdli.ucla.edu/search/result_details.php?ObjectID={cdli_no}"

            output.append([cdli_no, primary_publication, museum_no, period, dates_referenced, provenience, genre, item_link])        

# Create a DataFrame from the output list
df = pd.DataFrame(output, columns=['CDLI No', 'Primary Publication', 'Museum No', 'Period', 'Dates Referenced', 'Provenience', 'Genre', 'Item Link'])

# Save the DataFrame to an Excel file
df.to_excel("CDLI 78.xlsx")
