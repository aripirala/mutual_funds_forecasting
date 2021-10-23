from urllib.request import urlopen
from bs4 import BeautifulSoup
import string
import pandas as pd
import os

url = 'https://www.marketwatch.com/tools/mutual-fund/list/'
output_dir = '../input/'

page_appenders = list(string.ascii_uppercase)
print(page_appenders)

for letter in page_appenders:
    page = url+letter
    request_page = urlopen(page)
    page_html = request_page.read()
    request_page.close()

    html_soup = BeautifulSoup(page_html, 'html.parser')
    mutual_funds_items = html_soup.find_all('td', class_='quotelist-symb')
    counter = 0

    fund_list = []
    for i, fund in enumerate(mutual_funds_items):        
        fund_list.append(fund.text)
    
funds_df = pd.DataFrame(fund_list)
funds_df.columns = 'Fund_Symbol'
funds_df.write_csv(os.path.join(output_dir, 'mutual_funds.csv'), headers=True)
