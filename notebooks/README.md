# Workshop notebooks

Work through the notebooks in numerical order. Each one starts with a short setup cell that rebuilds what it needs
from the previous notebooks, so you can restart a kernel or skip ahead without losing anything. Timings are in
[SCHEDULE.md](../SCHEDULE.md).

| Notebook | Topic | Time |
|---|---|---|
| `00_setup_check.ipynb` | Verify the installation (run before the workshop) | 5 min |
| `01_equipment_costing.ipynb` | Cost correlations, CEPCI, installation factors, vendor quotes, composite equipment | 25 min |
| `02_building_a_plant.ipynb` | Plant configuration, FCI, OPEX, revenue, cash flow, NPV, IRR, ROI, payback, levelized cost | 35 min |
| `03_cost_breakdowns_and_sensitivity.ipynb` | Breakdown charts, cash-flow diagram, one-way sensitivity, tornado plots | 30 min |
| `04_monte_carlo_uncertainty.ipynb` | Uncertainty distributions, Monte Carlo, comparing plants, parameter dependencies | 25 min |
| `05_case_study_hydrogen.ipynb` | Capstone: steam methane reforming vs. water electrolysis | 35 min |
| `06_optional_json_and_cli.ipynb` | Optional: JSON configuration files and the command-line interface | 20 min |

## How the notebooks are organised

Every notebook follows the same pattern: title and learning goals, a short concept section, a worked demo, one or
more **exercises**, and a recap. Exercise cells start with `# YOUR CODE HERE`. In notebooks 01 to 04 and 06 the
solution is hidden in a collapsible **Solution** block right below the exercise. In the capstone (05) the solution
is an ordinary code cell, so that the notebook can always be run to the end.

## Running on Google Colab

Each notebook has an **Open in Colab** badge at the top. The first code cell installs OpenPyTEA if it is missing.
Notebook 06 downloads the JSON files in `assets/` automatically when they are not present.

## Assets

- `assets/smr_hydrogen.json`: combined OpenPyTEA configuration of the steam methane reforming plant (notebook 06)
- `assets/we_hydrogen.json`: combined configuration of the water electrolysis plant (notebook 06)

Notebooks 03 and 06 write files to the current folder and to `outputs/`; both are ignored by Git.
