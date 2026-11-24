# Run TLC and interpret results

## Discover and run the tools

Use the project's wrapper or pinned tool artifact.
Otherwise locate the existing `tla2tools.jar` and compatible Java.
Record the artifact version or digest and tool version output.
These examples use POSIX shell syntax. Adapt them to the host as needed.
Set `TLA_TOOLS_JAR` to the discovered JAR.
Run from the module directory with project library paths configured.
`Model` is an example name.

```sh
java -version
java -cp "$TLA_TOOLS_JAR" tla2sany.SANY -help
java -cp "$TLA_TOOLS_JAR" tlc2.TLC -help
java -cp "$TLA_TOOLS_JAR" pcal.trans -help

# Only for modules with PlusCal. This replaces the generated translation.
java -cp "$TLA_TOOLS_JAR" pcal.trans Model.tla
java -cp "$TLA_TOOLS_JAR" tla2sany.SANY Model.tla
java -cp "$TLA_TOOLS_JAR" tlc2.TLC -workers 1 -config Model.cfg Model.tla
```

Parsing establishes well-formedness, not correctness.
Check diagnostics and process status. Keep stdout/stderr and exit status for evidence.
Do not let a logging pipe hide a failed process.
Choose heap, workers, runtime, and storage from available resources.
Stop at the task budget. Report an incomplete result instead of increasing resources indefinitely.
Keep generated states and traces out of source control unless the project retains them.

For libraries, record sources and loaded Java overrides, versions or digests,
and resolution paths. TLA+ source lookup differs from Java classpath lookup.
Proof-bearing imports can require `TLAPS.tla` during SANY and TLC runs without invoking the proof manager.
Resolve those imports from the project's selected library distribution.
See [runtime override guidance](examples-and-modules.md#separate-definitions-from-runtime-overrides).

### Isolate diagnostic runs from active work

Consider an isolated copy when concurrent work can change model inputs or source writes are prohibited.
Record copied input identities, including dirty working-tree bytes.
A commit identity alone does not identify those bytes.
Run from the copied module directory; `-metadir` alone does not redirect every generated artifact.
Report runtime substitutions against the project's accepted toolchain as diagnostic evidence.

## Profile before optimizing

Profile a manageable representative configuration with installed TLC or Toolbox facilities.
Separate expression cost, action state counts, and memory or storage pressure.
Invocation counts alone do not show enumeration cost.
A rarely evaluated `SUBSET` can dominate runtime.
Investigate unexpected disabled actions as possible model errors.

Use measurements to select one change.
Options include equivalent expressions, earlier filtering, justified abstraction,
or resource settings. Keep behavior and properties fixed for expression or resource changes.
For abstraction changes, state the preservation argument.
Compare unprofiled runs with identical constants, properties, tool versions, and budgets.
Record status, time, state counts, and resource use.
Do not claim faster checking by reducing verification coverage.

Profiling adds overhead. The documented profiler excludes liveness expressions
and distributed TLC. Check installed capabilities.
For enumeration costs, inspect relevant library operators and overrides first.
For example, `FiniteSetsExt` can avoid intermediate sets or unnecessary enumeration.
Verify that the override loads. See [enumeration examples](examples-and-modules.md#optimize-the-measured-enumeration).

## Configure a finite experiment

Bind all required constants. Select the intended behavior and properties.
A module with `Spec`, `TypeOK`, `Safety`, `Response`, and constant `Nodes` can use:

```text
SPECIFICATION Spec
CONSTANT Nodes = {n1, n2}
INVARIANTS TypeOK Safety
PROPERTY Response
```

Here `n1` and `n2` are model values.
Use `PROPERTY Response` only if the operator exists and progress is in scope.
For suitable safety models, `INIT` and `NEXT` can select behavior instead.
Do not omit fairness from `Spec` when checking liveness.
Classify each finite domain for the stated claim:

- **Full supported domain.** Justify that the bounds cover every supported value and configuration in scope.
- **Proved reduction.** Record the argument that the reduced domain preserves the property under check.
- **Sample.** Report the exact values checked and limit the result to those instances.

Check that exploration covers the behaviors required by the claim under the recorded assumptions.

Start with the smallest informative instance.
Consider safety-only development runs before expensive liveness checks.
Restore required temporal properties for acceptance.
Vary relevant actor counts, capacities, retries, failures, initial states, and message orders.
Empty or singleton domains can reveal errors or remove the behavior being tested.
Explain the selection. Use traces or coverage to confirm expected activity.
Check that important branches and implication antecedents can occur.
A temporary false property can test checking activity.
Keep it separate from accepted configurations.

Before each run, record its expected outcome and checking mode.
A negative control succeeds only at its intended property or scenario.
An unrelated failure, timeout, evaluation error, or unexpected clean run does not suffice.
Keep expected failures separate from acceptance models.
See [expected outcomes](examples-and-modules.md#select-and-reproduce-an-example).

### Distinguish reachability witnesses from broken-design controls

To test target reachability, check `NotReached == ~Target` as an invariant in a separate configuration.
Retain applicable safety invariants.
An intended `NotReached` violation establishes reachability, not a design defect.
For a combined safety-and-reachability claim, pair the witness with a completed safety run.
Use the same behavior and bounds.
A scripted scenario covers only the interleavings permitted by its control variable.

A passing progress implication can coexist with an unreachable response when its antecedent is impossible.
Use a response-reachability check to diagnose suspected vacuity.

### Select boundary witnesses deliberately

Choose values that permit the intended scenario.
If expiry equals a hard deadline, a strict-after-expiry return cannot occur within that deadline.
Use separate configurations when equality and strict-after cases both matter.
Do not move boundaries just to pass checks.
Record the case that each configuration permits.

Keep evidence that separates occurrence, commitment, and normal return.
A return state alone does not establish a satisfiable liveness antecedent.
Apply the [conditional-progress review](modeling.md#review-conditional-progress-as-a-component-contract).
Include required configurations in the project's inventory, if it has one.

For proofs over general ordered timestamps, check imported premises.
Finite configuration choices must not silently become general proof assumptions.
Label finite orderings as diagnostic unless a reduction is established.
Prove ordering and monotonicity facts needed by the general argument.
A discretization theorem is needed only for claims that transfer finite results.

## Diagnose failures before changing the model

- For an invariant failure, find the first violating transition.
  Identify the guard, actor, old and new values, and domain event.
  Locate the error in design, abstraction, configuration, or property.
- For deadlock, inspect disabled actions and possible legitimate termination.
  TLC checks enabled `Next` steps. Stuttering in `[Next]_vars` does not automatically
  suppress a deadlock report. Model termination or justify a configuration-specific
  `CHECK_DEADLOCK FALSE`. Do not suppress unexplained deadlock.
- For liveness, inspect the repeating cycle or infinite stuttering suffix.
  Identify enabled actors and review fairness premises.
  Do not add the desired outcome as an assumption.
- Treat evaluation errors, unbounded enumeration, and missing constants as model
  or tool failures. They are not counterexamples to the requirement.
- Review semantic warnings even when TLC exits successfully.
  Separate reported property results from unresolved frame-condition or action-evaluation warnings.

## Reduce state space without changing the claim silently

Remove irrelevant data and use justified abstraction before adding cutoffs.
State and action constraints prune exploration. They can hide counterexamples.
Record their effect and inspect boundary behavior, especially for liveness.
Check whether finite bounds permit fair infinite behaviors.
Report profiles where cutoffs make progress checks vacuous.
Do not report constraints as checked invariants.

Symmetry requires interchangeable identities in behavior and properties.
TLC does not prove the symmetry reduction sound.
Do not use symmetry reduction for liveness checks.
Justify property preservation before using lossy views or other reductions.

Separate completed exhaustive finite exploration from simulation, depth limits,
timeouts, memory exhaustion, cancellation, and safety-only completion.
Record generated and distinct states, completion messages, properties, and bounds.
A completed run with no reported violation covers only that finite configuration.
It does not establish correctness for every size or implementation execution.

For proof preparation, use [candidate-invariant checks](invariant-development.md).
If enumeration is too costly and another checker is permitted, consider
[Apalache](apalache.md). Measure it on the same verification question.

## Authoritative references

- [TLA+ tools CLI usage](https://github.com/tlaplus/tlaplus/blob/master/USE.md):
  tool entrypoints and integration.
- [TLC configuration documentation in the TLA+ extension](https://github.com/tlaplus/vscode-tlaplus/blob/master/resources/knowledgebase/tlc-config-files.md):
  model configuration and reductions.
- [Specifying Systems](https://lamport.org/tla/book.html), TLC chapter: checking
  semantics and model construction. Consult the installed help for current flags.
- [First-printing PDF, §§14.1 and 14.3.5](https://lamport.azurewebsites.net/tla/book-02-08-08.pdf):
  safety-first debugging and finite-model liveness limitations.
- [Official TLC profiling documentation](https://nightly.tlapl.us/doc/model/profiling.html):
  evaluation/action metrics, overhead, and limitations.
