from util.InductFL import *
import json

def load_data():
    with open("dbench.json", "r") as file:
        data = json.load(file)
    return data

def get_clusters(data):
    clusters = []
    for d in data:
        if d["bug_type"] not in clusters:
            clusters.append(d["bug_type"])
    return clusters

def get_clustered_data(data, cluster):
    clustered_data = []
    for d in data:
        if d["bug_type"] == cluster:
            clustered_data.append(d)
    return clustered_data

def generate_heuristics(data, clusters, n_heuristics=1, n_sample=20, path="./chat_history/dbench"):
    for cluster in clusters:
        selected_data = get_clustered_data(data, cluster)
        cluster_heuristic_gen(selected_data, cluster, n_sampling=n_heuristics, n_sample=n_sample, verbose=True, path=path)
        print(f"Cluster {cluster}'s heuristic is extracted")
    return

def main():
    data = load_data()
    clusters = get_clusters(data)
    generate_heuristics(data, [clusters[0]], path="./chat_history/dbench-claude-3-opus/")

if __name__ == "__main__":
    main()