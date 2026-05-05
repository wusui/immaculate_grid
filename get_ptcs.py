# (c) 2026 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt
# for details)
"""
Find good player candidates
"""
import os
import time
import json
import pandas as pd

def get_plyr_teams(pname, tdata):
    """
    Get dict of teams indexing player played for
    """
    player = f"https://www.baseball-reference.com{pname}"
    df_list = pd.read_html(player)
    indx = 0
    if 'Team' not in df_list[0]:
        indx = 1
    fields = df_list[indx]['Team'].astype(str).tolist()
    mfields = list(filter(lambda a: a.isupper() and a.isalpha(), fields))
    lfields = list(map(lambda a: tdata[a], mfields))
    answer = list(set(lfields))
    return sorted(answer)

def get_ptcs(fplayers):
    """
    Run get_plyr_teams on all the entries in players.json
    """
    with open('data/team_link.json', 'r', encoding='utf-8') as ifd:
        tdata = json.load(ifd)
    with open(f'data/{fplayers}.json', 'r', encoding='utf-8') as ifd2:
        pdata = json.load(ifd2)
    if os.path.exists('data/player_teams.json'):
        with open('data/player_teams.json', 'r', encoding='utf-8') as ifd3:
            ret_val = json.load(ifd3)
    else:
        ret_val = {}
    for entry in pdata:
    #for entry in ["/players/h/hollida01.shtml", "/players/e/eisenji01.shtml"]:
        new_data = get_plyr_teams(entry, tdata)
        ret_val[entry] = new_data
        print(entry)
        with open('data/player_teams.json', 'w', encoding='utf-8') as ofd:
            json.dump(ret_val, ofd, indent=4)
        time.sleep(30)

if __name__ == "__main__":
    #get_ptcs('players')
    get_ptcs('new_players')
