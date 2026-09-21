# =====================================================================
#  MODULE 1 - SOLUTION (the annotated version)
#
#  Question: Did states that expanded Medicaid in 2014 have lower
#            working-age mortality than states that did not?
#
#  This is the completed script with the full commentary. Work from
#  scripts/01-i-do.py during the session and type along; come back here
#  afterwards, or if you fall behind and need to catch up.
#
#  The four passes, each auditing the one before:
#
#    DESCRIBE  what do the two groups look like?        (section 4)
#    TEST      is the gap bigger than chance?           (section 5)
#    CHECK     does the test's assumption change it?    (section 6)
#    MODEL     the same finding, as a coefficient       (section 7)
#
#  Section 0 loads the tools. Sections 1-3 get the data into the right
#  shape.
# =====================================================================


# ---- 0. Load the tools ----------------------------------------------

# Python on its own does not know about tables, plots, or statistics.
# Those live in libraries, and you load the ones you need at the top of
# every script. Nothing prints. That is success.
#
# `as pd` gives pandas a short nickname, so we can type pd.read_csv()
# instead of pandas.read_csv(). Everyone uses these same nicknames, so
# you will recognise them in other people's code.
import pandas as pd                     # tables: read, slice, group
import numpy as np                      # numbers: arrays, shuffling
import matplotlib.pyplot as plt         # pictures
from scipy import stats                 # the t-test
import statsmodels.formula.api as smf   # regression, written y ~ x

# "No module named pandas"? Check the top-right corner of Positron. It
# should name the Python from this project's .venv folder.


# ---- 1. Get the data ------------------------------------------------

# PREDICT before you run the next line: what do you think Python will
# print?

# pd.read_csv() reads a spreadsheet off disk and hands back a DataFrame:
# rows are observations, columns are variables.
counties = pd.read_csv("data/medicaid.csv", index_col=0)

# Nothing printed. That is success, not failure.
#   =             means "store this as". Storing is silent.
#   index_col=0   means "the first column is row labels, not data",
#                 which is why we get 13 columns from a 14-column file.
#
# To see that it worked, look at the Variables pane on the right --
# `counties` is now sitting in it.

# Three questions to ask of any new dataset. Always these three.
counties.shape      # how big is it?  (rows, columns)
counties.columns    # what are the variables called?
counties.head()     # what does a row actually look like?

# The dot means "belonging to": counties.shape is the shape OF counties.
#   With parentheses, .head() DOES something. That is a method: a
#   function that belongs to an object.
#   Without them, .shape just LOOKS something up. That is an attribute.
# Forget the parentheses on .head and you get a description of the
# method instead of the rows. No error, just not what you wanted.

# head() may print wide data as stacked blocks, each ending in a
# backslash. That is ONE table that ran out of room, not several tables.

# The variables we care about:
#   crude_rate_20_64  deaths per 100,000 people aged 20-64   <- our outcome
#   yaca              year the state expanded Medicaid, NaN if it never did
#   year              2009 - 2019
#
# Note: this extract covers 39 states, not 50. Some states (NY, PA, MA,
# VA and others) are simply not in the file. Worth knowing before you
# wonder later where they went.


# ---- 2. Look at the outcome before you test anything ----------------

# Never run a test on a variable you have not looked at.
plt.figure()
plt.hist(counties["crude_rate_20_64"])
plt.show()

# counties["crude_rate_20_64"] pulls one column out of a DataFrame. On
# its own it is a Series -- just a column of numbers, one per county.
# That is all plt.hist() ever wants.
#
# plt.figure() starts a fresh, blank picture. plt.show() says "done,
# show it". Positron keeps a picture open until you start a new one, so
# skip plt.figure() and the next plot you make lands on top of this one.
#
# plt.figure() and plt.hist() also print a note about what they made
# (a Figure, then the bar heights and edges) in the Console. You can
# ignore those.

# We took the default settings. They are fine. Making it pretty is a
# thing you do at the end, if ever.

# WATCH OUT -- the most common mistake you will make all day:
# misspell a column name. Python DOES stop with an error, but it is a
# long one, and the useful part is the LAST line. Try it:
#
#   counties["crude_rate2064"]
#
# A screenful of traceback, ending in   KeyError: 'crude_rate2064'
#
# Skip straight to the bottom. KeyError plus a column name almost
# always means "check your spelling".


# ---- 3. Build the comparison we actually want -----------------------

# Medicaid expansion is a STATE policy. Every county in Alabama has the
# same policy as every other county in Alabama.
#
# So our real sample size is the number of states, not the number of
# counties. This is the most important line of the whole workshop.

# Keep one year so we are comparing like with like.
d2014 = counties[counties["year"] == 2014]

# Square brackets with a True/False test inside keep the rows where the
# test is True. We asked for "rows where year is 2014", and we get every
# column.
#
# Note we write `counties` twice -- once to say which table, once inside
# to say which column to test. Unlike Stata, the dataset is never
# implied. Python needs to be told every time.
d2014.shape

# Now build the grouping variable.
# np.where(test, value_if_true, value_if_false) runs down the whole
# column and returns a new column.
#   .notna()  means "is not missing"
#   &         means "and"
# And note the square brackets doing a NEW job here: on the left of =
# they CREATE a column rather than pulling one out.
d2014["expanded"] = np.where(d2014["yaca"].notna() & (d2014["yaca"] == 2014), 1, 0)

# States that never expanded have yaca = NaN, "not a number", which is
# how pandas marks a missing value. In pandas, NaN == 2014 is False: a
# missing value answers False to EVERY comparison. Here that happens to
# put the never-expanders in the right group, and the .notna() guard
# says so out loud: not missing, and equal to 2014.
#
# Now the trap. The parentheses around (d2014["yaca"] == 2014) are not
# decoration. Python does & before ==, so drop them and it builds
# something else entirely -- and does NOT error. Run this and look:
#
#   np.where(d2014["yaca"].notna() & d2014["yaca"] == 2014, 1, 0).sum()
#
# 0. Every county in the "did not expand" group, and no complaint at
# all. Silent wrong answers are worse than errors.
d2014["expanded"].value_counts()

# One honesty note: yaca is also 2020, 2021 and 2023 for some states.
# Those are coded 0 here, so `expanded` means "expanded in the 2014
# wave", not "ever expanded". Fine for a 2014 snapshot -- but say so.

# PREDICT: after we collapse to states, how many rows will there be?

# .groupby() splits a table into groups, and whatever comes next is done
# to each group separately. Read it left to right, one dot at a time:
# "take d2014, group it by state and expansion status, take
# crude_rate_20_64, and average it."
#
# ["state", "expanded"] is a LIST: square brackets doing yet another
# job, holding two column names as one thing. as_index=False keeps state
# and expanded as ordinary columns, so we get back a plain table.
states_unwt = d2014.groupby(["state", "expanded"],
                            as_index=False)["crude_rate_20_64"].mean()

states_unwt.shape   # 39 rows -- one per state -- down from 2,372 county rows

# STOP. That line looks obvious and it hides a decision.
#
# It averaged the county RATES, giving every county one vote:
d2014["population_20_64"].agg(["min", "max"])
#
# 224 people, and 6.3 million. Loving County, Texas just counted for as
# much as Los Angeles. A county of 224 people should not count the same
# as a county of 6.3 million when you are computing a state's rate.

# A rate is deaths divided by people. To get a STATE's rate, add up the
# deaths and add up the people, then divide once.
d2014["deaths"] = d2014["crude_rate_20_64"] * d2014["population_20_64"] / 1e5

# Same .groupby() template as before, with .sum() this time, and two
# columns at once: double brackets [[ ]] pick a list of columns.
states = d2014.groupby(["state", "expanded"],
                       as_index=False)[["deaths", "population_20_64"]].sum()

# One row per state, deaths and people side by side. Now divide, once.
states["crude_rate_20_64"] = states["deaths"] / states["population_20_64"] * 1e5

# .groupby() hands rows back sorted by the groups, which here means
# alphabetically by state, so these two lines change nothing today.
# Write them anyway. The shuffling in step 6 depends on row order --
# same seed, different order, different answer -- and it has to line up
# with the file Modules 2 and 3 use. Make the order a decision you can
# see, not one you inherited.
states = states.sort_values("state")
states_unwt = states_unwt.sort_values("state")

# Same 39 states, two different answers for each one. How far apart?
gap = states_unwt["crude_rate_20_64"] - states["crude_rate_20_64"]
gap.describe()

# Which states move the most? Square brackets with a True/False test
# again -- same job as step 3, keeping the rows where the test is True.
# .tolist() just prints them compactly.
states["state"][abs(gap) > 75].tolist()

# Texas is off by more than 130 deaths per 100,000. That is bigger than
# any effect we are about to go looking for.
#
# We will use the weighted one, because it is the state's actual rate.
# Hold on to the other one -- we come back to it in step 8.


# ---- 4. DESCRIBE: look at the comparison ----------------------------

# "y broken down by x". Remember that idea. It is the same shape for
# pictures, group means, and models -- all day.
states.boxplot(column="crude_rate_20_64", by="expanded")
plt.show()

# .boxplot() starts its own fresh figure, so no plt.figure() this time.

# LOOK at that before you go on. The two boxes overlap enormously, and
# your eye says "these are the same." That reaction is correct.
#
# A test does not contradict your eye. It answers a narrower question:
# not "can I tell these states apart" (you can't -- look at the spread)
# but "are the two AVERAGES further apart than shuffling would produce".
# Those are different questions, and only the second one has an answer
# here.

# Same template, different goal: group means instead of a picture.
states.groupby("expanded")["crude_rate_20_64"].mean()

# The estimate we care about, as a single number.
# Save it -- we will need it in step 6.
group_means = states.groupby("expanded")["crude_rate_20_64"].mean()

# group_means has 2 rows, and the labels down the left are the groups:
# the row labelled 0 is expanded = 0, the row labelled 1 is
# expanded = 1. Look at it and confirm:
group_means

# A bracket with ONE value picks one row out by its LABEL:
# group_means[1] is the row labelled 1. This is not the [test] rule from
# step 3 -- same brackets, different job.
diff_obs = group_means[1] - group_means[0]
diff_obs

# np.float64(...) is numpy telling you what KIND of number this is. The
# number itself is the part inside the parentheses.

# We wrote [1] - [0], so this is (expanded) minus (not expanded).
# Negative means expansion states were LOWER. Get this order backwards
# on your own data and your headline result flips sign silently.

# Expansion states averaged about 39 fewer deaths per 100,000.
#
# States chose whether to expand, so the honest sentence is "expansion
# states had lower mortality", not "expansion lowered mortality". And
# the alternative to a real effect is not only luck -- it is anything
# else that differs between these two sets of states. Module 2 cashes
# that in.
#
# For now: is 39 more than we would expect from luck alone?


# ---- 5. TEST: the test you already know -----------------------------

# stats.ttest_ind() compares two independent groups. It does not take
# "y broken down by x": you hand it the two groups one at a time, using
# the same [test] brackets as step 3. Expanded states first, then the
# rest. equal_var=False asks for Welch's version of the test, which
# does not assume the two groups are equally spread out.
result = stats.ttest_ind(states["crude_rate_20_64"][states["expanded"] == 1],
                         states["crude_rate_20_64"][states["expanded"] == 0],
                         equal_var=False)
result
result.confidence_interval()

# Which way round? ttest_ind(a, b) subtracts a minus b. We handed it the
# expanded states first, so it did (expanded) minus (not expanded), the
# same order as our diff_obs, and its interval has the same sign:
# about -91 to +12.
#
# Hand them over the other way round and every sign flips, with no
# error and no warning. When a sign looks wrong, find out which way
# round the subtraction went before you assume you broke something.

# Now read the rest, and do not just harvest the p-value:
#   - the confidence interval: the SIZE of the gap the data supports,
#     anywhere from 91 FEWER to 12 MORE deaths per 100,000. That
#     interval crosses zero. The p-value never tells you that.
#   - pvalue = 0.13
#   - scipy does not print the two group means. You already have them,
#     in group_means from step 4.
#
# You can ignore statistic and df today. (Yes, df can have decimals;
# that is Welch's correction, see step 7.)


# ---- 6. CHECK: what that p-value actually means ---------------------

# First, the definition almost everyone walks in with:
#
#     "p is the probability the result is due to chance."
#
# That is the common answer and it is wrong. It has the logic backwards.
# A p-value does not tell you the probability that chance caused your
# result. It ASSUMES chance is all there is, and then asks:
#
#     if expansion made no difference at all, how often would luck
#     alone hand us a gap as big as ours?
#
# We do not have to trust a formula for that. We can just do it.

# The null hypothesis says the labels are meaningless. So let's make
# them meaningless -- shuffle which states "expanded".
#
# rng is a random number generator: the thing that does the shuffling.
rng = np.random.default_rng()
rng.permutation(states["expanded"])

# Run that last line a few times. Different shuffle every time.
#
# Note what stays fixed:
rng.permutation(states["expanded"]).sum()
# Always 22. The 1s add up to the number of expanded states, every time:
# we are dealing out the SAME 22 ones and 17 zeros in a new order, not
# flipping a coin for each state.

# One fake world: shuffle the labels, recompute the difference.
shuffled = rng.permutation(states["expanded"])
(states["crude_rate_20_64"][shuffled == 1].mean() -
 states["crude_rate_20_64"][shuffled == 0].mean())

# The square brackets again, doing the [test] job from step 3:
# states["crude_rate_20_64"][shuffled == 1] means "the mortality rates
# where the shuffled label came out 1".
#
# The outer ( ) let one calculation run over two lines. Without them,
# Python stops at the end of the first line and complains.

# WATCH OUT -- a pandas trap. pandas can shuffle too:
#
#   shuffled = states["expanded"].sample(frac=1)
#
# But pandas shuffles the row labels along with the values, and then
# lines everything back up by label -- so the shuffle quietly undoes
# itself. Every "fake world" comes back exactly -39.18, the real
# answer, with no error. rng.permutation() hands back bare values with
# no labels, which is what a shuffle needs.

# Run those two lines a few times. Sometimes positive, sometimes
# negative, no particular pattern -- that IS sampling variation, and you
# are looking straight at it.
#
# Now the thing to actually notice: keep running it and see how OFTEN
# you land somewhere near -39. Chance produces gaps that size routinely.

# PREDICT: out of 1000 fake worlds, how many will beat our real -39?

rng = np.random.default_rng(2026)   # so everyone in the room gets the same numbers
#
# The seed, 2026, is not optional here. Without it every person in this
# room gets a different p-value, and so do you the next time you run the
# file. Seed it, and write the seed down. Note also that the seed fixes
# the SHUFFLES, not the data -- reorder your rows and the same seed
# gives a different answer, which is why we sorted `states` in step 3.

# A for loop runs the indented lines once for each number in
# range(1000) -- that is, 1000 times -- and .append() keeps each answer
# in the list `diffs`, which starts out empty.
#
# The colon and the indent mark which lines repeat. In Python the indent
# is not decoration, it IS the grouping: line the lines up exactly.
diffs = []
for i in range(1000):
    shuffled = rng.permutation(states["expanded"])
    diffs.append(states["crude_rate_20_64"][shuffled == 1].mean() -
                 states["crude_rate_20_64"][shuffled == 0].mean())
diffs = np.array(diffs)

# np.array() turns the list of 1000 answers into an array, so the
# arithmetic below works on all of them at once.
#
# 1000 differences from 1000 worlds where the policy did nothing.

# And now the same plt.hist() from step 2, pointed at something new.
plt.figure()
plt.hist(diffs)
plt.axvline(diff_obs, color="red", linewidth=2)   # our real result, in red
plt.show()

# How many fake worlds were as extreme as the real one?
# This one line does three things, and all three are worth knowing:
#
#   abs()            throws away the minus sign, so we count BOTH tails
#                    -- shuffles beyond -39 AND beyond +39. That is what
#                    "two-sided" means, and it is what ttest_ind() did too.
#
#   >=               gives a True/False for each of the 1000 shuffles.
#
#   .mean()          of True/False gives the PROPORTION that are True,
#                    because True counts as 1 and False as 0. That is
#                    the counting step. This trick is everywhere.
(abs(diffs) >= abs(diff_obs)).mean()

# Drop the abs() and watch what happens:
(diffs >= diff_obs).mean()
#
# You get 0.92, not something near 0.07. Our difference is NEGATIVE, so
# "shuffles at least as big as ours" counts almost everything. Python
# will not warn you. If you want the one-sided p in the direction of the
# effect it is (diffs <= diff_obs).mean(). Getting this wrong does not
# error -- it just hands you the wrong number, confidently.

# That is a p-value. We built it out of rng.permutation(), .mean(), and
# counting. The t-test said 0.132; the shuffle says 0.131. Same
# conclusion.
#
# They will not match exactly, and should not. ttest_ind() assumes a
# normal distribution; the shuffle does not. And 1000 shuffles is itself
# a sample -- change the seed and the second digit moves. If that spread
# bothers you, run 10,000 instead of 1,000.

# CAREFUL: the shuffle is not assumption-free. It assumes the labels
# could have been dealt out any other way. That holds here, because each
# state made one decision. It does NOT hold if your rows are grouped --
# students inside classrooms, years inside countries -- because a shuffle
# that splits a group apart is not a world that could have happened.

# One more thing about your own data: `shuffled == 1`
# works only because our labels are the numbers 0 and 1. If your grouping
# is "treated"/"control", you need `shuffled == "treated"`. Get it wrong
# and Python returns nan with no error -- a silent failure again, just
# like the missing parentheses in step 3.


# ---- 7. MODEL: the same answer, as a regression ---------------------

# A difference in means is a regression coefficient. And here is
# "y broken down by x" again, written with an actual ~ this time.
#
# smf.ols() sets up an ordinary least squares regression: the outcome
# on the left of the ~, the predictor on the right, all inside quotes.
# .fit() actually fits it. We store the fitted model as `m`.
m = smf.ols("crude_rate_20_64 ~ expanded", data=states).fit()
print(m.summary())

# print() lays the summary table out properly. Without it you get the
# same table wrapped in some clutter.

# This printout is dense. You need exactly two numbers from it today,
# both on the `expanded` row:
#
#   coef        -39.18  <- our difference in means. The same number.
#   P>|t|        0.131  <- our p-value. The same number.
#
# And one bonus, on the row above:
#
#   Intercept            <- the mean of the group coded 0. Check it
#                           against the group means from step 4. Identical.
#                           The "intercept" is just the baseline group.
#
# std err is how much the coef would vary if you drew the sample
# again. Here it is 25.4 against a coef of -39.2, so the data is
# consistent with a wide range of values, including zero. That is
# little. That is what this result amounts to.
#
# R-squared, the F-statistic, and the blocks above and below the table
# answer questions we have not asked yet. They are the next workshop.
#
# So: a difference in means IS a regression coefficient. Once you can
# read this output you can read most quantitative papers.
#
# (ttest_ind(..., equal_var=False) is Welch's version, so the third
#  decimal differs, and that is also why its df was 34.63 rather than
#  37. ttest_ind(..., equal_var=True) matches ols() exactly. Try it.)


# ---- 8. Why we used 39 rows and not 2,372 --------------------------

# Here is the same test, run on the counties instead of the states.
stats.ttest_ind(d2014["crude_rate_20_64"][d2014["expanded"] == 1],
                d2014["crude_rate_20_64"][d2014["expanded"] == 0],
                equal_var=False)

# p is about 6e-17. Overwhelming, and wrong.
#
# It believes it has 2,372 independent observations. It has 39. Every
# county in a state shares one policy decision, so those rows repeat 39
# pieces of information rather than adding 2,372 new ones. Feed a test
# more rows than you have information and the standard error shrinks
# until any difference looks certain.
#
# You already saw the other version of this in step 3: averaging county
# rates instead of weighting by population gives -64 and p = 0.028,
# where weighting correctly gives -39 and p = 0.13. Neither was an
# arithmetic error. Which rows count as an observation, and how much
# each one counts, are decisions you make before any test runs.
#
# When a p-value looks too good, ask how many independent things you
# actually measured. It is usually fewer than the number of rows.

# =====================================================================
#  Every function and method used in this entire analysis:
#
#    pd.read_csv  .head  .describe                  <- get data, look at it
#      (plus two attributes: .shape  .columns)
#    plt.figure  plt.hist  .boxplot  plt.axvline  plt.show   <- pictures
#    np.where  .notna  .isna  .value_counts         <- build a grouping variable
#    .groupby  .mean  .sum  .median  .agg  abs      <- summarise
#    .sort_values  .tolist                          <- sort and list
#    stats.ttest_ind  .confidence_interval          <- test
#    smf.ols  .fit  .summary  print                 <- model
#    np.random.default_rng  .permutation            <- the permutation test
#    range  .append  np.array                       <- ... done 1000 times
#
#  Thirty-one, and most of them you used more than once.
#  That is a whole paper's worth of analysis. You do not need more
#  to start -- and the next two modules add almost nothing new.
# =====================================================================
