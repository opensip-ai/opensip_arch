# Independent design review — consolidated product **source36**

**Verdict: ACCEPT**, scoped to the source36 design and reference bytes.

- **A-13 is CLOSED.**
- Every finding of my focused totality assessment is either closed or explicitly and coherently bounded.
- There is no new MUST or SHOULD.
- There are two new advisories: **A-14** (the attestation route now pairs dependency scopes for totality)
  and **A-15** (one generic empty-program sentence).

This acceptance grants **no application outcome**. It also grants no architecture readiness, activation,
implementation authorization, blind or package acceptance, product qualification, residual grade,
commit or push. The fresh application review stays separate, and this origin cannot satisfy it.

Reviewer origin `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`, actual Claude. I authored no byte of source36.

- **Authorship.** `823bf66b…` authored the dependency-scope and dependency-totality corrections and is
  **not an independent acceptor**. Root authored the later prose, registry and docstring completion and the
  pin re-sealing. I am neither.
- **Baselines.** My complete source35 **ACCEPT** (`d7dc035c…` / `687ed3dd…`) and my focused totality
  assessment (`4df5fb24…` / `a4e3f39a…`), both preserved unchanged.
- **Not read.** No consumer input, output, diagnosis, report, root blind control or expected result.
  Consumer-custody package members were hashed for custody only.

### Disclosed overlap with candidate authorship

In the focused assessment I wrote in-process **prototypes A and B**:
- **A** drops a non-total same-kind position.
- **B** applies the same rule to an attestation's named scopes.

I also proposed contract wording and precision items for root's history-order and runtime-polarity texts.

- **None of that is in the final bytes.** Measured (`receipts/p01-totality36.json`, X1 and E14a): my
  patched text, prototype code and wording are absent. The final `atom_model` is byte-for-byte the
  totality author's after file, and the adopted law is the author's two-view law, which differs from my
  prototype.
- **Conceptual coincidence.** The final law shares my finding's principle (every owed subject must be
  covered) and an equivalent attestation owed set.
- **Root's texts implement my precision items.** For those two items my confirmation is owner
  verification plus measurement, **not independent origination**.

I claim no blind, consumer-reconstruction or application-review standing.

---

## 0. Custody and delta

- Manifest `a729406b…` and archive `7db498f0…` match their declared digests.
- **12,899** files and **736,854,701** bytes verify:
  - nothing missing, mismatched, extra or duplicated;
  - the snapshot walk equals the manifest;
  - the archive equals the manifest, member by member;
  - the freeze record agrees.
- The parent is `eb45c22b…`, the source35 I accepted. No parent path is omitted.

My manifest-derived delta is **10 changed, 0 added, 0 removed**, net +31,452 bytes. Root's inventory
agrees on both paths and digests. Parent bytes come from the frozen35 archive, hash-checked
(`receipts/r00-custody.json`, `receipts/r01-diffs.json`).

| File | Change |
|---|---|
| `foundation/atom-evaluation-contract.v1.md` | +51 / −2: §4 dependency paragraph, **Dependency totality (same kind)**, **Empty and different-kind dependency boundaries**; §6 **Runtime polarity**; §9 cases |
| `foundation/atom_model.v1.py` | +68 / −18 (details below) |
| `foundation/check-atoms.v1.py` | +364 / −0: 12 new cases (89 → 101) plus builders; **no existing case body changed** |
| `foundation/evaluator-projection-registry.v1.json` | `historySubjectOrder.order` text, `uniqueKey` removed, `duplicatePaths` added, `observabilityFilter` text |
| 5 pin ledgers + `workflows-report.v1.json` | digest re-pinning only; every new digest is the frozen36 digest of a changed file |

The `atom_model` change is exactly:
- the mapping fallback in `_select_dep_coverages` is deleted;
- `_dependency_totality_gaps` is new;
- `run_suff` evaluates the gap-removed view as well;
- there are three gap call sites.

I1, P1/P2, pairing, selection order, the fold and `_result` are byte-untouched.

**Final bytes, not author snapshots:**
- the dependency-scope author produced intermediate contract, model and checker bytes;
- the totality author produced model `4477285c…`, which is **final**;
- root then changed the contract (→ `8649b8b0…`), check-atoms (→ `42f11417…`, **one docstring**; the AST is
  equal ignoring docstrings) and the registry (→ `65f163cc…`).

I tested the final bytes.

## 1. A-13 — CLOSED

In §4, a `coverageScopes` entry naming a scope outside the exact dependency `(relation, rung, S)` now
*contributes no pairing*. A dependency occupies no position only when no selected Coverage remains. The
reference deletes the fallback branch.

Measured on both endpoints across the 10 carrier mutations:
- **20 of 20** rows that frozen35 healed to `true` are now identical to the dependency-absent answer:
  unknown, `required-relation-missing`, Coverage not cited.
- An exact scope still pairs beside a mapped wrong-universe scope, and the mapped Coverage is not cited.
- final36 equals the dependency-scope successor on every A-13 row.

This is atom-api evidence. A-13 was advisory on source35 because `close_run` already excluded the shape
for retained Runs.

## 2. Dependency totality — assessed on final bytes

I wrote the expected law (`law-derivation36.json`, 21:03:07Z) before the first semantic probe
(21:11:27Z). All fourteen expectation groups held (`receipts/p01-totality36.json`, 37 checks, 0 failed).

**The law is correct and conservative.**
- **Owed set.** The owed set of a view is the primary partition that view evaluates.
- **Covered.** A subject is covered when an exact selected scope contains it and pairs a Coverage at the
  evaluated target, using the one existing selection and pairing law.
- **Gap.** A present gap position is evaluated twice, on the actual view and on the gap-removed view.
  Satisfaction needs both, so the removed position answers `required-relation-missing` exactly as native
  `sufficiency_v2` step 1 does. Native step 8 recurses `DEPENDS_ON` to depth 4.
- **Owners that require it:**
  - native RC-4: reachability counts calls "over the same examined set";
  - atom §4: "No fictional complete entries";
  - identity §3: *complete* is a claim about the examined partition.

| Shape (incoming reachability over {f, g}) | frozen35 | final36 |
|---|---|---|
| g absent; g scope without Coverage; g Coverage at another target; g wrong-universe scope; unrelated h only; f absent | **true** for `all-covered`, `none` and `count≤1` in every shape (also on the dependency-scope successor) | **unknown** for all three with `required-relation-missing`; f's dependency stays cited |
| disjoint {f}+{g}; one spanning scope; disjoint plus h | true | true, no deficiency, h not cited |
| attestation: f-only; h-only; g scope without Coverage | **true** | **unknown** |
| attestation: f+g; spanning; none | true / true / unknown | true / true / unknown |
| outgoing from f or from g, any shape | — | identical value, causes and citations on frozen35, the dependency-scope successor and final36 |
| known fact (g reaches f), f-only: `exists`, `none`, `count≤0`, `count≤1`, `all-covered` | true, false, false, **true**, **true** | true, false, false, **unknown**, **unknown**; fact retained |

- **Cause and citation channels.** When f's partition carries `input-closure-incomplete` /
  `lockfile-missing` and g is uncovered, final36 reports:
  - `nativeDeficiencies` {`input-closure-incomplete`, `required-relation-missing`};
  - a single `coverage-unknown` with nativeCause `lockfile-missing`;
  - f's Coverage cited.

  Nothing is fabricated.
- **Determinism.**
  - 48 insertion orders × 5 totality shapes × both endpoints give one result each.
  - My E1 (24 orders) and E2 (480 orders) carrier controls and the totality shapes give one result each.
  - Six fresh interpreters with six hash-seeded map orders give **one digest**
    (`receipts/p02-determinism36.json`).
- **Controls discriminate.**
  - frozen36 check-atoms is **101/101** on final36.
  - Every totality control fails on frozen35 (9 failing cases, including the three A-13 controls) and
    on the dependency-scope successor (6).

### Author's two-view law vs my focused prototype A/B

**The two-view law is the better correction and supersedes my prototype.** Both give unknown on every
gap. The difference is what each keeps:

| Measure | final36 two-view | prototype A |
|---|---|---|
| `nativeDeficiencies` for f-partial with g uncovered | {`input-closure-incomplete`, `required-relation-missing`} | {`required-relation-missing`} |
| `coverage-unknown` nativeCause | `lockfile-missing` | null |
| f's Coverage cited | yes | **no** |
| attestation route, f complete, g uncovered | unknown | **true** (A without B) |
| frozen36 check-atoms totality controls | all pass | 4 fail (also under A+B) |

Native §4.6 retains "the evidence the evaluation read … with its own deficiency and nativeCause
carrier". Atom §4 cites every folded partition. `required-relation-missing` has no entry carrier, so no
truthful alternative nativeCause exists. **C36-01** records that my focused remedy recommendation is
superseded; its defect classification stands.

### Root's regrouping qualification — correct

The author's original sentence, "regrouping … cannot change the value or the cause set", is false for
partial carriers:

| Grouping | `coverage-unknown` records | Value |
|---|---|---|
| merged {f, g}, f carrying `lockfile-missing`, g uncovered | one (`lockfile-missing`) | unknown |
| split {f}, {g} | two (`lockfile-missing` and null) | unknown |

This comes from the published per-view fold law, not from totality. Frozen35 already splits two partial
carriers into two records. The value is equal across all six grouping shapes, and causes are equal for
complete-entry shapes.

Root's text keeps "preserves the truth of this totality check" and disclaims identical proof records,
cited primary ids and per-view carriers. No algorithm or assertion changed. The regrouping control
asserts equal causes only for complete-entry fixtures.

### Empty and different-kind boundaries — coherent

- **Empty program, reachability.**
  - The Coverage route stays unknown, even beside an explicit empty calls partition, because same-kind
    containment selects nothing.
  - The attestation route closes with an explicit empty calls partition and stays unknown without one.
  - `references`, which has no dependency, closes by either route.
  - Everything is unchanged from 35.
- **Different kind.** clones (file) → declares (symbol) stays whole-source and unchecked, so declares for f
  alone still closes clones.
- **Why this coherence holds:**
  - native `DEPENDS_ON` has only two edges, and RC-4 names reachability/calls only;
  - RC-6 invents no universal absence;
  - identity owes the omission half only for `file@enumerated`, and its partition law admits empty
    subjects without promising closure;
  - the execution-inputs census still discloses uncovered expected subjects;
  - no owner publishes a file-to-symbol correspondence (native line 301 is a capability-law statement).

Declining to invent one is the honest limit, and it is stated as a profile decision. One earlier generic
sentence should be scoped (**A-15**).

### Root's history-order and runtime-polarity texts — aligned and exact

Measured in `receipts/p03-history-runtime36.json`, 15 checks, 0 failed.

- **Registry delta.** Exactly two texts: `historySubjectOrder.uniqueKey` removed and `duplicatePaths`
  added.
  - No owner still says "strict unique path".
  - The registry text is consumed only as registry text.
  - The repair `targetSubjectProjection` ambiguity refusal is still published.
- **History behaviour.**
  - The stock schema admits duplicate paths in non-sorted producer order.
  - The atom keeps ordinals [1, 2] identically on 35 and 36.
- **Runtime behaviour, identical on 35 and 36:**
  - unfiltered `exists` is true on `observed-hit` and on `observable-unhit`;
  - `eq` filters restrict polarity;
  - `unobservable` and `unmapped` never enter R;
  - a filter naming them is admitted and matches nothing;
  - "relevant" means subject-occupancy-matched: such rows are disclosed as uncertain with cause under every
    filter, and a non-matching row is not.

### Reachability, by standing

| Standing | Finding |
|---|---|
| synthetic atom-api | **exercised**: p01, p02, p03; check-atoms 101/101 |
| native producer / carrier | producer not run; the carrier is reached through atom admission only |
| closed enumeration | **not run** |
| retained Run | package13's 13 Runs, replayed by me, carry only `exists/file/source` and `none/clones/source`. They have no reachability, incoming, runtime-observation or history-change atom (`receipts/p04-package-reach.json`), so **no retained Run reaches the changed branches** |
| product | **not established** |

## 3. Suites, reference, planning, package13

- **Suites.** Run on a hash-verified disposable copy of 1,357 files; the pinned launcher reads frozen36
  directly (`receipts/r04-suites.json`):
  - check-atoms **101/101**;
  - evaluator3 launcher **16/16**, pins valid;
  - foundation (1,240 files); integration **412**; native **375/375**; security;
  - workflows, with the regenerated report byte-equal;
  - all exit 0, with **0** frozen drift.
- **Root and codex reference, compared and not adopted** (`receipts/p06-reference-compare.json`):
  - Root's six groups exit 0 with sources equal to frozen36, **but root ran them on the mutable successor
    tree**; my runs are on frozen bytes.
  - My 16 children equal root's.
  - Identity counts recomputed from my run are **1,596** passing calls, **1,584** distinct ids and 12
    duplicate instances. They equal codex's, and my identity report is byte-equal to root's.
  - The codex copy equals root's runtime except `reference-checks.json`: codex holds the bound form and
    the runner original separately, both verified.
- **Planning.** The planning input layer (layer4) is **retained**. Its 29 inputs are byte-identical, all
  resolve against frozen36, and none is in the delta. Measured populations: **198** paths, **20 packages**, **320** mappings, M0–M6,
  **54** recovery cases, 0 executed. The planning owners are unchanged. Root's planning run was also on the
  mutable tree.
- **Package13** (`receipts/r05-package13.json`, `receipts/p05-package-lineage.json`,
  `receipts/p07-package-member-diffs.json`):
  - **Custody.** Manifest `47dbe781…` equals the declared and root-verified digests. **323/323** members
    verify, and the source manifest equals frozen36.
  - **Lineage.** The parent is package12 (`fb35036f…`): 6 added, 4 changed, 0 removed, 313 identical. The
    four changed members are binding-only: the verifier's `EXPECTED_SOURCE`, README version text, and
    the residual assessment's subject, standing and resolveAgainst.
  - **Exports.** All 13 exports and claims are byte-equal to package12, and so to package11 and
    package10. Construction accounts are byte-equal. **Mixed provenance is retained (TS groups on 33,
    normalized/Rust on 30).**
  - **Boundaries.** All 13 cases, through **both** `open_run_closure` and `close_run` with my own decoder
    and the frozen36 owner (unchanged 35→36):
    - 7 positives admit;
    - 3 semantic controls refuse `EVALUATOR_COMPLETE_PROOF_REPLAY`;
    - `ts-invalid-default-entry` refuses `ENUMERATION_BINDING_PROGRAM_ENTRY`;
    - the two lawful binding controls admit.
  - **Verifier.** `verify-package.py` exits 0 over 12,899 source and 323 package files, with **7/7**
    queries. Groups, observed outcomes and report digests equal root's, and verification.json is
    byte-equal. Binding is not replay; the replay standing is my own calls.
  - **Residual assessment.** Binds frozen36, 30 **PENDING**, TCB-SCOPE-01 over 13.
  - **Limits.** A-9 (repair reference-only) and A-10 (partial helper, exists/none operators, incomplete
    two-binding construction) are unchanged. No blind or product-qualification conclusion follows from
    these synthetic examples.

## 4. Advisories

- **A-9, A-10:** carried with limits intact. **A-11:** historical. **A-12:** closed on 35; its empty-scope
  and carrier behaviour still holds.
- **A-14 (new, informational).** On the attestation route, the totality check now pairs dependency scopes
  that hold owed subjects. An exact calls scope over f with a null or absent `enumeratorClosure` therefore
  refuses `ATOM_NATIVE_CARRIER`, where frozen35 answered true.
  - It is consistent with "covered … pairs at least one Coverage" and "a selected scope that fails the
    carrier is refused when paired".
  - It is conservative: the Coverage route already refused the same scope on 35, and `close_run` admits
    every retained subject-scope object.
  - No §9 case or control pins it; a successor should.
- **A-15 (new, textual precision).** Admitted-inputs item 1 (lines 242–246) says an empty program closes
  incoming with an empty scope "paired with complete S→U Coverage or named by a qualifying attestation".
  For a relation with a same-kind dependency, the Coverage alternative never closes. The source36 boundary
  paragraph says exactly that, and the §9 control uses `references`.
  - This is not a SHOULD: the reference result is never false, and the specific, labelled profile rule
    governs.
  - Recommended wording for item 1: add "; this closes the search account only, and dependency sufficiency
    still applies (see Empty and different-kind dependency boundaries)".
  - Recommended wording for §9: "merged and split partitions answer alike" → "answer alike in value".

## 5. The 107 rows

All maps are carried complete: **14 F, 30 evaluation residuals, 16 AR, 15 FW, 27 inherited, 5 scoped**.
Every baseline field is preserved verbatim, including all `*On33`, `*On34` and `*On35` fields. Each row
adds explicit `currentDispositionOn36`, `currentStatusOn36`, `readingStandingOn36` and the manifest-derived
`ownerFilesChangedIn35to36` (empty for every row) / `ownerFilesUnchangedIn35to36`.

The source36 standing, derived rather than copied (it coincides numerically with source35's historical
91/11/5):
- **91 inherited on exact bytes**, including F-04, F-07 and F-09. AR-08 and FW-10 add a checked note that
  the repair ambiguity refusal is unaffected.
- **11 F rows re-verified on package13.**
- **5 cross-owner rows:**
  - **AR-12** and **FW-08** are *strengthened*: an incoming negative or omission can no longer stand on a
    partial same-kind dependency census;
  - **AR-16**, **FW-06** and **DR-009** *hold*, re-measured: carrier order, insertion-order and
    cross-process determinism.
- **The nine legacy reading-standing corrections** (AR-13, FW-01, FW-02, FW-04, DR-011-R03, DR-011-R05,
  DR-011-R08, DR-011-R12, DR-204) are retained unchanged and still accurate. C34-01 and C35-01 are
  preserved, and **C36-01** is added.

Carried unchanged:
- **28** condition-2 obligations;
- **32** product gates, 0 performed, condition 5 **NOT MET**;
- **54** recovery cases, 0 executed;
- TCB-SCOPE-01 as one joint consequence over **13** rows, not closed;
- D9 on **DR-007** and **DR-011-R08**;
- all **30** residual proposals **PENDING** until the separate final application review.

Every row has `appliedByThisReview: false` and `finalApplicationOutcomeGranted: false`.

## 6. Probe errors kept on the record

- **p01, first run:** stopped at model load after its five byte-provenance checks passed. The disposable
  tree lacked `design-corrections/discovery-defaults.py`. The tree was widened, still hash-checked, and
  the probe rerun as `p01_totality36.2`. No semantic check had run.
- **r05, lineage:** it treated `predecessor-artifact-manifest.json` as package12's manifest, but that file
  is an older 97-member manifest. Its lineage rows are void and superseded by p05, which measured against
  package12 itself.
- **r05, reach marker:** its count of 26 had an operator-precedence flaw and is not relied on. p04 lists
  exact paths.
- **r08, keyword scan:** it matched all 107 rows because of carried history text, so it selected nothing.
  Cross-owner rows were chosen by reading row subjects.
- All source35 probe errors are preserved.

## 7. Remaining, stated plainly

There are no blocking design issues on these bytes. A-14 and A-15 are advisory.

Still open, outside this review:
- the 30 residual grades, 32 gates, 54 recovery cases, TCB-SCOPE-01 and D9;
- blind reconstruction;
- native-producer, closed-enumeration, retained-Run and product reachability of the dependency law;
- an empty-program producer attestation form;
- any successor correspondence for different-kind population;
- the separate final application review.
