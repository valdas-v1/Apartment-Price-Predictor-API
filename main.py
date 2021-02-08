from scrape_aruodas import Scraper

# Scraping 250 pages of aruodas.lt apartment listings
a = Scraper()
a.scrape_aruodas(250)
a.save_csv("scraping_data/250")
