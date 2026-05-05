# (c) 2026 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt
# for details)
"""
Generate solutions in log files
"""
import os
import time
import json
from itertools import chain
import requests
from bs4 import BeautifulSoup

def get_all_logs():
    """
    Extract the data files generated.  Save winning combinations as log
    files in log directory
    """
    def get_tp(solution):
        xlist = list(map(lambda a: plyrs[a.strip()], solution))
        xxlist = list(chain.from_iterable(xlist))
        xxxlist = list(set(xxlist))
        return xxxlist
    def t1_check(sols):
        plist = list(map(lambda a: a.split('|'), sols))
        xteams = list(map(get_tp, plist))
        mtch_up = list(zip(sols, list(map(len, xteams))))
        result = list(filter(lambda a: a[1] == 435, mtch_up))
        return list(map(lambda a: a[0], result))
    def align_tms(sols):
        def fixt(tinfo):
            tparts = list(filter(lambda a: '-' in a, tinfo.split('/')))
            tintv = sorted('-'.join(tparts).strip().split('-'))
            return '-'.join(tintv)
        spltp = list(map(lambda a: a.split(':'), sols))
        fixp = list(map(lambda a: [a[0], fixt(a[1])], spltp))
        return list(set(list(map(':'.join, fixp))))
    def t2_check(sols):
        ft_sols = list(set(align_tms(sols)))
        out_sols = []
        new_list = []
        for entry in ft_sols:
            teaml = entry.split(':')[-1].split('-')
            print(teaml)
            teame = list(map(list, enumerate(teaml)))
            teami = list(map(lambda a: [a[0] + 1, a[1]], teame))
            teamt = list(map(lambda a: f'&t{a[0]}={a[1]}', teami))
            chk_cmd = t2_html + ''.join(teamt)
            response = requests.get(chk_cmd, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            tfind = soup.find_all('table')
            nxt_ent = ''
            out_cmd = ''
            for itab in tfind:
                get_plyr = itab.find_all('th',
                                             attrs={'data-append-csv': True})
                for splyr in get_plyr:
                    nxt_ent = splyr['data-append-csv']
                    if nxt_ent in plyrs:
                        out_cmd = entry.split(':')[0] + f'/{nxt_ent}'
                        out_sols.append(out_cmd)
                        break
                if out_cmd:
                    break
            if not out_cmd:
                if len(nxt_ent) > 0:
                    new_list.append(nxt_ent)
                    out_cmd = entry.split(':')[0] + f'/{nxt_ent}'
                    out_sols.append(out_cmd)
            time.sleep(30)
        if new_list:
            print('New players have been added')
            print(new_list)
        return list(map(lambda a: '|'.join(sorted(a.split('/'))), out_sols))
    t2_html = ''.join(['https://www.baseball-reference.com/friv/',
                'players-who-played-for-multiple-teams-franchises.',
                'fcgi?level=franch'])
    logs = os.listdir('logs')
    biglist = []
    with open('data/plyr_team_pair.json', 'r', encoding='utf-8') as dfd:
        plyrs = json.load(dfd)
    for entry in logs:
        with open(f'logs/{entry}', 'r', encoding='utf-8') as ifd:
            newdata = ifd.readlines()
            biglist.append(newdata)
    alist = list(chain.from_iterable(biglist))
    type1 = t1_check(list(set(list(filter(lambda a: '|' in a, alist)))))
    type2 = t2_check(list(set(list(filter(lambda a: '/' in a, alist)))))
    both = list(chain.from_iterable([type1, type2]))
    both1 = list(map(lambda a: a.strip(), both))
    both2 = list(set(both1))
    with open('data/zz_solutions.logs', 'w', encoding='utf-8') as ofd:
        json.dump(both2, ofd, indent=4)

if __name__ == "__main__":
    get_all_logs()
