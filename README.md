# Swing or Shift?

**Project member:** Shamir Tyner 

**Dataset:** County Presidential Election Returns, 2000–2024, MIT Election Data + Science Lab / Harvard Dataverse: https://doi.org/10.7910/DVN/VOQCHQ. The CSV is in `Lab2/`.

**Research question:** Are swing states really swinging, or are they shifting? More precisely, do competitive presidential states show repeated election-to-election partisan swings or longer-term directional shifts in their two-party margins from 2000–2024?

**Planned problem type:** Regression. The two-party margin is a numerical value, so a simple regression could examine how a selected state?s margin changes over election years. The current analysis calculates margins; it does not yet train or evaluate a model.

**Progress:** The program selects Democratic and Republican records with `mode == TOTAL`, adds the available county votes into state totals, and calculates a two-party margin for every available state and election year. Positive margins favor Democrats; negative margins favor Republicans. Missing or incomplete county records can make a state-year unavailable or partial.

## Run

From the repository root, install pandas with `python -m pip install pandas` if needed, then run `python analysis.py`. The program stores margins by year and state in the `state_margins` dictionary while it runs.Other voting modes and parties are excluded.

The TOTAL-only filter leaves Virginia in 2020 and Wisconsin in 2024 unavailable due to data capture failures.

## Next Steps for Final Project

- [x] Load the election dataset.
- [x] Filter for Democratic and Republican TOTAL records.
- [x] Calculate state vote totals and two-party margins by election year.
- [x] Assess which state-year results have sufficient TOTAL-record coverage.
- [ ] Select competitive states to compare.
- [ ] Examine how their margins change from election to election.
- [ ] Create visualizations that help explain the results.
- [ ] Develop a basic model and evaluate its results.
- [ ] Prepare the final project report and presentation.
