import csv
import requests
from bs4 import BeautifulSoup
import time

# Initialize a list to store the scraped data
data = []

# Initialize the page number
page = 1

# Keep looping until there are no more pages
while True:
    # Request the current page of the search results
    url = f"https://catalog.perseus.org/?page={page}&per_page=100&q=B.C&search_field=all_fields&sort=title_display+asc&utf8=%E2%9C%93"
    try:
        response = requests.get(url,timeout=2100)
    except requests.exceptions.Timeout:
        # Wait for 10 seconds before trying the request again
        time.sleep(10)
        response = requests.get(url,timeout=2100)

    # Check the status code of the response
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
    else:
        print(f"Failed to retrieve page {page}")
        break

    # Find the container for all the works
    documents = soup.find("div", {"id": "documents"})

    # If the container is not found, there are no more pages
    if not documents:
        break

    # Iterate over each work in the container
    for document in documents.find_all("div", {"class": "document"}):
        # Scrape the title
        title_header = document.find("div", {"class": "documentHeader clearfix"})
        title = title_header.find("a").text

        # Scrape the author and language
        details = document.find("dl", {"class": "dl-horizontal dl-invert"})
        author = details.find("dd", {"class": "blacklight-exp_auth_name"}).text if details.find("dd", {"class": "blacklight-exp_auth_name"}) else ""
        language = details.find("dd", {"class": "blacklight-exp_language"}).text if details.find("dd", {"class": "blacklight-exp_language"}) else ""

        # Check if the language is English
        if language == "English":
            # Scrape the link to the text
            title_url = "https://catalog.perseus.org" + title_header.find("a")["href"]
            title_response = requests.get(title_url)
            title_soup = BeautifulSoup(title_response.text, "html.parser")
            link = title_soup.find("dd").find("a")
            if link:
                link = link["href"]
            else:
                link = ""
        else:
            link = ""

        # Add the scraped data to the list
        data.append([title, author, language, link])

    # Increment the page number
    page += 1

# Write the data to a CSV file
with open("Perseus Catalogue.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Author", "Language", "Link"])
