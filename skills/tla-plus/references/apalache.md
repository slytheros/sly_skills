# Optional symbolic checks with Apalache

Consider Apalache when explicit enumeration limits useful TLC checks, or the
project already uses symbolic checks. Preserve the user's tool choice and requirements.
Find the installed version and supported options.
Installation or specification migration is a separate decision.
Neither is a prerequisite for this skill.

Apalache needs a supported typed specification and suitable annotations.
TLC compatibility does not establish Apalache compatibility.
Check language and encoding restrictions before adapting a large specification.
Measure a representative obligation. Do not assume symbolic checks are faster.

## Candidate-invariant commands

Check these examples against installed help.
Preserve project constant bindings and configuration on each invocation.
Here `IndInv` contains `TypeOK` and the complete candidate invariant.

```sh
apalache-mc --help
apalache-mc typecheck Model.tla

# Check initialization, preservation, and implication of safety.
apalache-mc check --init=Init --inv=IndInv --length=0 Model.tla
apalache-mc check --init=IndInv --inv=IndInv --length=1 Model.tla
apalache-mc check --init=IndInv --inv=Safety --length=0 Model.tla
```

Inspect the selected next-state predicate and constant assignments.
Exit codes alone do not establish the selected claim.
Use the [invariant workflow](invariant-development.md) to interpret counterexamples.
Check installed deadlock behavior separately from induction implications.

Reachability checks through length `k` do not establish unbounded safety.
Initialization, one-step preservation from all modeled invariant states, and safety
implication support induction over the modeled domains and assumptions.
They do not automatically quantify over every parameter size.
Separate solver evidence from TLAPS proof and required independent reconstruction.

If symbolic encoding dominates runtime, compare supported encodings under fixed
obligations, bounds, solver versions, and resource budgets.
Experimental encodings depend on the version.
Published benchmark improvements do not guarantee improvement for this model.
Record timeouts and unsupported constructs as well as successes.

## Sources

- [Official Apalache CLI and inductive-invariant checking documentation](https://apalache-mc.org/docs/apalache/running.html):
  current commands and distinctions between checking modes.
- [Apalache modeling principles](https://apalache-mc.org/docs/apalache/principles/index.html):
  type annotations and symbolic transition requirements.
- [Symbolic Model Checking for TLA+ Made Faster](https://link.springer.com/chapter/10.1007/978-3-031-30823-9_7),
  Otoni et al., TACAS 2023: array-based SMT encoding and experimental evaluation.
