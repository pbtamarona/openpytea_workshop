# Workshop notebooks

The topics covered in each notebook of the hands-on session. Notebooks 01 to 06 will be uploaded on October 30, one week before the workshop.

| Notebook | Topics | Available |
|---|---|---|
| `00_setup_check.ipynb` | Checks the Python version, the OpenPyTEA installation, the notebook extras, and the working folder | Now |
| `01_equipment_costing.ipynb` | Cost correlations, CEPCI, installation factors, vendor quotes, composite equipment | From October 30 |
| `02_building_a_plant.ipynb` | Plant configuration, FCI, OPEX, revenue, cash flow, NPV, IRR, ROI, payback, levelized cost | From October 30 |
| `03_cost_breakdowns_and_sensitivity.ipynb` | Breakdown charts, cash-flow diagram, one-way sensitivity, tornado plots | From October 30 |
| `04_monte_carlo_uncertainty.ipynb` | Uncertainty distributions, Monte Carlo, comparing plants, parameter dependencies | From October 30 |
| `05_case_study_hydrogen.ipynb` | Capstone: steam methane reforming vs. water electrolysis, CO₂ tax break-even, Monte Carlo comparison | From October 30 |
| `06_json_and_cli.ipynb` | JSON configuration files, loading plants from JSON, the `openpytea` command-line interface, scenario files | From October 30 |

## How the notebooks are organised

Task cells start with `# YOUR CODE HERE`. Solutions are not included in this repository; they are in the printed handouts you receive at the workshop.

## Files

- `assets/smr_hydrogen.json`: combined OpenPyTEA configuration of the steam methane reforming plant (Exercise 6)
- `assets/we_hydrogen.json`: combined configuration of the water electrolysis plant (Exercise 6)

On Google Colab, Exercise 6 downloads these files automatically when they are not present. Exercises 3 and 6 write files to the current folder and to `outputs/`.
