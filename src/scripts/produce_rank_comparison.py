import glob
import json
import argparse
import matplotlib.pyplot as plt
import numpy as np

def produce_plots(user_name):
    with open('david_madras_1_scores.json', 'r') as file:
        scores = json.load(file)

    production = scores["production"]
    consumption = scores["consumption"]
    follower = scores["follower"]

    prod_ranking = list(sorted(production, key=production.get, reverse=True))
    cons_ranking = list(sorted(consumption, key=consumption.get, reverse=True))
    foll_ranking = list(sorted(follower, key=follower.get, reverse=True))

    fig, axes = plt.subplots(2, 3)

    fig.suptitle('Utility Ranking Comparison for the Machine Learning Cluster of david_madras')

    prod_v_cons = compare(prod_ranking, cons_ranking, axes[0,0], "Production", "Consumption")
    prod_v_foll = compare(prod_ranking, foll_ranking, axes[1,0], "Production", "Follower")

    cons_v_prod = compare(cons_ranking, prod_ranking, axes[0,1], "Consumption", "Production")
    cons_v_foll = compare(cons_ranking, foll_ranking, axes[1,1], "Consumption", "Follower")

    foll_v_prod = compare(foll_ranking, prod_ranking, axes[0,2], "Follower", "Production")
    foll_v_cons = compare(foll_ranking, cons_ranking, axes[1,2], "Follower", "Consumption")

    plt.show()

def compare(s1, s2, ax, type1, type2):
    s1_v_s2 = []
    for i in range(len(s1)):
        j = s2.index(s1[i])
        s1_v_s2.append(j)
    ax.set_title(type1 + " Ranking vs " + type2 + " Ranking")
    ax.set_ylabel(type2 + " Ranking")
    ax.set_xlabel(type1 + " Ranking")
    ax.bar(list(range(len(s1_v_s2))), s1_v_s2)

if __name__ == "__main__":
    """
    Short script to produce scatter plots
    """
    parser = argparse.ArgumentParser(description='Short script to produce scatter plots of utility')
    parser.add_argument('-n', '--screen_name', dest='name',
        help="The screen name of the user to download", required=True)

    args = parser.parse_args()

    produce_plots(args.name)
