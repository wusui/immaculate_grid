# (c) 2026 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt
# for details)
"""
Get players likely to be in the solution
"""
import json
from itertools import combinations

def gen_imm_data():
    """
    Generate a dict indexed by team-pair whose values are lists of players that
    hsve played on this combination of teams
    """
    def shorten(plyr):
        return plyr.split('/')[-1].split('.')[0]
    with open('data/team_link.json', 'r', encoding='utf-8') as ifd:
        teams = json.load(ifd)
    tvalues = sorted(set(list(map(lambda a: teams[a], teams.keys()))))
    tpairs = list(combinations(tvalues, 2))
    labels = list(map(lambda a: '-'.join([a[0], a[1]]), tpairs))
    boxes = [ [] for _ in range(len(labels))]
    hist = dict(list(zip(labels, boxes)))
    with open('data/player_teams.json', 'r', encoding='utf-8') as pfd:
        player_data = json.load(pfd)
    for entry in player_data:
        lpairs = list(combinations(player_data[entry], 2))
        lkeys = list(map(lambda a: '-'.join([a[0], a[1]]), lpairs))
        for ikey in lkeys:
            hist[ikey].append(shorten(entry))
    with open('data/team_pairs.json', 'w', encoding='utf-8') as ofd:
        json.dump(hist, ofd, indent=4)

if __name__ == "__main__":
    gen_imm_data()
