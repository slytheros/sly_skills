# Reuse examples and community modules

Use external material to answer a specific modeling or verification question.
Reuse only the needed definitions and proof support. An example does not require
adoption of its whole toolchain.

## Select and reproduce an example

Use the [TLA+ Examples catalog](https://github.com/tlaplus/Examples) to find relevant
techniques. Read the selected specification, README, configuration, and manifest.
Distinguish CI-validated entries from external or unvalidated examples.
Record the source revision. Reproduce the relevant baseline before adaptation.
Catalog inclusion does not verify an adaptation.

For choice, message, refinement, time, or trace examples, read the [modeling patterns](modeling-patterns.md).
Search manifest features and expected failures for specific techniques, such as `proof`, `pluscal`, or `liveness failure`.

The [manifest schema](https://github.com/tlaplus/Examples/blob/master/manifest-schema.json)
separates checking modes and expected outcomes. Use this distinction in the
project's evidence format. Identify the expected property and scenario for a
negative control. An unrelated failure does not satisfy the control.
Historical runtime and state counts help planning. They do not guarantee cost
on another machine or configuration.

## Preserve abstraction caveats

Check why a reduction preserves the required property. Take particular care
with liveness and generalization from finite models.
[FiniteMonotonic](https://github.com/tlaplus/Examples/tree/master/specifications/FiniteMonotonic)
describes finitization but reports no proof of soundness and completeness.
Preserve that limitation when adapting the technique. Do not report exploration
as an unbounded theorem. See [reduction guidance](tlc.md#reduce-state-space-without-changing-the-claim-silently).

## Separate definitions from runtime overrides

[CommunityModules](https://github.com/tlaplus/CommunityModules#how-to-use-it)
provides definitions and some Java implementations for TLC.
Pin the selected sources and runtime artifact. Record versions or digests,
lookup paths, and actual Java requirements. Do not use a moving `latest`
dependency for reproducible evidence. Check which implementation the run loads.
A copied `.tla` file alone does not establish an active Java override.

Inspect definitions, overrides, and tests when the claim depends on correspondence.
Test representative and boundary inputs when adopting or changing an override.
Samples support diagnosis. They do not prove universal equivalence.
A TLC runtime result differs from a TLAPS proof about a definition.

Some helpers have external effects.
[IOUtils](https://github.com/tlaplus/CommunityModules/blob/master/modules/IOUtils.tla)
includes file operations and subprocess execution. Inspect effects before running
an unfamiliar model. Stay within the task's authorization.

## Check operator contracts

Read definitions and premises. Do not rely on an operator's name alone.

- [Functions](https://github.com/tlaplus/CommunityModules/blob/master/modules/Functions.tla)
  defines domain requirements for restriction and pointwise operations.
  Filtering entries can leave gaps in sequence indices. Use sequence-preserving
  operations when consumers require sequences.
- [Folds](https://github.com/tlaplus/CommunityModules/blob/master/modules/Folds.tla)
  makes selection order explicit. For an order-independent result, establish
  associativity and commutativity on the actual operand domain. Otherwise use
  an explicit order. Arbitrary set traversal does not establish sequence order.

Check finiteness, empty inputs, existence, uniqueness, and result shape as needed.
Derive premises from model facts. Do not exclude permitted behavior just to make
a helper applicable.

## Reuse checked support theorems

Search for existing mathematics before writing replacement lemmas.
CommunityModules' [conventions](https://github.com/tlaplus/CommunityModules#the-modules)
place some theorems in `MTheorems.tla` and proofs in `MTheorems_proofs.tla`.
Match definitions, premises, and instance substitutions to the model.
Then apply the project's trust policy:

- For authored or modified support proofs, check required bodies and dependencies.
  Importing a theorem statement does not prove its body.
- For explicitly approved trusted libraries, use the approved version and assumptions.
  Record the dependency and applicable trust. Recheck bodies only as the project requires.
- For other libraries, establish acceptable proof evidence or obtain an explicit
  trust decision. Do not silently treat missing proofs as trusted mathematics.

Do not require each project to rebuild elementary mathematics.
Do not change its trusted base without authorization. Finite TLC results do not
prove library laws. See [TLAPS trust and completeness](tlaps.md#commands-and-proof-completeness).

## Optimize the measured enumeration

[FiniteSetsExt](https://github.com/tlaplus/CommunityModules/blob/master/modules/FiniteSetsExt.tla)
provides a `kSubset` override that enumerates subsets of the requested size.
`Quantify` avoids an intermediate filtered set. Consider these operators when
profiling identifies the relevant cost. Check domains, semantics, and the loaded
implementation. Compare fixed bounds, properties, and resources.
Separate an equivalence argument from a measured speed improvement.
