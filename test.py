from bs4 import BeautifulSoup
import requests
import pandas as pd
import pickle

headers = {'User-Agent':
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                    'Accept-Language': 'en-US, en;q=0.5'}

URL = "https://m.en.aruodas.lt/butai-vilniuje-zveryne-kestucio-g-esate-aplinkos-kokybei-reiklus-zmogus-tad-1-2850445/"
page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")

info = soup.find_all("dl")

flat_info = pd.DataFrame()
cleaned_key = []
for i in info[0].find_all('dt'):
    cleaned_key.append(i.text)

cleaned_value = []
for i in info[0].find_all('dd'):
    cleaned_value.append(i.text)

flat_info['key'] = cleaned_key
flat_info['value'] = cleaned_value

clean_df = flat_info.pivot_table(values='value', columns='key', aggfunc='first')

required_data = ['Area', 'Build year', 'Building type', 'Equipment', 'Floor', 'Heating system',
       'No. of floors', 'Number of rooms ']

clean_df.filter(required_data)

pickle.dump(clean_df, open("flat_info.pkl", "wb"))
