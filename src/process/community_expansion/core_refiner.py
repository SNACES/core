from src.process.community_expansion.community_expansion import \
    CommunityExpansionAlgorithm
from src.process.ranking.intersection_ranker import IntersectionRanker
from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)


def _is_same_list(list1, list2):
    for user1 in list1:
        ret = False
        for user2 in list2:
            if user1 == user2:
                ret = True
        if not ret:
            return ret
    return True


class CoreRefiner(CommunityExpansionAlgorithm):
    """Used to refine initial community, which we assume are a list of core
    users.
    By refining core before expansion, we expect a better result in community
    expansion.
    Refinement stops when no core user changed
    """
    def refine_core(self, threshold, top_size, candidates_size,
                    large_account_threshold,
                    core_size, num_of_candidate, community):
        iteration = 0
        intersection_ranker = IntersectionRanker(self.ranker_list)
        prev_community = []
        while True:
            community = intersection_ranker.rank(community)
            # Only take top core_size users
            if len(community) > core_size:
                community = community[:core_size]
            self.dataset_creator.write_dataset(
                "core_refine",
                iteration, community, prev_community)
            if _is_same_list(community, prev_community):
                break
            log.info("Core Refine Iteration: " + str(iteration))
            log.info("Current Community: " + str(community))
            self._download_friends(community)
            curr_candidate, more_potential_candidate = \
                self.find_potential_candidate(community,
                                              num_of_candidate,
                                              threshold)
            log.info("Download candidate and friends")
            curr_candidate = \
                self._download_user_info_and_tweet(curr_candidate, community)
            log.info("Potential candidate list length: " + str(len(curr_candidate)))
            log.info("Potential candidate list: \n" + str(curr_candidate))
            curr_candidate = self.filter_candidates(threshold, top_size,
                                                    candidates_size,
                                                    large_account_threshold,
                                                    community, curr_candidate)
            log.info("Final Candidate List Length(Fixed): " + str(len(curr_candidate)))
            log.info("Final Candidate : " + str(curr_candidate))
            user_names = []
            for user in curr_candidate:
                user_names.append(self.user_getter.get_user_by_id(user).screen_name)
            log.info(user_names)
            new_community = list(set(map(str, community + list(curr_candidate))))
            prev_community = community
            community = new_community
            iteration = iteration + 1
        return community
