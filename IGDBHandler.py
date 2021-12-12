"""
A portion of this program uses the IGDB API Python wrapper
Credit: https://github.com/twitchtv/igdb-api-python
"""


import time
import urllib.request, urllib.parse, urllib.error
import json
from requests import post
from requests.models import Request, Response
from typing import List

API_URL = "https://api.igdb.com/v4/"


def safe_get(req) -> str:
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


class IGDBHandler:
    """
    Handles operations using IGDB.com API
    """

    """
    Initialization & Authentication
    """

    def __init__(self, client_id: str, secret: str):
        """
        Initializes an instance of IGDB_handler that handles requests/data processing to IGDB

        :param client_id: Client ID string
        :param secret: Client secret string
        """
        # Cache client ID and secret
        self.client_id = client_id
        self.secret = secret

        # TODO: Remove debug code - Temporary cache for token
        from keys import IGDB_token
        self.token = IGDB_token
        self.exp_time = time.time() + 2134700
        return

        # Create token request as a JSON file
        data = {'client_id': client_id, 'client_secret': secret, 'grant_type': "client_credentials"}
        data = urllib.parse.urlencode(data).encode()

        # Request authentication token from IGDB server
        req = urllib.request.Request(url="https://id.twitch.tv/oauth2/token", data=data, method="POST")
        # Make request
        auth = safe_get(req)

        # TODO: Remove debug code
        print(auth)
        # Load request & cache the access token
        auth = json.loads(auth)

        # Make sure we received a token
        if "expires_in" not in auth or "access_token" not in auth:
            raise Exception("Cannot authenticate to IGDB")
        # Save the returned token and its expiration time
        self.exp_time = time.time() + auth['expires_in'] - 10
        self.token = auth['access_token']

    def _update_token(self) -> None:
        """
        Updates the access_token in this instance of IGDB handler
        """
        # Create token request as a JSON file
        data = {'client_id': self.client_id, 'client_secret': self.secret, 'grant_type': "client_credentials"}
        data = urllib.parse.urlencode(data).encode()
        # Request authentication token from IGDB server
        req = urllib.request.Request(url="https://id.twitch.tv/oauth2/token", data=data, method="POST")

        # Make request
        auth = safe_get(req)
        # Load request & cache the access token
        auth = json.loads(auth)

        # Make sure we received a token
        if "expires_in" not in auth or "access_token" not in auth:
            raise Exception("Cannot authenticate to IGDB")
        # Save the returned token and its expiration time
        self.exp_time = time.time() + auth['expires_in'] - 10
        self.token = auth['access_token']

    def _token_expired(self) -> bool:
        """
        Checks whether the token in self has expired
        :return: True if the token has expired, False otherwise.
        """
        return time.time() > self.exp_time

    """
    Requesting game from IGDB
    api_request(), _build_url(), and _compose_request() contains code from the official IGDB API wrapper
    """
    def api_request(self, endpoint: str, query: str) -> Response:
        """
        Takes an endpoint and the Apicalypse query and returns the api response as a byte string.
        """
        url = IGDBHandler._build_url(endpoint)
        params = self._compose_request(query)

        response = post(url, **params)
        response.raise_for_status()

        return response.content

    @staticmethod
    def _build_url(endpoint: str = '') -> str:
        return ('%s%s' % (API_URL, endpoint))

    def _compose_request(self, query: str) -> Request:
        if not query:
            raise Exception(
                'No query provided!\nEither provide an inline query following Apicalypse\'s syntax or an Apicalypse object')
        # Update the token of this instance
        if self._token_expired():
            self._update_token()

        request_params = {
            'headers': {
                'Client-ID': self.client_id,
                'Authorization': ('Bearer %s' % (self.token)),
            }
        }

        if isinstance(query, str):
            request_params['data'] = query
            return request_params

        raise TypeError(
            'Incorrect type of argument \'query\', only Apicalypse-like strings or Apicalypse objects are allowed')

    def search_game(self, name: str) -> List[dict]:
        req = self.api_request(
            'games',
            """
            fields name, involved_companies.company.name, involved_companies.developer,
             involved_companies.publisher, genres.name, platforms.name, platforms.platform_logo.url, 
             collection.name, collection.games.name, collection.games.category, collection.url,
             similar_games.name, similar_games.genres.name, cover.url;
            search "%s";
            where category = (0,3,6,8,9,10,11);
            """%name
        )
        return json.loads(req)

    def suggestions(self, name: str) -> List[str]:
        req = self.api_request(
            'games',
            """
            fields name;
            search "%s";
            where category = (0,3,6,8,9,10,11);
            """%name
        )
        res = json.loads(req)
        if len(res) == 0:
            return []
        return [x['name'] for x in res]

# Test code
if __name__ == "__main__":
    from keys import IGDB_ID, IGDB_secret

    test = IGDBHandler(IGDB_ID, IGDB_secret)
    # byte_array = test.api_request(
    #     'games',
    #     'fields id, name; offset 0; where platforms=48;'
    # )
    # print(json.loads(byte_array))
    # byte_array = test.api_request(
    #     'games',
    #     """
    #     fields name, involved_companies.company.name, involved_companies.developer,
    #          involved_companies.publisher, genres.name, platforms.name, platforms.platform_logo.url,
    #          collection.name, collection.games.name, collection.games.category, collection.url,
    #          similar_games.name, similar_games.genres.name;
    #     search "Forza horizon 4";
    #     where category = (0,6,8,9,10,11);
    #     """
    # )
    # print(json.loads(byte_array)[0])


    keyword = input("Enter a game:\n")
    print(test.search_game(keyword))
    exit()
