---
name: tla-plus
description: Write, review, explain, and verify TLA+ and PlusCal specifications with TLC. Develop and debug TLAPS proofs. Use for concurrent protocols, distributed systems, implementation-derived models, and embedded state machines. Cover safety, liveness, fairness, and refinement.
compatibility: Specification editing requires no runtime. SANY, PlusCal translation, and TLC require compatible Java and tla2tools.jar. TLAPS proofs require TLAPS and its configured backends.
---

# TLA+ Specification and Verification

First, identify the required guarantee, actors, environment, and abstraction boundary.
Identify the evidence that the user needs. For explanation tasks, explain the
formulas and behaviors. Do not create a verification project unless the task needs one.
Follow the consuming project's acceptance rules. Existing representations and
module layouts do not prevent a redesign that the user requests.

## Establish the existing contract

Inspect the relevant specifications, configurations, proofs, build commands, and
implementation paths. Identify constants, assumptions, model bounds, fairness, and
excluded behaviors. Get tool paths and versions from project configuration.
Do not install or upgrade tools just to use a preferred workflow. Report missing
tools and give commands for pending checks.

Use the smallest model that preserves the interactions needed by the property.
Separate component checks do not establish composition. Separate requirements,
assumptions, and implementation choices. Resolve ambiguities that change the
verification claim. Record other consequential assumptions.

## Choose the assurance approach

Separate behavioral checks, proofs over parameter domains, and implementation
correspondence. Select TLC, TLAPS, implementation tools, or a combination from
the required claim. A faithful model need not copy implementation details.
It does not automatically require an unbounded deductive proof.

Before substantial expansion, state which observations and interleavings the model
preserves. Identify abstracted representations and remaining concrete obligations.
State how to discharge those obligations. Include valid inputs, invalid inputs, and failure effects.
Classify each [finite domain](references/tlc.md#configure-a-finite-experiment) as full supported scope,
a justified reduction for the claim, or a sample.
Separate model and code checks do not establish correspondence.

## Run a bounded feasibility trial

Before substantial modeling or proof work, record:

- The required guarantee in plain language.
- One execution that would violate the guarantee.
- The owner and independent basis of each progress premise.
- The trial budget and the decision the trial will inform.

[Check one difficult required claim end to end](references/large-proof-projects.md#check-feasibility-before-scaling)
before expanding to similar cases. Stop the trial when its budget expires.
Recommend **continue**, **redesign**, or **resolve a product decision** when the trial ends.
Explain the recommendation using the evidence and any open required claim.
Choose proof tactics yourself. Refer unresolved choices about intended behavior to the maintainer.

## Load guidance for the task

Read only the references needed for the task:

- [Modeling](references/modeling.md) covers abstraction, action projections,
  atomicity, fairness, conditional progress, and PlusCal translation.
- Use the modeling checklists to [add a state variable](references/modeling.md#add-a-state-variable)
  or [split an action](references/modeling.md#split-an-action).
- [Modeling patterns](references/modeling-patterns.md): nondeterministic choice, message
  representations, refinement mappings, auxiliary variables, time, and worked examples.
- [TLC](references/tlc.md): finite configurations, commands, counterexamples,
  reductions, and run status.
- [TLAPS](references/tlaps.md): invariants, processing phases, caches, backend diagnosis,
  refinement, trust, and completeness.
- [Examples and libraries](references/examples-and-modules.md): external models,
  operators, Java overrides, and library theorems.
- [Large proofs](references/large-proof-projects.md) covers proof boundaries,
  feasibility trials, claim tracking, execution cost, and interruption.
- [Implementation and embedded models](references/implementation-and-embedded.md):
  code correspondence, interrupts, DMA, ownership, and memory ordering.

For language semantics or version-sensitive behavior, check the official sources
linked in each reference. Use the installed tool's help to check command options.

## Iterate and report evidence

Translate changed PlusCal and inspect the generated TLA+. Parse changed
specifications before checking properties. Use small TLC instances to find model
errors and test candidate invariants. Use TLAPS when the claim needs deductive proof.
Explain counterexamples in domain terms before changing the model or requirement.
Do not weaken a property, suppress deadlock, or add fairness just to pass a check.

Report the checked modules, configurations, or theorems. Include tool versions,
commands, assumptions, bounds, completion status, and unresolved obligations.
Separate finite checks, checked theorems, and implementation correspondence.
Model evidence alone does not establish implementation, hardware, or timing correctness.
