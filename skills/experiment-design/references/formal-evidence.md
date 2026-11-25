# Formal evidence

Use this reference for a confirmatory experiment, an acceptance decision, or a formal review.

## Define the claim

State the decision and the population or operating conditions that it applies to. Define the factor, its levels, and the control condition. A factor is an input that can affect the outcome. A level is one value of that factor.

Define each outcome so that another person can measure it. Specify the primary outcome, units, summary statistic, and comparison. Define the smallest effect that would change the decision. Specify limits for secondary outcomes when they affect acceptance.

Check two types of validity. Internal validity concerns whether the intervention caused the observed effect. External validity concerns whether the result applies to other units or conditions. Random assignment helps control differences between conditions. A suitable sample and suitable test conditions help show where the result applies.

## Select the design

| Condition | Design |
| --- | --- |
| Independent units can receive either condition | Assign the units at random. Give each condition the same measurement procedure. |
| Two similar units form a pair | Form pairs before assignment. Within each pair, randomly assign one unit to each condition. |
| The same unit can receive both conditions | Balance the order of the conditions. Assign the orders at random when possible. Use a reset or washout for effects that continue after a condition ends. |
| Batch, site, device, or day can affect the outcome | Group similar units into blocks. Randomize the conditions within each block. Include the relevant comparisons in each block when possible. |
| The effect of one factor can change with the level of another factor | Use a full factorial design when the budget permits it. Test each combination of levels. Include the interaction in the analysis. |
| The budget permits only some combinations | Use a fractional factorial design for screening. List the effects that the design cannot distinguish. Plan follow-up runs for effects that matter to the decision. |
| Some factors are difficult to change between runs | Use a split-plot design when appropriate. Randomize at each level where possible. Estimate uncertainty at the assignment level for each factor. |
| Random assignment is unavailable | Record how units receive conditions. Identify other causes that can explain the result. Limit the claim to an association if the evidence cannot establish causation. |

An order effect occurs when the position of a condition affects the result. For example, practice can improve the second result. Fatigue can make the second result worse. Use separate units if the effects of one condition cannot end before the next condition starts.

Check whether one unit can affect another unit. Check for condition combinations that the procedure cannot run. If knowledge of the condition can affect measurement, conceal the condition from the person who measures or evaluates the result. Keep a record of the actual assignments. [NIST/SEMATECH, *Choosing an experimental design*](https://itl.nist.gov/div898/handbook/pri/section3/pri3.htm).

## Check the procedure and set the sample size

Use a pilot to check that the intervention and control produce the intended conditions. Check that the measurement represents the outcome of interest. Repeat the measurement under the same conditions to check its consistency. Use the pilot to estimate variation, run time, and failure frequency. Set a limit for the pilot before it starts.

Count independent units at each level of assignment. For example, count independent pairs in a paired design. Choose the sample size for the required precision or power. Power is the probability that a test rejects the null hypothesis at a specified effect when the model assumptions hold.

Specify the assumed true effect, variation, error rate, and design assumptions for the calculation. If success requires a confidence bound above a threshold, calculate power at a plausible true effect above that threshold. If the budget fixes the sample size, estimate the precision or power under several plausible assumptions. Report limits on the decisions that the design can support. [Lakens, *Sample Size Justification*](https://doi.org/10.1525/collabra.33267).

## Select the analysis

Start with the quantity that the decision requires, such as a mean difference, a percentile, or a failure rate. Identify the outcome type. Check whether the observations are independent, paired, in blocks, or in groups that share common conditions. Check the assumptions of the procedure. Use these checks to select an estimator and a method for its uncertainty.

| Question | Method and checks |
| --- | --- |
| What is the difference between two means from independent groups? | Consider a Welch t interval or test. It permits different group variances. Check independence and whether the sample size and distribution support the t approximation. |
| What is the mean difference within pairs? | Calculate a difference for each pair. Consider a paired t interval or test. Check independence between pairs and the distribution of the differences. |
| Do several factors affect a numerical outcome? | Consider a regression or analysis of variance that includes the planned factors and interactions. Check the error structure, independence, and variance assumptions of the model. |
| Do two independent groups have different proportions? | Estimate the difference or ratio of proportions. Use a suitable interval. For a small two-by-two table with independent observations, consider Fisher's exact test for association. |
| Do paired units have different proportions? | Consider McNemar's test for binary outcomes from independent pairs. Count pairs with success only under A. Separately count pairs with success only under B. Use an interval that accounts for pairing. [NIST, *McNemar Test*](https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/mcnemar.htm). |
| Does the design have dependent observations or few independent units? | Use a method that accounts for the design. If you resample, keep each independent pair or group together. Report limited precision when the independent count is small. |

Rank tests have assumptions. A rank test can detect differences in distributions. Interpret it as a test of a location difference only if its assumptions support that interpretation. Use a randomization test only when its reassignment procedure matches the design and the null hypothesis. Check whether plausible alternatives to the analysis change the decision.

Specify the planned comparisons and control for multiple comparisons when the decision needs this control. Include comparisons that depend on the selection of a candidate. Report an effect estimate and an interval in useful units. Use an identified test and its assumptions if you also report a p-value.

A Type I error occurs when a test rejects a true null hypothesis. A Type II error occurs when a test fails to reject a false null hypothesis. Failure to reject the null hypothesis can leave the evidence inconclusive.

## Record the protocol

1. Record the decision, scope, conditions, primary outcome, effect threshold, and acceptance limits.
2. Record the experimental units, observation units, and units for the analysis.
3. Record the assignment schedule or the procedure that generates it. Keep the random seed when applicable.
4. Record the measurement procedure and run counts. Include the sample size justification.
5. Specify how to handle missing data, outliers, timeouts, and retries. Apply the same rules to all conditions. Count failures that the condition causes when failure is an outcome.
6. Specify the analysis and its assumptions. Set the stopping rule before you examine outcomes. For interim decisions, specify when to examine the data. Use a sequential method with the necessary error control.
7. Record the protocol and analysis versions before you examine confirmatory outcomes. Record subsequent changes with dates and reasons. [Nosek et al., *The preregistration revolution*](https://doi.org/10.1073/pnas.1708274114).

## Set the decision rule

- **Improvement.** Require the applicable confidence bound to pass the threshold in the direction of improvement.
- **Noninferiority.** Specify the maximum acceptable loss. Use a one-sided confidence bound to check the loss against this limit.
- **Equivalence.** Specify the lower and upper equivalence limits. Use an equivalence test or its corresponding confidence interval. For two one-sided tests at a 5% significance level, use the corresponding equal-tailed 90% confidence interval. Require the full interval to lie inside both limits. [Lakens, *Equivalence Tests*](https://doi.org/10.1177/1948550617697177).
- **Inconclusive evidence.** Specify the action to take if the evidence does not meet a decision criterion.

## Review the evidence

1. State the claim, conditions, and protocol version.
2. Compare the planned and actual assignments and counts. Give counts for each condition. Record missing data, exclusions, failed runs, and protocol changes.
3. Give the outcome summaries, estimated effects, and uncertainty. Show variation across independent units. Report the secondary outcomes that affect acceptance.
4. Identify planned and exploratory analyses. Explain how material protocol changes or analysis assumptions affect the conclusion.
5. State which acceptance criteria the evidence meets. State the limits of the result and which additional evidence could change the decision.
6. Give the data, run schedule, configurations, tool versions, and analysis commands or scripts necessary to reproduce the result.

## Book sources

- Peter Harris, *Designing and Reporting Experiments in Psychology*, 3rd edition, 2008. Chapters 3 to 5 and 9 to 13 give the basis for the design, pilot, and report guidance.
- Gopal K. Kanji, *100 Statistical Tests*, 3rd edition, 2006. The classification and test entries give the basis for the guidance on test objectives and assumptions.
