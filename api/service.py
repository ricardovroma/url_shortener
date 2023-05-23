import requests
from bs4 import BeautifulSoup

from .models import Website


async def store_website(website: Website):
    title = ""
    try:
        page = requests.get(website.url)
        soup = BeautifulSoup(page.content, "html.parser")
        title = soup.select('title')
        title = title[0].text
    except requests.exceptions.ConnectionError as e:
        print("Unable to retrieve the title")
    except Exception as e:
        print(e)
        print("somethig wrong")

    website.title = title
    website.save()
