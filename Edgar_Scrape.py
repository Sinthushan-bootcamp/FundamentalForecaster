import requests
from bs4 import BeautifulSoup
#import pandas as pd

filing_list_url = "https://www.sec.gov/cgi-bin/browse-edgar"

payload = {
        'action': 'getcompany', 
        'CIK': '320193',
        'type': '10-K',
        'count': '200'
    }

r = requests.get(filing_list_url, params=payload)

soup = BeautifulSoup(r.text, 'html.parser')

account_numbers = [link.get('href')
                    .split('accession_number=')[1]
                    .split('&')[0]
                    .replace('-','') 
                    for link in soup.find_all(id="interactiveDataBtn")]

base_url = 'https://www.sec.gov/Archives/edgar/data/'

for account in account_numbers:
    url = base_url + payload['CIK'] + f"/{account}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.select('a[href*="R"][href$=".htm"]')
    if links:
        for link in links:
            
    else:
        break
        #url = base_url + payload['CIK'] + f"/{account}/R{index}.htm" 
   


