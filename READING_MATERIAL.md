# Optional Reading Material

None of this is required for the hands-on session. The first item is the most useful one if you only have half an hour. Each item is marked by how you can access it:

- 🔓 **Free**: open access, free to read online.
- 🔒 **Paid**: behind a paywall. Read it only if you already have access, for example through your university library. You do not need to buy anything for the workshop.

## OpenPyTEA

1. Tamarona, P.B., Vlugt, T.J.H., & Ramdin, M. (2026). OpenPyTEA: An open-source python toolkit for techno-economic assessment of chemical process plants and energy systems with economic sensitivity and uncertainty evaluation. *SoftwareX, 35*, 102816. https://doi.org/10.1016/j.softx.2026.102816. Description: the paper describing the toolkit, its architecture, and the three case studies shipped with the package. Reading sections 1 to 3 gives you the vocabulary used throughout the session. 🔓 **Free**

2. OpenPyTEA documentation: https://openpytea.readthedocs.io. Description: the Quick Start page walks through a complete TEA in ten minutes. The User Guide pages on Equipment, Plant, and Analysis are the reference we will point to during the exercises. 🔓 **Free**

3. OpenPyTEA walkthrough notebooks: https://github.com/pbtamarona/OpenPyTEA/tree/main/walkthrough. Description: five notebooks covering every feature in more depth than we have time for. The workshop notebooks are a condensed version of these. 🔓 **Free**

## Cost engineering fundamentals

4. Towler, G., & Sinnott, R. (2022). *Chemical Engineering Design: Principles, Practice and Economics of Plant and Process Design* (3rd ed.). Elsevier. https://doi.org/10.1016/C2019-0-02025-0. Description: chapters 7 to 9 (capital cost estimating, operating costs, economic evaluation) are the source of most default factors in OpenPyTEA: installation factors, location factors, ISBL/OSBL/engineering/contingency multipliers. 🔒 **Paid**

5. Turton, R., Shaeiwitz, J.A., Bhattacharyya, D., & Whiting, W.B. (2018). *Analysis, Synthesis, and Design of Chemical Processes* (5th ed.). Prentice Hall. [Pearson book page](https://www.pearson.com/en-us/subject-catalog/p/analysis-synthesis-and-design-of-chemical-processes/P200000000651/9780137459483) Description: chapters 7 and 8 cover equipment cost correlations and manufacturing-cost estimation; the fixed OPEX factors used by OpenPyTEA follow this book. 🔒 **Paid**

Other classic chemical engineering textbooks cover the same topics well, and several of them are sources for the cost correlations in OpenPyTEA's database. If your library has one of these, it serves just as well as items 4 and 5:
- *Perry's Chemical Engineers' Handbook*, 9th ed. (Green & Southard, 2019); Section 9 covers process economics
- *Product and Process Design Principles*, 4th ed. (Seider et al., 2017)
- *Plant Design and Economics for Chemical Engineers*, 5th ed. (Peters, Timmerhaus & West, 2003)
- *Chemical Engineering Process Design and Economics*, 2nd ed. (Ulrich & Vasudevan, 2004)

## Uncertainty in TEA

6. Van der Spek, M., Roussanaly, S., & Rubin, E.S. (2019). Best practices and recent advances in CCS cost engineering and economic analysis. *International Journal of Greenhouse Gas Control, 83*, 91-104. https://doi.org/10.1016/j.ijggc.2019.02.006. 🔒 **Paid** The journal version is behind a paywall, but the authors' accepted manuscript is free in an open repository: [free author version](http://hdl.handle.net/11250/2598150). Description: a practical discussion of why sensitivity and Monte Carlo analysis belong in every TEA, and how to report them. Useful background for Exercises 3 and 4. 🔓 **Free** (author version)
