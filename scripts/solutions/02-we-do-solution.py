# =====================================================================
#  MODULE 2 - SOLUTION
#  Do high-poverty states have higher working-age mortality?
# =====================================================================

# ---- 0. Load the tools ----------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.formula.api as smf


# ---- 1. Get the data ------------------------------------------------
states = pd.read_csv("data/medicaid_states.csv")

states.shape       # 39 rows, 7 columns
states.columns
states.head()


# ---- 2. Look at it first --------------------------------------------
plt.figure()
plt.hist(states["poverty_rate"])
plt.show()
# Median 15.4, range about 9 to 22, mild right skew.


# ---- 3. Build the grouping variable ---------------------------------
states["poverty_rate"].median()

states["high_poverty"] = np.where(states["poverty_rate"] > states["poverty_rate"].median(), 1, 0)

states["high_poverty"].value_counts()
# 20 low, 19 high. Not exactly even: the median is itself a state's
# value, and > is strict, so that state falls in the "low" group.

# Why no .notna() guard? Because poverty_rate has no missing values:
states["poverty_rate"].isna().sum()   # 0
# In Module 1, yaca was NaN for every non-expanding state. pandas
# answers False to any comparison with NaN, so a missing value quietly
# lands in whichever group "False" means. The guard made that choice
# out loud instead of by accident.


# ---- 4. Look at the comparison --------------------------------------
states.boxplot(column="crude_rate_20_64", by="high_poverty")
plt.show()

states.groupby("high_poverty")["crude_rate_20_64"].mean()

group_means = states.groupby("high_poverty")["crude_rate_20_64"].mean()
diff_obs = group_means[1] - group_means[0]
diff_obs
# ~ +110. High-poverty states averaged about 110 MORE deaths per
# 100,000 working-age people.


# ---- 5. The test ----------------------------------------------------
# The error in the student script was a missing comma between the two
# groups. Python's message says so: "Perhaps you forgot a comma?"
result = stats.ttest_ind(states["crude_rate_20_64"][states["high_poverty"] == 1],
                         states["crude_rate_20_64"][states["high_poverty"] == 0],
                         equal_var=False)
result
result.confidence_interval()
# p = 7.0e-06. The confidence interval runs from about +70 to +149.
#
# It is positive because we handed ttest_ind() the high-poverty group
# first, the same order as our diff_obs. The data is compatible with a
# gap of roughly 70 to 150 deaths per 100,000. That SIZE is what the
# p-value alone never tells you.


# ---- 6. Build the p-value yourself ----------------------------------
rng = np.random.default_rng()
shuffled = rng.permutation(states["high_poverty"])
(states["crude_rate_20_64"][shuffled == 1].mean() -
 states["crude_rate_20_64"][shuffled == 0].mean())

rng = np.random.default_rng(2026)
diffs = []
for i in range(1000):
    shuffled = rng.permutation(states["high_poverty"])
    diffs.append(states["crude_rate_20_64"][shuffled == 1].mean() -
                 states["crude_rate_20_64"][shuffled == 0].mean())
diffs = np.array(diffs)

plt.figure()
plt.hist(diffs)
plt.axvline(diff_obs, color="red", linewidth=2)
plt.show()

(abs(diffs) >= abs(diff_obs)).mean()
# 0 out of 1000. Report as p < 0.001, not p = 0.
# The red line sits well outside the whole null distribution -- which is
# exactly what an overwhelming result looks like.


# ---- 7. The same answer as a regression -----------------------------
m = smf.ols("crude_rate_20_64 ~ high_poverty", data=states).fit()
print(m.summary())
# The high_poverty coef equals diff_obs from step 4 exactly.


# ---- 8. Discussion answers ------------------------------------------
#
# a) Poverty has the larger effect (~110 vs ~-39) AND the smaller
#    p-value here -- but those are different questions. Effect size is
#    "how big"; the p-value is "how sure we are it isn't zero." A tiny
#    effect measured precisely can have a smaller p than a large effect
#    measured noisily. Always report both.
#
# b) Neither variable was randomly assigned, so neither result is
#    causal. States chose to expand; poverty is a feature of a state,
#    not a treatment. These are associations. Everything today is an
#    association.
#
# c) Poorer states were less likely to expand Medicaid. Poverty also
#    raises mortality. So some of the -39 we attributed to expansion is
#    really poverty doing the work in the other direction -- a
#    confounder. That is the motivation for putting both variables in
#    one model, which is where a regression workshop picks up:
#
#      print(smf.ols("crude_rate_20_64 ~ expanded + poverty_rate",
#                    data=states).fit().summary())
#
#    Run it. The expanded coef falls from -39.2 to -12.1 and its
#    p-value goes from 0.13 to 0.49. Most of the little that was left of
#    an expansion gap was poverty. This is not a flaw in the method --
#    it is the method working, and it is the reason nobody stops at a
#    difference in means.
