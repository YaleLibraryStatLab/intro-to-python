# Intro to Python

Learn Python by using it to answer a real statistical question.

A two-hour StatLab workshop. By the end you will have read real data,
compared two groups, tested the difference, built a p-value by hand, and
fit a regression — using twenty-eight functions and methods.

## Before the workshop

1. Install **Positron** from [positron.posit.co](https://positron.posit.co)
2. Download this repository: green **Code** button above → **Download ZIP**,
   then unzip it. (Or `git clone` it if you use git.)
3. In Positron, **File → Open Folder** and choose the `intro-to-python`
   folder. Open a terminal in Positron with **Terminal → New Terminal**.
4. Install **uv**, the tool that sets up Python for you. Paste the line for
   your computer into the terminal and press Enter:

   Mac:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Windows:

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

5. Close that terminal and open a new one (so it can find uv), then run:

   ```bash
   uv sync
   ```

   uv downloads Python itself if you don't have it, and builds a `.venv`
   folder holding pandas, numpy, scipy, statsmodels, and matplotlib, in
   exactly the versions the workshop was tested with. It is the same on
   Mac and Windows. Nothing else to install.

6. **Check it worked.** Click the Python version in the top-right corner
   and choose the one from this folder's `.venv`. Then open
   `scripts/00-check.py` and run the whole file with **Cmd+Shift+Enter**
   (Mac) or **Ctrl+Shift+Enter** (Windows). The Console should end with
   `You're ready.`

   Anything else? Come to the room 15 minutes early and we will fix it
   with you. Please don't leave this for the start of the workshop: there
   is no time set aside for installing during the session.

## Getting started

Open **Positron**, then **File → Open Folder** and choose the
`intro-to-python` folder you just unzipped.

Open the **folder**, not a file. Positron treats whatever folder you open as
your working directory, which is why none of the scripts contain a file
path you have to change. `pd.read_csv("data/medicaid.csv")` just works.

Check the top-right corner says **Python**, and that it is the one from this
folder's `.venv`. If not, click it and choose that one. Then open
`scripts/01-i-do.py` and run a line with **Cmd+Enter** (Mac) or
**Ctrl+Enter** (Windows).

## What's in here

### `scripts/`

| File | |
|---|---|
| `00-check.py` | Run before the workshop. Ends with `You're ready.` if everything is installed. |
| `01-i-do.py` | **Start here.** Mostly empty: section headings and a note about what to write next. You type along with the instructor. |
| `02-we-do.py` | Work in pairs. Most of the code is written. Twelve blanks are yours, and four of them are whole expressions. |
| `03-they-do.py` | On your own. Nine steps, no code. |

### `scripts/solutions/`

| File | |
|---|---|
| `01-i-do-solution.py` | Module 1 finished, with full commentary explaining every line. Use it to catch up if you fall behind, and take it home as a reference. |
| `02-we-do-solution.py` | Module 2 answers, including the discussion questions. |
| `03-they-do-solution.py` | Module 3 answers, plus the extension exercises. |

The solutions are here on purpose. Try each module first — you will learn
more from a wrong answer you wrote than a right one you read.

### `data/`

| File | |
|---|---|
| `medicaid.csv` | 26,066 rows: US counties, 2009–2019, with mortality, poverty, unemployment and income. Used in Module 1. |
| `medicaid_states.csv` | The same data collapsed to 39 states. Used in Modules 2 and 3. |

### `presentation/`

`01-python-presentation.html` is the slide deck. Open it in a browser to
review anything from the session. Everything else in that folder is what
builds the deck, and you can ignore it.

### `pyproject.toml` and `uv.lock`

These tell `uv sync` exactly what to install. You can ignore them.

## Getting unstuck during the workshop

- **Red sticky note** means you are stuck. Put it up early; that is what
  the instructors are for.
- `help(pd.Series.mean)` opens Python's own help for any function.
- `No module named 'pandas'`? Check the top-right corner: Positron should be
  using the Python from this folder's `.venv`. No `.venv` folder at all?
  Run `uv sync` in the terminal.
- Your script from today is the best reference you will own. It works, you
  typed it, and you know what every line does.

StatLab office hours are free and are the fastest way to get unstuck:
[library.yale.edu/statlab](https://library.yale.edu/statlab)
