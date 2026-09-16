# Independent Grok review: native-wire-owner06

**Reviewer:** Grok (explicitly authorized). Codex remains implementation lead. This is not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-native-wire-owner-subject-06`
**Outer manifest SHA-256:** `4c221332f213f09e2c47e9b206ce2386a246820ca2910c865a0bbc75260df539`
**Entries:** 144
**Verdict:** **CHANGES REQUIRED**

Author06 was partial actual-Claude work interrupted by quota. Root completed the reference runs. This review reproduced those runs in a private copy and then ran independent counterexamples. Passing author/root tests is not acceptance. This is not product, M2/M3, production codec/admission/sender/generator, source-bridge promotion, or platform qualification.

## Custody (before and after)

Verified before work and again at completion. Frozen subject bytes were not written.

| Check | Before | After |
| --- | --- | --- |
| Manifest | `4c221332…df539` | same |
| Files | 144 listed = 144 walk, 0 extra/missing/mismatch | same |
| Symlinks / bytecode | none | none |
| Architecture pins | 44/44 | 44/44 |
| Node 24.16.0 | `1ee75375…c4b8` / 120573328 | same |
| Modes/symlinks in manifest | not listed; walk has no symlinks | same |

Evidence: `review/results/custody-before.json`, `review/results/custody-after.json`. Product and architecture trees were not edited. Failed root-check-01 controls and the author06 quota harness remain under `prior/`.

## Isolation

`tools/isolation.py` ran only from `review/copy` (documented `env -i`, `-I -B`, copy-local `TMPDIR`/`PYTHONPYCACHEPREFIX`, `SELFTEST_WORKERS=4`). It copied **41** `filelist.INPUTS` and did **not** copy `subject-files.json`.

| Isolation | Result |
| --- | --- |
| Check | 596/0, same ids and outcomes as primary |
| Selftest | 149/149 caught, no baseline failures |
| `pass` | true |

Primary `check.py` in the copy was already **596/0** and **byte-identical** to frozen `check-result.json` (`75724a7e…96e7`, 117120 bytes). Primary `selftest.py` was **149/149**, `allCaught: true`, `baselineFailures: []` (JSON bytes differ slightly from freeze; names and caught flags match). Isolation was not rerun after this resume.

## Authorship (do not conflate)

- **Author06 (actual Claude, partial):** quota harness preserved (`prior/author06-quota-harness/final-response.md`, 75 bytes). Did not produce the frozen 596/149/isolation results.
- **Root:** `prior/root-continuation-06/receipt.json` records 596 checks, 149/149, `rootSelftestExecuted: true`, `rootIsolationExecuted: true`. Initial root-check-01 (595 checks, 4 failures) is preserved. Root-04/05 remain 478 and 567 checks with `rootSelftestExecuted: false`.
- **This review (Grok):** independent. Coverage-binding02 is out of scope; no delta approval.

## Probe attempts: harness failures vs detected defects vs passing controls

Classification: `review/results/probe-assessment.json`.

**Attempt 1 (preserved, incomplete).** `review/results/independent-probes-attempt01.stdout` and `independent-probes.exc`. Seven sender/read assertions printed FAIL, then the script crashed on a sloppy pin-count parse (`TypeError: json.loads` of a `list`). Those FAILs compared `str(Refuse)` (which appends `:slot N`) to `Refuse.code`, and compared `len(read_text())` to a 75-byte file. **They are harness bugs, not subject defects.** The sender had already refused the expected codes. This attempt is kept; it is not a required finding.

**Attempt 2 (complete).** `review/results/independent-probes.json`, 33/33 harness assertions passed after using `Refuse.code`.

**Detected subject defect (not a passing product control).** These attempt-2 probes are written to PASS when the defect is present:

- `pattern-dialect-standing-still-says-selected-final-owner`
- `rf2-wording-check-misses-pattern-dialect-standing`
- `contract-claims-check-covers-carrier-rules`

**Passing subject behaviour (independent controls, not acceptance):** payload-digest refusal of same-length OpenUniverse substitution; typed Cancel `False` vs `0`; integer sequence; last-chunk content bind; prepared-read of ok rows only; failed-row unreadability; 149 declared selftest keys; preservation of root-check-01 failures.

## Review-05 items

### RF-1 sender binding — independently closed

`tools/sender_ref.py` `consume` compares `type(sequence) is int`, slot identity, payload bytes, and `payloadSha256` before sent state. Cancel echo is deterministic-CBOR equality of consumed correlation.

Independent synthetic plan (attempt 2):

| Attack | Result |
| --- | --- |
| Same-length OpenUniverse `executionId` | `payload-digest`, `framesSent=1`, correlation still null |
| Same substitution then planned Cancel | still `payload-digest` at that slot |
| Cancel `analysisOrdinal=False` vs `0` | `cancel-echo`; CBOR `\xf4` ≠ `\x00` |
| Sequence `False` | `sequence` at frame 0 |
| Float `0.0` ordinal | codec `UNENCODABLE` (encode/measure before echo) |
| First-chunk byte flip, two-chunk entry | last chunk `chunk-content`, `framesSent=1` (earlier corrupt chunk already sent; contracted) |
| Last-chunk byte flip | `chunk-content` before that frame is sent |

Frozen HOST-SEND-SCHEDULE vectors and `review05-sender-attacks-replayed` agree via the 596/0 check. Attempt-1 FAIL lines on these attacks were harness string compares, not acceptances.

### RF-2 wording — **not closed** (required finding below)

`OWNER-PATTERN-EVALUATION` uses “proposed reference owner correction” plus the promotion condition. Root attribution matches the 04/05 receipts. A mirrored “selected final owner” claim remains in `patternDialect.standing`.

### A-1 — closed as framed; gap recorded

fact-plane v1 `CanonicalPath` has no control-scalar clause. identity-model.v3 `registered_payload` does not call `_is_path`. Relation v2 still admits `a//b.rs`, `a/`, `a<BEL>b.rs`. Declared other-unit duty.

### A-2 — independently closed in this reference

`prepared_read_authority`: ok readable; failed `PREPARED_ROW_NOT_READABLE`; unknown ordinal refused. Defaulted partial-stale sets are not selected. Worker PO-1 context is not carried. M3 implementation remains future work.

### A-3 — retained

Defaulted 257 rows / 1 stale: fallback, 0 usable, disclosure `entries`.

### A-4 — pins and trust boundary

44 pins and Node bytes verified before and after. System libraries unpinned and named. Isolation is 41-input reproduction, not confinement.

## Required finding

### RF-1 — `patternDialect.standing` still names the unpromoted successor “the selected final owner”

- **File/line:** `wire-carriers.v1.json` 471 (from `tools/rules.py` 36). Scan hole: `tools/check_static.py` 521–532. Contract claim: `contract.md` 103.
- **Trigger:** Review-05 RF-2 forbade calling `owner-pattern-successor.v1.json` the selected/final owner while it is an in-memory author candidate.
- **Reproducer:** `review/probes/independent_probes.py` detection probes. Author-check regex over `admission[].rule` + successor docs + contract: no hits. Same regex over the whole carrier: `selected final owner`.
- **Observed:** standing text says schemaPatternRows are “the selected final owner of pattern evaluation, review-03 RF-2.” Frozen `unpromoted-successor-authority-wording` is `ok: true`, `"claims": {}`.
- **Expected:** no published carrier field asserts selected/final/approved/authoritative owner status for an unpromoted successor, or the check/contract must not claim that coverage. Use the same proposed-correction + promotion-condition language as `OWNER-PATTERN-EVALUATION`.
- **Reason:** mirrored RF-2 claim in the carrier consumers read. The wording check never dumps `patternDialect`. Control `rf2_selected_owner_wording_restored` only rewrites the admission rule. Root-check-01’s wording failure was other strings (`authoritative owner` / `selectedOwner`); fixing those greened the check without seeing this phrase. **596/0 does not close RF-2.**

## Advisories

- Early-chunk corruption is sent; only the last chunk is content-bound. Receiver publication is an M3 duty.
- Relation v2 CanonicalPath path-normalization gap remains a recorded other-unit duty.
- Isolation is not general confinement; Node system libraries stay unpinned.
- `selftest-result.json` / `isolation-result.json` / `outcome.json` are not always byte-stable; semantic pass/fail matched. Frozen `check-result.json` did reproduce byte-for-byte.

## Remaining integration duties (not defects of this unit)

Source-bridge promotion; production Rust/TS matchers with ECMA `[\s\S]*` lookahead; M3 `HOST-SEND-SCHEDULE` sender; M3 `PREPARED-V3-READ-AUTHORITY`; relation-registry/fact-plane CanonicalPath gap, inventory joins, and `admit_frame`; generator, renderer rebase, D9 successor.

## Independently accepted vs not

**Accepted as reference behaviour after the wording fix:** encoded payload/cancel/sequence binding; prepared-read of ok rows only; 149 mutation controls; 41-input isolation; 44 pins + Node bytes; A-1 framing with the path gap recorded elsewhere.

**Not accepted:** RF-2 authority-wording closure; product/M3/source promotion; production codec, admission, sender, generator.

## Commands (not rerun on this resume except freeze re-hash)

Private copy only. Python `-I -B`. No frozen-subject mutating checkers, network, commits, pushes, or agents.

1. Manifest/pin/Node verification
2. Copy 144 files → `review/copy`
3. Independent probes attempt 1 (harness FAILs + crash; preserved)
4. Independent probes attempt 2 (33/33)
5. `tools/build.py`, `tools/vectors.py` (generated carriers byte-identical to freeze)
6. `check.py` 596/0 byte-identical freeze
7. `selftest.py` 149/149
8. `tools/isolation.py` pass
9. Completion freeze re-hash (match)

## Verdict restated

**CHANGES REQUIRED.** Isolation, 149/149 selftest, 596/0 check, and RF-1/A-2 independent counterexamples hold. Attempt-1 probe FAILs were harness mistakes and are preserved as such. The remaining blocker is RF-2: `patternDialect.standing` still calls the unpromoted successor the selected final owner, and the wording check never looks there. Fix that standing text and scan the whole carrier (or stop claiming the check covers carrier rules). This is not product completion.
