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

    fig, axes = plt.subplots(1, 3)
    fig.suptitle('Number of Clusters by Data Cleaning Threshold for User: ' + str(user_name))
    types = ['default', 'follower_only', 'tweet_only']
    titles = ['Data Cleaning By Tweets and Followers', 'Data Cleaning By Followers Only', 'Data Cleaning By Tweets Only']

    for i in range(len(types)):
        ax = axes[i]
        type = types[i]
        title = titles[i]

        for val in series:
            filename_list = glob.glob('./dc2_exp/' + str(type) + '/clusters_' + str(val) + '/' + str(user_name) + '_clusters_*.json')
            counts = {}
            for filename in filename_list:
                # print("Parsing " + str(file))
                with open(filename, 'r') as file:
                    user_lists = json.load(file)
                    count = len(user_lists)
                    if count in counts:
                        counts[count] += 1
                    else:
                        counts[count] = 1

            series_means[val] = counts

        labels = []
        for val in series:
            mean = series_means[val]
            for key in mean:
                if key not in labels:
                    labels.append(key)

        labels.sort()
        print(str(labels))

        x = np.arange(len(labels))  # the label locations
        width = 0.9  # the width of the bars

        rects = []

        num_series = len(series)
        offsets = [-2*width/5, -width/5, 0, width/5, 2*width/5]
        for i in range(len(series)):
            val = series[i]
            offset = offsets[i]

            means = []
            for label in labels:
                series_mean = series_means[val]
                if label in series_mean:
                    means.append(series_mean[label]/200.)
                else:
                    means.append(0)

            rect = ax.bar(x + offset, means, width/5, label=val)
            rects.append(rect)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Fraction of Clusters')
        ax.set_xlabel('Number of Clusters')
        ax.set_title(title, fontsize=10)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

    plt.show()

if __name__ == "__main__":
    """
    Short script to produce scatter plots
    """
    parser = argparse.ArgumentParser(description='Short script to produce scatter plots of utility')
    parser.add_argument('-n', '--screen_name', dest='name',
        help="The screen name of the user to download", required=True)

    args = parser.parse_args()

    produce_plots(args.name)
