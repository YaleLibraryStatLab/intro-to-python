# =====================================================================
#  MODULE 1  -  I DO
#
#  Question: Did states that expanded Medicaid in 2014 have lower
#            working-age mortality than states that did not?
#
#  Type along with me. I will say every line before I type it, and the
#  slide will show it. Run each line as you write it: Cmd+Enter (Mac)
#  or Ctrl+Enter (Windows). Watch the Console and the Plots pane.
#
#  Fallen behind? Don't scramble. Put up a red sticky, keep listening,
#  and copy the line you missed from scripts/solutions/01-i-do-solution.py
#  when we pause. That file also has the full commentary to take home.
#
#  The four passes, each auditing the one before:
#
#    DESCRIBE  what do the two groups look like?        (section 5)
#    TEST      is the gap bigger than chance?           (section 6)
#    CHECK     does the test's assumption change it?    (section 7)
#    MODEL     the same finding, as a coefficient       (section 8)
#
#  Section 1 loads the tools. Sections 2-4 get the data into the right
#  shape.
# =====================================================================


# ---- 1. Load the tools ----------------------------------------------

# Load the five libraries we use today, each under its usual nickname:
# pandas as pd, numpy as np, matplotlib.pyplot as plt, stats from
# scipy, and statsmodels.formula.api as smf.

world = "Hello world!"
print(world)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.formula.api as smf

counties = pd.read_csv("data/medicaid.csv", index_col=0)

# ---- 2. Get the data ------------------------------------------------

# Read data/medicaid.csv and store it as `counties`.
# Column 1 is row labels, not data.



# Three questions for every new dataset: how big, what columns,
# what does a row look like.






# ---- 3. Look at the outcome before you test anything ----------------

# A histogram of crude_rate_20_64. Defaults are fine.
# Start a fresh figure first, and show it at the end.






# ---- 4. Get the data ready for the question -------------------------

# Three jobs before we compare anything:
#   1. Aggregate. Expansion is a STATE policy, so one rate per state.
#   2. Deal with the NAs. How is the policy recorded right now? Look at
#      the first few values of yaca.
#   3. Weight by population. A state's rate is its deaths over its people.

d2014 = counties[counties["year"] == 2014]
d2014.shape

dn2014 = counties[counties["year"] != 2014]

# 4a. Keep one year: the rows of `counties` where year is 2014.
#     Call it `d2014`. Then check its size.






# 4b. Label each state. Make a column `expanded`: 1 if the state
#     expanded in 2014, 0 otherwise. Guard against the NaNs in `yaca`.
#     Then count how many landed in each group.






# 4c. Weight by population. Turn each county's rate back into a count
#     of deaths: a new column called `deaths`. Then add up the deaths
#     and the people by state, and divide once. Call the result
#     `states`. Sort it by state so the shuffling later lines up, and
#     check its size.










# ---- 5. DESCRIBE: look at the comparison ----------------------------

# A boxplot of crude_rate_20_64 broken down by expanded.
# Then the two group means.






# Save the difference between the two means as `diff_obs`.
# The row labelled 1 is the expanded group, 0 is not.






# ---- 6. TEST: the test you already know -----------------------------

# A t-test of crude_rate_20_64: the expanded states against the rest.
# Then its confidence interval.
# Read the whole output, not just the p-value.






# ---- 7. CHECK: what that p-value actually means ---------------------

# Make a random number generator, then shuffle the expansion labels
# once. Run the shuffle a few times.



# Check what stays fixed when you shuffle.



# One fake world: shuffle, then recompute the difference.






# Now a thousand fake worlds. Seed the generator first so we all get
# the same numbers, then collect the differences in `diffs`.










# The null distribution, with our real result marked on it.






# What fraction of fake worlds were as extreme as ours?
# Then try it without abs() and see what changes.






# ---- 8. MODEL: the same answer, as a regression ---------------------

# Fit crude_rate_20_64 on expanded. Store it as `m`, then read it.
# You need two numbers: the coef and P>|t| on the expanded row.






# ---- 9. Why we used 39 rows and not 2,372 --------------------------

# The same test, run on the counties instead of the states.
# Watch what happens to the p-value, and ask why it is wrong.






# =====================================================================
#  Functions and methods you used today:
#
#    pd.read_csv  .head                             <- get data, look at it
#      (plus two attributes: .shape  .columns)
#    plt.figure  plt.hist  .boxplot  plt.axvline  plt.show   <- pictures
#    np.where  .notna  .isna  .value_counts         <- build a grouping variable
#    .groupby  .mean  .sum  .median  abs            <- summarise
#    .sort_values                                   <- sort
#    stats.ttest_ind  .confidence_interval          <- test
#    smf.ols  .fit  .summary  print                 <- model
#    np.random.default_rng  .permutation            <- the permutation test
#    range  .append  np.array                       <- ... done 1000 times
#
#  Twenty-eight. That is a whole paper's worth of analysis.
# =====================================================================
