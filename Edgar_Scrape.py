import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import math
from re import sub
from decimal import Decimal

filing_list_url = "https://www.sec.gov/cgi-bin/browse-edgar"

payload = {
        'action': 'getcompany', 
        'CIK': '320193',
        'type': '10-K',
        'count': '200'
    }

r = requests.get(filing_list_url, params=payload)

soup = BeautifulSoup(r.text, 'html.parser')

balance_sheets = []
for link in soup.find_all(id="interactiveDataBtn"):
    r = requests.get('https://www.sec.gov/' + link.get('href'))
    statement_soup = BeautifulSoup(r.text, 'html.parser')
    balance_sheet_link = statement_soup.find_all("a", string="CONSOLIDATED BALANCE SHEETS")
    if balance_sheet_link:
        balance_sheets.append({
            'account_number':link.get('href')
                                .split('accession_number=')[1]
                                .split('&')[0]
                                .replace('-',''),
            'index':balance_sheet_link[0]['href']
                                .split('(')[1]
                                .split(')')[0]
        }
        )

base_url = 'https://www.sec.gov/Archives/edgar/data/'
json_output = json.loads('{}')
for balance_sheet in balance_sheets:
    url = base_url + payload['CIK'] + f"/{balance_sheet['account_number']}/R{balance_sheet['index']}.htm"
    try:
        df = pd.read_html(url)[0]
        df[df.columns[0]] = df[df.columns[0]].replace(
                                to_replace=r'[^a-zA-Z\s]',
                                value='', 
                                regex=True
                            ).replace(r'\r\n', '').replace(r'\n', '').replace(r'\r', '')
        balance_sheet_groups = []
        for index, row in df.iterrows():
            if type(row[df.columns[1]]) == float:
                balance_sheet_group = row[df.columns[0]]
            balance_sheet_groups.append(balance_sheet_group)
        df['balance_sheet_group'] = balance_sheet_groups
        df = df[df[df.columns[0]] != balance_sheet_groups ]
        df = df.set_index(['balance_sheet_group', df.columns[0]])
        json_output.update(json.loads(df.to_json()))
    except:
        pass

print(json_output)