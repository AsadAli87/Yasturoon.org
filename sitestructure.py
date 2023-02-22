import requests
from bs4 import BeautifulSoup

url = ''
response = requests.get(url)
html_content = response.text

# Now you can pass the HTML content to BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
print(soup.prettify())
