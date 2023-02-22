import requests
import subprocess
from bs4 import BeautifulSoup
import csv
import sys

sys.setrecursionlimit(10000)

with open('CDLI.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader) # skip header row

    count = 0
    for row in reader:
        if count >= 100:
            break

        cdli_no = row[0]
        item_link = "cdli.ucla.edu/search/search_results.php?SearchMode=Text&ObjectID=" + cdli_no
        
        if "no translation" in item_link:
            continue
        
        try:
            response = requests.get("https://" + item_link, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for tag in soup.find_all(class_="markTrans"):
                tag.decomposed()
            
            html_content = str(soup)
            with open(f'{cdli_no}.html', 'w') as f:
                f.write(html_content)
            subprocess.run(["wkhtmltopdf", f'{cdli_no}.html', f'{cdli_no}.pdf'], check=True)
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch HTML content for {item_link}: {e}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate PDF for {item_link}: {e}")

        count += 1
