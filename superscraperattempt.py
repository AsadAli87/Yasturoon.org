import time
import requests
from bs4 import BeautifulSoup
import csv

# Define the scope of the data to be collected as an empty dictionary
data_scope = {}

# Function to scrape data from a website
def scrape_data(url, scope):
    # Make a request to the website and get the HTML content
    response = requests.get(url, timeout=600)
    html_content = response.text
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Code to extract relevant information based on the scope defined
    # The data_scope dictionary will be updated with information found on the website
    for key in scope:
        # Check if data is present on the website for each key in the scope
        data = soup.find(key=key)
        if data:
            scope[key] = data.text
        else:
            # If data is not present, leave the value as an empty string
            scope[key] = ''
    return scope

# List of websites to scrape data from
websites_list = [
    'https://www.example1.com',
    'https://www.example2.com',
    'https://www.example3.com'
]

# Loop through the list of websites
for i, website in enumerate(websites_list):
    # Scrape data from each website
    data = scrape_data(website, data_scope)
    
    # Add new keys to the data_scope if needed
    for key in data:
        if key not in data_scope:
            data_scope[key] = ''
    
    # Write the data to a CSV file
    filename = 'output_' + str(i) + '.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_scope.keys())
        writer.writeheader()
        writer.writerow(data)
    
    # Delay each request by 1 second to be respectful of the website's resources
    time.sleep(1)
