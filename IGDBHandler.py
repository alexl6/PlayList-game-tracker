import time
import urllib.request, urllib.parse, urllib.error
import json
# from IGDB_wrapper import IGDBWrapper
from requests import post
from requests.models import Request, Response

API_URL = "https://api.igdb.com/v4/"


def safe_get(req: str) -> str:
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

    def update_token(self) -> None:
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

    def token_expired(self) -> bool:
        """
        Checks whether the token in self has expired
        :return: True if the token has expired, False otherwise.
        """
        return time.time() > self.exp_time

    """
    Initialization & Authentication
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
        if self.token_expired():
            self.update_token()

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

    def search_game(self, name: str) -> list[dict]:
        """
        Searches a game in IGDB

        :param name: Name of the game
        :return: A list of dictionaries containing the name of games that matches the search query & their id
        """
        req = self.api_request(
            'games',
            "search \"%s\"; fields *;" % name
        )
        return json.loads(req)

    # def search_involved_company(self, involved_companies: str, params: str = "") -> list[dict]:
    #     """
    #     Searches for a list of companies involved in a game
    #
    #     :param involved_companies: IDs for a list of involved_companies, comma separated
    #     :param params: Additional parameters specified by the caller
    #     :return: A list of dictionaries representing companies that matches the specific requirements
    #     """
    #     req = self.api_request(
    #         'involved_companies',
    #         "fields company; where id = (%s)%s;" % (involved_companies, params)
    #     )
    #     return json.loads(req)
    #
    # def search_company(self, ids: str) -> list[dict]:
    #     """
    #     Searches a list company
    #
    #     :param ids: IDs for a list of companies, comma separated
    #     :return: List of dictionaries representing companies matching the given IDs
    #     """
    #     req = self.api_request(
    #         'companies',
    #         "fields name; where id = (%s);" % ids
    #     )
    #     return json.loads(req)
    #
    # def get_company(self, involved_companies: list[int], type: str = "developer", limit: int = 2) -> list[str]:
    #     """
    #     Returns a list of companies that worked on the game
    #     :param involved_companies: List of integer IDs representing companies that worked on the game.
    #            "involved_companies" entry in a game dictionary.
    #     :param type: Type of company, defaults to developer (Possible values: "developer","publisher", "porting")
    #     :param limit: Maximum number of companies names to return, defaults to 2.
    #     :return: List of company names
    #     """
    #     # Convert the involved companies id into comma separated values
    #     ids = ",".join(str(i) for i in involved_companies)
    #     # Get copmany ID for those companies that are developers
    #     print(ids)
    #     response = self.search_involved_company(ids, " & %s = true" % type)
    #     # Convert company IDs to CSV
    #     company_ids = ",".join(str(i['company']) for i in response)
    #     # Query for their names
    #     response = self.search_company(company_ids)
    #
    #     developer_names = [i['name'] for i in response]
    #     if len(developer_names) > limit:
    #         return developer_names[:limit]
    #     return developer_names

    def searchgame(self, name: str):
        req = self.api_request(
        """
        fields name, collection, involved_companies.company.*, genres.name, platforms.*;
        search "%s";
        where category = (0,6,8,9,10,11);
        """%name
        )
        return json.loads(req)

# Test code
if __name__ == "__main__":
    from keys import IGDB_ID, IGDB_secret

    test = IGDBHandler(IGDB_ID, IGDB_secret)
    # byte_array = test.api_request(
    #     'games',
    #     'fields id, name; offset 0; where platforms=48;'
    # )
    # print(json.loads(byte_array))
    byte_array = test.api_request(
        'games',
        """
        fields name, collection, involved_companies.company.*, genres.name; platforms.*;
        search "Forza horizon 4";
        where category = (0,6,8,9,10,11);
        """
    )
    print(json.loads(byte_array)[0])
    exit()

    game_info = test.search_game("Minecraft")[0]

    print(game_info)

    developers = test.get_company(game_info['involved_companies'])
    print(developers)
    # involved_companies = (",".join(str(i) for i in game_info["involved_companies"]))
    # print(involved_companies)
    #
    # req = test.api_request(
    #     'involved_companies',
    #     "fields company; where id = (%s) & developer = true; |" % involved_companies
    # )
    # req = json.loads(req)
    # print(req)
    #
    # companies_id = ",".join(str(i['company']) for i in req)
    #
    # companies = test.api_request(
    #     'companies',
    #     "fields name; where id = (%s);" % companies_id
    # )
    #
    # print(companies)
    # involved_company_data = test.search_involved_company(company)[0]
    # print(involved_company_data)

    #
    # company = test.search_company(involved_company_data['company'])
    # print(company)
