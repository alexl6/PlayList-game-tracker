import time
import urllib.request, urllib.parse, urllib.error
import json

from bs4 import BeautifulSoup

import jinja2
from flask import Flask

rawHTML = urllib.request.urlopen('https://howlongtobeat.com/game?id=93948')
doc = rawHTML.read().decode('utf8')
soup:BeautifulSoup = BeautifulSoup(doc, 'html.parser')

playtime = soup.findAll("li", class_="short time_100")
# print(playtime)

# rawHTML = urllib.request.urlopen('https://store.steampowered.com/search/?filter=topsellers')
# doc = rawHTML.read().decode('utf8')
# soup:BeautifulSoup = BeautifulSoup(doc, 'html.parser')
# top_games = soup.findAll("span", class_="title")
# print(top_games)
exit()

# Main method
if __name__ == "__main__":
    exit()