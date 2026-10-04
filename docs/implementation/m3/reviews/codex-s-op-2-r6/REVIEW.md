# S-OP-2 r6 review

**Verdict: ACCEPT-DESIGN-UNIT.** SOP2-R5-01 is resolved. No required findings remain.

Subject: `docs/implementation/m3/operability/s-op-2/PROPOSAL.md`, 130,001 bytes, sha256 `ce8d3a4b783328915f0bf550dd111f227aa9901d5efddbcd9ccc8707cd4cb11d`. The subject matches the request. `PROPOSAL-r5.md` matches the exact previous review subject: sha256 `a75afe9cede097dd52e8c83862060a8debd1b298e2320ab9321068745601b15b`, 129,029 bytes.

## Finding resolution

**SOP2-R5-01 — resolved.** Item 13c at line 532 restores the operative object rule: each composite has exactly its selected listed form's keys, with no extra, missing or duplicate key; writers use the listed order; readers accept any order and canonicalize on re-encoding. The selected-form language preserves variants such as K13 with or without a column. Item 13a's whole-line duplicate and header checks remain unchanged.

C-4 at line 941 now requires a permuted-key composite to be admitted and canonically re-encoded, and extra/missing/duplicate keys to be refused. This supplies the requested reader positive and negatives while preserving the existing canonical writer round trips.

## Diff assessment

The complete exact-byte diff contains three changed regions: the r6 changes section, the restored Objects rule, and the C-4 addition. Reversing those three textual edits reconstructs r5 exactly. No other substantive text changes. The previously reviewed prescope partition, marker protocol, lawful path suffixes, bounds, ownership and deferred-successor decisions are preserved. Evidence is in `subject-diff.txt` and `change-summary.json`.

## Non-blocking observation

**SOP2-R6-NB-01.** At line 941, the new C-4 Key order control was appended in the table's Items column. Its requirement is present and clear. Move that prose into the What/control column before the Items separator when formatting the recording text.

## Scope

This accepts the pinned successor text only. The later recording unit still requires its own ACCEPT-DESIGN-UNIT and single-string subjectManifestSha256. No product implementation or inventory is accepted here.

All new artifacts are confined to this r6 review directory. No repository edit, commit, push, build, Cargo command, test, crash-matrix run, delegation, real OpenSIP-home access or 413-fixture access occurred. Read-only-input digest/diff scripts used Python 3.14.6 with -I -B, nice -n 19 and a private 0700 TMPDIR under this directory.
