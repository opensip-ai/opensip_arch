# Review: OpenSIP developer design-lock v2 (m1-successor-subject-01)

**Verdict: CHANGES-REQUIRED**, for one finding that changes tests only. No verifier change is required.

- Subject manifest SHA-256: `3fabfe4759fb6555813a05d54e9f99e5f2e8d3a7ed54a5806a5dd9f1c0ea4caa`, verified before and after (13/13 rows, no extra files, no `__pycache__`)
- Scope: `design-lock.json` v2, `tools/verify_design.py` and `tools/tests/test_design_binding.py`. These are the only files that differ from canonical-subject-04, and the Rust bytes are identical. This is not full M1, product or release approval.

## What works

- **Real verification.** `python3 -I -B tools/verify_design.py --architecture /Users/sb/code/opensip-ai/opensip_arch` passes. It verifies 46 inputs and selects `repository-file-inventory.v3.json` (`63027fb6…`) with `addedFiles: 4` and `productQualification: false`. The same result holds with a relative architecture path.
- **Tests.** All 17 Python tests pass (9 base + 8 successor).
- **Backward compatibility.** The new verifier accepts the canonical-04 lock1 with identical output. The old verifier fails closed on lock2 with "unsupported design lock". The only other verifier diff removes a redundant `"bytes" in row` guard.
- **Closed shapes.** The top-level key set depends on the version. `schemaVersion` must be an int of 1 or 2. The successor has exactly five closed `{path,sha256,bytes}` pins.
- **Authenticated pins and joins.** All five documents are length- and hash-checked before decoding. The verifier checks these joins:
  - the record against the parent and candidate, including size;
  - the review assessment against the candidate (with size), the parent (with size) and the record;
  - the assent against the review and the candidate;
  - the review and assent implementation subject digests against each other;
  - the parent against a selected lock input.
- **Adversarial probes on real evidence (59).** Each of these was refused with a meaningful diagnostic:
  - honest repins to the superseded v2 inventory, the v1 record or the canonical-02 review;
  - swapped or role-confused pins, or a different parent input;
  - traversal, missing files, a bool or float `bytes`, uppercase hashes;
  - non-ACCEPT verdicts, missing or open findings, truthy `1` assent, a changed subject digest;
  - package-edge, row-package, removal, reorder, duplicate or pendingDecisions changes;
  - zero additions, or unknown top-level keys, even when the chain is fully rebound.
- **Inherited rows.** The real 198 inherited rows, the packages and pendingDecisions are strictly JSON-type equal between v1 and v3; only `standing` differs. The four additions use declared packages and existing roles.
- **Trust model.** The checked-in lock is the trust anchor. This is a developer provenance-consistency checker, not a reviewer identity service: session IDs are not verified and there are no signatures. It also grants no runtime authorization and is not a general design-change protocol. The docstring and proposal state this accurately.
- **Proportionality.** The bounded additive profile fits selecting the already accepted v3. No additional schema or generalization is needed now; non-additive or contract successors should get their own reviewed profile.

## Required finding

### SUCC-R1-01: successor refusal tests do not isolate the guards they name

`change()` re-pins only the document it mutates, and every case asserts only a generic `DesignError`. When a record or review is mutated, the review and assent joins are left stale. If the targeted guard were deleted, a downstream join such as "root review names a different subject" would still refuse, so the test would still pass.

I tested this with mutation testing (`probes/mutants.py`). **14 of 26 guard-removal mutants survive all 17 tests.** The survivors remove these checks:

- the review `ACCEPT-UNIT` verdict, the assessment `ACCEPT` verdict, and both required-findings checks;
- the review's candidate, parent and record joins;
- the assent status;
- the record candidate size and the preservation flags;
- parent-is-selected-input;
- at-least-one addition;
- the closed binding key set when the extra key holds a valid pin.

In other words, someone could remove the proposal's core "independent ACCEPT-UNIT plus ACCEPT assessment, empty findings" requirement and every test would still pass. `probes/masking.log` shows the correct guard fires first today, so the verifier behaves correctly; only regression protection is missing.

**Fix:**
- After each mutation, rebind the downstream pins in order: record → `review.successorRecord` → `assent.actualClaudeReview`.
- Assert the diagnostic, for example with `assertRaisesRegex`.
- Add isolated cases for zero additions, a fully joined parent that is not a selected input, and an extra binding key holding a valid pin.

As a demonstration, `probes/test_design_binding_augmented.py` is a reviewer copy with 12 such tests added. It runs 29 tests, all passing on the unmodified verifier, and kills 25 of the 26 mutants. The one survivor, M02 (`candidate path != parent path`), is equivalent: the pin hash and zero-addition checks already cover that case.

## Advisories (not blocking)

- **SUCC-A1-01.** Equality uses Python `==`, so `false`→`0`, `1`→`true` and `71497.0`→`71497` pass in rebound evidence. The real data is strictly equal and the evidence is hash-pinned and reviewed, so this is defense in depth only. Comparing canonical JSON would make it type-strict.
- **SUCC-A1-02.** Added rows are not structurally validated: an undeclared package, a `../` path or missing fields would be accepted. The proposal's scope allows this and review remains the control, so no change is needed now.
- **SUCC-A1-03.** The pinned record and v3 rows still say "PROPOSED" or "acceptance pending". Ignoring that text in favour of the later pinned review and assent is correct and documented, but may confuse readers.
- **SUCC-A1-04.** The implementation subject join compares digests only; the subject manifest file itself is not pinned. That is acceptable because the review and assent are pinned.
- **SUCC-A1-05.** The pinned architecture evidence (`docs/implementation/`, inventory v1) is untracked in arch git. Verification is unaffected, but durable provenance depends on committing those bytes unchanged. The reviewer did not touch them.
- **SUCC-A1-06.** Only one successor is allowed and its parent must be a base input. A future additive inventory must therefore be cumulative over v1 with a new review chain, or use a new profile. That is fine for now.

## Executed checks and honesty notes

Logs and scripts are in `probes/`:

| Check | Log |
|---|---|
| Subject manifest, before and after | `manifest-before.log`, `manifest-after.log` |
| 17 subject tests | `unittest.log` |
| Real verification and compatibility matrix | `real-verify.log` |
| Relative path and malformed CLI input | `relative-path.log` |
| 59 adversarial probes | `adversarial.log` |
| Strict row comparison | `strict-rows.log` |
| Mutation testing (subject tests, augmented tests) | `mutants.log`, `mutants-augmented.log` |
| First-firing guard per test case | `masking.log` |
| Architecture evidence hashes and git status digest (unchanged) | `arch-*.sha256` |

Two of my own mistakes, both fixed:
- My first probe run crashed on 13 document-level cases because of a harness bug (a KeyError on mutator keys). I fixed the probe script and reran all probes.
- My first relative-path attempt used the wrong `../` depth. I corrected it and reran.

Neither mistake involved the subject.

Not rerun: Rust and crypto checks, since those bytes are unchanged. Checks ran only on macOS with Python 3.14.6. The mutation set is my own selection and is not exhaustive. I did not read the pre-existing launcher and event files in the review directory.
