# Small backend controls

Use these controls to diagnose TLAPS invocation or a custom Isabelle method.
Copy [the modules](../assets/backend-probes/) to a temporary directory.
Do not include them in accepted project proofs.
Two controls intentionally fail. One intentionally omits its proof.
Check installed help before using the flags below.

## Reproduce and retain diagnostics

Set `TLAPM` to the discovered executable.
Set `TLA_PROBE_SOURCE` to this skill's `assets/backend-probes` directory.
The POSIX shell commands below were tested with TLAPM `901ae51`,
source commit `901ae51ed5224f88d43a1a02969cd9be4ed1b48d`.
The build included Isabelle2025 and Poly/ML 5.9.1.
These controls select Isabelle. They need no legacy SMT encoder or tool upgrade.

```sh
probe_directory=$(mktemp -d)
cp "$TLA_PROBE_SOURCE"/*.tla "$probe_directory/"
cd "$probe_directory"
"$TLAPM" --version > tool-version.txt 2>&1
"$TLAPM" --help > tool-help.txt 2>&1
"$TLAPM" --config > tool-config.txt 2>&1

# Run serially; each authored method has a five-second backend timeout.
# Preserve individual statuses: the loop's status is not an acceptance result.
for module in GroupedMethod FalseGoal Incomplete MalformedMethod ExactValues
do
    "$TLAPM" --strict --nofp --threads 1 --debug tempfiles "$module.tla" \
        > "$module.stdout" 2> "$module.stderr"
    probe_status=$?
    printf '%s\n' "$probe_status" > "$module.exit"
done
```

Keep the directory, including hidden `.tlacache` files.
Retain original modules, commands, and tool identities.
In the tested build, `tlapm_*.thy` and `.thy.out` files contain backend input and output.
Check that diagnostics actually retain these artifacts.
Flags and locations can change between versions.
Do not use these debug runs as project acceptance evidence.

## Observed outcomes

These results were checked on 2026-10-19 with the build above.
Backends ran fresh, with fingerprint reuse disabled.
Counts include TLAPS-generated support obligations.
These observations do not define behavior for other versions.

| Module | Exit | Observed result |
|---|---|---|
| `GroupedMethod` | 0 | All 2 obligations proved; generated method is `by (rule impI, assumption)`. |
| `FalseGoal` | 10 | 1/2 obligations failed; Isabelle reports failure to apply the method to `FALSE`. |
| `Incomplete` | 11 | One omitted proof; also prints `All 0 obligation proved`, which is insufficient evidence of success. |
| `MalformedMethod` | 10 | 1/2 obligations failed; Isabelle reports an outer-syntax error at the ungrouped comma. |
| `ExactValues` | 0 | All 4 obligations proved: exact set equality and equality of a small record with its explicit function representation. |

`GroupedMethod` and `MalformedMethod` state the same valid theorem.
Only method grouping differs.
`FalseGoal` has valid method syntax and an intentionally false claim.
Both failure cases return 10. The summary alone cannot distinguish syntax failure
from an unsuccessful method. An unsuccessful method does not establish a false theorem.

`ExactValues` illustrates exact set and record equality.
It does not establish a general large-record construction or remove enumeration limits.
Test the actual required size and operations separately.
Prove equivalence of any changed representation.

For setup, encoding, timeout, or interruption failures, keep the original reproducer
and process or backend evidence.
These controls neither simulate those failures nor establish large-proof feasibility.

## Test output interpretation

When changing an output parser, runner, or status classifier, you SHOULD include captured tool output in regression fixtures.
Record the producing command, tool version, exit status, and expected interpretation.
Use real output variations alongside focused synthetic cases.
Preserve diagnostics needed to classify failures when removing sensitive or host-specific data.
Ordinary proof work does not require fixture infrastructure.

For negative controls, you MUST identify the intended failing claim and expected failure reason.
Successfully proved support obligations are permitted.
Check the target obligation and its diagnostics rather than rejecting every output that reports some success.
A crash, launch failure, encoding error, or syntax error does not satisfy a logical negative control.

## Primary references

- [TLAPS tactics](https://proofs.tlapl.us/doc/web/content/Documentation/Tutorial/Tactics.html):
  `IsaMT`, custom methods, and backend selection.
- [TLAPS options and strict outcomes](https://proofs.tlapl.us/doc/web/content/Documentation/Tutorial/Advanced_options.html):
  exit-code interpretation and worker limits; installed help governs availability.
- [Isabelle/Isar proof method expressions](https://isabelle.in.tum.de/dist/library/Doc/Isar_Ref/Proof.html):
  method composition and grouping; consult the matching release when reproducing.
- [Tested TLAPM Isabelle backend source](https://github.com/tlaplus/tlapm/blob/901ae51ed5224f88d43a1a02969cd9be4ed1b48d/src/backend/isabelle.ml):
  emitted theory and proof-method integration; inspect actual generated input too.
- [Matching record rules](https://github.com/tlaplus/tlapm/blob/901ae51ed5224f88d43a1a02969cd9be4ed1b48d/isabelle/Zenon.thy)
  and [function rules](https://github.com/tlaplus/tlapm/blob/901ae51ed5224f88d43a1a02969cd9be4ed1b48d/isabelle/Functions.thy):
  sources to inspect for arity-specific rules and generic introduction premises,
  rather than assuming a permanent backend-size limit.
