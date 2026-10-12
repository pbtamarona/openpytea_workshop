# INSTRUCTIONS BEFORE THE WORKSHOP

Please complete these steps before November 6. They take about 15 minutes. The goal is to spend the hands-on session learning, not debugging installations.

If you get stuck, contact: `P.B.Tamarona@tudelft.nl`

## What you need

- A laptop with **Windows, macOS, or Linux** and at least 4 GB of RAM. OpenPyTEA is lightweight.
- An internet connection during installation. The workshop itself works offline once everything is installed.
- About 1 GB of free disk space for Python, Jupyter Lab, and the scientific Python stack.

## What these tools are for

- `Python` (3.10 or newer): the programming language OpenPyTEA is written in.
- `venv` (or `conda`): creates an isolated environment for the workshop.
- `pip`: the Python package installer, used to install OpenPyTEA with `pip install openpytea`.
- `openpytea`: the techno-economic assessment toolkit used in the session.
- `Jupyter Lab`: runs the workshop notebooks in your browser. If you already use a code editor with notebook support, you can run the notebooks there instead (see step 6).
<!-- - `Git` (optional): downloads and updates this repository. You can also download it as a ZIP file. -->

## Option 0: no installation (Google Colab)

If you cannot install software on your laptop, you can run every notebook in Google Colab with a Google account. Open https://colab.research.google.com/github/pbtamarona/openpytea_workshop/ and pick a notebook, or use the **Open in Colab** badge at the top of each notebook. The first code cell installs OpenPyTEA in the Colab session. Nothing else is needed.

**We still recommend a local installation so that you can keep using OpenPyTEA on your own projects afterwards.**

## 1) Install Python

Check whether Python 3.10 or newer is already available. Open a terminal (`Terminal` on macOS or Linux, `PowerShell` on Windows) and run:

```bash
python --version
```

On Windows, if that fails, also try:

```powershell
py --version
```

If you see `Python 3.10.x` or higher, skip to step 2. Otherwise, install Python:

- Recommended route: https://www.python.org/downloads/ (on Windows, tick **Add python.exe to PATH** during installation)
- Alternative route: Miniforge (conda) from https://github.com/conda-forge/miniforge/releases/latest

## 2) Download this repository

Option A (no Git): on the GitHub page, click **Code**, then **Download ZIP**, and unzip it somewhere convenient, for example `Documents/openpytea_workshop`.

Option B (Git): run the following in a terminal (`Terminal` on macOS/Linux, `PowerShell` on Windows):

```bash
cd Documents
git clone https://github.com/pbtamarona/openpytea_workshop.git
cd openpytea_workshop
```

## 3) Create an environment and install OpenPyTEA

Run the commands below in a terminal, PowerShell, or Miniforge Prompt window, from the repository root (the `openpytea_workshop` folder containing `INSTRUCTIONS.md`). Keep this window open: steps 4 and 5 use it too.

### 3a) Create and activate an empty environment

An environment is an isolated Python installation just for this workshop, so nothing you install here interferes with other projects. Pick one route.

**Route A: venv (recommended, comes with Python)**

macOS or Linux (`Terminal`):

```bash
python3 -m venv .venv-openpytea
source .venv-openpytea/bin/activate
```

Windows (`PowerShell`):

```powershell
py -m venv .venv-openpytea
.\.venv-openpytea\Scripts\Activate.ps1
```

If PowerShell refuses to run the activation script, run this once in the same window and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Route B: conda (if you installed Miniforge)**, in `Terminal` or `Miniforge Prompt`:

```bash
conda create -n openpytea-ws python=3.12 pip
conda activate openpytea-ws
```

Once the environment is active, its name appears in brackets at the start of the prompt, for example `(.venv-openpytea)` or `(openpytea-ws)`.

### 3b) Install OpenPyTEA

OpenPyTEA is published on the Python Package Index (PyPI), so one `pip` command downloads it together with everything it depends on (numpy, pandas, scipy, matplotlib, and a few more):

```bash
python -m pip install --upgrade pip
pip install "openpytea[ipython]"
```

**Why `[ipython]`?** The part in square brackets is an *extra*: an optional group of packages that OpenPyTEA only needs in some situations. The `ipython` extra adds IPython and `ipywidgets`, which OpenPyTEA uses to display results nicely in Jupyter notebooks, including the live progress bar shown while a Monte Carlo simulation runs. Because the workshop runs in notebooks, we want this extra. When you later use OpenPyTEA in plain Python scripts, `pip install openpytea` without the extra is enough.

Keep the quotes around `"openpytea[ipython]"`. Without them, some shells (for example zsh, the default on macOS) read the square brackets as a file pattern and stop with `no matches found`.

### 3c) Install Jupyter Lab

The `ipython` extra lets OpenPyTEA work well inside notebooks, but it does not install the notebook application itself. The workshop exercises are Jupyter notebooks, so install Jupyter Lab as well:

```bash
pip install jupyterlab
```

## 4) Verify the installation

With the environment still active, run these commands in the same window as step 3:

```bash
python -c "import openpytea; print('OpenPyTEA', openpytea.__version__)"
openpytea --help
```

The first command prints the installed version (3.1.0 or newer). The second prints the command-line help.

## 5) Launch Jupyter Lab and run the setup notebook

Prefer your own code editor? Skip this step and follow [step 6](#6-alternative-run-the-notebooks-in-your-code-editor) instead.

From the repository root, with the environment activated, in the same terminal, PowerShell, or Miniforge Prompt window:

```bash
jupyter lab
```

A browser tab opens. Navigate to `notebooks/`, open `00_setup_check.ipynb`, and run all cells (menu **Run**, then **Run All Cells**).
Every check should print `OK`. If one fails, read the message: it tells you which step above to repeat.

Tip: if the notebook cannot import `openpytea`, the kernel is probably not using the environment you created. In Jupyter Lab, use **Kernel**, then **Change Kernel**, and pick the one whose name matches your environment. If it is not listed, run this once in a terminal, PowerShell, or Miniforge Prompt window with the environment activated, then restart Jupyter Lab:

```bash
python -m ipykernel install --user --name openpytea-ws --display-name "Python (openpytea-ws)"
```

## 6) Alternative: run the notebooks in your code editor

If you already work in a code editor with notebook support, such as VS Code, Cursor, Windsurf, or PyCharm, you can run the workshop notebooks there instead of in Jupyter Lab. Steps 1 to 4 stay the same: the editor only needs to know which environment to use.

Keep step 3c: installing Jupyter Lab also installs `ipykernel`, the package editors use to run notebook cells. If you are sure you will never use Jupyter Lab, `pip install ipykernel` is enough instead.

1. **Enable notebook support.** In VS Code and editors built on it (Cursor, Windsurf), install the **Python** and **Jupyter** extensions from the Extensions view. PyCharm supports notebooks out of the box from version 2025.1; older Community editions cannot run notebooks.
2. **Open the repository folder** as your project (usually **File**, then **Open Folder** or **Open**), and choose the `openpytea_workshop` folder.
3. **Open** `notebooks/00_setup_check.ipynb`.
4. **Select the workshop environment** as the notebook kernel or project interpreter. Look for **Select Kernel** in the top-right corner of the notebook (VS Code-based editors) or the **Python Interpreter** setting (PyCharm), and pick `.venv-openpytea` (Route A) or `openpytea-ws` (Route B). If it is not listed, point the editor to the Python executable of the environment:
   - Route A: `.venv-openpytea/Scripts/python.exe` (Windows) or `.venv-openpytea/bin/python` (macOS, Linux), inside the repository folder
   - Route B: run `conda env list` to see where `openpytea-ws` is stored, then use `python.exe` directly in that folder (Windows) or `bin/python` inside it (macOS, Linux)
5. **Run all cells** and check that every cell prints `OK`.

Most editors also have a built-in terminal (often **Terminal**, then **New Terminal**) that opens in the project folder. You can use it for steps 3 and 4 instead of a separate window.

Two things to check if something goes wrong:

- **Wrong environment.** If `import openpytea` fails, the notebook is using a different Python. Select the workshop environment again. The first cell of the setup notebook prints which Python it is using; the path should contain `.venv-openpytea` or `openpytea-ws`.
- **Working folder.** Each notebook should run from its own `notebooks/` folder, which is the default in most editors. Exercise 6 reads and writes files relative to that folder. The setup notebook prints the current folder so you can check.

## 7) Updating the repository during the workshop

We may correct a notebook during the session. If we ask you to update, run this in a terminal, PowerShell, or Miniforge Prompt window:

```bash
git pull
```

If Git refuses because you have edited a notebook we changed, copy your edited notebook outside the repository first, then run `git restore <notebook>` and `git pull` again. If you downloaded the ZIP, simply download it again and copy your own edited notebooks over.

## 8) If something fails

If `pip install` fails behind a proxy or firewall (perhaps due to company policy), use Google Colab instead (see [Option 0](#option-0-no-installation-google-colab)).

For anything else, send an email to `P.B.Tamarona@tudelft.nl` with:

- Your operating system (Windows, macOS Intel, macOS Apple Silicon, Linux)
- The route you used (venv/pip, conda, or Colab) and, if you use one, your code editor
- The output of `python --version`
- The full error message from the terminal or notebook

At the start of the hands-on session (11:55) there are five minutes to confirm the setup check. If it still fails then, you continue in Google Colab and we fix your installation during lunch.
