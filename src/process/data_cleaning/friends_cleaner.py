from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)

class FriendsCleaner():
    def __init__(self, user_friends_getter, cleaned_user_friends_setter, user_getter):
        self.user_friends_getter = user_friends_getter
        self.cleaned_user_friends_setter = cleaned_user_friends_setter
        self.user_getter = user_getter

    def clean_friends(self, user_id, tweet_threshold=200, follower_threshold=100, bot_threshold=True, percent_threshold=30):
        friends_list = self.user_friends_getter.get_user_friends_ids(user_id)

        clean_friends_list = []
        clean_users = []
        for id in friends_list:
            user = self.user_getter.get_user_by_id(id)
            if user is None:
                log.info("Removed user " + str(id) + " because they couldn't be downloaded")
                continue
            elif user.followers_count < follower_threshold:
                log.info("Removed user " + str(id) + " because they have " + str(user.followers_count) +" followers")
                continue
            elif user.statuses_count < tweet_threshold:
                log.info("Removed user " + str(id) + " because they have " + str(user.statuses_count) + " tweets")
                continue
            elif bot_threshold and user.followers_count < user.friends_count:
                log.info("Removed user " + str(id) + " because they follow more people than follow them")
                continue
            else:
                clean_friends_list.append(id)
                clean_users.append(user)

        # TODO Remove more until it meets the percent threshold

        log.info("original friends: " + str(len(friends_list)) + " remaining friends: " + str(len(clean_friends_list)))

        self.cleaned_user_friends_setter.store_friends(user_id, clean_friends_list)
