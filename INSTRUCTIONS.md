# INSTRUCTIONS BEFORE THE WORKSHOP

Please complete these steps before November 6. They take about 15 minutes with a normal internet connection.
The goal is to spend the hands-on session learning, not debugging installations.

If you get stuck, contact: `P.B.Tamarona@tudelft.nl`

## What you need

- A laptop with **Windows, macOS, or Linux** and at least 4 GB of RAM. OpenPyTEA is lightweight.
- An internet connection during installation. The workshop itself works offline once everything is installed.
- About 1 GB of free disk space for Python, Jupyter Lab, and the scientific Python stack.

## What these tools are for

- `Python` (3.10 or newer): the programming language OpenPyTEA is written in.
- `pip` and `venv` (or `conda`): create an isolated environment and install packages into it.
- `openpytea`: the techno-economic assessment toolkit used in the session.
- `Jupyter Lab`: runs the workshop notebooks in your browser.
- `Git` (optional): downloads and updates this repository. You can also download it as a ZIP file.

## Option 0: no installation (Google Colab)

If you cannot install software on your laptop, you can run every notebook in Google Colab with a Google account.
Open https://colab.research.google.com/github/pbtamarona/openpytea-workshop/ and pick a notebook, or use the **Open in Colab** badge at the top of each notebook.
The first code cell installs OpenPyTEA in the Colab session. Nothing else is needed.

We still recommend a local installation so that you can keep using OpenPyTEA on your own projects afterwards.

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

Option A (no Git): on the GitHub page, click **Code**, then **Download ZIP**, and unzip it somewhere convenient, for example `Documents/openpytea-workshop`.

Option B (Git):

```bash
cd Documents
git clone https://github.com/pbtamarona/openpytea-workshop.git
cd openpytea-workshop
```

## 3) Create the workshop environment

Run the commands from the repository root (the folder containing this file).

### Route A: venv and pip (recommended)

macOS or Linux:

```bash
python3 -m venv .venv-openpytea
source .venv-openpytea/bin/activate
python -m pip install --upgrade pip
python -m pip install -r envs/requirements.txt
```

Windows PowerShell:

```powershell
py -m venv .venv-openpytea
.\.venv-openpytea\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r envs\requirements.txt
```

If PowerShell refuses to run the activation script, run this once in the same window and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Route B: conda or Miniforge

```bash
conda env create -f envs/environment.yml
conda activate openpytea-ws
```

## 4) Verify the installation

With the environment activated:

```bash
python -c "import openpytea; print('OpenPyTEA', openpytea.__version__)"
openpytea --help
```

The first command prints the installed version (3.0.0 or newer). The second prints the command-line help.

## 5) Launch Jupyter Lab and run the setup notebook

From the repository root, with the environment activated:

```bash
jupyter lab
```

A browser tab opens. Navigate to `notebooks/`, open `00_setup_check.ipynb`, and run all cells (menu **Run**, then **Run All Cells**).
Every check should print `OK`. If one fails, read the message: it tells you which step above to repeat.

Tip: if the notebook cannot import `openpytea`, the kernel is probably not using the environment you created. In Jupyter Lab, use **Kernel**, then **Change Kernel**, and pick the one whose name matches your environment. If it is not listed, run this once with the environment activated and restart Jupyter Lab:

```bash
python -m ipykernel install --user --name openpytea-ws --display-name "Python (openpytea-ws)"
```

## 6) Updating the repository during the workshop

We may correct a notebook during the session. If we ask you to update:

```bash
git pull
```

If Git refuses because you have edited a notebook we changed, copy your edited notebook outside the repository first, then run `git restore <notebook>` and `git pull` again. If you downloaded the ZIP, simply download it again and copy your own edited notebooks over.

## 7) If something fails

Send an email to `P.B.Tamarona@tudelft.nl` with:

- Your operating system (Windows, macOS Intel, macOS Apple Silicon, Linux)
- The route you used (venv/pip, conda, or Colab)
- The output of `python --version`
- The full error message from the terminal or notebook

At the start of the hands-on session (11:55) there are five minutes to confirm the setup check. If it still fails then, you continue in Google Colab and we fix your installation during lunch.
