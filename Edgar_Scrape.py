import requests
from bs4 import BeautifulSoup

filing_list_url = "https://www.sec.gov/cgi-bin/browse-edgar"

payload = {
        'action': 'getcompany', 
        'CIK': '51143',
        'type': '10-K',
        'count': '200'
    }
r = requests.get(filing_list_url, params=payload)


soup = BeautifulSoup(r.text, 'html.parser')
for link in soup.find_all(id="interactiveDataBtn"):
    print(link.get('href'))

