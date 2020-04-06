# fah-teamstats
A Python script that downloads public team data from the [Folding@Home](https://foldingathome.org/) Statistics API and prints it to the console.

![Screenshot of Example Output](https://github.com/ratticon/fah-teamstats/raw/master/fah-teamstats%20screenshot.png)

Written in Python 3.7.0 by Benjamin Cooper ([Ratticon](https://ratticon.com)) of [x0ptis](https://stats.foldingathome.org/team/236098)

## What It Does:
Downloads public team data from the Folding@Home [Statistics API](https://stats.foldingathome.org/api) and prints it
to the console.

## Getting Started:
Download [fahstats.py](https://github.com/ratticon/fah-teamstats/blob/master/fah-teamstats.py) and edit the following line with the team IDs you wish to query:

`print_team_data(team_ids=[236098])`

You can query multiple teams by filling the team_ids array like so:

`print_team_data(team_ids=[1,2,3])`

Enjoy, and keep on foldin'!
