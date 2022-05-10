#Usage: python3 bench-diff.py bench_master bench_patched

import json
import os
import numpy as np
import sys

f = open(sys.argv[1])
old_data = json.load(f)
f.close()

f = open(sys.argv[2])
new_data = json.load(f)
f.close()

index_types = ["HASH", "TREE"]
stats = ["MEDIAN", "MEAN"]
deltas = ["STD"]

print('Format: [replaces, selects, selrepl, updates, deletes]')

for idx_ty in index_types:
    print('------', idx_ty, '------')
    for stat in stats:
        print('---', stat, '---')
        old = np.array(old_data[idx_ty][stat])
        new = np.array(new_data[idx_ty][stat])
        print('master:', old)
        print('patched:', new)
        print('diff(%):', ((new - old) / old) * 100)
    for delta in deltas:
        print('---', delta, '---')
        print('master:', old_data[idx_ty][delta])
        print('patched:', new_data[idx_ty][delta])
