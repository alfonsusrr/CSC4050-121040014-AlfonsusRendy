import json
import os
import pprint
from util.DBenchLoader import load_dbench_bug_data


def main():
    data = load_dbench_bug_data()
    langs = ["cpp", "java", "python3"]

    extracted_types = []
    extracted_data = []
    for lang in langs:
        for bug_type in data[lang]["types"]:
            if bug_type not in ["double", "triple", "quadruple"]:
                if bug_type not in extracted_types:
                    extracted_types.append(bug_type)
                for code in data[lang][bug_type]:
                    extracted_data.append({
                        "lang": lang,
                        "bug_type": bug_type,
                        "buggy_code": code["buggy_code"],
                        "reasoning": code["explanations"]
                    })
    print(extracted_types)

    with open("dbench.json", "w") as file:
        json.dump(extracted_data, file)

if __name__=="__main__":
    main()