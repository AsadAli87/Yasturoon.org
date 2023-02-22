import subprocess
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load the DataFrame from the CSV file
df = pd.read_csv("CDLI new.csv")

# Iterate through the DataFrame
for index, row in df.iterrows():
    # Get the item link for the current row
    links = row['Links']
    # Fetch the HTML content
    response = requests.get(links)
    html_content = response.text
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find the "Expand All" button
    expand_all_button = soup.find('button', text='Expand All')
    # If the "Expand All" button was found
    if expand_all_button:
        # Add the script to expand all content to the HTML head
        script = soup.new_tag("script")
        script.string = "window.onload = function() { document.querySelector('.btn.bg-white.text-primary').click(); };"
        soup.head.append(script)

    # Generate the PDF file name
    pdf_file = row['Artifact'] + ".pdf"
    # Convert the modified HTML content to a PDF
    with open('temp.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

    subprocess.call(['wkhtmltopdf', 'temp.html', pdf_file])
    print(f"{pdf_file} saved.")
