from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)

class FriendsCleaner():
    def __init__(self, user_friends_getter, cleaned_user_friends_setter, user_getter):
        self.user_friends_getter = user_friends_getter
        self.cleaned_user_friends_setter = cleaned_user_friends_setter
        self.user_getter = user_getter

    def clean_friends(self, user_id, tweet_threshold=0, follower_threshold=0, bot_threshold=False, percent_threshold=100): # 200, 100, True, 40
        friends_list = self.user_friends_getter.get_user_friends_ids(user_id)
        self.clean_friends_from_list(user_id, friends_list, tweet_threshold, follower_threshold, bot_threshold, percent_threshold)

    def clean_friends_from_list(self, user_id, friends_list, tweet_threshold=0, follower_threshold=0, bot_threshold=False, percent_threshold=100):
        clean_friends_list = []
        clean_users = []
        for id in friends_list:
            user = self.user_getter.get_user_by_id(id)
            if user is None:
                log.info("Removed user " + str(id) + " because they couldn't be downloaded")
                continue
            elif user.followers_count < follower_threshold:
                log.info("Removed user " + str(id) + " because they have " + str(user.followers_count) + " followers")
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


        target_num = int(len(friends_list) * (percent_threshold/100))

        curr_tweet_thresh = tweet_threshold
        curr_follower_thresh = follower_threshold
        while len(clean_users) > target_num:
            curr_tweet_thresh += 200
            curr_follower_thresh += 100
            log.info("Increasing Thresholds to " + str(curr_tweet_thresh)
                + " tweets and " + str(curr_follower_thresh)
                + " followers")

            new_clean_users = []
            for user in clean_users:
                if user.followers_count < curr_follower_thresh:
                    log.info("Removed user " + str(user.id) + " because they have " + str(user.followers_count) +" followers")
                    clean_friends_list.remove(user.id)
                elif user.statuses_count < curr_tweet_thresh:
                    log.info("Removed user " + str(user.id) + " because they have " + str(user.statuses_count) + " tweets")
                    clean_friends_list.remove(user.id)
                else:
                    new_clean_users.append(user)

            clean_users = new_clean_users


        log.info("original friends: " + str(len(friends_list)) + " remaining friends: " + str(len(clean_friends_list)))

        if self.cleaned_user_friends_setter is not None:
            self.cleaned_user_friends_setter.store_friends(user_id, clean_friends_list)

        return clean_friends_list
