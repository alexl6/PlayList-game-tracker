"""
This program implements OpenCritic API
https://app.swaggerhub.com/apis-docs/OpenCritic/OpenCritic-API/0.1.0
"""

import time
import urllib.request, urllib.parse, urllib.error
import json

from typing import List


def _safe_get(req: str) -> str:
    """
    Safely make an request and returns the result in a json file

    :param req: A parsed request encoded by urllib.parse.urlencode
    :return: Requested object in json. Returns None if an error has occured
    """
    try:
        # Need to provide a valid user-agent header (otherwise we get 403 error)
        request = urllib.request.Request(req, headers={'User-Agent': 'Mozilla/5.0'})
        return urllib.request.urlopen(request).read()
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print("The server couldn't fulfill the request.")
            print("Error code: ", e.code)
        elif hasattr(e, 'reason'):
            print("We failed to reach a server")
            print("Reason: ", e.reason)
        return None


def search(game: str) -> List[dict]:
    """
    Search for matching entries in OpenCritic for a given game

    :param game: Name of the game
    :return: A list of dictionaries representing games that matches the queried term
    """
    baseurl = "https://api.opencritic.com/api/game/search"
    param = {'criteria': game}
    # Switch alternate quote_via function to work with the API
    return json.loads(_safe_get(baseurl + "?" + urllib.parse.urlencode(param, quote_via=urllib.parse.quote)))


def top_id(games: List[dict]) -> int:
    """
    Returns the OpenCritic game ID for the top result in a given list of games

    :param games: A list of games dictionary
    :return: Integer game ID of the first game in the list
    """
    return games[0]['id']


def check_validity(games: List[dict]) -> bool:
    return games[0]['dist'] < 0.7


def get_review(id: int) -> dict:
    """
    Gets the core game data for the game represented by a given game ID
    :param id: Game ID of the game to search
    :return: A dictionary object containing basic information about the game
    """
    # Encode game ID in the url directly
    url = "https://api.opencritic.com/api/game/%d"%id
    # Switch alternate quote_via function to work with the API
    return json.loads(_safe_get(url))


def top_critic_score(game_data: dict) -> int:
    """
    Gets the average top critic review score for a given game data object. This is the main metric
    displayed on OpenCritic's website.

    :param game_data: A game data object from OpenCritic
    :return: Average top critic score
    """
    return int(game_data['topCriticScore'])


if __name__ == '__main__':
    val = search(input("Enter a game:\n"))

    game_id = top_id(val)
    review = get_review(game_id)
    print(top_critic_score(review))
