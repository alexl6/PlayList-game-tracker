class game:
    def __init__(self, name:str,
                 genre:list[str],
                 developer: str,
                 price: float,
                 platforms: list[str],
                 time_to_beat: float,
                 url: str,
                 cover_art: str,
                 metacritic: int = -1) -> None:
        '''
        Creates a new instance of the game object
        :param name: Name of the game
        :param genre: Genre of a game (list of strings)
        :param developer: Name of the developer (if there are multiple, put in the first one)
        :param price: Current price of the game
        :param platforms: Available platforms (list of strings)
        :param metacritic: Metacritic score (-1 if not available)
        :param time_to_beat: Time to beat the game (in hours)
        :param url: URL to the game on IsThereAnyDeal
        :param cover_art: URL to the cover art
        '''
        # TODO: Update price to be its own object
        self.name: str = name
        self.genre: list[str] = genre
        self.developer: str = developer
        self.price: float = price
        self.platforms: list[str] = platforms
        self.metacritic: int = metacritic
        self.time_to_beat: float = time_to_beat
        self.url: str = url
        self.cover_art: str = cover_art

