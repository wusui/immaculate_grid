# (c) 2026 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt
# for details)
"""
Get players likely to be in the solution
"""
import json
import requests
from bs4 import BeautifulSoup

def get_players():
    """
    Read file of all players who have been on 8 or more teams.
    Save ids in data/players.json
    """
    header = "https://www.baseball-reference.com"
    fname = "leaders/leaders_most_franchises.shtml"
    ifile = '/'.join([header, fname])
    response = requests.get(ifile, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.find_all('tr')
    peeple = list(map(lambda a: a.find_all('td'), rows[1:]))
    mpeep = list(filter(lambda a: int(a[1].get_text().split('-')[0]) >= 1940,
                        peeple))
    plyrs = list(map(lambda a: a[0].find('a')['href'], mpeep))
    with open('data/players.json', 'w', encoding='utf-8') as ofd:
        json.dump(plyrs, ofd, indent=4)

if __name__ == "__main__":
    get_players()
