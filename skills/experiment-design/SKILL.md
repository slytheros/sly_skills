---
name: experiment-design
description: Use this skill to plan or review an experiment, pilot, or benchmark. Use it for A/B comparisons, factorial experiments, and formal evidence reviews.
---

# Experiment design

Start with a short experiment that can help the user make a decision. For formal claims, use [formal evidence](references/formal-evidence.md). For software or hardware measurements, use [systems benchmarking](references/systems-benchmarking.md). Use functional verification to check a specified deterministic behavior.

## Design a short experiment

1. **State the decision.** Identify the baseline and the candidate. Specify the conditions for the comparison. Define the smallest change that would affect the decision. If the user gives no threshold, state a practical assumption. If no threshold is available, use a pilot to learn what the procedure can measure.
2. **Define the primary outcome.** Specify the units, measurement procedure, summary statistic, and direction of improvement. Specify any acceptance limit for a secondary outcome. For example, limit the failure rate when the primary outcome is throughput.
3. **Identify the units.** The experimental unit is the unit that receives a condition. The observation unit is the unit that gives a measurement. Identify which units give independent repetitions. For example, many samples from one run share the run conditions.
4. **Control other causes.** Use the same procedure for all conditions. Check for factors that can affect the outcome and differ systematically between conditions. Randomize assignment or order when possible. Use pairs or groups of similar units when appropriate. Reset the system between runs if an earlier condition can affect a later result.
5. **Set the run budget.** Use a short pilot if the measurement, setup, or variation is unknown. Check the complete procedure in the pilot. Specify a run schedule and a stopping rule. Set rules for missing data, failures, and retries before you examine the results. Use more independent repetitions when extra samples from the same run add little information.
6. **Set the decision rule.** Specify how to calculate the effect. Specify how to show variation between independent repetitions. State when to keep the baseline, try the candidate, or get more data. Limit the conclusion to the tested conditions.

Record the date and the changes from the preceding experiment. If the results suggest a new hypothesis, use a new experiment to test it.

## Run and review

- **Run.** Run the experiment when the user requests execution and gives the necessary authorization. Check the setup before the first run. Keep the run schedule and raw data. Record failures and changes to the protocol. Follow the stopping rule. Keep pilot data separate unless the protocol specifies how to include them.
- **Review.** Compare the actual runs with the protocol. Check the assignment, independent repetitions, missing data, and stopping rule. Check for other causes of the observed effect. Report the effect and its uncertainty when the data permit. Identify results from analyses that you selected after you examined the data.
- **Report.** State what action the evidence supports. State the limits of the conclusion. If another experiment can change the decision, specify the simplest one. For a design request, give a procedure that the user can run.
