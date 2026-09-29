# =====================================================================
#  SETUP CHECK - run this before the workshop
#
#  Open this file in Positron and run the whole thing:
#  Cmd+Shift+Enter (Mac) or Ctrl+Shift+Enter (Windows).
#
#  The last line of the Console should say "You're ready." Anything
#  else, bring your laptop to the room 15 minutes early and we will fix
#  it with you.
# =====================================================================

# "No module named 'pandas'"? Click the Python version in the top-right
# corner and pick the one from this folder's .venv. No .venv folder at
# all? Run `uv sync` in the terminal first.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.formula.api as smf

# "FileNotFoundError"? You opened a file, not the folder. Use
# File -> Open Folder and choose intro-to-python.
counties = pd.read_csv("data/medicaid.csv", index_col=0)
states = pd.read_csv("data/medicaid_states.csv")

print("You're ready.")
