# =====================================================================
#  MODULE 3 - SOLUTION
#  Do above-median-unemployment states have higher mortality?
# =====================================================================

# ---- 0. Load the tools ----------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.formula.api as smf


# ---- 1. Get the data ------------------------------------------------
states = pd.read_csv("data/medicaid_states.csv")

states.shape       # 39 x 7
states.columns
states.head()


# ---- 2. Look at the variable before you test it ---------------------
plt.figure()
plt.hist(states["unemp_rate"])
plt.show()
# Median 6.19, spanning about 2.8 to 8.2.


# ---- 3. Build the grouping variable ---------------------------------
states["unemp_rate"].isna().sum()   # 0, no guard needed
# (The county file has 21 NaNs in unemp_rate. Build state averages from
#  it yourself with .groupby() and .mean(), and pandas SKIPS those rows
#  rather than averaging them -- skipna=True is its default. Worth
#  knowing: silent row loss, no warning.)

states["unemp_rate"].median()

states["high_unemp"] = np.where(states["unemp_rate"] > states["unemp_rate"].median(), 1, 0)

states["high_unemp"].value_counts()
# 20 low, 19 high, same off-by-one as Module 2, same reason.


# ---- 4. Look at the comparison --------------------------------------
states.boxplot(column="crude_rate_20_64", by="high_unemp")
plt.show()

group_means = states.groupby("high_unemp")["crude_rate_20_64"].mean()
group_means

diff_obs = group_means[1] - group_means[0]
diff_obs
# ~ +56. High-unemployment states averaged about 56 more deaths per
# 100,000 working-age people.


# ---- 5. Run the test you already know -------------------------------
result = stats.ttest_ind(states["crude_rate_20_64"][states["high_unemp"] == 1],
                         states["crude_rate_20_64"][states["high_unemp"] == 0],
                         equal_var=False)
result
result.confidence_interval()
# p = 0.029. CI runs about +6 to +106 (high-unemployment group handed
# over first, so the sign matches diff_obs).
#
# In words: high-unemployment states had higher working-age mortality,
# by somewhere between roughly 6 and 106 deaths per 100,000. The lower
# end of that interval is close to zero, so this is suggestive rather
# than settled.


# ---- 6. Build the p-value yourself ----------------------------------
rng = np.random.default_rng(2026)
diffs = []
for i in range(1000):
    shuffled = rng.permutation(states["high_unemp"])
    diffs.append(states["crude_rate_20_64"][shuffled == 1].mean() -
                 states["crude_rate_20_64"][shuffled == 0].mean())
diffs = np.array(diffs)

plt.figure()
plt.hist(diffs)
plt.axvline(diff_obs, color="red", linewidth=2)
plt.show()

(abs(diffs) >= abs(diff_obs)).mean()
# 0.020, against ttest_ind's 0.029. Same conclusion, no formula required.


# ---- 7. The same answer as a regression -----------------------------
m = smf.ols("crude_rate_20_64 ~ high_unemp", data=states).fit()
print(m.summary())
# high_unemp coef = 55.87, matching diff_obs exactly.
# p = 0.027. Note that is the POOLED p; ttest_ind with equal_var=False
# (Welch) gave 0.029. ttest_ind(..., equal_var=True) is the one that
# matches ols().


# ---- 8. Write down what you found -----------------------------------
#
# ANSWER:
# Across 39 states in 2014, those with above-median unemployment had
# working-age mortality about 56 deaths per 100,000 higher than states
# below the median (95% CI roughly 6 to 106; t-test p = 0.029). A
# permutation test that makes no distributional assumption returns a
# similar p-value (0.020), so the result does not hinge on normality. The interval is wide and its lower bound is near zero, so
# this is suggestive, not decisive.
#
# It is not causal. Unemployment was not assigned to states; it travels
# with poverty, industry mix, age structure, and health-system capacity,
# any of which could produce this gap on its own. With n = 39 states we
# also have very little power to separate them.


# =====================================================================
#  EXTENSION ANSWERS
# =====================================================================

# --- 1. median_income instead ---
states["high_income"] = np.where(states["median_income"] > states["median_income"].median(), 1, 0)
stats.ttest_ind(states["crude_rate_20_64"][states["high_income"] == 1],
                states["crude_rate_20_64"][states["high_income"] == 0],
                equal_var=False)
# High-income states average about 117 FEWER deaths per 100,000
# (ttest_ind p = 3.0e-07), much stronger than unemployment, and in the
# expected direction. Note these three groupings (poverty,
# unemployment, income) are largely re-sorting the same states, so they
# are not three independent findings.


# --- 2. what dichotomising cost ---
m_cont = smf.ols("crude_rate_20_64 ~ unemp_rate", data=states).fit()
plt.figure()
plt.scatter(states["unemp_rate"], states["crude_rate_20_64"])
plt.axline((0, m_cont.params["Intercept"]), slope=m_cont.params["unemp_rate"])
plt.show()
print(m_cont.summary())
# plt.scatter() is the scatterplot. plt.axline() draws a straight line
# through the point (0, intercept) with the fitted slope: the regression
# line. m_cont.params holds the two coefs from the summary table.
#
# As a continuous predictor: about 20 more deaths per 100,000 for each
# extra percentage point of unemployment, p = 0.028 -- essentially what
# the median split gave (0.029), off the same 39 states.
#
# Splitting at the median threw away the difference between 4% and 6%
# unemployment, and between 8% and 12%. That is real information, and
# discarding it costs power. Dichotomise for a picture; model the
# continuous variable for an answer.


# --- 3. two variables at once ---
print(smf.ols("crude_rate_20_64 ~ unemp_rate + poverty_rate", data=states).fit().summary())
#
# Read this one carefully. On its own, unemployment looked
# HARMFUL: +20 deaths per point (p = 0.028). Put poverty in the model
# and unemployment's coef flips sign to -9.1 and loses
# significance (p = 0.22), while poverty comes in at +21.8 (p = 9e-08).
#
# The two travel together (correlation 0.59). Alone, unemp_rate was partly
# standing in for poverty. Once poverty is measured directly and held
# fixed, what is left of unemployment points the other way.
#
# Do not over-read the flip, n = 39, and these are states, not people.
# The lesson is the fragility, not the new sign: a coefficient means
# nothing except relative to what else is in the model. Same lesson as
# Module 2's expansion result. A difference in means is where an
# analysis starts, not where it ends.
