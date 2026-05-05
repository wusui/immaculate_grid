# (c) 2026 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt
# for details)
"""
Generate the json files in the data directory
"""
from get_players import get_players
from get_teams import get_teams, get_current_links
from get_ptcs import get_ptcs
from gen_imm_data import gen_imm_data
from gen_plyr_team_pair import gen_plyr_team

get_players()
get_teams()
get_current_links()
get_ptcs('new_players')
gen_imm_data()
gen_plyr_team()
