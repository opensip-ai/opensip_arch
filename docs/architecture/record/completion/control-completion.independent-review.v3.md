# Independent control completion review v3

**OBJECT — one refusal-precedence defect remains.** External replay is **448/448 PASS**, byte-identical to the retained report. All eight subject hashes matched before and after inspection; no subject or register file changed.

Freeze SHA-256: `47e033370a633fe6bad5ffd2399fb9438a6384f4764d833cdf93c5eced08c8c9`. Exact subject/source hashes, complete independent probe bytes and reproducer are retained in [the review JSON](control-completion.independent-review.v3.json).

## CCR-1 — sequence faults bypass structural RF-2 precedence

The completed contract requires other simultaneous structural faults to win RF-2. The parser returns RF-7 immediately for zero/overflow/large sequence values, before checking all other structure. Independent probes show RF-7 for `seq=0` with an unknown body field, an oversized sequence with `body=[]`, a large sequence with string-valued `controlMajor`, and `seq=0` with an unknown type.

This is a deterministic classification defect; both outcomes remain terminal. Standalone zero/overflow sequence values correctly remain RF-7.

**Required repair:** Record the sequence range fault while validating all remaining applicable structure. For a supported-major message, validate known type/body with only the invalid seq substituted by a valid validation sentinel, then select RF2 if any other structure fails, otherwise RF7 for sequence. For unsupported-major hello, inspect only frozen envelope constraints, preserving opaque future body handling and integer-lexeme resource safety. Do not convert arbitrarily large seq text to int. Add the compound-invalid cases alongside standalone zero/overflow positives.

## Scope and positive evidence

The iterative parser repair survives the retained deep/large-input cases. Independent malformed-comma, escaped duplicate-key, and known-string surrogate probes correctly refuse RF-2. The 256-cell matrix, actual preview handshake, pinned active-corpus selector, 212 replacement references and 9768 active-case arithmetic were independently checked. RF5 has an explicit closed-preview argument without a semantic Boolean oracle.

SHOULD: add a stateful two-direction FAULTED teardown witness; single-frame matrix contexts do not prove a stopped direction stays stopped. Security/journal activation and successor adoption remain separate explicit dependencies, not added review defects.

No product qualification, acceptance/SATISFIED status, or register change is asserted.
