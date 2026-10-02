# =====================================================================
#  MODULE 3  -  YOU DO
#  Your turn. Same pipeline, your own question.
#
#  Question: Do states with above-median unemployment have higher
#            working-age mortality than states below it?
#
#  This time there is no code. Only the nine steps, in order, and a
#  reminder of what each one is for.
#
#  You have done all nine before, twice. Module 1 and Module 2 are
#  open in your other tabs -- USE THEM. Copying your own working code
#  and changing the variable name is not cheating, it is the job.
#
#  Green sticky = I'm through.  Red sticky = I'm stuck.
# =====================================================================


# ---- 0. Start clean -------------------------------------------------
# Run this line first: Cmd+Enter / Ctrl+Enter. It empties the
# Variables pane, so everything you use below is something you
# made in this script, not a leftover from Module 2.
get_ipython().run_line_magic("reset", "-f")


# ---- 1. Load the tools ----------------------------------------------
# The same five import lines as Modules 1 and 2.








# ---- 2. Get the data ------------------------------------------------
# Read data/medicaid_states.csv into an object called `states`.
# Then ask your three questions: how big, what columns, what's a row.






# ---- 3. Look at the variable before you test it ---------------------
# Histogram of unemp_rate.
# Where is the middle? Is it symmetric? Any state way out on its own?






# ---- 4. Build the grouping variable ---------------------------------
# Make a column called high_unemp: 1 if the state's unemp_rate is above
# the median, 0 otherwise.
#
# Then check it with .value_counts(). How many states in each group?
#
# CAREFUL: does unemp_rate have missing values? Check before you split.
# (.isna().sum(), and look at what Module 1 step 4 had to do about it.)






# ---- 5. Look at the comparison --------------------------------------
# A boxplot of crude_rate_20_64 by your new group.
# Then the two group means, and the difference between them.
# Save that difference as diff_obs, step 7 needs it.
#
# Say the number out loud in units before you go on.






# ---- 6. Run the test you already know -------------------------------
# stats.ttest_ind, with the high-unemployment group first.
# Read the whole output, and its confidence interval. Write the p-value
# and the confidence interval in a comment, in your own words.






# ---- 7. Build the p-value yourself ----------------------------------
# The permutation test, in four moves:
#   a) shuffle the group labels once, recompute the difference
#   b) do that 1000 times with a for loop, np.random.default_rng(2026)
#      first
#   c) histogram the 1000 differences, with plt.axvline() marking
#      diff_obs
#   d) what fraction of shuffles were as extreme as the real result?
#
# Does it agree with step 6?






# ---- 8. The same answer as a regression -----------------------------
# smf.ols(), same template. Does the coef match your diff_obs?






# ---- 9. Write down what you found -----------------------------------
# Three or four sentences, as a comment, that you would be willing to
# put in a draft. Include:
#   - the direction and size of the difference, in units
#   - how sure you are, and how you know
#   - one reason a referee would not let you call this causal
#
# ANSWER:
#
#
#
#


# =====================================================================
#  DONE EARLY? Pick one:
#
#  1. Swap the grouping variable to median_income. Does the story
#     change? Should it?
#
#  2. Your step 4 split at the median, which threw away everything
#     except "above" or "below". Try the relationship without the
#     split:
#         m_cont = smf.ols("crude_rate_20_64 ~ unemp_rate", data=states).fit()
#         plt.figure()
#         plt.scatter(states["unemp_rate"], states["crude_rate_20_64"])
#         plt.axline((0, m_cont.params["Intercept"]),
#                    slope=m_cont.params["unemp_rate"])
#         plt.show()
#         print(m_cont.summary())
#     What did dichotomising cost you?
#
#  3. Put two variables in one model and see what happens to each:
#         print(smf.ols("crude_rate_20_64 ~ unemp_rate + poverty_rate",
#                       data=states).fit().summary())
#
#  4. Take today's script and point it at your own data.
#     That is the actual goal. We are here for another 20 minutes.
# =====================================================================
