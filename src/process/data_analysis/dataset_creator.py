import csv


class DatasetCreator:
    def __init__(self, file_path,
                 user_getter, user_downloader,
                 user_tweet_getter, user_tweet_downloader,
                 user_friend_getter, user_friends_downloader,
                 ranker_list):
        self.user_getter = user_getter
        self.user_downloader = user_downloader
        self.user_tweet_getter = user_tweet_getter
        self.user_tweet_downloader = user_tweet_downloader
        self.user_friend_getter = user_friend_getter
        self.user_friends_downloader = user_friends_downloader
        self.ranker_list = ranker_list
        self.file_path = file_path

    def _get_local_follower_count(self, user, user_ids):
        count = 0
        for user2 in user_ids:
            friend2 = self.user_friend_getter.get_user_friends_ids(user2)
            friend2 = list(map(str, friend2))
            if user in friend2:
                count += 1
        return count

    def _get_local_following_count(self, user, user_ids):
        friend1 = self.user_friend_getter.get_user_friends_ids(user)
        friend1 = list(map(str, friend1))
        count = 0
        for user2 in user_ids:
            if user2 in friend1:
                count += 1
        return count

    def write_dataset(self, filename_prefix, iteration, user_ids,
                      prev_user_ids):
        file_str = filename_prefix + "_iteration_" + str(iteration)
        f = open(self.file_path + file_str + '.csv', 'w')
        content = ["rank", "userid", "username"]
        scores = []
        for ranker in self.ranker_list:
            content.append(ranker.ranking_function_name)
            scores.append(ranker.score_users(user_ids))
        content.extend(["local follower",
                        "local following",
                        "global follower",
                        "global following",
                        "is new user"])
        writer = csv.writer(f)
        writer.writerow(content)
        for i in range(len(user_ids)):
            rank = i
            user_id = user_ids[i]
            user_info = self.user_getter.get_user_by_id(user_id)

            is_new_user = 0
            if user_id not in prev_user_ids:
                is_new_user = 1
            # write a row to the csv file
            row = [rank, user_ids[i], user_info.screen_name]
            for j in range(len(self.ranker_list)):
                row.append(scores[j][user_id])
            row.extend([self._get_local_follower_count(user_id, user_ids),
                        self._get_local_following_count(user_id, user_ids),
                        user_info.followers_count,
                        user_info.friends_count,
                        is_new_user])
            writer.writerow(row)
        # close the file
        f.close()
