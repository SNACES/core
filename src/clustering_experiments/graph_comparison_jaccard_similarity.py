from collections import defaultdict
from typing import List, Dict
from src.model.cluster import Cluster
from src.shared.utils import get_project_root
from src.clustering_experiments.compare_clustering_algorithms import compare_clusters, compare_clusters_jaccard, get_clusters
from src.clustering_experiments.clustering_data import connect_to_db, get_all_data, format_all_data
from src.clustering_experiments.compare_clustering_same_size import categorize_clusters_by_length
import matplotlib.pyplot as plt

TOTAL_NUM = 430;

def experiment_results(initial_user: str):
    """Writes the clustering comparison experiment results for the screen_name."""
    with open(f"{str(get_project_root())}/src/clustering_experiments/data/{initial_user}_clustering_comparison_aggregated", "a") as f:
        clusters, refined_clusters = get_clusters(initial_user)
        subset_similarity_clusters, subset_similarity_refined_clusters = compare_clusters(clusters, refined_clusters)
        f.write("-" * 20 + "\n")
        print(subset_similarity_clusters)

        print(subset_similarity_refined_clusters)
        for refined_cluster in subset_similarity_refined_clusters:
            f.write(f"Refined Cluster {refined_cluster[0]} of size {refined_cluster[1]}: \n")
            for cluster in subset_similarity_refined_clusters[refined_cluster]:
                f.write(f"\t is contained in Cluster {cluster[0]} of size {cluster[2]} about {round(cluster[1] * 100, 2)}%. \n")

def select_unrefined_baseline(unrefined_list)->List[Cluster]:
    """for now select a random cluster of size 2 to compare each refined cluster to"""
    return unrefined_list[5]

def aggregate_data(all_refined_clusters, all_unrefined_clusters):
    baseline = select_unrefined_baseline(all_unrefined_clusters)
    # for refined_clusters in all_refined_clusters:
    #     refined_threshold_clusters = threshold_clusters(refined_clusters)
    #     if len(refined_threshold_clusters) == 2:
    #         double_refined_clusters.append(refined_threshold_clusters)
    #     elif len(refined_threshold_clusters) == 3:
    #         triple_refined_clusters.append(refined_threshold_clusters)
    #
    # double_unrefined_clusters = []
    # triple_unrefined_clusters = []
    # for unrefined_clusters in all_unrefined_clusters:
    #     if len(unrefined_clusters) == 2:
    #         double_unrefined_clusters.append(unrefined_clusters)
    #     if len(unrefined_clusters) == 3:
    #         triple_unrefined_clusters.append(unrefined_clusters)
    single_unrefined_clusters, double_unrefined_clusters, triple_unrefined_clusters =\
        categorize_clusters_by_length(all_unrefined_clusters)

    single_refined_clusters, double_refined_clusters, triple_refined_clusters =\
        categorize_clusters_by_length(all_refined_clusters)



def graph_triple_count(clusters, fig_name):
    labels = []
    c1 = []
    c2 = []
    c3 = []
    c4 = []
    for i in range(min(10, len(clusters))):
        labels.append(i)
        clusters[i].sort(key=lambda x: abs(len(x.users)))
        c1.append(len(clusters[i][0].users)/TOTAL_NUM)
        c2.append(len(clusters[i][1].users)/TOTAL_NUM)
        c3.append(len(clusters[i][2].users)/TOTAL_NUM)
        c4.append((len(clusters[i][0].users) + len(clusters[i][1].users))/TOTAL_NUM)

    width = 0.25
    fig, ax = plt.subplots()

    ax.bar(labels, c1, width, label='Cluster0')
    print(c2)
    print(c1)
    ax.bar(labels, c2, width, bottom=c1, label='Cluster1')
    ax.bar(labels, c3, width, bottom=c4, label='Cluster2')


    ax.set_title('Division of Users into Clusters Across Experiments')
    ax.set_ylabel('Ratio of Size of Clusters')
    ax.set_xlabel('Experiment Runs')
    ax.legend()

    plt.savefig(fig_name)
    plt.show()

def graph_double_count(clusters, fig_name):
    labels = []
    c1 = []
    c2 = []
    for i in range(min(10, len(clusters))):
        labels.append(i)
        clusters[i].sort(key=lambda x: len(x.users))
        c1.append(len(clusters[i][0].users)/TOTAL_NUM)
        c2.append(len(clusters[i][1].users)/TOTAL_NUM)


    width = 0.25
    fig, ax = plt.subplots()

    ax.bar(labels, c1, width, label='Cluster 0')
    ax.bar(labels, c2, width, bottom=c1,
           label='Cluster 1')

    ax.set_title('Division of Users into Clusters Across Experiments')
    ax.set_ylabel('Ratio of Size of Clusters')
    ax.set_xlabel('Experiment Runs')
    ax.legend()

    plt.savefig(fig_name)
    plt.show()

def graph_similarity(baseline, clusters, num2=3, fig_name="lol", type="subset", plot="scatter"):
    num1 = len(baseline)
    if type == 'subset':
        compare_f = compare_clusters
    else:
        compare_f = compare_clusters_jaccard

    test_result, throwaway = compare_f(baseline, clusters[0])
    keys = list(test_result.keys())
    print(keys)
    fig, axs = plt.subplots(1, num1)

    for i in range(num1):
        x_val = []
        c1_sim = []
        c2_sim = []
        c3_sim = []
        sim_graph = [c1_sim, c2_sim, c3_sim]
        for j in range(min(10, len(clusters))):
            x_val.append(j)
            sim1, sim2 = compare_f(baseline, clusters[j], key=0)
            k = 0
            for sim in sim1[keys[num1 - i - 1]]: #num1 - i - 1 for reverse
                if len(sim1[keys[num1 - i - 1]]) == 3:
                    tmp = 2-k
                else:
                    tmp = 1-k
                sim_graph[tmp].append(sim[1])
                k += 1
        color = [0, 1, 2]
        if plot == "scatter":
            for j in range(num2):
            # colors = [color[j]] * min(10, len(clusters))
            # print(colors)
                axs[i].scatter(x_val, sim_graph[j], label=f'Refined Cluster {j}')

        if plot == "box":
            box_plots = []
            labels = range(len(sim_graph))
            for j in range(num2):
                bplot = axs[i].boxplot(sim_graph[:num2],
                        vert=True,  # vertical box alignment
                        patch_artist=True,  # fill with color
                        labels=labels[:num2])  # will be used to label x-ticks
                box_plots.append(bplot)

            colors = ["dodgerblue", "orange",  "lime"]
            for bplot in box_plots:
                for patch, color in zip(bplot['boxes'], colors):
                    patch.set_facecolor(color)

    k = 0
    r = range(num1)
    for ax in axs:
        ax.yaxis.grid(True)
        if plot == "scatter":
            ax.set_xlabel("Experiment Runs")
        elif plot == 'box':
            ax.set_xlabel(f"Refined cluster #")
        ax.set_title(f"vs Refined Cluster {r[k]}")
        ax.set_ylabel(f'{type} similarity')
        k += 1

    if plot == "scatter":
        handles, labels = axs[num1-1].get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper center', ncol=num2)

    fig.tight_layout(pad=3.0)
    plt.savefig(fig_name)
    plt.show()





if __name__ == "__main__":
    #experiment_results("david_madras")
    conn, db = connect_to_db()
    print("here")
    all_refined = get_all_data(refined = True)
    all_unrefined = get_all_data(refined = False)

    all_refined_clusters = format_all_data(all_refined)
    all_unrefined_clusters = format_all_data(all_unrefined)
    # This formats each cluster in data['clusters'] from dict to Cluster object
    # all_clusters is List[List[Cluster]]
    # each nested List[Cluster] gives the results of one clustering experiment

    single_unrefined_clusters, double_unrefined_clusters, triple_unrefined_clusters = \
        categorize_clusters_by_length(all_unrefined_clusters)

    single_refined_clusters, double_refined_clusters, triple_refined_clusters = \
        categorize_clusters_by_length(all_refined_clusters)

    refined_clusters_categorized = [single_refined_clusters, double_refined_clusters, triple_refined_clusters]
    unrefined_clusters_categorized = [single_unrefined_clusters, double_unrefined_clusters, triple_unrefined_clusters]

    print([len(c) for c in unrefined_clusters_categorized])
    print([len(c) for c in refined_clusters_categorized])

    # print(triple_refined_clusters)
    #graph_triple_count(triple_refined_clusters, "triple_refined_clusters")
    #graph_triple_count(triple_unrefined_clusters, "triple_unrefined_clusters")


    #graph_double_count(double_refined_clusters, "double_refined_clusters")
    #graph_double_count(double_unrefined_clusters, "double_unrefined_clusters")

    graph_similarity(double_refined_clusters[0], triple_refined_clusters, type="subset", plot="box", fig_name="2_unref_vs_3_ref_box_subset")
    graph_similarity(double_refined_clusters[0], double_refined_clusters, num2=2, type="subset", plot="box", fig_name="2_unref_vs_2_ref_box_subset")

    graph_similarity(double_refined_clusters[0], triple_refined_clusters, type="subset", fig_name="2_unref_vs_3_ref_scat_subset")
    graph_similarity(double_refined_clusters[0], double_refined_clusters, num2=2, type="subset", fig_name="2_unref_vs_2_ref_scat_subset")
