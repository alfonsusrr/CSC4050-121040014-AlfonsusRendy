from util.Chat import RemoteChatAgent
from util.InductFL import generate_prompt
import logging
import os
import json
from dotenv import load_dotenv
import random
import datetime 


CLUSTERS = 10
PROXY="OMG"
PATH="./chat_history/"

def get_cluster_data(cluster):
    with open("clustered_defects4j.json", "r") as file:
        dataset = json.load(file)

    result = []
    for data in dataset:
        if data["cluster"] == cluster:
            result.append(data)
    return result

def initialize_chat(file_path=None):
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    if file_path:
        try:
            with open(file_path, "w") as file:
                json.dump([], file)
        except:
            print("Error creating chat history file")
    
    logger = logging.getLogger()
    model_name="gpt-3.5-turbo"

    
    chat = RemoteChatAgent(API_KEY, model_name, file_path, logger)
    return chat

def analyze_cluster_data(cluster_data):
    print(f"Cluster: {cluster_data[0]['cluster']}")
    method_length = []
    
    for instance in cluster_data:
        method_length.append(len(instance["method"]))
    
    
    print(f"Total Data: {len(method_length)}")
    print(f"Average Line per Method: {sum(method_length)/len(method_length)}")
    print(f"Maximum Line number: {max(method_length)}")
    print("-----------------------------------")

def export_result(path, data):
    with open(path, "w") as file:
        json.dump(data, file)


def cluster_heuristic_gen(cluster, method="sampling", n_sampling=5, n_sample=3):
    cluster_data = get_cluster_data(cluster)
    if method == "sampling":
        for _ in range(n_sampling):
            sample_indices = random.sample(range(len(cluster_data)), n_sample)
            input_output_pairs = []
            selected_data = []
            for index in sample_indices:
                input_text = "".join([f"<{i + 1}>\t {line}" for i, line in enumerate(cluster_data[index]["method"])])
                output_text = ", ".join([str(i) for i in cluster_data[index]["faulty_lines"]])
                input_output_pairs.append({
                    "input": input_text,
                    "output": output_text
                })
                selected_data.append(cluster_data[index])
            

            file_name = create_chat_history_path(f"sampling_{cluster}")
            chat = initialize_chat()

            prompt = generate_prompt(input_output_pairs=input_output_pairs)
            response = chat.chat(prompt, f"sampling_{cluster}", PROXY)
            result = {
                "dataset": selected_data,
                "heuristic": response
            }
            export_result(file_name, result)
        
    elif method == "refine":
        chat = initialize_chat()
        random.shuffle(cluster_data)
        for i in range(0, len(cluster_data), n_sample):
            batch = cluster_data[i:i+n_sample]

def get_cluster_info():
    for cluster in range(CLUSTERS):
        cluster_data = get_cluster_data(cluster)
        analyze_cluster_data(cluster_data)

def main():
    cluster_heuristic_gen(cluster = 6, method="sampling", n_sampling=1)
        
if __name__ == "__main__":
    main()