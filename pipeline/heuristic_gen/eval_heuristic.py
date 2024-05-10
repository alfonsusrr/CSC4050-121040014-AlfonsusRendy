import json
from util.Chat import RemoteChatAgent
from dotenv import load_dotenv
import logging
import os

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
    model_name="gpt-4"

    chat = RemoteChatAgent(API_KEY, model_name, file_path, logger)
    return chat

def generate_prompt(hclass, heuristic):
    if hclass == "other error":
        hclass = "logic error"

    inst = "Act as a heuristic evaluator. You are given the following heuristic for debugging some codes\n\n"
    command = f"Give three ratings from 1 to 10 for whether (1) the heuristic is relevant for {hclass} (2) the heuristic is correct, that is can result in lines with condition error (3) the heuristic is precise so that it can be implemented as a program that automatically execute the heuristic. "
    criteria = f"The evaluation criteria is: \
                - Relevancy: 5 for some relevancy, touch some specific case, 7 for relevant and touch 75% of the error type, 10 for perfect relevancy\
                - Correctness: 1 for solving 10% of the cases, 2 for 20% and so on\
                - Precision: 0 for ambiguous heuristics, 3 for no real steps, 5 for clear steps barely implementable, 7 for implementable but hard and need modification, 10 for directly implementable\
                "
    format_output = 'NO MORE THAN ONE SENTENCE FOR REASONS! Give the evaluation in the format of: \
                        score: {<score for relevancy>, <score for correctness>, <score for precision>}\
                        reason: {"<reason for relevancy>", "<reason for correctness>", "<reason for precision>"}\
                    '
    return inst + heuristic + command + criteria + format_output

def evaluate_heuristic(fname):
    heuristics = []
    with open(fname, "r") as file:
        heuristics = json.load(file)

    i = 0
    evaluation = []
    try: 
        for heuristic in heuristics:
            chat = initialize_chat()
            prompt = generate_prompt(heuristic["type"], heuristic["heuristic"])
            response = chat.chat(prompt, f"heuristic-{i + 1}", PROXY)
            # response = "a"
            evaluation.append(response)
            i += 1
            print(f"Evaluated Heuristic {i}")
            with open(f"{fname.split('.json')[0]}_eval.json", "w") as file:
                json.dump(evaluation, file)
    except:
        pass
    finally:
        with open(f"{fname.split('.json')[0]}_eval.json", "w") as file:
            json.dump(evaluation, file)

if __name__ == "__main__":
    json_file = "./chat_history/dbench-gpt4.json"
    evaluate_heuristic(json_file)