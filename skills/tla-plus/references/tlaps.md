# Develop and check TLAPS proofs

## Establish the theorem and supporting invariant

State the theorem, constant assumptions, and exact specification. Where executable
instances exist, use small TLC checks to refute candidate lemmas early.
Finite checks do not discharge general proof obligations.

Before writing elementary mathematics, look for existing definitions and theorems.
Match their premises and substitutions to the model. Distinguish authored support
proofs from libraries explicitly accepted under the project's trust policy.
Check authored proof dependencies as required. Do not require fresh proofs of
approved library mathematics unless the project requires them. Do not silently
expand the trusted base. See [library reuse](examples-and-modules.md#reuse-checked-support-theorems).

Before duplicating successor witnesses, you SHOULD specialize an applicable general theorem.
If specialization fails, inspect the generated obligation for missing premises or relationships hidden by abstraction or preprocessing.
Expose only the definitions needed to connect the theorem and goal before adding proof infrastructure.
Construct witnesses when no suitable theorem applies.

For mathematical laws accepted as assumptions, finite TLC definition overrides
can find transcription errors. TLC checks `ASSUME`, not `AXIOM`.
Bounded checks do not prove a general law. Report the trusted assumptions.

Before extensive proof writing, use the
[candidate-invariant workflow](invariant-development.md).
For an invariant proof, find a strengthening `Inv` and establish:

1. `Init => Inv`.
2. `Inv /\ [Next]_vars => Inv'`, including each action and stuttering.
3. `Inv => Safety`.
4. `Spec => []Safety`, with an applicable induction rule.

State necessary typing, ownership, uniqueness, and history facts. Prove
preservation from arbitrary states satisfying `Inv`. TLC observations alone
are insufficient. A failed preservation proof can indicate a weak invariant,
an incorrect action, or an incorrect property. Do not assume the missing result.

## Structure proofs for tractable obligations

Use hierarchical `ASSUME/PROVE`, `SUFFICES`, `CASE`, and local lemmas to show why
each step follows. Split `Next` by action where useful. Supply facts and
definitions through `BY`, `DEF`, and scoped `USE`. A named fact is not necessarily
usable by a backend. Keep relevant hypotheses visible.

For a failed obligation, increase diagnostic detail as needed:

1. Start with the failed goal, relevant assumptions, usable facts, and visible
   definitions. Keep the source version, command, reported error, and exit status.
   Check syntax, missing premises, domains, priming, and cases first.
2. Make one justified repair. Rerun the obligation and affected dependent proofs.
   Record the result. Do not require an isolated module for a clear local error.
3. If the failure persists or appears tool-related, retain generated backend input,
   backend commands, stdout/stderr, and tool/library identities. Use supported
   diagnostics in an isolated run. Capture temporary artifacts before removal
   when they are needed. Report unavailable artifacts.
4. Reproduce a persistent or suspected tool failure in a selected step or temporary
   module. Preserve the original logical context before reducing it. Confirm the
   same failure. A reduction that changes the failure is a different experiment.
5. Locate the failing boundary below. After repair, rerun the original obligation
   and the checks required by the project's acceptance rules.

| Failing boundary | Evidence and action |
|---|---|
| Parsing or elaboration | Repair reported source, name, or proof syntax errors. |
| Backend launch or encoding | Check executables, libraries, supported constructs, and generated input against the installed version. |
| Backend method syntax | Inspect the generated method and syntax error. Test the correction on a small valid goal. |
| Method leaves a goal | Check premises, domains, definitions, priming, and cases. An unsuccessful method does not refute the theorem. |
| Missing proof | Close the missing body. A zero-obligation summary does not establish completeness. |
| Timeout or termination | Locate the active phase and check resource evidence before retrying. See [slow check diagnosis](#locate-the-cost-of-slow-checks). |
| Stale inputs | Identify source or tool changes. Rerun affected checks on consistent inputs. |

You MUST distinguish individual backend attempts from the final obligation result.
Preserve available attempt history, including fallback within one run.
Classify unsuccessful search, timeout, crash, launch failure, and encoding error separately.
Distinguish encoding failures, internal timeouts, and timeouts after backend launch.
A successful fallback can follow ordinary search failure or timeout.
Earlier unsuccessful attempts do not automatically invalidate the successful proof.
Report their diagnostic and resource costs separately from proof status.

Selected steps, backend experiments, and debug runs are diagnostic evidence.
They do not replace required complete proofs or trust checks. Use the
[backend controls](backend-probes.md) when invocation or reporting is in doubt.

Switch backends for a supported logical fragment, an unavailable backend,
an internal failure, or a bounded diagnostic comparison. Preserve theorem and
trust requirements. Do not cycle through solvers or increase timeouts indefinitely.
Before repeated decomposition adds more support, apply the
[large-proof stop rules](large-proof-projects.md#reassess-the-approach-before-scaling).

### Locate the cost of slow checks

Before retrying a slow or terminated run, identify its last confirmed phase.
Compare wall time with supported `--timing` output, backend attempts, and available process data.
Use the following evidence to select a bounded diagnostic check.

| Phase or failure | Evidence to collect |
|---|---|
| Parsing or import elaboration | Parse with the actual import paths. Check transitively loaded modules and semantic processing before any obligation output. |
| Obligation generation | Compare supported generation-only output and timing. Check normalization, obligation counts, and reporting volume. |
| Backend startup or encoding | Check whether a worker started and accepted its input. Inspect launch, encoding, or scheduling delays before attributing time to search. |
| Solving or reconstruction | Compare per-attempt solve times with wall time. Check fallback attempts and any separate reconstruction phase. |
| Resource exhaustion or enforced limits | Check exit status, limits, and available host, runner, or container records. Compare peak resource use with the applicable limit. |

An unexplained SIGKILL does not establish memory exhaustion.
An `interaction` total or near-zero backend time does not locate the cost.
Inspect matching tool source when timings and logs cannot locate the phase.
Interpret log milestones against the installed revision.

At TLAPM commit `901ae51ed5224f88d43a1a02969cd9be4ed1b48d`, statistics output reports obligation totals before fingerprint loading/cleanup.
See the [revision-matched driver](https://github.com/tlaplus/tlapm/blob/901ae51ed5224f88d43a1a02969cd9be4ed1b48d/src/tlapm_lib.ml#L311-L398).

Use `-N` to inspect obligation generation without backend execution when the installed tool supports it.
This experiment does not check the proof or measure every backend encoding cost.
Count generated obligations, trivial obligations, and backend launches separately.
Cited `BY` facts can generate additional obligations; source theorem counts do not predict checking cost.

| Observed cost | Candidate experiment |
|---|---|
| Many small backend calls | Compare a direct conjunction or tuple-frame proof with separate field proofs. Keep useful abstraction lemmas. |
| Repeated unsupported-fragment failures | Test a local supported method or proof decomposition. Distinguish encoding failure from unsuccessful search. |
| Large diagnostic logs | Compare output modes with unchanged proof inputs. Preserve diagnostics required by the project's evidence contract. |

A leaf pragma can override the command-line method; inspect the actual backend attempts.

Benchmark the changed body and required support using the
[total checking cost rules](large-proof-projects.md#compare-total-checking-cost).
Use the [interruption procedure](large-proof-projects.md#keep-long-runs-interruptible)
to account for owned processes before retrying.

### Repair common proof stalls

Use these patterns after identifying a logical or search failure.
They do not repair launch or encoding errors.

| Symptom | Targeted repair |
|---|---|
| `BY ONLY` stops proving a step | Cite needed facts, including ordinary enclosing `ASSUME/PROVE` hypotheses. Known domain formulas remain available. `ONLY` does not hide already usable definitions. Inspect the generated obligation if context is unclear. |
| Function equality, application, or `EXCEPT` stalls | Prove function shape and exact domains. Establish `i \in DOMAIN f` where needed. Prove pointwise equality on the common domain. Equal selected fields alone do not prove function equality. |
| `ENABLED` stalls on successor choices | Construct successor witnesses. Prove guards, updates, frame conditions, and witness domains. For fairness, prove nonstuttering enabledness: `ENABLED A` alone need not imply `ENABLED <<A>>_vars`. Check installed support such as `ExpandENABLED`. |
| Small leaves pass but `QED` times out | Use named preservation, projection, enabledness, or progress lemmas. Expand only needed outer connectives. Use `HIDE DEF` for large usable definitions where necessary. `BY ONLY` alone does not hide them. Apply the stop rules before repeated expansion. |
| Large formulas or expanded `LET` expressions | Introduce equivalent local definitions. Prove needed facts, then use `HIDE DEF`. Proof-local definitions are usable by default. Specification definitions need explicit use. |
| Circular equalities stall Isabelle rewriting | Break rewrite cycles with hidden local definitions. |
| Set equality stalls | Prove membership equivalence. Cite set extensionality for SMT, or try `IsaWithSetExtensionality` for Isabelle. |
| `CHOOSE` reasoning stalls | Prove existence and the property for every satisfying witness. With no witness, the value is fixed but arbitrary. Handle that case separately. SMT can lack choice determinacy axioms. `NoSetContainsEverything` supports choosing outside a set. |
| Records stall in Zenon or Isabelle | Cite relevant field equalities. SMT can need less help. |
| An instantiated theorem does not match local facts | Discharge instantiated module assumptions. Relate prefixed and local operators when aliases become distinct backend symbols. |

One justified successor can prove enabledness of a nondeterministic action.
This proof does not restrict the action to that successor. Check witness domains,
especially for possibly empty sets. Separate first-order successor reasoning from
temporal assembly. The [consensus example](https://github.com/tlaplus/Examples/blob/master/specifications/byzpaxos/Consensus.tla)
reduces nonstuttering enabledness to a state predicate.

### Reduce preprocessing pressure with explicit facts

For tactic comparisons, keep the normalized goal and hypotheses unchanged where
the tool exposes them. For context changes, preserve the required claim and
justify the transformation. Identical normalization is not required for changed contexts.
Keep tool versions, resource limits, and cache policy fixed across comparisons.
Keep both results. A cached success does not measure fresh backend cost.

When definitions expand excessively, prove the small facts that the consumer needs.
Examples include constructor equalities, domains, field values, and arithmetic.
Use only needed facts and definitions, with `BY ONLY ... DEF ...` where appropriate.
Retain required hypotheses and justified support. Smaller contexts can reduce
cost, but they do not justify different trust settings.

For example, consider `\A i \in DOMAIN children : ChildOK(children[i])`.
If the constructor gives `DOMAIN children = {}`, prove that fact first.
The quantified conjunct is then vacuous. If another conjunct needs
`depth + 1 <= bound`, separately prove suitable facts such as `depth = 0`
and `bound >= 1`. An empty child domain does not imply zero depth.
This example illustrates decomposition. It is not a checked module or permission
to add these conditions as model guards.

Preserve theorem statements and model semantics during context reduction.
`LOCAL` controls visibility; it is not necessarily an AST-pruning or memory boundary.
Verify the installed implementation before recommending `LOCAL` helpers or instances for performance.
Do not assume the result, remove needed premises, or increase limits to force success.
After diagnosis, run [required body and acceptance checks](large-proof-projects.md#preflight-integration-before-expensive-acceptance)
with actual imports. Apply the stop rules if support continues to grow.

For an Isabelle backend that emits `by <method>`, group multiple methods.
The checked control uses `IsaMT("(rule impI, assumption)", 5)`.
The ungrouped string causes an outer-syntax error on the tested version.
Inspect generated text before copying a method across proofs.
Correct grouping fixes syntax. It does not establish mathematical adequacy.

Do not upgrade tools without a demonstrated need. If an upgrade is necessary,
record new identities and check positive, false, and incomplete controls.
Apply required trust and reconstruction checks. Check soundness before using a
legacy encoder. A compatible or passing encoder is not necessarily sound.

If liveness is required, run the early
[enabledness and fairness trial](large-proof-projects.md#check-feasibility-before-scaling).
An installed backend does not establish support for the required temporal fragment.
`PTL` handles propositional temporal reasoning. It does not automatically prove
arbitrary quantified temporal or fairness arguments. Use supported rules and
explicit progress lemmas. Report missing arguments or tool limitations.
Do not report a safety proof as a liveness proof.

## Backend roles and trust

Inspect installed configuration. Do not assume a fixed backend set or order.

| Backend | Role |
|---|---|
| SMT | Automated reasoning over supported first-order encodings and theories, including arithmetic. Results depend on encoding and solver support. |
| Zenon | First-order tableaux proof search. Supported proofs can be reconstructed through Isabelle/TLA+. |
| Isabelle/TLA+ | A TLA+ formalization in Isabelle. TLAPS can invoke tactics such as `auto` or `blast` without an interactive session. |
| PTL | Propositional temporal reasoning through the configured temporal prover. It does not replace quantified temporal or first-order arguments. |

Record the backend that discharged each obligation, at the detail needed by the
project. Separate backend success from independent proof reconstruction.
Where supported, `tlapm -C Model.tla` requests Isabelle checking of supported proofs.
Check its scope and actual output.
SMT or Zenon success does not establish completed independent Isabelle reconstruction.
Do not claim reconstruction of all SMT or PTL results.
Reconstruction still trusts the formalization and TLAPS transformations.

For substantial or composed proofs, use the [large-proof workflow](large-proof-projects.md).

## Probe large records and enumerations

Before working around a suspected backend limit, inspect the installed rule
library or matching source. Test small cases around the suspected boundary.
Record rule names and versions. A rule's fixed arity in one build does not
establish a universal record limit. Separate parsing, encoding, search, and reconstruction.

For record or function packing, prove function shape, exact domain, index-domain
equalities, and field membership from existing premises. Check introduction-rule
premises. Mentioned fields do not establish that an unconstrained value is a function.
Use parameterized constructor, update, or eta lemmas only when needed.
Discharge their premises at each consumer. Reassess before support dominates.

For large enumerations, test the needed size and representative operations before
proof generation. After representation changes, prove exact equality of names
and values. Equal cardinalities can conceal substitutions or duplicates.
Preserve domains, field associations, statements, and project parameter contracts.
The [exact-value control](backend-probes.md) is a small illustration, not a general
large-record solution.

Do not add desired-result guards, assumed support laws, unnecessary state, or
weaker claims to make a representation work. A parsed but unrun candidate remains
unverified. Do not publish it as a checked recipe.

## Refinement

State concrete and abstract specifications. Map abstract variables to concrete
expressions. Prove mapped initialization and step simulation, including abstract
stuttering. Justify any history or prophecy variables.
When redesigning, map the new steps to the promised observations and competing behaviors.
Check coverage of required behaviors separately from inclusion of permitted behaviors.
Safety simulation alone does not transfer liveness. Discharge the required
fairness and progress obligations. Specification refinement still needs a separate
correspondence argument to implementation code.

## Commands and proof completeness

Use the project's prover command. Otherwise locate `tlapm` and inspect its
configuration, library paths, and supported options:

```sh
tlapm --version
tlapm --help
tlapm --config

# Use only if installed help lists --strict.
tlapm --strict Model.tla

# On older versions, check completeness explicitly.
tlapm Model.tla
```

Pass include directories through supported `-I` options. Keep output and exit status.
A selected theorem verifies only that selection. Recheck affected modules and
dependencies after edits. Cached GUI status can be stale.
Use supported fingerprint controls, such as `--nofp`, when fresh checks are required.
Do not delete project caches indiscriminately.

### Audit cache scope

Distinguish proof-result fingerprints from compiled AST/module caches.
`--nofp` does not necessarily disable compiled-module reuse.
Audit compiler identity, transitive dependency freshness, selection settings, and target/imported status.
Verify full obligation regeneration when the project's freshness rules require it.
A cache keyed only by the current source file can be insufficient.

At commit `901ae51ed5224f88d43a1a02969cd9be4ed1b48d`, the driver filters selected obligations before compiled-module storage.
See the [revision-matched driver](https://github.com/tlaplus/tlapm/blob/901ae51ed5224f88d43a1a02969cd9be4ed1b48d/src/tlapm_lib.ml#L386-L398).
This ordering does not establish cache invalidation correctness or behavior in other releases.
Verify the matching loader, generator, and cache implementation before relying on reuse.

### Check completeness and report results

Newer versions document these strict exit codes: 0 for complete verification,
10 for failed obligations, 11 for incomplete proofs, and 12 for an empty selection.
Internal errors use 3. Confirm behavior in the installed binary.
Older releases can return success with omitted proofs, including
`All 0 obligation proved`. Inspect intended theorem statuses and expected
obligation selection. Identify unjustified steps, `OMITTED`, and `PROOF OMITTED`.
Audit `ASSUME`, `AXIOM`, and imported trusted facts. A checked theorem remains
conditional on its trusted assumptions. An axiomatized lemma is not a proved lemma.

Separate cached status, generated obligations, and actual backend execution.
Report fresh versus cached results and the applicable trust policy.
Claim independent reconstruction only when it completed.
Use [backend controls](backend-probes.md) when invocation or reporting needs testing.
These controls do not prove a project's theorem or establish proof feasibility.

## Authoritative references

- [TLAPS advanced options](https://proofs.tlapl.us/doc/web/content/Documentation/Tutorial/Advanced_options.html):
  backend concurrency, method selection, fingerprints, and obligations generated for cited facts.
- [TLAPM command-line implementation](https://github.com/tlaplus/tlapm/blob/main/src/tlapm_args.ml):
  diagnostic generation and timing options. Match behavior to the installed revision.
- [TLAPS pragma definitions](https://github.com/tlaplus/tlapm/blob/main/library/TLAPS.tla):
  local backend selection and pragma precedence.
- [TLAPS practical hints](https://proofs.tlapl.us/doc/web/content/Documentation/Tutorial/Practical_hints.html):
  expression size, rewriting, extensionality, choice, records, theorem instances,
  decomposition, and mathematical assumptions.
- [TLA+ Version 2 guide, §7.2](https://lamport.azurewebsites.net/tla/tla2-guide.pdf):
  `BY ONLY`, usable facts/definitions, and domain formulas.
- [TLAPS hierarchical proof tutorial](https://proofs.tlapl.us/doc/web/content/Documentation/Tutorial/Hierarchical_proofs.html):
  scoped facts, decomposition, induction, and propositional temporal reasoning.
- [TLAPS prover options and exit codes](https://proofs.tlapl.us/doc/web/content/Documentation/Tutorial/Advanced_options.html):
  strict-mode behavior, fingerprints, and status checking.
- [TLAPS tactics](https://proofs.tlapl.us/doc/web/content/Documentation/Tutorial/Tactics.html):
  backend selection and proof maintainability.
- [Isabelle/Isar reference: proof methods](https://isabelle.in.tum.de/dist/library/Doc/Isar_Ref/Proof.html):
  method expressions and grouping; use the installed release's documentation.
