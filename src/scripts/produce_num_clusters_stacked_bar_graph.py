import glob
import json
import argparse
import matplotlib.pyplot as plt
import numpy as np

def produce_plots(user_name):
    series = ['100', '80', '60', '40', '20']
    # series = ['0', '200', '400', '600', '800', '1000', '1200', '1400', '1600', '1800', '2000']

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

        x = np.arange(len(series))  # the label locations
        width = 0.9  # the width of the bars

        rects = []

        num_series = len(series)
        # offsets = [-2*width/5, -width/5, 0, width/5, 2*width/5]
        # colors = [
        #     (43, 226, 237, 255),
        #     (20, 57, 226, 255),
        #     (89, 8, 117, 255),
        #     (77, 18, 37, 255),
        #     (56, 6, 6, 255)
        # ]
        # colors = [[i/255. for i in color] for color in colors]

        bottom = np.zeros(len(series))
        for i in range(len(labels)):
            # color = colors[i]
            label = labels[i]
            means = []

            for j in range(len(series)):
                val = series[j]

                series_mean = series_means[val]
                mean = 0
                if label in series_mean:
                    mean = series_mean[label]/200.

                means.append(mean)

            print(str(len(x)) + " " + str(len(means)) + " " + str(len(bottom)), flush=True)
            rect = ax.bar(x, means, width, bottom=bottom, label=label)
            rects.append(rect)
            bottom += means
            print(str(means))
            print(str(bottom))

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Fraction of Clusters')
        ax.set_xlabel('Data Cleaning Percentage')
        ax.set_title(title, fontsize=10)
        ax.set_xticks(x)
        ax.set_ylim([0, 1])
        ax.set_xticklabels(series)
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
