# (c) 2026 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt
# for details)
"""
Get team abbreviations
"""
import time
import json
import requests
from bs4 import BeautifulSoup

def expand_team(team_ind):
    """
    Look through a team's webpage and find all previous abbreviations for
    this team
    """
    tm_ind = team_ind.split('/')[2]
    header = "https://www.baseball-reference.com"
    ifile = ''.join([header, team_ind])
    response = requests.get(ifile, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    team_tab = soup.find('table', id="franchise_years")
    tbody = team_tab.find('tbody')
    blist = tbody.find_all('a', href=True)
    abbrevs = list(filter(lambda a: a['href'].startswith('/teams/'), blist))
    tabbrv = list(map(lambda a: a['href'], abbrevs))
    team_3c = list(set(list(map(lambda a: a.split('/')[2], tabbrv))))
    print(tm_ind, team_3c)
    time.sleep(30)
    return [tm_ind, team_3c]

def get_teams():
    """
    Read file of all current teams.  t
    """
    ifile = "https://www.baseball-reference.com/teams/"
    response = requests.get(ifile, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    team_table = soup.find('table', id="teams_active")
    nrows = team_table.find_all('a', class_=False)
    links = list(map(lambda a: a['href'], nrows))
    team_info = dict(list(map(expand_team, links)))
    with open('data/teams.json', 'w', encoding='utf-8') as ofd:
        json.dump(team_info, ofd, indent=4)

def get_current_links():
    """
    Create current_links.json, which links other abbreviations to
    current teams (KCA to OAK or MON to WSN)
    """
    with open('data/teams.json', 'r', encoding='utf-8') as ifd:
        tdata = json.load(ifd)
    out_dict = {}
    for new_dest in tdata.keys():
        for new_ind in tdata[new_dest]:
            out_dict[new_ind] = new_dest
    with open('data/team_link.json', 'w', encoding='utf-8') as ofd:
        json.dump(out_dict, ofd, indent=4)

if __name__ == "__main__":
    get_teams()
    get_current_links()
