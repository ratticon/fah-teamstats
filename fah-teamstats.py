'''
fahstats.py

Author:     Benjamin Cooper (Ratticon [x0ptis])
Released:   2020-04-06
Written on: Python 3.7.0

Function:
Downloads public team data from the Folding@Home Statistics API and prints it
to the console. Edit the following line with the team IDs you wish to query:

print_team_data(team_ids=[236098])

You can query multiple teams by filling the array like so:

print_team_data(team_ids=[1,2,3])

Enjoy, and keep on foldin'!
'''

import requests
import math
from datetime import datetime


def get_timestamp():
    return f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"


def get_team_stats_json(team_id):
    '''
    Queries the Folding@Home statistics API for team_id's data.
    Returns JSON response.
    Exits on errors.
    '''
    print(f"\nDownloading statistics for Folding@Home team id {team_id}...")
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
    if response:
        print(f'[API Response {response.status_code} - OK]\n')
    else:
        print(f'[API Response {response.status_code} - ERROR]\n')
        exit()
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


def print_team_info(json):
    '''
    Reads team info from json and prints to console.
    '''
    # for key, value in json.items():
    #     print(f"{key}={value}")
    first_col_width = 14
    rank_percentile = calculate_team_rank_percentile(json['rank'], json['total_teams'], inverse=True)
    print(f"{str('Team: ').ljust(first_col_width)}{json['name']} ({json['team']})")
    print(f"{str('Homepage: ').ljust(first_col_width)}{json['url']}")
    print(f"{str('Ranked: ').ljust(first_col_width)}{json['rank']} of {json['total_teams']} (Top {rank_percentile}%)")
    print(f"{str('Score: ').ljust(first_col_width)}{json['credit']}")
    print(f"{str('Work Units: ').ljust(first_col_width)}{json['wus']}")
    print(f"{str('Active CPUS: ').ljust(first_col_width)}{json['active_50']} in last 50 days")
    total_members = len(json['donors'])
    if total_members == 1000:
        total_members = "1000+"
    print(f"{str('Members: ').ljust(first_col_width)}{total_members}")
    print(f"{str('As of: ').ljust(first_col_width)}{get_timestamp()}\n")


def print_member_info(json, margin=2, result_limit=20):
    '''
    Reads team member info from json and prints a table to console.
    Optional margin argument defines column margins (2 characters by default).
    Optional result_limit argument defines maximum number of members to print.
    '''
    # Calculate table column widths
    max_lengths = {}
    lengths_checked = 0
    for member in json['donors']:
        if lengths_checked >= result_limit:
            break
        for key, value in member.items():
            val_length = len(str(value))
            if key not in max_lengths:
                max_lengths[key] = val_length
            elif val_length > max_lengths[key]:
                max_lengths[key] = val_length
        lengths_checked += 1
    print(
          f"{str('Rank').rjust(max_lengths['rank'])}{' '*margin}"
          f"{str('Name').ljust(max_lengths['name'])}{' '*margin}"
          f"{str('Credit').rjust(max_lengths['credit'])}{' '*margin}"
          f"{str('WUs').rjust(max_lengths['wus'])}"
    )
    # Print line under table header
    table_width = margin*3
    for key in ['rank', 'name', 'credit', 'wus']:
        table_width += max_lengths[key]
    print('-'*table_width)
    # Print member statistics
    members_printed = 0
    for member in json['donors']:
        if members_printed >= result_limit:
            print(f"[...] (List truncated to top {members_printed} members)")
            break
        if 'rank' not in member.keys():
            member['rank'] = 'N/A'
        print(
             f"{str(member['rank']).rjust(max_lengths['rank'])}{' '*margin}"
             f"{str(member['name']).ljust(max_lengths['name'])}{' '*margin}"
             f"{str(member['credit']).rjust(max_lengths['credit'])}{' '*margin}"
             f"{str(member['wus']).rjust(max_lengths['wus'])}"
        )
        members_printed += 1
    print()


def print_team_data(team_ids=[1], member_result_limit=20):
    '''
    Queries Folding@Home API and prints all team data for team_ids.
    Limits length of member lists to member_result_limit. (Default limit 20)
    '''
    for team_id in team_ids:
        team_data = get_team_stats_json(team_id)
        print_team_info(team_data)
        print_member_info(team_data, result_limit=member_result_limit)


print_team_data(team_ids=[236098])
