import math
import matplotlib.pyplot as plt
from typing import List
from tqdm import tqdm

def generate_boxplot(data, graph_type, count):
    #scores_001 = []
    # #scores_001_ceil = []
    # for id in tqdm(user_ids.users):
    #     user = user_getter.get_user_by_id(id)
    #     #scores_001_ceil.append(math.log(user.get_likes()))
    #     likes = user.get_likes()
    #     if likes != 0:
    #         likes = math.log(user.get_likes())
    #     scores_001.append(likes)


    # fig, (ax1,ax2) = plt.subplots(1,2)
    # ax1.set_title("Like*0.001")
    # ax1.boxplot(scores_001)
    # ax2.set_title("Ceiling of Like*0.001")
    # ax2.boxplot(scores_001_ceil)
    plt.title("top 50 "+graph_type)
    plt.boxplot(data)
    filename = '/Users/rachel/Desktop/ROP/core/plots/top_50_'+graph_type+'_boxplot_'+str(count)+'.png'
    plt.savefig(filename)
    plt.clf()

def generate_hist(data, graph_type, count):
    plt.title("top 50 "+graph_type)
    plt.hist(data)
    filename = '/Users/rachel/Desktop/ROP/core/plots/top_50_'+graph_type+'_hist_'+str(count)+'.png'
    plt.savefig(filename)
    plt.clf()


def generate_scatterplot(x_name, y_name, x_score, y_score, count):
    # scatter plot with matplotlib in Python
    plt.scatter(x_score, y_score)
    # set x-axis label and specific size
    plt.xlabel(x_name,size=16)
    # set y-axis label and specific size
    plt.ylabel(y_name,size=16)
    # set plot title with specific size
    plt.title(x_name+ ' vs. ' + y_name,size=16)
    # save the plot as PNG file with dpi=150
    filename = '/Users/rachel/Desktop/ROP/core/plots/top_50_'+x_name+"_"+y_name +'_plot_'+str(count)+'.png'
    plt.savefig(filename)
    plt.clf()
