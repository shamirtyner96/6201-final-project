# Swing or Shift? Visualizing Partisan Movement in U.S. Presidential Elections, 2000–2024

**Author:** Shamir Tyner

**Dataset:** U.S. county presidential election results, 2000–2024 (`Lab2/countypres_2000-2024.csv`).

**Problem type:** Exploratory analysis of voting trends; classification versus regression has not yet been specified.

**Research question:** Do swing states actually swing, or is there a longer-term directional shift in presidential voting?

**Current progress:** The initial code loads the dataset, filters for Democratic and Republican votes with total reporting mode, groups county votes by year, state, and party, and prints state totals. Calculations for vote shares and margins are present as comments. Visualization and further analysis remain to be developed. The original code notes that the counting loop needs further work.

## Code organization

The five numbered Python files contain consecutive sections of the original `swing_shift.py`, with no new Python code added. They share variables and are not standalone scripts: execute their contents in order in the same Python session, from the repository root, with pandas installed. The last file contains commented-out exploratory calculations.

1. `01_load_election_data.py` — project notes and data loading.
2. `02_filter_election_data.py` — filter parties and reporting mode.
3. `03_group_county_votes.py` — group and accumulate votes.
4. `04_print_state_totals.py` — inspect grouped data and print totals.
5. `05_explore_vote_shares.py` — commented-out vote share and margin calculations.
