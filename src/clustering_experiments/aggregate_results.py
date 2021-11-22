from compare_clustering_algorithms import get_clusters, threshold_clusters
from ranking_users_in_clusters import rank_users


def write_cluster_sizes(initial_user: str, clusters, refined_clusters):
    """Write number of clusters to text files given clusters and refined_clusters of a particular experiment run."""
    with open(f"./src/clustering_experiments/data/{initial_user}_number_of_clusters.txt", "a") as f:
        f.write(str(len(clusters)) + "\n")
    with open(f"./src/clustering_experiments/data/{initial_user}_number_of_refined_clusters.txt", "a") as f:
        non_discarded_refined_clusters = threshold_clusters(refined_clusters)
        f.write(str(len(non_discarded_refined_clusters)) + "\n")


def write_cluster_ranking(initial_user: str, clusters, refined_clusters):
    """Write number of clusters to text files given clusters and refined clusters of a particular experiment run."""
    refined_clusters = threshold_clusters(refined_clusters)  # Discard the very small clusters
    with open(f"./src/clustering_experiments/data/{initial_user}_rankings/clustering_production_ranking.txt", "a") as p:
        with open(f"./src/clustering_experiments/data/{initial_user}_rankings/clustering_consumption_ranking.txt", "a") as c:        
            ranking_users_all_clusters = [rank_users(initial_user, cluster) for cluster in clusters]
            p.write("-"*15 + "\n")
            c.write("-"*15 + "\n")
            for i, ranking_of_one_cluster in enumerate(ranking_users_all_clusters):
                p.write(f"*Cluster {i}*\n")
                c.write(f"*Cluster {i}*\n")
                for prod_user in ranking_of_one_cluster[0]:
                    p.write(prod_user + "\n")
                for con_user in ranking_of_one_cluster[1]:
                    c.write(con_user + "\n")

    with open(f"./src/clustering_experiments/data/{initial_user}_rankings/refined_clustering_production_ranking.txt", "a") as p:
        with open(f"./src/clustering_experiments/data/{initial_user}_rankings/refined_clustering_consumption_ranking.txt", "a") as c:        
            ranking_users_all_clusters = [rank_users(initial_user, refined_cluster) for refined_cluster in refined_clusters]
            p.write("-"*15 + "\n")
            c.write("-"*15 + "\n")
            for i, ranking_of_one_cluster in enumerate(ranking_users_all_clusters):
                p.write(f"*Refined Cluster {i}*\n")
                c.write(f"*Refined Cluster {i}*\n")
                for prod_user in ranking_of_one_cluster[0]:
                    p.write(prod_user + "\n")
                for con_user in ranking_of_one_cluster[1]:
                    c.write(con_user + "\n")


if __name__ == "__main__":
    # clusters, refined_clusters = get_clusters("david_madras")
    # write_cluster_sizes("david_madras", clusters, refined_clusters)
    # write_cluster_ranking("david_madras", clusters, refined_clusters)

    # clusters, refined_clusters = get_clusters("hardmaru")
    # write_cluster_sizes("hardmaru", clusters, refined_clusters)
    # write_cluster_ranking("hardmaru", clusters, refined_clusters)

    # clusters, refined_clusters = get_clusters("tw_killian")
    # write_cluster_sizes("tw_killian", clusters, refined_clusters)
    # write_cluster_ranking("tw_killian", clusters, refined_clusters)

    # clusters, refined_clusters = get_clusters("timnitGebru")
    # write_cluster_sizes("timnitGebru", clusters, refined_clusters)
    # write_cluster_ranking("timnitGebru", clusters, refined_clusters)

    pass