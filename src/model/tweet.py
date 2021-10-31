from typing import Dict, Optional
import json

class Tweet:
    """
    A class to represent a tweet
    """
    def __init__(self, id: str, user_id: str, created_at: str, text: str,
            lang: str, retweet_id: Optional[int],
            retweet_user_id: Optional[int], quote_id: Optional[int],
            quote_user_id: Optional[int]):
        """
        Default constructor for a tweet

        @param id the tweet's unique id
        @param user_id the id of the user who tweeted the tweet
        @param created_at a date string representation of the date the tweet
            was created
        @param text the text of the tweet
        @param lang the language of the tweet
        @param retweet_id if the tweet is a retweet, this is the id of the
            original tweet, otherwise it is None
        @param retweet_user_id if the tweet is a retweet, this is the user
            id of the original tweet's tweeter, otherwise it is None
        @param quote_id if the tweet is a quote, this is the id of the
            original tweet, otherwise it is None
        @param quote_user_id if the tweet is a quote, this is the user id of the
            original tweet's tweeter, otherwise it is None
        """
        self.id = id
        self.user_id = user_id
        self.created_at = created_at
        self.text = text
        self.lang = lang
        self.retweet_id = retweet_id
        self.retweet_user_id = retweet_user_id
        self.quote_id = quote_id
        self.quote_user_id = quote_user_id

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
        tweet = Tweet(
            obj.get("id"),
            obj.get("user_id"),
            obj.get("created_at"),
            obj.get("text"),
            obj.get("lang"),
            obj.get("retweet_id"),
            obj.get("retweet_user_id"),
            obj.get("quote_id"),
            obj.get("quote_user_id"))

        return tweet

    def fromDict(dict: Dict):
        tweet = Tweet(dict["id"], dict["user_id"], dict["created_at"],
            dict["text"], dict["lang"], dict["retweet_id"],
            dict["retweet_user_id"], dict["quote_id"], dict["quote_user_id"])

        return tweet

    def fromTweepyJSON(json_in: Dict):
        """
        Given a json representation of a tweet returned by Tweepy, returns the
        tweet object

        @param json_in the json to convert to a Tweet

        @return the Tweet object
        """
        id = json_in.get("id")
        user_id = json_in.get("user").get("id")
        created_at = json_in.get("created_at")
        text = json_in.get("text")
        lang = json_in.get("lang")

        retweet_id = json_in.get("retweeted_status").get("id") \
            if json_in.get("retweeted_status") is not None \
            else None
        retweet_user_id = json_in.get("retweeted_status").get("user").get("id") \
            if json_in.get("retweeted_status") is not None \
            else None
        quote_id = json_in.get("quoted_status").get("id") \
            if json_in.get("quoted_status") is not None \
            else None
        quote_user_id = json_in.get("quoted_status").get("user").get("id") \
            if json_in.get("quoted_status") is not None \
            else None

        tweet = Tweet(id=id, user_id=user_id, created_at=created_at, text=text,
            lang=lang, retweet_id=retweet_id, retweet_user_id=retweet_user_id,
            quote_id=quote_id, quote_user_id=quote_user_id)

        return tweet

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
