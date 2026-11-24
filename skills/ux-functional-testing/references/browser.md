# Browser interfaces

## Select journeys and states

MUST identify supported browsers, routes, roles, input methods, and viewport combinations.
SHOULD reuse the existing browser harness.
SHOULD select the primary journey and its highest-risk states.
MUST record viewport emulation separately from physical-device evidence.

| Area | Required checks when relevant |
|---|---|
| Navigation | Test deep links, refresh, back/forward, parameters, and unknown routes. Verify agreement between location, selection, and displayed data. |
| Forms | Test omitted, malformed, boundary, Unicode, and long inputs. Verify field errors and preserved valid input. Complete correction without restarting. |
| Submission | Test slow responses, double activation, rejection, success, and retry. Verify resulting records and duplicate prevention. |
| Sessions | Test signed-out, authorized, denied, expired, and logout states. Verify recovery and retained private content. |
| Data | Test loading, empty, populated, partial, and failed responses. Verify feedback, retry, stale data, filters, and pagination. |
| Persistence | Reload after save. Cancel edits. Navigate away from unsaved work. Verify required retention or discard. |
| Layout | Test relevant narrow/wide layouts, long text, zoom, scrolling, sticky elements, and dialogs. Verify primary actions remain reachable. |

MAY inject failures through controlled dependencies.
MUST record mocked behaviour and integration limits.
MUST NOT infer backend persistence from a mocked save.
MAY prepare fixtures through an API.
MUST exercise the UI operation under evaluation through the UI.
SHOULD use the [physical touch checks](mobile.md#exercise-physical-touch) for relevant touch-browser journeys.

## Execute and collect evidence

SHOULD use accessible roles, names, labels, or stable project test identifiers.
SHOULD wait for observable completion.
MUST NOT use a fixed sleep as the success criterion.
SHOULD isolate session and data state between cases.
SHOULD follow [Playwright best practices](https://playwright.dev/docs/best-practices).

MUST verify visible success against resulting state.
SHOULD use an independent read or reload where practical.
MUST record browser identity, viewport, route, initial state, steps, and outcome.
MAY retain relevant console/network evidence.
MUST remove secrets.
MUST connect console warnings to user impact before reporting product defects.
MUST report browser launch failures as tool/environment blockers.
MUST label markup-only assessment as static review.

## Inspect accessibility and usability

SHOULD complete selected tasks with keyboard alone.
MUST check order, visible focus, activation, dialog entry/exit, focus restoration, and traps when keyboard testing is available.
SHOULD inspect accessible names, roles, states, labels, error association, headings, announcements, contrast, and zoom.
SHOULD use an available screen reader for important dynamic interactions.
MUST NOT infer actual announcements from DOM semantics alone.
MUST record accessibility tools and evaluated states.

MUST assess next-action discoverability, loading/success feedback, error recovery, and destructive-action feedback.
MUST connect screenshot differences to task impact before reporting defects.
SHOULD control browser, viewport, operating system, fonts, and data for visual comparisons.
SHOULD apply [W3C preliminary checks](https://www.w3.org/WAI/test-evaluate/preliminary/) and relevant [WCAG 2.2 criteria](https://www.w3.org/TR/WCAG22/).
MUST map criteria only when evidence supports the mapping.

### Exercise dynamic interactions

SHOULD select checks for components in the tested journey.
SHOULD consult the applicable [ARIA Authoring Practices Guide pattern](https://www.w3.org/WAI/ARIA/apg/patterns/) for widget conventions.

- **Autocomplete.** Test keyboard selection for the applicable pattern. Test keyboard dismissal. If requests can overlap, deliver responses out of order through a controlled dependency. If the product cancels requests, verify that the cancellation works. Verify the final suggestions against the expected behaviour for the latest query. If dismissal is supported during a pending response, test it. Verify the expected popup state after the response.
- **Filtering.** Apply filters that return zero results. Check that active filters are identifiable and reachable. Clear a filter. Verify the results against the remaining selection. Include a change that restores known matches. Check reload and Back behaviour where the product defines it.
- **Form errors.** Submit invalid data with the keyboard. Check that the error is reachable from the resulting focus position. Check that the error identifies the field. Check that the error explains the correction. Correct the error. Resubmit the form. Verify that the form retains valid entries.
- **Focus and status.** Navigate within a single-page app or remove a focused item. Verify that the next keyboard action continues the task from a meaningful position. Trigger a background update during the task. Verify that focus stays usable. Record actual screen-reader announcements when available. Record unavailable screen-reader checks separately from inspected semantics.

Sources for exploratory checks include Vitaly Friedman, *Smart Interface Design Patterns Checklists* (Filtering, Autocomplete, Inline Validation), and Heydon Pickering,
*Inclusive Design Patterns* (A Registration Form) and *Inclusive Components* (A Todo List, Notifications).
See also Marcy Sutton, “Accessibility in Times of Single-Page Apps,” *Smashing Book 6*, pp. 57–69.

### Exercise background jobs

SHOULD record the job identifier or other visible correlation detail.
SHOULD reload or reopen the status view.
SHOULD verify that the view still identifies the submitted job.
MUST distinguish request acceptance from completion.
SHOULD open the result or artifact when the job reports success.
SHOULD exercise the documented next action when the job reports failure.
MUST reconcile uncertain outcomes before resubmitting a state-changing request.

## Limit claims

MUST observe action completion beyond button activation.
MUST verify saved state beyond HTTP success.
MUST distinguish pointer coverage from keyboard coverage.
MUST identify untested viewports, roles, routes, and interaction states.
MUST NOT infer human comprehension from automation success.
