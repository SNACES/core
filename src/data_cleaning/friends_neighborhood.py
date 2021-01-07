
class FriendsNeighborhood():
    def __init__(self, user_neighbourhood_getter, user_neighbourhood_setter, user_wordcount_getter):
        self.user_neighbourhood_getter = user_neighbourhood_getter
        self.user_neighbourhood_setter = user_neighbourhood_setter
        self.user_wordcount_getter = user_wordcount_getter
    
    def clean_by_friends(self, base_user, threshold):
        user_friends, all_users = self.user_neighbourhood_getter.get_user_neighbourhood(base_user)

        friends_list = []
        for item in all_users:
            user = item
            if user in user_friends and len(all_users[user]) > threshold:
                friends_list.append(user)
        print("original friends number is: ", len(user_friends))
        print("remaining friends number is: ", len(friends_list))

        remaining_neighborhood = {}
        for users in friends_list:
            remaining_neighborhood[users] = all_users[users]
        self.user_neighbourhood_setter.store_user_neighbourhood(remaining_neighborhood)
        

    def clean_by_tweets(self, base_user, threshold):
        user_friends, all_users = self.user_neighbourhood_getter.get_user_neighbourhood(base_user)
        user_word_count = self.user_neighbourhood_getter.get_user_wordcount()
        
        friends_list = []
        for item in all_users:
            user = item
            if user in user_friends and sum(user_word_count[user].values()) > 100:
                friends_list.append(user)
        print("original friends number is: ", len(user_friends))
        print("remaining friends number is: ", len(friends_list))     
        remaining_neighborhood = {}
        for users in friends_list:
            remaining_neighborhood[users] = all_users[users]
        self.user_neighbourhood_setter.store_user_neighbourhood(remaining_neighborhood)


