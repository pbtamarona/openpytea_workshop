"""Regenerate the workshop notebooks and the JSON assets from scratch.

The notebooks in ``notebooks/`` were produced by this script and can be edited directly in
Jupyter afterwards. Re-running the script OVERWRITES them, so only use it when you want to
rebuild everything from this source, for example after a large restructuring.

Usage (from the repository root, with nbformat installed):

    python tools/build_notebooks.py notebooks
"""
import json
import sys
import textwrap
from pathlib import Path

import nbformat as nbf

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "assets").mkdir(exist_ok=True)

REPO = "pbtamarona/openpytea-workshop"
PKG_IMG = "https://raw.githubusercontent.com/pbtamarona/OpenPyTEA/main/examples/img"


def md(s):
    return nbf.v4.new_markdown_cell(textwrap.dedent(s).strip("\n"))


def code(s):
    return nbf.v4.new_code_cell(textwrap.dedent(s).strip("\n"))


def header(fname, title, intro, goals, refs):
    colab = f"https://colab.research.google.com/github/{REPO}/blob/main/notebooks/{fname}"
    goal_lines = "\n".join(f"- {g}" for g in goals)
    ref_lines = "\n".join(f"- {r}" for r in refs)
    return [
        md(f"""
        # {title}

        [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab})

        {textwrap.dedent(intro).strip()}
        """),
        md(f"""
        ## Learning goals

        {goal_lines}
        """),
        md(f"""
        ## Background references

        {ref_lines}
        """),
    ]


SETUP_CELL = code("""
# Run this cell first. It installs OpenPyTEA if it is missing (for example on Google Colab).
try:
    import openpytea
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "openpytea"])
    import openpytea

print("OpenPyTEA version:", openpytea.__version__)
""")

REF_PAPER = ("Tamarona, P.B., Vlugt, T.J.H., & Ramdin, M. (2026). OpenPyTEA: An open-source python toolkit for "
             "techno-economic assessment of chemical process plants and energy systems with economic sensitivity "
             "and uncertainty evaluation. *SoftwareX, 35*, 102816. https://doi.org/10.1016/j.softx.2026.102816")
REF_TOWLER = ("Towler, G., & Sinnott, R. (2022). *Chemical Engineering Design* (3rd ed.). Elsevier. "
              "https://doi.org/10.1016/C2019-0-02025-0")
REF_TURTON = ("Turton, R., Shaeiwitz, J.A., Bhattacharyya, D., & Whiting, W.B. (2018). "
              "*Analysis, Synthesis, and Design of Chemical Processes* (5th ed.). Prentice Hall.")
REF_DOCS = "OpenPyTEA documentation: https://openpytea.readthedocs.io"

# --------------------------------------------------------------------------------------
# Shared code blocks: the green-ammonia demo plant, rebuilt at the start of notebooks 02-04
# --------------------------------------------------------------------------------------
AMMONIA_EQUIPMENT = """
from openpytea import Equipment

# Equipment of the green-ammonia synthesis loop (sizes from the process simulation, see notebook 01)
compressor  = Equipment(name="C-101 Syngas compressor", param=1_200, process_type="Fluids",
                        category="Compressors, fans, & blowers", type="Compressor, centrifugal",
                        material="Carbon steel")
motor       = Equipment(name="M-101 Compressor motor", param=1_200 / 0.90, process_type="Electrical",
                        category="Motors & generators", type="Totally enclosed motor")
exchanger   = Equipment(name="E-101 Feed/effluent exchanger", param=250, process_type="Fluids",
                        category="Heat Exchangers", type="U-tube shell & tube",
                        material="304 stainless steel")
converter   = Equipment(name="R-101 Ammonia converter", param=12_000, process_type="Fluids",
                        category="Reactors", type="Tubular fixed bed", material="304 stainless steel")
separator   = Equipment(name="V-101 Ammonia separator", param=25, process_type="Fluids",
                        category="Pressure vessels", type="Vertical", material="Carbon steel")
chiller     = Equipment(name="K-101 Refrigeration unit", param=800, process_type="Fluids",
                        category="Utilities", type="Packaged mechanical refrigerator")
product_pump = Equipment(name="P-101 Product pump", param=20, process_type="Fluids",
                         category="Pumps", type="Single-stage centrifugal", material="Carbon steel")

equipment_list = [compressor, motor, exchanger, converter, separator, chiller, product_pump]
"""

AMMONIA_CONFIG = """
from openpytea import Plant

ammonia_config = {
    "plant_name": "Green Ammonia",
    "process_type": "Fluids",
    "country": "Netherlands",
    "equipment": equipment_list,

    # Financial assumptions
    "interest_rate": 0.08,
    "project_lifetime": 20,      # years
    "plant_utilization": 0.90,   # fraction of the year on stream
    "tax_rate": 0.25,

    # Products: the first entry is the main product used for the levelized cost
    "plant_products": {
        "ammonia": {"production": 100_000, "price": 0.95},   # kg/day, USD/kg
    },

    # Variable OPEX: daily consumption and unit price
    "variable_opex_inputs": {
        "hydrogen":    {"consumption": 17_800, "price": 2.00},   # kg/day,  USD/kg
        "nitrogen":    {"consumption": 82_400, "price": 0.05},   # kg/day,  USD/kg
        "electricity": {"consumption": 60_000, "price": 0.08},   # kWh/day, USD/kWh
    },
}

ammonia_plant = Plant(ammonia_config)
ammonia_plant.calculate_all()
print(f"Fixed capital investment : {ammonia_plant.fixed_capital:,.0f} USD")
print(f"Levelized cost of ammonia: {ammonia_plant.levelized_cost:.3f} USD/kg")
print(f"Net present value        : {ammonia_plant.npv:,.0f} USD")
"""

# ======================================================================================
# 00 - Setup check
# ======================================================================================
nb00 = nbf.v4.new_notebook()
nb00.cells = header(
    "00_setup_check.ipynb",
    "00 - Setup and first checks",
    """
    Run this notebook **before the workshop** to verify that your laptop is ready. Use it together with
    [INSTRUCTIONS.md](../INSTRUCTIONS.md). Every check prints `OK` when it passes. If a check fails, the
    message tells you which installation step to repeat.

    Expected time: 5 minutes.
    """,
    [
        "Confirm that the notebook runs in the environment you created for the workshop.",
        "Confirm that `openpytea` and its scientific-Python dependencies import correctly.",
        "Run a five-line techno-economic assessment and produce one plot, so that the whole toolchain is exercised once.",
        "Confirm that the `openpytea` command-line tool is on your PATH (optional, used in notebook 06).",
    ],
    [REF_PAPER, REF_DOCS],
) + [
    md("## 1) Environment snapshot"),
    code("""
    import platform
    import sys
    from pathlib import Path

    print("Python version   :", sys.version.split()[0])
    print("Python executable:", sys.executable)
    print("Platform         :", platform.platform())
    print("Current folder   :", Path.cwd())

    major, minor = sys.version_info[:2]
    print("OK: Python 3.10 or newer" if (major, minor) >= (3, 10) else "FAIL: OpenPyTEA needs Python 3.10 or newer")
    """),
    md("""
    ## 2) Import checks

    All of these must print `OK`. If `openpytea` fails, go back to step 3 of [INSTRUCTIONS.md](../INSTRUCTIONS.md)
    and make sure the notebook kernel uses the environment where you installed it (menu **Kernel**, then **Change Kernel**).
    On Google Colab, run the next cell twice: the first run installs the package.
    """),
    SETUP_CELL,
    code("""
    import importlib

    for name in ["openpytea", "numpy", "pandas", "scipy", "matplotlib", "tqdm"]:
        try:
            module = importlib.import_module(name)
            print(f"OK   {name:<11} version {getattr(module, '__version__', 'unknown')}")
        except Exception as exc:
            print(f"FAIL {name:<11} {type(exc).__name__}: {exc}")
    """),
    code("""
    from packaging.version import Version  # ships with pip/setuptools

    import openpytea

    print("OK: OpenPyTEA version is recent enough" if Version(openpytea.__version__) >= Version("3.0.0")
          else f"FAIL: found {openpytea.__version__}, please run  pip install --upgrade openpytea")
    """),
    md("""
    ## 3) A five-line techno-economic assessment

    This exercises the full chain: cost correlation lookup, plant economics, and plotting.
    A small figure should appear below the cell.
    """),
    code("""
    from openpytea import Equipment, Plant, fixed_capital_data, plot_stacked_bar

    compressor = Equipment(name="C-101", param=1_000, process_type="Fluids",
                           category="Compressors, fans, & blowers", type="Compressor, centrifugal")
    plant = Plant({
        "plant_name": "Setup check", "process_type": "Fluids", "equipment": [compressor],
        "plant_products": {"product": {"production": 10_000, "price": 3.0}},
        "variable_opex_inputs": {"electricity": {"consumption": 24_000, "price": 0.08}},
    })
    plant.calculate_all()
    fig, ax = plot_stacked_bar(fixed_capital_data(plant))
    print(f"OK: levelized cost = {plant.levelized_cost:.2f} USD/unit, NPV = {plant.npv:,.0f} USD")
    """),
    md("""
    ## 4) Command-line tool (optional)

    Installing `openpytea` also installs a command-line tool of the same name. It is used only in the optional
    notebook 06, so a `WARNING` here is not a problem for the session.
    """),
    code("""
    import shutil

    cli = shutil.which("openpytea")
    print(f"OK: openpytea CLI found at {cli}" if cli else
          "WARNING: openpytea CLI not on PATH (only needed for notebook 06; `python -m openpytea.cli` works as a fallback)")
    """),
    md("""
    ## Troubleshooting quick list

    - `ModuleNotFoundError: openpytea`: the kernel is not the workshop environment. Change the kernel, or run
      `python -m ipykernel install --user --name openpytea-ws` with the environment activated and restart Jupyter Lab.
    - `pip install` fails behind a proxy or firewall: try Google Colab (see [INSTRUCTIONS.md](../INSTRUCTIONS.md), Option 0).
    - No figure appears: run `%matplotlib inline` in a cell and re-run the plot cell.
    - Anything else: email `P.B.Tamarona@tudelft.nl` with the full error message and your operating system.

    ## Recap

    If every cell above printed `OK`, you are ready. See you at the workshop!
    """),
]

# ======================================================================================
# 01 - Equipment costing
# ======================================================================================
nb01 = nbf.v4.new_notebook()
nb01.cells = header(
    "01_equipment_costing.ipynb",
    "01 - Equipment costing",
    """
    Every techno-economic assessment (TEA) starts from a list of equipment with sizes taken from a process
    simulation or a hand calculation. In this notebook we turn those sizes into **purchased** and **installed
    (direct) costs** with OpenPyTEA's `Equipment` class, and we build the equipment list of a small green-ammonia
    synthesis loop that we will use for the rest of the session.

    Expected time: 25 minutes.
    """,
    [
        "Create an `Equipment` object from a category, type, size parameter, and material.",
        "Explain how OpenPyTEA computes the purchased cost (cost correlation), adjusts it for inflation (CEPCI), and turns it into a direct cost (installation factors).",
        "Browse the built-in cost-correlation database to find the right category, type, and size units.",
        "Use a vendor quote instead of a correlation, change the cost year, and let OpenPyTEA split oversized equipment into parallel units.",
        "Assemble the equipment list of the workshop's demo plant.",
    ],
    [REF_TOWLER + " (chapter 7: capital cost estimating)", REF_TURTON + " (appendix A: cost correlations)", REF_DOCS],
) + [
    md("## 0) Setup"),
    SETUP_CELL,
    md("""
    ## 1) From size to cost in three steps

    ![OpenPyTEA architecture](https://raw.githubusercontent.com/pbtamarona/OpenPyTEA/main/examples/img/architecture.png)

    For each equipment item OpenPyTEA does the following:

    1. **Purchased cost** $C_p$ from a cost correlation selected by `category` and `type`. The database
       (`cost_correlations.csv`, shipped with the package) stores 400+ correlations from Towler & Sinnott, Turton et al.,
       Seider et al., Ulrich, Perry, and journal papers, each with its size parameter, validity range, and cost year.
    2. **Inflation adjustment** to the target year (2024 by default) with the Chemical Engineering Plant Cost Index:
       $C_{\\text{target}} = C_{\\text{base}} \\cdot \\text{CEPCI}_{\\text{target}} / \\text{CEPCI}_{\\text{base}}$.
    3. **Direct (installed) cost** with the factorial method of Towler & Sinnott:
       $C_D = C_p \\left[(1 + f_p) f_m + (f_{er} + f_{el} + f_i + f_c + f_s + f_l)\\right]$,
       where $f_m$ is the material factor and the other factors (piping, erection, electrical, instrumentation,
       civil, structural, lagging) depend on the `process_type` (`Fluids`, `Solids`, `Mixed`, `Electrical`).

    Let us cost a shell-and-tube heat exchanger of 250 m² in 304 stainless steel:
    """),
    code("""
    from openpytea import Equipment

    exchanger = Equipment(
        name="E-101",
        param=250,                          # heat-transfer area in m2 (the units come from the correlation)
        process_type="Fluids",
        category="Heat Exchangers",
        type="U-tube shell & tube",
        material="304 stainless steel",
    )

    print(exchanger)
    print(f"Purchased cost (2024 USD): {exchanger.purchased_cost:,.0f}")
    print(f"Direct cost    (2024 USD): {exchanger.direct_cost:,.0f}")
    print(f"Material factor          : {exchanger.material_factor}")
    """),
    md("""
    The direct cost is about 3.7 times the purchased cost: this is the well-known "Lang factor" effect for fluid
    processes. The installation factors used are class attributes, so you can always inspect (or override) them:
    """),
    code("""
    import pandas as pd

    print("Installation factors per process type:")
    display(pd.DataFrame(Equipment.process_factors))

    print("A few material factors:")
    print({m: Equipment.material_factors[m] for m in ["Carbon steel", "304 stainless steel", "316 stainless steel", "Hastelloy C", "Nickel"]})
    """),
    md("""
    ## 2) Finding the right correlation

    The most common question is *"what category, type, and units do I use?"*. The database is a CSV file inside the
    package, so we can load it with pandas and filter it. The `units` column tells you what `param` must be.
    """),
    code("""
    from importlib.resources import files

    correlations = pd.read_csv(files("openpytea") / "data" / "cost_correlations.csv")
    print(f"{len(correlations)} correlations in {correlations['category'].nunique()} categories")

    # All categories
    print(sorted(correlations["category"].unique()))
    """),
    code("""
    # All correlations for compressors: type, size units, validity range, cost year, and source
    columns = ["category", "type", "units", "s_lower", "s_upper", "cost_year", "source"]
    correlations[correlations["category"].str.contains("Compressors", case=False)][columns]
    """),
    md("""
    > **Tip.** Matching on `category` and `type` is case-insensitive. When several correlations share the same
    > category and type, OpenPyTEA takes the first one in the file. Pass `cost_func="<key>"` to pick a specific one.

    ## 3) Four things you will need in practice
    """),
    md("**3a. Material and process type change the installed cost, not the purchased cost**"),
    code("""
    for material in ["Carbon steel", "304 stainless steel", "Hastelloy C"]:
        e = Equipment(name="E-101", param=250, process_type="Fluids", category="Heat Exchangers",
                      type="U-tube shell & tube", material=material)
        print(f"{material:<20} purchased {e.purchased_cost:>10,.0f}   direct {e.direct_cost:>10,.0f}")
    """),
    md("**3b. A vendor quote or literature value replaces the correlation** (give `purchased_cost` and its `cost_year`, OpenPyTEA still escalates it to the target year)"),
    code("""
    electrolyzer_stack = Equipment(
        name="Electrolyzer stack",
        param=None,                         # not needed when the cost is given directly
        process_type="Fluids",
        category="Electrolysis",            # free label: this category is not in the database
        type="Alkaline stack",
        purchased_cost=17_194_000,          # quote in 2020 USD (DOE report)
        cost_year=2020,
    )
    print(f"2020 quote escalated to 2024: {electrolyzer_stack.purchased_cost:,.0f} USD")
    """),
    md("**3c. Costs in another year** (`target_year`) and **oversized equipment** (automatic parallel units when `param` exceeds the correlation's upper bound)"),
    code("""
    exchanger_2019 = Equipment(name="E-101", param=250, process_type="Fluids", category="Heat Exchangers",
                               type="U-tube shell & tube", material="304 stainless steel", target_year=2019)
    print(f"Same exchanger in 2019 USD: {exchanger_2019.purchased_cost:,.0f} (2024 USD: {exchanger.purchased_cost:,.0f})")

    big_compressor = Equipment(name="C-201", param=45_000, process_type="Fluids",
                               category="Compressors, fans, & blowers", type="Compressor, centrifugal")
    print(f"45 MW compressor -> {big_compressor.num_units} parallel units, direct cost {big_compressor.direct_cost:,.0f} USD")
    """),
    md("""
    **3d. Assemblies** such as a pressure-swing adsorption (PSA) skid can be built from sub-components with
    `CompositeEquipment`. The composite behaves like a single equipment item in the plant.
    """),
    code("""
    from openpytea import CompositeEquipment

    vessels = Equipment(name="Adsorber vessels", param=8.0, process_type="Fluids", category="Pressure vessels",
                        type="Vertical", material="Carbon steel", num_units=2)       # two identical vessels of 8 m3
    zeolite = Equipment(name="Zeolite 5A", param=2 * 150.0, process_type="Solids",
                        category="Packings & adsorbents", type="Molecular sieves")    # ft3 of adsorbent
    psa = CompositeEquipment(name="PSA unit", process_type="Fluids", components=[vessels, zeolite],
                             category="Adsorption", type="Pressure-swing adsorber")
    print(psa)
    psa.breakdown().round(0)
    """),
    md("""
    ## 4) Exercise 1: cost the green-ammonia synthesis loop

    The demo plant of this workshop is a small **green-ammonia synthesis loop** (100 t NH₃/day) fed with hydrogen
    from an electrolyzer and nitrogen from an air separation unit. The process simulation gives the following sizes:

    | Tag | Equipment | Category | Type | Size (`param`) | Material |
    |---|---|---|---|---|---|
    | C-101 | Syngas compressor | `Compressors, fans, & blowers` | `Compressor, centrifugal` | 1 200 kW driver power | Carbon steel |
    | M-101 | Compressor motor | `Motors & generators` | `Totally enclosed motor` | 1 200 / 0.90 kW shaft power | default |
    | E-101 | Feed/effluent exchanger | `Heat Exchangers` | `U-tube shell & tube` | 250 m² | 304 stainless steel |
    | R-101 | Ammonia converter | `Reactors` | `Tubular fixed bed` | 12 000 kg shell mass | 304 stainless steel |
    | V-101 | Ammonia separator | `Pressure vessels` | `Vertical` | 25 m³ | Carbon steel |
    | K-101 | Refrigeration unit | `Utilities` | `Packaged mechanical refrigerator` | 800 kW evaporator duty | default |
    | P-101 | Product pump | `Pumps` | `Single-stage centrifugal` | 20 L/s | Carbon steel |

    The motor is an electrical item, so use `process_type="Electrical"` for it; everything else is `"Fluids"`.

    **Tasks**
    1. Create the seven `Equipment` objects and put them in a list called `equipment_list`.
    2. Print a table with the name, purchased cost, and direct cost of each item, and the total direct cost (this total is the ISBL of the plant).
    3. Which item dominates? Does that match your engineering intuition?
    """),
    code("""
    # YOUR CODE HERE
    # Hints:
    #   Equipment(name=..., param=..., process_type=..., category=..., type=..., material=...)
    #   Leave `material` out for the motor and the refrigeration unit (the correlation's default material is used).
    #   pd.DataFrame([{"name": e.name, "purchased": e.purchased_cost, "direct": e.direct_cost} for e in equipment_list])
    """),
    md("""
    <details>
    <summary><b>Solution</b> (click to expand)</summary>

    ```python
    from openpytea import Equipment
    import pandas as pd

    compressor   = Equipment(name="C-101 Syngas compressor", param=1_200, process_type="Fluids",
                             category="Compressors, fans, & blowers", type="Compressor, centrifugal", material="Carbon steel")
    motor        = Equipment(name="M-101 Compressor motor", param=1_200 / 0.90, process_type="Electrical",
                             category="Motors & generators", type="Totally enclosed motor")
    exchanger    = Equipment(name="E-101 Feed/effluent exchanger", param=250, process_type="Fluids",
                             category="Heat Exchangers", type="U-tube shell & tube", material="304 stainless steel")
    converter    = Equipment(name="R-101 Ammonia converter", param=12_000, process_type="Fluids",
                             category="Reactors", type="Tubular fixed bed", material="304 stainless steel")
    separator    = Equipment(name="V-101 Ammonia separator", param=25, process_type="Fluids",
                             category="Pressure vessels", type="Vertical", material="Carbon steel")
    chiller      = Equipment(name="K-101 Refrigeration unit", param=800, process_type="Fluids",
                             category="Utilities", type="Packaged mechanical refrigerator")
    product_pump = Equipment(name="P-101 Product pump", param=20, process_type="Fluids",
                             category="Pumps", type="Single-stage centrifugal", material="Carbon steel")

    equipment_list = [compressor, motor, exchanger, converter, separator, chiller, product_pump]

    table = pd.DataFrame([{"name": e.name, "purchased cost": e.purchased_cost, "direct cost": e.direct_cost}
                          for e in equipment_list]).set_index("name")
    display(table.round(0))
    print(f"Total direct cost (ISBL): {table['direct cost'].sum():,.0f} USD")
    ```

    The syngas compressor is by far the largest item, as expected for an ammonia loop operating at high pressure.
    </details>
    """),
    md("""
    ## 5) Exercise 2: how sensitive is the estimate to your choices?

    Using the ammonia converter (R-101), answer the following:

    1. What is the direct cost in carbon steel instead of 304 stainless steel? By what factor does it change?
    2. What is the purchased cost expressed in 2015 USD instead of 2024 USD?
    3. Look up the validity range of the `Tubular fixed bed` correlation in the database. Is 12 000 kg inside it?
    """),
    code("""
    # YOUR CODE HERE
    """),
    md("""
    <details>
    <summary><b>Solution</b> (click to expand)</summary>

    ```python
    r_ss = Equipment(name="R-101", param=12_000, process_type="Fluids", category="Reactors",
                     type="Tubular fixed bed", material="304 stainless steel")
    r_cs = Equipment(name="R-101", param=12_000, process_type="Fluids", category="Reactors",
                     type="Tubular fixed bed", material="Carbon steel")
    print(f"Direct cost 304SS / CS: {r_ss.direct_cost / r_cs.direct_cost:.2f}")

    r_2015 = Equipment(name="R-101", param=12_000, process_type="Fluids", category="Reactors",
                       type="Tubular fixed bed", material="304 stainless steel", target_year=2015)
    print(f"Purchased cost: {r_2015.purchased_cost:,.0f} USD(2015) vs {r_ss.purchased_cost:,.0f} USD(2024)")

    row = correlations[correlations["type"].str.lower() == "tubular fixed bed"].iloc[0]
    print(f"Valid for {row['units']} between {row['s_lower']} and {row['s_upper']}")
    ```
    </details>
    """),
    md("""
    ## Recap

    - `Equipment(name, param, process_type, category, type, material)` looks up a correlation, escalates the cost with CEPCI, and applies installation factors.
    - Check the `units` column of the database before you set `param`; the validity range tells you how far you are extrapolating.
    - Vendor quotes go in via `purchased_cost` and `cost_year`; assemblies via `CompositeEquipment`.
    - The list of `Equipment` objects is the input to the `Plant` we build in the next notebook.

    **Next:** [02 - Building a plant](02_building_a_plant.ipynb)
    """),
]

# ======================================================================================
# 02 - Building a plant
# ======================================================================================
nb02 = nbf.v4.new_notebook()
nb02.cells = header(
    "02_building_a_plant.ipynb",
    "02 - Building a plant",
    """
    A `Plant` combines an equipment list with economic assumptions and returns everything a TEA report needs:
    fixed capital investment, fixed and variable operating costs, revenue, yearly cash flows, and the profitability
    metrics (NPV, IRR, ROI, payback time, levelized cost). In this notebook we build the green-ammonia plant step by
    step and learn how to read and change its assumptions.

    Expected time: 35 minutes.
    """,
    [
        "Write a plant configuration dictionary with financial assumptions, products, and variable OPEX inputs.",
        "Compute and read the fixed capital investment (ISBL, OSBL, design and engineering, contingency, location factor).",
        "Compute fixed OPEX, variable OPEX, revenue, and the yearly cash flow.",
        "Interpret NPV, IRR, ROI, payback time, and the levelized cost of product, and know which assumptions each depends on.",
        "Change assumptions with `update_configuration()` and re-run the calculation.",
    ],
    [REF_TOWLER + " (chapters 7 to 9)", REF_TURTON + " (chapters 7 to 10)", REF_DOCS],
) + [
    md("## 0) Setup: rebuild the equipment list from notebook 01"),
    SETUP_CELL,
    code(AMMONIA_EQUIPMENT + """
print(f"ISBL (sum of direct costs): {sum(e.direct_cost for e in equipment_list):,.0f} USD")
"""),
    md("""
    ## 1) The plant configuration

    A `Plant` is created from one dictionary. Only `plant_name`, `process_type`, `equipment`, and `plant_products`
    are strictly required; everything else has a documented default. Units are up to you, but they must be
    consistent: OpenPyTEA multiplies **daily** quantities by 365 and by the plant utilization to get yearly values,
    and prices are per unit of that quantity.
    """),
    code("""
    from openpytea import Plant

    ammonia_config = {
        "plant_name": "Green Ammonia",
        "process_type": "Fluids",            # "Solids" | "Fluids" | "Mixed" -> sets default OSBL, D&E, contingency factors
        "country": "Netherlands",            # location factor lookup (see Plant.locFactors); "region" is needed for some countries
        "equipment": equipment_list,

        # Financial assumptions
        "interest_rate": 0.08,               # discount rate
        "project_lifetime": 20,              # years, including construction
        "plant_utilization": 0.90,           # fraction of the year on stream
        "tax_rate": 0.25,

        # Products: the FIRST entry is the main product used for the levelized cost
        "plant_products": {
            "ammonia": {"production": 100_000, "price": 0.95},   # kg/day, USD/kg
        },

        # Variable OPEX: daily consumption and unit price of every feed and utility
        "variable_opex_inputs": {
            "hydrogen":    {"consumption": 17_800, "price": 2.00},   # kg/day,  USD/kg
            "nitrogen":    {"consumption": 82_400, "price": 0.05},   # kg/day,  USD/kg
            "electricity": {"consumption": 60_000, "price": 0.08},   # kWh/day, USD/kWh
        },
    }

    ammonia_plant = Plant(ammonia_config)
    """),
    md("""
    ## 2) Fixed capital investment

    $$\\text{FCI} = \\text{ISBL} \\cdot (1 + OS) \\cdot (1 + D\\&E + X) \\cdot LF$$

    ISBL is the sum of the equipment direct costs. The offsite (OS), design and engineering (D&E), and contingency
    (X) factors default to 0.3, 0.3, and 0.1 for fluid plants (Towler & Sinnott). The location factor LF comes from
    the country (and region). Any of these can be overridden.
    """),
    code("""
    ammonia_plant.calculate_fixed_capital(print_results=True)
    """),
    code("""
    # The location factors OpenPyTEA knows about
    Plant.locFactors
    """),
    md("""
    ## 3) Operating costs and revenue

    - **Variable OPEX**: consumption × price × 365 × utilization, for each item in `variable_opex_inputs`.
    - **Fixed OPEX**: operating labor (from an operator count based on the number of process steps, or a number you
      give), supervision, overheads, maintenance (5 % of ISBL), taxes and insurance, and so on, following Turton et al.
    - **Revenue**: production × price × 365 × utilization, for each product.
    """),
    code("""
    ammonia_plant.calculate_variable_opex(print_results=True)
    """),
    code("""
    ammonia_plant.calculate_fixed_opex(print_results=True)
    print(f"Operators hired (auto-estimated): {ammonia_plant.calculate_operators_hired()}")
    """),
    code("""
    ammonia_plant.calculate_revenue(print_results=True)
    """),
    md("""
    ## 4) Cash flow and profitability metrics

    `calculate_cash_flow()` builds the year-by-year table. By default the capital is spent over three construction
    years (30 / 60 / 10 %), production ramps up (0 / 0 / 40 / 80 / 100 %), depreciation follows MACRS, and taxes are
    paid with a one-year lag. Working capital (15 % of FCI by default) is drawn at start-up and released at the end.
    """),
    code("""
    ammonia_plant.calculate_cash_flow(print_results=True)
    """),
    md("""
    Once the cash flows exist, the metrics follow:

    | Metric | Meaning | Method |
    |---|---|---|
    | NPV | Present value of all cash flows at the interest rate | `calculate_npv()` |
    | LCOP | Levelized cost of product: the selling price at which NPV = 0, after crediting by-products | `calculate_levelized_cost()` |
    | PBT | Payback time: FCI divided by average annual cash flow | `calculate_payback_time()` |
    | ROI | Average yearly net profit over total investment | `calculate_roi()` |
    | IRR | Discount rate at which NPV = 0 | `calculate_irr()` |

    `calculate_all()` runs every step above in the right order.
    """),
    code("""
    ammonia_plant.calculate_all()

    print(f"Fixed capital investment : {ammonia_plant.fixed_capital:>14,.0f} USD")
    print(f"Variable OPEX            : {ammonia_plant.variable_production_costs:>14,.0f} USD/yr")
    print(f"Fixed OPEX               : {ammonia_plant.fixed_production_costs:>14,.0f} USD/yr")
    print(f"Revenue                  : {ammonia_plant.revenue:>14,.0f} USD/yr")
    print(f"Levelized cost of ammonia: {ammonia_plant.levelized_cost:>14.3f} USD/kg")
    print(f"Net present value        : {ammonia_plant.npv:>14,.0f} USD")
    print(f"Internal rate of return  : {ammonia_plant.irr:>14.1%}")
    print(f"Return on investment     : {ammonia_plant.roi:>14.1f} %")
    print(f"Payback time             : {ammonia_plant.payback_time:>14.1f} years")
    """),
    md("""
    > **Reading the result.** The levelized cost (about 0.89 USD/kg) sits just below the assumed selling price of
    > 0.95 USD/kg, so the project is marginally profitable: the NPV is a few million USD and the IRR is a little
    > above the 8 % discount rate. Hydrogen is by far the largest cost item. Keep these numbers in mind: the next
    > notebooks ask how robust this conclusion is.

    ## 5) Changing assumptions

    `update_configuration()` merges a partial dictionary into the existing configuration (nested dictionaries are
    merged, not replaced), so you can change one number and recalculate. Overrides exist for almost every default:
    `fixed_capital_factors`, `fixed_opex_factors`, `loc_factor`, `operators_hired`, `capex_ramp`,
    `production_ramp`, `depreciation`, `working_capital`, `additional_capex_cost` and `additional_capex_years`.
    """),
    code("""
    from copy import deepcopy

    variant = deepcopy(ammonia_plant)
    variant.update_configuration({
        "plant_name": "Green Ammonia (cheaper H2)",
        "variable_opex_inputs": {"hydrogen": {"price": 1.50}},       # only the price changes; consumption is kept
        "fixed_opex_factors": {"maintenance": 0.03},                 # 3 % of ISBL instead of 5 %
    })
    variant.calculate_all()

    print(f"LCOP: {ammonia_plant.levelized_cost:.3f} -> {variant.levelized_cost:.3f} USD/kg")
    print(f"NPV : {ammonia_plant.npv:,.0f} -> {variant.npv:,.0f} USD")
    """),
    md("""
    ## 6) Exercise 3: where should the plant be built?

    Location factors scale the ISBL to local construction costs. Compare the fixed capital investment and the
    levelized cost of the ammonia plant for these locations:

    - Netherlands
    - United States, region `"Gulf Coast"`
    - China, region `"indigenous"` (locally sourced equipment)
    - India

    Use `deepcopy(ammonia_plant)` and `update_configuration({"country": ..., "region": ...})` in a loop and collect
    the results in a pandas DataFrame. Note that a country with regional factors requires `region`, and one without
    should have `"region": None`.
    """),
    code("""
    # YOUR CODE HERE
    """),
    md("""
    <details>
    <summary><b>Solution</b> (click to expand)</summary>

    ```python
    import pandas as pd
    from copy import deepcopy

    locations = [("Netherlands", None), ("United States", "Gulf Coast"), ("China", "indigenous"), ("India", None)]
    rows = []
    for country, region in locations:
        p = deepcopy(ammonia_plant)
        p.update_configuration({"country": country, "region": region})
        p.calculate_all()
        rows.append({"location": f"{country} {region or ''}".strip(), "FCI [MUSD]": p.fixed_capital / 1e6,
                     "LCOP [USD/kg]": p.levelized_cost, "NPV [MUSD]": p.npv / 1e6})
    pd.DataFrame(rows).set_index("location").round(3)
    ```
    </details>
    """),
    md("""
    ## 7) Exercise 4: the break-even price and the effect of catalyst replacement

    1. By definition the levelized cost is the price at which NPV = 0 **before taxes**. Check it: set the ammonia
       price equal to the computed `levelized_cost` on a copy of the plant and print the NPV. It comes out negative,
       because the 25 % tax is still paid on the profitable years. Now also set `"tax_rate": 0` and confirm that the
       NPV becomes zero.
    2. The converter catalyst must be replaced every 5 years at 1.2 MUSD each time. Add this with
       `"additional_capex_cost": [1.2e6, 1.2e6, 1.2e6]` and `"additional_capex_years": [7, 12, 17]`, run
       `calculate_all(additional_capex=True)` and report how much the NPV and levelized cost change.
    """),
    code("""
    # YOUR CODE HERE
    """),
    md("""
    <details>
    <summary><b>Solution</b> (click to expand)</summary>

    ```python
    breakeven = deepcopy(ammonia_plant)
    breakeven.update_configuration({"plant_products": {"ammonia": {"price": ammonia_plant.levelized_cost}}})
    breakeven.calculate_all()
    print(f"NPV at price = LCOP, 25 % tax: {breakeven.npv:,.0f} USD")

    breakeven.update_configuration({"tax_rate": 0.0})
    breakeven.calculate_all()
    print(f"NPV at price = LCOP, no tax  : {breakeven.npv:,.0f} USD")

    with_catalyst = deepcopy(ammonia_plant)
    with_catalyst.update_configuration({"additional_capex_cost": [1.2e6, 1.2e6, 1.2e6],
                                        "additional_capex_years": [7, 12, 17]})
    with_catalyst.calculate_all(additional_capex=True)
    print(f"LCOP: {ammonia_plant.levelized_cost:.3f} -> {with_catalyst.levelized_cost:.3f} USD/kg")
    print(f"NPV : {ammonia_plant.npv:,.0f} -> {with_catalyst.npv:,.0f} USD")
    ```
    </details>
    """),
    md("""
    ## Recap

    - One dictionary configures a `Plant`; the first product is the main product used for the levelized cost.
    - FCI = ISBL × (1 + OS) × (1 + D&E + X) × LF, all factors visible and overridable.
    - `calculate_all()` gives FCI, OPEX, revenue, cash flow, NPV, LCOP, PBT, ROI, IRR in one call.
    - `deepcopy` + `update_configuration()` is the pattern for scenarios; we automate it in the next notebook.

    **Next:** [03 - Cost breakdowns and sensitivity](03_cost_breakdowns_and_sensitivity.ipynb)
    """),
]

# ======================================================================================
# 03 - Cost breakdowns, cash-flow diagram, sensitivity, tornado
# ======================================================================================
nb03 = nbf.v4.new_notebook()
nb03.cells = header(
    "03_cost_breakdowns_and_sensitivity.ipynb",
    "03 - Cost breakdowns, cash-flow diagrams, and sensitivity analysis",
    """
    Totals hide where the money goes. This notebook uses OpenPyTEA's analysis and plotting functions to break costs
    down, draw the cumulative cash-flow diagram, and ask *"what if"* questions with one-way sensitivity curves and
    tornado plots.

    Expected time: 30 minutes.
    """,
    [
        "Apply the `*_data()` + `plot_*()` pattern that every OpenPyTEA visualization follows.",
        "Produce stacked-bar breakdowns of direct costs, fixed capital, variable and fixed OPEX, and levelized cost, for one plant or several side by side.",
        "Read a cumulative cash-flow diagram: maximum investment, break-even point, final cumulative value.",
        "Run a one-way sensitivity analysis on a price, a financial assumption, or a process quantity, and read the break-even point off the curve.",
        "Rank cost drivers with a tornado plot and know its limitations.",
    ],
    [REF_PAPER, "Van der Spek, M., Roussanaly, S., & Rubin, E.S. (2019). Best practices and recent advances in CCS cost engineering and economic analysis. *IJGGC, 83*, 91-104. https://doi.org/10.1016/j.ijggc.2019.02.006", REF_DOCS],
) + [
    md("## 0) Setup: rebuild the green-ammonia plant from notebooks 01 and 02"),
    SETUP_CELL,
    code(AMMONIA_EQUIPMENT),
    code(AMMONIA_CONFIG),
    md("""
    ## 1) The data + plot pattern

    Every visualization in OpenPyTEA is two functions: a `*_data()` function in `openpytea.analysis` that returns a
    plain dictionary, and a `plot_*()` function in `openpytea.plotting` that draws it with matplotlib. You can
    therefore reuse the numbers in a report or in your own plotting code.

    | Data function | Plot function | Shows |
    |---|---|---|
    | `direct_costs_data` | `plot_stacked_bar` | direct cost per equipment item |
    | `fixed_capital_data` | `plot_stacked_bar` | ISBL, OSBL, D&E, contingency (and additional CAPEX) |
    | `variable_opex_data` | `plot_stacked_bar` | variable OPEX per feed and utility |
    | `fixed_opex_data` | `plot_stacked_bar` | fixed OPEX components |
    | `levelized_cost_data` | `plot_stacked_bar` | LCOP split into discounted CAPEX, OPEX, and by-product credit |
    | `cash_flow_data` | `plot_cash_flow` | cumulative cash flow over the project life |
    | `sensitivity_data` | `plot_sensitivity` | one-way sensitivity curve |
    | `tornado_data` | `plot_tornado` | one-at-a-time ranking of parameters |
    | `monte_carlo` | `plot_monte_carlo`, `plot_multiple_monte_carlo`, `plot_monte_carlo_inputs` | notebook 04 |
    """),
    code("""
    from openpytea.analysis import (direct_costs_data, fixed_capital_data, variable_opex_data,
                                    fixed_opex_data, levelized_cost_data, cash_flow_data,
                                    sensitivity_data, tornado_data)
    from openpytea.plotting import plot_stacked_bar, plot_cash_flow, plot_sensitivity, plot_tornado
    import matplotlib.pyplot as plt
    """),
    md("## 2) Cost breakdowns"),
    code("""
    fig, ax = plot_stacked_bar(direct_costs_data(ammonia_plant))              # equipment-level CAPEX
    fig, ax = plot_stacked_bar(fixed_capital_data(ammonia_plant))             # FCI components
    """),
    code("""
    fig, ax = plot_stacked_bar(variable_opex_data(ammonia_plant))             # feeds and utilities
    fig, ax = plot_stacked_bar(fixed_opex_data(ammonia_plant, pct=True))      # fixed OPEX as percentages
    """),
    code("""
    # Where does the levelized cost come from? Discounted CAPEX vs. OPEX (by-product credits would appear as negative bars)
    lcop_breakdown = levelized_cost_data(ammonia_plant)
    fig, ax = plot_stacked_bar(lcop_breakdown)
    """),
    md("""
    Passing a **list of plants** puts one bar per plant side by side. Let us compare the base case with the
    cheaper-hydrogen variant from notebook 02:
    """),
    code("""
    from copy import deepcopy

    cheap_h2 = deepcopy(ammonia_plant)
    cheap_h2.update_configuration({"plant_name": "Cheaper H2", "variable_opex_inputs": {"hydrogen": {"price": 1.50}}})
    cheap_h2.calculate_all()

    fig, ax = plot_stacked_bar(levelized_cost_data([ammonia_plant, cheap_h2]))
    fig, ax = plot_stacked_bar(variable_opex_data([ammonia_plant, cheap_h2]))
    """),
    md("""
    ## 3) Cumulative cash-flow diagram

    The diagram shows the dip into debt during construction, the point of maximum investment, the break-even year,
    and the final cumulative position. The returned dictionary carries these numbers so you can quote them directly.
    """),
    code("""
    cash_flow = cash_flow_data([ammonia_plant, cheap_h2])
    fig, ax = plot_cash_flow(cash_flow)

    for curve in cash_flow["curves"]:
        print(f"{curve['plant']:<20} max investment {curve['max_investment']:>14,.0f} USD in year {curve['max_investment_year']:.0f}; "
              f"payback after {curve['payback_time']:.1f} years")
    """),
    md("""
    ## 4) One-way sensitivity curves

    `sensitivity_data()` varies **one** parameter by ± a fraction of its base value, recalculates the plant at each
    point, and returns the curve of the chosen `metric` (`LCOP`, `NPV`, `IRR`, `ROI`, or `PBT`). The parameter can be:

    - a price: `"hydrogen"`, `"electricity"`, `"ammonia"` (any `variable_opex_inputs` or `plant_products` key)
    - a financial assumption: `"fixed_capital"`, `"fixed_opex"`, `"interest_rate"`, `"project_lifetime"`, `"plant_utilization"`, `"tax_rate"`, `"operator_hourly_rate"`
    - a process quantity: `"hydrogen.consumption"`, `"ammonia.production"`
    """),
    code("""
    h2_sensitivity = sensitivity_data(ammonia_plant, parameter="hydrogen", plus_minus_value=0.5, metric="LCOP",
                                      label="Levelized cost of ammonia / [USD/kg]")
    fig, ax = plot_sensitivity(h2_sensitivity)
    """),
    code("""
    # Several plants on one figure, and a profitability metric this time
    npv_vs_price = sensitivity_data([ammonia_plant, cheap_h2], parameter="ammonia", plus_minus_value=0.3,
                                    metric="NPV", n_points=31)
    fig, ax = plot_sensitivity(npv_vs_price)
    """),
    md("""
    The returned dictionary has one entry per plant under `"curves"`, each with the relative change `x` (in %) and
    the metric `y`. With `numpy.interp` we can read the break-even point off the curve:
    """),
    code("""
    import numpy as np

    curve = npv_vs_price["curves"][0]                       # base-case plant
    x_pct, npv = np.asarray(curve["x"]), np.asarray(curve["y"])
    breakeven_pct = np.interp(0.0, npv, x_pct)              # NPV increases with price, so interpolation is valid
    base_price = ammonia_plant.plant_products["ammonia"]["price"]
    print(f"NPV = 0 at {breakeven_pct:+.1f} % of the base price, i.e. {base_price * (1 + breakeven_pct / 100):.3f} USD/kg")
    """),
    md("""
    ## 5) Tornado plots

    A tornado plot varies every parameter one at a time by the same ± fraction and ranks them by the swing they
    cause in the metric. It is the quickest way to see which inputs deserve better data. By default it covers prices
    and financial assumptions; `include_process_params=True` adds consumption and production quantities.
    """),
    code("""
    fig, ax = plot_tornado(tornado_data(ammonia_plant, plus_minus_value=0.3, metric="LCOP"))
    """),
    code("""
    fig, ax = plot_tornado(tornado_data(ammonia_plant, plus_minus_value=0.3, metric="NPV", include_process_params=True))
    """),
    md("""
    > **A caveat.** Varying `Ammonia prod.` alone while hydrogen and nitrogen consumption stay fixed is not a
    > physically reachable state: less ammonia means less hydrogen consumed. Treat process-parameter bars as upper
    > bounds on their isolated leverage. Notebook 04 shows how to declare such dependencies so that the sweep
    > respects them.

    ## 6) Exercise 5: at what electricity price does the project stop being profitable?

    1. Run a one-way sensitivity of the **NPV** to the **electricity price** over ± 100 % (`plus_minus_value=1.0`, `n_points=41`).
    2. Plot it, then use `numpy.interp` on the returned curve to find the electricity price at which NPV = 0.
       Watch the direction: NPV *decreases* with price, so flip the arrays (`npv[::-1]`, `x[::-1]`) before interpolating.
    3. Compare with the hydrogen price: run the same analysis for `"hydrogen"` with `plus_minus_value=0.3`. Which of
       the two feeds is the project more exposed to, in relative terms?
    """),
    code("""
    # YOUR CODE HERE
    """),
    md("""
    <details>
    <summary><b>Solution</b> (click to expand)</summary>

    ```python
    def breakeven_price(plant, parameter, plus_minus_value, n_points=41):
        data = sensitivity_data(plant, parameter=parameter, plus_minus_value=plus_minus_value, metric="NPV", n_points=n_points)
        curve = data["curves"][0]
        x, npv = np.asarray(curve["x"]), np.asarray(curve["y"])
        pct = np.interp(0.0, npv[::-1], x[::-1])             # NPV falls as an input price rises
        base = plant.variable_opex_inputs[parameter]["price"]
        return data, pct, base * (1 + pct / 100)

    for parameter, pm in [("electricity", 1.0), ("hydrogen", 0.3)]:
        data, pct, price = breakeven_price(ammonia_plant, parameter, pm)
        fig, ax = plot_sensitivity(data)
        print(f"{parameter}: NPV = 0 at {pct:+.1f} % of the base price -> {price:.3f} USD/unit")
    ```

    The electricity price has to rise by about 30 % (to roughly 0.10 USD/kWh) before the NPV turns negative, while a
    hydrogen price increase of only about 4 % (to roughly 2.08 USD/kg) already does it. In relative terms the project
    is far more exposed to the hydrogen price.
    </details>
    """),
    md("""
    ## 7) Exercise 6: make it publication-ready

    Every plot function accepts `show=False` and returns `(fig, ax)`, so you can restyle it with matplotlib. Take the
    variable OPEX comparison of the two plants, give it a title, remove the top and right spines, and save it as a
    PNG at 300 dpi with `fig.savefig(...)`.
    """),
    code("""
    # YOUR CODE HERE
    """),
    md("""
    <details>
    <summary><b>Solution</b> (click to expand)</summary>

    ```python
    fig, ax = plot_stacked_bar(variable_opex_data([ammonia_plant, cheap_h2]), show=False)
    ax.set_title("Variable OPEX: base case vs. cheaper hydrogen")
    ax.spines[["right", "top"]].set_visible(False)
    fig.tight_layout()
    fig.savefig("variable_opex_comparison.png", dpi=300, bbox_inches="tight")
    plt.show()
    ```
    </details>
    """),
    md("""
    ## Recap

    - `*_data()` returns numbers, `plot_*()` draws them; pass a list of plants to compare.
    - The cash-flow diagram gives maximum investment and payback at a glance.
    - One-way sensitivity curves answer "at what price does this break even?"; tornado plots rank the drivers.
    - Both are deterministic and vary one input at a time. The next notebook varies them all at once.

    **Next:** [04 - Monte Carlo uncertainty analysis](04_monte_carlo_uncertainty.ipynb)
    """),
]

# ======================================================================================
# 04 - Monte Carlo
# ======================================================================================
nb04 = nbf.v4.new_notebook()
nb04.cells = header(
    "04_monte_carlo_uncertainty.ipynb",
    "04 - Monte Carlo uncertainty analysis",
    """
    Prices, capital estimates, and process quantities are uncertain, and they are uncertain **at the same time**.
    Monte Carlo simulation samples all of them from probability distributions, recomputes the plant thousands of
    times, and returns distributions of NPV, levelized cost, and the other metrics instead of single numbers.

    Expected time: 25 minutes.
    """,
    [
        "Attach uncertainty distributions to prices, process quantities, the operator rate, and project-level factors.",
        "Run `monte_carlo()` and plot the resulting distributions of LCOP and NPV.",
        "Extract percentiles and probabilities (for example P(NPV > 0)) from the raw samples.",
        "Check the sampled inputs, and compare two plants under uncertainty.",
        "Declare dependencies between parameters so that Monte Carlo, sensitivity, and tornado analyses respect the process.",
    ],
    [REF_PAPER, "Van der Spek, M., Roussanaly, S., & Rubin, E.S. (2019). Best practices and recent advances in CCS cost engineering and economic analysis. *IJGGC, 83*, 91-104. https://doi.org/10.1016/j.ijggc.2019.02.006", REF_DOCS],
) + [
    md("## 0) Setup: rebuild the green-ammonia plant"),
    SETUP_CELL,
    code(AMMONIA_EQUIPMENT),
    code(AMMONIA_CONFIG),
    code("""
    import numpy as np
    from copy import deepcopy
    from openpytea.analysis import monte_carlo, tornado_data, sensitivity_data
    from openpytea.plotting import (plot_monte_carlo, plot_multiple_monte_carlo, plot_monte_carlo_inputs,
                                    plot_tornado, plot_sensitivity)
    """),
    md("""
    ## 1) Describing what you do not know

    Uncertainty is configured **per item**, in the same configuration dictionary:

    | Where | Key | Samples |
    |---|---|---|
    | any `variable_opex_inputs` or `plant_products` entry | `price_uncertainty` | the price |
    | any `variable_opex_inputs` entry | `consumption_uncertainty` | the daily consumption |
    | any `plant_products` entry | `production_uncertainty` | the daily production |
    | `operator_hourly_rate` | `rate_uncertainty` | the operator wage |
    | top level | `project_uncertainties` | `fixed_capital_factor`, `fixed_opex_factor`, `project_lifetime`, `interest_rate`, `plant_utilization`, `tax_rate` |

    Each uncertainty block takes `std`, `min`, and `max` (a **truncated normal** around the base value by default), or
    a `dist_id` to pick another `scipy.stats` family: 2 lognormal, 3 normal, 4 uniform, 5 triangular, 7 discrete
    uniform, 9 gamma, 10 beta, 12 Student's t, and more (see the Analysis user guide). The four project-level factors
    `fixed_capital_factor` (std 0.3), `fixed_opex_factor` (std 0.3), `project_lifetime` (std 5 years), and
    `interest_rate` (std 0.03) are sampled **by default**; set `"std": 0` to freeze one.
    """),
    code("""
    ammonia_plant.update_configuration({
        "plant_products": {
            "ammonia": {"price_uncertainty": {"dist_id": 5, "min": 0.70, "max": 1.25}},            # triangular, mode at the base price 0.95
        },
        "variable_opex_inputs": {
            "hydrogen":    {"price_uncertainty": {"std": 0.50, "min": 1.0, "max": 4.0}},          # truncated normal
            "electricity": {"price_uncertainty": {"std": 0.03, "min": 0.02, "max": 0.20}},
            "nitrogen":    {"price_uncertainty": {"std": 0.01, "min": 0.02, "max": 0.10}},
        },
        "operator_hourly_rate": {"rate": 38.11, "rate_uncertainty": {"std": 8, "min": 25, "max": 60}},
        "project_uncertainties": {
            "fixed_capital_factor": {"std": 0.30, "min": 0.6, "max": 1.6},   # +-30 % class-4 estimate accuracy
            "fixed_opex_factor":    {"std": 0.15, "min": 0.7, "max": 1.3},
            "interest_rate":        {"std": 0.015, "min": 0.04, "max": 0.12},
            "project_lifetime":     {"std": 0},                              # frozen at 20 years
            "plant_utilization":    {"dist_id": 4, "min": 0.80, "max": 0.95},  # uniform, opt-in
        },
    })
    """),
    md("""
    ## 2) Running the simulation

    20 000 samples take a couple of seconds for this plant. Increase `num_samples` for smoother histograms;
    `batch_size` only controls memory use. `random_seed` makes the run reproducible.
    """),
    code("""
    mc_base = monte_carlo(ammonia_plant, num_samples=20_000, batch_size=5_000, random_seed=2026)

    fig, ax = plot_monte_carlo(mc_base, metric="LCOP", bins=40, label="Levelized cost of ammonia / [USD/kg]")
    fig, ax = plot_monte_carlo(mc_base, metric="NPV", bins=40)
    """),
    md("""
    The result is a dictionary with the raw samples under `"metrics"` (`LCOP`, `NPV`, `ROI`, `PBT`) and the sampled
    inputs under `"inputs"`. Percentiles and probabilities are one line of numpy away:
    """),
    code("""
    lcop = np.asarray(mc_base["metrics"]["LCOP"])
    npv = np.asarray(mc_base["metrics"]["NPV"])

    p10, p50, p90 = np.percentile(lcop, [10, 50, 90])
    print(f"LCOP  P10 / P50 / P90 : {p10:.3f} / {p50:.3f} / {p90:.3f} USD/kg   (deterministic: {ammonia_plant.levelized_cost:.3f})")
    print(f"P(NPV > 0)            : {np.mean(npv > 0):.1%}")
    print(f"P(LCOP < 0.95 USD/kg) : {np.mean(lcop < 0.95):.1%}")
    """),
    md("""
    ## 3) Always look at the inputs

    `plot_monte_carlo_inputs()` shows the sampled distributions, split into **process** quantities and **economic**
    parameters. Inputs without an uncertainty block appear as a single bar at their fixed value, so you see what
    varies and what does not.
    """),
    code("""
    fig, axes = plot_monte_carlo_inputs(mc_base, category="economic", bins=40)
    """),
    md("""
    ## 4) Comparing two plants under uncertainty

    A deterministic comparison gives one number per design; Monte Carlo tells you how often the ranking holds.
    Let us compare the base case with a design that pays about 7 % more capital for a converter with 5 % lower
    hydrogen consumption. Deterministically the two levelized costs differ by less than 0.01 USD/kg.
    """),
    code("""
    efficient = deepcopy(ammonia_plant)
    efficient.update_configuration({
        "plant_name": "Efficient converter",
        "fixed_capital_factors": {"contingency": 0.20},                         # contingency 10 % -> 20 %, about +7 % FCI
        "variable_opex_inputs": {"hydrogen": {"consumption": 17_800 * 0.95}},
    })
    efficient.calculate_all()
    mc_efficient = monte_carlo(efficient, num_samples=20_000, batch_size=5_000, random_seed=2026)

    fig, ax = plot_multiple_monte_carlo([mc_base, mc_efficient], metric="LCOP", bins=40,
                                        label="Levelized cost of ammonia / [USD/kg]")
    print(f"Deterministic LCOP: {ammonia_plant.levelized_cost:.3f} vs {efficient.levelized_cost:.3f} USD/kg")
    print(f"P(efficient design is cheaper): {np.mean(np.asarray(mc_efficient['metrics']['LCOP']) < lcop):.1%}")
    """),
    md("""
    ## 5) Dependencies between parameters

    So far every input was sampled independently. In reality the hydrogen and nitrogen consumption follow the
    ammonia production (stoichiometry), and the electricity consumption follows it too. OpenPyTEA lets you declare
    such links as a small graph: `dependent = Σ wᵢ · parentᵢ + offset`. Because the dependency lives on the plant,
    Monte Carlo, `sensitivity_data()`, and `tornado_data()` all honour it, and a dependent can no longer be varied on
    its own.
    """),
    code("""
    ammonia_plant.update_configuration({
        "plant_products": {
            "ammonia": {"production_uncertainty": {"std": 5_000, "min": 85_000, "max": 110_000}},   # the root of the graph
        },
        "variable_opex_inputs": {
            "hydrogen":    {"consumption_dependency": {"depends_on": {"production:ammonia": 17_800 / 100_000}}},
            "nitrogen":    {"consumption_dependency": {"depends_on": {"production:ammonia": 82_400 / 100_000}}},
            "electricity": {"consumption_dependency": {"depends_on": {"production:ammonia": 60_000 / 100_000}}},
        },
    })

    mc_linked = monte_carlo(ammonia_plant, num_samples=20_000, batch_size=5_000, random_seed=2026)
    fig, axes = plot_monte_carlo_inputs(mc_linked, category="process", bins=40)
    """),
    code("""
    # The tornado now sweeps ammonia production together with the feeds it drives, and drops the dependents as separate bars
    fig, ax = plot_tornado(tornado_data(ammonia_plant, plus_minus_value=0.3, metric="NPV", include_process_params=True))
    """),
    md("""
    ## 6) Exercise 7: how much would better cost data be worth?

    The capital cost estimate is the largest single uncertainty (`fixed_capital_factor`, ± 30 %). Suppose a detailed
    engineering study could narrow it to ± 10 %.

    1. Copy `ammonia_plant`, set `project_uncertainties.fixed_capital_factor` to `{"std": 0.10, "min": 0.8, "max": 1.2}`,
       and rerun Monte Carlo with the same seed.
    2. Compare P10 / P90 of the NPV and P(NPV > 0) before and after. How much of the NPV spread was due to the capital estimate?
    3. Bonus: repeat for the hydrogen price (`std` 0.5 to 0.2). Which piece of information would you buy first?
    """),
    code("""
    # YOUR CODE HERE
    """),
    md("""
    <details>
    <summary><b>Solution</b> (click to expand)</summary>

    ```python
    def summarize(mc, name):
        npv = np.asarray(mc["metrics"]["NPV"])
        p10, p90 = np.percentile(npv, [10, 90])
        print(f"{name:<28} NPV P10 {p10/1e6:>7.1f}  P90 {p90/1e6:>6.1f} MUSD   spread {(p90-p10)/1e6:>6.1f} MUSD   P(NPV>0) {np.mean(npv>0):.1%}")

    summarize(mc_linked, "base uncertainties")

    better_capex = deepcopy(ammonia_plant)
    better_capex.update_configuration({"project_uncertainties": {"fixed_capital_factor": {"std": 0.10, "min": 0.8, "max": 1.2}}})
    summarize(monte_carlo(better_capex, num_samples=20_000, batch_size=5_000, random_seed=2026), "capex +-10 %")

    better_h2 = deepcopy(ammonia_plant)
    better_h2.update_configuration({"variable_opex_inputs": {"hydrogen": {"price_uncertainty": {"std": 0.20, "min": 1.0, "max": 4.0}}}})
    summarize(monte_carlo(better_h2, num_samples=20_000, batch_size=5_000, random_seed=2026), "hydrogen price std 0.2")
    ```

    Both refinements narrow the NPV spread by roughly 10 %, and neither changes P(NPV > 0) much: the remaining spread
    comes from the ammonia price and the other inputs sampled at the same time. Narrowing the hydrogen price helps
    slightly more than narrowing the capital estimate, so a long-term hydrogen supply contract is the first thing to
    secure. Note that the hydrogen and ammonia prices are sampled independently here; in reality they are
    correlated, which is exactly the kind of link the dependency mechanism above can express.
    </details>
    """),
    md("""
    ## Recap

    - Uncertainty blocks (`price_uncertainty`, `consumption_uncertainty`, `production_uncertainty`, `rate_uncertainty`, `project_uncertainties`) live next to the values they describe.
    - `monte_carlo()` returns raw samples; percentiles and probabilities are yours to compute.
    - Look at the inputs, compare plants with `plot_multiple_monte_carlo()`, and declare dependencies so the sweeps stay physical.

    **Next:** [05 - Case study: hydrogen production pathways](05_case_study_hydrogen.ipynb)
    """),
]

# ======================================================================================
# 05 - Capstone case study
# ======================================================================================
nb05 = nbf.v4.new_notebook()
nb05.cells = header(
    "05_case_study_hydrogen.ipynb",
    "05 - Case study: steam methane reforming vs. water electrolysis",
    f"""
    Time to put everything together. Two plants each produce **50 t of hydrogen per day** on the US Gulf Coast:
    a **steam methane reforming (SMR)** plant sized from an Aspen Plus simulation, and a pressurized **alkaline
    water electrolysis (WE)** plant costed from a US DOE report. You will build both, compare their cost
    structures, find the CO₂ tax at which electrolysis becomes competitive, and compare the two under uncertainty.

    The data are adapted from case study 1 of the OpenPyTEA repository (Tamarona et al., 2026), where a third
    pathway, methane pyrolysis, is also analysed.

    Expected time: 35 minutes. The SMR plant is given; the electrolysis plant and the comparison are exercises.
    Each exercise is followed by a solution cell so that the notebook can always be run to the end.
    """,
    [
        "Translate a process flowsheet and a sizing table into an OpenPyTEA equipment list and plant configuration.",
        "Handle equipment given as vendor quotes, periodic replacement CAPEX, and a manual operator count.",
        "Compare two technologies with breakdown charts, cash-flow diagrams, and sensitivity curves.",
        "Find a policy break-even point (the CO₂ tax that equalizes the levelized cost of hydrogen).",
        "Quantify the probability that one technology is cheaper than the other.",
    ],
    [
        REF_PAPER,
        "Acevedo, Y.M., Prosser, J.H., Huya-Kouadio, J.M., McNamara, K.R., & James, B.D. (2023). *Hydrogen Production Cost with Alkaline Electrolysis*. DOE-SA-09629-1, Strategic Analysis Inc. https://doi.org/10.2172/2203367",
        "Boyano, A., Blanco-Marigorta, A.M., Morosuk, T., & Tsatsaronis, G. (2011). Exergoenvironmental analysis of a steam methane reforming process for hydrogen production. *Energy, 36*(4), 2202-2214. https://doi.org/10.1016/j.energy.2010.05.020",
    ],
) + [
    md("## 0) Setup"),
    SETUP_CELL,
    code("""
    import numpy as np
    import pandas as pd
    from copy import deepcopy
    from openpytea import Equipment, Plant
    from openpytea.analysis import (fixed_capital_data, variable_opex_data, fixed_opex_data, levelized_cost_data,
                                    direct_costs_data, cash_flow_data, sensitivity_data, tornado_data, monte_carlo)
    from openpytea.plotting import (plot_stacked_bar, plot_cash_flow, plot_sensitivity, plot_tornado,
                                    plot_monte_carlo, plot_multiple_monte_carlo)
    """),
    md("""
    ## 1) Common assumptions

    Both plants share the location, financing, and price assumptions below. Prices carry an uncertainty block
    straight away so that the Monte Carlo comparison at the end needs no extra configuration.
    """),
    code("""
    country, region   = "United States", "Gulf Coast"
    interest_rate     = 0.09
    project_lifetime  = 30          # years
    plant_utilization = 0.95
    tax_rate          = 0.25

    h2_production = 50_000          # kg/day (50 t/day)
    h2_price      = 5.0             # USD/kg

    operator_rate = {"rate": 38.11, "rate_uncertainty": {"std": 10, "min": 25, "max": 50}}          # USD/h

    # Prices with their uncertainty: (base, std, min, max)
    electricity_price   = {"price": 0.05,      "price_uncertainty": {"std": 0.03,  "min": 0.01,  "max": 3.0}}     # USD/kWh
    natural_gas_price   = {"price": 0.40,      "price_uncertainty": {"std": 0.25,  "min": 0.0,   "max": 5.0}}     # USD/kg
    cooling_water_price = {"price": 2.4592e-4, "price_uncertainty": {"std": 1e-4,  "min": 1e-5,  "max": 4e-4}}    # USD/MJ
    co2_tax             = {"price": 0.075,     "price_uncertainty": {"std": 0.02,  "min": 0.0,   "max": 0.15}}    # USD/kg CO2
    water_price         = {"price": 0.003,     "price_uncertainty": {"std": 0.001, "min": 0.0,   "max": 0.005}}   # USD/kg
    """),
    md(f"""
    ## 2) Steam methane reforming (given)

    Methane is reformed with steam at 700 °C over a nickel catalyst, the syngas is shifted in high- and
    low-temperature water-gas-shift reactors, and hydrogen is recovered by pressure-swing adsorption. The tail gas
    and extra methane fire the reformer furnace.

    ![SMR flowsheet]({PKG_IMG}/CS_2-Fig_1.png)

    The sizes below come from the Aspen Plus simulation shipped with the OpenPyTEA repository.
    """),
    code("""
    # Compressors and their electric motors (90 % motor efficiency)
    comp_1 = Equipment("COMP-1", 945, "Fluids", "Compressors, fans, & blowers", "Compressor, centrifugal", "Carbon steel")
    comp_2 = Equipment("COMP-2", 491, "Fluids", "Compressors, fans, & blowers", "Compressor, centrifugal", "Carbon steel")
    mtr_1  = Equipment("MTR-1", 945 / 0.9, "Electrical", "Motors & generators", "Totally enclosed motor", "Carbon steel")
    mtr_2  = Equipment("MTR-2", 491 / 0.9, "Electrical", "Motors & generators", "Totally enclosed motor", "Carbon steel")

    # Heat exchangers (m2)
    hx_1   = Equipment("HX-1",   31.87,  "Fluids", "Heat Exchangers", "U-tube shell & tube", "304 stainless steel")
    hx_2   = Equipment("HX-2",   22.74,  "Fluids", "Heat Exchangers", "U-tube shell & tube", "304 stainless steel")
    hx_3   = Equipment("HX-3",   107.19, "Fluids", "Heat Exchangers", "U-tube shell & tube", "304 stainless steel")
    cooler = Equipment("COOLER", 191.47, "Fluids", "Heat Exchangers", "U-tube shell & tube", "Carbon steel")

    # Reactors (shell mass, kg) and furnace (duty, kW), pump (L/s)
    smr_reactor    = Equipment("SMR-REACTOR",    160,     "Fluids", "Reactors", "Tubular fixed bed", "304 stainless steel")
    wgs_ht_reactor = Equipment("WGS-HT-REACTOR", 376.54,  "Fluids", "Reactors", "Tubular fixed bed", "304 stainless steel")
    wgs_lt_reactor = Equipment("WGS-LT-REACTOR", 3822.92, "Fluids", "Reactors", "Tubular fixed bed", "304 stainless steel")
    furnace = Equipment("FURNACE", 33.26, "Fluids", "Boilers, heaters, & furnaces", "Furnace, cylindrical", "304 stainless steel")
    pump    = Equipment("PUMP",    5.16,  "Fluids", "Pumps", "Single-stage centrifugal", "Carbon steel")

    # PSA: no verified correlation in the database, so a literature cost (1994 USD) is entered directly
    psa = Equipment("PSA", 1023.49, "Fluids", "Adsorption & membrane separation", "Pressure-swing adsorber",
                    "Carbon steel", purchased_cost=284_692.37, cost_year=1994)

    smr_equipment = [comp_1, mtr_1, comp_2, mtr_2, hx_1, hx_2, hx_3, cooler,
                     smr_reactor, wgs_ht_reactor, wgs_lt_reactor, furnace, pump, psa]
    """),
    code("""
    smr_plant = Plant({
        "plant_name": "Steam methane reforming",
        "process_type": "Fluids",
        "country": country, "region": region,
        "equipment": smr_equipment,
        "interest_rate": interest_rate, "project_lifetime": project_lifetime,
        "plant_utilization": plant_utilization, "tax_rate": tax_rate,
        "operator_hourly_rate": operator_rate,
        "plant_products": {
            "hydrogen": {"production": h2_production, "price": h2_price},
        },
        "variable_opex_inputs": {                                           # daily quantities from the simulation
            "electricity":   {"consumption": (945 + 491) / 0.9 * 24, **electricity_price},    # kWh/day
            "methane_feed":  {"consumption": (5139 + 4025) * 24,     **natural_gas_price},    # kg/day, feed + fuel
            "cooling_water": {"consumption": 20_222.67 * 24,         **cooling_water_price},  # MJ/day
            "CO2_tax":       {"consumption": 25_124.64 * 24,         **co2_tax},              # kg CO2/day emitted
        },
    })
    smr_plant.calculate_all()
    print(f"SMR  FCI {smr_plant.fixed_capital/1e6:6.1f} MUSD   LCOH {smr_plant.levelized_cost:.2f} USD/kg   NPV {smr_plant.npv/1e6:7.1f} MUSD   IRR {smr_plant.irr:.1%}")
    """),
    md(f"""
    ## 3) Exercise 8: build the water-electrolysis plant

    The DOE report describes a pressurized alkaline system (about 30 bar) delivering 99.99 % hydrogen without
    downstream compression.

    ![WE flowsheet]({PKG_IMG}/CS_2-Fig_3.png)

    Instead of sized units, the report gives **system costs** (2020 USD): stack 17.194 MUSD, mechanical balance of
    plant 11.019 MUSD, electrical balance of plant 16.974 MUSD. The system consumes **98 MW** of electricity and
    **3.78 kg of water per kg H₂ twice over** (process plus cooling make-up, so 3.78 × 2 × 50 000 kg/day).

    **Tasks**
    1. Create three `Equipment` items from the quotes (`purchased_cost=..., cost_year=2020`, `param=0`). Use
       `process_type="Electrical"` for the electrical balance of plant and `"Fluids"` for the other two, `category="Electrolysis"`.
    2. Create `we_plant` with the common assumptions, `process_type="Fluids"`, hydrogen as product, and electricity
       and water as variable OPEX inputs (reuse `electricity_price` and `water_price`).
    3. The automatic operator estimate counts equipment items, which is meaningless for three "systems". The
       flowsheet has 11 fluid process steps: compute `we_plant.calculate_operators_hired(no_fluid_process=11, no_solid_process=0)`
       and set it with `update_configuration({{"operators_hired": ...}})`.
    4. The stack lasts 10 years, so it is replaced in years 10 and 20: set `additional_capex_cost` to the stack's
       (escalated) purchased cost twice and `additional_capex_years` to `[10, 20]`.
    5. Run `we_plant.calculate_all(additional_capex=True)` and print FCI, LCOH, NPV, and IRR as for SMR.
    """),
    code("""
    # YOUR CODE HERE
    """),
    md("**Solution** (run this cell to continue even if you did not finish the exercise):"),
    code("""
    stack          = Equipment("Stack",          0, "Fluids",     "Electrolysis", "Stack",      "Carbon steel", purchased_cost=17_194_000, cost_year=2020)
    mechanical_bop = Equipment("Mechanical BOP", 0, "Fluids",     "Electrolysis", "Mechanical", "Carbon steel", purchased_cost=11_019_000, cost_year=2020)
    electrical_bop = Equipment("Electrical BOP", 0, "Electrical", "Electrolysis", "Electrical", "Carbon steel", purchased_cost=16_974_000, cost_year=2020)
    we_equipment = [stack, mechanical_bop, electrical_bop]

    we_plant = Plant({
        "plant_name": "Water electrolysis",
        "process_type": "Fluids",
        "country": country, "region": region,
        "equipment": we_equipment,
        "interest_rate": interest_rate, "project_lifetime": project_lifetime,
        "plant_utilization": plant_utilization, "tax_rate": tax_rate,
        "operator_hourly_rate": operator_rate,
        "plant_products": {"hydrogen": {"production": h2_production, "price": h2_price}},
        "variable_opex_inputs": {
            "electricity": {"consumption": 98 * 1000 * 24, **electricity_price},     # kWh/day
            "water":       {"consumption": 3.78 * 2 * h2_production, **water_price},   # kg/day
        },
    })

    operators = we_plant.calculate_operators_hired(no_fluid_process=11, no_solid_process=0)
    we_plant.update_configuration({
        "operators_hired": operators,
        "additional_capex_cost": [stack.purchased_cost, stack.purchased_cost],
        "additional_capex_years": [10, 20],
    })
    we_plant.calculate_all(additional_capex=True)
    print(f"Operators hired: {operators}")
    print(f"WE   FCI {we_plant.fixed_capital/1e6:6.1f} MUSD   LCOH {we_plant.levelized_cost:.2f} USD/kg   NPV {we_plant.npv/1e6:7.1f} MUSD   IRR {we_plant.irr:.1%}")
    """),
    md("""
    ## 4) Comparing cost structures

    Pass both plants as a list. For the electrolysis plant, `additional_capex=True` includes the stack replacements
    in the capital breakdown.
    """),
    code("""
    plants = [smr_plant, we_plant]
    fig, ax = plot_stacked_bar(fixed_capital_data(plants, additional_capex=True))
    fig, ax = plot_stacked_bar(variable_opex_data(plants))
    fig, ax = plot_stacked_bar(levelized_cost_data(plants))
    """),
    code("""
    fig, ax = plot_stacked_bar(direct_costs_data(smr_plant, pct=True))    # what drives the SMR capital cost?
    fig, ax = plot_cash_flow(cash_flow_data(plants))
    """),
    md("""
    > Electrolysis is dominated by capital and electricity; reforming by the methane feed and, to a lesser extent,
    > the CO₂ tax. At today's assumptions SMR produces hydrogen at about 4 USD/kg and electrolysis at about
    > 7.5 USD/kg.

    ## 5) Sensitivity: what would change the ranking?
    """),
    code("""
    fig, ax = plot_sensitivity(sensitivity_data(plants, parameter="electricity", plus_minus_value=0.6, metric="LCOP",
                                                label="Levelized cost of hydrogen / [USD/kg]", n_points=31))
    fig, ax = plot_sensitivity(sensitivity_data(plants, parameter="interest_rate", plus_minus_value=0.6, metric="NPV", n_points=31))
    """),
    code("""
    fig, ax = plot_tornado(tornado_data(we_plant, plus_minus_value=0.3, metric="LCOP", additional_capex=True))
    fig, ax = plot_tornado(tornado_data(smr_plant, plus_minus_value=0.3, metric="LCOP"))
    """),
    md("""
    ## 6) Exercise 9: the CO₂ tax that levels the field

    The SMR plant emits about 12 kg CO₂ per kg H₂. At what CO₂ tax (USD per kg CO₂) does the levelized cost of
    hydrogen from SMR equal that of electrolysis?

    Sweep the tax from 0 to 0.5 USD/kg CO₂ in steps of 0.025: for each value, `deepcopy(smr_plant)`, update
    `variable_opex_inputs.CO2_tax.price`, run `calculate_levelized_cost()`, and store the result. Then plot LCOH
    versus tax for SMR together with a horizontal line at the electrolysis LCOH, and interpolate the crossing with
    `numpy.interp`. Express the answer also in USD per tonne CO₂.
    """),
    code("""
    # YOUR CODE HERE
    """),
    md("**Solution:**"),
    code("""
    import matplotlib.pyplot as plt

    taxes = np.arange(0, 0.501, 0.025)
    smr_lcoh = []
    for tax in taxes:
        p = deepcopy(smr_plant)
        p.update_configuration({"variable_opex_inputs": {"CO2_tax": {"price": float(tax)}}})
        p.calculate_levelized_cost()
        smr_lcoh.append(p.levelized_cost)
    smr_lcoh = np.asarray(smr_lcoh)

    breakeven_tax = np.interp(we_plant.levelized_cost, smr_lcoh, taxes)
    print(f"Break-even CO2 tax: {breakeven_tax:.3f} USD/kg CO2 = {breakeven_tax*1000:.0f} USD/t CO2")

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(taxes, smr_lcoh, label="SMR")
    ax.axhline(we_plant.levelized_cost, color="tab:orange", ls="--", label="Electrolysis")
    ax.axvline(breakeven_tax, color="grey", ls=":")
    ax.set_xlabel("CO$_2$ tax / [USD/kg CO$_2$]"); ax.set_ylabel("LCOH / [USD/kg H$_2$]"); ax.legend()
    plt.show()
    """),
    md("""
    ## 7) Exercise 10: which one is cheaper, and how sure are we?

    Every price already carries an uncertainty block, and the default project-level uncertainties are active.

    1. Run `monte_carlo` on both plants with 20 000 samples and the same `random_seed` (pass `additional_capex=True` for electrolysis).
    2. Plot both LCOH distributions on one figure with `plot_multiple_monte_carlo`.
    3. Compute the probability that electrolysis is cheaper than SMR: `np.mean(lcoh_we < lcoh_smr)`.
    4. Bonus: what is the probability if the electricity price is a long-term contract at 0.02 USD/kWh with `std` 0.005?
    """),
    code("""
    # YOUR CODE HERE
    """),
    md("**Solution:**"),
    code("""
    mc_smr = monte_carlo(smr_plant, num_samples=20_000, batch_size=5_000, random_seed=7)
    mc_we  = monte_carlo(we_plant,  num_samples=20_000, batch_size=5_000, random_seed=7, additional_capex=True)

    fig, ax = plot_multiple_monte_carlo([mc_smr, mc_we], metric="LCOP", bins=40,
                                        label="Levelized cost of hydrogen / [USD/kg]")

    lcoh_smr = np.asarray(mc_smr["metrics"]["LCOP"])
    lcoh_we  = np.asarray(mc_we["metrics"]["LCOP"])
    print(f"SMR  LCOH P10/P50/P90: {np.percentile(lcoh_smr, [10, 50, 90]).round(2)}")
    print(f"WE   LCOH P10/P50/P90: {np.percentile(lcoh_we,  [10, 50, 90]).round(2)}")
    print(f"P(electrolysis cheaper than SMR): {np.mean(lcoh_we < lcoh_smr):.1%}")

    cheap_power = deepcopy(we_plant)
    cheap_power.update_configuration({"plant_name": "Water electrolysis, 0.02 USD/kWh PPA",
                                      "variable_opex_inputs": {"electricity": {"price": 0.02, "price_uncertainty": {"std": 0.005, "min": 0.005, "max": 0.05}}}})
    cheap_power.calculate_all(additional_capex=True)
    mc_cheap = monte_carlo(cheap_power, num_samples=20_000, batch_size=5_000, random_seed=7, additional_capex=True)
    fig, ax = plot_multiple_monte_carlo([mc_smr, mc_we, mc_cheap], metric="LCOP", bins=40,
                                        label="Levelized cost of hydrogen / [USD/kg]")
    print(f"P(electrolysis with cheap power cheaper than SMR): {np.mean(np.asarray(mc_cheap['metrics']['LCOP']) < lcoh_smr):.1%}")
    """),
    md("""
    ## 8) Discussion

    Take five minutes with your neighbour:

    - Which three inputs would you spend effort on before showing these results to a decision maker?
    - The comparison uses a **class-4 factorial estimate** for SMR and **vendor-level system costs** for electrolysis. Is that a fair comparison? How would you make the accuracy classes consistent?
    - What does the CO₂ break-even tax tell a policy maker, and what does it hide (for example, upstream methane emissions, electricity carbon intensity, or learning-curve cost reductions of electrolyzers)?

    ## Recap

    You have built two plants from process data, compared their cost structures, identified their drivers, found a
    policy break-even point, and quantified the ranking under uncertainty. That is the complete OpenPyTEA workflow.

    - Keep going with the optional [06 - JSON configuration files and the command line](06_optional_json_and_cli.ipynb).
    - Try the [home assignment](../HOME_ASSIGNMENT.md) on a process of your own.
    - Missing a cost correlation? Contribute it: https://github.com/pbtamarona/OpenPyTEA
    """),
]

# ======================================================================================
# 06 - Optional: JSON and CLI
# ======================================================================================
nb06 = nbf.v4.new_notebook()
nb06.cells = header(
    "06_optional_json_and_cli.ipynb",
    "06 - Optional: JSON configuration files and the command line",
    """
    Everything we did in Python can also be driven by a **JSON configuration file**: equipment, plant, analysis
    settings, and output options in one document. This makes a study reproducible, shareable, and easy to
    version-control, and it lets colleagues without Python run the same assessment from the command line.

    Expected time: 20 minutes (self-study or if time allows).
    """,
    [
        "Read a combined OpenPyTEA JSON configuration file and map its blocks to the Python objects you know.",
        "Run a complete TEA from a file with `run_openpytea()` and reload the exported results with `load_results()`.",
        "Run the same file from the terminal with the `openpytea` command-line tool.",
        "Export a plant you built in Python to JSON.",
    ],
    [REF_DOCS + " (User Guide, Config Files & CLI page)", REF_PAPER],
) + [
    md("## 0) Setup"),
    SETUP_CELL,
    code("""
    # Make sure the example configuration files are available (downloaded from GitHub when running on Colab)
    import os, urllib.request

    os.makedirs("assets", exist_ok=True)
    for name in ["smr_hydrogen.json", "we_hydrogen.json"]:
        if not os.path.exists(f"assets/{name}"):
            urllib.request.urlretrieve(
                f"https://raw.githubusercontent.com/pbtamarona/openpytea-workshop/main/notebooks/assets/{name}",
                f"assets/{name}")
    print(sorted(os.listdir("assets")))
    """),
    md("""
    ## 1) Anatomy of a configuration file

    A combined file has four top-level blocks:

    | Block | Content | Python equivalent |
    |---|---|---|
    | `equipment` | list of items, each with the `Equipment` arguments | notebook 01 |
    | `plant` | the `Plant` configuration dictionary, uncertainty blocks included | notebooks 02 and 04 |
    | `analysis` | which analyses to run and their arguments | notebook 03 and 04 |
    | `output` | whether to save JSON results and plots, in which format | - |

    `assets/smr_hydrogen.json` is the SMR plant of notebook 05 written this way:
    """),
    code("""
    import json

    with open("assets/smr_hydrogen.json") as f:
        smr_config = json.load(f)

    print("Top-level blocks:", list(smr_config))
    print("\\nFirst equipment item:", json.dumps(smr_config["equipment"][0], indent=2))
    print("\\nAnalysis block:", json.dumps(smr_config["analysis"], indent=2)[:900], "...")
    """),
    md("""
    ## 2) Running a study from a file

    `run_openpytea()` builds the equipment and the plant, runs every analysis with `"run": true`, and writes the
    results (and plots, if requested) to the output directory. It returns the same results as a dictionary.
    """),
    code("""
    from openpytea import run_openpytea, load_results

    results = run_openpytea("assets/smr_hydrogen.json", output_dir="outputs/smr")
    print("Result blocks:", list(results))
    print("Files written:", sorted(os.listdir("outputs/smr")))
    """),
    code("""
    # Results are plain JSON, so they can be reloaded later without recomputing anything
    from openpytea.plotting import plot_monte_carlo, plot_tornado

    saved = load_results("outputs/smr/Steam methane reforming_analysis_results.json")
    fig, ax = plot_monte_carlo(saved["monte_carlo"], metric="LCOP", bins=40)
    fig, ax = plot_tornado(saved["tornado"])
    """),
    md("""
    ## 3) The command-line interface

    The same file runs from a terminal, without any Python code:

    ```bash
    openpytea run assets/we_hydrogen.json --output-dir outputs/we
    ```

    `openpytea --help` lists the other commands (`equipment`, `plant`, and `tea` for the three-file layout). Below
    we call it from the notebook through the current Python interpreter, which works even when the `openpytea`
    executable is not on your PATH.
    """),
    code("""
    import subprocess, sys

    completed = subprocess.run([sys.executable, "-m", "openpytea.cli", "run", "assets/we_hydrogen.json",
                                "--output-dir", "outputs/we"], capture_output=True, text=True)
    print(completed.stdout[-1500:])
    print(completed.stderr[-500:])
    print("Files written:", sorted(os.listdir("outputs/we")))
    """),
    code("""
    from openpytea.plotting import plot_multiple_monte_carlo

    we_saved = load_results("outputs/we/Water electrolysis_analysis_results.json")
    fig, ax = plot_multiple_monte_carlo([saved["monte_carlo"], we_saved["monte_carlo"]], metric="LCOP", bins=40,
                                        label="Levelized cost of hydrogen / [USD/kg]")
    """),
    md("""
    ## 4) From Python to JSON

    A `Plant` built interactively can be exported with `to_dict()` and `json.dump`, which is a convenient way to
    freeze the assumptions of a study next to its results.
    """),
    code("""
    from openpytea import Equipment, Plant

    compressor = Equipment(name="C-101", param=1_200, process_type="Fluids",
                           category="Compressors, fans, & blowers", type="Compressor, centrifugal")
    plant = Plant({"plant_name": "Export demo", "process_type": "Fluids", "equipment": [compressor],
                   "plant_products": {"ammonia": {"production": 100_000, "price": 0.85}},
                   "variable_opex_inputs": {"hydrogen": {"consumption": 17_800, "price": 2.0}}})
    plant.calculate_all()

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/export_demo_plant.json", "w") as f:
        json.dump(plant.to_dict(), f, indent=2, default=str)
    print(json.dumps(plant.to_dict(), indent=2, default=str)[:800], "...")
    """),
    md("""
    ## 5) Exercise 11: a scenario file

    1. Load `assets/we_hydrogen.json`, change the electricity price to 0.02 USD/kWh and the plant name to
       `"Water electrolysis, cheap power"`, and save it as `outputs/we_cheap_power.json`.
    2. Run it with `run_openpytea` and compare the Monte Carlo LCOH distribution with the base electrolysis case.
    3. Reduce the Monte Carlo `num_samples` in the file to 5 000 and check how much faster it runs.
    """),
    code("""
    # YOUR CODE HERE
    """),
    md("""
    <details>
    <summary><b>Solution</b> (click to expand)</summary>

    ```python
    with open("assets/we_hydrogen.json") as f:
        cfg = json.load(f)
    cfg["plant"]["plant_name"] = "Water electrolysis, cheap power"
    cfg["plant"]["variable_opex_inputs"]["electricity"]["price"] = 0.02
    cfg["analysis"]["monte_carlo"]["args"]["num_samples"] = 5_000
    with open("outputs/we_cheap_power.json", "w") as f:
        json.dump(cfg, f, indent=2)

    cheap = run_openpytea("outputs/we_cheap_power.json", output_dir="outputs/we_cheap")
    fig, ax = plot_multiple_monte_carlo([we_saved["monte_carlo"], cheap["monte_carlo"]], metric="LCOP", bins=40)
    ```
    </details>
    """),
    md("""
    ## Recap

    - One JSON file = one reproducible study: equipment, plant, analyses, outputs.
    - `run_openpytea()` in Python or `openpytea run` in a terminal give identical results and files.
    - `load_results()` reloads exported results for plotting without recomputation.

    Thank you for taking part in the workshop. Questions and contributions are welcome at
    https://github.com/pbtamarona/OpenPyTEA.
    """),
]

# ======================================================================================
# Write notebooks
# ======================================================================================
KERNEL = {
    "kernelspec": {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "pygments_lexer": "ipython3"},
}
for name, nb in [
    ("00_setup_check.ipynb", nb00),
    ("01_equipment_costing.ipynb", nb01),
    ("02_building_a_plant.ipynb", nb02),
    ("03_cost_breakdowns_and_sensitivity.ipynb", nb03),
    ("04_monte_carlo_uncertainty.ipynb", nb04),
    ("05_case_study_hydrogen.ipynb", nb05),
    ("06_optional_json_and_cli.ipynb", nb06),
]:
    nb.metadata = KERNEL
    nbf.validate(nb)
    nbf.write(nb, OUT / name)
    print("wrote", name, len(nb.cells), "cells")

# ======================================================================================
# JSON assets (combined configuration files for notebook 06)
# ======================================================================================
ANALYSIS_BLOCK = {
    "direct_costs":   {"run": True, "args": {"pct": True}},
    "fixed_capital":  {"run": True, "args": {"additional_capex": False, "pct": False}},
    "fixed_opex":     {"run": True, "args": {"pct": True}},
    "variable_opex":  {"run": True, "args": {"pct": False}},
    "levelized_cost": {"run": True, "args": {"pct": False}},
    "cash_flow":      {"run": True},
    "sensitivity": {
        "run": True,
        "cases": [
            {"name": "electricity_lcop", "args": {"parameter": "electricity", "plus_minus_value": 0.6, "metric": "LCOP"}},
            {"name": "interest_rate_npv", "args": {"parameter": "interest_rate", "plus_minus_value": 0.6, "metric": "NPV"}},
        ],
    },
    "tornado": {"run": True, "args": {"plus_minus_value": 0.3, "metric": "LCOP"}},
    "monte_carlo": {"run": True, "args": {"num_samples": 20000, "batch_size": 5000, "additional_capex": False, "random_seed": 7},
                    "metric": ["LCOP", "NPV"], "plot_inputs": False},
}
OUTPUT_BLOCK = {"save_json": True, "save_plots": True, "plot_format": "png", "dpi": 200}

price = lambda p, std, mn, mx: {"price": p, "price_uncertainty": {"std": std, "min": mn, "max": mx}}
common_plant = {
    "country": "United States", "region": "Gulf Coast",
    "interest_rate": 0.09, "project_lifetime": 30, "plant_utilization": 0.95, "tax_rate": 0.25,
    "operator_hourly_rate": {"rate": 38.11, "rate_uncertainty": {"std": 10, "min": 25, "max": 50}},
    "plant_products": {"hydrogen": {"production": 50000, "price": 5.0}},
}

smr_json = {
    "equipment": [
        {"name": "COMP-1", "param": 945, "process_type": "Fluids", "category": "Compressors, fans, & blowers", "type": "Compressor, centrifugal", "material": "Carbon steel"},
        {"name": "MTR-1", "param": 1050, "process_type": "Electrical", "category": "Motors & generators", "type": "Totally enclosed motor", "material": "Carbon steel"},
        {"name": "COMP-2", "param": 491, "process_type": "Fluids", "category": "Compressors, fans, & blowers", "type": "Compressor, centrifugal", "material": "Carbon steel"},
        {"name": "MTR-2", "param": 545.56, "process_type": "Electrical", "category": "Motors & generators", "type": "Totally enclosed motor", "material": "Carbon steel"},
        {"name": "HX-1", "param": 31.87, "process_type": "Fluids", "category": "Heat Exchangers", "type": "U-tube shell & tube", "material": "304 stainless steel"},
        {"name": "HX-2", "param": 22.74, "process_type": "Fluids", "category": "Heat Exchangers", "type": "U-tube shell & tube", "material": "304 stainless steel"},
        {"name": "HX-3", "param": 107.19, "process_type": "Fluids", "category": "Heat Exchangers", "type": "U-tube shell & tube", "material": "304 stainless steel"},
        {"name": "COOLER", "param": 191.47, "process_type": "Fluids", "category": "Heat Exchangers", "type": "U-tube shell & tube", "material": "Carbon steel"},
        {"name": "SMR-REACTOR", "param": 160, "process_type": "Fluids", "category": "Reactors", "type": "Tubular fixed bed", "material": "304 stainless steel"},
        {"name": "WGS-HT-REACTOR", "param": 376.54, "process_type": "Fluids", "category": "Reactors", "type": "Tubular fixed bed", "material": "304 stainless steel"},
        {"name": "WGS-LT-REACTOR", "param": 3822.92, "process_type": "Fluids", "category": "Reactors", "type": "Tubular fixed bed", "material": "304 stainless steel"},
        {"name": "FURNACE", "param": 33.26, "process_type": "Fluids", "category": "Boilers, heaters, & furnaces", "type": "Furnace, cylindrical", "material": "304 stainless steel"},
        {"name": "PUMP", "param": 5.16, "process_type": "Fluids", "category": "Pumps", "type": "Single-stage centrifugal", "material": "Carbon steel"},
        {"name": "PSA", "param": 1023.49, "process_type": "Fluids", "category": "Adsorption & membrane separation", "type": "Pressure-swing adsorber", "material": "Carbon steel", "purchased_cost": 284692.37, "cost_year": 1994},
    ],
    "plant": {
        "plant_name": "Steam methane reforming", "process_type": "Fluids", **common_plant,
        "variable_opex_inputs": {
            "electricity":   {"consumption": 38293.44, **price(0.05, 0.03, 0.01, 3.0)},
            "methane_feed":  {"consumption": 219936, **price(0.40, 0.25, 0.0, 5.0)},
            "cooling_water": {"consumption": 485344.08, **price(2.4592e-4, 1e-4, 1e-5, 4e-4)},
            "CO2_tax":       {"consumption": 602991.36, **price(0.075, 0.02, 0.0, 0.15)},
        },
    },
    "analysis": ANALYSIS_BLOCK,
    "output": OUTPUT_BLOCK,
}

we_analysis = json.loads(json.dumps(ANALYSIS_BLOCK))
we_analysis["fixed_capital"]["args"]["additional_capex"] = True
we_analysis["monte_carlo"]["args"]["additional_capex"] = True
we_analysis["tornado"]["args"]["additional_capex"] = True
we_json = {
    "equipment": [
        {"name": "Stack", "param": 0, "process_type": "Fluids", "category": "Electrolysis", "type": "Stack", "material": "Carbon steel", "purchased_cost": 17194000, "cost_year": 2020},
        {"name": "Mechanical BOP", "param": 0, "process_type": "Fluids", "category": "Electrolysis", "type": "Mechanical", "material": "Carbon steel", "purchased_cost": 11019000, "cost_year": 2020},
        {"name": "Electrical BOP", "param": 0, "process_type": "Electrical", "category": "Electrolysis", "type": "Electrical", "material": "Carbon steel", "purchased_cost": 16974000, "cost_year": 2020},
    ],
    "plant": {
        "plant_name": "Water electrolysis", "process_type": "Fluids", **common_plant,
        "operators_hired": 14,                                  # calculate_operators_hired(no_fluid_process=11, no_solid_process=0)
        "additional_capex_cost": [23071452.53, 23071452.53],    # stack quote (17.194 MUSD in 2020) escalated to 2024 USD

        "additional_capex_years": [10, 20],
        "variable_opex_inputs": {
            "electricity": {"consumption": 2352000, **price(0.05, 0.03, 0.01, 3.0)},
            "water":       {"consumption": 378000, **price(0.003, 0.001, 0.0, 0.005)},
        },
    },
    "analysis": we_analysis,
    "output": OUTPUT_BLOCK,
}

for name, data in [("smr_hydrogen.json", smr_json), ("we_hydrogen.json", we_json)]:
    with open(OUT / "assets" / name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("wrote assets/" + name)
