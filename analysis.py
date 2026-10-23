# Swing or Shift? Shamir Tyner, CSCI 6201 Lab 2
# Run from the repository root: python analysis.py
import pandas as pd

# Load the original county returns. Keep FIPS codes as text, including leading zeros.
raw_data = pd.read_csv('Lab2/countypres_2000-2024.csv', dtype={'county_fips': str})

# Identify a county or county-equivalent. Some special records have no FIPS code.
def county_key(row):
    if pd.notna(row['county_fips']):
        return row['county_fips']
    return 'NO FIPS: ' + row['county_name']

print('DATASET EXPLORATION')
print('Rows and columns:', raw_data.shape)
print('Number of samples (records):', len(raw_data))
print('Number of columns:', len(raw_data.columns))
print('Columns:', ', '.join(raw_data.columns))
print('Analytical outcome: Democratic minus Republican two-party vote margin')
print('Model type: regression')
print('Election years:', sorted(raw_data['year'].unique()))
print('States and DC:', raw_data['state'].nunique())
print('Party values:', ', '.join(sorted(raw_data['party'].dropna().unique())))
print('Voting mode values:', ', '.join(sorted(raw_data['mode'].dropna().unique())))

# Preserve the original party and TOTAL-mode filters.
filter_rows = (raw_data['party'].isin(['REPUBLICAN', 'DEMOCRAT'])) & (raw_data['mode'] == 'TOTAL')
voter_data = raw_data[filter_rows]
print('\nFILTERED DATA')
print('Democratic/Republican TOTAL records:', len(voter_data))
used_columns = ['year', 'state', 'county_name', 'county_fips', 'party', 'mode', 'candidatevotes']
print('Missing values in used fields:')
print(voter_data[used_columns].isna().sum().to_string())
print('Candidate votes per filtered record:')
print(voter_data['candidatevotes'].describe().to_string())

# Track all party/locality records, including non-TOTAL modes, to identify gaps.
all_counties = {}
for index, row in raw_data[raw_data['party'].isin(['DEMOCRAT', 'REPUBLICAN'])].iterrows():
    key = (row['year'], row['state'])
    if key not in all_counties:
        all_counties[key] = set()
    all_counties[key].add((row['party'], county_key(row)))

# Continue the original nested-dictionary loop. The county FIPS code distinguishes
# places with the same name, such as Fairfax County and Fairfax city in Virginia.
groupedData = {}
for index, row in voter_data.iterrows():
    party = row['party']
    state = row['state']
    county = county_key(row)
    year = row['year']
    votes = row['candidatevotes']
    if pd.isna(votes) or pd.isna(year) or pd.isna(state) or pd.isna(row['county_name']):
        raise ValueError('A required filtered field is missing')
    if year not in groupedData:
        groupedData[year] = {}
    if state not in groupedData[year]:
        groupedData[year][state] = {}
    if party not in groupedData[year][state]:
        groupedData[year][state][party] = {'total': 0, 'counties': {}}
    if county in groupedData[year][state][party]['counties']:
        raise ValueError('Duplicate TOTAL record for: ' + str((year, state, party, county)))
    groupedData[year][state][party]['counties'][county] = votes
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

state_results = {}
incomplete = []
for year, state in sorted(all_counties):
    if year not in state_results:
        state_results[year] = {}
    if year not in groupedData or state not in groupedData[year]:
        incomplete.append((year, state, 'no TOTAL records'))
        continue
    parties = groupedData[year][state]
    total_counties = set()
    for party in parties:
        for county in parties[party]['counties']:
            total_counties.add((party, county))
        assert sum(parties[party]['counties'].values()) == parties[party]['total']
    missing_count = len(all_counties[(year, state)] - total_counties)
    if missing_count:
        incomplete.append((year, state, str(missing_count) + ' party/locality records without TOTAL'))
    if 'DEMOCRAT' not in parties or 'REPUBLICAN' not in parties:
        continue
    result = calculate_shares(parties['DEMOCRAT']['total'], parties['REPUBLICAN']['total'])
    if result is None:
        continue
    result['complete_total_coverage'] = missing_count == 0
    state_results[year][state] = result
    assert abs(result['democratic_share'] + result['republican_share'] - 100) < 0.000001
    assert (result['margin'] > 0) == (result['democratic_votes'] > result['republican_votes'])
    assert (result['margin'] < 0) == (result['democratic_votes'] < result['republican_votes'])

# Straightforward checks of filters, duplicate handling, sums, and coverage.
assert set(voter_data['party'].unique()) == {'DEMOCRAT', 'REPUBLICAN'}
assert set(voter_data['mode'].unique()) == {'TOTAL'}
assert len(groupedData) > 1
assert calculate_shares(60, 40)['margin'] > 0
assert calculate_shares(40, 60)['margin'] < 0
print('\nVALIDATION: filters, unique locality records, county sums, shares, and margin signs passed.')
print('Year coverage (states/DC with TOTAL records):')
for year in sorted(groupedData):
    print(year, len(groupedData[year]))
print('State-years with incomplete or absent TOTAL coverage:', len(incomplete))
for year, state, reason in incomplete:
    print(year, state, '-', reason)
print('\nSELECTED EXAMPLES (D votes, R votes, two-party margin)')
for year, state in [(2000, 'VIRGINIA'), (2024, 'VIRGINIA'), (2020, 'PENNSYLVANIA'), (2024, 'WISCONSIN')]:
    result = state_results.get(year, {}).get(state)
    if result is None:
        print(year, state, 'unavailable under TOTAL-only filter')
    else:
        print(year, state, int(result['democratic_votes']), int(result['republican_votes']),
              round(result['margin'], 2), 'percentage points;',
              'complete coverage:', result['complete_total_coverage'])

# Initial visualizations: use two competitive states with complete TOTAL coverage.
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

years = sorted(state_results)
selected_states = ['PENNSYLVANIA', 'MICHIGAN']
state_margins = {}
for state in selected_states:
    state_margins[state] = []
    for year in years:
        result = state_results[year].get(state)
        if result is None or not result['complete_total_coverage']:
            raise ValueError('Incomplete TOTAL coverage for ' + state + ' ' + str(year))
        state_margins[state].append(result['margin'])

figures = Path('figures')
figures.mkdir(exist_ok=True)
plt.figure(figsize=(9, 5))
for state in selected_states:
    plt.plot(years, state_margins[state], marker='o', label=state.title())
plt.axhline(0, color='gray', linewidth=1)
plt.title('Two-party presidential vote margin by state')
plt.xlabel('Election year')
plt.ylabel('Democratic minus Republican margin (percentage points)')
plt.xticks(years)
plt.legend()
plt.tight_layout()
plt.savefig(figures / '01_state_margins.png', dpi=150)
plt.close()

plt.figure(figsize=(9, 5))
for state in selected_states:
    changes = []
    for index in range(1, len(years)):
        changes.append(state_margins[state][index] - state_margins[state][index - 1])
    plt.plot(years[1:], changes, marker='o', label=state.title())
plt.axhline(0, color='gray', linewidth=1)
plt.title('Election-to-election change in two-party margin')
plt.xlabel('Election year (compared with previous election)')
plt.ylabel('Change in margin (percentage points)')
plt.xticks(years[1:])
plt.legend()
plt.tight_layout()
plt.savefig(figures / '02_margin_changes.png', dpi=150)
plt.close()

# Basic regression: learn Pennsylvania's earlier trend and check later elections.
# X is election year; y is the Democratic-minus-Republican two-party margin.
X = []
y = []
for index in range(len(years)):
    X.append([years[index]])
    y.append(state_margins['PENNSYLVANIA'][index])
X_train, X_test = X[:5], X[5:]
y_train, y_test = y[:5], y[5:]
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
error = mean_absolute_error(y_test, predictions)
results = Path('results')
results.mkdir(exist_ok=True)
report = 'Pennsylvania linear regression demonstration\n'
report += 'X: election year; y: Democratic-minus-Republican two-party margin (percentage points)\n'
report += 'Training elections: 2000–2016; test elections: 2020 and 2024\n'
for index in range(len(X_test)):
    report += str(X_test[index][0]) + ': actual ' + format(y_test[index], '.2f')
    report += ', predicted ' + format(predictions[index], '.2f') + ' percentage points\n'
report += 'Test mean absolute error: ' + format(error, '.2f') + ' percentage points\n'
report += 'Only two test elections: this is a preliminary exercise, not a forecast.\n'
(results / 'preliminary_results.txt').write_text(report, encoding='utf-8')
print('\n' + report)
print('Saved two figures in figures/.')
