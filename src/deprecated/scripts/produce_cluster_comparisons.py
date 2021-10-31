import glob
import json
import argparse
import matplotlib.pyplot as plt
import numpy as np
import logging
from src.shared.logger_factory import LoggerFactory
from src.dependencies.injector import Injector
from src.shared.utils import get_project_root

log = LoggerFactory.logger(__name__)
DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/default_config.yaml"

def produce_plots(user_name, path = DEFAULT_PATH):
    #series = ['5', '10', '15']
    # series = ['0', '200', '400', '600', '800', '1000', '1200', '1400', '1600', '1800', '2000']
    labels = []
    series_means = {}
    injector = Injector.get_injector_from_file(path)
    # fig = plt.figure()

    fig, axes = plt.subplots(1, 3)
    fig.suptitle('Jaccard Similarity ' + str(user_name) + " with Global Threshold 50 and Local Threshold 10")

    titles = ['Cluster 1', 'Cluster 2', 'Cluster 3']
    type = 'local_and_global'
    prefix = "./dc2_exp/"

    d_repr = './dc2_exp/local_and_global/clusters_local_10.0_global_50/david_madras_clusters_0.json'
    d2_repr = './dc2_exp/default/clusters_80/david_madras_clusters_8.json'

    repr_lst = []
    with open(d_repr) as file:
        user_lists = json.load(file)
        #assert len(user_lists) == 3, "Nope!"

        repr1 = user_lists[0]
        repr2 = user_lists[1]
        repr3 = user_lists[2]

    title1 = titles[0]
    title2 = titles[1]
    title3 = titles[2]

    filename_list = glob.glob(prefix + str(type) + '/clusters_local_10.0_global_50' '/' + str(user_name) + '_clusters_*.json')
    counts1 = []
    counts2 = []
    counts3 = []

    iterations = []

    ax1 = axes[0]
    ax2 = axes[1]
    ax3 = axes[2]
    j = 0
    filename_start = prefix + str(type) + '/clusters_local_10.0_global_50' '/' + str(user_name) + '_clusters_'
    for k in range(20):
        filename = filename_start + str(k) + '.json'
        with open(filename, 'r') as file:
            user_lists = json.load(file)
            count = len(user_lists)
            sims1 = []
            sims2 = []
            sims3 = []
            for i in range(count):
                sims1.append(jaccard_similarity(user_lists[i], repr1))
                sims2.append(jaccard_similarity(user_lists[i], repr2))
                sims3.append(jaccard_similarity(user_lists[i], repr3))
            index1 = sims1.index(max(sims1))
            index2 = sims2.index(max(sims2))
            index3 = sims3.index(max(sims3))
            if index1 == index2 or index2 == index3 or index3 == index1:
            #if index1 == index2 or count == 3:
                log.info('does not work for ' + filename + ', ' + str(j))
            else:
                cluster1 = user_lists[index1]
                cluster2 = user_lists[index2]
                cluster3 = user_lists[index3]

                d1 = jaccard_similarity(repr1, cluster1)
                d2 = jaccard_similarity(repr2, cluster2)
                d3 = jaccard_similarity(repr3, cluster3)

                counts1.append(d1)
                counts2.append(d2)
                counts3.append(d3)
                iterations.append(j)
        j += 1

    ax1.bar(iterations, counts1)
    ax2.bar(iterations, counts2)
    ax3.bar(iterations, counts3)

    # Add some text for labels, title and custom x-axis tick labels, etc.

    for ax in [ax1, ax2, ax3]:
    #for ax in [ax2, ax2]:
        ax.set_ylabel('Jaccard Similarity')
        ax.set_xlabel('Iteration Number')

    ax1.set_title(title1, fontsize=10)
    ax2.set_title(title2, fontsize=10)
    ax3.set_title(title3, fontsize=10)

    plt.show()

def jaccard_similarity(user_list1, user_list2):
    intersection = len(list(set(user_list1).intersection(user_list2)))
    union = (len(user_list1) + len(user_list2)) - intersection

    return float(intersection) / union

def overlap(user_list1, user_list2):
    intersection = len(list(set(user_list1).intersection(user_list2)))

    return float(intersection) / len(user_list1)

if __name__ == "__main__":
    """
    Short script to produce scatter plots
    """
    parser = argparse.ArgumentParser(description='Short script to produce scatter plots of utility')
    parser.add_argument('-n', '--screen_name', dest='name',
                        help="The screen name of the user to download", required=True)

    args = parser.parse_args()

    produce_plots(args.name)
