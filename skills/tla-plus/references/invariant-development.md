# Develop invariants with counterexamples to induction

Use this workflow to find or strengthen an invariant before deductive proof.
Define `IndInv` with required `TypeOK` facts and candidate support lemmas.
Keep the desired `Safety` claim explicit. Check three obligations:

1. Initialization: `Init => IndInv`.
2. Preservation: `IndInv /\ Next => IndInv'`.
3. Sufficiency: `IndInv => Safety`.

Include stuttering in the final temporal proof.
Ordinary reachable-state checks can refute candidates.
They do not check preservation from every state satisfying `IndInv`.
Some such states can be unreachable from `Init`.

## Use TLC on finite instances

Keep the ordinary configuration for reachable-state checks.
For a separate induction experiment, keep finite constant bindings and use:

```text
INIT IndInv
NEXT Next
INVARIANTS IndInv Safety
```

This checks preservation and sufficiency over enumerated invariant states.
Check initialization separately with the ordinary initial predicate.
The induction experiment does not check liveness or inherit fairness from `Spec`.
State intentional terminal states and deadlock policy.
An evaluation error or deadlock report does not establish a failed induction implication.

TLC needs enumerable initial states.
Bind variables through finite domains before evaluating predicates that use them.
Apply filters once their dependencies are bound, before enumerating unrelated choices.
Preserve logical equivalence.

Enumeration of all type-correct states can cost more than reachable-state exploration.
Start with a tiny instance. If enumeration is too costly, consider bounded random
sampling or the optional [symbolic checker](apalache.md).
A passing sample is neither exhaustive checking nor proof.
Keep sampled states or enough replay information.
A seed alone need not capture every source of randomization.

## Strengthen from the actual failure

Keep each counterexample's predecessor, action, successor, failed conjunct, and bounds.
An unreachable predecessor can show an insufficient invariant without a reachable bug.
If a reachable predecessor violates safety, investigate the design.
Do not exclude a permitted execution just to strengthen the invariant.

Propose small lemmas for the missing relationship.
Check ordinary reachable states, then the problematic induction predecessors.
Prefer relevant lemmas over unrelated accumulated facts.
Individual conjuncts need not be inductive. Recheck initialization, preservation,
and sufficiency of their conjunction. Track
[lemma/action dependencies](large-proof-projects.md#build-in-dependency-order).
If support keeps growing without advancing the required guarantee, apply the
[stop rules](large-proof-projects.md#reassess-the-approach-before-scaling).

After finite or sampled exploration, use the project's required method to discharge
the general theorem and its support. Do not generalize finite evidence to all parameters.

## Sources

- [Using TLC to Check Inductive Invariance](https://lamport.azurewebsites.net/tla/inductive-invariant.pdf),
  Leslie Lamport, 2018: alternate initialization, enumeration order, and randomized
  induction-counterexample search. Use installed-tool documentation for current
  randomization operators rather than copying the note's old version advice.
- [Plain and Simple Inductive Invariant Inference for Distributed Protocols in TLA+](https://iandardik.github.io/assets/papers/ind_inf_fmcad22.pdf),
  Schultz, Dardik, and Tripakis, FMCAD 2022: candidate lemma generation and selection
  by induction-counterexample elimination. The method informs this workflow;
  its research tool is not a required dependency.
