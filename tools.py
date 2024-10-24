import openmeteo_requests
from openmeteo_sdk.Variable import Variable
import requests
from newsapi import NewsApiClient

with open("credentials.yml", "r") as c:
    news_key = c.readlines()[0]

# Init
newsapi = NewsApiClient(api_key=news_key)

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(language='de', country='de')

# /v2/top-headlines/sources
#sources = newsapi.get_sources()

print(top_headlines)