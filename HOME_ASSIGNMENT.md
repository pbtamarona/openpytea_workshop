# Home Assignment (Optional)

Participants who want to go further can complete a short assignment after the workshop. We will read every submission and send back feedback.

## The Goal

Perform a small, reproducible techno-economic assessment with OpenPyTEA of a process you care about (target effort: **3 to 6 hours**).

## Recommended scope

Preferably, apply OpenPyTEA to a process from your own research, studies, or professional work. If you do not have one at hand, pick one of these:

- Re-implement a published TEA from the literature and compare your levelized cost with the published one.
- Extend the capstone case study with a third hydrogen pathway (for example SMR with CCS, methane pyrolysis, coal/biomass gasification - see `examples/case_study_1.ipynb` in the OpenPyTEA repository for reference).
- Take the geothermal case study (`examples/case_study_3.ipynb` in the OpenPyTEA repository) and test how the conclusion changes with your own country's energy price and location factor.

## Guidelines

1. **Hand in one or more Jupyter notebooks** (`.ipynb`), the same format as the workshop exercises. If you are recreating a TEA from literature, please also provide the reference document/link.
2. **Use at least two of the analysis concepts covered in the session**: cost breakdowns, cash-flow analysis, sensitivity or tornado analysis, Monte Carlo uncertainty analysis, comparison of alternatives, or the JSON/CLI workflow.
3. **Start the notebook with a short background section** in Markdown cells, before any code:
   - **Process**: what the process does, its product and capacity, and its main steps or equipment. A simple flowsheet image helps but is optional.
   - **Question**: what you want to find out, for example "What is the levelized cost of product?" or "Which of two designs is cheaper?".
   - **Data sources**: where the process data come from (simulation, literature, your own measurements), with references.
   - **Key assumptions**: location, prices, project lifetime, interest rate, and anything else that drives the result.

   **Don't be afraid to make assumptions for details you don't have**, as well as spending too much time hunting for input data for now. A reasonable estimate that is clearly listed under key assumptions is fine.

4. **End with a conclusion** that states the main result in two or three sentences.
5. **Make it reproducible**: the notebook must run from top to bottom after **Kernel**, then **Restart Kernel and Run All Cells**. Send any input files it reads along with it, and save the notebook with its outputs so we can see your results without running it. If you use packages beyond the workshop environment, put their install lines in the first code cell of the notebook, for example:

   ```python
   %pip install seaborn
   ```

## Submission

Email your notebook(s) and any input files as attachments to `P.B.Tamarona@tudelft.nl` with the subject line `OpenPyTEA workshop assignment`. If you have several files, put them in one ZIP file. If the attachment is larger than about 20 MB, send a download link instead. If you used an online repository, sending its link is enough.

## Contributing back

If your assessment turns out well, and with your permission, we would like to add it to the [OpenPyTEA repository](https://github.com/pbtamarona/OpenPyTEA) as one of its case studies, with you credited as the author. This helps other users learn from a real application, broadens the range of processes the toolkit is tested on, and makes your work visible to the TEA community. We will always ask first; nothing is published without your consent.

Also if you find cost correlations that are not on OpenPyTEA, consider opening a pull request to add it to `cost_correlations.csv`. The contributing guide is at https://openpytea.readthedocs.io.
