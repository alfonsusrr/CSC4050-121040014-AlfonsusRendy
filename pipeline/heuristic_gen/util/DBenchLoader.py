import json
import os

def load_dbench_bug_data():
    """ load data with different languages and bug types """

    SRC_DIR = f"../../DebugBench/benchmark"

    res = {
        'cpp': {
            "types":[]
        },
        'java': {
            "types": []
        },
        'python3': {
            "types": []
        },
    }
    files = os.listdir(SRC_DIR)
    for file in files:
        file_name = os.path.splitext(file)[0]
        lang = file_name[:file_name.find('_')]
        bug_type = file_name[file_name.find('_') + 1:]
        if bug_type not in res[lang]["types"]:
            res[lang]["types"].append(bug_type)
        res[lang][bug_type] = json.load(open(os.path.join(SRC_DIR, file)))
    return res