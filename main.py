from scrape_setUp import *

# web url to scrap the data from :
URL = "https://www.windguru.cz/885370"

# User-Agent --> Find Your User-Agent: https://httpbin.org/get
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70"

scrape_data = ScrapeData(URL, user_agent)
scrape_data.initiate_scrape()