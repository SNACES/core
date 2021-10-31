import math
import matplotlib.pyplot as plt
from typing import List
from tqdm import tqdm

def generate_boxplot(user_ids, user_getter, count):
    scores_001 = []
    #scores_001_ceil = []
    for id in tqdm(user_ids.users):
        user = user_getter.get_user_by_id(id)
        #scores_001_ceil.append(math.log(user.get_likes()))
        likes = user.get_likes()
        if likes != 0:
            likes = math.log(user.get_likes())
        scores_001.append(likes)

    # fig, (ax1,ax2) = plt.subplots(1,2)
    # ax1.set_title("Like*0.001")
    # ax1.boxplot(scores_001)
    # ax2.set_title("Ceiling of Like*0.001")
    # ax2.boxplot(scores_001_ceil)
    plt.title("log(like) (like = 0 remains 0)")
    plt.boxplot(scores_001)
    filename = '/Users/rachel/Desktop/ROP/core/plots/like_log_boxplot_'+str(count)+'.png'
    plt.savefig(filename)
# fig, (ax1,ax2) = plt.subplots(1,2)
# ax1.boxplot([1,2,3])
# ax2.boxplot([3,4,5])
# plt.show()
