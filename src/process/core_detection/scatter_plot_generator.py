import math
import matplotlib.pyplot as plt
from typing import List
from tqdm import tqdm

def generate_plot(x_name, y_name, x_rank, x_score, y_rank, y_score, user_id, count,user_getter):
    # scatter plot with matplotlib in Python
    x_score_lst = []
    y_score_lst = []
    z_score_lst = []
    id_x = 0
    id_y = 0
    id_z = 0
    for i in range(0, len(x_score)):
        id = x_rank.ids[i]
        score_x = x_score.get(id)
        score_y = y_score.get(id)
        user = user_getter.get_user_by_id(id)
        likes = user.get_likes()
        x_score_lst.append(score_x)
        y_score_lst.append(score_y)
        z_score_lst.append(likes)
        if user_id == id:
            id_x = score_x
            id_y = score_y
            id_z = likes

    plt.scatter(x_score_lst, y_score_lst,
                alpha=0.5)
    plt.scatter(id_x, id_y, color="red")
    # set x-axis label and specific size
    plt.xlabel(x_name,size=16)
    # set y-axis label and specific size
    plt.ylabel(y_name,size=16)
    # set plot title with specific size
    plt.title(x_name+ ' vs. ' + y_name,size=16)
    # save the plot as PNG file with dpi=150
    filename = '/Users/rachel/Desktop/ROP/core/plots/'+x_name+"_"+y_name +'_plot_'+str(count)+'.png'
    plt.savefig(filename)
    plt.clf()

    plt.scatter(x_score_lst, z_score_lst,
                alpha=0.5)
    plt.scatter(id_x, id_y, color="red")
    # set x-axis label and specific size
    plt.xlabel(x_name,size=16)
    # set y-axis label and specific size
    plt.ylabel("Global Like",size=16)
    # set plot title with specific size
    plt.title(x_name+ ' vs. Global Like',size=16)
    # save the plot as PNG file with dpi=150
    filename = '/Users/rachel/Desktop/ROP/core/plots/'+x_name+'_global_like_plot_'+str(count)+'.png'
    plt.savefig(filename)
    plt.clf()

def generate_plot_2(x_name, y_name, x_rank, x_score, y_rank, y_score, user_id, count,user_getter):
    # scatter plot with matplotlib in Python
    x_score_lst = []
    y_score_lst = []
    z_score_lst = []
    follower_lst =[]
    for i in range(0, len(x_score)):
        id = x_rank.ids[i]
        score_x = x_score.get(id)
        if score_x != 0:
            score_x = math.log(score_x)
        score_y = y_score.get(id)
        if score_y != 0:
            score_y = math.log(score_y)
        user = user_getter.get_user_by_id(id)
        likes = user.get_likes()
        follower = user.get_followers()
        if likes != 0:
            likes = math.log(user.get_likes())
        if follower != 0:
            follower = math.log(user.get_followers())
        x_score_lst.append(score_x)
        y_score_lst.append(score_y)
        z_score_lst.append(likes)
        follower_lst.append(follower)

    plt.scatter(x_score_lst, y_score_lst,
                alpha=0.5)
    # set x-axis label and specific size
    plt.xlabel("Log"+x_name,size=16)
    # set y-axis label and specific size
    plt.ylabel("Log"+y_name,size=16)
    # set plot title with specific size
    plt.title(x_name+ ' vs. ' + y_name,size=16)
    # save the plot as PNG file with dpi=150
    filename = '/Users/rachel/Desktop/ROP/core/plots/'+"correlation_"+x_name+"_"+y_name +'_plot_'+str(count)+'.png'
    plt.savefig(filename)
    plt.clf()

    plt.scatter(follower_lst, z_score_lst,
                alpha=0.5)
    # set x-axis label and specific size
    plt.xlabel("Log Follower",size=16)
    # set y-axis label and specific size
    plt.ylabel("Log"+"Global Like",size=16)
    # set plot title with specific size
    plt.title(x_name+ ' vs. Global Like',size=16)
    # save the plot as PNG file with dpi=150
    filename = '/Users/rachel/Desktop/ROP/core/plots/'+"correlation_"+x_name+'_global_like_plot_'+str(count)+'.png'
    plt.savefig(filename)
    plt.clf()

#generate_plot(1, 2, 3)
