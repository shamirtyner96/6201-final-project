# Swing or Shift? Shamir Tyner, CSCI 6201 Lab 2
# Run from the repository root: python analysis.py
import pandas as pd

# Load the original county returns. Keep FIPS codes as text, including leading zeros.
raw_data = pd.read_csv('Lab2/countypres_2000-2024.csv', dtype={'county_fips': str})

# Identify a county or county-equivalent. Some special records have no FIPS code.
def county_key(row):
    if pd.notna(row['county_fips']):
        return (row['county_fips'], row['county_name'])
    return ('NO FIPS', row['county_name'])

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

# Keep Democratic and Republican records. Some years report separate modes
# or leave the mode blank instead of providing a TOTAL row.
voter_data = raw_data[raw_data['party'].isin(['REPUBLICAN', 'DEMOCRAT'])]
print('\nFILTERED DATA')
print('Democratic/Republican records:', len(voter_data))
used_columns = ['year', 'state', 'county_name', 'county_fips', 'party', 'mode', 'candidatevotes']
print('Missing values in used fields:')
print(voter_data[used_columns].isna().sum().to_string())
print('Candidate votes per record (may represent one voting mode):')
print(voter_data['candidatevotes'].describe().to_string())

# Gather all records for each year, state, party, and locality.
# A TOTAL row takes precedence over the same locality's mode breakdowns.
locality_rows = {}
for index, row in voter_data.iterrows():
    year = row['year']
    state = row['state']
    party = row['party']
    county = county_key(row)
    votes = row['candidatevotes']
    mode = row['mode'] if pd.notna(row['mode']) else 'UNLABELED'
    if pd.isna(votes) or pd.isna(year) or pd.isna(state) or pd.isna(row['county_name']):
        raise ValueError('A required field is missing')
    key = (year, state, party, county)
    if key not in locality_rows:
        locality_rows[key] = []
    locality_rows[key].append((mode, votes))

# Continue the original nested-dictionary structure, keeping each locality.
groupedData = {}
reconstructed = 0
for key in locality_rows:
    year, state, party, county = key
    rows = locality_rows[key]
    total_rows = []
    modes_seen = set()
    for mode, votes in rows:
        if mode == 'TOTAL':
            total_rows.append(votes)
        # North Carolina 2024 has multiple unlabeled components per locality.
        # Their summed state totals are checked against published FEC results.
        elif mode in modes_seen and not any(item[0] == 'TOTAL' for item in rows) and not (year == 2024 and state == 'NORTH CAROLINA' and mode == 'UNLABELED'):
            raise ValueError('Repeated mode needs review: ' + str((key, mode)))
        modes_seen.add(mode)
    if len(total_rows) > 1:
        raise ValueError('Repeated TOTAL needs review: ' + str(key))
    if total_rows:
        votes = total_rows[0]
    else:
        votes = 0
        for mode, amount in rows:
            votes += amount
        reconstructed += 1
    if year not in groupedData:
        groupedData[year] = {}
    if state not in groupedData[year]:
        groupedData[year][state] = {}
    if party not in groupedData[year][state]:
        groupedData[year][state][party] = {'total': 0, 'counties': {}}
    groupedData[year][state][party]['counties'][county] = votes
    groupedData[year][state][party]['total'] += votes
print('Locality/party totals reconstructed without a TOTAL row:', reconstructed)

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
for year in sorted(groupedData):
    state_results[year] = {}
    for state in sorted(groupedData[year]):
        parties = groupedData[year][state]
        for party in parties:
            assert sum(parties[party]['counties'].values()) == parties[party]['total']
        if 'DEMOCRAT' not in parties or 'REPUBLICAN' not in parties:
            raise ValueError('Missing party for ' + state + ' ' + str(year))
        result = calculate_shares(parties['DEMOCRAT']['total'], parties['REPUBLICAN']['total'])
        if result is None:
            raise ValueError('Zero two-party votes for ' + state + ' ' + str(year))
        state_results[year][state] = result
        assert abs(result['democratic_share'] + result['republican_share'] - 100) < 0.000001
        assert (result['margin'] > 0) == (result['democratic_votes'] > result['republican_votes'])
        assert (result['margin'] < 0) == (result['democratic_votes'] < result['republican_votes'])

assert set(voter_data['party'].unique()) == {'DEMOCRAT', 'REPUBLICAN'}
assert len(groupedData) > 1
assert calculate_shares(60, 40)['margin'] > 0
assert calculate_shares(40, 60)['margin'] < 0
# Published statewide totals check labeled, unlabeled, and multiple-unlabeled modes.
checks = [(2020, 'VIRGINIA', 2413568, 1962430),
          (2020, 'PENNSYLVANIA', 3458229, 3377674),
          (2024, 'WISCONSIN', 1668229, 1697626),
          (2024, 'NORTH CAROLINA', 2715375, 2898423)]
print('\nVALIDATION: party filter, locality totals, shares, and margin signs passed.')
print('State/DC coverage by year:')
for year in sorted(groupedData):
    print(year, len(groupedData[year]))
print('Selected published state totals:')
for year, state, dem_expected, rep_expected in checks:
    result = state_results[year][state]
    assert result['democratic_votes'] == dem_expected
    assert result['republican_votes'] == rep_expected
    print(year, state, int(result['democratic_votes']), int(result['republican_votes']),
          'margin:', round(result['margin'], 2), 'percentage points')

# Initial visualizations: compare two competitive states.
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
        if result is None:
            raise ValueError('Missing results for ' + state + ' ' + str(year))
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
