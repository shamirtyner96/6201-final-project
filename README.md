# Swing or Shift?

**Project member:** Shamir Tyner (individual project, instructor approved).

**Dataset:** County Presidential Election Returns, 2000–2024, MIT Election Data + Science Lab / Harvard Dataverse: https://doi.org/10.7910/DVN/VOQCHQ. The CSV is in `Lab2/`.

**Research question:** Are swing states really swinging, or are they shifting? More precisely, do competitive presidential states show repeated election-to-election partisan swings or longer-term directional shifts in their two-party margins from 2000–2024?

**Model type:** Regression. A simple Pennsylvania linear regression uses election year as X and the Democratic-minus-Republican two-party margin as y. The model fits 2000–2016 and tests on 2020 and 2024. Its mean absolute error is 2.16 percentage points on those two elections; this is a small preliminary exercise, not an election forecast. See `results/preliminary_results.txt`.

**Progress:** The program selects only Democratic and Republican records with `mode == TOTAL`, groups votes by state, year, and locality, calculates two-party shares and margins, creates two figures, and evaluates a basic model. A locality is included in a state's comparison only when both parties have a TOTAL record. Missing or unpaired records are omitted; results may therefore be partial and should not automatically be treated as complete statewide totals.

## Run

From the repository root, run `python -m pip install -r requirements.txt`, then `python analysis.py`. The script uses the repository-relative CSV path and saves figures and results. It stores locality records in `groupedData` and state-year results in `state_results` during the run. Localities are identified by FIPS and name where available; records without FIPS use their locality name. Other voting modes and parties are excluded.

The TOTAL-only filter leaves some states unavailable in certain years, including Virginia in 2020 and Wisconsin in 2024. Some other state-year results may contain only a subset of localities. The presence of a state in the output does not establish complete coverage.

The five numbered files preserve the original exploratory script in consecutive sections; they are not standalone programs. `analysis.py` continues that code as the runnable Lab 2 analysis.

## Initial visualizations

- `figures/01_state_margins.png` shows Pennsylvania and Michigan's two-party margins over seven elections. Both crossed from a Democratic advantage in 2012 to a Republican advantage in 2016, then switched direction again in 2020 and 2024.
- `figures/02_margin_changes.png` shows each election's change from the preceding election. Both states moved toward the Democrats in 2008 and 2020 and toward the Republicans in 2012, 2016, and 2024.

Positive margin or change means a Democratic advantage or movement toward Democrats; negative values mean a Republican advantage or movement toward Republicans. These two selected states do not establish a pattern for every swing state.

## Next Steps for Final Project

- **Working:** Data loading, filtering, locality grouping, two-party calculations, validation, two plots, and a preliminary regression.
- **Needs work:** Assess which state-year results have sufficient TOTAL-record coverage and improve the small model evaluation.
- **Plan:** Compare more competitive states and refine the interpretation of movement over time.
- **Instructor feedback:** None requested at this time.
