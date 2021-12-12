import time
import urllib.request, urllib.parse, urllib.error
import json

from typing import List

'''
Helper class:
    Handles tasks related to IsThereAnyDeal.com API
'''

def _safe_get(req: str) -> str:
    """
    Safely make an request and returns the result in a json file
    :param req: A parsed request encoded by urllib.parse.urlencode
    :return: Requested object in json. Returns None if an error has occured
    """
    try:
        return urllib.request.urlopen(req).read()
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print("The server couldn't fulfill the request.")
            print("Error code: ", e.code)
        elif hasattr(e, 'reason'):
            print("We failed to reach a server")
            print("Reason: ", e.reason)
        return None


class ITADHandler:
    def __init__(self, api_key: str):
        """
        Initializes a new instance of the IsThereAnyDeal.com API handler
        :param api_key: API Key
        """
        self.key:str = api_key

    def request_popular(self, lim: int = 50) -> str:
        """
        Requests a list of most popular game on IsThereAnyDeal.com.
        :param lim: Number of games to return. Max is 500
        :return: JSON file containing the result of the request
        """
        baseurl = 'https://api.isthereanydeal.com/v01/stats/popularity/chart/'
        params = {'key': self.key,
                  'offset': 0,
                  'limit': lim}

        return _safe_get(baseurl + "?" + urllib.parse.urlencode(params))

    @staticmethod
    def parse_popular(result: {}) -> List[str]:
        """
        Parses the JSON file containing the most popular game on ITAD, sorted by their rank
        :param result: A dictionary of the most popular games
        :return: A list of strings containing the  (UID used by ITAD for each specific game) plains for each game
        """
        games : list = []
        for entry in result['data']:
            games.append(entry['plain'])
        return games

    def get_games_info(self, games: List[str]) -> str:
        """
        Requests basic information about the list of games
        :param games: A list of games in the format of plains (UID used by ITAD for each specific game)
        :return: A JSON file containing basic information about the games
        """
        baseurl = 'https://api.isthereanydeal.com/v01/game/info/'
        params = {'key': self.key,
                  'plains': ','.join(games),    # This creates a comma delimited string with the values in the list
                  'optional': 'metacritic'}
        return _safe_get(baseurl + "?" + urllib.parse.urlencode(params))

    def get_historic_low(self, game: str) -> dict:
        """
        Requests the historical lowest price of the games on the Steam game store
        :param game: A game's name (string)
        :return: A JSON file containing historic lowest price information about the games
        """
        baseurl = 'https://api.isthereanydeal.com/v01/game/storelow/'
        params = {'key': self.key,
                  'plains': game,  # This creates a comma delimited string with the values in the list
                  'region': 'us'}
        data = _safe_get(baseurl + "?" + urllib.parse.urlencode(params))
        if data is None:
            return None
        return json.loads(data)['data']

    def get_current_price(self, game: str) -> dict:
        """
        Requests the current lowest price of the games on the Steam game store
        :param game: A game's name (string)
        :return: A JSON file containing current price information about the games
        """
        baseurl = 'https://api.isthereanydeal.com/v01/game/prices/'
        params = {'key': self.key,
                  'plains': game,    # This creates a comma delimited string with the values in the list
                  'region': 'us'}
        data = _safe_get(baseurl + "?" + urllib.parse.urlencode(params))
        if data is None:
            return None
        return json.loads(data)['data']

    def search(self, game: str) -> str:
        """
        Performs lookup for the plain of a given game title.
        :param game: Name of the game
        :return: The matching plain in string
        """
        baseurl = "https://api.isthereanydeal.com/v02/game/plain/"
        params = {'key': self.key, 'title': game}
        response = _safe_get(baseurl + "?" + urllib.parse.urlencode(params))
        # Returns None if error/no match
        if response is None:
            return None
        response = json.loads(response)
        if not response['.meta']['match']:
            return None
        return response['data']['plain']

# Demo code for the class ported from HW5
if __name__ == "__main__":
    from keys import ITAD_key
    handler = ITADHandler(ITAD_key)

    keyword = input("Enter a game:\n")
    # Search demo
    plain = handler.search(keyword)

    print(plain)

    val = handler._get_current_price(plain)
    print(val)
    val = json.loads(val)
    print(val)
    exit()
    # Caches the result to avoid exceeding request rate limit
    # Get the list of top 50 games on IsThereAnyDeal
    most_popular = json.loads(handler.request_popular(50))
    most_popular_plains = handler.parse_popular(most_popular)

    # Get basic info about those games
    popular_games_info = json.loads(handler.get_games_info(most_popular_plains))['data']


