# NatureNewsScraper
A web scraping tool for Nature's news articles

### Input

- start_date (str): the lower bound of the date range to filter articles, has the format yyyy-mm-dd
- end_date (str): the upper bound (inclusive) of the date range to filter articles, has the format yyyy-mm-dd
- keywords (str): keywords to filter articles
- title_contains (str): title keywords to filter articles

### Return

List[Dict[str, str]] : a list of parsed JSON dictionaries for each article

### Example Usage

See `test.py`:

`scraper = NatureNewsScraper()`

`j = scraper.extract_nature_articles("2020-03-01", "2020-04-01", "coronavirus", "health WHO")`
                
