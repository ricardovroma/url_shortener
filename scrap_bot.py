import concurrent.futures
import time


import time

import requests
from bs4 import BeautifulSoup

from api.models import Website
from api.url_shortener import bijective_encode

base_url = "https://books.toscrape.com/catalogue/"
start_url = base_url + "page-49.html"


def process_book(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    data = {
        "url": url,
        "short_url": "",
        "views": 0,
        "title": soup.select_one('title').text,
    }
    print(f"Creating Book {data}")
    website = Website.create(**data)
    website.short_url = bijective_encode(website.id)
    website.save()


def start_scrap(url):
    print(f"PAGE {url}")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    books = soup.select("article.product_pod")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for book in books:
            # pass
            executor.submit(process_book, base_url + book.select_one("h3 a")['href'])

        next_page = soup.select_one("li.next a").get('href', None) if soup.select_one("li.next a") else None
        if next_page:
            next_page_url = base_url + next_page
            start_scrap(next_page_url)
            executor.submit(start_scrap, next_page_url)


start = time.perf_counter()

start_scrap(start_url)

finish = time.perf_counter()

print(f'Finished in {round(finish - start, 2)} second(s)')

start = time.perf_counter()



# with concurrent.futures.ProcessPoolExecutor() as executor:
#     results = [executor.submit(do_something, 1) for _ in range(10)]
#     for f in concurrent.futures.as_completed(results):
#         print(f.result())

# with concurrent.futures.ThreadPoolExecutor() as executor:
# with concurrent.futures.ProcessPoolExecutor() as executor:
#     results = executor.map(do_something, secs)
#
#     for result in results:
#         print(result)

finish = time.perf_counter()

print(f'Finished in {round(finish - start, 2)} second(s)')
