GROK2 review: **M3-E1 r5, round 2**, the syntax crate and grammar registry law. It answers your round 1 review (`reviews/grok2-syntax-e-r5/`, REQUIRED-FINDINGS: E-R5-1 to E-R5-3, with E-R5-NB-1 and E-R5-NB-2). Claude Opus 5.5 leads, and you are the single reviewer. This is a **law and contract-soundness** review of a record revision. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/grok2-syntax-e-r5-round2`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- **No run.** No product build, cargo, test, lane or verifier run. Other units may be using this machine, and the lead keeps the native lane.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- If you compute digests, counts or diffs, use read-only scratch scripts under your review directory. Read-only `git show`, `git diff` and `git log` are fine.
- No network is needed.

## Subject

- **The subject:** `docs/implementation/m3/syntax-e/PROPOSAL.md`, r5 round 2, 165,418 bytes, sha256 `3b9eae379574d037bf879ff67605232803fcf1f97641b86c860ce93d5f5fb6f0`. It is the subject of `subjectSha256`, and it stays uncommitted in arch until acceptance.
- **Diff base:** `docs/implementation/m3/syntax-e/PROPOSAL-r5-round1.md`, the bytes you reviewed in round 1 (`2c268a07…`, 161,442 bytes), committed at arch `7fc02d0a6`. Diff round 2 against it.
- **The name stays "E1 r5".** The E2a records already cite it, so the lead keeps the name (ON, "E1 r5: GROK2 raised three precise transcription findings").
- **Pins:** `hashes.txt` pins the subject, the diff base, this request, your round 1 review and the sources of every round 2 change. It pins snapshots only. The overnight log is pinned as its bytes at arch `7fc02d0a6`, not as the live file.

## What round 2 changes

The proposal's "Round 2 changes" table maps each change to its finding and source, and each changed passage is marked "(round 2)".

| Finding | Round 2 | Where |
|---|---|---|
| **E-R5-1** | The constants are each derived by E0's P6 rule from E2b's native T2a run: `base` as E0R:264 derives `fuelBase`, and `perByte` as E0R:265 derives `fuelPerByte` (the ceiling of the maximum over the non-empty files of (4 × count − `base`) ÷ bytes, rounded up to two significant figures). The sentence that gave both the base formula is gone. | item 11; r5 changes row 2 |
| **E-R5-2** | The three-field compile-model definition is gone. The T-native receipt records the crate archives and the compile models, with null toolchain fields. E2b writes it, and `buildReceiptSha256` is never null. Its field list is left to E2b's proposal and E1's next revision, alongside A8's range (lead ruling 1 below). | item 4's receipt row; item 20's E2b row and its integration gate |
| **E-R5-3** | E-12 records LD-NS8's closed set: `ref x`, `mut x` (also `ref mut x`), `x @ p`, `let mut x`, a `mut x: T` parameter, and `S { mut a }` or `S { ref a }`. Declares extraction uses the same forms. LD-NS9's disqualification for a `macro_invocation`, `attribute_item` or `inner_attribute_item` is kept. | item 14's E-12 bullet; r5 changes row 14 |
| **E-R5-NB-1** | Taken up: the level files also carry `atomicKinds` and, from SYN-NS r2, `lineTerminators`, in L1, L2 and L3. | item 14 |
| **E-R5-NB-2** | No change. | none |

The header gains a "round 2" paragraph, the draft line reads "Draft r5 (round 2)", and the lead decisions paragraph names the new ruling. Nothing else changes from round 1.

## Lead rulings (Claude Opus 5.5, on round 2)

These are lead decisions under the owner's standing direction, made on 2026-10-04. Round 2 records ruling 1, and this section is its source.

| # | Ruling | Rejected |
|---|---|---|
| 1 | **The T-native receipt's field list** is left to E2b's proposal and E1's next revision, alongside A8's range. E1 r5 records only what the call 1 ruling states: crate archives and compile models, toolchain fields null, written by E2b, with `buildReceiptSha256` never null. | A field list fixed in E1 r5, which no ruling makes (E-R5-2). |
| 2 | **Round 2 keeps the name "E1 r5"**, because the E2a records cite it. | A new revision number. |

## Decide

1. **E-R5-1.** Do item 11 and row 2 now state `base` as E0R:264 states `fuelBase`, and `perByte` as E0R:265 states `fuelPerByte`, both from E2b's native T2a run?
2. **E-R5-2.** Does item 4 record the receipt exactly as the call 1 ruling states it, with no field list? Are the field list's deferral and its gate on E2b's integration stated as ruling 1 makes them?
3. **E-R5-3.** Does item 14 record LD-NS8's closed set, `ref mut x` included, with declares extraction on the same forms and LD-NS9's disqualification kept?
4. **Scope.** Does round 2 change anything beyond these rows and the header notes?

## Output

Write REVIEW.md and review.json. review.json needs:
- "verdict": ACCEPT or REQUIRED-FINDINGS;
- "requiredFindings": each with id, location, problem or claim, evidence and fix;
- "nonBlockingObservations";
- "subjectSha256": PROPOSAL.md's sha256, as a single string.

This is a law review, not a `verify_design` unit. Do not commit.
