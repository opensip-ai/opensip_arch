# Independent design review — consolidated product **source34**

**Verdict: CHANGES_REQUIRED.** One new MUST (MUST-34-01), no new SHOULD, one new advisory (A-12).
Everything else verifies, including the changed atom law on every branch I tested.

Reviewer origin `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`, continuing. I have authored no source in this
lineage and am none of the six excluded acceptor origins. My source33 ACCEPT and both source33
reconciliations are historical and unchanged; they do not accept these bytes. No consumer output,
runtime, report or root blind replay file was opened, and no blind result is an input here.

---

## 0. Custody

- Manifest `bd00c07d…` and archive `5c9768de…` match their declared digests.
- All **12,899** rows (**736,798,408** bytes) verify by hash and size. Nothing is missing, mismatched
  or extra.
- The archive equals the manifest across every member.
- The parent is `1cf3db70…`, exactly the source33 I reviewed.

My delta comes from the two manifests: **9 changed, 0 added, 0 removed**, net +34,099 bytes. It agrees
with root's inventory on all 9 paths.

| File | Change |
|---|---|
| `foundation/atom-evaluation-contract.v1.md` | +169 / −1 lines; only **§4 Completeness partitions** changed (11 sections both sides) |
| `foundation/atom_model.v1.py` | +30 / −5; `_coverages_exact`, `_scopes_exact`, `_unique_pairs`, `_coverages_for_current_source` |
| `foundation/check-atoms.v1.py` | +339 / −0; 11 new cases plus fixtures |
| 5 pin ledgers + `workflows-report.v1.json` | digest re-pinning of those three owners only |

Root's later prose completion (`2d7c2594…` → `d7ef1336…`, the frozen34 contract) added the
search-accounting table, the absent/non-qualifying-vs-refusal sentence, the owed unknown-family wording
and the tie wording. The author-v2 run never reviewed those bytes; I did, below.

## 1. The changed atom completeness law

**Standing of my evidence.** Every control is my own design, not a reuse of the author's 81 cases or
root's five-case probe. Two standings appear:

- **atom-api**: real global atom-input admission, including IncomingSearchV1 schema and joins, plus
  `evaluate_atom`, over synthetic inputs.
- **helper-unit**: a private fold function called directly.

Neither is a retained Run or qualification. **No package11 retained Run contains an incoming-endpoint
atom or an IncomingSearchV1 record**, so retained Runs say nothing about the changed incoming branches.

| Branch | Result | Controls |
|---|---|---|
| Shared prelude P1/P2 | correct: P2 is shared by both endpoints, and its null universe projects as an absent key; an owed unavailable binding of **unknown** family blocks incoming only | A1, A3, A5 |
| No binding at subject universe, **outgoing** | correct: `selector-unbound`, unknown | A2 |
| No binding at subject universe, **incoming** | **defect: MUST-34-01** | A2, A4, q09 |
| Outgoing early returns | correct: each ends completeness only. With two known facts at every stop, `exists` true, `none` false, `count≤1` false, `count≤2` **unknown**, `all-covered` unknown, and the cause is kept. Without the stop, `count≤2` is true | B1, B2 |
| Incoming accumulation | correct: no further early return, per-(U, provider) accounting, a selected provider with no scope cannot disappear, and one failing universe hides nothing | F1, F2, F3, H1 |
| Cause channels / typed universe | correct: causes, `nativeDeficiencies` and the typed carrier stay separate, and endpoint causes carry the partition's S. Observation only: `target-export-unknown` carries the target universe | F3, E4, I1 |
| Dependency traversal | correct and unchanged from 33: only a calls partition paired to **this** subject at the **same** (S,T) heals reachability | D1–D5 |
| Fold ordering | correct: ascending ids, dedup **after** pairing, carrier = first partition **with** a deficiency, a Coverage paired by two scopes cited once. Every insertion order gives one result (24 and 480 orderings), and six fresh interpreters with six hash-seeded orders give one digest. **Frozen33 gives two results in both**, so the controls discriminate | E1, E2, H3 |
| Whole-record folds / ties | correct: RC/closedWorld replaced whole only when strictly worse, ties (incl. complete/not-applicable) keep the incumbent, confidence is an independent minimum, derivationKinds an ordered union. Helper-unit over natively valid records | E5b |
| Search-accounting table | agrees with the branches on **all 21 admitted cells** (6 pairings × 4 attestation kinds; the 3 no-scope attestations refuse at schema). A qualifying attestation with insufficient closedWorld still emits `coverage-unknown` | G1, G2 |
| Qualification predicate | over all 16 field combinations, 8 are admitted and qualify iff all four fields hold; a non-qualifying one equals an absent one. The other 8 are **global** refusals (`INCOMING_SEARCH_SCHEMA` / `_JOIN`), including attestations that don't match the current atom | G3, G4 |

## 2. MUST-34-01 — an incoming negative without searching the subject's own program

The published law defines incoming owed programs as the plan bindings of `capabilityForRelation`.
**P2** fires only when there is no binding at all. Incoming then makes **no further early return**.

So when the subject's own universe U has no binding for the relation, but another same-family
program is bound and fully evidenced, incoming never accounts for U at all:

| Same inputs, differing only at U | incoming `none` | incoming `exists` | outgoing `none` |
|---|---|---|---|
| U unbound, U2 fully evidenced | **true** (no cause) | **false** | unknown (`selector-unbound`) |
| U bound, no evidence | unknown | unknown | unknown |
| U bound, unavailable | unknown | unknown | unknown |
| U bound and evidenced | true | false | true |
| U unbound, only a Rust program bound | **true** (non-blocking disclosure only) | **false** | unknown |
| no references binding anywhere | unknown (`missing-relation-coverage`) | unknown | unknown |

Requesting **less** analysis turns unknown into a certain negative, and the result cites only the
other program's Coverage. The design already holds the opposite rule for outgoing (step 1) and for P2.
The defect is in the normative prose, not only in the reference.

- **Default profile: not reachable.** `requiredDefault` requests every non-NOT-SELECTED cell, and no
  engine family mixes NOT-SELECTED with requested modes for any incoming-capable capability.
  `syntax-only` is UNSUPPORTED-TYPED, which is requested and blocking.
- **Explicit narrowing: reachable by a lawful request.** `analysis.capabilities` overrides the request
  with its own provenance, and plan cells are exactly the requested tuples. My narrowed plan passes
  `enumeration-plan.schema.v1.json`. I did **not** run enumeration closed-world admission or build a
  retained Run.
- **Pre-existing.** The frozen33 model gives identical results. This is not a source34 regression, and
  **my own source33 ACCEPT and reconciliations missed it** (C34-01).
- **Required resolution** (wording is not mine to author): the incoming law must make an unbound
  subject universe visible and blocking, as outgoing does, or normatively define why it is not owed and
  require a typed disclosure. Either way it must also say what the foreign-family-only case answers.

## 3. Advisory A-12 — two published incoming alternatives cannot be reached

1. **Table row 1** says "no source scopes **and no qualifying attestation**". But IncomingSearchV1
   `scopeRefs` has `minItems 1`, and admission requires it to equal the provider's owned scopes, which
   are empty. So no admissible attestation can exist for that group. Attempting one refuses the
   **whole atom** globally instead of leaving it unknown. The lawful closure for an empty selected
   program is an explicit **empty-subject scope** with complete S→U Coverage. The native carrier
   admits it, and it closes incoming (R1).
2. **"Untagged scopes fall back to all S scopes"** is unreachable. A scope without `enumeratorClosure`
   is refused by the native scope carrier as soon as it is paired.

Every reachable outcome is correct, which is why this is an advisory and not a SHOULD.

## 4. Suites, planning, package

All jobs ran in a hash-verified disposable copy (1,357 files), except the pinned launcher, which
reads frozen34 directly. Frozen34 drift after every probe: **0**.

| Job | Why | Result |
|---|---|---|
| `check-atoms.v1.py` | own bytes changed | rc 0, **81/81** |
| `run-evaluator3-checks.py` | pins re-digested; atoms/full-replay consume atom_model | rc 0, pins valid, **16/16** children |
| foundation `run-reference-checks.py` | foundation pins | rc 0 |
| `check-integration.py` | all ledgers | rc 0, 412 passed |
| `check_native_evidence.v2.py` | native pins; sufficiency_v2 owner | rc 0, **375/375** |
| `check-security-lifecycle.v1.py` | security pins | rc 0 |
| workflows `run-reference-checks.py` | workflows pins + report | rc 0; regenerated report byte-equal |
| planning inventory / planning | planning checks on 34 | PASS 198 paths; PASS 320 mappings, 54 cases |

**Planning.** Layer4 is **retained**: the file is byte-identical, all 29 pins resolve against frozen34,
and none is in the delta. Layer3, layer2 and the original source25 layer remain history. Populations
are unchanged: 198 paths, 20 packages, 320 mappings, M0–M6, **54 recovery cases with 0 executed**. The
module-layout and inventory owners are byte-identical.

**Package11.**

- Artifact manifest `38f7ce94…`, identical to root's verified manifest. **311/311** members verify, and
  the source manifest is byte-equal to frozen34.
- Parent is the package10 I verified. **All 13 exports are byte-identical to package10**, so the
  construction provenance is unchanged and mixed: TS groups built on 33, normalized and Rust on 30.
  Only the verification is current.
- All 13 cases behave as expected through **both** `open_run_closure` and `close_run` with my own
  decoder.
- `verify-package.py` exits 0 over 12,899 source files and 311 package files, with **7/7** queries and
  group/report digests equal to root's.
- Compared with package10: +6 members, 0 removed, 4 changed (README, residual assessment, source
  manifest, verifier). The residual assessment now binds frozen34: 30 rows PENDING, TCB-SCOPE-01 over 13.
- A-10 limits are unchanged, and verifying the package grants no package acceptance.

## 5. The 107 rows

All maps are carried complete: **14 F, 30 evaluation residuals, 16 AR, 15 FW, 27 inherited, 5 scoped**.
No baseline field is edited; source34 facts are added as `currentStatusOn34`, `readingStandingOn34` and
manifest-derived `ownerFiles…In33to34`. **No row's owner is in the 9-file delta.**

- **91 inherited on exact bytes**: 88 owner-bearing rows plus F-04, F-07 and F-09. Each is labelled
  INHERITED, not re-read.
- **11 F rows re-verified on package11.**
- **5 cross-owner consequences of the atom law:**
  - **AR-12** and **FW-08** are *partially reopened by MUST-34-01*.
  - **FW-06**, **DR-009** and **AR-16** are *strengthened*, by the measured ordering and carrier
    determinism.
- **Stale legacy `readingStanding` strings: nine**, each qualified in
  `readingStandingLegacyCorrectionOn34` with the legacy string kept. Root counted eight: the rows that
  claim "unchanged" although their owners changed 32→33. The ninth, **DR-011-R12**, is the inverse case:
  it claims a changed owner region, but none of its owners changed.

Carried unchanged: **28** condition-2 obligations; **32** product gates with **0** performed and
condition 5 **NOT MET**; **54** recovery cases unexecuted; TCB-SCOPE-01 as one joint consequence over
**13** rows, not closed; the D9 implementation obligation on **DR-007** and **DR-011-R08**. All **30**
author proposals remain **PENDING**. Every row has `appliedByThisReview: false` and
`finalApplicationOutcomeGranted: false`. This review grants nothing: no grade, readiness, activation,
implementation, blind or package acceptance, application outcome, commit or push.

## 6. Probe errors kept on the record

- **q00**: assumed the wrong manifest size key.
- **q05 F4**: the fixture was refused by the native carrier, and that refusal became A-12(2).
- **q05 H3**: the child processes hit an import-path error; rerun in q06.
- **q05 E5**: used two natively invalid RC records; repeated as E5b.
- **q05 G4**: one mutation refused at schema before any join.
- **q08**: the scanner also counted schema-shaped objects as atoms; only the narrow counts are used.
- **q10**: the matrix parser measured nothing; replaced by q11.

## 7. Remaining issues, stated plainly

- **MUST-34-01** blocks design acceptance of these bytes. It needs a normative incoming-law decision,
  which is not mine to author.
- **A-12** is a prose/branch precision advisory.
- Out of scope and still open: the 30 residual grades, 32 gates, 54 recovery cases, TCB-SCOPE-01, D9,
  blind reconstruction and the final application review.
