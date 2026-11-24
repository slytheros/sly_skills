# Mobile interfaces

## Establish device coverage

MUST identify supported OS versions, device classes, app build, accounts, dependencies, and available runtimes.
SHOULD reuse existing native or cross-platform tests.
MUST distinguish host tests, simulators/emulators, and physical devices.
MUST record each check's execution environment.
SHOULD consult [Android testing fundamentals](https://developer.android.com/training/testing/fundamentals) for host and instrumented testing distinctions.

## Select journeys and transitions

| Area | Required checks when relevant |
|---|---|
| Navigation | Test primary tasks, back/up, supported swipe navigation, deep links, and repeat entry. Verify destinations and retained/discarded state. |
| Input | Test touch targets, gestures, scrolling, selection, validation, autofill, and keyboard submission/dismissal. Check keyboard and safe-area obstruction. |
| Layout | Test supported rotations, small screens, large text, long content, insets, and scrolling. Verify task state through view recreation. |
| Permissions | Test first request, denial, grant, revocation, and supported reduced scope. Verify explanation, fallback, and recovery. |
| Lifecycle | Test background/foreground, lock, interruption, recreation, relaunch, and supported process-death recovery. Inspect drafts, pending work, duplicates, and sessions. |
| Connectivity | Test offline start, slow/failed requests, interrupted submission, reconnect, and stale caches. Verify sync and documented conflict handling. |
| Persistence | Create/edit data. Reopen the app. Inspect saved state. Verify cancellation leaves intended data unchanged. |

MUST use scoped fixtures and test accounts.
MUST distinguish logout, data clearing, reinstall, and process termination as different preconditions.
MUST NOT clear unrelated application data.
MUST NOT send real messages or notifications solely to simulate interruption.
SHOULD use available test controls.
MUST record simulation limits.

## Inspect accessibility and usability

SHOULD inspect names, roles, states, reading/focus order, errors, announcements, touch alternatives, and supported text scaling.
SHOULD run available TalkBack or VoiceOver journeys.
MUST NOT infer spoken feedback or gesture usability from hierarchy inspection alone.
SHOULD follow [Android accessibility testing](https://developer.android.com/guide/topics/ui/accessibility/testing) or [Apple accessibility testing](https://developer.apple.com/documentation/accessibility/performing-accessibility-testing-for-your-app).

MUST assess gesture discovery, accidental-action recovery, permission explanations, and interruption recovery within selected tasks.
MUST connect concerns to observed task friction.
MUST require suitable participant evidence for human comprehension or one-handed comfort claims.

### Exercise physical touch

SHOULD select checks for relevant controls and gestures on a supported physical device.

- **Adjacent controls.** Tap near the edge of a critical target. Repeat next to a neighbouring control. Start a scroll over a tappable row. Record the action for each gesture. Check whether the finger obscures essential activation feedback.
- **Accidental activation.** Use disposable data. Try rapid repeat taps or a slipped drag. Verify the resulting state. Check whether a second tap at the same position can unintentionally confirm a consequential action. Exercise documented cancellation or undo.
- **Screen edges.** Exercise important edge controls with supported system navigation or browser controls active. Verify access to the app action. Verify that system navigation behaves as documented.

MUST record the gesture, screen region, attempt count, and resulting state.
SHOULD record the system navigation mode and browser controls when relevant.
MUST use applicable platform criteria and the product contract for acceptance thresholds.

The exploratory checks draw on Steven Hoober’s *Touch Design for Mobile Interfaces*, pp. 201–208 and 378–380.

## Retain evidence and limit claims

MUST record OS/build, device model, viewport/density, orientation, font scale, permissions, connectivity, and lifecycle sequence.
SHOULD pair screenshots/video with logs and independent state reads.
MUST distinguish simulated transitions from actual device transitions.

MUST NOT treat browser viewport emulation as native mobile testing.
MUST NOT infer physical touch, vendor lifecycle, hardware integration, or assistive output from host tests alone.
MAY assess supplied recordings when runtime access is unavailable.
MUST identify recording provenance and build/date.
MUST report current execution as blocked when its runtime is unavailable.
MUST NOT extrapolate recorded success to untested devices.
