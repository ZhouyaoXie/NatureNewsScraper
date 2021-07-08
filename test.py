from NatureNewsScraper import NatureNewsScraper
import json

scraper = NatureNewsScraper()
j = scraper.extract_nature_articles("2020-03-01", "2020-04-01", "coronavirus", "health WHO")