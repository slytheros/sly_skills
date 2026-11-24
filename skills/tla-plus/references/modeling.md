# Construct and review models

## Choose an abstraction boundary

Start with the property and a possible violating execution. Keep the state and
steps needed to distinguish that execution from correct behavior.
Do not size the model from implementation fields or functions.
A behavioral abstraction can omit representations while preserving relevant
effects and interference.

For a delayed-timeout race, invocation identity, event time, ordering, and overflow
can matter. Timestamp byte encoding usually belongs in a separate representation
argument. Keep encoding details when the property depends on them.
Abstract payloads can suffice for ownership. Aliasing and partial-copy failures
need explicit effects or a separately checked boundary contract.

For composition, identify shared observations and producer/consumer guarantees.
Choose a joint-state model or a compositional proof as appropriate.
Conjoining component specifications can permit simultaneous actions.
Check interleaving restrictions and shared-variable frames explicitly.
Importing every concrete field does not establish coverage.
Relate required behaviors across boundaries, including rejection, intermediate
steps, and failure. Do not abstract away a possible violation.

Before large component proofs, test boundaries likely to affect the model.
For scoped or revocable operations, check these cases:

| Boundary | Question |
|---|---|
| Scope entry | Does every relevant path enter the required scope before using its guarantees? |
| Authorization | If authority changes, is it checked at the required use or commit point? |
| Identity reuse | Can an old delayed event affect a new invocation after cancellation, retirement, or reuse? |
| Resolution | Can the responsible actor complete, reject, or clean up after a consumer blocks or fails? |

Exercise relevant cases in a small joint model or trace.
Component-local invariants can hold while interactions violate the contract.
Repair the boundary. Do not assume the missing guarantee.

### Choose between proof restructuring and model redesign

For proof restructuring, keep the existing action relation as the source of the argument.
Use the proof-kernel checks below to justify each projection.

For model redesign, specify the observations, competing behaviors, and progress that the replacement must preserve.
Change internal steps where the required behavior permits it.
Relate the redesigned behaviors to the promised contract using a [refinement mapping](tlaps.md#refinement) where applicable.
Account for interference, failures, and allowed outcomes at the boundary.
Discharge the progress obligations under justified scheduling and environment premises.

### Calibrate an abstract proof kernel

A small record-value kernel can avoid a large concrete configuration and proof hierarchy.
Use a difficult behavioral interaction from the [feasibility trial](large-proof-projects.md#check-feasibility-before-scaling).
Check its projection from actual actions.
Evaluate both projections on the same concrete transition.
Preserve the existing action's guards, cancellation selectors, frames, and required observations in the projection argument.
Derive kernel premises from concrete assumptions and actions.
Connect the kernel conclusion to the required concrete property.
Check primed projection endpoints explicitly where needed.
Do not assume the desired post-invariant.

Track initialization, stuttering, remaining action projections, primitive contracts, and final invariant coverage as displaced obligations.
Treat the decomposition as provisional until the concrete projections and the join for the selected claim pass.

## State and transitions

Choose state that expresses the property and its failure.
Separate independent actors and environment actions. Include relevant failure,
retry, loss, and reordering. Do not assume the intended result in the environment.

For a conventional specification, define `vars`, `Init`, and the action disjunction
`Next`. A temporal specification can use `Spec == Init /\ [][Next]_vars`.
Add only justified fairness. A prime denotes the next-state value.
An action is a relation, not a sequence of assignments.
Prefer explicit next-state values, such as `v' = e` or `v' \in S`, over equations requiring inversion.
Constrain every next-state variable in each action. Use `UNCHANGED` for fixed values.
An omitted constraint permits arbitrary values. Keep `vars` complete.

Use nondeterminism for permitted alternatives. Give TLC finite domains.
Do not treat those domains as a universal theorem.
For actor or input selection, see [nondeterministic choice](modeling-patterns.md#preserve-nondeterministic-choices).
Include `TypeOK` for state shape and ranges. TLA+ is untyped; `TypeOK` is an
asserted property, not a static type declaration.
Check that initialization is satisfiable and represents intended starting conditions.

Combine implementation operations into one abstract step only with a preservation
argument. Include observations and interleavings needed by the property.
Review read-modify-write and check-then-act sequences carefully.
Stuttering leaves abstract state unchanged. It does not justify hiding an
intermediate state that can violate the property.

Before reusing operators, check domains, finiteness, empty inputs, order, and uniqueness.
Function restriction can break contiguous sequence indices.
A set fold need not preserve sequence order.
Retain required premises in typing facts and consumer proofs.
See [library contracts](examples-and-modules.md#check-operator-contracts).

### Add a state variable

For PlusCal, edit the algorithm and audit the [generated actions](#pluscal).

- [ ] Identify the variable's purpose, domain, and intended writers.
- [ ] Declare the variable in the module that owns it.
- [ ] Constrain its initial value on every `Init` branch.
- [ ] Extend `TypeOK` or the equivalent invariant if present.
- [ ] Audit every branch of every action in `Next`, including nested alternatives and branches in helper operators.
- [ ] Constrain the new variable's next value in every branch that permits a step.
  Use `UNCHANGED` where the value should stay fixed, including branches with no existing frame clause.
- [ ] Update the full state tuple used by `[Next]_vars`.
  Review shared frame operators and projected tuples before changing their scope.
- [ ] Recheck enabledness and nonstuttering steps for each affected fairness formula.
- [ ] For auxiliary state, check that hiding it preserves original safety and liveness behaviors.
  Use the [auxiliary-variable guidance](modeling-patterns.md#add-auxiliary-state-only-for-a-specific-mapping-problem).
- [ ] Parse the result and check affected properties in a small TLC model.
  Use a proof when the preservation claim requires one.

Based on the upstream [add-variable recipe](https://github.com/tlaplus/AgentSkills/blob/main/skills/tlaplus-add-variable/SKILL.md).

### Split an action

For PlusCal, split at a label and audit the [generated actions](#pluscal).

- [ ] Identify the original guard, effects, destination, and properties that depend on atomicity.
- [ ] Use the existing phase or program counter to represent the intermediate state when possible.
  Extend the control-state domain and affected type invariant.
- [ ] Route the first action to the intermediate state.
  Guard the second action on that state for the same actor.
  Route successful completion to the original destination.
- [ ] Check which original guards and values must survive the split.
  Capture old values when the second action must use the original observations.
- [ ] Audit every branch of both actions for explicit next-state constraints and frames.
- [ ] Update `Next` or its action groups to include both actions.
- [ ] Enumerate competing steps between the two actions, including retries, cancellation, and interference where relevant.
  Check their effects on intermediate invariants and on the second action's guard.
- [ ] Reassess fairness using the intended scheduling assumptions and the enabledness of each nonstuttering step.
  Check whether the second step can be disabled indefinitely or enabled only intermittently.
  Justify each fairness change against the [progress requirement](#safety-progress-and-fairness).
- [ ] Parse the result before checking it with TLC.
- [ ] Use a small TLC model to reach the intermediate state and exercise relevant competing steps.
  Check affected invariants, deadlock, and liveness.
- [ ] If refinement is required, relate each new step to an abstract step or stuttering.
  Check the required progress across the split.

Based on the upstream [split-action recipe](https://github.com/tlaplus/AgentSkills/blob/main/skills/tlaplus-split-action/SKILL.md).

## Safety, progress, and fairness

Where possible, express safety as predicates over reachable states.
Use history variables or temporal formulas when the behavior requires them.
Separate the desired safety property from a stronger inductive invariant.
A reachable-state invariant need not hold inductively over every state satisfying it.

For progress, identify the trigger, required response, and responsible actor.
Separate eventual response (`P ~> Q`), perpetual availability, and absence of deadlock.
Examine infinite stuttering and cycles that postpone work.

- `WF_vars(A)` prevents indefinite postponement of a continuously enabled
  nonstuttering action. It does not ensure service if enablement keeps disappearing.
- `SF_vars(A)` also covers nonstuttering actions enabled infinitely often.
  Justify this stronger scheduling or environment assumption.

Choose fairness for the relevant action or process.
Fairness of a disjunction does not imply fairness of each branch.
Justify assumed lock service, interrupt delivery, and device completion.
Fairness alone gives no wall-clock deadline.
Check whether assumptions exclude the failure or make a progress trigger unreachable.
When liveness should only schedule permitted steps, check machine closure.
Machine closure means each finite safety prefix has a continuation satisfying liveness.
Fairness on actions outside `Next` can remove safety prefixes.

### Review conditional progress as a component contract

Identify the component responsible for each progress premise.
Examples include advancing time, captured events, finite demand, valid input,
and resource supply. A consumer can assume service under a component contract.
Trace each premise to an environment contract or an independently established result from its supplier.
Reject a premise if its only justification depends on the progress claim it supports.

Derive each action's guard at the point where the temporal argument needs it.
Identify which reachable-state facts or component guarantees supply the guard.
Check what other actions can do while the guard holds.
An action can become permanently disabled after a consumer fault.
Fairness then need not provide service. If opportunities occur independently of
consumption, model or justify those occurrences separately.
Counters must represent actual supply actions. Unrelated steps must not simulate progress.

Check that temporal premises can hold together.
Eventual service plus service-before-deadline excludes late-service behaviors.
It does not prove deadline feasibility. For a claimed conditional outcome,
justify a behavior satisfying the complete antecedent and a compatible infinite continuation.
A reached return state alone is insufficient.
Label deliberately impossible antecedents as vacuous tests.

Separate abstract service from physical schedulability.
Positive resource charges at one timestamp can represent logical milestones,
rather than executable CPU fragments. Atomic event capture or endpoint writes
leave transport and partial-copy obligations elsewhere when those matter.
State the required correspondence argument.

### Example: resolve a pending request

This model starts with one pending request and a closed resource.
The provider opens the resource. Service and cancellation are distinct terminal outcomes.
The requirement counts either outcome as resolution.

~~~tla
---- MODULE RequestResolution ----
VARIABLES status, ready

vars == <<status, ready>>
Pending == status = "pending"
Resolved == status \in {"served", "cancelled"}

Init == Pending /\ ~ready
Open == Pending /\ ~ready /\ ready' = TRUE /\ UNCHANGED status
Serve == Pending /\ ready /\ status' = "served" /\ UNCHANGED ready
Cancel == Pending /\ status' = "cancelled" /\ UNCHANGED ready
Done == Resolved /\ UNCHANGED vars
Next == Open \/ Serve \/ Cancel \/ Done

Spec == Init /\ [][Next]_vars /\ WF_vars(Open) /\ WF_vars(Serve)
Resolution == Pending ~> Resolved
====
~~~

The reachable-state invariant gives `ready \in BOOLEAN` and
`status \in {"pending", "served", "cancelled"}`.
Initialization and each step of `[Next]_vars` preserve these facts.
The initial state witnesses reachability of the trigger with readiness false.

1. From a pending state with readiness false, the invariant gives `ready = FALSE`.
   The provider can take `Open` with successor `<<"pending", TRUE>>`.
   The successor satisfies the frame condition and changes `ready`.
   While the request remains pending and unready, `Open` stays enabled.
   Weak fairness forces opening unless cancellation resolves the request first.
2. From a ready pending state, service can take `Serve` with successor `<<"served", TRUE>>`.
   The successor preserves `ready` and changes `status`.
   The action establishes `Resolved`.
   Every step that leaves the request pending preserves readiness from this state.
   Weak fairness forces service unless cancellation resolves the request first.
3. The first argument gives `Pending ~> ((Pending /\ ready) \/ Resolved)`.
   The second gives `(Pending /\ ready) ~> Resolved`.
   Combine both with `Resolved ~> Resolved` to derive `Resolution`.

A request that cancels before opening falsifies a service-only response requirement.
If a late arrival can repeatedly revoke readiness, reopening and revocation can alternate forever.
Service is then enabled intermittently, which satisfies weak fairness without service.
Recheck persistence or justify a different progress premise from the actual model.

## PlusCal

Preserve existing PlusCal syntax. Use PlusCal when procedural control flow helps.
Use direct TLA+ when action relations or refinement are clearer.
PlusCal labels define atomic steps. Statements between labels are not independent
interleavings. Review labels around shared reads, writes, `await`, and retries.

After algorithm edits, [translate](tlc.md) and inspect generated `Init`, `Next`,
control variables, fairness, and termination. Repair the algorithm source, then
regenerate. Do not repair the generated translation by hand.
Preserve translation markers and checksums. Include generated control state in
manual state tuples or properties where required.
The generated terminal stuttering action represents termination.
It does not justify disabling all deadlock checks.

## Authoritative references

- [Specifying Systems](https://lamport.org/tla/book.html): action semantics,
  stuttering, invariants, composition, fairness, and refinement.
- [First-printing PDF, §§7.6, 8.9.2, and 10.1](https://lamport.azurewebsites.net/tla/book-02-08-08.pdf):
  next-state definitions, machine closure, and simultaneous component steps.
- [Lamport's PlusCal tutorial](https://lamport.azurewebsites.net/tla/tutorial/home.html):
  procedural specifications and translation-based checking.
