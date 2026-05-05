# (c) 2026 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt
# for details)
"""
Generate the text files in the logs directory
"""
import os
from time import sleep
import json
from brainz import solver
from brain_check import brain_check

def find_solution(person):
    """
    Solve for one player
    """
    if os.path.exists(f'logs/{person}.log'):
        print(f'skipping {person}')
        return
    solver(person)
    brain_check(person)
    sleep(120)

def find_all_solutions(tsize):
    """
    Loop for all players that have played for a given number of teams
    """
    with open('data/plyr_team_pair.json', 'r', encoding='utf-8') as ifd:
        plyrs = json.load(ifd)
    csize = tsize * (tsize - 1) // 2
    sol_list = list(filter(lambda a: len(plyrs[a]) == csize, plyrs.keys()))
    for entry in sol_list:
        find_solution(entry)

if __name__ == "__main__":
    find_all_solutions(9)
