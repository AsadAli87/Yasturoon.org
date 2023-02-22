import requests
import pandas as pd
from bs4 import BeautifulSoup

# Create the base URL
base_url = 'https://cdli.ucla.edu/search/search_results.php?SearchMode=Line&PrimaryPublication=&MuseumNumber=&Provenience=&Period=&TextSearch=&ObjectID=&requestFrom=Submit&offset='
offset = 0
while offset >= 0 and offset <= 154000:

        # Create an empty list to store the data
        output = []

        # Use a while loop to keep fetching the data until all results are retrieved
        while True:
            # Construct the URL with the current offset
            url = base_url + str(offset)

            # Send a request to the website and retrieve the HTML content of the webpage
            response = requests.get(url, verify=False)
            html_content = response.content

            # Use the BeautifulSoup library to parse the HTML and extract the information needed
            soup = BeautifulSoup(html_content, 'html.parser')
            text_elements = soup.find_all('tr')
            
            # Check if there are no more results
            if not text_elements:
                break

            for tr in text_elements:
                td = tr.find_all('td')
                if td:
                    td_values = [td_element.text.strip() if td_element.text.strip() else '' for td_element in td]
                    # Fill up td_values list with empty strings if there are less values than the number of columns
                    td_values = td_values + [''] * (7 - len(td_values))
                    cdli_no, primary_publication, museum_no, period, dates_referenced, provenience, genre = td_values

                    # Construct the link to the Object ID page
                    item_link = f"https://cdli.ucla.edu/search/result_details.php?ObjectID={cdli_no}"

                    output.append([cdli_no, primary_publication, museum_no, period, dates_referenced, provenience, genre, item_link])
                        
            # Increment the offset by 2000 for the next iteration
            offset += 2000
            if offset > 154000:
                break

# Create a DataFrame from the output list
df = pd.DataFrame(output, columns=['CDLI No', 'Primary Publication', 'Museum No', 'Period', 'Dates Referenced', 'Provenience', 'Genre', 'Item Link'])

# Save the DataFrame to an Excel file
df.to_csv("CDLI initial.csv")
