from src.process.ranking.intersection_ranker import IntersectionRanker
from src.shared.utils import get_project_root
from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)
DEFAULT_PATH = str(
    get_project_root()) + "/src/scripts/config/create_social_graph_and_cluster_config.yaml"


class CommunityExpansionAlgorithm:
    def __init__(self, user_getter, user_downloader,
                 user_tweet_getter, user_tweet_downloader,
                 user_friend_getter, user_friends_downloader,
                 ranker_list, dataset_creator):
        self.user_getter = user_getter
        self.user_downloader = user_downloader
        self.user_tweet_getter = user_tweet_getter
        self.user_tweet_downloader = user_tweet_downloader
        self.user_friend_getter = user_friend_getter
        self.user_friends_downloader = user_friends_downloader
        self.ranker_list = ranker_list
        self.intersection_ranker = IntersectionRanker(self.ranker_list)
        self.dataset_creator = dataset_creator

    def _download_friends(self, community):
        for user in community:
            friend_list = \
                self.user_friend_getter.get_user_friends_ids(str(user))
            if friend_list is None:
                log.info("Download friends of " + str(user))
                self.user_friends_downloader.download_friends_ids_by_id(
                    user)

    def _download_user_info_and_tweet(self, curr_candidate, community):
        new_candidate = []
        for i in range(len(curr_candidate)):
            user = curr_candidate[i]
            user_info = self.user_getter.get_user_by_id(user)
            if user_info is None:
                try:
                    self.user_downloader.download_user_by_id(user)
                    user_info = self.user_getter.get_user_by_id(user)
                    user = user_info.id
                    if str(user_info.id) not in community:
                        new_candidate.append(user_info.id)
                except:
                    log.info("[Download Error] Cannot download user " + user)
            else:
                user = user_info.id
                if str(user_info.id) not in community:
                    new_candidate.append(user_info.id)
            friend_list = self.user_friend_getter.get_user_friends_ids(
                user)
            if friend_list is None:
                self.user_friends_downloader.download_friends_ids_by_id(
                    user)
        self.user_tweet_downloader.download_user_tweets_by_user_list(
            new_candidate)
        return new_candidate

    def filter_candidates(self, threshold, top_size, candidates_size,
                          large_account_threshold,
                          community, candidates):
        """
        threshold: candidate must have utility more than <threshold>% of
            average utility of top <top_size> users.
        top_size: Top <top_size> users are used for measurement
        candidates_size: Only keep <candidates_size> user
            by their intersection rank.
        large_account_threshold: If no restriction on large account,
            large_account_threshold = -1. Otherwise, candidate cannot have
            more than <large_account_threshold>% number of followers than
            average of top <top_size> users.
        """
        log.info("Candidate utilities higher than " +
                 str(threshold) + "% of average of top " + str(top_size) +
                 " users in the community.")
        # Calculate threshold for each utility
        thresholds = []
        for i in range(len(self.ranker_list)):
            thresholds.append(0)
            for j in range(top_size):
                user = community[j]
                thresholds[i] += self.ranker_list[i].score_user(user, community)
            thresholds[i] = thresholds[i] / float(top_size)
            log.info("Top " + str(top_size) + " users average " +
                     self.ranker_list[i].ranking_function_name + " is " +
                     str(thresholds[i]))
            thresholds[i] = thresholds[i] * threshold
            log.info("Candidate " + self.ranker_list[i].ranking_function_name +
                     " must be no less than " + str(thresholds[i]))

        threshold_followers = 0
        # If filter user with large size of followers:
        if large_account_threshold != -1:
            for j in range(top_size):
                user = community[j]
                threshold_followers += self.user_getter.get_user_by_id(
                    user).followers_count
            threshold_followers = threshold_followers / top_size
            log.info("Top " + str(top_size) +
                     " users average number of follower is " +
                     str(threshold_followers))
            threshold_followers = threshold_followers * large_account_threshold
            log.info("Candidate number of follower must be no more than " +
                     str(threshold_followers))
        filtered_candidates = []
        for candidate in candidates:
            accept = True
            for i in range(len(self.ranker_list)):
                score = self.ranker_list[i].score_user(
                    str(candidate), [str(candidate)] + community)
                if score < thresholds[i]:
                    accept = False
            if large_account_threshold != -1 and \
                    self.user_getter.get_user_by_id(candidate).followers_count > \
                    threshold_followers:
                accept = False
            if accept:
                filtered_candidates.append(str(candidate))
        log.info(
            "Candidates after utility filtering: " + str(filtered_candidates))
        log.info("Candidate list length after utility filtering: " + str(
            len(filtered_candidates)))

        # Take the top <candidate_size> new users by intersection_ranking
        candidate_list = []
        intersection_ranking = \
            self.intersection_ranker.rank(filtered_candidates + community)
        for user in intersection_ranking:
            if user not in community:
                candidate_list.append(user)
            if len(candidate_list) == candidates_size:
                break
        return candidate_list

    def find_potential_candidate(self, users, num_of_candidate, threshold):
        """
        Find potential candidates from users' followings
        in current community.
        """
        # user_map: key: candidate, value: number of follower in community
        user_map = {}
        for user_id in users:
            user_list = list(
                map(str, self.user_friend_getter.get_user_friends_ids(user_id)))
            for candidate in user_list:
                if candidate not in users:
                    if candidate in user_map:
                        user_map[candidate] += 1
                    else:
                        user_map[candidate] = 1
        log.info("Potential candidate list: " + str(len(user_map.keys())))
        # key: number of follower in community, value: list of users
        result = {}
        for k, v in user_map.items():
            if v not in result:
                result[v] = [k]
            else:
                result[v].append(k)
        # at least threshold% user in the community are candidate's follower
        threshold = len(users) * threshold
        log.info("want candidate have at least" + str(threshold) +
                 "followers in the community")
        candidate = []
        # whether or not there are more potential candidate than we asked for
        more_potential_candidate = True
        for i in range(len(users), -1, -1):
            if i in result:
                if len(result[i]) + len(candidate) <= num_of_candidate and \
                        i >= threshold:
                    log.info(str(len(result[i])) + " candidates has " + str(i) +
                             "common followers in current cluster")
                    candidate.extend(result[i])
                else:
                    if i < threshold:
                        log.info(
                            "break because common user reaches the minimum")
                        more_potential_candidate = False
                    break
        return candidate, more_potential_candidate

    def expand_community(self, threshold, top_size, candidates_size,
                         large_account_threshold, num_of_candidate, community):
        """Adding candidates until no more is added"""
        iteration = 0
        prev_community = []
        prev_community_size = 0
        more_potential_candidate = True
        # When no available candidate
        while prev_community_size != len(community) or more_potential_candidate:
            # if no candidate is added, but there is more candidate available
            if prev_community_size == len(community) and \
                    more_potential_candidate:
                num_of_candidate += 200

            prev_community_size = len(community)
            community = self.intersection_ranker.rank(community)
            self.dataset_creator.write_dataset(
                "expansion", iteration, community, prev_community)
            log.info("Iteration: " + str(iteration))
            log.info("Current community size: " + str(len(community)))
            self._download_friends(community)
            curr_candidate, more_potential_candidate = \
                self.find_potential_candidate(community,
                                              num_of_candidate,
                                              threshold)
            log.info("Download candidate and friends")
            curr_candidate = self._download_user_info_and_tweet(curr_candidate,
                                                                community)
            log.info(
                "Potential candidate list length: " + str(len(curr_candidate)))
            log.info("Potential candidate list: \n" + str(curr_candidate))
            curr_candidate = self.filter_candidates(
                threshold, top_size, candidates_size, large_account_threshold,
                community, curr_candidate)
            log.info("Final Candidate List Length(Fixed): " + str(
                len(curr_candidate)))
            log.info("Final Candidate : " + str(curr_candidate))
            new_community = list(
                set(map(str, community + list(curr_candidate))))
            prev_community = community
            community = new_community
            iteration = iteration + 1
