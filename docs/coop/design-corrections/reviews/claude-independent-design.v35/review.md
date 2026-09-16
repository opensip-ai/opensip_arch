# Independent design review — consolidated product **source35**

**Verdict: ACCEPT**, scoped to the source35 design and reference bytes. **MUST-34-01 is CLOSED** and
**A-12 is CLOSED**. There is no new MUST or SHOULD. One new advisory, **A-13**, records a pre-existing
reference path that retained Runs cannot reach.

This acceptance grants **no application outcome**, and no readiness, activation, implementation
authorization, blind or package acceptance, product qualification, commit or push. The fresh
application review stays separate, and this origin cannot satisfy it.

Reviewer origin `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`, actual Claude. I have authored no source, I am
not the source35 correction author (`823bf66b…`), and I am none of the six excluded acceptors. My
baseline is my own **source34 CHANGES_REQUIRED** record (`c31f1c47…` / `72e4e1b0…`), preserved
unchanged. Source33 acceptance is not resurrected, and root's bounded assessments are not treated as
whole-design assent. No consumer output, diagnosis, report, root blind control or expected result was
read.

---

## 0. Custody and delta

- Manifest `eb45c22b…` and archive `f5292e68…` match their declared digests.
- **12,899** files and **736,823,249** bytes verify: nothing missing, mismatched or extra.
- The archive equals the manifest, and the freeze record agrees.
- The parent is `bd00c07d…`, the source34 I reviewed.

My manifest-derived delta is **10 changed, 0 added, 0 removed**, net +24,841 bytes. It agrees with both
root inventories.

| File | Change |
|---|---|
| `foundation/atom-evaluation-contract.v1.md` | +63 / −4; §4 (I1, admitted-inputs note, owed programs, table row 1) and §9 cases |
| `foundation/atom_model.v1.py` | +21 / −19; `_native_completeness` (I1), `_scope_descriptor`, `_derive_scope_commitment` |
| `foundation/check-atoms.v1.py` | +316 / −1; 8 new cases plus builders; one fixture enum corrected |
| `foundation/incoming-search.schema.v1.json` | **metadata only**: `x-opensip-law/joins/5` text; no validation keyword changed |
| 5 pin ledgers + `workflows-report.v1.json` | digest re-pinning only |

**Final bytes, not author snapshots.** After the author finished, root changed three files:

- the contract (`7ee61c18…` → `f6c3b375…`): empty `scopeRefs` is a SCHEMA refusal, while borrowed
  non-empty `scopeRefs` is a SCOPE_MISJOIN;
- the schema metadata (`fd5c51ea…` → `fcea86fa…`);
- one checker assertion (`258099be…` → `11aa038a…`).

All three final digests equal frozen35. I tested the final bytes.

## 1. MUST-34-01 — CLOSED

**Law now published (§4 I1).** When no available owed binding has `universe = U`, incoming emits
`selector-unbound` with the universe key omitted and marks completeness unknown. It does **not** return.
It runs after P1/P2 and before per-universe accumulation. The owed-programs paragraph now states that
the subject universe is always an owed source.

**My independent controls** (atom-api, synthetic inputs, frozen35 compared with frozen34):

| Control | Result |
|---|---|
| Predictor written from the §4 prose vs actual answer | **192** cell-ops (4 subject-U states × 3 same-family states × foreign available/unavailable × 4 ops): **0 mismatches** in value and exact cause set |
| Any incoming negative without an available binding at U | **none** on frozen35 |
| Outgoing and P2 | all 48 outgoing cells **byte-equal on 34 and 35** and equal to the outgoing predictor |
| What changed 34→35 | 92 cell-ops, **all** with U lacking an available binding and gaining `selector-unbound` (28 value changes, 64 cause-only); P2 cell unchanged |
| Record shape | one `selector-unbound`, universe key omitted |
| Known matches and count bounds, U unbound | `exists` true, `none` false, `count≤0` / `count≤1` false (bound exceeded), `count≤2` / `count≤3` **unknown**, `all-covered` unknown, facts retained. With U bound: `count≤2`/`≤3` and `all-covered` true |
| Provider / cell / attestation / map permutations | 240, 1,440 and 240 orderings in 3 cases → **1** result each |
| Same- and foreign-family unavailable cases | unavailable never satisfies I1; `unavailable-program-binding` and both `cross-family-edge-not-owed` routes are kept beside `selector-unbound` |

**Scope.** This is atom-api evidence. Closed enumeration admission was not run, and no package12
retained Run contains an incoming-endpoint atom or an IncomingSearchV1 record. Whether product
configuration can express per-unit narrowing remains unestablished. The law no longer depends on it:
an unbound subject universe is unknown however the request was produced.

One synthetic observation, not an issue: a `rust-cargo` binding carrying a TypeScript-domain universe U
satisfies I1 and is then skipped as foreign, on both 34 and 35. The enumeration contract requires an
available binding's universe to be the native admission of that mode's own context, so no admitted
plan has that shape.

## 2. A-12 — CLOSED, with one residual (A-13)

**Scope-less groups and empty programs**, identical on 34 and 35, so no code change was needed:

- no attestation → `source-target-search-unattested`;
- empty `scopeRefs` → global `INCOMING_SEARCH_SCHEMA`;
- borrowed or nonexistent non-empty `scopeRefs` → global `INCOMING_SEARCH_SCOPE_MISJOIN`, as the root
  wording says;
- an explicit **empty-subject scope** closes only with complete S→U Coverage or a qualifying
  attestation; with unknown Coverage or a non-qualifying attestation it stays unknown;
- it **cannot hide real inventoried subjects** (`uncovered-expected-source-subject`), and it never
  closes an outgoing subject.

**Missing-key carrier bypass.** I tested all **8** carrier fields × absent/null × **4** consumption
paths: outgoing containing scope, incoming source scope, dependency pairing, and a scope named by a
globally admitted attestation of another relation.

- On frozen35, 58 of 64 cases are either a refusal (42) or identical to the scope-deleted answer (16).
  The other 6 are A-13.
- **18** frozen34 cases that answered as though the inadmissible scope were valid evidence now refuse.
  They cover absent `schemaVersion`, `snapshotId`, `targetUniverse` and `enumeratorClosure`, plus
  `subjects` absent or null on the attestation path.
- The only null-field change is `subjects: null`, which frozen34 also skipped.

**Schema owner.** Every probe instance gets the same verdict under the 34 and 35 schema. The join text
now names the native carrier and states that there is no untagged fallback.

**A-13 (advisory, new finding, pre-existing behaviour).** Suppose no exact (relation, rung, S)
dependency scope exists. Then the `_select_dep_coverages` coverageScopes mapping fallback still accepts
a scope whose `relation`, `resolution` or `sourceUniverse` is absent, null, **or validly different**. It
heals reachability to `all-covered` true, whereas deleting that scope gives unknown. Frozen34 behaves
identically. The new §4 sentence says pairing validates the carrier wherever a scope is consumed; the
reference is looser on this one branch.

It is not a SHOULD because retained Runs cannot reach it. `close_run` admits every retained
subject-scope object and requires `coverage.scopeId` in the view (`COVERAGE_SCOPE_JOIN`). It also re-runs
native `admit_coverage_result_v3` over that retained scope.

## 3. Cross-owner consequences, suites, planning, package

- **Determinism on the changed pairing path, re-measured:**
  - E1: 24 orderings × 4 → one result each.
  - E2: 480 orderings × 2, including a Coverage paired by two scopes through the derived commitment →
    one result, carrier `lockfile-missing`.
  - Six fresh interpreters with six hash-seeded orders → **one digest**.
- **Suites** (hash-verified disposable copy of 1,357 files; the pinned launcher reads frozen35):
  - check-atoms **89/89**;
  - evaluator3 launcher **16/16**, pins valid;
  - foundation reference; integration 412; native **375/375**; security; workflows, with a regenerated
    report byte-equal;
  - planning PASS: 198 paths, 320 mappings, 54 cases.
  - All exit 0, with **0** frozen drift.
- **Planning.** Layer4 is **retained**: its 29 inputs are byte-identical and none is in the delta.
  Populations are unchanged: 198 paths, 20 packages, 320 mappings, M0–M6, 54 recovery cases, 0 executed.
  The layout and coverage owners are byte-identical.
- **Package12:**
  - Artifact manifest `fb35036f…` equals the declared and root-verified digests; **317/317** members
    verify, and the source manifest equals frozen35.
  - Parent is package11. **All 13 exports are byte-identical** to package11, and so to package10: no
    remint, no relabelled execution, and mixed construction (TS groups on 33, normalized and Rust on 30).
  - All 13 cases behave as expected through **both** `open_run_closure` and `close_run` with my own
    decoder. `verify-package.py` exits 0 over 12,899 source files and 317 package files, with **7/7**
    queries and digests equal to root's.
  - Residual assessment: binds frozen35, 30 PENDING, TCB over 13.

## 4. The 107 rows

All maps are carried complete: **14 F, 30 evaluation residuals, 16 AR, 15 FW, 27 inherited, 5 scoped**.
No baseline field is edited, including every `*On34` field. **No row's owner is in the 10-file delta**,
and all 107 owner sets are byte-equal 34/35.

- **91 inherited on exact bytes**: 88 owner-bearing rows plus F-04, F-07 and F-09.
- **11 F rows re-verified on package12.**
- **5 cross-owner rows:**
  - **AR-12** and **FW-08** are *restored* now that MUST-34-01 is closed;
  - **FW-06**, **DR-009** and **AR-16** are *strengthened and still holding*, re-measured on 35.
- **The nine legacy reading-standing corrections** (AR-13, FW-01, FW-02, FW-04, DR-011-R03, DR-011-R05,
  DR-011-R08, DR-011-R12, DR-204) are retained unchanged and still accurate.
- **C35-01 corrects my own source34 record.** My A-12(2) said a scope without `enumeratorClosure` is
  refused as soon as it is paired. That held only for an explicit null. An **absent** key skipped the
  carrier on frozen34.

Carried unchanged: **28** condition-2 obligations; **32** product gates, 0 performed, condition 5
**NOT MET**; **54** recovery cases unexecuted; TCB-SCOPE-01 as one joint consequence over **13** rows,
not closed; D9 on **DR-007** and **DR-011-R08**. All **30** author proposals remain **PENDING**. A-9 and
A-10 limits are unchanged; A-11 is historical. Every row has `appliedByThisReview: false` and
`finalApplicationOutcomeGranted: false`.

## 5. Probe errors kept on the record

- **r02 M3:** my outgoing predictor treated the non-blocking cross-family disclosure as blocking on
  three cells. 34 = 35 held throughout; corrected in r07 M3b.
- **r02 P1:** the claim text said "720" plan-cell orders. That is exact for the U-bound case (720, or
  1,440 with reversal) but overstated for the two U-unbound cases (120, or 240 with reversal). My first
  draft of this note called all three 240; the invariant check caught it.
- **r03 C2/C3:** framed too strictly; recomputed from the same receipt in r07. C1's six failures are
  real and became A-13.

## 6. Remaining, stated plainly

There are no blocking design issues on these bytes. A-13 is advisory, and so is the synthetic
contradictory-family observation.

Still open, outside this review: the 30 residual grades, 32 gates, 54 recovery cases, TCB-SCOPE-01,
D9, blind reconstruction, closed enumeration and retained-Run reachability of the incoming law, and
the separate final application review.
