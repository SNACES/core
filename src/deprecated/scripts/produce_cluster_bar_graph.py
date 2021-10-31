import glob
import json
import argparse
import matplotlib.pyplot as plt
import numpy as np

def produce_plots(user_name):
    series = ['10.0', '15.0']
    # series = ['0', '200', '400', '600', '800', '1000', '1200', '1400', '1600', '1800', '2000']

    labels = []
    series_means = {}

    # fig = plt.figure()

    fig, axes = plt.subplots()
    fig.suptitle('Number of Clusters on Largest Cluster by Data Cleaning with Local Cleaning for User: ' + str(user_name))
    types = ['Ratio', 'ratio_and_profile']
    titles = ['Data Cleaning with Follower to Following Ratio',
              'Data Cleaning with Follower to Following Ratio and Default Profile Picture Check']

    ax = axes
    type = 'local_and_global_of_cluster'
    title = 'Data Cleaning with Global Threshold 50 and Local Thresholds Set to Different Values'

    count10 = 0
    count15 = 0
    for val in series:
        filename_list = glob.glob('./dc2_exp/' + str(type) + '/clusters_local_' + str(val) + '_global_50' '/' + str(user_name) + '_clusters_*.json')
        counts = {}
        for filename in filename_list:
            with open(filename, 'r') as file:
                user_lists = json.load(file)
                count = len(user_lists)
                total = 0
                for i in range(count):
                    total += len(user_lists[i])
                if total <= 447: # To make sure we only count those who had 3/2 clusters
                    if count in counts:
                        counts[count] += 1
                    else:
                        counts[count] = 1
                    if val == '10.0':
                        count10 += 1
                    if val == '15.0':
                        count15 += 1

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
                if val == '10.0':
                    mean = series_mean[label]/count10
                if val == '15.0':
                    mean = series_mean[label]/count15
            means.append(mean)

        print(str(len(x)) + " " + str(len(means)) + " " + str(len(bottom)), flush=True)
        rect = ax.bar(x, means, width, bottom=bottom, label=label)
        rects.append(rect)
        bottom += means
        print(str(means))
        print(str(bottom))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Fraction of Clusters')
    ax.set_xlabel('Local Threshold')
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
