import time
import urllib.request, urllib.parse, urllib.error
import json

'''
Helper class:
    Handles tasks related to IsThereAnyDeal.com API
'''


class ITAD_handler:
    def __init__(self, api_key: str):
        '''
        Initializes a new instance of the IsThereAnyDeal.com API handler
        :param api_key: API Key
        '''
        self.key:str = api_key

    @staticmethod
    def pretty(obj) -> json:
        '''
        Prettifies JSON file returns by ITAD
        :param obj: JSON file to prettify
        :return: Prettified JSON
        '''
        return json.dumps(obj, sort_keys=True, indent=4)

    @staticmethod
    def safe_get(req: str)-> str:
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


    def request_popular(self, lim: int = 50) -> str:
        '''
        Requests a list of most popular game on IsThereAnyDeal.com.
        :param lim: Number of games to return. Max is 500
        :return: JSON file containing the result of the request
        '''
        baseurl = 'https://api.isthereanydeal.com/v01/stats/popularity/chart/'
        params = {'key': self.key,
                  'offset': 0,
                  'limit': lim}

        return self.safe_get(baseurl + "?" + urllib.parse.urlencode(params))

    @staticmethod
    def parse_popular(result: {}) -> list[str]:
        '''
        Parses the JSON file containing the most popular game on ITAD, sorted by their rank
        :param result: A dictionary of the most popular games
        :return: A list of strings containing the  (UID used by ITAD for each specific game) plains for each game
        '''
        games : list = []
        for entry in result['data']:
            games.append(entry['plain'])
        return games


    def get_games_info(self, games: list[str]) -> str:
        '''
        Requests basic information about the list of games
        :param games: A list of games in the format of plains (UID used by ITAD for each specific game)
        :return: A JSON file containing basic information about the games
        '''
        baseurl = 'https://api.isthereanydeal.com/v01/game/info/'
        params = {'key': self.key,
                  'plains': ','.join(games),    # This creates a comma delimited string with the values in the list
                  'optional': 'metacritic'}
        return self.safe_get(baseurl + "?" + urllib.parse.urlencode(params))


    def get_historic_low(self, games: list[str]) -> json:
        '''
        Requests the historical lowest price of the games on the Steam game store
        :param games: A list of games in the format of plains (maximum length is 5)
        :return: A JSON file containing historic lowest price information about the games
        '''
        baseurl = 'https://api.isthereanydeal.com/v01/game/storelow/'
        params = {'key': self.key,
                  'plains': ','.join(games),    # This creates a comma delimited string with the values in the list
                  'shops': 'steam'}
        return self.safe_get(baseurl + "?" + urllib.parse.urlencode(params))


    def load_historical_low(self, games: list[str]) -> dict:
        '''
        Load the historical lowest price for the given list of games on the Steam game store.
        Uses a loop to overcome the API limitations of 5 games prices per request
        :param games: A list of games in the format of plains
        :return: A dictionary containing the historical low price data
        '''
        temp = {}
        print("Loading price data. This might take a while due to API limitations")
        # Load price data for 5 games at a time
        for i in range(0, len(games), 5):
            # Slows down the program to reduce the request rate
            time.sleep(0.1)
            results = json.loads(self.get_historic_low(games[i:i + 5]))['data']
            temp.update(results)
        # Handle the remaining game in the remainder
        if i < len(games):
            time.sleep(0.1)
            results = json.loads(self.get_historic_low(games[i:len(games)]))['data']
            temp.update(results)
        return temp

# Demo code for the class ported from HW5
# Does NOT work
if __name__ == "__main__":
    from keys import ITAD_key
    handler = ITAD_handler(ITAD_key)

    # Caches the result to avoid exceeding request rate limit
    # Get the list of top 50 games on IsThereAnyDeal
    most_popular = json.loads(handler.request_popular(50))
    most_popular_plains = handler.parse_popular(most_popular)

    # Get basic info about those games
    popular_games_info = json.loads(handler.get_games_info(most_popular_plains))['data']
    # Output a csv file containing review score information about those games
    with open('Part 2 - review score.csv', 'w', encoding='utf-8') as out:
        # Write column titles
        out.write("Rank,Name,Steam pct positive, Metacritic (critic), Metacritic (user)\n")
        # Print game rank & basic info
        for i in range(len(most_popular_plains)):
            plain = most_popular_plains[i]
            info = popular_games_info[plain]
            out.write("%d,%s,%d,"%(i+1, info['title'], info['reviews']['steam']['perc_positive']))

            # Handles the case where Metacritic score is unavailable
            if not info['metacritic'] is None:
                if not info['metacritic']['critic_score'] is None:
                    out.write("%d," %info['metacritic']['critic_score'])
                if not info['metacritic']['user_score'] is None:
                    out.write(str(info['metacritic']['user_score']))
                out.write("\n")
            else:
                out.write(",\n")

    # Get the lowest price of these games on Steam game store
    popular_games_lowest = handler.load_historical_low(most_popular_plains)
    # Output a csv file containing review score information about those games
    with open('Part 2 - lowest price.csv', 'w', encoding='utf-8') as out:
        # Write column titles
        out.write("Rank,Name,Lowest price on Steam\n")
        # Print game rank & basic info
        for i in range(len(most_popular_plains)):
            plain = most_popular_plains[i]
            price = popular_games_lowest[plain]
            out.write("%d,%s,%f\n"%(i+1, popular_games_info[plain]['title'], price[0]['price']))

