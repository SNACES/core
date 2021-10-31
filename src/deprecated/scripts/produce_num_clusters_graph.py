import glob
import json
import argparse
import matplotlib.pyplot as plt
import numpy as np

def produce_plots(user_name):
    filename_list = glob.glob('./clusters_80/' + str(user_name) + '_clusters_*.json')
    counts = []
    for filename in filename_list:
        # print("Parsing " + str(file))
        with open(filename, 'r') as file:
            user_lists = json.load(file)
            count = len(user_lists)
            counts.append(count)

    counts_dict = {}
    for count in counts:
        if count in counts_dict:
            counts_dict[count] += 1
        else:
            counts_dict[count] = 1

    d = np.diff(np.unique(counts)).min()
    left_of_first_bin = min(counts) - float(d)/2
    right_of_last_bin = max(counts) + float(d)/2

    plt.hist(counts, bins=np.arange(left_of_first_bin, right_of_last_bin + d, d), density=True, facecolor='blue', alpha=0.5, rwidth=0.85)
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
