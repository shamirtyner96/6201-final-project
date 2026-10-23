# Swing or Shift?

**Project member:** Shamir Tyner (individual project, instructor approved).

**Dataset:** County Presidential Election Returns, 2000–2024, MIT Election Data + Science Lab / Harvard Dataverse: https://doi.org/10.7910/DVN/VOQCHQ. The CSV is in `Lab2/`.

**Research question:** Are swing states really swinging, or are they shifting? More precisely, do competitive presidential states show repeated election-to-election partisan swings or longer-term directional shifts in their two-party margins from 2000–2024?

**Progress:** The program selects only Democratic and Republican records with `mode == TOTAL`, groups votes by state, year, and locality, and calculates two-party shares and margins. A locality is included in a state's comparison only when both parties have a TOTAL record. Missing or unpaired records are omitted; results may therefore be partial and should not automatically be treated as complete statewide totals.

## Run

From the repository root, run `python -m pip install -r requirements.txt`, then `python analysis.py`. The script uses the repository-relative CSV path. It stores locality records in `groupedData` and state-year results in `state_results` during the run. Localities are grouped by `county_name` within each state and year. Records with the same name in the same state and year are combined; this may merge a county and an independent city that share a name. Other voting modes and parties are excluded.

The TOTAL-only filter leaves some states unavailable in certain years, including Virginia in 2020 and Wisconsin in 2024. Some other state-year results may contain only a subset of localities. The presence of a state in the output does not establish complete coverage.

The five numbered files preserve the original exploratory script in consecutive sections; they are not standalone programs. `analysis.py` continues that code as the runnable Lab 2 analysis.

## Next Steps for Final Project

- **Working:** Data loading, filtering, locality grouping, and two-party calculations.
- **Needs work:** Assess which state-year results have sufficient TOTAL-record coverage.
- **Plan:** Compare more competitive states and refine the interpretation of movement over time.
- **Instructor feedback:** None requested at this time.
