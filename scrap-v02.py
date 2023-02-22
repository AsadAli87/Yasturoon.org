# This script will Scrap the information on a website and create an Excel table. 

import requests
import pandas as pd
from bs4 import BeautifulSoup

# Send a request to the website and retrieve the HTML content of the webpage
url = ''
response = requests.get(url)
html_content = response.content

# Use the BeautifulSoup library to parse the HTML and extract the information needed
soup = BeautifulSoup(html_content, 'html.parser')
text_elements = soup.find_all('li')
for element in text_elements:
        text = element.text
        if '' in text:
            start = text.index('.') + 2
            end = text.index(':')
            text_name = text[start:end]
            links = element.find_all('a')
            if len(links) >= 2:
                transliteration_link = links[0]['href']
                translation_link = links[1]['href']
                print(text_name, transliteration_link, translation_link)
            else:
                print("Not enough links for:",text_name)

# Create a list to store the output
output = []
for element in text_elements:
    text = element.text
    if 'transliteration' in text:
        start = text.index('.') + 2
        end = text.index(':')
        text_name = text[start:end]
        links = element.find_all('a')
        if len(links) >= 2:
            transliteration_link = links[0]['href']
            translation_link = links[1]['href']
            output.append([text_name, transliteration_link, translation_link])
        else:
            output.append([text_name, "Not enough links"])

# Create a DataFrame from the output list
df = pd.DataFrame(output, columns=['Text Name', 'Transliteration Link', 'Translation Link'])

# Save the DataFrame to an Excel file
df.to_excel(".xlsx")

