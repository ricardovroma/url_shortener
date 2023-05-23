# Url Shortener

## Install
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python setup.py

## Run
uvicorn api.main:app --reload

## Tests
pytest

## Scrap bot
python scrap_bot.py

## REQUIREMENTS
• We must be able to post an URL into a route/endpoint and get back a new URL with the shortest possible length.

• We must be redirected to the full URL when we enter/send the short URL in a form/endpoint (ex:http://localhost:3000/a => https://google.com)

• There should be an endpoint that returns top 100 most frequently accessed URLs.

• There must be a background job that crawls the URL being shortened, pulls the HTML <title> tag from the website and stores it.

• Display the title with the URL on the top 100 endpoint.

• There must be a README that explains how to setup the application and the algorithm used for generating the URL short code.

## NICE TO HAVE:
• Write a bot to populate your DB, and include it in the source code

• Write Unit or Integration Tests