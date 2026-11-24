---
name: ux-functional-testing
description: Test software interfaces for functional behaviour, usability, and accessibility. Report reproducible findings with evidence. Use for browser, CLI/TUI, desktop, mobile, API/library, and embedded interface evaluations. Default to testing and reporting. Change products or permanent test suites only within the requested scope.
compatibility: Use available application runtimes and project, browser, terminal, API, simulator, or device tools. No single framework is required. Limit execution claims when runtimes are unavailable.
---

# UX and Functional Behaviour Testing

MUST evaluate intended tasks against the product contract.
MUST report user impact and reproducible evidence.
SHOULD use a risk-based thorough pass unless the user specifies another depth.
SHOULD reuse the project's harness and available interaction tools.
MUST NOT install a preferred framework merely to follow this skill.

## Establish the contract and execution boundary

MUST inspect project instructions, requirements, interface documentation, relevant tests, supported environments, and launch/reset commands.
MUST identify users, primary tasks, data lifecycle, dependencies, and available tools.
MUST separate explicit requirements, platform conventions, and inferred expectations.
MUST NOT use current implementation behaviour as the sole correctness criterion.
SHOULD check existing test expectations for shared implementation mistakes.

MUST resolve ambiguities that change consequential expected outcomes or authorization.
SHOULD continue independent checks while blocked.
MAY state assumptions for lesser ambiguities.
MUST qualify findings that depend on those assumptions.
MUST preserve the requested scope.

MUST default to testing and reporting.
MAY create temporary drivers, isolated fixtures, and test data.
MUST require a corresponding user request for product fixes, permanent suite changes, or CI changes.
MUST preserve existing authorization for services, accounts, and hardware.
SHOULD use disposable environments and scoped test accounts.
MUST identify external effects before sending, purchasing, deleting, or actuating.
MUST NOT treat this skill as additional access authorization.

## Select coverage and load relevant guidance

MUST record coverage using the [report reference](references/report.md).
MUST record each selected capability's expected outcome, expectation basis, risk, states/inputs, environment, method, result, and evidence.
SHOULD prioritize impact, likely use, recent changes, and failure-prone boundaries.
SHOULD select representative supported configurations.

SHOULD apply these techniques from the [ISTQB foundation syllabus](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf):

- Partition inputs into equivalence classes.
- Test boundaries and nearby invalid values.
- Test decision combinations for interacting rules.
- Test state transitions for lifecycle behaviour.
- Define exploratory tasks for uncertain areas.

MUST cover relevant success, rejection, empty/loading, failure, cancellation, recovery, and persistence paths.
MUST NOT claim exhaustive coverage from representative cases.
MUST read only the relevant platform references:

- [Browser](references/browser.md): websites and browser applications.
- [CLI and TUI](references/cli-tui.md): commands, pipelines, and terminal UIs.
- [Desktop](references/desktop.md): native windows and desktop integration.
- [Mobile](references/mobile.md): touch interfaces and mobile lifecycle.
- [APIs and libraries](references/apis-libraries.md): programmatic consumers.
- [Embedded and device interfaces](references/embedded.md): device commands,
  controls, feedback, and recovery.

SHOULD use [workflow enforcement](references/workflow-enforcement.md) when stages depend on prerequisites, selected artifacts, or explicit authorization.

MUST test important handoffs between selected interfaces.
SHOULD verify UI operations against API-visible state where applicable.
SHOULD consume CLI exports through their intended consumer.
SHOULD compare device commands with reported status.
MUST NOT infer successful handoffs from isolated component checks.

## Exercise and inspect the experience

MUST run available relevant checks within the established execution boundary.
MUST exercise representative journeys through the actual interface when accessible.
MUST observe completion and resulting state.
SHOULD verify persistence through an independent read, reload, restart, or reconnect.
MAY inspect source to diagnose issues.
MUST distinguish static review, recorded-evidence review, simulation, and fresh runtime testing.

### Exercise consequential confirmations and artifacts

SHOULD exercise stale confirmation when relevant state can change between review and submission.
MUST isolate test data before changing reviewed state.
SHOULD open the review.
SHOULD change relevant state through a separate view or session when supported.
SHOULD submit the original confirmation.
MUST compare the outcome with the documented stale-state policy when defined.
SHOULD verify the resulting state against the selected expectation basis.
SHOULD check the documented recovery path after rejection.

SHOULD check the preview when a task offers one before commitment.
SHOULD open the final artifact with its intended consumer.
SHOULD compare the artifact with the reviewed values and the documented outcome.
SHOULD independently read the related records.
MAY inject artifact-generation failure through a controlled dependency.
SHOULD verify documented rollback or recovery across the related records and artifacts.

### Control execution and collect evidence

MUST use known initial states and scoped fixtures.
SHOULD keep cases independent.
SHOULD use semantic controls and observable completion conditions.
MUST record timeouts, repeated attempts, and tool failures.
MAY control dependencies through mocks.
MUST identify material mocks and their integration limits.
SHOULD apply [Playwright's reliability principles](https://playwright.dev/docs/best-practices) through the available platform tools.

MUST inspect discoverability, feedback, terminology, consistency, user control, error prevention, and recovery in selected tasks.
MUST connect usability concerns to a concrete task, state, and user impact.
SHOULD use [Nielsen's heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) as inspection prompts.
MUST require [participant evidence](https://www.nngroup.com/articles/usability-testing-101/) for claims about actual users' comprehension, preferences, or success rates.

SHOULD combine available automated accessibility checks with relevant keyboard, focus, text scaling, zoom, and assistive-technology checks.
MUST test relevant interaction states.
MUST identify evaluated and unavailable checks.
MUST NOT claim comprehensive conformance from a clean scanner or preliminary pass.
SHOULD follow [W3C WAI's evaluation guidance](https://www.w3.org/WAI/test-evaluate/preliminary/) where applicable.
SHOULD include observed responsiveness and documented timing requirements.
MUST require a corresponding request for dedicated performance tests, security audits, formal verification, or participant recruitment.

## Investigate and report

MUST reduce suspected failures to reproducible steps where practical.
MUST check preconditions and resulting state.
SHOULD retest from a known state.
MUST preserve initial failures and attempt counts.
MUST NOT erase an intermittent failure because a later attempt succeeds.
MUST distinguish product defects, environment/tool failures, heuristic concerns, and unverified hypotheses.
SHOULD deduplicate underlying behaviours while retaining distinct user impacts.

MUST use the [report reference](references/report.md) for severity, confidence, coverage, and evidence.
MUST preserve the project's report location when defined.
Otherwise, MUST create a temporary task directory.
MUST return the report's absolute path.
SHOULD retain minimal useful screenshots, transcripts, calls, or traces.
MUST omit credentials and sensitive payloads.
MUST record the tested revision/build and relevant working changes.
MUST NOT apply old results to changed builds without verification.

MUST finish when selected coverage completes or concrete blockers prevent further useful execution.
MUST clean up only test-created resources.
MUST preserve retained evidence.
MUST report uncertain cleanup.
MUST present findings, meaningful passed coverage, blocked/untested cases, assumptions, and suggested regression coverage.
MUST NOT claim whole-product acceptance from a sample.
MUST NOT invent defects to populate a clean report.
