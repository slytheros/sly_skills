# Inspect saved proof logs and TLC witnesses

Both scripts require Python 3.10 or later. They use the Python standard library.
Use the reports to investigate a run under your project's acceptance rules.

## Summarize a TLAPM log

Run TLAPM in Toolbox mode on one module. Save stdout and stderr in the same log.
Keep the original log, command, and exit status.
Set `TLA_SKILL_DIR` to the directory containing this skill's `SKILL.md`.

```sh
tlapm --toolbox 0 0 Model.tla > proof.log 2>&1
proof_status=$?
python3 "$TLA_SKILL_DIR/scripts/summarize_tlaps.py" proof.log --source Model.tla
```

Use the flags for your project. Newer TLAPM builds support `--strict`.
The script produces a JSON report from the Toolbox frames, the obligation count,
and the final TLAPM summary. If a later attempt proves an obligation, the script
omits that obligation from the unresolved list. For each unresolved obligation,
the report gives the last recorded attempt, even if the log ends early. The
report gives elapsed time in seconds from `time-used` in the method field.
The report uses `null` for unavailable fields.

To include theorem names, give `--source` the exact source file from the run.
The script maps names from conventional top-level theorem declarations in a
single module. The report gives any source coordinates from the Toolbox frames
and any file name from the final TLAPM summary, even without `--source`.

| Status | Evidence |
| --- | --- |
| `complete` | The final summary and Toolbox records agree that TLAPM discharged all selected obligations. |
| `proof_failure` | The final summary and Toolbox records agree. At least one final failure has a reason other than `timeout` or `internal timeout`, or has no recorded reason. |
| `timeout` | Each final unresolved attempt reports `timeout` or `internal timeout`, or the runner supplies explicit timeout evidence. |
| `memory_exhaustion` | The runner supplies explicit memory exhaustion evidence. |
| `incomplete_log` | The recorded obligation count, final summary, or complete attempt records are missing or disagree. This also covers non-Toolbox logs. |
| `incomplete_proof` | The log is complete and every backend obligation is resolved. TLAPM reported missing or omitted proof steps or an empty selected target in strict mode. |

If the runner identifies why the process stopped, save its diagnosis in a JSON
file. Set `termination` to `timeout` or `memory_exhaustion`. Copy the runner's
evidence into `evidence`. Pass the file with `--runner-status runner.json`.
If you supply a runner status file, the script uses its `termination` value
as the run status. A bare exit 137 or SIGKILL leaves the cause unknown.

```json
{"termination": "memory_exhaustion", "evidence": "Container terminated with reason OOMKilled"}
```

Exit status 0 means the script emitted a diagnostic report. Exit status 2
indicates an input or usage error. Preserve the actual TLAPM exit status
separately for the project's proof checks.

## Evaluate predicates on one TLC state

Use a compatible Java runtime and a `tla2tools.jar` that supports
`-dumpTrace tla`. Save the raw state fields without `ALIAS` projections.
The script reads the pairs in `CounterExample.state`. Each pair has a
one-based state number and a full state record. TLC must be able to load the
module and evaluate its values. If TLC puts the dump path in the module header,
the script corrects the header in its temporary copy. Console traces, JSON
dumps, and other TLA+ trace layouts produce a format error.

```sh
java -cp "$TLA_TOOLS_JAR" tlc2.TLC -config Model.cfg -dumpTrace tla Witness.tla Model
python3 "$TLA_SKILL_DIR/scripts/inspect_tlc_state.py" \
  --jar "$TLA_TOOLS_JAR" --variables x,y --constants constants.cfg \
  Witness.tla Model.tla 3 BelowLimit CanIncrement
```

List all model state variables with `--variables`. Give the names of exported
nullary Boolean predicates. For enabledness, use a state-level predicate such as
`CanIncrement == ENABLED Increment`.

If the model has constants, copy the original run's `CONSTANT` or `CONSTANTS`
declarations to a separate configuration file. Pass that file with
`--constants`. If the dump contains bare TLC model values, list their names
with `--model-values a,b`. The script searches the model's directory for imports.
Repeat `--library DIR` for each additional module directory.

The script creates a temporary TLC module and configuration. TLC evaluates the
predicates on the selected state with the supplied model and constants. The
script prints the state number, its TLA+ record, and each Boolean result.
It reports `FALSE` as a result. It exits with status 2 if the state is missing,
the fields do not match, a predicate is invalid, or TLC reports an error.
Use the saved witness and its original run as reachability evidence.

## Run the regression checks

```sh
TLA_TOOLS_JAR=/path/to/tla2tools.jar \
  python3 -B -m unittest discover -s "$TLA_SKILL_DIR/tests" -v
```

Omit `TLA_TOOLS_JAR` to run the proof-log and unsupported-format checks alone.
The [fixture notes](../tests/fixtures/README.md) describe how the inputs were captured.
See the [TLC command reference](https://github.com/tlaplus/tlaplus/blob/master/general/docs/current-tools.md)
for trace output options in the tools.
