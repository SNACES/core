class User:
    """
    A class that represents a twitter user
    """
    def __init__(self, id: int, screen_name: str, name: str, created_at: str,
            followers_count: int, friends_count: int, listed_count: int,
            favourites_count: int, statuses_count: int, default_profile: bool,
            default_profile_image: bool):
        """
        Constructor for a User object

        @param id the unique id of the twitter user
        @param screen_name the screen name of the twitter user
        @param name the name of the twitter user
        @param created_at the date the twitter user was created
        @param followers_count the number of followers of the twitter user
        @param friends_count the number of friends of the twitter user
        @param listed_count the number of lists the user is a part of
        @param favourites_count the number of tweets this user has liked
        @param statuses_count the number of tweets the user has tweeted
            (including retweets)
        @param default_profile a boolean that is true iff the user has not
            edited their theme or background
        @param default_profile_image a boolean that is true iff the user has
            not edited their profile image
        """
        self.id = id
        self.screen_name = screen_name
        self.name = name
        self.created_at = created_at
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.listed_count = listed_count
        self.favourites_count = favourites_count
        self.statuses_count = statuses_count
        self.default_profile = default_profile
        self.default_profile_image = default_profile_image

    def toJSON(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
            indent=4)

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
