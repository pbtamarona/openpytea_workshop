# Home Assignment (Optional)

Participants who want to go further can complete a short assignment after the workshop.
Panji B. Tamarona will read every submission and send back feedback.

## Goal

Perform a small, reproducible techno-economic assessment with OpenPyTEA of a process you care about.

## Expected workload

- Target effort: **3 to 6 hours**.

## Requirements

1. Use at least three of the concepts covered in the session: equipment costing, plant configuration, cost breakdowns, cash-flow analysis, sensitivity or tornado analysis, Monte Carlo uncertainty analysis, comparison of alternatives, or the JSON/CLI workflow.
2. Share the work as a **repository** (GitHub, GitLab, or similar) or as a single notebook, and send us the link.
3. Others must be able to reproduce your results: include the notebook or script and any input files.
4. Include a short `README` (or an introductory cell) explaining:
   - the process and the question you are asking,
   - where the process data come from (simulation, literature, your own measurements),
   - how to run the code,
   - the main result in two or three sentences.

## Recommended scope

Preferably, apply OpenPyTEA to a process from your own research, studies, or professional work. If you do not have one at hand, pick one of these:

- Extend the capstone case study with a third hydrogen pathway (for example methane pyrolysis, see `examples/case_study_1.ipynb` in the OpenPyTEA repository).
- Re-implement a published TEA from the literature and compare your levelized cost with the published one.
- Take the geothermal case study (`examples/case_study_3.ipynb` in the OpenPyTEA repository) and test how the conclusion changes with your own country's electricity price and location factor.

## Contributing back

If you find a cost correlation that is missing from OpenPyTEA, or you build one for your equipment, consider opening a pull request to add it to `cost_correlations.csv`. The contributing guide is at https://openpytea.readthedocs.io.

## Submission

Send the link to `P.B.Tamarona@tudelft.nl` with the subject line `OpenPyTEA workshop assignment`.
