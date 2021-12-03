import time
import urllib.request, urllib.parse, urllib.error
import json

from bs4 import BeautifulSoup

import jinja2
from flask import Flask

rawHTML = urllib.request.urlopen('https://howlongtobeat.com/game?id=93948')
doc = rawHTML.read().decode('utf8')
soup:BeautifulSoup = BeautifulSoup(doc, 'html.parser')
print(soup.prettify())

playtime = soup.findAll("li", class_="short time_100")
print(playtime)
exit()

# Main method
if __name__ == "__main__":
