# FX-CAP-1 review, round 2

Verdict: **ACCEPT-DESIGN-UNIT**.

Subject `docs/implementation/fallow-expansion/capacity-r2/subject.json` is 2075 bytes, SHA-256 `2148a4824286f0046fef02e070e3b0fe51c19a34fc6bd191820c6d3bf04e557d`. All ten members match. `requiredFindings` is empty. `supersededPassages` equals this record's two `passageSupersessions[].supersedes` values. The unit was not bound. This is not a performance qualification and not a claim that product schema sources have changed.

Round 1 (`docs/implementation/fallow-expansion/reviews/grok-capacity-r1/review.json`, subject `7edc19474112ccc23d2571aef5d379e52b7b7d6cc85630785a8f0fa2d0aea47b`) was REQUIRED-FINDINGS. Both required findings are closed, and the named non-blocking test route is addressed.

## Closure of round 1

**FX-CAP-1-RF-01 is closed.** The successor has nine passage overrides and no `maxItems` JSON Pointer. Every override `before` and `after` is a string. The pinned `selected_passage` returns that same string for each one. The four numeric keywords remain integers in the schema copies: `requestedCapabilities` 11264, `plan.nativeContextDigests` 1024, and both `CapabilityAvailabilityStepV1.notices` 11264. Native-evidence.md line 4276 names the three complete copies under `docs/implementation/fallow-expansion/capacity-r2/` and says the numeric maxima are selected through those copies, not through text-value JSON Pointer overrides. The `majorLaw` supersession names the same four increases.

**FX-CAP-1-RF-02 is closed.** Both common-schema parents have a text override of `/$defs/CapabilityAvailabilityStepV1/description`. `before` is the parent sentence that stated the 1024 bound. `after` states the bound as 11264 because that is the analysis-spec bound, keeps one absence per requested row, keeps `noticeCount` equal to the array length, and keeps uniqueness within a step. Each candidate description equals that `after`, and each `notices.maxItems` is the integer 11264. The present-tense "bounded at 1024 because that is the analysis-spec" sentence is gone from both copies. `CapabilityAvailabilityV1.description`, the historical flat-array sentence, is byte-identical to its parent in both copies.

**FX-CAP-1-NB-03 is addressed.** `CONTRACT.md` names C2-T16 for the 129-context test, moves the published capability cardinality one-over to 11265, and keeps C4-T9 as the 1025-character malformed-string schema refusal. The phrase "1025-capability crossing" is gone. C4-T7 still keeps closure and import crossings at 129 and 257.

## What was checked

Product worktree `/Users/sb/code/opensip-ai/opensip-fx-design` is clean at `f5f5b4d20eca34ab2312b3ffc141c378da326afe`. `design-lock.json` is 526786 bytes, SHA-256 `205eee0fcecb7076107db695b351c430cbc6866d10441857719f5bdeee235c83`: 102 contract successors and 103 inventory successors. Parents and candidates are sorted. The nine candidate pins equal the subject members other than `successor.json`. All six parent byte pins match.

| Parent | Bytes | SHA-256 |
|---|---:|---|
| `docs/coop/design-corrections/workflows/schemas/common.schema.json` | 55042 | `b7b25d5e7c2bf2c8d3496a2f222c31bcc87360f3e2541fbdb551136358f7d39c` |
| `docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json` | 64623 | `ce45b9ff712fa0ea4302fbdaf04cb84dfd8a3cf734f4f9677c4547672af30a8b` |
| `docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json` | 200510 | `73645b7633d95f5d7b8e5183d789b8aab028148be0dd158e0b503a4cc3e2bd19` |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | 135448 | `c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f` |
| `docs/v2/contracts/product-v1/native-evidence.md` | 329013 | `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0` |
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | 133335 | `1ee203e3ce626d88a53d0247881cd3ffb0d52b421821ac798b9f0b57346ff6ed` |

The seven prose overrides match their parent lines: native-evidence.md 1115, 1117, 1119, 3534, 4276, and 4280, and workflows-and-surfaces.md 1317. Both supersessions name HSR-1 at lock index 101 (18546 bytes, SHA-256 `224b0037105fd7aa896e2d83425136688e38c09c6bdfb7c51225da50aeb9c61e`). Each `before` equals that record's `after`, and each `after` only appends the third exception sentence. For identity-and-evidence.md line 214, HSR-1's `before` equals I1-L's `after`. No other selected successor owns these selectors except that ancestor chain.

Independent diffs, without executing `build.py`:

- The identity candidate is 202676 bytes, SHA-256 `b3ffd2fe4f535695f291b45eaeeb27f5585e4d20dca8f09f0e8b33d6ee27c3f2`. Against the SYN-1F parent it has six differences: the two FX-CAP-1 integers, CRC-2's `closureKinds.note` and `closureMembership.selectionLaw`, HSR-1's `payloadSchemaDigest`, and this unit's `majorLaw`. `$id` stays `urn:opensip:product-v1:identity:v3`. `semanticClosures` stays 128 and `importIds` stays 256.
- Each workflow candidate differs from its parent by exactly `notices.maxItems` and `CapabilityAvailabilityStepV1.description`. `steps.maxItems` stays 64.
- The payload registry still names exactly eight documents. The identity bundle and both common schemas are not among them.
- The matrix is unchanged: 36595 bytes, SHA-256 `4b1c19b03a34a271718b1e7e79335aa6f0735affd7cd36018035eeb4e7b18a14`, widest requestable width 11. `1024 × 11 = 11264`.
- `cases.json` is unchanged, SHA-256 `d9c37523094eedab3f4063d934f338c22185557db74db517d61f9e28d0349005`: requestedCapabilities 1024, 1034, and 11264 continue and 11265 is `PROJECT.SCOPE_LIMIT`; contexts 128, 129, and 1024 continue and 1025 refuses; closures stay 128/129; importIds stay 256/257; notices 11264 continue and 11265 is a schema refusal.

Line 4276 keeps the public termination, the seven-field family, cardinality-before-shape, the prospective-Plan order `semanticClosures`, `nativeContextDigests`, `importIds`, and the rule that a non-array is a schema shape. It sets `requestedCapabilities` to 11264 and `nativeContextDigests` to 1024, leaves `importIds` at 256 and `semanticClosures` at 128, and states that fitting the cardinality bound does not guarantee every 1024-unit input fits the unchanged byte, frame, stage, dependency, and work bounds. Line 4280 selects only the two identity maxima and both notice maxima. No protocol or handshake member is in the subject.

## Non-blocking

- FX-CAP-1-NB-04. Both step descriptions spell `at11264` without a space. The number is 11264. Not required.
- FX-CAP-1-NB-02 remains queued. The enumeration-plan cross-reference to `plan.nativeContextDigests` maxItems 128 stays outside this subject because that document is a payload-registry row.

The diagnostic cell at native line 3534 says the other bounded-selection fields keep their own limits, meaning they do not become 11264. Line 4276 is the sentence that sets `nativeContextDigests` to 1024. Those readings agree.

## Methods and limitations

Member, parent, lock, matrix, and schema hashes were computed independently. Every passage was compared with `selected_passage` from the pinned `tools/verify_design.py` (SHA-256 `7b313de629f2c958a1e62538b909d6f01545be2519238ba9b3d86ab7e7ba3326`). Schema copies were deep-diffed against their parents. Folded annotations were compared with CRC-2 and HSR-1 after-text. `build.py` was not executed. A full baseline `verify_design` was not re-run. Cargo, the lane lock, binding, and both repositories were left untouched.

Live architecture HEAD is `a9f6557eeb924d3163d7494e83adbd69106e41fb`, outside the `f5f5b4d` lock. The six named parent pins still match. The synthetic spike is sizing evidence only.
