import time
import urllib.request, urllib.parse, urllib.error
import json
from hltbapi import HtmlScraper

from bs4 import BeautifulSoup

import jinja2
from flask import Flask

res = HtmlScraper().search(name = "animal crossing new horizons")
for entry in res:
    print('===================================')
    print(entry.detailId)
    print(entry.gameName)
    print(entry.imageUrl)
    print(entry.timeLabels)
    print(entry.gameplayMain)
    print(entry.gameplayMainExtra)
    print(entry.gameplayCompletionist)
    print('===================================')


# rawHTML = urllib.request.urlopen('https://store.steampowered.com/search/?filter=topsellers')
# doc = rawHTML.read().decode('utf8')
# soup:BeautifulSoup = BeautifulSoup(doc, 'html.parser')
# top_games = soup.findAll("span", class_="title")
# print(top_games)

# Main method
if __name__ == "__main__":
    print("It worked!")