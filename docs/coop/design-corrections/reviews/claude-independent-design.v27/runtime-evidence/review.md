# Independent design review — consolidated product **source27**

**Successor delta and focused evidence review.** Same reviewer origin that produced the source26
`CHANGES_REQUIRED` review (`ce3dec3b-0620-44ec-86e6-129b0e25cb1b`). Design, architecture, schema and
reference layers only.

**Verdict: ACCEPT.**

Every required action is completed and there is no unresolved MUST or SHOULD. The one MUST and the
three SHOULDs I raised against source26, and all three of my v26 advisories, are resolved in source27
by properties I measured or executed. I raise no new MUST and no new SHOULD. Three advisories are
recorded; two sit on inherited material the delta did not touch, and each states why it is not a
SHOULD.

This grants **no application grade, no activation, no blind acceptance and no implementation
authorization**, and closes none of the 30 evaluation residuals, none of the 28 condition-2
obligations, none of the 32 gates and none of the 54 recovery cases.

---

## 1. What I verified before reading anything

| Binding | Expected | Measured |
|---|---|---|
| Manifest sha256 | `a1ae88ef…0227a` | ✅ matches |
| Archive sha256 | `adb78633…27603` | ✅ matches |
| Files | 12,893 | ✅ 12,893 verified, every sha256 and byte count, 0 extras |
| Total bytes | 736,295,158 | ✅ 736,295,158 |
| Declared parent | `c9a6c26a…0ffb2` | ✅ **byte-identical to the manifest of the source26 subject I reviewed** |
| Author package `artifact-manifest.json` | `7d6ad55a…d8e00` | ✅ 213/213 verified, 0 mismatched, 0 missing |
| Package `source-manifest.json` binding | exact27 | ✅ binds `a1ae88ef…` |

Ancestry is proven by measurement, not narrative. The frozen snapshot re-measured **unchanged** after
every run I performed (0 deviations). No pin gate was bypassed, disabled or rewritten; report-writing
checkers ran only inside a disposable copy whose every byte I first verified against the frozen
manifest.

## 2. The 26→27 delta, derived by me

From the set difference of the two frozen manifests, then line-diffed with both sides
manifest-authenticated: **1 added, 0 removed, 19 changed, +17,818 bytes.** Nothing touches the
reviews tree. Eight of the changed files are pure digest or pin refreshes — I diffed them and
confirmed the only semantic edits are the B11→B14 anchor disambiguation and pin-digest updates.

The delta is small enough to review exhaustively, and I did.

## 3. Correcting my own prior review

I am recording these here and leaving the v26 report exactly as issued.

**C-1 — scope overclaim (required correction).** v26 set
`requiredReviewActions.targetAttributionV2AndProviderReturnSchemasReadCompletely = true` while its
`contractsReadCompletely` list carried **no entry** for
`foundation/provider-target-attribution-return.schema.v2.json`. The flag overstated what the reading
record supported. I have now read that entire file — 253 lines, all 13 `schemaKeys` including
`PROVIDER_RETURN_SCHEMA` and `TARGET_ATTRIBUTION_SCHEMA`, and all ~40 `joinKeys` — together with the
incorporated provider-return laws, the registered definitions and the affected joins. A programmatic
traversal is not a complete tool-delivered prose read, and this report keeps the two apart
everywhere.

**C-2 — evidence mislabelling.** v26's probe pB2 was described as exercising the
buffer/bind/capture/atom boundaries. It used `inspect.getsource` and `jsonschema` validation: it read
and validated source, it did not execute those boundaries. This session executed
`buffer_fact_batch_occupancy`, `bind_worker_occupancy`, `capture_occupancy`,
`project_companion_to_v2` and `AM._admit_target_attributions` for real.

**C-3 — evidence over-weighting.** v26 framed a two-record differing-digest pair as defeating
independent replay. Supplying different optional hints intentionally is *expected* to change
descriptor digests; my pair was neither a complete reminted Run demonstration nor a general
nondeterminism proof. Re-measuring every position shows the positions that still admit several
digests are exactly the ones the contract declares **meaningful** — the `fact.anchors` precedent. The
real defect was the eight positions where the contract calls the hint meaningless yet two spellings
were admissible, and 27 closes those eight.

**C-4 — citation undercount.** v26 S-3 said "the two (B11/B12) citations". There were three, and
root updated all three.

**C-5 — my probe defects this session,** all preserved in the receipts and labelled mine, never as
design faults: wrong kwargs to `buffer_fact_batch_occupancy` and a missing `diagnostic_bytes`
(TypeErrors); a fixture missing `packageManifestPath`; passing the membership wrapper where
`admit_unit_roots` takes the unit list (all nine cases wrongly refused); computing guard precedence
against a *definition* line rather than a call site (wrong `False`); selecting a 185-char `standing`
string over the 8-row `standingRules` list; and one probe invocation with the wrong flags.

## 4. The source26 issues, re-assessed against corrected bytes

**M-1 (MUST) — RESOLVED.** Both `logicalPath` schemas and the prose now exclude the hint at
`kind=unknown`, and the atom contract reads "null when `kind=package` **or `kind=unknown`**". My
exhaustive 4 kinds × 3 occupancies × 2 spellings audit finds **24/24 cells conforming**: the eight
positions the contract calls meaningless admit exactly one encoding, and the four it calls meaningful
still admit the lawful hint — the correction is not over-narrowed. Executed at all three host entries
plus retained-atom admission; every meaningless-position hint refuses.

**Route sufficiency — root's declination is correct, and my v26 suggestion was unnecessary.** I
suggested a new internal fault key. Root routed through the existing `PROVIDER_RETURN_SCHEMA` /
`TARGET_ATTRIBUTION_SCHEMA` keys instead. I executed the public derivation: the two *pre-existing*
sibling keys `TARGET_ATTRIBUTION_LOGICAL_PATH_ON_FIRST_PARTY` and `_ON_PACKAGE` are themselves
`input-schema-invalid` and reach the **identical** public termination — operational-failed,
`PROVIDER.PROTOCOL_VIOLATION`, provider-protocol, `EVALUATION.INPUT_REFUSED`. A new key would be
publicly indistinguishable from ones already there. I do not demand a key merely because I suggested
one.

**S-1 — RESOLVED.** The standing narrows to "Every **bare** 64-hex digest field", the three prose
sentences narrow the same way, and a new `x-opensip-digest-domains.scope` block publishes
machine-readable selectors (`^[0-9a-f]{64}(?![\s\S])`, `$ref: #/$defs/Hash`) plus explicit rules for
nullable branches and typed-prefix identities. Measured: **64 bare occurrences, 0 unannotated**; 63
typed-prefix occurrences, all now explicitly outside scope. The universal quantifier is true of what
it quantifies over.

**S-2 — RESOLVED.** Intent validation is scoped to the inherited-carrier path (acts A–B–C) including
a resumed migration, and the fresh-install path in `openDispatch` step 8 — including its
interrupted-install act-C resume — takes **no** `CarrierMigrationIntentV1`, with `first_generation` 1
and null migration fields. The intent domains are unchanged and no longer need a satisfying value on
a path that never constructs one.

**S-3 — RESOLVED.** 14 anchors, **0 duplicate ids**; `security-completion.v1.md` is now B14 and
`workflows-and-surfaces.md` keeps B11. Re-counted: **0** B11/B12 citations remain and **3** B14/B12
are present — three updated, one more than my v26 text described.

**A-1, A-2, A-3 — all RESOLVED.** `witnessMalformed` is now declared a read-only recovery diagnosis
that "deliberately is not a durable `carrier_quarantine.reason`"; the stale 456-case and ten-sweep
literals are replaced by derived language naming the measured report as the count authority; and a
new evidence-custody paragraph declares the scratch citations runtime-relative, states they add no
law, and distinguishes a rerun from reproduction of the original C1–C18 measurements.

## 5. The author package: F-01 … F-14

The instruction named `claude-author-package-review.v1/review.json`. **That file does not exist.**
The directory holds `review.md` (sha `398e0a1d…`) plus session metadata. The rows are spelled
**`F-01`…`F-14`** in an embedded JSON block at `$.report.findings`; all 14 were recovered complete
with severity, claim, evidence, impact and requested correction. They were raised against
candidate25 and the 97-file package, so I assessed each remedy against the 213-file successor and
snapshot27.

| Row | Disposition | How I decided it |
|---|---|---|
| **F-01** charter custody | **RESOLVED** | The charter is now inside the frozen package and its sha256 equals the F-01 pin `08dffd7f…5196e` exactly. I counted the rows myself: 123 / 8 / 3. |
| **F-02** consumer-b custody | **RESOLVED** | v6 `root-owner-assessment.v1` and v7 `root-partial-assessment.v1` are frozen in-package with an attachment manifest: **16/16 hash-match, 0 mismatch, 0 missing**. |
| **F-03** query regenerability | **RESOLVED** | The absent `blind13` import is gone; the checker now loads the query owner from **snapshot27**. I ran it: all **eight outputs regenerate byte-identical** to the shipped copies, and `assess-author-query.py` reports PASS 7. |
| **F-04** internal root spelling | **RESOLVED** | See §6 — I executed it. |
| **F-05** default-unit control | **RESOLVED** | `ts-invalid-default-entry` replays through the snapshot27 owner as structural **ADMIT** then semantic **REFUSE `ENUMERATION_BINDING_PROGRAM_ENTRY`**. |
| **F-06** two-binding construction | **PARTIAL, remainder disclosed** | The dead parameter is gone and a non-default `ts-lawful-explicit-selection` admits. The *second* binding was not built; the recorded refusals are the owner enforcing published obligations against an incomplete construction. Evidence limit, not an owner defect. AR-01 Q3 stays unanswerable from this package. |
| **F-07** combinators | **RESOLVED BY DISCLOSURE** | F-07 allowed a plain statement. README:9 gives it and I re-measured: `NotImplementedError` at both atom ops, no `and`/`or`/`not` anywhere. |
| **F-08** effective edition | **RESOLVED** | `selectedUnitIds`, `selectedUnits`, `sourceUnitOwnershipId`, `measuredBodyOwner` and `effectiveEdition` with an `editionBasis` are now published; the pre-remedy file is retained beside it and has none of them. I ran the checker: passes, asserting both the change and the stability. |
| **F-09** citation accuracy | **RESOLVED** | I checked the clause rather than the correction: `EXECUTION_INPUTS_COVERAGE_DERIVE` is raised only inside `load_coverage` and `partitions_in_cell`, and §5 is "Native Coverage accounts (derived)" while §3 is "Stage ordinal and receipts". The §5 citation is right. I reproduced the refusal. |
| **F-10** portability | **RESOLVED** | Proved by execution: all five builders ran from scratch in a fresh arbitrary directory with only `--source/--package/--out`, **no helper overlay** — which retires the remint review's own caveat that the limitation could only be retired if the overlay were merged. Every runId identical. |
| **F-11** self-comparison | **RESOLVED** | Zero occurrences of `compare_proof(proof, proof)` remain. |
| **F-12** evidence weighting | **RESOLVED** | README:9 states the per-group split; my own replay agrees, and I weight the six owner-derived Runs as determinism and self-consistency, never as two-implementation agreement. |
| **F-13** shared TCB dependency | **RESOLVED** | See §7 — I re-derived the list rather than accepting it. |
| **F-14** uniform self-assessment | **ACKNOWLEDGED** | Still 30/30 identical verdicts with 30 distinct rationales. F-14 asked for no correction, only that uniformity not be read as corroboration. I grade no row from it. |

## 6. F-04 in detail: I executed the boundary

`rootPath` is now `$ref: #/$defs/InternalUnitRootV1` — a per-segment pattern admitting the empty
string or a canonical relative dir, never `"."`. `native-evidence.md` carries a normative **U-0**
clause and documents the `workspaceRoot`-versus-`rootPath` asymmetry on both edges. A dedicated
admission fault `NATIVE_UNIT_ROOT_REPRESENTATION` names the offending root **and** its schema
selector.

Executed on snapshot27:

```
project root ""            ADMIT
rootPath "."               REFUSE  NATIVE_UNIT_ROOT_REPRESENTATION:units[0].rootPath:#/$defs/InternalUnitRootV1:'.'
rootPath "./"              REFUSE  … :'./'
rootPath "packages/a"      ADMIT
rootPath "/abs"            REFUSE
rootPath "a/../b"          REFUSE
memberPackageRoots ["."]   REFUSE  … :#/$defs/CanonicalRelativeDirV1:'.'
memberPackageRoots [""]    REFUSE  … length=0:bounds=1..4096
memberPackageRoots ["packages/a"]  ADMIT
```

The misattribution F-04 complained about is closed structurally: `_admit_membership_unit_roots` is
wired at `enumeration_model.v1.py:581` and **short-circuits** before the only `_unit_for_cell` call
(`:747`) and before every `ENUMERATION_BINDING_PROGRAM_ENTRY` raise (`:738/740/750/757`), translating
to the internal-only `ENUMERATION_MEMBERSHIP_UNIT_ROOT` with **no new public D9 route**.

One honest qualification: this remedy **predates 27** — all three owning files are unchanged in my
delta — and no reference checker exercises it. That is advisory **A-4**, not a SHOULD, because the
law itself is complete and correct and I demonstrated it directly.

## 7. The thirty evaluation residuals and TCB-SCOPE-01

All 30 rows of source27's `evaluation-residual-dispositions.proposed.json` (sha `8f7d940e…`) are read
in full and disposed individually in `review.json`, keyed by the exact ids. Binding checks I ran:
**30/30 ids match**, 0 selector mismatches, 0 evidence paths unresolved against frozen27, 0 sha
mismatches, **0 disagreements between the rows' `sourceBytesChanged` claims and my own delta**, 30/30
`PENDING`, 0 claiming `applied`, 0 reclassifying history. Of the six distinct cited documents, only
`identity-and-evidence.md` changed in 27.

**TCB-SCOPE-01 is assessed once, as one shared assumption.** It declares selected authenticated
in-process host/evaluator code trusted and adversarial code sharing that process outside the threat
model. **Rejecting or changing that one assumption reopens all thirteen dependent accounts together —
it would never be thirteen independent successes.**

I did not take the declared list on trust. I classified all 30 rows myself; a keyword pass returned
**14** and disagreed on three. Reading those three in full: `RES-EP13-13` *does* belong (its
disposition is "fixture isolation only, no process isolation against hostile Python"), while
`IR-EP13-NB-02` and `IR-EP13-NB-06` do *not* — their dispositions ("a grep is not a structural
guarantee"; "a parity rule imposes cost without closing the class") hold wherever the boundary is
drawn, and my classifier had matched a shared evidence-scope *label* rather than their reasoning.
**Read row by row, the declared 13 is exactly right.**

As design the assumption is coherent, disclosed and consistently applied, and
`admission-and-qualification.md` states it explicitly rather than leaving it implicit. I do not grade
it. An authenticated pure host/evaluator consuming inert typed data is what the bytes describe: I
claim **no same-process hostile-code containment, no qualified provider isolation, and no measured
compiler, OS or crypto enforcement.**

## 8. Evidence I generated, and how I weight it

The seven exact exports were re-executed through **both** boundaries with my own store decoder and
the snapshot27 owner — the package's checkers were not imported:

- 7 positives — structural custody **ADMIT**, complete semantic replay **ADMIT**
- 3 false-result controls — structural **ADMIT**, then replay **REFUSE `EVALUATOR_COMPLETE_PROOF_REPLAY`**
- binding controls — invalid-default **REFUSED**; lawful-default and single-explicit **ADMITTED**

I also built everything from scratch in a fresh arbitrary directory. Fresh exports differ from
shipped by exactly **one unreferenced retained blob per store** — the
`target-attribution.schema.v2.json` document itself, which changed in 27 — which I proved inert by
mutual replay: each build passes `close_run` while lacking the other's copy, with identical
objectTable, frames, meta and RunIds. **I repaired no input export.**

On weighting, candidly: these are **AUTHOR-assisted** oracles, never a blind reconstruction. One Run
is an author-helper composition compared with the frozen owner; **six are frozen-owner derivations
replayed by that same owner** — determinism and self-consistency, not two-implementation agreement.
`and`/`or`/`not` remain unexercised, `count-at-most`/`all-covered` unimplemented, and the two-binding
experiment incomplete. Missing author controls limit evidence; they are not by themselves a
demonstrated normative defect. I graded no row from author self-assessment and treated no expected
output as correctness evidence.

Reference execution on 27: the source-pinned evaluator3 launcher validates **1242 pins, 0 changed or
missing, 16/16 children exit 0**, and every remaining contract and reference group passes with **0
frozen-snapshot deviations**.

The 123/8/3 charter handoff verifies as **123 / 8 / 3 with ids identical to the frozen charter, 123
PENDING, `independentAcceptance: false`, 0 waiver tokens**. The separate blind test remains required
and uninfluenced: I did not read or touch the blind consumer work at any point.

## 9. Advisories (no MUST, no SHOULD)

- **A-4** — the internal-root guard is exercised by **0 of 27** reference checkers. Not a SHOULD: the
  law is complete and I demonstrated it by execution, and the three owning files are unchanged in
  this delta, so it is neither a regression here nor something I should raise as blocking against a
  delta that did not touch it. An application reviewer may reasonably elevate it.
- **A-5** — `AX6`, `AX9`, `MD5` and `RX2c` preserve neither an inline original nor a title, and both
  cited source artifacts have **0 occurrences** in the 12,893 files of frozen27 (19 rows keep a full
  inline original; 7 keep a title). Their dispositions are assessable on their own terms and all four
  correctly claim nothing, so this limits evidence rather than showing a defect — the same custody
  shape F-01 and F-02 already fixed for the charter.
- **A-6** — the regenerated query checks are not wired into `verify-package.py`. Author-package
  convenience only; F-03's actual impact is eliminated because I regenerated them myself.

## 10. What this review does not do

All five owner routes carry `appliedByThisReview=false` and `finalApplicationOutcomeGranted=false`.
**All 28** condition-2 obligations are retained OPEN. **All 32** qualification gates are unperformed
and **condition 5 is NOT MET**. **All 54** commit-recovery cases remain unexecuted product
obligations. DR-007 and DR-011-R08 keep the successor D9 artifact carrying host-invariant as a
disclosed, attributed implementation obligation, carried forward and not closed.

No grade, no activation, no blind acceptance, no implementation authorization. The final separate
application review must still grade the 30 evaluation residuals and the 28 condition-2 obligations.

---

*Full machine-readable dispositions — 30 evaluation residuals, 16 AR, 15 FW, 27 inherited residual, 5
scoped owner routes and 14 F rows, each with its own reason — are in `review.json`. Every probe,
including the ones that failed on my own errors, is preserved under `receipts/`.*
