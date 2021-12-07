import time
import urllib.request, urllib.parse, urllib.error
import json
from hltbapi import HtmlScraper

# Import helper class
from IGDBHandler import IGDBHandler
from ITADHandler import ITADHandler
import OCHandler
from keys import IGDB_ID, IGDB_secret, ITAD_key

# import jinja2
# from flask import Flask

# res = HtmlScraper().search(name="animal crossing new horizons")
# for entry in res:
#     print('===================================')
#     print(entry.detailId)
#     print(entry.gameName)
#     print(entry.imageUrl)
#     print(entry.timeLabels)
#     print(entry.gameplayMain)
#     print(entry.gameplayMainExtra)
#     print(entry.gameplayCompletionist)
#     print('===================================')

# rawHTML = urllib.request.urlopen('https://store.steampowered.com/search/?filter=topsellers')
# doc = rawHTML.read().decode('utf8')
# soup:BeautifulSoup = BeautifulSoup(doc, 'html.parser')
# top_games = soup.findAll("span", class_="title")
# print(top_games)

# Main method
if __name__ == "__main__":
    # Initialize external helper objects to handle requests/API calls
    IGDB: IGDBHandler = IGDBHandler(IGDB_ID, IGDB_secret)
    ITAD: ITADHandler = ITADHandler(ITAD_key)

    keyword = input("Enter the name of a game:\n")
    # Lookup in IGDB
    data1 = IGDB.search_game(keyword)[0]
    full_name = data1['name']

    # Lookup in ITAD
    plain = ITAD.search(full_name)
    lowest = ITAD.load_historical_low([plain])
    lowest_price = lowest[plain][0]['price']

    # Load OC score
    ID = OCHandler.top_id(OCHandler.search(full_name))
    OC_Score = OCHandler.top_critic_score(OCHandler.get_review(ID))

    # Time to beat the game
    TTB = HtmlScraper().search(name=full_name)[0].gameplayMain

    print()
    print("=====%s=====" % data1['name'])
    print("Genre: %s" % ", ".join(x['name'] for x in data1['genres']))
    print("Developed by: %s" % [x['company']['name'] for x in data1['involved_companies'] if x['developer'] == True][0])
    print("Published by: %s" % [x['company']['name'] for x in data1['involved_companies'] if x['publisher'] == True][0])
    print("Historic low price on Steam: %s" % str(round(lowest_price, 2)))
    print("Average time to beat: %d hrs" % int(TTB))
    print("OpenCritic score: %d" % OC_Score)

    print("You made it!")
