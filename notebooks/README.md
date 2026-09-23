# Workshop notebooks

Each exercise of the hands-on session is one notebook, and the exercise number is the notebook number. Work through them in order. Each one starts with a short setup cell that rebuilds what it needs
from the previous notebooks, so you can restart a kernel or skip ahead without losing anything. Timings are in
[SCHEDULE.md](../SCHEDULE.md).

| Notebook | Exercise | Topic | Session time |
|---|---|---|---|
| `00_setup_check.ipynb` | Setup | Verify the installation (run at home before the workshop) | 5 min |
| `01_equipment_costing.ipynb` | 1 | Cost correlations, CEPCI, installation factors, vendor quotes, composite equipment | 12 min |
| `02_building_a_plant.ipynb` | 2 | Plant configuration, FCI, OPEX, revenue, cash flow, NPV, IRR, ROI, payback, levelized cost | 18 min |
| `03_cost_breakdowns_and_sensitivity.ipynb` | 3 | Breakdown charts, cash-flow diagram, one-way sensitivity, tornado plots | 15 min |
| `04_monte_carlo_uncertainty.ipynb` | 4 | Uncertainty distributions, Monte Carlo, comparing plants, parameter dependencies | 15 min |
| `05_case_study_hydrogen.ipynb` | 5 | Capstone: steam methane reforming vs. water electrolysis | 25 min |
| `06_json_and_cli.ipynb` | 6 | JSON configuration files and the command-line interface | 10 min |

## How the notebooks are organised

Every notebook follows the same pattern: title and learning goals, a short concept section, a worked demo, one or
more **tasks** numbered per exercise (Task 1.1, Task 1.2, ...), and a recap. Tasks marked **bonus** are for
participants who finish early. Task cells start with `# YOUR CODE HERE`. In Exercises 1 to 4 and 6 the solution is
hidden in a collapsible **Solution** block right below the task. In the capstone (Exercise 5) the solution is an
ordinary code cell, so that the notebook can always be run to the end.

## Running on Google Colab

Each notebook has an **Open in Colab** badge at the top. The first code cell installs OpenPyTEA if it is missing.
Exercise 6 downloads the JSON files in `assets/` automatically when they are not present.

## Assets

- `assets/smr_hydrogen.json`: combined OpenPyTEA configuration of the steam methane reforming plant (Exercise 6)
- `assets/we_hydrogen.json`: combined configuration of the water electrolysis plant (Exercise 6)

Exercises 3 and 6 write files to the current folder and to `outputs/`; both are ignored by Git.
