# (c) 2026 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt
# for details)
"""
Get table of team-pairs indexed by player
"""
import json
from itertools import combinations

def gen_plyr_team():
    """
    Return dict indexed by shortened name, where the value is a list of
    team pairs
    """
    def pt_conv(in_data):
        def ptc_indv(plyr):
            def csimp(plyr):
                return plyr.split('/')[-1].split('.')[0]
            def tcombos(tlist):
                return list(map('-'.join, list(combinations(tlist, 2))))
            return (csimp(plyr),tcombos(in_data[plyr]))
        return list(map(ptc_indv, in_data))
    with open('data/player_teams.json', 'r', encoding='utf-8') as ifd:
        plyr_team_data = json.load(ifd)
    ptp = dict(pt_conv(plyr_team_data))
    with open('data/plyr_team_pair.json', 'w', encoding='utf-8') as ofd:
        json.dump(ptp, ofd, indent=4)

if __name__ == "__main__":
    gen_plyr_team()
