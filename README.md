# Swing or Shift?

**Project member:** Shamir Tyner (individual project, instructor approved).

**Dataset:** County Presidential Election Returns, 2000–2024, MIT Election Data + Science Lab / Harvard Dataverse: https://doi.org/10.7910/DVN/VOQCHQ. The CSV is in `Lab2/`.

**Research question:** Are swing states really swinging, or are they shifting? More precisely, do competitive presidential states show repeated election-to-election partisan swings or longer-term directional shifts in their two-party margins from 2000–2024?

**Progress:** The program selects Democratic and Republican records with `mode == TOTAL`, adds the available county votes into state totals, and calculates a two-party margin for every available state and election year. Positive margins favor Democrats; negative margins favor Republicans. Missing or incomplete county records can make a state-year unavailable or partial.

## Run

From the repository root, run `python -m pip install -r requirements.txt`, then `python analysis.py`. The program stores margins by year and state in the `state_margins` dictionary while it runs. A value of `None` means no usable TOTAL records were available. Uncomment the final print statement in `analysis.py` to see an example. Other voting modes and parties are excluded.

The TOTAL-only filter leaves some states unavailable in certain years, including Virginia in 2020 and Wisconsin in 2024. Some other state-year results may contain only a subset of localities. The presence of a state in the output does not establish complete coverage.

The five numbered files preserve the original exploratory script in consecutive sections; they are not standalone programs. `analysis.py` continues that code as the runnable Lab 2 analysis.

## Next Steps for Final Project

- **Working:** Data loading, filtering, state vote totals, and two-party margins.
- **Needs work:** Assess which state-year results have sufficient TOTAL-record coverage.
- **Plan:** Compare more competitive states and refine the interpretation of movement over time.
