import time
import urllib.request, urllib.parse, urllib.error
import json
import requests

def safe_get(req: str) -> str:
    '''
    Safely make an request and returns the result in a json file
    :param req: A parsed request encoded by urllib.parse.urlencode
    :return: Requested object in json. Returns None if an error has occured
    '''
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

class IGDB_handler:
    """
    Handles operations using IGDB.com API
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

        #TODO: Remove debug code - Temporary cache for token
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
        if auth is None:
            raise Exception("Cannot authenticate to IGDB")

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
        if auth is None:
            raise Exception("Cannot authenticate to IGDB")
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


if __name__ == "__main__":
    from keys import IGDB_ID, IGDB_secret
    test = IGDB_handler(IGDB_ID, IGDB_secret)
