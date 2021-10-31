from typing import Dict, Optional
import json

class LikedTweet:
    """
    A class to represent a tweet
    """
    def __init__(self, id: str, user_id: str, created_at: str, liked_id: int):
        """
        Default constructor for a tweet

        @param id the tweet's unique id
        @param user_id the id of the user who tweeted the tweet
        @param created_at a date string representation of the date the tweet
            was created
        @param liked_id the id of the user who liked the tweet
        """
        self.id = id
        self.user_id = user_id
        self.created_at = created_at
        self.liked_id = liked_id

    def toJSON(self) -> str:
        """
        Returns a json corresponding to the given tweet object

        @return a json representation of the tweet
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)

    def fromJSON(json_in: str):
        """
        Given a json representation of a tweet, returns the tweet object

        @param json_in the json to convert to a Tweet

        @return the Tweet object
        """
        obj = json.loads(json_in)
        tweet = LikedTweet(
            obj.get("id"),
            obj.get("user_id"),
            obj.get("created_at"),
            obj.get("liked_id"))
        return tweet

    def fromDict(dict: Dict):
        tweet = LikedTweet(dict["id"], dict["user_id"], dict["created_at"],
                      dict["liked_id"])
        return tweet

    def fromTweepyJSON(json_in: Dict, liked_id):
        """
        Given a json representation of a tweet returned by Tweepy, returns the
        tweet object

        @param json_in the json to convert to a Tweet

        @return the Tweet object
        """
        id = json_in.get("id")
        created_at = json_in.get("created_at")
        user_id = json_in.get("user").get("id")

        tweet = LikedTweet(id=id, user_id=user_id, created_at=created_at, liked_id=liked_id)

        return tweet

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
