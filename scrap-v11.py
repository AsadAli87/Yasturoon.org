import csv
import requests
import time
from bs4 import BeautifulSoup

data = []

page = 1

filename = "Perseus Catalogue.csv"
with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Author", "Language", "Link"])

# Request the first page of the search results
while True:
    url = "https://catalog.perseus.org/?page={page}&per_page=100&q=B.C&search_field=all_fields&sort=title_display+asc&utf8=%E2%9C%93"
    try:
        response = requests.get(url, timeout=600)
    except requests.exceptions.Timeout:
        time.sleep(10)
        response = requests.get(url, timeout=600)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the container for all the works
    documents = soup.find("div", {"id": "documents"})
    if not documents:
        break

    # Iterate over each work in the container
    for document in documents.find_all("div", {"class": "document"}):
        # Scrape the title
        title_header = document.find("div", {"class": "documentHeader clearfix"})
        title = title_header.find("a").text

        # Scrape the author and language
        details = document.find("dl", {"class": "dl-horizontal dl-invert"})
        try:
            author = details.find("dd", {"class": "blacklight-exp_auth_name"}).text
        except AttributeError:
            author = ""
        try:
            language = details.find("dd", {"class": "blacklight-exp_language"}).text
        except AttributeError:
            language = ""
            
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

        # Add the scraped data to the list
        data.append([title, author, language, link])

    # Increment the page number
    page += 1
    
    # Wait for 5 seconds before making the next request
    time.sleep(5)

    # Save the data to a separate file
    filename = "Perseus Catalogue Page " + str(page) + ".csv"
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Author", "Language", "Link"])
        writer.writerows(data)
        print("Page No", page, "completed and saved as", filename)
