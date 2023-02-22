import requests
import csv
import time

# Define the search term to use
search_term = "BCE writing"

# Define the URL for the Google search results page
url = "https://www.google.com/search?q=" + search_term + "&start="

# Define the headers for the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
}

# Define the CSV file to write the results to
csv_file = open('search_results.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)

# Write the headers for the CSV file
writer.writerow(['Title', 'Link', 'Description'])

# Iterate over the pages of the search results
for i in range(0, 40, 10):  # 0, 10, 20, ..., 190
    # Make a request to the URL
    response = requests.get(url + str(i), headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        # Get the HTML content of the page
        html_content = response.text
        # Find the start and end indices of the search results
        start = html_content.find('<div id="search">')
        end = html_content.find('<div id="foot">')
        # Extract the search results from the HTML content
        search_results = html_content[start:end]
        # Split the search results into individual search result blocks
        search_result_blocks = search_results.split('<div class="g">')
        # Iterate over the search result blocks
        for search_result_block in search_result_blocks[1:]:
            # Find the start and end indices of the title and link
            title_start = search_result_block.find('<h3 class="LC20lb">') + 17
            title_end = search_result_block.find('</h3>')
            link_start = search_result_block.find('<a href="') + 9
            link_end = search_result_block.find('"', link_start)
            # Extract the title and link from the search result block
            title = search_result_block[title_start:title_end]
            link = search_result_block[link_start:link_end]
            # Find the start and end indices of the description
            description_start = search_result_block.find('<span class="st">') + 14
            description_end = search_result_block.find('</span>')
            # Extract the description from the search result block
            description = search_result_block[description_start:description_end]
            # Write the title, link, and description to the CSV file
            writer.writerow([title, link, description])
    # Wait for 0.5 seconds before making the next request
    time.sleep(0.5)
    print(f"Page No {i/10 + 1} completed")
# Close the CSV file
csv_file.close()
