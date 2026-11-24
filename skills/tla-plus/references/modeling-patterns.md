# Apply modeling patterns from worked examples

Use the [example-reuse workflow](examples-and-modules.md#select-and-reproduce-an-example) when adapting these sources.

## Preserve nondeterministic choices

Use `\E p \in Actors : Step(p)` to permit any eligible actor.
Use `x' \in Values` to permit any next value from a finite domain.

`CHOOSE p \in Actors : Eligible(p)` denotes a fixed witness for the same predicate and domain.
It does not explore every eligible actor.

You MAY use `CHOOSE` for a unique witness or an intentionally arbitrary fixed value.
Establish existence before relying on the selected value's predicate.
Establish uniqueness when the intended meaning requires it.
For message selection, ordering and tie-breaking facts can establish uniqueness.

The [EWD998 workshop](https://github.com/tlaplus-workshops/ewd998/blob/main/EWD998.tla)
contrasts receiver selection with deterministic choice.
The [Paxos specification](https://github.com/tlaplus/Examples/blob/master/specifications/Paxos/Paxos.tla)
uses `CHOOSE` to define a sentinel outside the proposed values.

## Select a message representation

Choose the representation from observable order, multiplicity, consumption, and failure effects.

| Representation | Preserved information | Required review |
|---|---|---|
| Set of messages ever sent | Message availability and contents | Repeated receipt remains possible; consumption and multiplicity are absent. |
| Set of messages in transit | Presence of each distinct message | Equal copies collapse; removal can erase all indistinguishable copies. |
| Bag or per-message counts | Multiplicity without order | Receipt must decrement a count; duplication and loss need applicable actions. |
| Sequence | Order and multiplicity | Receipt guards determine whether delivery is FIFO or permits reordering. |
| Aggregate count | Quantity without individual contents | Distinct identities and contents need a separate preservation argument. |

In [TwoPhase](https://github.com/tlaplus/Examples/blob/master/specifications/transaction_commit/TwoPhase.tla),
`msgs` retains every sent message.
For its safety claim, loss is indistinguishable from never receiving an available message.
Repeated receipt has no additional effect in that protocol.
Reassess this abstraction for delivery, capacity, consumption, and non-idempotent effects.
Do not infer eventual delivery from permanent message availability.

[EWD998Chan](https://github.com/tlaplus/Examples/blob/master/specifications/ewd998/EWD998Chan.tla)
stores inboxes as sequences but receives from an existentially selected position.
Inspect receipt actions before inferring FIFO behavior from a sequence type.
For a FIFO example, inspect `Head`, `Tail`, and `Append` in
[InnerFIFO](https://github.com/tlaplus/Examples/blob/master/specifications/SpecifyingSystems/FIFO/InnerFIFO.tla).

## Relate concrete steps to an abstract contract

Use the [refinement obligations](tlaps.md#refinement) to relate concrete and abstract specifications.
Instantiate the abstract module with `INSTANCE ... WITH` when substitution is needed.
Preserve shared variables directly when they already have the required meaning.

[TCommit](https://github.com/tlaplus/Examples/blob/master/specifications/transaction_commit/TCommit.tla)
defines the transaction outcome contract.
`TwoPhase` preserves its `rmState` variable and states `TPSpec => TC!TCSpec`.
This example specifies safety only.

### Add auxiliary state only for a specific mapping problem

| Mapping problem | Candidate auxiliary variable |
|---|---|
| The abstract state remembers information already discarded by the concrete state. | History variable |
| The abstract contract commits to a choice before the concrete execution determines it. | Prophecy variable |
| Matching the specifications requires additional steps that preserve original state. | Stuttering variable |

You MUST preserve original behaviors when hiding auxiliary variables.
You MUST preserve the original liveness condition when applying the auxiliary-variable construction.
Do not mechanically replace fairness with fairness over auxiliary-only movement.
For prophecy, establish prediction coverage using the construction's premises.

Use [Auxiliary Variables in TLA+](https://lamport.org/pubs/auxiliary.pdf),
sections 3–5, for construction rules and liveness conditions.
Section 6 develops a snapshot and linearizability example.
Consider a simpler mapping before introducing prophecy or stuttering machinery.

## Make time progress explicit

For unbounded-time claims, you MUST justify that time advances without bound.
Infinitely many clock steps can still approach a finite limit with dense time.
Such executions are Zeno behaviors.

Use chapter 9 of [Specifying Systems](https://lamport.org/tla/book.html)
for explicit clocks, timing bounds, and non-Zeno requirements.
Use the [conditional-progress review](modeling.md#review-conditional-progress-as-a-component-contract) to assess deadline feasibility and assumption compatibility.

## Validate observed executions

Map logged events and values to specification actions and variables.
Preserve causal order and the model's atomicity boundary in that mapping.
Account for implementation events that require zero, one, or several specification steps.
Do not infer a distributed total order from unsynchronized timestamps alone.
Treat unlogged state as unknown rather than unchanged.
Constrain missing values through permitted specification steps and finite enumerable domains.

Acceptance requires at least one complete trace match, not successful extension of every partial assignment.
Do not reject a trace solely because one candidate matching path deadlocks.
Classify discrepancies as implementation, specification, instrumentation, or mapping problems.
A finite accepted trace establishes compatibility of those observations with some permitted behavior.
It does not establish universal refinement or eventual progress after the recorded prefix.

[Validating Traces of Distributed Programs Against TLA+ Specifications](https://arxiv.org/abs/2404.16075)
describes partial-state logging and matching with TLC.
The [EWD998 trace-validation notes](https://github.com/tlaplus/Examples/blob/master/specifications/ewd998/EWD998ChanTrace.md)
show logging-boundary mistakes, missing events, causal-order issues, and atomicity mismatches.
Trial a representative trace before building extensive instrumentation.
MongoDB's [eXtreme Modelling in Practice](https://arxiv.org/abs/2006.00915)
reports an unsuccessful trace-checking project and successful model-based test generation.
Choose between these techniques using model alignment and integration cost.
