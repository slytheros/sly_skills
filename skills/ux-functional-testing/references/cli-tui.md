# CLI and TUI interfaces

## Establish the consumer contract

MUST identify supported shells/OSes, command grammar, input sources, configuration precedence, and external effects.
MUST distinguish human and scripted consumers.
SHOULD reuse native subprocess, PTY, and project test facilities.
SHOULD apply [CLI Guidelines](https://clig.dev/) as conventions.
MUST preserve explicit product contracts when conventions differ.
MUST label convention-based concerns accordingly.

## Select and execute cases

| Area | Required checks when relevant |
|---|---|
| Discovery | Test help, subcommand help, no arguments, unknown commands/options, examples, and typo recovery. Verify documented recovery works. |
| Parsing | Test missing/repeated/conflicting options, option terminators, hyphen-prefixed values, empty strings, spaces, Unicode, and boundaries. |
| Results | Capture exit status, stdout, stderr, and resulting state separately. Verify machine output and actionable diagnostics. |
| Composition | Test pipes, redirects, empty input, early-closing consumers, and machine-readable modes. Check for corrupting prompts, colours, progress, or logs. |
| Interaction | Test TTY/non-TTY modes, EOF, defaults, invalid answers, confirmation, and cancellation. Check for inaccessible prompts and hangs. |
| Configuration | Test defaults, file/env/flag overrides, malformed configuration, explicit empty values, and working-directory changes. Verify documented precedence with conflicting values. |
| Filesystem | Test missing/readonly paths, existing outputs, overwrite refusal, unusual names, partial writes, and retries. Verify that rejection preserves protected content. Check permitted rejection effects against the contract. |
| Lifecycle | Test interruption, timeout, repetition, partial completion, and recovery. Inspect child processes, remote outcomes, and partial artifacts. |
| TUI | Test keyboard navigation, focus, shortcuts, back/escape, scrolling, resize, narrow terminals, and long text. Verify redraw and terminal restoration. |

SHOULD pass arguments as an argv array unless shell behaviour is under test.
MUST use disposable data and configuration.
MAY pass isolated directories through supported application overrides.
MUST NOT repurpose shell HOME or other system variables for test bookkeeping.
MUST bound command duration and retained output.
MUST inspect remaining processes after a timeout.
MUST reconcile uncertain state-changing outcomes before retrying.

SHOULD use a PTY for prompt and TUI checks.
MUST NOT claim interactive rendering or terminal restoration from pipe-only tests.
SHOULD test progress during actual work.
MUST label help-only checks as discovery coverage.

### Exercise preview and resume

SHOULD identify the state that a documented no-write preview promises to preserve.
SHOULD capture the relevant state before the preview.
SHOULD run the preview.
SHOULD verify the promised invariants after the preview.
SHOULD interrupt a resumable operation at a documented checkpoint in an isolated environment.
SHOULD reopen the interface.
SHOULD verify the offered next action against the persisted checkpoint.
SHOULD resume if the documented continuation permits it.
SHOULD verify the final state against the contract.
SHOULD verify that previously completed effects are preserved without duplication where required.

## Retain evidence

MUST record executable/build, relevant OS/shell, working directory, argv, inputs, configuration, TTY status, exit status/signal, and separated streams.
SHOULD retain before/after artifact evidence.
MUST remove credentials from arguments and environment records.
MAY use hashes or minimal diffs for sensitive files.
MUST provide safe reproduction commands with correct shell quoting.

## Limit claims

MUST evaluate exit codes and output against the intended consumer.
MUST check whether error output accompanies an incorrect success exit.
MUST NOT require friendly prose from a machine-readable mode.
MUST NOT infer screen-reader usability, redraw, or terminal restoration from incomplete transcripts.
MUST identify unavailable PTY and OS coverage.
