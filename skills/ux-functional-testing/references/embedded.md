# Embedded and device interfaces

## Establish the contract and access owner

MUST identify firmware/build, target/simulator, controls, outputs, states, deadlines, persistent settings, and recovery procedures.
MUST load relevant CLI, API, or GUI guidance for host-facing surfaces.
MUST follow established access, reservation, flashing, debugger, and acceptance workflows.
MUST preserve the runtime owner's responsibilities.
MUST NOT infer access authorization from a device address or debugger configuration.
MAY use offline evidence or simulation when hardware access is outside scope.
MUST report fidelity limits.
MUST NOT infer target, safety, or timing acceptance from interface checks alone.

## Select stateful scenarios

MUST map selected states and transitions from the documented contract.
MUST identify expected feedback and side effects.
SHOULD include invalid transitions and interrupted operations.

| Area | Required checks when relevant |
|---|---|
| Startup | Test boot, readiness, premature commands, startup failure, and retry. Verify readiness permits the intended operation. |
| Commands | Test valid, malformed, boundary, repeated, and unsupported inputs. Check acknowledgment, rejection reason, status, and actual effect. |
| States | Test idle/busy/error transitions and inappropriate commands. Compare reported state with observable operation. |
| Connectivity | Test disconnect, partial messages, reconnect, supported duplicate delivery, and resynchronization. Determine completed work before retry. |
| Timing | Test documented timeout/deadline, cancellation, missing response, and eventual completion. Record measurement method and resolution. |
| Persistence | Apply settings. Query settings. Perform authorized restart/reset. Query again. Distinguish volatile changes, commit, factory reset, and firmware replacement. |
| Recovery | Test acknowledgment, retry, authorized reset, and restored usability. Check unintended actuation and data loss against the contract. |

MUST bound each experiment.
MUST identify starting state, expected end state, and recovery action.
MUST use authorized methods for reset, power cycling, fault injection, flash writes, actuation, and timing-sensitive probes.
MUST NOT improvise fault experiments on shared or unidentified targets.

## Execute and retain evidence

SHOULD correlate stimulus, acknowledgment, completion, and observed state with sequence identifiers or timestamps.
MUST preserve framing and units in retained protocol evidence.
SHOULD use independent status, telemetry, display, or permitted measurement.
MUST distinguish issued commands from confirmed effects.
MUST record timeouts, resets, dropped observations, and probe influence.
MUST NOT infer target timing solely from host timing.

MUST record candidate identity, target class, simulator configuration or trace provenance, initial state, inputs, transitions, and resulting state.
MUST omit secret connection details and sensitive payloads.
MUST record ownership and recovery status for touched resources.

## Limit claims

MUST limit simulator results to the simulated model.
MUST NOT infer physical I/O, electrical behaviour, real boot behaviour, or hardware timing from simulation alone.
MUST bind recorded logs to their observed events and candidate.
MUST report unavailable current target execution as blocked.
MUST separate trace-supported findings from target-dependent hypotheses.
MUST NOT infer safe state from silence, missing logs, or interrupted sessions.
