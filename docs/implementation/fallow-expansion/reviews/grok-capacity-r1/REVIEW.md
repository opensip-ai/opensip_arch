# FX-CAP-1 review

Verdict: **REQUIRED-FINDINGS**.

Subject `docs/implementation/fallow-expansion/capacity-r1/subject.json` is 2075 bytes, SHA-256 `7edc19474112ccc23d2571aef5d379e52b7b7d6cc85630785a8f0fa2d0aea47b`. All ten members match the manifest. This review does not accept the unit, does not bind it, and does not qualify a 1024-unit analysis.

The frozen subject is judged on its own terms. It raises `requestedCapabilities` to 11264, `plan.nativeContextDigests` to 1024, and both per-step notice arrays to 11264. It keeps importIds at 256, states cardinality expressibility, and selects no component capability and no S-R or S-B work. Those choices are inside the subject. They are not findings.

## What holds

Baseline product worktree `/Users/sb/code/opensip-ai/opensip-fx-design` is clean at `f5f5b4d20eca34ab2312b3ffc141c378da326afe`, branch `design/fallow-expansion`. `design-lock.json` is 526786 bytes, SHA-256 `205eee0fcecb7076107db695b351c430cbc6866d10441857719f5bdeee235c83`, with 102 contract successors and 103 inventory successors. All six parents match the successor pins:

| Parent | Bytes | SHA-256 |
|---|---:|---|
| `docs/v2/contracts/product-v1/native-evidence.md` | 329013 | `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0` |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | 135448 | `c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f` |
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | 133335 | `1ee203e3ce626d88a53d0247881cd3ffb0d52b421821ac798b9f0b57346ff6ed` |
| `docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json` | 200510 | `73645b7633d95f5d7b8e5183d789b8aab028148be0dd158e0b503a4cc3e2bd19` |
| `docs/coop/design-corrections/workflows/schemas/common.schema.json` | 55042 | `b7b25d5e7c2bf2c8d3496a2f222c31bcc87360f3e2541fbdb551136358f7d39c` |
| `docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json` | 64623 | `ce45b9ff712fa0ea4302fbdaf04cb84dfd8a3cf734f4f9677c4547672af30a8b` |

The matrix `docs/coop/design-corrections/native/native-capability-matrix.v2.json` is 36595 bytes, SHA-256 `4b1c19b03a34a271718b1e7e79335aa6f0735affd7cd36018035eeb4e7b18a14`: 11 capabilities, 6 modes, 66 cells. Requestable width is 11 for `ts-tsconfig`, `js-allowjs`, and `js-synthesized`, and 10 for `rust-cargo`, `rust-cargo-prepared`, and `syntax-only`. The three unselected cells are `clones-cross-tsjs` on the Rust and syntax-only modes. `1024 × 11 = 11264`.

Independent JSON diffs, without executing `build.py`:

- Identity candidate versus the SYN-1F parent has six differences. Two are this unit's integers (`requestedCapabilities` 1024→11264, `nativeContextDigests` 128→1024). `closureKinds.note` and `closureMembership.selectionLaw` equal CRC-2's after-text. `payloadSchemaDigest` equals HSR-1's after-text. `majorLaw` equals this unit's supersession after-text, which is HSR-1's after-text plus the third exception sentence. `$id` stays `urn:opensip:product-v1:identity:v3`.
- Each workflow candidate differs from its parent by exactly `CapabilityAvailabilityStepV1.notices.maxItems` 1024→11264.
- Preserved integers checked in the candidate identity bundle: `semanticClosures` 128, `importIds` 256. Workflow `steps.maxItems` stays 64. No protocol, handshake, byte-cap, or producer-maximum member is in the subject.

The seven prose overrides match the parent lines exactly: native-evidence.md 1115, 1117, 1119, 3534, 4276, and 4280, and workflows-and-surfaces.md 1317. Both supersessions name HSR-1's lock pin (index 101, 18546 bytes, SHA-256 `224b0037105fd7aa896e2d83425136688e38c09c6bdfb7c51225da50aeb9c61e`). Each `before` equals that record's `after`. For identity-and-evidence.md line 214, HSR-1's `before` equals I1-L's `after`. No other selected successor owns the seven prose selectors. The same-major sentence names the four numeric increases, keeps majors and digest preimages, says older readers may refuse the larger sets and never truncate or reinterpret them, and adds no historical payload reader row.

The payload registry in the identity copy names exactly eight documents: `foundation/enumeration-plan.schema.v1.json`, `foundation/evaluator-emission-plan.schema.v1.json`, `foundation/import-source-context.schema.json`, `foundation/relation-payload-schemas.v2.json`, `native/native-evidence.schemas.v2.json`, `workflows/schemas/imported-evidence.schema.json`, `workflows/schemas/policy-document.schema.json`, and `workflows/schemas/test-execution.schema.json`. The identity bundle and both common schemas are not among them, so the no-reader-row claim holds for the documents this unit changes.

`cases.json` matches the published cardinality boundaries: requestedCapabilities 1024, 1034, and 11264 continue and 11265 is `PROJECT.SCOPE_LIMIT`; nativeContextDigests 128, 129, and 1024 continue and 1025 refuses; semanticClosures stays 128/129; importIds stays 256/257; notices 11264 continue and 11265 is a schema refusal. That last split is consistent with notices not being one of the seven cardinality-first fields. Public termination, pre-Plan order, and the absence of a new detail code are restated in the rewritten native paragraphs and match the existing route.

## Required findings

### FX-CAP-1-RF-01 — Four maxItems passages are JSON numbers and cannot bind

Severity: P1.

`successor.json` passageOverrides 0–3 select:

- `/$defs/analysis-spec/properties/requestedCapabilities/maxItems` before `"1024"`, after `"11264"`
- `/$defs/plan/properties/nativeContextDigests/maxItems` before `"128"`, after `"1024"`
- `/$defs/CapabilityAvailabilityStepV1/properties/notices/maxItems` on each common schema, before `"1024"`, after `"11264"`

The pinned checker at `f5f5b4d`, `tools/verify_design.py` SHA-256 `7b313de629f2c958a1e62538b909d6f01545be2519238ba9b3d86ab7e7ba3326`, returns the decoded JSON value from `selected_passage`. Those four values are the integers 1024, 128, 1024, and 1024. `contract_successor` requires `before` and `after` to be strings and then requires the selected value to equal `before`. A string is not equal to those integers, so the record fails with `passage override before text differs from accepted parent`. Lines 401–408 also reject a line selector once the parent parses as JSON. A JSON number cannot be a contract passage under this checker.

The candidate files already hold the intended integers. The passage record is what binding checks.

Required fix: delete the four numeric overrides. Do not change `verify_design` in this unit. Keep the integers in the three candidate schema copies. Record the notice change with the string passage in FX-CAP-1-RF-02. Leave the two identity increases authorized by the `majorLaw` supersession, which already names both. Do not add another pointer whose selected value is not text.

### FX-CAP-1-RF-02 — Step notice description still states the retired 1024 bound

Severity: P2.

Both candidate common schemas, and both parents at line 1499, carry this present-tense `CapabilityAvailabilityStepV1.description`:

> `notices` is bounded at 1024 because that is the analysis-spec requestedCapabilities bound and one selection produces at most one absence per requested row, so a STEP's collection can never truncate and its noticeCount always equals its array length.

The same definition's `maxItems` is 11264. The contract says that maximum becomes 11264 so one notice per selected row is kept without truncation, and that the schema copy is the implementation input. The description and the keyword disagree. The native and workflow prose lines that state the current bound were updated; this description was not.

Required fix: override `/$defs/CapabilityAvailabilityStepV1/description` on each common-schema parent. `before` is the parent description exactly. `after` states the current bound and its analysis-spec reason as 11264, keeps one absence per requested row, keeps `noticeCount` equal to the array length, and keeps uniqueness within a step. Leave the separate historical sentence that begins "An earlier revision used one flat array bounded at 1024" unchanged. Materialize both copies so the description matches and `notices.maxItems` remains the integer 11264. That string override replaces the two numeric notice overrides removed under FX-CAP-1-RF-01.

## Non-blocking

- FX-CAP-1-NB-01. The invocation-level description, and native lines 1122–1123 and workflows lines 1318–1319, still illustrate the retired flat 1024 array and the 1023/2046 composition. `BoundedText` at 1024 is a path-text bound. Leave them.
- FX-CAP-1-NB-02. `foundation/enumeration-plan.schema.v1.json` still contrasts its own 128-item array with `plan.nativeContextDigests` maxItems 128. That document is a payload-registry row. A later description revision can correct the cross-reference and carry any reader row. This subject must not edit it.
- FX-CAP-1-NB-03. The implementation sentence "C4's 1025-capability crossing" does not name a C4 test. C2-T16 is the 129-context refusal. C4-T7 splits closures, contexts, and imports. C4-T9 is a 1025-character string and stays on the schema route. `cases.json` already has the cardinality boundaries.

## Methods and limitations

Member, parent, lock, and matrix hashes were computed independently. Every passage was compared with `selected_passage` imported from the pinned `tools/verify_design.py`. Schema copies were deep-diffed against their parents. Folded identity annotations were compared with CRC-2 and HSR-1 after-text. `build.py` was not executed. Cargo, the lane lock, binding, and both repositories were left untouched. A full baseline `verify_design` was not re-run; the passage predicate is the check this record fails.

Live architecture HEAD is `a9f6557eeb924d3163d7494e83adbd69106e41fb` (K1c inventory v145), which is outside the `f5f5b4d` lock. The six named parent byte pins still match. Untracked architecture trees, including the fallow planning package and S-OP drafts, are not members of this subject.

The synthetic spike was not treated as qualification. No performance envelope is accepted. Product handshake generation remains a separate lane: the product handshake at this pin is behind the selected RUST3-LIM copies, and this subject does not regenerate it.

`review.json` records `supersededPassages` equal to this record's two `passageSupersessions[].supersedes` values. Findings remain, so the verdict is not `ACCEPT-DESIGN-UNIT`.
