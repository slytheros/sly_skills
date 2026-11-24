# Model implementation and embedded behavior

## Allocate behavioral and representation obligations

Separate the behavioral specification, boundary contracts, and implementation checks.
Use TLA+ for interactions at the selected abstraction level.
Concrete arithmetic, layouts, buffers, pointers, and decoders can need implementation
tools, such as CBMC or a deductive C verifier.
Choose from the claim and available project workflow.
Do not require another tool or move obligations just because a proof is difficult.

State boundary identities, values, permitted effects, unchanged state, and interference.
Include success, rejection, and partial failure as applicable.
Relate concrete pre/post states to abstract steps or stuttering.
Check producer bodies and consumer preconditions. Do not assume valid requests
or desired postconditions without justification.
Local code checks plus a model proof do not establish unrestricted implementation refinement.
Retain bounds, applicability arguments, and unresolved premises.
Keep assembly, hardware, weak-memory, and timing evidence with their actual owners.

## Connect the model to the code

Start with relevant call paths, shared state, synchronization, and interfaces.
For important model actions and state, identify the code counterpart and abstraction.
Record atomicity justification and omitted detail.
Use the project's verification notes; a small table can suffice.
Record source revision and configuration. Reassess affected assumptions after code changes.

Select action granularity from the property.
A locked region can be atomic only if competing observers cannot distinguish
relevant intermediate states. An unlocked test and update usually need separate steps.
Do not replace weak atomics with sequential consistency without justification.
For linearizability, identify the linearization point.
Include pending operations and observations needed by that claim.

Relate counterexamples to plausible calls, scheduling, failures, or device observations.
An impossible implementation trace can reveal an overly permissive abstraction.
An unsupported assumption excluding a trace can reveal a design problem.
Keep evidence before changing the model or code.
Tests and trace replay support correspondence. They do not prove refinement of
every implementation execution.
For execution logs, use the [trace-validation guidance](modeling-patterns.md#validate-observed-executions).

## Embedded concurrency

Include only relevant platform details. Use target architecture, SoC, and driver contracts.
Keep these distinctions explicit:

- **Interrupts and scheduling:** include relevant mask scope, priorities, nesting,
  pending events, coalescing, preemption, and per-core state.
  Local interrupt masking does not stop other cores or DMA.
  Justify eventual delivery or task service.
- **Ownership and DMA:** distinguish ownership transfer, publication, device access,
  completion, reuse, cancellation, and reset.
  A software flag update need not make data visible to another observer.
- **Memory and MMIO:** separate language atomics, architectural ordering, cache
  visibility, device ordering, and completion.
  Model visibility steps when needed, or justify the ordering abstraction.
  A barrier is not a universal flush or completion event.
- **Faults and timing:** include relevant lost or spurious interrupts, device failure,
  counter wraparound, and reset.
  For timing claims, model time and its advance assumptions.
  Qualitative fairness alone gives no latency bound.

For exact weak-memory claims, use an established formal model or tool.
Otherwise state the limits of the TLA+ abstraction.
A few instruction effects do not establish architecture verification.
Coherency, instruction lowering, and real-time bounds need their own evidence.

## Review scenarios

Use relevant scenarios to test the abstraction:

| Scenario | Question |
|---|---|
| Two callers see a free slot before either claims it | Did the model incorrectly combine the check and claim? |
| A task clears a flag while an interrupt publishes work | Can work be lost? What ensures another notification? |
| A CPU publishes a DMA descriptor before payload visibility | Which documented ordering contract excludes stale data? |
| A lock waiter is enabled only briefly | Does weak fairness establish the required service? |
| Reset races with late device completion | Does ownership or generation tracking prevent reuse corruption? |

Use these as review prompts. Do not add every scenario to every model.
Keep the user's verification scope.

## Authoritative references

- [Specifying Systems](https://lamport.org/tla/book.html): abstraction,
  composition, refinement, and explicit real-time specifications.
- For concrete ordering and device guarantees, consult the consuming project's
  exact language, architecture, SoC, and device documentation. TLA+ language
  semantics do not supply those platform facts.
