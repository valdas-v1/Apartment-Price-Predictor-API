from bs4 import BeautifulSoup
import requests
import pandas as pd
import pickle
import re

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}

URL = "https://m.en.aruodas.lt/butai-vilniuje-zveryne-kestucio-g-esate-aplinkos-kokybei-reiklus-zmogus-tad-1-2850445/"
page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")

info = soup.find_all("dl")

flat_info = pd.DataFrame()
cleaned_key = []
for i in info[0].find_all("dt"):
    cleaned_key.append(i.text)

cleaned_value = []
for i in info[0].find_all("dd"):
    cleaned_value.append(i.text)

flat_info["key"] = cleaned_key
flat_info["value"] = cleaned_value

clean_df = flat_info.pivot_table(values="value", columns="key", aggfunc="first")

required_data = [
    "Area",
    "Build year",
    "Building type",
    "Equipment",
    "Floor",
    "Heating system",
    "No. of floors",
    "Number of rooms ",
]

clean_df = clean_df.filter(required_data)
clean_df['Area'] = clean_df['Area'].str.findall(r'(\d+)')[0]
clean_df['Build year'] = clean_df['Build year'].str.findall(r'(\d+)')


price = soup.find("span", class_="main-price")
price = re.findall("\d+", price.text)
clean_df['price'] = ''.join(price)

address = soup.find("h1")
address = address.text.split(",")

clean_df['city'] = address[0].strip()
clean_df['region'] = address[1].strip()

if len(address) > 2:
    clean_df['street'] = address[2].strip()
else:
    clean_df['street'] = 'None'

print(clean_df)
pickle.dump(clean_df, open("flat_info.pkl", "wb"))