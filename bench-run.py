import json
import os
import numpy as np

iter_num = 10

tree_result = np.ndarray((iter_num, 5), dtype=float)
hash_result = np.ndarray((iter_num, 5), dtype=float)
 
hash_idx = 1
tree_idx = 2

for iter in range(iter_num):
    for file in os.listdir("."):
        if file.endswith(".json"):
            os.remove(file)
    cmd = "./bench-cfg.lua"
    os.system(cmd)
    for file in os.listdir("."):
        if file.endswith(".json"):
            f = open(file)
            data = json.load(f)
            f.close()
    hash_obs = data[hash_idx][1]
    for i in range(len(hash_obs)):
        hash_result[iter][i] = hash_obs[i][1]
    tree_obs = data[tree_idx][1]
    for i in range(len(tree_obs)):
        tree_result[iter][i] = tree_obs[i][1]
        
data_set = {
"HASH":
    {
    "MEDIAN": np.median(hash_result, axis=0).tolist(),
    "MEAN": np.mean(hash_result, axis=0).tolist(),
    "STD": np.std(hash_result, axis=0).tolist()
    },
"TREE":
    {
    "MEDIAN": np.median(tree_result, axis=0).tolist(),
    "MEAN": np.mean(tree_result, axis=0).tolist(),
    "STD": np.std(tree_result, axis=0).tolist()
    }
}

json_dump = json.dumps(data_set)
f = open('bench-res.json', 'w')
f.write(json_dump)
f.close()
