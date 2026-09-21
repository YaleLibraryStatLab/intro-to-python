# =====================================================================
#  MODULE 2  -  WE DO
#  Same pipeline, new question. Work in pairs.
#
#  Question: Do high-poverty states have higher working-age mortality
#            than low-poverty states?
#
#  Every line you need is a line you already ran in Module 1. Where you
#  see ______ , fill it in. Where you see a full line, just run it.
#
#  Rule for pairs: one person types, one person reads the code out loud
#  and says what it should do BEFORE you run it. Swap at step 4.
#
#  Stuck for more than two minutes? Flag us down. That is what we are
#  here for -- do not burn the module on one blank.
# =====================================================================


# ---- 0. Load the tools ----------------------------------------------

# Same five as Module 1. Just run them.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.formula.api as smf


# ---- 1. Get the data ------------------------------------------------

# This is the state-level file. We built it in Module 1; here it is
# ready-made, with a few extra columns.
states = pd.read_csv("data/medicaid_states.csv")

# Your three questions for any new dataset. Fill them in:
states.______       # how big is it?
states.______       # what are the variables called?
states.______()     # what does a row look like?

# Variables available to you:
#   crude_rate_20_64   deaths per 100,000 aged 20-64      <- the outcome
#   poverty_rate       percent of the state in poverty
#   unemp_rate         unemployment rate
#   median_income      median household income, $thousands
#   population_20_64   people aged 20-64
#   expanded           1 = expanded Medicaid in 2014, 0 = did not


# ---- 2. Look at it first --------------------------------------------

# Same rule as Module 1: never test a variable you have not looked at.
# Make a histogram of poverty_rate.
plt.figure()
plt.hist(states["______"])
plt.show()

# PREDICT before you run it: roughly where will the middle be?


# ---- 3. Build the grouping variable ---------------------------------

# In Module 1 the groups came ready-made (a state expanded, or it did
# not). Poverty is a number, not a group -- so we have to make groups.
#
# We will split at the median: above it is "high poverty", below is not.

states["poverty_rate"].median()

# YOUR TURN -- this is the one genuinely new thing in Module 2.
# np.where(test, value_if_true, value_if_false). Same function as
# Module 1, but the test is new: "is this state's poverty_rate above
# the median?"
states["high_poverty"] = np.where(______________________________, 1, 0)

# Check it worked. How many states landed in each group?
states["high_poverty"].value_counts()

# NOTE: we did not need the .notna() guard this time. Why not?
# (Look back at Module 1, step 3. Hint: check
#  states["poverty_rate"].isna().sum().)


# ---- 4. Look at the comparison --------------------------------------
#  >>> SWAP TYPIST HERE <<<

# The "y broken down by x" template. Outcome in column=, groups in by=.
states.boxplot(column="crude_rate_20_64", by="______")
plt.show()

# Group means, same template:
states.groupby("______")["crude_rate_20_64"].______()

# Now pull out the single number: the difference between the two means.
# The row labelled 1 is the high-poverty group, 0 is the low. Subtract
# them.
group_means = states.groupby("high_poverty")["crude_rate_20_64"].mean()
diff_obs = ______________________________________________
diff_obs

# Say out loud what this number means, in units, before moving on.
# "High-poverty states averaged ___ more deaths per 100,000."


# ---- 5. The test ----------------------------------------------------

# Same test again. This will throw an error, see if you can figure it out.
result = stats.ttest_ind(states["crude_rate_20_64"][states["high_poverty"] == 1]
                         states["crude_rate_20_64"][states["high_poverty"] == 0],
                         equal_var=False)
result
result.confidence_interval()

# Read the whole output, not just p. What is the confidence interval,
# and what does it tell you that the p-value does not?


# ---- 6. Build the p-value yourself ----------------------------------

# Shuffle the labels, recompute the difference, one fake world:
rng = np.random.default_rng()
shuffled = rng.permutation(states["high_poverty"])
(states["crude_rate_20_64"][shuffled == 1].mean() -
 states["crude_rate_20_64"][shuffled == 0].mean())

# Run the last two a few times. Watch it bounce around zero.

# Now 1000 fake worlds. Fill in the blank -- it is the same two-line
# subtraction you just ran.
# You wrote the observed difference by hand in step 4. This is the same
# subtraction, on the shuffled labels instead of the real ones.
rng = np.random.default_rng(2026)
diffs = []
for i in range(1000):
    shuffled = rng.permutation(states["high_poverty"])
    diffs.append(______________________________________________)
diffs = np.array(diffs)

# Look at the null distribution with your real result marked on it.
#
# NEW BIT: last time our result sat inside the histogram. This time it
# may not. plt.axvline() widens the x-axis to fit the red line, so if
# the line sits far out on its own with empty space in between, that
# gap IS the result, not a drawing glitch.
plt.figure()
plt.hist(diffs)
plt.axvline(diff_obs, color="red", linewidth=2)
plt.show()

# What fraction of fake worlds were as extreme as the real one?
# Three pieces: abs() to count both tails, >= to get True/False for each
# shuffle, .mean() to turn True/False into a proportion.
(______________________________).mean()

# If you got 0, that does NOT mean the probability is zero. It means
# none of our 1000 shuffles got that far -- so p is smaller than about
# 1/1000. Report it as p < 0.001, never as p = 0.


# ---- 7. The same answer as a regression -----------------------------

m = smf.______("crude_rate_20_64 ~ high_poverty", data=states).fit()
print(m.summary())

# Check: does the coef on the high_poverty row match your diff_obs
# from step 4? It should, to the decimal.


# ---- 8. Compare your two analyses -----------------------------------

# Module 1 could not distinguish expansion from chance: -39, p = 0.13.
# You just found high poverty associated with about +110, p < 0.001.
#
# Discuss with your partner, then we will take answers:
#
#   a) Which effect is larger? Which is more certain? Are those the
#      same question?
#
#   b) Poverty was not assigned to states by anyone. Neither, really,
#      was expansion. What does that stop you from saying about either
#      result?
#
#   c) Poor states were also less likely to expand Medicaid. What does
#      that do to the Module 1 estimate?
