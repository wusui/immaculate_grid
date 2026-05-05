# (c) 2026 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt
# for details)
"""
Generate display files from the log files
"""
import os
import time
import json
from itertools import chain
import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

def create_html(fname, in_data):
    """
    jinja2 interface
    """
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(fname)
    out_html = template.render(in_data)
    if 'index' in in_data:
        htmln = fname.split('.')[0]
        fname = '.'.join([f"{htmln}{in_data['index']}", 'html'])
    with open(f"displays/{fname}", 'w', encoding='utf-8') as ofd:
        ofd.write(out_html)

def get_name(abbrev):
    """
    Extract player's real name from baseball reference (abbrev is their
    abbreviation used on baseball reference)
    """
    html_str = f"/{abbrev[0]}/{abbrev}.shtml"
    html_src = "https://www.baseball-reference.com/players"
    htmlf = html_src + html_str
    response = requests.get(htmlf, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    nmpart = soup.find('title').text
    time.sleep(30)
    return nmpart.split(' Stats, ')[0]

def get_name_tab(solution):
    """
    Loop to extract all names based on abbreviations
    """
    name_tab = {}
    for person in solution:
        name_tab[person] = get_name(person)
    return name_tab

def main_rtn():
    """
    Main routine used to generate display files
    """
    def breakup(ilist):
        return [ilist[ind:ind + 87] for ind in range(0, len(ilist), 87)]
    def gen_solution(sol_info):
        def get_pr_data(tm_pair):
            plist = list(filter(lambda a: a in tp_info[tm_pair], sol_info[1]))
            return [len(plist), plist[0]]
        tdata = list(map(get_pr_data, tp_info))
        if min(list(map(lambda a: a[0], tdata))) == 0:
            print("Error: uncovered pair found")
        if len(list(set(list(map(lambda a: a[1], tdata))))) > 18:
            print("Invalid number of players in solution")
        return tdata
    def simplify(xtra_data):
        conv0 = list(map(lambda a: roll_call[a], xtra_data[0][1]))
        conv1 = list(map(lambda a: [a[0], roll_call[a[1]]], xtra_data[1]))
        conv2 = list(zip(list(tp_info.keys()), conv1))
        conv3 = list(map(lambda a: [a[0], a[1][0], a[1][1]], conv2))
        return [conv0, conv3]
    def get_pi():
        def gpi_in(person):
            sol_int = list(filter(lambda a: person in a[0][1], answr))
            sol_nums = list(map(lambda a: a[0][0], sol_int))
            return [roll_call[person], sol_nums]
        return list(map(gpi_in, sorted(everybody)))
    with open("data/zz_solutions.logs", 'r', encoding='utf-8') as idf:
        xtract = json.load(idf)
    solutions = {}
    for entry in enumerate(xtract):
        solutions[entry[0] + 1] = entry[1].split('|')
    all_ans = []
    for solda in solutions.items():
        all_ans.append(solda[1])
    everybody = list(set(chain.from_iterable(all_ans)))
    if not os.path.exists("data/peep_tbl.json"):
        roll_call = {}
    else:
        with open("data/peep_tbl.json", 'r', encoding='utf-8') as ifd:
            roll_call = json.load(ifd)
    for person in everybody:
        if person not in roll_call:
            roll_call[person] = get_name(person)
            print(person, '---', roll_call[person])
    with open("data/peep_tbl.json", 'w', encoding='utf-8') as ofd:
        json.dump(roll_call, ofd, indent=4)
    with open("data/team_pairs.json", 'r', encoding='utf-8') as ifd:
        tp_info = json.load(ifd)
    result = list(map(gen_solution, solutions.items()))
    zip(list(tp_info.keys()), result)
    answr = list(zip(list(solutions.items()), result))
    answer = list(map(simplify, answr))
    fanswer = list(map(lambda a: {'index': a[0] + 1,
            'answer': ', '.join(a[1][0]),
            'table': breakup(a[1][1])}, enumerate(answer)))
    per_indx =  get_pi()
    outans = list(map(lambda a: a[1], answer))
    soltxt = list(range(1, len(outans) + 1))
    create_html('immaculate.html', {'snumb': len(outans), 'slist': soltxt})
    create_html('player_index.html', {'in_data': per_indx})
    for entry in fanswer:
        create_html('solutions.html', entry)

if __name__ == "__main__":
    main_rtn()
