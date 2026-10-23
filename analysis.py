# Swing or Shift? Shamir Tyner, CSCI 6201 Lab 2
# Run from the repository root: python analysis.py
import pandas as pd

# Load the original county returns.
raw_data = pd.read_csv('Lab2/countypres_2000-2024.csv')

print('DATASET EXPLORATION')
print('Rows and columns:', raw_data.shape)
print('Columns:', ', '.join(raw_data.columns))
print('Analytical outcome: Democratic minus Republican two-party vote margin')
print('Election years:', sorted(raw_data['year'].unique()))
print('States and DC:', raw_data['state'].nunique())

# Use only Democratic and Republican TOTAL records. Other modes are ignored.
filter_rows = raw_data['party'].isin(['REPUBLICAN', 'DEMOCRAT']) & (raw_data['mode'] == 'TOTAL')
voter_data = raw_data[filter_rows]
print('\nFILTERED DATA')
print('Democratic/Republican TOTAL records:', len(voter_data))
print('Candidate votes per TOTAL record:')
print(voter_data['candidatevotes'].describe().to_string())

# Group county records using the original nested dictionary.
groupedData = {}
for index, row in voter_data.iterrows():
    year = row['year']
    state = row['state']
    party = row['party']
    county = row['county_name']
    votes = row['candidatevotes']
    if year not in groupedData:
        groupedData[year] = {}
    if state not in groupedData[year]:
        groupedData[year][state] = {}
    if party not in groupedData[year][state]:
        groupedData[year][state][party] = {'total': 0, 'counties': {}}
    if county not in groupedData[year][state][party]['counties']:
        groupedData[year][state][party]['counties'][county] = 0
    groupedData[year][state][party]['counties'][county] += votes
    groupedData[year][state][party]['total'] += votes

# Calculate shares and signed margins for each available state and election year.
def calculate_shares(democratic, republican):
    total = democratic + republican
    if total == 0:
        return None
    dem_share = democratic / total * 100
    rep_share = republican / total * 100
    return {'democratic_votes': democratic, 'republican_votes': republican,
            'two_party_total': total, 'democratic_share': dem_share,
            'republican_share': rep_share, 'margin': dem_share - rep_share}

# Compare only localities where TOTAL records exist for both parties.
state_results = {}
for year in sorted(groupedData):
    state_results[year] = {}
    for state in sorted(groupedData[year]):
        parties = groupedData[year][state]
        if 'DEMOCRAT' not in parties or 'REPUBLICAN' not in parties:
            continue
        democrats = parties['DEMOCRAT']['counties']
        republicans = parties['REPUBLICAN']['counties']
        common_counties = set(democrats) & set(republicans)
        if not common_counties:
            continue
        dem_total = 0
        rep_total = 0
        for county in common_counties:
            dem_total += democrats[county]
            rep_total += republicans[county]
        result = calculate_shares(dem_total, rep_total)
        if result is None:
            continue
        result['county_count'] = len(common_counties)
        state_results[year][state] = result

print('State/DC counts with paired TOTAL records by year (not a completeness guarantee):')
for year in sorted(state_results):
    print(year, len(state_results[year]))
print('Selected examples (D votes, R votes, margin):')
for year, state in [(2020, 'VIRGINIA'), (2020, 'PENNSYLVANIA'), (2024, 'WISCONSIN')]:
    result = state_results.get(year, {}).get(state)
    if result is None:
        print(year, state, 'unavailable under TOTAL-only filter')
    else:
        print(year, state, int(result['democratic_votes']), int(result['republican_votes']),
              round(result['margin'], 2), 'percentage points,', result['county_count'], 'localities')
