# Coverage prerequisite subject01: separate narrow verdict

This is a **resumed** independent review in the same Claude session as the report asset reviews. It is not a fresh session. No subagents, background tasks, commits, pushes or private session inspection were used. It is reported separately from the assembly verdict, and root acceptance is independent.

## Verdict

**Acceptable for root's independent acceptance as a narrow bookkeeping correction. No required issues and no defects.**

The successor adds exactly `moduleFirstMilestone["crates/reporting/src/assets.rs"] = "M1"` and nothing else. This closes RP-OBL-K01. It does not select report05 or qualify anything.

## Custody

- **Subject:** manifest SHA-256 `480350895e0943c26db10eb6fd5277709733a169510a7c6f7cfdd2a421bf7ff9`, exactly 6 files, matching before and after.
- **Pins:** all 40 input pins and the parent pin (`implementation-coverage.v2.json` `f4d99fd4…`, 371850 bytes) matched before and after.
- **Run:** `check.py` ran on a copy with reference Python 3.14.6 `-I -B -X pycache_prefix=<empty>` and exit 0. Its output equals the frozen `root-result.json` exactly.

## Independent evidence (`probe-src/coverage_probes.py`)

- **Exact delta.** A recursive diff that also compares key order finds one addition, and the key is appended last. The bytes of v3 equal `json.dumps(indent=2)` of v2 with only that key added (+44 bytes, one line). The historical standing and subject-manifest fields are unchanged, as the README states.
- **Value selection.**
  - The validator requires the module keys to equal the delivery owners, and each delivery row's milestone to be at least its owners' values.
  - `assets.rs` is owned only by `commands/version` at M1.
  - Results by value: absent fails; **M0 and M1 are valid**; M2 through M6 fail with "Delivery precedes module prerequisite: version"; malformed values fail.
  - 40 of 41 modules use the earliest owning delivery-row milestone. The single pre-existing exception (`crates/host/src/analysis.rs`, M3 vs M4) is unrelated.
  - M1 follows that convention and equals the pending report05 overlay's own workaround value. M0 only passes the ordering check.
- **Pending overlay.** Composed with report05's own hash-verified `apply_overlay(..., with_workaround=False)`, which is independent of check.py's inline code:
  - 323 rows are valid, and the asset row stays version/M1;
  - the same value matrix holds;
  - composition over the uncorrected v2 still fails;
  - command metadata drift is still detected.

  Subject-05 (`a9f6c22a…`) verifies exactly and remains an unreviewed carrier correction. It is composed, not selected.
- **check.py negative controls.** A reformatted but semantically equal v3 passes. Each of these fails: value M0, key removed, a standing edit, a row milestone edit, and a changed input pin digest.

## Provenance note

The validator hash `dc7ac14a…` is the same one pinned by report projection subjects 03–06. In the architecture repository (HEAD `c3856824`), 24 of 37 pinned files are untracked and 8 tracked files carry local modifications, so provenance is by byte pin rather than by commit.

## Advisories

- **CA-1:** Acceptance should cite the frozen manifest and pin hashes, because commits don't cover the inputs.
- **CA-2:** check.py compares semantics only. Byte exactness comes from the frozen manifest, and this review confirmed it.
- **CA-3:** v3 keeps the historical metadata-v2 standing prose. Current standing belongs to `successor.json` and the manifest.
- **CA-4:** After acceptance, report05's scoped workaround must be removed and this successor bound explicitly. That rebase is not done here.

No report05 selection, source promotion, M1, implementation or release qualification is claimed.
