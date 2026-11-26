# Inspect saved proof logs and TLC witnesses

Both scripts require Python 3.10 or later and use its standard library.
Use their output to investigate a run under the consuming project's acceptance rules.

## Summarize a TLAPM log

Save the combined stdout and stderr from one TLAPM invocation targeting one
module. Use Toolbox mode. Retain the original log, command, and exit status.
Set `TLA_SKILL_DIR` to the directory containing this skill's `SKILL.md`.

```sh
tlapm --toolbox 0 0 Model.tla > proof.log 2>&1
proof_status=$?
python3 "$TLA_SKILL_DIR/scripts/summarize_tlaps.py" proof.log --source Model.tla
```

Use the project's flags when capturing its run. For example, `--strict` is
available in newer TLAPM builds. The summarizer reads saved data and emits JSON.
It uses complete Toolbox frames, the obligation count, and the final TLAPM
obligation summary. A later successful fallback removes the obligation from the
unresolved list. Each remaining entry includes its last recorded attempt, even
when the log ends before TLAPM reports the outcome. The elapsed time comes from
`time-used` in the method field and is in seconds. Timing and other unavailable
fields are `null`.

Supply `--source` with the exact source used by the run to include theorem names
where they can be mapped. The script recognizes named theorem-family declarations
in a single module with conventional top-level declarations. Toolbox coordinates
and any file name recorded in the TLAPM summary remain available independently.

| Status | Evidence |
| --- | --- |
| `complete` | The final summary and Toolbox records agree that all selected obligations discharged. |
| `proof_failure` | The final records show unresolved failures beyond an all-timeout result. Inspect each attempt's reason, including any timeouts in a mixed result. |
| `timeout` | Each final unresolved attempt reports `timeout` or `internal timeout`, or the runner supplies explicit timeout evidence. |
| `memory_exhaustion` | The runner supplies explicit memory exhaustion evidence. |
| `incomplete_log` | The recorded obligation count, final summary, or complete attempt records are missing or disagree. This also covers non-Toolbox logs. |
| `incomplete_proof` | TLAPM emitted a strict-mode diagnostic for missing or omitted proof steps or an empty selected target, with no unresolved backend failure in the completed log. |

When the runner identifies how the process terminated, save its diagnosis in a
JSON sidecar and pass `--runner-status runner.json`. Use `timeout` or
`memory_exhaustion` for `termination` and preserve the runner's evidence.
For example, a container runner may explicitly record `OOMKilled`.
The sidecar governs the run status. A bare exit 137 or SIGKILL leaves the cause
unknown.

```json
{"termination": "memory_exhaustion", "evidence": "Container terminated with reason OOMKilled"}
```

Exit status 0 means the script emitted a diagnostic report. Exit status 2
indicates an input or usage error. Preserve the actual TLAPM exit status
separately for the project's proof checks.

## Evaluate predicates on one TLC state

Use a compatible Java and `tla2tools.jar` that can produce the saved witness.
This script supports a TLC `-dumpTrace tla` module with a
`CounterExample.state` set of pairs containing a one-based state number and
a full state record. Save the raw state fields without `ALIAS` projections.
The saved module must be loadable by TLC, with state values it can evaluate.
Console traces, JSON dumps, and other TLA+ trace layouts produce a format error.
If TLC put the dump path in the module header, the inspector normalizes that
header in its temporary copy.

```sh
java -cp "$TLA_TOOLS_JAR" tlc2.TLC -config Model.cfg -dumpTrace tla Witness.tla Model
python3 "$TLA_SKILL_DIR/scripts/inspect_tlc_state.py" \
  --jar "$TLA_TOOLS_JAR" --variables x,y --constants constants.cfg \
  Witness.tla Model.tla 3 BelowLimit CanIncrement
```

Provide all model state variable names and the names of exported nullary Boolean
predicates defined by the model. Use state-level enabledness predicates such as
`CanIncrement == ENABLED Increment`. Supply the same constant settings as the
original run in a cfg fragment containing only `CONSTANT` or `CONSTANTS`
declarations. Omit the fragment for a model without constants. If the dump
contains bare TLC model values, list those names with `--model-values a,b`
so the probe binds them as model values. The model's
directory is searched for imports. Repeat `--library DIR` for other module
directories.

The script uses TLC to bind the selected state and evaluate the predicates in
a temporary module and configuration. It prints the state number, its TLA+
record, and the Boolean results. A false predicate is a result. A missing
state, mismatched fields, invalid predicate, or TLC error exits with status 2.
The probe evaluates the selected input state under the supplied model and
constants. Reachability evidence comes from the saved witness and its original
run.

## Run the regression checks

```sh
TLA_TOOLS_JAR=/path/to/tla2tools.jar \
  python3 -B -m unittest discover -s "$TLA_SKILL_DIR/tests" -v
```

Omit `TLA_TOOLS_JAR` to run the proof-log and unsupported-format checks alone.
The [fixture notes](../tests/fixtures/README.md) describe how the inputs were captured.
See the [TLC command reference](https://github.com/tlaplus/tlaplus/blob/master/general/docs/current-tools.md)
for trace output options in the tools.
