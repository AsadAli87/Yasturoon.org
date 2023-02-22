import subprocess
import pandas as pd
import requests
import time
import csv

# Load the DataFrame from the CSV file
df = pd.read_csv("C:\\Users\\Asad Ali\\Desktop\\Yasturoon.org\\CCP Commentaries.csv")

# Iterate through the DataFrame
for index, row in df.iterrows():
    # Get the item link for the current row
    links = row['Link']
    try:
        response = requests.get(links, timeout=2100, verify=False)
    except requests.exceptions.Timeout:
        # Wait for 10 seconds before trying the request again
        time.sleep(10)
        response = requests.get(links, timeout=2100, verify=False)
    # Generate the PDF file name
    pdf_file = row['CDLI No'] + ".pdf"
    # Convert the webpage to a PDF
    subprocess.call(['wkhtmltopdf', links, pdf_file])
    print(f"{pdf_file} saved.")
