# Import packages
import time
import json
from flask import Flask, request, abort
from flask_cors import CORS
from hltbapi import HtmlScraper
from gameobj import GameObj
from typing import List, Dict
from fuzzywuzzy import fuzz
from threading import Thread

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
suggestions_cache: List[str] = []
last_req: float = time.time()


# Multithreading helper functions
# Previously, the program performance is poor due to the amount of time it takes to
# sequentially call and wait for the response from 4 APIs. Now the program
# can run 3 of the 4 games
def run_search_oc(full_name: str, return_target: List[int]):
    """
    Helper function for multithreading: Calls the OCHandler to get the OpenCritic Review score
    :param full_name: Full name fo the game (supplied from IGDB data)
    :param return_target: List target to return the result after the thread finishes
    """
    search_res = OCHandler.search(full_name)
    if OCHandler.check_validity(search_res):
        ID = OCHandler.top_id(search_res)
        return_target[0] =int(OCHandler.top_critic_score(OCHandler.get_review(ID)))


def run_search_itad(full_name: str, return_target: List[dict]):
    """
    Helper function for multithreading: Calls the ITADHandler to get the price data from IsThereAnyDeal.com
    :param full_name: Full name fo the game (supplied from IGDB data)
    :param return_target: List target to return the result after the thread finishes
    """
    plain: str = ITAD.search(full_name)
    if plain is not None:
        try:
            price_data = ITAD.get_price_data(plain)
            return_target[0] = price_data
        except Exception:
            return_target[0] = None


def run_search_hltb(full_name: str, return_target: List[int]):
    """
    Helper function for multithreading: Uses the unofficial HowLongToBeat.com wrapper to get the time it takes to beat the game
    :param full_name: Full name fo the game (supplied from IGDB data)
    :param return_target: List target to return the result after the thread finishes
    """
    try:
        data = HtmlScraper().search(name=full_name)
        return_target[0] = data[0].gameplayMain
    except Exception:
        # Using a generic Exception here because the unofficial HowLongToBeat API doesn't seem to handle errors
        print("Unable to find this game on HowLongToBeat.com")
        return_target[0] = -1


def add_game(full_name: str):
    """
    Add a new game into the games list. Expects all calls to this function to provide a well-formatted name.
    Accepts user selection from a list of suggested names, avoid directly sending name from input textbox.
    :param full_name: Full name of the new game to add (Should be well-formatted)
    """
    # Experimental: Parallelize IsThereAnyDeal, OpenCritic, and HowLongToBeat search to improve user experience
    # Create empty lists (trick Python to pass by reference) and pass them into the threads to holds their results
    OC_score = [-1]
    prices = [{}]
    time_to_beat = [-1]

    itad_thread: Thread = Thread(target=run_search_itad, args=(full_name, prices))
    itad_thread.start()
    hltb_thread: Thread = Thread(target=run_search_hltb, args=(full_name, time_to_beat))
    hltb_thread.start()
    opencritic_thread: Thread = Thread(target=run_search_oc, args=(full_name, OC_score))
    opencritic_thread.start()

    # Continue running current thread with IGDBHandler
    IGDB_res = IGDB.search_game(full_name)
    # Stops if the game doesn't exist as an entry in IGDB, should not be triggered if the keyword is well-formatted
    if len(IGDB_res) == 0:
        print("Invalid input detected")
        return
    
    # Find the game with the most similar name in the result
    # IGDB search doesn't always find the best match
    most_similar = 0
    similarity_score = fuzz.ratio(IGDB_res[0]['name'], full_name)
    for i in range(len(IGDB_res)):
        if fuzz.ratio(IGDB_res[i]['name'], full_name) > similarity_score:
            similarity_score = fuzz.ratio(IGDB_res[i]['name'], full_name)
            most_similar = i
            #print("%d - %s"%(similarity_score, IGDB_res[most_similar]['name']))

    IGDB_res = IGDB_res[most_similar]
    
    # Extract game name from the response before 
    full_name = IGDB_res['name']

    # Continue process IGDB data in the current thread
    # Get game genres
    genres: List[str] = []
    if 'genres' in IGDB_res:
        genres = [x['name'] for x in IGDB_res['genres']]

    # Get game developer & publisher
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
    platforms: List[str] = []
    if 'platforms' in IGDB_res and len(IGDB_res['platforms']) > 0:
        platforms = [x['name'] for x in IGDB_res['platforms']]

    # Game series
    series: str = ""
    series_games: List[str] = []
    if 'collection' in IGDB_res and len(IGDB_res['collection']['games']) > 0:
        series = IGDB_res['collection']['name']
        series_games = [x['name'] for x in IGDB_res['collection']['games'] if x['category'] in {0, 6, 8, 9, 10, 11}]
        if len(series_games) >= 4:
            series_games = series_games[:5]
            series_games.append("...")

    # Related games
    related: List[str] = []
    if 'similar_games' in IGDB_res and len(IGDB_res['similar_games']) > 0:
        related = [x['name'] for x in IGDB_res['similar_games']]

    # URL to cover art on IGDB
    cover_art: str = ""
    if 'cover' in IGDB_res and 'url' in IGDB_res['cover']:
        cover_art = IGDB_res['cover']['url']
        cover_art = "https:" + cover_art.replace("t_thumb", "t_cover_big")

    # Wait for other threads to finish
    opencritic_thread.join()
    itad_thread.join()
    hltb_thread.join()

    # Create & add the new game object
    new_game = GameObj(full_name, genres, devs, publishers, series, series_games,
                       related, prices[0], platforms, time_to_beat[0], "url", cover_art, OC_score[0])
    games_list.append(new_game)


def autocomplete(keyword: str) -> List[str]:
    """
    Returns a list of possible games matching the keyword string.
    @param keyword: The keyword used to get search suggestions
    @return: A list of matching game strings
    """
    # Get suggestions from IGDB search
    l1: List[str] = IGDB.suggestions(keyword)
    output: Dict[str, int] = {}
    # The list returned by the API can be ordered in strange manners, attempt to fix it here with sort.
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


def clear_games():
    """
    Clears all games stored in the program, resets to initial state
    """
    games_list.clear()
    suggestions_cache.clear()
    last_req = time.time()


# Flask handlers
@app.route("/")
def main_handler():
    return json.dumps([to_dict(x) for x in games_list])


@app.route("/addgame")
def add_game_handler():
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
    if time.time() - last_req > 0.8:
        global suggestions_cache
        suggestions_cache= autocomplete(key)

    return json.dumps(suggestions_cache)


@app.route("/getgames")
def getgames_handler():
    return json.dumps(games_list, default=to_dict)


@app.route("/clearall")
def cleargames_handler():
    clear_games()
    return json.dumps("OK")


# Main method
if __name__ == "__main__":
    # test = input("Game name?\n")
    # add_game(test)
    # exit()

    # Host of localhost when testing
    app.run(host="localhost", port=4567, debug=True)