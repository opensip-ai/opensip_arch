# Independent Grok delta review: native-wire-owner07

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-native-wire-owner-subject-07`
**Manifest SHA-256:** `fa2096e4e04c2d23d4489e9ab9aa0facdbcc9e834b67366689083b630c4996b9`
**Entries:** 209
**Parent native06:** `4c221332f213f09e2c47e9b206ce2386a246820ca2910c865a0bbc75260df539` (verdict **CHANGES REQUIRED**, unchanged)
**Verdict:** **ACCEPT WITHIN STATED REFERENCE SCOPE**

This is a delta review of the root07 wording correction against Grok native06 RF-1. It is not product acceptance, source-bridge promotion, M2/M3, or a production codec/admission/sender/generator. Native06 review files were not rewritten.

## Custody

Verified before work and at completion.

| Check | Result |
| --- | --- |
| Outer manifest | `fa2096e4…96b9`, 209/209 |
| Extra / missing / mismatch / symlinks / bytecode | none |
| Parent native06 manifest | still `4c221332…df539` |
| Changed predecessor members | exactly the 10 paths in `prior/root-correction07-receipt.json` |
| New in 07 | 65 evidence files (`prior/subject-06/**`, `prior/root-correction07-*`, `prior/root-validation07/**`) |
| Native06 review.md | still 10198 bytes, sha256 `1c4689d9…a9907`, verdict `changes-required` |

Sender, wire codec, representability, admission_ref, owner_successor, check_reference, and `check.py` are **byte-identical** to native06. Runtime algorithms were not part of this delta.

## What changed (actual bytes, not root claims)

| Path | Delta |
| --- | --- |
| `tools/rules.py` 36 | `patternDialect.standing` no longer says “the selected final owner of pattern evaluation”. It now says “a proposed reference correction, effective as selected semantics only after root acceptance and source-bridge promotion; review-03 RF-2.” |
| `wire-carriers.v1.json` 471 | Regenerated standing matches the producer (build in the copy was byte-identical to the freeze). |
| `tools/check_static.py` 526–531 | Premature-authority scan dumps **entire** `self.wire`, not `admission[].rule`. Standing map now requires the promotion sentence in `patternDialect.standing`. |
| `selftest.py` | Two new controls: `grok06_dialect_premature_authority`, `grok06_dialect_promotion_condition_missing` (151 total). |
| `contract.md` | Root07 preface added; historical author06 body kept. |

Outputs (`check-result.json`, `selftest-result.json`, `isolation-result.json`, `outcome.json`, `subject-files.json`) changed as expected from those edits.

## Native06 RF-1 disposition: **resolved in native07**

Grok06 required finding: `patternDialect.standing` called the unpromoted successor the selected final owner, and `unpromoted-successor-authority-wording` never scanned that field.

Independent evidence on 07:

- Current standing contains the promotion condition and “proposed reference correction”; the native06 forbidden regex has **no** hits in the full carrier.
- Frozen native06 standing still contains “the selected final owner of pattern evaluation”.
- Mutation restoring “The selected final owner.” to `patternDialect.standing` fails `unpromoted-successor-authority-wording` (`claims.wire-carriers.v1.json: ["selected final owner"]`).
- Mutation replacing the promotion sentence with “in force” fails with `standing.patternDialect: false`.
- Mutation putting “selected final owner” on `profiles.ts2-cbor.decodeRule` (a **non-admission** field native06 did not scan) also fails the wording check. The expanded scan is real.
- Author controls `grok06_dialect_premature_authority` and `grok06_dialect_promotion_condition_missing` both caught (2/2).

Clean `check.py` in the copy: **596/0**, **byte-identical** to frozen `check-result.json`. Wording detail now includes `"patternDialect": true`.

No new required or should-fix issue was found in this delta.

## Newly executed vs inherited

**Newly executed on 07:** `tools/build.py`; `check.py` 596/0; the two new selftest controls; eight independent delta probes (three of them full `check.py` mutations).

**Not repeated, inherited from Grok06 on unchanged algorithms:** full 149-control suite, 41-input isolation, sender payload/cancel/sequence probes, prepared-read probes, chunk-publication honesty. Those sources are byte-identical to native06; repeating them would not test this delta.

Root’s 151/151 and isolated 41-input run are recorded in the receipt. This review did not re-run full isolation or the other 149 controls.

## Native06 advisories and integration duties (kept)

These remain open as in native06; 07 did not address them and does not need to:

- Early-chunk corruption is sent; only the last chunk is content-bound. Receiver publication is an M3 duty.
- Relation v2 CanonicalPath still admits `a//b.rs`, `a/`, `a<BEL>b.rs`. Relation-registry / fact-plane duty, plus inventory joins and `admit_frame`.
- Isolation is declared-input reproduction, not confinement. Node system libraries unpinned.
- Some result JSON files are not byte-stable across reproductions; this freeze’s `check-result.json` did reproduce byte-for-byte.

**Remaining integration duties:** source-bridge promotion of pattern rows and scope; production Rust/TS matchers with ECMA `[\s\S]*` lookahead; M3 `HOST-SEND-SCHEDULE` sender; M3 host/worker `PREPARED-V3-READ-AUTHORITY`; relation-registry/fact-plane path gap and joins; generator, renderer rebase, D9 successor.

## Commands

Private copy only: `review/copy`. Python `/tmp/opensip-implementation/metadata-reference-env/bin/python -I -B`. No frozen-subject mutating checkers, agents, installs, commits, or pushes. Native06 review directory not written.

1. Manifest + 209-file verify; diff vs native06; copy
2. `tools/build.py` (carriers byte-identical to freeze)
3. `check.py` 596/0 byte-identical freeze
4. `selftest.py grok06_dialect_premature_authority grok06_dialect_promotion_condition_missing` → 2/2 caught
5. `review/probes/delta_probes.py` → 8/8
6. Completion re-hash of frozen 07 and native06 review bytes

## Limitations

- Full 151-control run and 41-input isolation were not re-executed here; 149 unchanged controls plus isolation remain Grok06 evidence. The two new controls and a clean 596/0 check were executed.
- No `admit_frame`, production sender, or regex-crate lowering.
- Reference-unit scope only.

## Verdict restated

**ACCEPT WITHIN STATED REFERENCE SCOPE.** Native06 RF-1 is actually fixed: producer standing carries the promotion condition, the wording check scans the entire published carrier, and independent mutations of the previously missed field and of a non-admission field both fail. Sender/prepared-read algorithms are unchanged. Native06 remains CHANGES REQUIRED as a historical review. This accept is not source promotion or product completion.
