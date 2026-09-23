# Hands-On Session Schedule

The hands-on session lasts about **3 hours**. Times are given relative to the start of the session; the instructor announces the actual start time on the day. Break timing may be adjusted.

The morning lectures (process design, TEA fundamentals, OpenPyTEA design and capabilities) are not part of this repository. The session assumes you have heard them, but every notebook restates the concepts it needs.

## Before the session

Complete:
- [INSTRUCTIONS.md](INSTRUCTIONS.md)
- [notebooks/00_setup_check.ipynb](notebooks/00_setup_check.ipynb)
- Optionally, the [reading material](READING_MATERIAL.md)

## How to open the notebooks

- Open a terminal in the repository root.
- Activate the environment:

```bash
# venv/pip route on macOS or Linux
source .venv-openpytea/bin/activate

# venv/pip route on Windows PowerShell
.\.venv-openpytea\Scripts\Activate.ps1

# conda route
conda activate openpytea-ws
```

- Start Jupyter Lab and open the notebook we are working on from the `notebooks/` folder:

```bash
jupyter lab
```

Alternatively, open the notebook in Google Colab via the badge at the top of each notebook.

## Session plan

### 0:00 - 0:15 Welcome and setup check
Roadmap of the session, troubleshooting of installations, a five-minute tour of the notebook layout.
- [00_setup_check.ipynb](notebooks/00_setup_check.ipynb)

### 0:15 - 0:40 Equipment costing
Cost correlations, inflation adjustment with CEPCI, material and installation factors, vendor quotes, composite equipment.
- [01_equipment_costing.ipynb](notebooks/01_equipment_costing.ipynb)

### 0:40 - 1:15 Building a plant
Plant configuration, fixed capital investment, fixed and variable OPEX, revenue, cash flow, NPV, IRR, ROI, payback time, levelized cost.
- [02_building_a_plant.ipynb](notebooks/02_building_a_plant.ipynb)

### 1:15 - 1:25 Break

### 1:25 - 1:55 Cost breakdowns, cash-flow diagrams, and sensitivity
The data-plus-plot pattern, stacked-bar breakdowns, cumulative cash-flow diagram, one-way sensitivity curves, tornado plots.
- [03_cost_breakdowns_and_sensitivity.ipynb](notebooks/03_cost_breakdowns_and_sensitivity.ipynb)

### 1:55 - 2:20 Monte Carlo uncertainty analysis
Uncertainty distributions on prices, quantities, and project-level factors; running and interpreting a Monte Carlo simulation; comparing plants under uncertainty.
- [04_monte_carlo_uncertainty.ipynb](notebooks/04_monte_carlo_uncertainty.ipynb)

### 2:20 - 2:55 Capstone case study
Steam methane reforming versus water electrolysis for hydrogen production: build both plants from simulation results, compare cost structures, run sensitivity and Monte Carlo, and draw a conclusion.
- [05_case_study_hydrogen.ipynb](notebooks/05_case_study_hydrogen.ipynb)

### 2:55 - 3:00 Wrap-up
Where to find help, how to contribute cost correlations, the optional [home assignment](HOME_ASSIGNMENT.md).

### Optional, if time allows or for self-study
The JSON configuration workflow and the `openpytea` command-line interface for reproducible, script-free studies.
- [06_optional_json_and_cli.ipynb](notebooks/06_optional_json_and_cli.ipynb)
