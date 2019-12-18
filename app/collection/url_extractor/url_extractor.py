import pprint

import requests
from extruct.opengraph import OpenGraphExtractor
from w3lib.html import get_base_url

from app.collection.url_extractor.utils import get_html, save_bookmark
from bs4 import BeautifulSoup


def extract_open_graph(url):
    url_page = get_html(url)
    og = OpenGraphExtractor()
    try:
        data = og.extract(url_page.text)[0]["properties"]

        # new_data = {key: value for key, value in data if key not in data}
        new_data = {}
        for key, value in data:
            if key not in new_data:
                new_data[key] = value

        return new_data
    except IndexError:
        data = og.extract(url_page.text)
        return data


def extract_url_info(url):
    html = get_html(url).text
    if html: 
        soup = BeautifulSoup(html, "lxml")
        title = soup.title.text
        data = {"title": title, "url": url}
    
        return data
    
    return False

def find_base_url(url):
    html = get_html(url)
    base_url = get_base_url(html.text, html.url)

    if base_url == url:
        base_url = url.split("/")[2]
        return base_url

    return base_url


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(extract_open_graph(
        "https://habr.com/en/post/349860/"))
    print("-"*40)
    print(find_base_url("https://habr.com/en/post/349860/"))
