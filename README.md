# Open-Science Techno-Economic Assessment with OpenPyTEA

<p align="center">
  <img src="_images/delft_during_fall.webp" alt="Canal in Delft during fall" width="800"/>
</p>
<p align="center"><sub>Delft in autumn. Image source: <a href="https://www.leshuttle.com/uk-en/discover/traveller-guides/delft-the-hidden-gem-of-the-netherlands">LeShuttle, "Delft: the hidden gem of the Netherlands"</a>.</sub></p>

## Overview

Welcome! This repository holds all material of the one-day workshop **Open-Science Techno-Economic Assessment with OpenPyTEA: From Process Design to Economic Insights**: lecture and industry-talk slides (uploaded after the workshop), notes from the community discussion, and the core **hands-on session with OpenPyTEA**.

The hands-on session (11:45 - 12:30 and 13:30 - 14:45, two hours in total) opens with a short presentation on why we built OpenPyTEA. You then build a complete techno-economic assessment (TEA) in Python with the open-source [OpenPyTEA](https://github.com/pbtamarona/OpenPyTEA) toolkit, in six exercises:

- Equipment cost estimation from cost correlations and vendor quotes
- Plant-level CAPEX, OPEX, cash flow, and profitability metrics (NPV, IRR, ROI, payback time, levelized cost)
- Cost breakdowns, cash-flow diagrams, sensitivity and tornado analysis
- Monte Carlo uncertainty propagation
- A capstone case study comparing two hydrogen production pathways
- The JSON configuration workflow and command-line interface, and a demonstration of the OpenPyTEA graphical user interface

Each exercise is one Jupyter notebook with a short demo, core tasks, bonus tasks for fast participants, and solutions. All material stays available after the workshop.

## Quick Links

- [INSTRUCTIONS.md](INSTRUCTIONS.md): pre-workshop installation steps (15 minutes, please do this before you arrive)
- [SCHEDULE.md](SCHEDULE.md): the full-day program and the detailed agenda of the hands-on session
- [slides/](slides/README.md): slides of all talks, added during and after the workshop
- [discussion/](discussion/README.md): agenda and outcomes of the community discussion on shared TEA standards
- [READING_MATERIAL.md](READING_MATERIAL.md): optional background reading
- [HOME_ASSIGNMENT.md](HOME_ASSIGNMENT.md): optional post-workshop assignment
- [OpenPyTEA documentation](https://openpytea.readthedocs.io)

## Learning Outcomes

By the end of the session, you will be able to:

- Explain how OpenPyTEA turns process-simulation results into a TEA (equipment, plant, analysis, plotting).
- Estimate purchased and installed equipment costs, including inflation adjustment and material and installation factors.
- Configure a `Plant` with financial assumptions, products, and variable OPEX inputs, and compute CAPEX, OPEX, NPV, IRR, and levelized cost.
- Produce and interpret cost-breakdown charts, cash-flow diagrams, sensitivity curves, and tornado plots.
- Define uncertainty distributions and run a Monte Carlo simulation.
- Compare technology alternatives in a consistent, reproducible way.

## Target Audience

- Students, researchers, and engineers in chemical, energy, and sustainability sciences.
- Basic Python skills (variables, lists, dictionaries, functions) are sufficient. No prior OpenPyTEA experience is required.
- Familiarity with basic process-design and cost-engineering concepts (CAPEX, OPEX, NPV) helps but is not required; the morning lectures cover the fundamentals.

---
**NOTE**

If you are completely new to Python, we recommend spending one or two hours on a beginner tutorial before the workshop, for example the University of Helsinki online course (no installation needed):
- https://programming-25.mooc.fi/part-1/1-getting-started

---

## Repository Structure

- [notebooks/](notebooks/README.md): the workshop notebooks; the exercise number is the notebook number
  - `00_setup_check.ipynb`: run before the workshop to verify your installation
  - `01_equipment_costing.ipynb`: Exercise 1, equipment cost estimation
  - `02_building_a_plant.ipynb`: Exercise 2, plant configuration, CAPEX, OPEX, and profitability metrics
  - `03_cost_breakdowns_and_sensitivity.ipynb`: Exercise 3, breakdown charts, cash flow, sensitivity, and tornado plots
  - `04_monte_carlo_uncertainty.ipynb`: Exercise 4, uncertainty distributions and Monte Carlo simulation
  - `05_case_study_hydrogen.ipynb`: Exercise 5, capstone, steam methane reforming vs. water electrolysis
  - `06_json_and_cli.ipynb`: Exercise 6, the JSON configuration workflow and command-line interface
  - `assets/`: JSON configuration files used in Exercise 6
- `envs/`: environment files (`requirements.txt` for pip/venv, `environment.yml` for conda)
- [slides/](slides/README.md): slides of the lectures, the hands-on introduction, and the industry talk
- [discussion/](discussion/README.md): agenda, notes, and outcomes of the community discussion
- `_images/`: figures used in the README and notebooks

## Recommended Workflow

Before the workshop:
1. Follow [INSTRUCTIONS.md](INSTRUCTIONS.md) to install Python, OpenPyTEA, and Jupyter Lab.
2. Run `notebooks/00_setup_check.ipynb` and check that every cell passes.
3. Optional: skim the [reading material](READING_MATERIAL.md).

During the session:

4. Work through Exercises 1 to 6 in order. Start with the core tasks; do the bonus tasks if you are ahead.
5. Each notebook is self-contained: it starts by rebuilding what it needs from the previous notebook, so you can restart the kernel or skip ahead without losing anything.

No data download is needed. Everything used in the session is either bundled in this repository or shipped with the `openpytea` package.

## No Installation? Use Google Colab

Every notebook can also be opened in Google Colab, where the first cell installs OpenPyTEA for you. Use the **Open in Colab** badge at the top of each notebook, or open a notebook directly from https://colab.research.google.com/github/pbtamarona/openpytea-workshop/. A local installation is still recommended so that you know how to set up and use OpenPyTEA after the workshop.

## Software

OpenPyTEA is a pure-Python package available on PyPI and requires Python 3.10 or newer:

```bash
pip install openpytea
```

The workshop environment adds Jupyter Lab. See [INSTRUCTIONS.md](INSTRUCTIONS.md) for the complete commands and the environment files in `envs/`.

## Workshop Information

- **Date:** Friday, November 6, 2026, 09:30 to 18:00
- **Hands-on session:** 11:45 - 12:30 and 13:30 - 14:45
- **Location:** Lecture Hall B - Isaac Newton, Faculty of Mechanical Engineering, TU Delft (see [Venue and Directions](#venue-and-directions))
- **Bring:** your own laptop, with the software from [INSTRUCTIONS.md](INSTRUCTIONS.md) installed
<!-- - **Registration:** [aanmelder.nl/openpytea2026](https://aanmelder.nl/openpytea2026) (closes October 15, 2026) -->
- **Package repository:** https://github.com/pbtamarona/OpenPyTEA
- **Documentation:** https://openpytea.readthedocs.io

<!-- <p align="center">
  <img src="_images/workshop-flyer.jpg" alt="Open-Science Techno-Economic Assessment with OpenPyTEA" width="700"/>
</p> -->

## Venue and Directions

The workshop takes place in **[Lecture Hall B - Isaac Newton](https://esviewer.tudelft.nl/space/6/)** (room 34.A-0-720, ground floor, 167 seats) in the building of the **[Faculty of Mechanical Engineering](https://www.tudelftcampus.nl/nl/poi/mechanical-engineering-me)** (building 34) on the TU Delft campus.

- **Address:** Mekelweg 2, 2628 CD Delft, The Netherlands
- **Google Maps:** [Faculty of Mechanical Engineering, Mekelweg 2](https://www.google.com/maps/search/?api=1&query=TU+Delft+Faculty+of+Mechanical+Engineering+Mekelweg+2+2628+CD+Delft)
- **Landmark:** the building is directly opposite the Aula Conference Centre. Signs at the main entrance point you to the lecture halls.

### By public transport from Delft Station

1. Walk out of the station hall on the city-centre side to the bus platforms in front of the station.
2. Take **bus 69** (direction TU Campus) or **bus 40** (direction Rotterdam Centraal). Buses 174 and 455 also stop at the campus.
3. Get off at **Aula TU** after about 7 to 10 minutes.
4. Cross Mekelweg: the Mechanical Engineering building is across the road from the Aula. Lecture Hall B is on the ground floor.

**Tram 19** is scheduled to open its new route from Delft Station to the TU Delft campus in the second half of 2026. If it is running by November, it is an alternative to the bus.

Check the live timetable in the [9292 journey planner](https://9292.nl/en) (search for "Delft, Aula TU") and pay with a contactless bank card or an OV-chipkaart. The trip also takes about 25 minutes on foot or 10 minutes by bicycle.

## Organizers and lecturers
- [Panji B. Tamarona](mailto:P.B.Tamarona@tudelft.nl), TU Delft (contact person)
- Mahinder Ramdin, TU Delft
- Thijs J.H. Vlugt, TU Delft
- Artur M. Schweidtmann, TU Delft
- Arnoud Higler, Shell

## Graphical User Interface

The session closes with a demonstration of the OpenPyTEA GUI, which runs the same workflow without writing code. It is still in development and does not yet offer every feature of the Python package. Installers for Windows and macOS are on the [OpenPyTEA releases page](https://github.com/pbtamarona/OpenPyTEA/releases).

## Citing OpenPyTEA

If you use OpenPyTEA in your work, please cite:

> Tamarona, P.B., Vlugt, T.J.H., & Ramdin, M. (2026). *OpenPyTEA: An open-source python toolkit for techno-economic assessment of chemical process plants and energy systems with economic sensitivity and uncertainty evaluation.* SoftwareX, 35, 102816. https://doi.org/10.1016/j.softx.2026.102816

## License

The material in this repository is licensed under the MIT License. See [LICENSE](LICENSE).
