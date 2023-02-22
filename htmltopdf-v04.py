import subprocess
import pandas as pd
import csv

# Load the DataFrame from the Excel file
df = pd.read_csv("CDLI.csv")

# Iterate through the DataFrame
for index, row in df.iterrows():
    # Get the translation link for the current row
    item_link = row['Item Link']
    # Generate the PDF file name
    pdf_file = row['CDLI No'] + ".pdf"
    # Convert the webpage to a PDF
    subprocess.call(['wkhtmltopdf', item_link, pdf_file])
    print(f"{pdf_file} saved.")
