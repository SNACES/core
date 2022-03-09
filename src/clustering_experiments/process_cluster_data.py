import src.clustering_experiments.clustering_data_threshold as dt
import src.clustering_experiments.create_social_graph_and_cluster as csgc
import src.clustering_experiments.ranking_users_in_clusters as rk
import src.clustering_experiments.graph_ranking as gr
import src.clustering_experiments.graph_threshold as gt

if __name__ == "__main__":
    conn, db = dt.connect_to_db()

    # # generate cluster data and store in mongodb
    # dt.generate_threshold_cluster_data(conn, "jps_astro", 0.3)
    # dt.generate_threshold_cluster_data(conn, "jps_astro", 0.4)
    # dt.generate_threshold_cluster_data(conn, "RoyalAstroSoc", 0.3)
    # dt.generate_threshold_cluster_data(conn, "NASA", 0.3)

    # all clusters
    # gt.graph_size_of_clusters(conn, "jps_astro", 0.3, one=True)
    # gt.graph_size_of_clusters(conn, "jps_astro", 0.4, one=True)
    # gt.graph_size_of_clusters(conn, "RoyalAstroSoc", 0.3, one=True)
    # gt.graph_size_of_clusters(conn, "NASA", 0.3, one=True)


    # get top 10
    gr.compare_top_users_mongo_single(conn, "jps_astro", 0.4, 60)
    # gr.compare_top_users_mongo_single(conn, "RoyalAstroSoc", 0.3, 500)
    # gr.compare_top_users_mongo_single(conn, "NASA", 0.3, 100)




