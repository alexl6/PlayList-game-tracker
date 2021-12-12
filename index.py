# Import packages
import time
import urllib.request, urllib.parse, urllib.error
import json
from flask import Flask, request, abort
from flask_cors import CORS
from hltbapi import HtmlScraper
from gameobj import GameObj
from typing import List, Dict
from fuzzywuzzy import fuzz

# Import helper class
from IGDBHandler import IGDBHandler
from ITADHandler import ITADHandler
import OCHandler
from keys import IGDB_ID, IGDB_secret, ITAD_key

# Initialize external handlers
IGDB: IGDBHandler = IGDBHandler(IGDB_ID, IGDB_secret)
ITAD: ITADHandler = ITADHandler(ITAD_key)

# Create new flask app
app = Flask(__name__)
CORS(app)

# Global variables
games_list: List[GameObj] = []
genres_dict: Dict[str, int] = {}
suggestions_cache: List[str] = []
lastReq: float = time.time()

# Helper functions
def add_game(keyword: str) -> None:
    """
    Add a new game into the games list
    :param keyword: Name of the new game to add
    """
    # Lookup in IGDB
    IGDB_res = IGDB.search_game(keyword)
    # Stops if the game doesn't exist as an entry in IGDB
    if len(IGDB_res) == 0:
        return
    # Find the game with the most similar name in the result
    # IGDB search doesn't always find the best match
    most_similar = 0
    similarity_score = fuzz.ratio(IGDB_res[0]['name'], keyword)
    for i in range(len(IGDB_res)):
        if fuzz.ratio(IGDB_res[i]['name'], keyword) > similarity_score:
            similarity_score = fuzz.ratio(IGDB_res[i]['name'], keyword)
            most_similar = i
            print("%d - %s"%(similarity_score, IGDB_res[most_similar]['name']))

    IGDB_res = IGDB_res[most_similar]

    # Extract useful data form the response
    full_name = IGDB_res['name']
    # Get game genres
    genres = []
    if 'genres' in IGDB_res: # maybe add the following code     and len(IGDB_res['genres']) > 0:
        genres = [x['name'] for x in IGDB_res['genres']]

    # Add genre to the overall genre dictionary
    for g in genres:
        genres_dict[g] = genres_dict.get(g, 0) + 1

    # Get game developer
    devs: List[str] = []
    publishers: List[str] = []
    if 'involved_companies' in IGDB_res:
        temp = [x['company']['name'] for x in IGDB_res['involved_companies'] if x['developer'] == True]
        if len(temp) > 0:
            devs = temp[:min(2,len(temp))]

        temp = [x['company']['name'] for x in IGDB_res['involved_companies'] if x['publisher'] == True]
        if len(temp) > 0:
            publishers = temp[:min(2, len(temp))]

    # Get available platforms
    platforms: List[Dict[str, str]] = []
    if 'platforms' in IGDB_res and len(IGDB_res['platforms']) > 0:
        # TODO: Fix this
        platforms = [{'name': x['name'], 'logo': x['platform_logo']['url'][2:]} for x in IGDB_res['platforms']]

    # Game series
    series: str = ""
    series_games: List[str] = []
    if 'collection' in IGDB_res and len(IGDB_res['collection']['games']) > 0:
        series = IGDB_res['collection']['name']
        series_games = [x['name'] for x in IGDB_res['collection']['games'] if x['category'] in {0, 6, 8, 9, 10, 11}]

    # Related games
    related: List[str] = []
    if 'similar_games' in IGDB_res and len(IGDB_res['similar_games']) > 0:
        related = [x['name'] for x in IGDB_res['similar_games']]

    cover_art: str = ""
    if 'cover' in IGDB_res and 'url' in IGDB_res['cover']:
        cover_art = IGDB_res['cover']['url']
        cover_art = "https:" + cover_art.replace("t_thumb", "t_cover_big")

    # Lookup in ITAD
    # TODO: Implement full ITAD feature set
    plain = ITAD.search(full_name)
    prices = {'price': -1, 'lowest': -1}
    if plain is not None:
        lowest = ITAD.load_historical_low([plain])
        if len(lowest) > 0:
            prices['lowest'] = lowest[plain][0]['price']

    # Load OC score
    search_res = OCHandler.search(full_name)
    if OCHandler.check_validity(search_res):
        ID = OCHandler.top_id(search_res)
        OC_score = int(OCHandler.top_critic_score(OCHandler.get_review(ID)))
    else:
        OC_score = -1

    # Time to beat the game
    try:
        TTB = HtmlScraper().search(name=full_name)
        TTB = TTB[0].gameplayMain
    except Exception:
        # Using a generic Exception here because the unofficial HowLongToBeat API doesn't seem to handle errors
        print("Unable to find this game on HowLongToBeat.com")
        TTB = -1

    # TODO: Fix price
    new_game = GameObj(full_name, genres, devs, publishers, series, series_games,
                       related, prices, platforms, TTB, "url", cover_art, OC_score)

    # Add the newly created game object to the list
    games_list.append(new_game)


# This function draws inspiration from contents on the following website:
# https://www.geeksforgeeks.org/fuzzywuzzy-python-library/
def autocomplete(keyword: str) -> List[str]:
    """
    Returns a list of possible games matching the keyword string
    @param keyword: The keyword used to get search suggestions
    @return: A list of matching game strings
    """
    # Get suggestions from IGDB and OpenCritic search
    # l1: List[str] = OCHandler.suggestions(keyword)
    l1: List[str] = IGDB.suggestions(keyword)
    # l1 += l2
    output: Dict[str, int] = {}
    # Calculate the distance from suggestion to keyword
    for e in l1:
        if e not in output.keys():
            # token_set_ratio seems to work best in my experiment
            output[e] = fuzz.token_set_ratio(e, keyword)

    return sorted(output.keys(), key=lambda x: output[x], reverse=True)


def to_dict(obj):
    """
    Returns the dictionary view of a given object
    @param obj: A Python object
    @return: Its dictionary view
    """
    return obj.__dict__

#TODO: Remove debug function
# add_game("Overcooked 2")

def get_games():
    return games_list

# Flask handlers
@app.route("/")
def main_handler():
    return json.dumps([to_dict(x) for x in games_list])


@app.route("/addgame")
def addgame_handler():
    name = request.args.get('name')
    if name is None:
        abort(400)
    add_game(name)

    return json.dumps(to_dict(games_list[len(games_list) - 1]))


@app.route("/autocomplete")
def autocomplete_handler():
    key = request.args.get('key')
    if key is None:
        abort(400)
    if time.time() - lastReq > 0.8:
        suggestions_cache: List[str] = autocomplete(key)

    return json.dumps(suggestions_cache)


@app.route("/getgames")
def getgames_handler():
    return json.dumps(games_list, default=to_dict)

# res = HtmlScraper().search(name=input("Enter a game:\n"))
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
    #
    # keyword = input("Enter the name of a game:\n")
    # # Lookup in IGDB
    # data1 = IGDB.search_game(keyword)[0]
    # full_name = data1['name']
    #
    # # Lookup in ITAD
    # plain = ITAD.search(full_name)
    # lowest = ITAD.load_historical_low([plain])
    # lowest_price = lowest[plain][0]['price']
    #
    # # Load OC score
    # ID = OCHandler.top_id(OCHandler.search(full_name))
    # OC_Score = OCHandler.top_critic_score(OCHandler.get_review(ID))
    #
    # # Time to beat the game
    # TTB = HtmlScraper().search(name=full_name)[0].gameplayMain
    #
    # print()
    # print("=====%s=====" % data1['name'])
    # print("Genre: %s" % ", ".join(x['name'] for x in data1['genres']))
    # print("Developed by: %s" % [x['company']['name'] for x in data1['involved_companies'] if x['developer'] == True][0])
    # print("Published by: %s" % [x['company']['name'] for x in data1['involved_companies'] if x['publisher'] == True][0])
    # print("Historic low price on Steam: %s" % str(round(lowest_price, 2)))
    # print("Average time to beat: %d hrs" % int(TTB))
    # print("OpenCritic score: %d" % OC_Score)

    # Host of localhost when testing
    app.run(host="localhost", port=4567, debug=True)