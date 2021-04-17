'''
fahstats.py

Author:     Benjamin Cooper (Ratticon [x0ptis])
Released:   2020-04-06
Written on: Python 3.7.0
Requires:   requests (2.23.0 at time of writing)

Function:
Downloads public team data from the Folding@Home Statistics API and prints it
to the console. Edit the following line with the team IDs you wish to query:

print_team_data(team_ids=[236098])

You can query multiple teams by filling the array like so:

print_team_data(team_ids=[1,2,3])

Enjoy, and keep on foldin'!
'''

import argparse
import requests
import math
from datetime import datetime


def get_timestamp():
    return f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"


def get_team_info_json(team_id):
    '''
    Queries the Folding@Home statistics API for team_id's data.
    Returns JSON response.
    Exits on errors.
    '''
    print(f"\nQuerying statistics API for Folding@Home team id {team_id}...", end='')
    # Try API Query
    try:
        response = requests.get(f'https://api2.foldingathome.org/team/{team_id}')
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:\n" + repr(errh))
        exit()
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the FAH Statistics API occurred:\n" + repr(errc))
        exit()
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:\n" + repr(errt))
        exit()
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred:\n" + repr(err))
        exit()
    # Check API response is OK
    if not response:
        print(f'\nQuery failed. API Response = {response.status_code} - ERROR.')
        exit()
    print('Done')
    return response.json()


def get_team_count():
    '''
    Queries the Folding@Home statistics API for the total number of Folding@home teams.
    Returns an integer.
    Exits on errors.
    '''
    print(f"\nQuerying statistics API for total number of teams...", end='')
    # Try API Query
    try:
        response = requests.get(f'https://api2.foldingathome.org/team/count')
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:\n" + repr(errh))
        exit()
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the FAH Statistics API occurred:\n" + repr(errc))
        exit()
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:\n" + repr(errt))
        exit()
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred:\n" + repr(err))
        exit()
    # Check API response is OK
    if not response:
        print(f'\nQuery failed. API Response = {response.status_code} - ERROR.')
        exit()
    # Print and return total
    result = int(response.json())
    print(f'{result}')
    return result


def get_members_json(team_id):
    '''
    Queries the Folding@Home statistics API for info on team_id's members.
    Returns JSON response.
    Exits on errors.
    '''
    print(f"Querying statistics API for Folding@Home team id {team_id}'s member stats...", end='')
    # Try API Query
    try:
        response = requests.get(f'https://api2.foldingathome.org/team/{team_id}/members')
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:\n" + repr(errh))
        exit()
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the FAH Statistics API occurred:\n" + repr(errc))
        exit()
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:\n" + repr(errt))
        exit()
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred:\n" + repr(err))
        exit()
    # Check API response is OK
    if not response:
        print(f'\nQuery failed. API Response = {response.status_code} - ERROR.')
        exit()
    print('Done\n')
    return response.json()


def get_legacy_team_stats_json(team_id):
    '''
    Queries the legacy Folding@Home statistics API for team_id's data.
    Returns JSON response.
    Exits on errors.
    '''
    print(f"\nQuerying legacy statistics API for Folding@Home team id {team_id}...", end='')
    # Try API Query
    try:
        response = requests.get(f'https://stats.foldingathome.org/api/team/{team_id}')
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:\n" + repr(errh))
        exit()
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the FAH Statistics API occurred:\n" + repr(errc))
        exit()
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:\n" + repr(errt))
        exit()
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred:\n" + repr(err))
        exit()
    # Check API response is OK
    if not response:
        print(f'\nQuery failed. API Response = {response.status_code} - ERROR.')
        exit()
    print('\n')
    return response.json()


def calculate_team_rank_percentile(rank_integer, total_teams_integer, inverse=False):
    '''
    Takes rank and total teams, calculates and returns the ranking percentile.\n
    Example of inverse=False: 1 of 100 = 99 (Ranks better than 99%)
    Example of inverse=True: 1 of 100 = 1 (Ranks in top 1%)\n
    '''
    percentile = (100 / total_teams_integer) * rank_integer
    if not inverse:
        percentile = 100 - percentile
    return math.ceil(percentile)


def print_team_info(team_info_json, team_count, members_json):
    '''
    Reads team info from provided data and prints to console.
    '''
    # TEAM INFO JSON DEBUG
    # for key, value in team_info_json.items():
    #     print(f"{key}={value}")
    # TEAM INFO JSON DEBUG
    # print(members_json)
    # for m_name, m_id, m_rank, m_score, m_wus in members_json:
    #     print(f"Name:{m_name} Id:{m_id}, Rank:{m_rank}, Score:{m_score}, WUs:{m_wus}")
    # print()
    first_col_width = 14
    rank_percentile = calculate_team_rank_percentile(team_info_json['rank'], team_count, inverse=True)
    print(f"{str('Team: ').ljust(first_col_width)}{team_info_json['name']} ({team_info_json['id']})")
    print(f"{str('Homepage: ').ljust(first_col_width)}{team_info_json['url']}")
    print(f"{str('Ranked: ').ljust(first_col_width)}{team_info_json['rank']} of {team_count} (Top {rank_percentile}%)")
    print(f"{str('Score: ').ljust(first_col_width)}{team_info_json['score']}")
    print(f"{str('Work Units: ').ljust(first_col_width)}{team_info_json['wus']}")
    # Active CPUs commented out because is it not exposed easily in new API
    # print(f"{str('Active CPUs: ').ljust(first_col_width)}{team_info_json['active_50']} in last 50 days")
    total_members = len(members_json)-1
    if total_members == 1000:
        total_members = "1000+"
    print(f"{str('Members: ').ljust(first_col_width)}{total_members}")
    print(f"{str('As of: ').ljust(first_col_width)}{get_timestamp()}\n")


def print_member_info(members_json, margin=2, result_limit=20):
    '''
    Reads team member info from json and prints a table to console.
    Optional margin argument defines column margins (2 characters by default).
    Optional result_limit argument defines maximum number of members to print.
    '''
    # DEBUG MEMBERS_JSON
    # for m_name, m_id, m_rank, m_score, m_wus in members_json:
    #     print(f"Name:{m_name} Id:{m_id}, Rank:{m_rank}, Score:{m_score}, WUs:{m_wus}")
    # print()

    # Calculate table column widths
    max_lengths = {
        'name': 0,
        'id': 0,
        'rank': 0,
        'score': 0,
        'wus': 0
    }
    lengths_checked = 0
    for m_name, m_id, m_rank, m_score, m_wus in members_json:
        if m_name == "name":
            continue
        if lengths_checked >= result_limit:
            break
        if len(m_name) > max_lengths['name']:
            max_lengths['name'] = len(m_name)
        if len(str(m_id)) > max_lengths['id']:
            max_lengths['id'] = len(str(m_id))
        if len(str(m_rank)) > max_lengths['rank']:
            max_lengths['rank'] = len(str(m_rank))
        if len(str(m_score)) > max_lengths['score']:
            max_lengths['score'] = len(str(m_score))
        if len(str(m_wus)) > max_lengths['wus']:
            max_lengths['wus'] = len(str(m_wus))
        lengths_checked += 1
    print(
          f"{str('Rank').rjust(max_lengths['rank'])}{' '*margin}"
          f"{str('Name').ljust(max_lengths['name'])}{' '*margin}"
          f"{str('Score').rjust(max_lengths['score'])}{' '*margin}"
          f"{str('WUs').rjust(max_lengths['wus'])}"
    )
    # Print line under table header
    table_width = margin*3
    for key in ['rank', 'name', 'score', 'wus']:
        table_width += max_lengths[key]
    print('-'*table_width)
    # Print member statistics
    members_printed = 0
    for m_name, m_id, m_rank, m_score, m_wus in members_json:
        if m_name == "name":
            continue
        if members_printed >= result_limit:
            print(f"[...] (List truncated to top {members_printed} members)")
            break
        if m_rank is None:
            m_rank = "-"
        print(
             f"{str(m_rank).rjust(max_lengths['rank'])}{' '*margin}"
             f"{str(m_name).ljust(max_lengths['name'])}{' '*margin}"
             f"{str(m_score).rjust(max_lengths['score'])}{' '*margin}"
             f"{str(m_wus).rjust(max_lengths['wus'])}"
        )
        members_printed += 1


def print_team_data(team_ids=[1], member_result_limit=20):
    '''
    Queries Folding@Home API and prints all team data for team_ids.
    Limits length of member lists to member_result_limit. (Default limit 20)
    '''
    team_count = get_team_count()
    for team_id in team_ids:
        team_info_json = get_team_info_json(team_id)
        members_json = get_members_json(team_id)
        print_team_info(team_info_json, team_count, members_json)
        # This probably needs to change under here
        print_member_info(members_json, result_limit=member_result_limit)
    print()


# Main Code-------------------------------------------------------------------

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Downloads and prints Folding@Home team statistics")
parser.add_argument(
    'team_ids', metavar='#', type=int, nargs='*',
    help='Team ID(s) to get statistics for'
)
args = parser.parse_args()

if args.team_ids:
    print_team_data(team_ids=args.team_ids)
else:
    print_team_data(team_ids=[236098])
