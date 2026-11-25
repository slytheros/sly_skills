# Systems benchmarking

Use this reference for software and hardware measurements. For a formal claim, also use [formal evidence](formal-evidence.md).

## Define the measurement

1. Specify the system boundary and the baseline. Select a workload that represents the use in the decision. Specify the inputs, load pattern, concurrency, and operating conditions. Record the settings that differ between conditions.
2. Specify the unit and the start and end events for a timing measurement. For example, identify the event, its capture, the start of service, and the completion of service.
3. Check the clock source, resolution, and conversion to time units. Check clock synchronization when measurements use more than one clock or core. Check for counter wraparound where applicable. Measure or set a bound for instrument overhead and capture uncertainty. Check whether the instrument loses or cuts off data.
4. Specify the initial state, including the cache and the warm-up procedure. Record temperature, power settings, and background load when they can affect the result. Reset the system between runs when required. Use equivalent instruments and procedures for all conditions. Randomize the order within blocks when possible. [Mytkowicz et al., *Producing Wrong Data Without Doing Anything Obviously Wrong!*](https://sape.inf.usi.ch/publications/asplos09.html).
5. Check correctness and completion. Record the number of attempts, timeouts, missed deadlines, and invalid or incomplete measurements. Record the reason when known. Distinguish system failures from instrument failures. If a timeout gives only a lower bound on latency, keep that bound. State how timeouts affect the latency summary.

## Select the repetitions

Identify the sources of variation at each level. These levels can include build, device, session, and event. Record the identifier for each level that affects the claim. Events from one session share the session conditions. Use more sessions to estimate variation between sessions.

Use a short pilot to check the workload, reset procedure, and run time. Estimate variation and cost at each relevant level. Add repetitions at the levels that most affect uncertainty. Repeat builds if the claim includes variation between builds. Use pairs or blocks for comparable runs when appropriate. [Kalibera and Jones, *Rigorous Benchmarking in Reasonable Time*](https://kar.kent.ac.uk/33611/).

## Set limits on the claim

Define the summary before the runs. A summary of session percentiles gives each session a value. A pooled percentile gives more weight to sessions with more events. For a tail percentile or rare failure rate, check the number of events and independent runs. Account for dependence when you estimate uncertainty.

Report the sample maximum as an observed value. A hard deadline claim needs a justified worst-case bound for the specified operating conditions. Use target measurements for claims about timing on that target. Use simulation or emulation to check behavior under its model and to develop hypotheses for target tests.

Keep the exact artifacts and configurations. Record the test tools, input versions, event identifiers, and run order. Keep the raw traces or measurements.

## Example of an interrupt latency experiment

1. Compare firmware A and B on one board at a constant interrupt rate and background load. Measure the time from interrupt assertion to a marker at handler entry. Use the same calibrated instrument and markers for both builds.
2. Use a short pilot. Check that the instrument matches each interrupt to its marker. Measure clock resolution and marker overhead. Estimate reboot and capture time. For this example, set a minimum useful decrease of 5 microseconds.
3. Set a fixed budget for complete boot pairs. Use both AB and BA orders in equal numbers when possible. Randomize the sequence of pairs. Reset the board before each boot. Apply the same warm-up procedure for each boot.
4. Record the same number of attempted interrupts per boot. Keep counts of interrupts, missing markers, and instrument losses. Record the build, board, workload, and session identifiers. Keep the raw captures.
5. For this example, calculate the 99th percentile for a boot only if all attempted interrupts have a valid latency. Include only pairs with two percentile values in the latency summary. Report all incomplete pairs. Treat a missing marker as unresolved until the data show a system failure or instrument loss. Report the counts in each category.
6. Subtract the 99th percentile for B from the 99th percentile for A in each valid pair. Report the median and range of these differences. Use the range to describe variation across the observed pairs.
7. Try B in a follow-up experiment if every planned pair is valid and every difference is at least 5 microseconds. Require zero response failures for B. If the result is uncertain, design a new experiment with more pairs or a better measurement. Limit the result to the board, builds, and workload in the experiment.
