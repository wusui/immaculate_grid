# (c) 2026 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt
# for details)
"""
Analyze a single player and save possible solutions in data/temp_solutions.json
"""
import json
from itertools import chain, combinations

def solver(person):
    """
    Wrapper that reads data before solving
    """
    def comp_group(plyrs, pl_data, comb_cnt):
        bestsofar = 0
        solutions = []
        ret_sol = []
        comb_list = combinations(pl_data, comb_cnt)
        for entry in comb_list:
            for last_set in plyrs:
                new_list = list(chain.from_iterable([last_set, list(entry)]))
                pairs = list(map(lambda a: full_data[a], new_list))
                fpairs = list(set(chain.from_iterable(pairs)))
                if len(fpairs) == bestsofar:
                    print('same: ', len(fpairs), entry)
                    ret_sol.append(list(chain.from_iterable([last_set, entry])))
                    solutions.append(fpairs)
                if len(fpairs) > bestsofar:
                    solutions = [fpairs]
                    ret_sol = [list(chain.from_iterable([last_set, entry]))]
                    bestsofar = len(fpairs)
                    print('better: ', bestsofar, entry)
        return ret_sol
    with open('data/plyr_team_pair.json', 'r', encoding='utf-8') as ifd:
        full_data = json.load(ifd)
    d_items = list(full_data.items())
    top12 = dict(filter(lambda a: len(a[1]) >= 66, d_items))
    topb9 = dict(filter(lambda a: len(a[1]) >= 36, d_items))
    plist = list(top12.keys())
    plist.append(person)
    res10 = comp_group([plist], topb9, 4)
    res13 = comp_group(res10, full_data, 3)
    res16 = comp_group(res13, full_data, 3)
    res18 = comp_group(res16, full_data, 2)
    strize = list(set(list(map(','.join, list(map(sorted, res18))))))
    result = list(map(lambda a: a.split(','), strize))
    with open('data/temp_solution.json', 'w', encoding='utf-8') as ofd:
        json.dump(result, ofd, indent=4)

if __name__ == "__main__":
    solver('hawkila01')
