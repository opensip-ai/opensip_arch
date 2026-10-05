Codex review: law **HSR r2**, the correction of HSR-RF-01. Grok leads as of 2026-10-04. You are the single reviewer.

HSR-1 stays **ACCEPT-DESIGN-UNIT**. Do not re-review it and do not write another `hsr-1/review.json`. Its review is `docs/implementation/m3/reviews/grok-hsr-r1/hsr-1/review.json` (5,297 bytes, sha256 `fd5906f65fda99ec5ea255812dffeab002de4b15d27bf75aaa9551bdf4771c7f`). The six subject files are byte-identical to that review. Binding stays held until this law is accepted.

One verdict. `ACCEPT` or `REQUIRED-FINDINGS`, with `requiredFindings` and `subjectSha256` of `docs/implementation/m3/syntax-e/hsr/PROPOSAL.md` (`f56145e21f6e05a3699c636bc0d6bc5bf0733decb7f213601670d70a927334fe`, 47,157 bytes).

Write only `review.json` and `REVIEW.md` under `/tmp/opensip-implementation/reviews/grok-hsr-r2/`. Do not rewrite `/tmp/opensip-implementation/reviews/grok-hsr-r1/` or anything under `docs/implementation/m3/reviews/grok-hsr-r1/`. No repository edits, commits, pushes, or delegation. No cargo, build, test, or crash-matrix run. Do not take the lane lock.

**Rules:**

- Git is read-only. Product main is `/Users/sb/code/opensip-ai/opensip` at `43ea32a`. Arch is `/Users/sb/code/opensip-ai/opensip_arch`.
- Python only if you check the fixture: `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`. Private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`.
- Do not rerun `verify_scratch.py`. The r1 binding evidence stands because the HSR-1 files did not change.
- Never touch `~/Library/Application Support/OpenSIP`. Never read the private 413 UUID fixture.
- The lane lock is held by the I1-c review. Do not start cargo and do not remove the lock.

## Subject

Diff base: `docs/implementation/m3/syntax-e/hsr/PROPOSAL-r1.md` (44,788 bytes, sha256 `19770e3541f71139b2771350399e7967df6da8c6517b747e07d4a435d2d5ae6e`), the bytes of your r1 review.

r1's law verdict was REQUIRED-FINDINGS, finding HSR-RF-01 only. r1's HSR-1 verdict was ACCEPT-DESIGN-UNIT. r2's edit is the answer to that finding:

- Fourteen producer cases have `payloadSchemaDigest: null`. HSR-a re-points only those to `Some(H1)`.
- `wrong-schema` keeps its explicit 64 zero digits and its expected `REFUSE` / `native.coverage-payload-schema-not-registered` / empty faults, both while H1 is dormant (HSR-T9) and after H1 is active (HSR-T10, E2s-T3).
- The corpus file is not edited.

The test that preserves an explicit digest and uses `None` only for null is `crates/host/src/native_owner_tests.rs:865-869` at product `43ea32a`. The 15 cases are `coverageProducer` in `crates/host/tests/fixtures/native-context-fixtures.json`.

## Decide

- Is HSR-RF-01 closed by that re-point, with the corpus unchanged and the unknown-digest refusal kept before and after H1 activation?
- Did r2 change any other decision? A new disagreement is a finding. Q1, Q2, Q3 and Q5 were PASS on r1; say if the r2 text disturbs them.
- Do not bind HSR-1.

When you finish, reply with one line: the verdict and the `review.json` path.

Do not commit.
