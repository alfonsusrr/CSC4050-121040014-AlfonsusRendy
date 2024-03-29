import random
import os
import json
import datetime 
import logging
from util.Chat import RemoteChatAgent
from dotenv import load_dotenv

PROXY="OMG"

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
    model_name="claude-3-opus-patch"

    chat = RemoteChatAgent(API_KEY, model_name, file_path, logger)
    return chat

def create_chat_history_path(path, file_path):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")
    return f"{path}{file_path}-{timestamp}.json"

def export_result(path, data):
    with open(path, "w") as file:
        json.dump(data, file)

def generate_prompt(input_output_pairs, previous_heuristics=None):
    starting_prompt = "Act as a professional code debugger. You are given a list of input and output of a debugger as follows:\n"
    data_prompt = "\n".join([f"Code: {data['input']} Defect Lines: {data['output']}" for data in input_output_pairs])
    
    if not previous_heuristics:
        ending_prompt = "\nYou extract the patterns from these bugs. The heuristics to get the defect lines is "
    else: 
        ending_prompt = f"\nYou have extract the patterns from these bugs, that is: {previous_heuristics}. Given the new code, the heuristics to get the defect lines is "

    prompt = starting_prompt + data_prompt + ending_prompt
    return prompt

def generate_prompt_explanation(input_output_pairs, previous_heuristics=None):
    starting_prompt = "Act as a professional code debugger. You are given a list of code with the explanation of its bugs:\n"
    data_prompt = "\n".join([f"Code: {data['input']} Bug Explanation: {data['output']}" for data in input_output_pairs])
    
    # heuristics_prompt = "You are also given example heuristics formulation for general fault localization as follows:"
    if not previous_heuristics:
        ending_prompt = "\nYou extract the patterns from these bugs. Generate one (only one) step-by-step automated fault localization heuristic to find the defective line of every bug of the same type correctly with mathematical formulation explained in one paragraph. Start the heuristic with <heuristic> and end it with </heuristic>"
    else: 
        ending_prompt = f"\nYou have extract the patterns from these bugs, that is: {previous_heuristics}. Given the new code, refine your hypothesis and generate one (only one) step-by-step heuristic to find the defective line of every bug of the same type correctly in one paragraph. Start the heuristic with <heuristic> and end it with </heuristic>"

    prompt = starting_prompt + data_prompt + ending_prompt
    return prompt

# data:
#   buggy_code
#   explanation
#

def cluster_heuristic_gen(data, cluster, method="sampling", n_sampling=5, n_sample=3, path="./chat_history/", verbose=False):
    if method == "sampling":
        for _ in range(n_sampling):
            if verbose:
                print(f"Generating heuristic sample {_}...")
            sample_indices = random.sample(range(len(data)), n_sample)
            input_output_pairs = []
            selected_data = []
            for index in sample_indices:
                input_text = data[index]["buggy_code"]
                output_text = data[index]["reasoning"]
                input_output_pairs.append({
                    "input": input_text,
                    "output": output_text
                })
                selected_data.append(data[index])
            

            file_name = create_chat_history_path(path, f"sampling_{cluster}")
            chat = initialize_chat()

            prompt = generate_prompt_explanation(input_output_pairs=input_output_pairs)
            response = chat.chat(prompt, f"sampling_{cluster}", PROXY)
            result = {
                "dataset": selected_data,
                "heuristic": response
            }
            export_result(file_name, result)
        
    elif method == "refine":
        chat = initialize_chat()
        random.shuffle(data)
        for i in range(0, len(data), n_sample):
            batch = data[i:i+n_sample]



# def isEven(a):
#     if a % 2 <= 0:
#         return True
#     else:
#         return False


# def getListElement(list, index):
#     if index > len(list):
#         return None
#     else:
#         return list[index]