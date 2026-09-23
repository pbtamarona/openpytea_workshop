# Workshop Schedule

**Friday, November 6, 2026**, Lecture Hall B - Isaac Newton, Faculty of Mechanical Engineering, TU Delft
(directions in the [README](README.md#venue-and-directions)).

## Full-day program

The day combines lectures, the hands-on session, an industry perspective, and an open discussion.

| Time | Session |
|---|---|
| 09:30 - 09:55 | Welcome and coffee |
| 09:55 - 10:00 | Opening remarks |
| 10:00 - 10:45 | From Lab to Industry: Process Design |
| 10:45 - 11:30 | TEA Fundamentals: Theory and Practice |
| 11:30 - 11:45 | Coffee break |
| 11:45 - 12:30 | **Hands-on session with OpenPyTEA: Part 1** |
| 12:30 - 13:30 | Lunch |
| 13:30 - 14:45 | **Hands-on session with OpenPyTEA: Part 2** |
| 14:45 - 15:30 | Multi-Agent Systems for Process Design |
| 15:30 - 15:45 | Coffee break |
| 15:45 - 16:30 | Industry talk: feasibility assessment in practice (Shell) |
| 16:30 - 16:45 | Community discussion: shared standards for transparent and reproducible TEA |
| 16:45 - 18:00 | Closing, social drinks, and networking |

Slides of the talks go into [slides/](slides/README.md) after the workshop; the agenda and outcomes of the community discussion are in [discussion/](discussion/README.md). Everything stays online afterwards.

## Hands-on session with OpenPyTEA

The hands-on session runs in two parts around lunch:

| Part | Time | Duration |
|---|---|---|
| Part 1 | 11:45 - 12:30 | 45 min |
| Lunch | 12:30 - 13:30 | |
| Part 2 | 13:30 - 14:45 | 75 min |

It consists of six exercises, one notebook each. The exercise number is the notebook number. Inside a notebook, tasks are numbered per exercise (Task 1.1, Task 1.2, ...). Tasks marked **bonus** are for participants who finish early. Every task has a solution in the notebook, so nobody gets stuck.

### Part 1

#### 11:45 - 11:55 Why OpenPyTEA? (presentation, 10 min)
Why we built an open-source TEA toolkit, what it does, and how it fits into the TEA workflow.

#### 11:55 - 12:30 Setup and Exercises 1 and 2 (35 min)

| Time | Duration | Notebook | Core task | Bonus task |
|---|---|---|---|---|
| 11:55 - 12:00 | 5 min | [00 Setup check](notebooks/00_setup_check.ipynb) | Confirm every check prints `OK` | |
| 12:00 - 12:12 | 12 min | [Exercise 1: Equipment costing](notebooks/01_equipment_costing.ipynb) | 1.1 Cost the green-ammonia loop | 1.2 Material and cost-year choices |
| 12:12 - 12:30 | 18 min | [Exercise 2: Building a plant](notebooks/02_building_a_plant.ipynb) | 2.1 Where should the plant be built? | 2.2 Break-even price and catalyst replacement |

Participants whose setup check fails at 11:55 switch to Google Colab and continue there; installation issues are fixed during lunch.

### Lunch (12:30 - 13:30)

Installation help desk during the first 15 minutes of lunch for anyone who used Colab in Part 1.

### Part 2

### 13:30 - 14:35 Exercises 3 to 6 (65 min)

| Time | Duration | Notebook | Core task | Bonus task |
|---|---|---|---|---|
| 13:30 - 13:45 | 15 min | [Exercise 3: Cost breakdowns and sensitivity](notebooks/03_cost_breakdowns_and_sensitivity.ipynb) | 3.1 Break-even electricity price | 3.2 Publication-ready figure |
| 13:45 - 14:00 | 15 min | [Exercise 4: Monte Carlo uncertainty](notebooks/04_monte_carlo_uncertainty.ipynb) | 4.1 Value of better cost data | |
| 14:00 - 14:25 | 25 min | [Exercise 5: Case study, SMR vs. electrolysis](notebooks/05_case_study_hydrogen.ipynb) | 5.1 Electrolysis plant, 5.2 CO₂ break-even tax, 5.3 Monte Carlo comparison | |
| 14:25 - 14:35 | 10 min | [Exercise 6: JSON configuration files and CLI](notebooks/06_json_and_cli.ipynb) | Run the demo cells | 6.1 Scenario file |

### 14:35 - 14:45 Wrap-up and GUI demonstration (10 min)
- Key take-aways and the discussion questions of Exercise 5.
- Live demonstration of the OpenPyTEA graphical user interface: the same workflow without writing code. Installers for Windows and macOS are on the [Releases page](https://github.com/pbtamarona/OpenPyTEA/releases).
- Where to get help, how to contribute cost correlations, and the optional [home assignment](HOME_ASSIGNMENT.md).
