from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        # Placeholder dataframes to hold listing and category data
        self.df = pd.DataFrame()

    def collect_information(self, no_of_examples, keyword):

        """
        Collects the number of examples for category, title, price, url and the thumbnail url from eBay for the provided keyword. 
        Appends the results to the main dataframe

        Parameters:
            no_of_examples (int): The number of listings to scrape
            keyword (str): The keyword to scrape listings from
        """

        category, title, price, url, thumbnail_url = ([] for i in range(5))

        for page_no in range(1, (math.ceil(no_of_examples / 96) + 1)):
            soup = self.get_page_soup(
                f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={keyword}&_ipg=96&LH_BIN=1&_pgn={page_no}")

            category.extend([keyword for value in soup.find_all("h3", class_="s-item__title")])
            title.extend([value.text for value in soup.find_all("h3", class_="s-item__title")])
            price.extend([value.text for value in soup.find_all("span", class_="s-item__price")])
            url.extend([value['href'][:150] for value in soup.find_all("a", class_="s-item__link")])
            thumbnail_url.extend([value['src'] for value in soup.find_all("img", class_="s-item__image-img")])

        collected_info = pd.DataFrame({
            "category_id": category,
            "title": title,
            "price": price,
            "url": url,
            "thumbnail_url": thumbnail_url
        })

        self.df = self.df.append(collected_info, ignore_index=True)