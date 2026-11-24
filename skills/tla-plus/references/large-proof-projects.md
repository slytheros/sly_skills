# Manage substantial proof efforts

Use this reference for proofs that span many lemmas, components, or work sessions.
Keep small edits lightweight. Use the consuming project's evidence format.
Do not introduce a separate acceptance system.

## Reassess the approach before scaling

Apply the [abstraction review](modeling.md#choose-an-abstraction-boundary) before
building proof infrastructure. Use the [feasibility trial](#check-feasibility-before-scaling)
to test the proposed proof boundary.

Stop expansion when repairs repeatedly add support lemmas, modules, or expanded
state without closing required behavioral obligations. Also stop when support
cost dominates the argument or exceeds the task budget. Do not treat more proof
text or more passing fragments as evidence of adequate progress.
This includes repeated witness or frame-condition expansion without behavioral progress.
Review the abstraction before generating more similar proofs.

Within a fixed part of the remaining budget, compare the current approach with a
smaller abstraction or a different decomposition. Include:

- The required guarantee and behaviors that each option preserves.
- Boundary contracts and concrete obligations that each option leaves elsewhere.
- Expected total checking cost, restart cost, and maintenance cost.
- Measured results, remaining uncertainty, and the reason to continue or stop.

Report the tradeoffs before substantial further expansion. Recommend a redesign
or report the proof blocked if no option is feasible. Preserve valid requirements
and project acceptance rules. Do not require reuse of prior proof work.
Do not turn a model-checking task into a general proof project without a claim
that needs one.

## Plan proof boundaries before expensive runs

Inspect required claims, actions, invariant components, imports, and reusable support before writing or checking large proof families.
Flag these structural risks:

- Action projections import large invariant proofs that their local arguments do not use.
- One preservation argument spans several action families or invariant components.
- Consumers repeatedly expand the same typing facts, namespace conversions, record updates, or deep definitions.
- A case split or namespace bridge expands many guarded alternatives at once.
- Related measurements show high aggregate obligation preparation, backend startup, or search costs within one module.

Use the smallest useful proof boundary for each risk:

- Separate lean action projections from the heavier invariant-preservation joins that consume them.
- Group action cases or invariant components into cohesive proofs with explicit shared premises.
- Establish reusable typing, domain, field, and namespace facts once in dependency order.
- Keep final joins focused on composition and coverage.
- Use local lemmas when they isolate the cost adequately.
- Create separate modules when they reduce import context or bound complete-body checking costs.

Treat these criteria as early risk indicators.
Do not impose universal line, theorem, or module-count thresholds.
Do not create one module per lemma merely to satisfy a limit.

Apply a successful trial's decomposition to structurally similar proofs.
Revisit the grouping when a materially different proof structure appears.

Preserve required guarantees, behavior, guards, assumptions, and theorem premises during decomposition.
Retain any required joint invariant when proving component cases separately.

### Inspect proof-bearing model dependencies

Inspect both `EXTENDS` and `INSTANCE`, including transitive dependencies and redundant imports.
Models can inherit large proof hierarchies merely to access definitions.
You SHOULD keep semantic definitions in model modules and explicit proof dependencies in proof modules.
Import diamonds can amplify inherited contexts despite small source files and final joins.
Preserve definitions, theorem availability, constants, instance bindings, and actual consumers during refactoring.
Do not remove imports indiscriminately or assume namespace aliases reduce processing cost.

In SANY from tla2tools 1.7.4, `processExtendsList` invokes `copyTheorems` for each extendee.
That method appends inherited theorem vectors without deduplication.
See the matching [Generator](https://github.com/tlaplus/tlaplus/blob/v1.7.4/tlatools/org.lamport.tlatools/src/tla2sany/semantic/Generator.java#L2010-L2043)
and [ModuleNode](https://github.com/tlaplus/tlaplus/blob/v1.7.4/tlatools/org.lamport.tlatools/src/tla2sany/semantic/ModuleNode.java#L563-L568) sources.

## Check feasibility before scaling

Select one difficult required claim that exercises the proposed interfaces.
Use the [trial inputs and decision rule](../SKILL.md#run-a-bounded-feasibility-trial).
Set an observable resource limit before launch. Use the installed toolchain and required trust settings.
Include the typing, mathematical, and component support used by the claim.
For an abstract kernel, include the [concrete projections](modeling.md#calibrate-an-abstract-proof-kernel).

If liveness is required, choose a claim that exercises enabledness and fairness.
Start from a reachable trigger in the actual specification.
Derive readiness from the reachable-state invariant or an established progress premise.
If readiness is delayed, prove how the behavior reaches the guard or resolves the trigger first.
Construct a successor that satisfies the action, frame conditions, and nonstuttering on the full state tuple.
Show what the action achieves towards the required response.
Check whether interference, cancellation, or late arrivals can revoke readiness or change the response.
Apply the justified fairness rule to reach the required temporal conclusion.
See the [request resolution example](modeling.md#example-resolve-a-pending-request).

Check the final join for the selected claim with its actual imports.
Check the authored support bodies that supply its premises.
Apply the project's [trust policy](examples-and-modules.md#reuse-checked-support-theorems) to library facts.
Expand to similar cases only after this chain checks within the budget.
If the trial stalls, [locate the blocker](tlaps.md#structure-proofs-for-tractable-obligations) within the remaining budget.
At expiry, [stop the active run](#keep-long-runs-interruptible) and stop trial work.
Record the open required claim and the evidence needed to reproduce the blocker.
Passing helpers do not close an open final join.

- Recommend **continue** when the evidence supports a specific next stage within the available budget.
- Recommend **redesign** when the current approach is infeasible and another route can preserve the guarantee.
- Recommend **resolve a product decision** when the next step depends on intended behavior or a product-owned premise.

Explain any uncertainty in the recommendation. An expired trial needs a new budget before further attempts.

## Preflight integration before expensive acceptance

Use the project's checks, dependency order, and acceptance contract. As a general
rule, record the development and acceptance commands, selected scope, and cache policy.
State which cached results each command can reuse and when it invokes backends.
Use the same runner with different options where suitable.
Development checks can use selections and valid cached results.
During exploration, check the affected claim and its relevant dependencies.
Retain the selected claim, input identity, command, tool settings, and result needed to reproduce a blocker.
Collect backend-by-backend diagnostics for failure investigation, performance measurement, or a project requirement.
Audit [compiled-module reuse separately from proof-result caching](tlaps.md#audit-cache-scope).

Use this general sequence:

1. Parse changed modules. Check module names and import resolution.
2. Check affected proof bodies and authored dependencies with the actual imports
   and required tool, backend, and trust settings.
3. Run the remaining proof and integration checks required for acceptance.

Selected theorems and standalone copies can help diagnosis. They do not replace
required checks of complete bodies. After a repair, repeat affected inexpensive
checks before restarting an expensive run. Invalidate affected evidence when
sources, definitions, assumptions, imports, configuration, or tools change.
If dependencies are uncertain, mark the enclosing claim stale.

Some projects require manifests, parameter profiles, ownership records, hashes,
or claim-to-evidence inventories. Check these only when the project requires them.
Follow its schema, freshness rules, controls, and independent verification rules.
Do not impose these examples on other projects. If acceptance requires one fresh
complete run, do not combine results from different input snapshots.

You MUST separate performance measurements, final validation, and assurance claims.
Before claiming assurance, run a fresh, complete check of the frozen candidate and its required proof dependency closure.
Check for omitted or open obligations and empty selections.
Use the project's trust policy and all required acceptance controls.
Independent validation does not inherently require another prover or reviewer.
Record backend attribution and completed reconstruction at the detail the project's acceptance rules require.
An “all obligations proved” summary can still fail required artifact validation.
Retain required artifacts and the evidence needed to reproduce failed attempts.
Do not weaken classifiers or acceptance rules to make an experiment pass.
Report trusted assumptions, accepted libraries, transformations, and unchecked dependencies that limit the assurance claim.
See [backend roles and trust](tlaps.md#backend-roles-and-trust).

### Bind parameter profiles to the actual model

If the project uses parameter profiles, derive constants from the actual import
closure and instance substitutions. Bind profiles to the model that they describe.
Distinguish a valid empty profile from a missing or malformed profile.
Do not invent bounds or parameters to satisfy metadata requirements.
Use the project's controls for transitive constants and unrelated proof constants.

## Freeze inputs and bound execution

Before an expensive run, identify the source and import snapshot, configuration,
libraries, tools, and backends. Include uncommitted and generated inputs where
applicable. Review the exact integrated changes. Do not copy a whole candidate
directory over newer repairs. Keep outputs separate from source inputs.
Do not edit a snapshot while a check uses it.
Bind results to that input identity. Reject results with missing or changed inputs.

When resource costs are unknown, start with one heavy proof process. Measure
representative difficult modules and their support. Select concurrency from
available resources and measured use. Include each process's backend workers.
Estimate the full run's cost and uncertainty. Report material cost and restart
risk before launch. Preserve task budgets and project limits.

Record commands, limits, elapsed time, completion status, and exit status.
Record CPU time and peak memory where available and useful.
For slow checks, [locate the cost](tlaps.md#locate-the-cost-of-slow-checks) before changing proof structure or backend settings.

### Compare total checking cost

Split when the boundary improves the argument or measurements show a checking-cost benefit.
Compare equivalent claims under the project's cache, trust, and resource rules.
For an overall improvement claim, measure complete affected bodies and all required authored dependencies.
Include import processing, new modules, retries, and backend fallbacks.
Keep overall claims provisional when measurements cover only selected proofs or omit dependencies.

A bounded retry with unchanged inputs can test host timing sensitivity.
Preserve the result of each attempt.
Stop retries at the planned limit.
If stable execution is required, repair the cause or report the blocker.
Follow the consuming project's limits and acceptance rules.

### Keep long runs interruptible

Before launch, choose how to stop the run and its workers.
Record the runner or direct prover process identity and the log location.
For a direct invocation, use a dedicated job or process group where supported.
Track owned workers or containers that can outlive the parent.
Use the project's runner controls when available.

Cancel superseded runs. On stop, cancel the active run.
Verify that the runner and all owned workers and containers have exited before resubmitting or reporting the run stopped.
If an owned process remains, report its identity and status.
Preserve logs, input identity, resource observations, and the next bounded command.
Mark unfinished checks incomplete. Recheck the input identity and remaining checks before resuming.
During long runs, report material failures, delays, or revised estimates.

## Build in dependency order

Work backward from the required guarantee. Use the actual dependency graph.
A common safety proof order is:

1. Necessary mathematical support and typing facts.
2. Initialization of the strengthened invariant.
3. Preservation by each action, including environment and recovery actions.
4. Coverage of `Next`, stuttering, and required component interactions.
5. The final safety theorem and its connection to the required guarantee.

For refinement or liveness, include the additional simulation, temporal, and
fairness obligations. Discharge component assumptions through valid composition.
Do not use circular component guarantees as premises.

For a large invariant, record which current-state lemmas support each action's
preservation obligation. For lemma `L` and action `A`, the shape can be
`Support /\ L /\ A => L'`. Split obligations where that helps the argument.
Use [counterexamples to induction](invariant-development.md) to find missing support.

Support dependencies can form cycles under simultaneous induction. Prove every
lemma initially. Then prove every action preserves each lemma from the complete
current-state invariant. Check the final conjunction. Do not assume a next-state
lemma to prove itself.

Keep diagnostic views focused on relevant variables, guards, and updates.
A smaller displayed trace does not justify removing verification state or premises.
Require a validity-preservation argument for any logical slicing transformation.

Close useful increments, such as an action case and its callers. State which
required guarantee each increment advances. Mark affected dependents stale after
changes. Do not regenerate valid unrelated proof text just for uniformity.

## Maintain a completeness ledger

Track progress by required claims closed. Use the project's evidence format.
For each claim, record its premises, their suppliers, and authored proof bodies still due for checking.
Record the evidence status, location, input identity, and check command.
Group shared metadata. Include composition, refinement, and liveness where required.

This example shows a hypothetical status for the [pending request proof](modeling.md#example-resolve-a-pending-request).

| Required proof step | Premise and supplier | Status |
|---|---|---|
| Service has a nonstuttering successor under its guard | `Pending /\ ready`, supplied by the caller | Action lemma checked. |
| A pending request reaches readiness or resolution | `Open` fairness from the resource provider, with preservation from `Next` | Check the readiness progress proof and its preservation support. |
| A ready pending request reaches resolution | `Serve` fairness from the service process, with persistence from `Next` | Check the temporal proof that uses the action lemma. |
| `Pending ~> Resolved` | Both progress theorems and their authored support | Open until the support and the final join check. |

Separate finite TLC results, TLAPS results, and implementation correspondence.
Distinguish fresh, cached, incomplete, blocked, and stale evidence.
Report edits, checked bodies, checked dependency closure, and final acceptance
as different states when the project uses those stages. State remaining checks.

Before declaring a guarantee closed, follow its dependencies to the final checked
theorem. Locate the required body checks for authored support theorems.
Apply the project's policy to explicitly approved trusted libraries.
A passing consumer does not prove an unchecked authored dependency.
Report partially verified guarantees and blockers. Do not summarize progress
by theorem counts, fragments, or the number of proof modules.

## Package evidence when review requires it

Use the project's format and required evidence. This can include source inputs,
configurations, tool identities, results, witnesses, and reproduction commands.
Preserve historical receipts. Give current commands when old receipts contain
host-local paths. If portability is required, check an extracted package outside
the original path. Check required source and evidence identities, not just hashes.
A new manifest cannot make stale evidence valid. Hashes do not authenticate an
unsigned manifest. Do not execute historical shell text as an audit shortcut.

## Supporting references

- [TLAPS proof workflow](tlaps.md): obligation diagnosis, backend roles, trust,
  and proof completeness.
- [Interactive Safety Verification of Distributed Protocols by Inductive Proof Decomposition](https://arxiv.org/abs/2404.18048v2),
  Schultz et al., revised 2026: lemma/action proof graphs, localized induction
  counterexamples, and variable slicing. Finite counterexample search guides
  development; the reported final proofs are validated with TLAPS.
- [TLAPS hierarchical proof tutorial](https://proofs.tlapl.us/doc/web/content/Documentation/Tutorial/Hierarchical_proofs.html):
  structure and dependencies within checked proofs. The project-management
  practices above supplement the proof language; they are not TLAPS requirements.
