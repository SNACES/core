from typing import Dict
from src.data_cleaning.DAOFactory.FriendsCleaningDAOFactory import FriendsCleaningDAOFactory
from src.data_cleaning.friends_neighborhood import FriendsNeighborhood

class FriendsCleaningActivity():
    """
    Get rid of inactive users.
    """
    def __init__(self, config: Dict):
        self.friends_neighborhood = None

        self.configure(config)
    
    def configure(self, config: Dict):
        if config is not None:
            input_datastore = config["input-datastore"]
            input_user_neighborhood = input_datastore["User-Friend"]
            input_user_wordcount = input_datastore["User-WordCount"]

            user_neighbourhood_getter = FriendsCleaningDAOFactory.create_getter(input_user_neighborhood)
            user_wordcount_getter = FriendsCleaningDAOFactory.create_wordcount_getter(input_user_wordcount)

            output_datastore = config["output-datastore"]
            output_user_neighbourhood = output_datastore["User-Friend"]

            user_neighbourhood_setter = FriendsCleaningDAOFactory.create_setter(output_user_neighbourhood)

            friends_neighborhood = FriendsNeighborhood(user_neighbourhood_getter, user_neighbourhood_setter, user_wordcount_getter)

            self.friends_neighborhood = friends_neighborhood
    
    def clean_by_friends(self, base_user, threshold):
        self.friends_neighborhood.clean_by_friends(base_user, threshold)
    
    def clean_by_tweets(self,  base_user, threshold):
        self.friends_neighborhood.clean_by_tweets(base_user, threshold)

            

