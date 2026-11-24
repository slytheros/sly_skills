# Desktop interfaces

## Establish the native context

MUST identify OS/version, application build, display configuration, document types, and available native tools.
MUST preserve authorized desktop surfaces and accounts.
MAY use the browser guide for webviews.
MUST evaluate native integration separately from webview content.

## Select journeys and failures

| Area | Required checks when relevant |
|---|---|
| Entry | Test launch, reopen, supported files, missing/invalid files, and additional instances. Verify the active document/window. |
| Commands | Test menus, toolbars, context menus, and shortcuts. Verify enabled states against selection and application state. |
| Focus | Test tab order, default action, Escape, dialog entry/exit, restoration, and multiple windows. Check hidden modals and blocked parents. |
| Documents | Test create/edit/save/reopen, Save As, dirty indicators, undo/redo, and unsaved close/quit. Verify Save, Discard, and Cancel independently. |
| Files | Test cancelled dialogs, invalid/unwritable destinations, extensions, and external changes. Verify selected paths and retained file contents. |
| Clipboard | Test supported formats, large content, and unusual content. Use disposable clipboard data. |
| Display | Test resizing, minimum size, scaling, long labels, and supported multi-monitor moves. Check clipping, scrolling, and restored positions. |
| Lifecycle | Test minimize/restore, close/quit, restart, interrupted work, and recovery. Verify persistence and background operations. |

MUST isolate the application before destructive lifecycle tests.
MUST NOT terminate an unidentified application instance.
MUST NOT reconfigure the user's desktop merely to obtain a preferred test setup.
MUST preserve existing authorization for installation, upgrades, and configuration changes.

## Execute and inspect accessibility

SHOULD use native tests or available UI automation.
SHOULD prefer accessible controls and OS command semantics.
MAY use coordinates when semantic interaction is unavailable.
MUST record position and scaling for coordinate-dependent reproduction.
MUST verify state after consequential actions.
MUST NOT bypass a native dialog when that dialog is under evaluation.

SHOULD check keyboard completion, visible focus, names, roles, states, selection announcements, contrast modes, and text scaling.
SHOULD use the native accessibility tree.
SHOULD use an available screen reader for important tasks.
SHOULD follow [Windows testing guidance](https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessibility-testing) or [Apple testing guidance](https://developer.apple.com/documentation/accessibility/performing-accessibility-testing-for-your-app).
MUST use tools compatible with the actual platform version.

## Retain evidence and limit claims

MUST record build, OS, scaling, active window/document, initial state, actions, and outcome.
SHOULD pair screenshots/accessibility snapshots with document or persistence checks.
MUST scope test files and commands.

MAY assess supplied recordings when native interaction is unavailable.
MUST identify historical/static evidence and its build/date.
MUST NOT claim current reproduction from historical footage.
MUST NOT infer keyboard or screen-reader success from pointer-only footage.
MUST identify untested native integration, display, and OS combinations.
MUST identify native surfaces excluded by webview-only tools.
