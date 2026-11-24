# Workflow enforcement

## Select workflow gates

MUST identify the documented prerequisites, permitted transitions, and effects for each selected gate.
MUST identify which interfaces expose the gate.
SHOULD select representative allowed, blocked, stale, and unavailable cases.
MUST use isolated fixtures for state-changing checks.

## Compare decisions across interfaces

SHOULD exercise a shared gate through each selected interface from equivalent starting states.
SHOULD match the effective inputs, actor permissions, and build across interfaces.
MUST compare each result with the workflow contract.
SHOULD compare the meaning of decisions, blocking reasons, recovery actions, and resulting state across interfaces.
SHOULD check whether the interface explains what blocks the action.
MUST check for prohibited effects using observable state or independent evidence.
MUST report effects that could not be verified.
SHOULD verify cross-interface continuity when one interface resumes work started in another.
MUST record which interfaces were exercised.
MUST record planned but unavailable interface checks as blocked or untested.

## Verify selected inputs and authority

SHOULD record each relevant input's effective selection, identity, and selection origin.
SHOULD exercise a missing or invalid explicit selection while a valid lower-priority input exists.
MUST verify the documented selection and fallback rules.
SHOULD change one bound input after a producing stage completes.
SHOULD verify the consumer's response against the documented freshness or snapshot rules.
SHOULD check whether the diagnostic identifies the producer or input needed for recovery.

MUST identify what a successful stage permits under the workflow contract.
SHOULD exercise a successful stage that leaves a later action unauthorized, where supported.
MUST verify any required later authorization at the action that uses it.
MUST preserve existing authorization boundaries during execution.

## Reconcile interrupted publication

SHOULD record the published state before starting the attempt.
SHOULD interrupt publication at a controlled point in an isolated fixture.
SHOULD reopen each selected interface after the interruption.
MUST independently read the published state before retrying.
MUST record the resulting selection or its absence.
SHOULD verify any current selection against its complete artifact.
SHOULD verify that the workflow preserves prior attempts as documented.
MUST report uncertainty when the available evidence cannot establish the interrupted attempt's outcome.
MUST follow the documented retry rules.
MUST defer retry while the outcome is uncertain unless the contract permits a safe retry in that state.
SHOULD exercise a documented retry when permitted.

## Record evidence

MUST [record coverage](report.md#record-coverage) for each selected interface.
SHOULD link results for the same gate and fixture.
SHOULD record the stage, relevant input or attempt identifiers, and observed effects.
MUST distinguish host fixture results from integrated or target execution.
