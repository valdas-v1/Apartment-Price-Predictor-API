from bs4 import BeautifulSoup
import requests
import pandas as pd
pd.options.mode.chained_assignment = None

import pickle
import re
import time


class Scraper:
    def __init__(self):
        # Placeholder dataframes to hold listing and category data
        self.df = pd.DataFrame()

    def get_soup(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Accept-Language": "en-US, en;q=0.5",
        }

        time.sleep(1.51)

        page = requests.get(url, headers=headers)

        return BeautifulSoup(page.content, "html.parser")

    def extract_info(self, soup):
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
        
        clean_df["Area"] = clean_df["Area"].str.findall(r"(\d+)")
        clean_df["Area"] = float(".".join(clean_df['Area'].iloc[0]))
        
        clean_df["Build year"] = clean_df["Build year"].str.findall(r"(\d+)")
        
        clean_df['Renovation year'] = 0
        if len(clean_df['Build year'].iloc[0]) == 2:
            clean_df['Renovation year'].iloc[0] = int(clean_df['Build year'].iloc[0][1])
            clean_df['Build year'].iloc[0] = int(clean_df['Build year'].iloc[0][0])
        else:
            clean_df['Build year'].iloc[0] = int(clean_df['Build year'].iloc[0][0])

        price = soup.find("span", class_="main-price")
        price = re.findall("\d+", price.text)
        clean_df["price"] = float("".join(price))

        address = soup.find("h1")
        address = address.text.split(",")

        clean_df["city"] = address[0].strip()
        clean_df["region"] = address[1].strip()

        if len(address) > 2:
            clean_df["street"] = address[2].strip()
        else:
            clean_df["street"] = "None"

        self.df = self.df.append(clean_df, ignore_index=True)

    def scrape_aruodas(self, pages):
        for page in range(pages):
            search = self.get_soup(f"https://m.en.aruodas.lt/butai/puslapis/{page}/")
            search = search.find_all("a", class_="object-image-link")

            for link in search:
                print(f'https://m.en.aruodas.lt{link["href"]}')
                flat = self.get_soup(f'https://m.en.aruodas.lt{link["href"]}')

                self.extract_info(flat)

    def save(self):
        pickle.dump(self.df, open("df.pkl", "wb"))


a = Scraper()
a.scrape_aruodas(1)
a.save()
