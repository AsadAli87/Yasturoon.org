import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import pdfkit
import time

# Define the base URL
base_url = "https://pseudepigrapha.org"

# Request the page with the links
response = requests.get("https://pseudepigrapha.org/default/index")
soup = BeautifulSoup(response.text, "html.parser")

# Find all the links on the page
links = soup.find_all("a", href=True)

# Make a Translator object
translator = Translator()

# Loop through the links
for link in links[:32]:
    # Get the link's URL
    url = base_url + link["href"]
    
    # Request the page with the text
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Get the text from the page
    text = soup.get_text()
    
    # Translate the text into English
    translated_html = translator.translate(html, dest='en').text
    
    # Save the translated text as a PDF file
    pdfkit.from_string(translated_text, link["href"].replace("/", "") + ".pdf")

    # Add a delay of 0.5 seconds
    time.sleep(0.5)
