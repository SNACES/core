import glob
import json
import argparse
import matplotlib.pyplot as plt
import numpy as np

def produce_plots(user_name):
    series = ['20', '40', '60', '80', '100']
    labels = []
    series_means = {}

    # fig = plt.figure()

    fig, axes = plt.subplots(2, 3)
    fig.suptitle('Overlap Between Community of david_madras and Local Neighbourhood of hardmaru')
    types = ['default', 'follower_only', 'tweet_only']
    titles = ['Data Cleaning By Tweets and Followers', 'Data Cleaning By Followers Only', 'Data Cleaning By Tweets Only']

    for i in range(len(types)):
        ax1, ax2 = axes[:, i]
        type = types[i]
        title = titles[i]

        series_counts = []
        for val in series:
            filename_list1 = glob.glob('./dc_exp/' + str(type) + '/clusters_' + str(val) + '/' + str(user_name) + '_clusters_*.json')
            filename_list2 = glob.glob('./dc_exp/' + str(type) + '/clusters_' + str(val) + '/' + str('hardmaru') + '_clusters_*.json')

            prev1 = None
            prev2 = None
            parity = True

            counts1 = []
            counts2 = []

            for i in range(len(filename_list1)):
                filename1 = filename_list1[i]
                filename2 = filename_list2[i]

                cluster1 = None
                cluster2 = None
                with open(filename1, 'r') as file:
                    user_lists = json.load(file)
                    count = len(user_lists)

                    if count == 2:

                        hardmaru = '2895499182'
                        fchollet = '68746721'

                        target = hardmaru
                        if target in user_lists[0]:
                            cluster1 = user_lists[0]
                            cluster2 = user_lists[1]
                        else:
                            cluster1 = user_lists[1]
                            cluster2 = user_lists[0]
                    else:
                        continue

                local_neighbourhood = []
                with open(filename2, 'r') as file:
                    user_lists = json.load(file)
                    for user_list in user_lists:
                        local_neighbourhood += user_list

                d1 = jaccard_similarity(cluster1, local_neighbourhood)
                d2 = jaccard_similarity(cluster2, local_neighbourhood)
                counts1.append(d1)
                counts2.append(d2)
            series_counts.append([counts1, counts2])

        num_series = len(series)

        data1 = []
        data2 = []

        for i in range(len(series)):
            count1, count2 = series_counts[i]
            data1.append(count1)
            data2.append(count2)

        ax1.boxplot(data1, labels=series)
        # print(data1)
        ax2.boxplot(data2, labels=series)

        x = np.arange(len(series))

        # Add some text for labels, title and custom x-axis tick labels, etc.
        for ax in [ax1, ax2]:
            ax.set_ylabel('Jaccard Similarity')
            ax.set_xlabel('Data Cleaning Parameter (percentage)')

        ax1.set_title("Machine Learning Cluster\n" +  title, fontsize=10)
        ax2.set_title("Basketball Cluster\n" +  title, fontsize=10)

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
