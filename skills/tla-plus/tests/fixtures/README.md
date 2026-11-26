# Diagnostic fixtures

The proof logs were captured with TLAPM v1.6.0-slytheros.2, with the executable
path and trailing whitespace normalized. The command was
`tlapm --strict --nofp --toolbox 0 0 --threads 1 MODULE.tla`. The timeout
capture added `--wait 0`.

| Log | Input and expected outcome |
| --- | --- |
| `grouped.log` | [GroupedMethod.tla](../../assets/backend-probes/GroupedMethod.tla), exit 0, two obligations proved. |
| `false.log` | `FalseGoal.tla`, exit 10, Isabelle fails on the false theorem. |
| `Fallback.log` | `THEOREM FallbackWorked == TRUE => TRUE` with `BY IsaMT("fail", 5), IsaMT("(rule impI, assumption)", 5)`, exit 0 after fallback. |
| `Timeout.log` | `THEOREM SlowProof == TRUE => TRUE` with `BY IsaMT("(rule impI, assumption)", 0.001)`, exit 10 with a backend timeout. |
| `truncated.log` | Prefix of the timeout capture cut inside the final attempt frame for obligation 1. |
| `oom.json` | Simulated explicit container runner evidence for the truncated log. |

The proof inputs extend `TLAPS`.

TLC 2026.11.19.180144 (rev `bc1b506`) produced `witness/Witness.tla`
with `java -cp "$TLA_TOOLS_JAR" tlc2.TLC -workers 1 -noGenerateSpecTE
-dumpTrace tla Witness.tla Counter`. Use `INIT Init`, `NEXT Next`,
`INVARIANT BelowLimit`, and `CONSTANT Limit = 2` in `Counter.cfg`.
The invariant fails in state 3. Both `BelowLimit` and `CanIncrement` hold
at state 2 and evaluate to false at state 3. The unsupported JSON fixture
exercises the format diagnostic.

`witness/AtomWitness.tla` was generated from `Atoms.tla` and `Atoms.cfg`
using the same TLC options. State 2 has two fields, including a bare model
value. The inspector must preserve that value's equality with members of
the configured set.
