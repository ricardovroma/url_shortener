import asyncio

from fastapi import FastAPI
from fastapi import Request
from peewee import DoesNotExist
from pydantic import HttpUrl
from starlette.responses import Response, RedirectResponse

from .models import WebsitePydantic, Website
from .service import store_website
from .url_shortener import bijective_encode

app = FastAPI()


@app.get("/", response_model=list[WebsitePydantic])
async def top100() -> list[WebsitePydantic]:
    data = [item.to_pydantic() for item in Website.select().order_by(Website.views.desc()).limit(100)]
    return data


@app.get("/{id}")
async def url_redirect(id: str, response: Response):
    try:
        item = Website.select().where(Website.short_url == id).get()
    except DoesNotExist as e:
        response.status_code = 404
        return response

    item.views += 1
    item.save()
    return RedirectResponse(item.url)


@app.post("/add/", responses={409: {}, 201: {}})
async def add(url: HttpUrl, response: Response, request: Request):
    if Website.select().where(Website.url == url):
        response.status_code = 409
    else:
        data = {
            "url": url,
            "short_url": "",
            "title": "",
            "views": 1,
        }
        website = Website.create(**data)
        website.short_url = bijective_encode(website.id)
        website.save()

        loop = asyncio.get_running_loop()
        loop.create_task(store_website(website))
        return {'url': f"{request.base_url}{website.short_url}"}
    return response



