# APIs and libraries

## Establish the consumer contract

MUST identify published contracts, supported clients/versions, examples, identity rules, data models, and side effects.
MUST apply HTTP expectations only to HTTP interfaces.
MUST include construction, invocation, errors, ownership, and cleanup for libraries.
SHOULD reuse existing clients, contract tests, and protocol tools.
MAY create temporary public-interface drivers.
MAY prepare fixtures through private methods or direct data access.
MUST test the selected operation through its public interface.

## Select functional and consumer cases

| Area | Required checks when relevant |
|---|---|
| Inputs | Test valid partitions, omissions, null/empty/absent values, malformed values, types, boundaries, Unicode, and conditional fields. Separate parsing and business validation. |
| Outcomes | Verify fields/types, errors/exceptions, protocol status/headers, diagnostics, and resulting state. Check negative cases for partial writes. |
| Identity | Test documented authorized, unauthenticated, expired, and denied cases with scoped identities. Verify that rejection preserves protected state. Check permitted rejection effects against the contract. |
| Collections | Test empty/one/many records, order, filters, page boundaries, cursor exhaustion, and documented inter-page changes. Check duplicates and omissions. |
| Repetition | Test repeated calls, uncertain completion, cancellation, and documented idempotency. Verify actual effects and operation identifiers. |
| Lifecycle | Test initialization, invalid ordering, disposal, use after close, partial failure, and recovery. Verify documented ownership. |
| Compatibility | Test supported client versions, serialization, optional/unknown fields, examples, and error handling. Verify explicit compatibility guarantees. |
| Concurrency | Test relevant competing updates and repeated activation with isolated fixtures. Check lost updates and duplicate effects. |

SHOULD use [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) for HTTP method, status, and idempotency semantics.
MUST evaluate idempotency through intended effects.
MUST NOT require identical response bytes unless the contract requires them.
MUST reconcile uncertain mutations before retrying.
MUST apply the actual contract to RPC, events, and other protocols.
MUST NOT impose undocumented tolerance, compatibility, or concurrency guarantees.
MUST NOT expand functional role checks into an unrequested penetration test.
MUST NOT expand concurrency checks into unrequested load testing.

## Execute and retain evidence

MUST use bounded timeouts and isolated data.
MUST capture call order, sanitized inputs, outputs/errors, and resulting state.
SHOULD use an independent read to verify side effects.
MUST observe documented terminal state for asynchronous operations.
MUST NOT treat acceptance as completed execution.
MUST identify fake services and in-memory substitutes.
MUST limit deployed integration claims accordingly.

MUST record build, schema/client version, environment identity, fixtures, and exact steps.
SHOULD record timing when relevant.
MUST omit tokens, cookies, private endpoints, personal data, and sensitive payloads.
SHOULD retain safe sample identifiers or reproducible redacted transcripts.

## Inspect consumer experience and limit claims

SHOULD assess examples, discovery, errors, defaults, and recovery.
MUST execute examples before claiming runtime usability.
MUST NOT infer external compatibility solely from internal code review.
MUST classify missing credentials, unreachable dependencies, and unavailable clients as coverage limits without further product-defect evidence.
