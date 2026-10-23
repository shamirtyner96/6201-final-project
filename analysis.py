# Swing or Shift? Shamir Tyner, CSCI 6201 Lab 2
# Run from the repository root: python analysis.py
import csv
from pathlib import Path
import pandas as pd

# Load the original county returns.
raw_data = pd.read_csv('Lab2/countypres_2000-2024.csv')

# Uncomment these to explore the dataset.
# print(raw_data.shape, raw_data.columns.tolist())

# Use only Democratic and Republican TOTAL records. Other modes are ignored.
filter_rows = raw_data['party'].isin(['REPUBLICAN', 'DEMOCRAT']) & (raw_data['mode'] == 'TOTAL')
voter_data = raw_data[filter_rows]
# print(voter_data['candidatevotes'].describe())

# Add the county records to state-level party totals for each election year.
groupedData = {}
for index, row in voter_data.iterrows():
    year = row['year']
    state = row['state']
    party = row['party']
    votes = row['candidatevotes']

    if year not in groupedData:
        groupedData[year] = {}
    if state not in groupedData[year]:
        groupedData[year][state] = {}
    if party not in groupedData[year][state]:
        groupedData[year][state][party] = 0
    groupedData[year][state][party] += votes

# Store one margin per state and year. None means there is no usable TOTAL data.
state_margins = {}
years = sorted(raw_data['year'].unique())
states = sorted(raw_data['state'].unique())
for year in years:
    state_margins[year] = {}
    for state in states:
        state_margins[year][state] = None
        if year not in groupedData or state not in groupedData[year]:
            continue
        votes = groupedData[year][state]
        if 'DEMOCRAT' not in votes or 'REPUBLICAN' not in votes:
            continue
        dem_votes = votes['DEMOCRAT']
        rep_votes = votes['REPUBLICAN']
        total = dem_votes + rep_votes
        if total == 0:
            continue
        dem_share = dem_votes / total * 100
        rep_share = rep_votes / total * 100
        state_margins[year][state] = dem_share - rep_share

# Save the results so they remain available after the program finishes.
Path('results').mkdir(exist_ok=True)
with open('results/state_margins.csv', 'w', newline='', encoding='utf-8') as output:
    writer = csv.writer(output)
    writer.writerow(['year', 'state', 'margin_percentage_points'])
    for year in years:
        for state in states:
            margin = state_margins[year][state]
            if margin is None:
                writer.writerow([year, state, ''])
            else:
                writer.writerow([year, state, round(margin, 2)])

print('\nSaved state margins to results/state_margins.csv')
print('Positive margins favor Democrats; negative margins favor Republicans.')
print('A blank margin means no usable TOTAL records were available.')
