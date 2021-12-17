from typing import List
import json

class GameObj:
    def __init__(self, name:str,
                 genre:List[str],
                 developer: List[str],
                 publisher: List[str],
                 series: str,
                 series_games: List[str],
                 related: List[str],
                 prices: dict,
                 platforms: List[str],
                 time_to_beat: float,
                 urls: dict,
                 cover_art: str,
                 opencritic: int = -1) -> None:
        '''
        Creates a new instance of the game object
        :param name: Name of the game
        :param genre: Genre of a game (list of strings)
        :param developer: Name of the developer (if there are multiple, put in the first 2)
        :param publisher: Name of the publisher (if there are multiple, put in the first 2
        :param related: List of related games
        :param prices: Price & store information for the game
        :param platforms: Available platforms
        :param opencritic: Metacritic score (-1 if not available)
        :param time_to_beat: Time to beat the game (in hours)
        :param url: URL to the game on IsThereAnyDeal
        :param cover_art: URL to the cover art
        '''
        # TODO: Update price to be its own object
        self.name: str = name
        self.genre: List[str] = genre
        self.developer: List[str] = developer
        self.publisher: List[str] = publisher
        self.series: str = series
        self.series_games: List[str] = series_games
        self.related: List = related
        self.prices: dict = prices
        self.platforms: List[str] = platforms
        self.time_to_beat: float = time_to_beat
        self.urls: dict = urls
        self.cover_art: str = cover_art
        self.opencritic: int = opencritic
