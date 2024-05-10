import json

def clean_evaluation(efile):
    with open(efile, "r") as file:
        evaluations = json.load(file)
    
    types = []
    score = {}
    for e in evaluations:
        if e["type"] not in types:
            types.append(e["type"])
            score[e["type"]] = {
                "relevancy": 0,
                "correctness generalisability": 0,
                "precision": 0,
                "count": 0
            }
    for e in evaluations:
        score[e["type"]]["relevancy"] += e["relevancy"]["score"]
        score[e["type"]]["correctness generalisability"] += e["correctness generalisability"]["score"]
        score[e["type"]]["precision"] += e["precision"]["score"]
        score[e["type"]]["count"] +=1

    tot_rel = 0
    tot_corr = 0
    tot_prec = 0
    tot = 0
    for k, v in score.items():
        print("-----")
        print(k)
        print(f'Relevancy: {v["relevancy"]/v["count"]}')
        print(f'Correctness: {v["correctness generalisability"]/v["count"]}')
        print(f'Precision: {v["precision"]/v["count"]}')
        tot += 1
        tot_rel += v["relevancy"]/v["count"]
        tot_corr += v["correctness generalisability"]/v["count"]
        tot_prec += v["precision"]/v["count"]
    print("-----")
    print(f'Relevancy: {tot_rel/tot}')
    print(f'Correctness: {tot_corr/tot}')
    print(f'Precision: {tot_prec/tot}')


if __name__ == "__main__":
    efile = "./chat_history/dbench-gpt4_eval_cleaned.json"
    clean_evaluation(efile)