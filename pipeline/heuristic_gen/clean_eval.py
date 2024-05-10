import json

def clean_evaluation(hfile, efile):
    with open(hfile, "r") as file:
        heuristics = json.load(file)
    
    with open(efile, "r") as file:
        evaluations = json.load(file)
    
    cleaned_evaluations = []
    for i in range(len(evaluations)):
        splitted = evaluations[i].split("\n")
        score_split = splitted[0].split(":")[1].strip()[1:-1].split(", ")
        if splitted[1] == '':
            ind = 2
        else:
            ind = 1
        reason_split = splitted[ind].split("n:")[1].strip()[1:-1].replace(',"', '",').split('",')
        ind2metric = {
            0: "relevancy",
            1: "correctness generalisability",
            2: "precision"
        }
        evl = {}
        evl["type"] = heuristics[i]["type"]
        for j in range(3):
            evl[ind2metric[j]] = {
                "score": int(score_split[j]),
                "reason": reason_split[j].replace('"',  '').strip()
            }
        cleaned_evaluations.append(evl)
    with open(f"{efile.split('.json')[0]}_cleaned.json", "w") as file:
        json.dump(cleaned_evaluations, file)

if __name__ == "__main__":
    hfile = "./chat_history/dbench-gpt4.json"
    efile = "./chat_history/dbench-gpt4_eval.json"
    clean_evaluation(hfile, efile)