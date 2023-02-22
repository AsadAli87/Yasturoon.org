import requests
from bs4 import BeautifulSoup
import csv
import time

# Iterating through each page, starting from page 0, incrementing by 10 results per page
for i in range(0, 40, 10):
    data = []
    url = f"https://www.google.com/search?q=BCE+writing&start={i}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    # Iterating through each result on the page
    for g in soup.find_all("div", class_="r"):
        title_element = g.find("h3")
        if title_element:
            title = title_element.text
        else:
            title = ""
        link_element = g.find("a")
        if link_element:
            link = link_element["href"]
        else:
            link = ""
        description_element = g.find("span", class_="st")
        if description_element:
            description = description_element.text
        else:
            description = ""
        data.append([title, link, description])
    # Creating a CSV file
    filename = "search_results.csv"
    # Write the data to a csv file
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if i == 0:
            writer.writerow(["Title", "Link", "Description"])
        writer.writerows(data)
    # Adding a time delay of 0.5 seconds between requests
    time.sleep(0.5)
    print(f"Page No {i/10 + 1} completed")
