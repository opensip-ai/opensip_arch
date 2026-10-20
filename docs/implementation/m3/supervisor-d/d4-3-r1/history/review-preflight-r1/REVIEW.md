# D4-3 request classifier source preflight

**Verdict: REQUIRED-FINDINGS**

**Implementation adaptations: PERMITTED**

**Subject manifest SHA-256:** `b95d08e03088a9122bf4276d28c8fcac7a655d2103cf0b996dec4572e7375cc3`

The 1,590-byte manifest and all ten declared members match their recorded sizes and SHA-256 digests. `PLAN-r1.md` and accepted `PLAN-r2.md` are byte-identical to the architecture authorities. The frozen base invocation, test, and outcome sources are byte-identical to product commit `3c02526e5fc6e3de83eec8abf04ecdb669a6ca11`, and the frozen product diff applies cleanly to that base. The candidate changes only `crates/host/src/invocation.rs` and its existing test module.

## Adaptation rulings

### LD-D4-3-I1 — PERMITTED

Using `outcomes::RequestExcludedClass` is the faithful request-domain interpretation of the plan's `Option<ExcludedForm>`. Its closed variants are exactly EE-2, EE-4's request part, and EE-6a, and the existing `Observation::ExcludedRequest` and row-57 projection already consume that type. `components::manifest::ExcludedForm` carries manifest digest and manifest-class data and cannot represent item 25 without inventing a request or a cast. I1 introduces no type, carrier, outcome, or authority and does not alter D4-1.

### LD-D4-3-I2 — PERMITTED

Calling the classifier inside the sole `AdmittedRequest::admit` constructor after successful step-list validation and typed construction, before returning the opaque token, preserves the accepted plan's ordering. It strengthens enforcement at the existing boundary without moving classification before validation or adding an effect. The constructor performs no request-ID draw, durable entry, filesystem, ledger, or custody operation. A future non-`None` result takes the existing `Observation::ExcludedRequest` route, and `Vec::new()` itself allocates no heap storage.

The classifier's closed destructures cover every `AdmittedRequest` field, all five `RequestFlags` fields, the mode field, and the sole JSON format. Its request match has no wildcard and returns `None` for `Default`, `Analyze`, and `AnalyzeEphemeral`. The focused value control covers all three requests, both interactive values, and all 32 presence/boolean combinations of the flags. No excluded request representation is added, so D4-T2 remains unrepresentable and row 57 remains unreachable from the M3 request admission path.

## Required findings

### D4-3-PRE-R1-RF-1 — The sole-constructor pin does not detect `Self` struct expressions

`candidate-invocation_tests.rs:1092` claims to preserve the only construction-to-classification-to-handover path by asserting that `source.matches("AdmittedRequest {").count()` is three. Those three matches are the struct declaration, `impl AdmittedRequest`, and the classifier destructure. The actual construction at `candidate-invocation.rs:121` is `Self { ... }` and is not counted.

Consequently, another associated function in the same private-field module can return a fresh `Self { ... }` without calling `request_excluded_form`; the asserted count remains three, the existing admission ordering check still passes, and an unclassified opaque token can be handed out. Private fields prevent construction from sibling modules, but they do not prevent this same-module bypass. This fails LD-D4-7's required call-order pin over the one constructor.

Add a control that accounts for every `AdmittedRequest` construction expression, including `Self { ... }`, and proves that each fresh construction is followed by classification before any return or handover. A construction API that makes the classified state structural is also acceptable. Retain the current exhaustive request/field/mode/format pins.

## Non-blocking observations

### D4-3-PRE-R1-NBO-1 — Final evidence remains outstanding

This review covers source shape only. The complete base and candidate component/host suites, owning checks, runtime-caught wildcard and ordering mutations, final unit review, integration, and any later inventory treatment remain pending. Existing outcome projection tests for row 57 do not make that row reachable from an M3 request.

No tests, builds, cargo commands, lanes, network access, private data access, other panes, delegation, or repository changes were used during this review.
