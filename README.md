# Swing or Shift?

**Project member:** Shamir Tyner (individual project, instructor approved).

**Dataset:** County Presidential Election Returns, 2000–2024, MIT Election Data + Science Lab / Harvard Dataverse: https://doi.org/10.7910/DVN/VOQCHQ. The CSV is in `Lab2/`.

**Research question:** Are swing states really swinging, or are they shifting? More precisely, do competitive presidential states show repeated election-to-election partisan swings or longer-term directional shifts in their two-party margins from 2000–2024?

**Model type:** Regression. A simple Pennsylvania linear regression uses election year as X and the Democratic-minus-Republican two-party margin as y. The model fits 2000–2016 and tests on 2020 and 2024. Its mean absolute error is 2.16 percentage points on those two elections; this is a small preliminary exercise, not an election forecast. See `results/preliminary_results.txt`.

**Progress:** The program explores and filters the data, groups votes by state, year, and locality, calculates two-party shares and margins, checks the results, creates two figures, and evaluates a basic model. For each locality and party, the program uses a TOTAL row when available; otherwise it sums the reported mode records. This restores records absent from a TOTAL-only filter. All 50 states and DC appear in each election year; selected totals have been checked against published state or FEC results. Coverage does not independently prove that every locality or mode is complete.

## Run

From the repository root, run `python -m pip install -r requirements.txt`, then `python analysis.py`. The script uses the repository-relative CSV path and saves figures and results. It stores results in `state_results` and locality records in `groupedData` during the run. A locality is identified by its FIPS code and name where available; records without FIPS use their locality name. The program keeps the TOTAL row when present so it is not added to its component modes. When TOTAL is absent, it adds the mode records; some 2024 records have no mode label. North Carolina has multiple unlabeled rows per locality, which are added together and checked against statewide results.

Validation references: [Virginia 2020 official audit results](https://www.elections.virginia.gov/rla-results_nov-3-2020/), [FEC 2024 official results](https://www.fec.gov/documents/5644/2024presgeresults.pdf), and [Pennsylvania 2020 results](https://www.presidency.ucsb.edu/statistics/elections/2020). MIT warns that combining TOTAL and component modes can double-count votes in its [election-data documentation](https://github.com/MEDSL/2024-elections-official#usage).

The five numbered files preserve the original exploratory script in consecutive sections; they are not standalone programs. `analysis.py` continues that code as the runnable Lab 2 analysis.

## Initial visualizations

- `figures/01_state_margins.png` shows Pennsylvania and Michigan's two-party margins over seven elections. Both crossed from a Democratic advantage in 2012 to a Republican advantage in 2016, then switched direction again in 2020 and 2024.
- `figures/02_margin_changes.png` shows each election's change from the preceding election. Both states moved toward the Democrats in 2008 and 2020 and toward the Republicans in 2012, 2016, and 2024.

Positive margin or change means a Democratic advantage or movement toward Democrats; negative values mean a Republican advantage or movement toward Republicans. These two selected states do not establish a pattern for every swing state.

## Next Steps for Final Project

- **Working:** Data loading, filtering, locality grouping, two-party calculations, validation, two plots, and a preliminary regression.
- **Needs work:** Check more reconstructed state totals against official sources and improve the small model evaluation.
- **Plan:** Compare more competitive states and refine the interpretation of movement over time.
- **Instructor feedback:** None requested at this time.
