import requests
from datetime import datetime as dt
import pandas as pd
import numpy as np
import json, collections, time, re, string, os
import bs4
from bs4 import BeautifulSoup

class NatureNewsScraper:

    def __init__(self):
        """
        Initialize a NatureNewsScraper object

        """
        pass

    def parse_page_nature(self, url):
        """
        Parse the page of a single article

        args:
            url: url to the article

        returns:
            dict: a dictionary that contains keys `Title`, `Author` (a list of author names)
                `Summary`, `Published Date`, and `Content` (a list of paragraphs)
        """
        
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        
        # get author list
        author_lst = []
        for a in soup.select('body div ul li.c-author-list__item'):
            for b in a.find('a'):
                author_lst.append(b.string.strip())
                
        # get content
        content_lst = []
        for i in soup.find_all('div', class_ = 'c-article-body u-clearfix'):
            for p in i.find_all('p'):
                content_lst.append(p.get_text().strip())
            # remove related article content
            not_include = soup.find_all('div', {'data-label': 'Related'})
            for dd in not_include:
                try:
                    while True:
                        content_lst.remove(dd.find('p').get_text().strip())
                except ValueError:
                    pass
        content_lst = [l for l in content_lst if l is not None and len(l) > 0]
        
        # get summary
        summary = soup.find('div', {'class': 'c-article-teaser-text'})
        if summary is not None:
            summary = summary.text.strip()
        else:
            summary = ''
                
        return {'Title': soup.title.string.strip(),
            'Author': author_lst,
            'Summary': summary,
            'Published Date': dt.strptime(str(soup.find('time', {'itemprop': 'datePublished'}).string), '%d %B %Y').strftime('%Y-%m-%d'),
            'Content': [line for line in content_lst if len(line) > 0]
            }


    def extract_nature_articles(self, start_date, end_date, keywords, title_contains):
        """
        Search for all Natures News article published in the given period, supporting search by title and keywords
        
        args:
            start_date (str): the lower bound of the date range to filter articles,
                has the format yyyy-mm-dd
            end_date (str): the upper bound (inclusive) of the date range to filter articles,
                has the format yyyy-mm-dd
            keywords (str): keywords to filter articles
            title_contains (str): title keywords to filter articles
        
        return:
            List[Dict[str, str]] : a list of parsed JSON for each articles returned by
                the search query
        """
        base_url = "https://www.nature.com"
        i = 1
        re = []
        LOOP = True
        while LOOP:
            url = base_url+'/search?q='+keywords+'&title='+title_contains+'&order=date_asc&journal=nature&date_range='+start_date[:4]+'-'+end_date[:4]+'&article_type=news&page=' + str(i)
            response = requests.get(url)
            if 'Sorry, no results' in response.text:
                break
            soup = BeautifulSoup(response.text, "html.parser")
            for article in soup.select('body div div div div div div section ol li div h2'):
                article_title = article.text.strip()
                article_url = base_url + article.find('a')['href']
                time.sleep(0.3)
                nature = self.parse_page_nature(article_url)
                if dt.strptime(nature["Published Date"], '%Y-%m-%d') >= dt.strptime(start_date, '%Y-%m-%d') and \
                    dt.strptime(nature["Published Date"], '%Y-%m-%d') <= dt.strptime(end_date, '%Y-%m-%d'):
                    re.append(nature)
                elif dt.strptime(nature["Published Date"], '%Y-%m-%d') > dt.strptime(end_date, '%Y-%m-%d'):
                    LOOP = False
                    break
            i += 1
        return sorted(sorted(re, key = lambda x: x['Title']), key = lambda x: x["Published Date"])