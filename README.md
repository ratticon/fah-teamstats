# fah-teamstats
A Python script that downloads public team data from the [Folding@Home](https://foldingathome.org/) Statistics API and prints it to the console.

![Screenshot of Example Output](https://github.com/ratticon/fah-teamstats/raw/master/fah-teamstats-screenshot.png)

Written in Python 3.7.0 by Benjamin Cooper ([Ratticon](https://ratticon.com)) of [x0ptis](https://stats.foldingathome.org/team/236098)

## What It Does:
Downloads public team data from the [Folding@Home](https://foldingathome.org) [Statistics API](https://stats.foldingathome.org/api) and prints it
to the console.

## Requirements:
- Python 3 (3.7.0 at time of writing)
- requests (2.23.0 at time of writing)

## Getting Started:
Install [Python 3](https://www.python.org/downloads/) if needed.

Install the [requests](https://pypi.org/project/requests/) library if needed by running `pip install requests`

Download [fahstats.py](https://github.com/ratticon/fah-teamstats/blob/master/fah-teamstats.py) and edit the following line with the team IDs you wish to query:

`print_team_data(team_ids=[236098])`

You can query multiple teams by filling the team_ids array like so:

`print_team_data(team_ids=[1,2,3])`

Run the script with `python fah-teamstats.py`

Enjoy, and keep on foldin'!
