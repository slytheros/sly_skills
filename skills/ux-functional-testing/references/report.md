# Coverage and findings report

MUST preserve the consuming project's report format and location when defined.
Otherwise, MUST create a fresh temporary task directory.
MUST return the report's absolute path and key findings.
SHOULD link raw evidence instead of copying full logs.
MUST omit secrets and sensitive payloads.

## Record scope and identity

MUST record the requested task, users/consumers, primary journeys, revision/build, relevant working changes, date, and environment.
SHOULD record tool versions that affect reproduction.
MUST identify material mocks, safe account aliases, fixtures, and reset methods.
MUST identify historical evidence by provenance, build, and date.
MUST distinguish fresh runtime, recorded, simulated, and static evidence.
MUST state unknown build identity.
MUST NOT silently bind an unknown application build to checkout HEAD.

MUST record assumptions and material ambiguities.
MUST classify expectation bases as requirement, documented contract, convention, or inference.
MUST NOT present a heuristic concern as a proven contract breach without supporting evidence.

## Record coverage

MUST use the project's coverage format when defined.
Otherwise, MUST use the matrix below.
SHOULD add a companion record if the project format lacks required fields and the requested scope permits it.
MUST identify any required fields that remain unrecorded.

| ID | Journey/capability | Expected outcome and basis | Risk | States/inputs | Environment and method | Result | Evidence |
|---|---|---|---|---|---|---|---|

MUST use these result meanings:

| Result | Acceptance criterion |
|---|---|
| Passed | Observe the expected outcome for the selected check. |
| Failed | Observe a mismatch. Link a finding. |
| Blocked | Identify the dependency, permission, runtime, or tool that prevented completion. State any completed assessment. |
| Untested | Identify the selected case without execution/evidence. Explain the gap. |

MUST label recorded/static review methods explicitly.
MUST limit recorded passes to their recorded context.
MUST NOT report a current runtime pass from recorded evidence.
MAY omit irrelevant combinations with a rationale.
MUST NOT mark omitted cases as passed.
MUST summarize gaps and residual risks.
MUST NOT calculate whole-product success rates from selected cases.

## Record findings

MUST include these fields for each actionable finding:

- Identify the finding and classification.
- Describe affected users, impaired tasks, consequences, and workarounds.
- Assign impact-based severity.
- State confidence and evidential uncertainty.
- Record build/environment, role, fixtures, and starting state.
- Provide minimal reproduction steps or a safe command/call sequence.
- Compare expected and actual outcomes.
- Cite the expectation basis.
- Include resulting state and unintended effects.
- Link supporting evidence.
- Record attempt counts for intermittent results.
- Suggest regression behaviour and assertions.

MUST classify findings as functional defects, accessibility barriers, heuristic concerns, environment/tool issues, or unverified hypotheses.
MUST distinguish confirmed observations, intermittent observations, and hypotheses.
MUST state uncertainty about causes, expectations, and reproduction.

MUST use project severity definitions when available.
Otherwise, SHOULD apply these defaults:

| Severity | Impact criterion |
|---|---|
| Critical | Severe irreversible harm, substantial data loss, or broadly unusable essential operation without a practical workaround. |
| High | Blocked core tasks, materially wrong results, or excluded user groups without a practical workaround. |
| Medium | Impaired or error-prone tasks with a reasonable workaround or narrower impact. |
| Low | Limited friction or presentation/consistency issues with little effect on task completion. |

MUST keep severity, confidence, and scheduling priority separate.
MUST NOT downgrade observed impact solely because occurrence is intermittent.
MUST NOT present severe hypotheses as confirmed defects.
MUST treat implementation suggestions as proposals unless fixes were requested.

## Record completion and limitations

MUST summarize prioritized findings and meaningful passed checks.
MUST identify blocked/untested cases, unavailable environments/tools, mock limits, and unresolved expectations.
MUST state when no actionable findings occurred within the evaluated scope.
MUST NOT invent defects from personal preferences.

MUST report test-resource cleanup and uncertain external completion.
SHOULD recommend the smallest useful follow-up for important gaps.
MUST separate suggested fixes, regression additions, and CI changes from completed work.
MUST NOT claim user-study results, accessibility certification, exhaustive quality, or release acceptance from this report alone.
