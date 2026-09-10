# bv5-corrections-author.v2 — correction handoff

**Role.** Correction coauthor (actual Claude), follow-up turn. Not an independent reviewer, not an
accepting reviewer. **Technical assent: true**, to the exact bytes in §1 and to nothing else. No
product qualification, no implementation authorization, no readiness change, no independence, no
blind acceptance.

**Responds to.** `root-input/root-assessment.json` (finalSourceAssent **false**),
`root-input/bv5-draft-root-feedback.v1.md` (8 points), the full-Run diagnostic
`root-input/bv5-rc1-full-run-result.v1.json` and its probe, plus `CODEX-PUBLIC-NOTE.md`, which added
**CX-BV5-09**, the **CX-BV5-08 retained-scope completion**, the **CX-BV5-01 follow-through** and
three wording-precision items. `assessment.md` answers the feedback point by point and records
honestly that it was written *after* the corrections, not before.

**Scope.** Only `/tmp/opensip-design-corrections/bv5-corrections-author.v2` was written. The
released v1 output, the live repo, frozen subjects, historical reports and evidence were read only.

**I reproduced root's evidence before changing anything.** `root-input/probe-bv5-rc1-full-run.py`
run on my work copy produced *identical* runIds to root's result — all four cases ADMIT
(`evidence/root-probe-reproduced-before.json`). My v1 prose therefore contradicted the reference
admission on three counts, and root's criticism of my own cross-rung probe is correct: it used
`unresolved-edge@resolved-binding`, which only exercises the resolved-rung not-applicable refusal
and cannot establish relation-specific membership at all.

---

## 1. Exact final source

### Aggregate delta vs frozen v15 — 11 files

| Path | frozen v15 SHA-256 | final SHA-256 | bytes | first changed |
|---|---|---|---|---|
| `docs/coop/design-corrections/foundation/identity-model.py` | `fe301a101ee3d05ecfd51338a46ae6a9fcc115478358a00482e239dc83f4816d` | `66d8bd5a824479d4190202cb17c8531014aec36a434f02fd8ad67630ebc36b32` | 120278 | v2 |
| `docs/coop/design-corrections/foundation/identity-schemas.v2.json` | `f127fb117c3f3526fa6fad62a63e203a75e510fc7950f8e3dfd5b736d614e287` | `76ef8912015e468513135352574ed7a1ac7426cd06af669d5ddf3f14f516cf8b` | 131612 | v1 |
| `docs/coop/design-corrections/native/capability-manifest-domains.v2.json` | `939626cf8533c53cdebfa6421ceb89b9ca6128e3deb841b8a1f6070e0f8e4582` | `1456ae1476dfe1b0f3b1134c9d7a36e35890e45e20f57e7bbc2b7ada2144aef6` | 16522 | v1 |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `9ef09ab70c280d63d390fcafef1254d74504fa12d3839823518a1cf111099602` | `2a5fc49339fbeb65d2dfdadcd062054e7e514924e23e16c82a4e84338092cc0f` | 204072 | v1 |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | `3619accb0b190586cabd9fdcca41c9f4db981862d13ff2dd7953f5bf65a6566d` | `8301e8e3518f2bc75e4193852d106d8fa00ef6b2a35019cb6cbaefc317447b18` | 260349 | v1 |
| `docs/coop/design-corrections/workflows/schemas/repair.schema.json` | `9188163012b57421b13ff0155c51270250f2f19c782da0875711db75a30137ef` | `b8fe3464f2475307f3059132c3c15461a3bb043ea7dfd5e6e98dfd63a8f8dc3d` | 26142 | v1 |
| `docs/coop/design-corrections/workflows/workflow-cases.v1.json` | `365707e6916bf33c78d9e77c4f6726fa2824307c5ab84fea0a13e92ec481288b` | `688506e60b2aa57025b453d1a2642c875ffe5539f47b948c36d81023bb0ec93a` | 236539 | v2 |
| `docs/coop/design-corrections/workflows/workflows_model.v1.py` | `4b4dc9ed823674273ba3285a6bfcc56fc4499ad3b821cd0446c4ebcf137d8106` | `8d45d1156f72b9ab5a8ce1859a5a4281af5203ca04ea59b4e81681ca5a99793b` | 112744 | v1 |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `751de4d460aabcd5bb7f7b163d9286a40d6605e0ab53060a19cc9d7eb1a12407` | `64a2a019d6aa94177f59ca0b2cbd380f7e89f3aa3682707b82f50166c72fb8b3` | 102837 | v1 |
| `docs/v2/contracts/product-v1/native-evidence.md` | `706b7e0fc94bb1467e33c9f75d5406046e32ab9859f57f08a1f6642dfbdc7d46` | `b50c814c4cc3335bec166190fd4468742429b11e2b014fba64eab7a6acbd3fea` | 229045 | v1 |
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | `80dcc7474d7202b631194be9c4dc07828c5d507a5c9fd1e961a76f9dcfbc2abc` | `4a5f0c4edb1eb80d49c548c91e1a7bdc47093b9edf79b43c99e8e19a2e263742` | 71910 | v1 |

### This turn's delta vs released v1 — 10 files

| Path | released v1 SHA-256 | final SHA-256 | bytes |
|---|---|---|---|
| `docs/coop/design-corrections/foundation/identity-model.py` | `fe301a101ee3d05ecfd51338a46ae6a9fcc115478358a00482e239dc83f4816d` | `66d8bd5a824479d4190202cb17c8531014aec36a434f02fd8ad67630ebc36b32` | 120278 |
| `docs/coop/design-corrections/foundation/identity-schemas.v2.json` | `4e06e1869f0702f720a960e93390be38363fd2a622475fcd08cac1d6f8284a9d` | `76ef8912015e468513135352574ed7a1ac7426cd06af669d5ddf3f14f516cf8b` | 131612 |
| `docs/coop/design-corrections/native/capability-manifest-domains.v2.json` | `088e2fd256681d238502d84092b48b67b89cb5fed0d7dc16d43223a30680b866` | `1456ae1476dfe1b0f3b1134c9d7a36e35890e45e20f57e7bbc2b7ada2144aef6` | 16522 |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `7738c372ec7e3d5dbf3766340839d2352f03e0b086d52b2056796dcc24e04508` | `2a5fc49339fbeb65d2dfdadcd062054e7e514924e23e16c82a4e84338092cc0f` | 204072 |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | `9ad4e2682fbc8294666ec9984ded5651ea46718a4b1d352dcba720785fd1e439` | `8301e8e3518f2bc75e4193852d106d8fa00ef6b2a35019cb6cbaefc317447b18` | 260349 |
| `docs/coop/design-corrections/workflows/schemas/repair.schema.json` | `797f06565223363c0c2b29bb89e9f9eed49e8c8d5ac1ececb090bb1c2172d456` | `b8fe3464f2475307f3059132c3c15461a3bb043ea7dfd5e6e98dfd63a8f8dc3d` | 26142 |
| `docs/coop/design-corrections/workflows/workflow-cases.v1.json` | `365707e6916bf33c78d9e77c4f6726fa2824307c5ab84fea0a13e92ec481288b` | `688506e60b2aa57025b453d1a2642c875ffe5539f47b948c36d81023bb0ec93a` | 236539 |
| `docs/coop/design-corrections/workflows/workflows_model.v1.py` | `3b302d7d63b8976cb9dec448db20ec24f8c60f18ac7364d0d278fca6a22adfe5` | `8d45d1156f72b9ab5a8ce1859a5a4281af5203ca04ea59b4e81681ca5a99793b` | 112744 |
| `docs/v2/contracts/product-v1/native-evidence.md` | `db1d427e146613132f4d045731617af19efa2cb03a853c663ff3d4c7b06005f0` | `b50c814c4cc3335bec166190fd4468742429b11e2b014fba64eab7a6acbd3fea` | 229045 |
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | `1545b36e65c1e1d6a103c3f82659b7f44a34fec9fe653f536de0eef6639c14fa` | `4a5f0c4edb1eb80d49c548c91e1a7bdc47093b9edf79b43c99e8e19a2e263742` | 71910 |

`docs/v2/contracts/product-v1/identity-and-evidence.md` is the one v1-corrected file **untouched**
this turn. Before-images for both baselines are under `before-images/frozen-v15/` and
`before-images/released-v1/`; unified diffs are `vs-frozen-v15.diff` and `this-turn.diff`.

Two files are new in the delta this turn: `foundation/identity-model.py` (retained-scope membership
at closure) and `workflows/workflow-cases.v1.json` (the fixture's seventh closed-world member).

---

## 2. The two MUST corrections are in the admission, not only in prose

Root's central point was that my v1 wording *mandated* a law the reference did not enforce. That is
now fixed at the code, and at every boundary a Coverage entry or scope can reach:

| Site | What it now enforces |
|---|---|
| `coverage_bijection` (RC-0, runs first) | the entry's `(relation, rung)` must be a **registered pair** — the rung a member of *that relation's* own ladder |
| `coverage_bijection` (RC-1) | on a non-resolved rung: `state=not-applicable`, `attempted=false`, count `0`, class list **empty** |
| `coverage_bijection` (RC-2) | `complete` and `not-attempted` now also require an **empty class list** (CX-BV5-09) |
| `admit_coverage_result_v3` | the producer boundary, via the above |
| `open_run_closure` | retained closure re-runs that same admission — so nothing contradictory can be minted *or* carried into a sealed Run |
| `subject_scope_descriptor` | refuses a non-registered pair at mint |
| `open_run_closure` (new) | **every retained scope a view names**, independent of whether a Coverage wrapper or a fact exists |

The last row is the CODEX-PUBLIC-NOTE completion: a constructor guard cannot see retained bytes that
never went through the constructor, and a scope with no Coverage reaches no other check.

**Measured, on full retained Run closures through the shared integration fixture:**

| Case | before | after |
|---|---|---|
| `unresolved-edge@observed`, valid | ADMIT | **ADMIT** (unchanged) |
| `unresolved-edge@enumerated` | ADMIT | REFUSE — producer *and* closure |
| `observed` with `attempted=true` | ADMIT | REFUSE — producer *and* closure |
| `observed` with a registered class beside count 0 | ADMIT | REFUSE — producer *and* closure |
| **fact-free** `enumerated` (empty examined scope) | — | REFUSE |
| **fact-free** `observed` | — | ADMIT |
| retained scope, **no Coverage wrapper**, `enumerated` | ADMIT | REFUSE |
| retained scope, **no Coverage wrapper**, `observed` | ADMIT | **ADMIT** (unchanged) |
| `complete` + count 0 + `[computed-member-access]` | ADMIT | REFUSE (CX-BV5-09) |

**What was deliberately not weakened**, each with its own control: all **17** registered pairs still
admit (swept through the producer boundary); the five resolved rungs still refuse `not-applicable`;
RC-2 still refuses `complete` over a non-complete stage; `stageTerminal` stays free on a
not-applicable entry (`complete`, `budget-exhausted` and `null` all admit); `examinedExhaustive`
stays independent; and an honest `incomplete` observation still carries its classes and admits.
`incomplete`/`partial` were not touched at all — they already required exact count *and* class
equality, and nothing here converts an honest partial observation into a completeness claim.

---

## 3. The Unicode fold: named, and the binding made effective

Root's measurement is exact and I reproduced it on UCD 15.0.0. `str.lower()` is **full**,
**context-sensitive**, **non-tailored** default lowercase — not simple lowercase, not casefold:

| Input | `fold` (published) | simple lowercase | case folding |
|---|---|---|---|
| `U+0130` | `U+0069 U+0307` (two code points) | `U+0069` | `U+0069 U+0307` |
| `U+039F U+03A3` (final sigma) | `U+03BF U+03C2` | `U+03BF U+03C3` | `U+03BF U+03C3` |
| `U+03A3 U+039F` (not final) | `U+03C3 U+03BF` | `U+03C3 U+03BF` | `U+03C3 U+03BF` |
| `U+00DF` | `U+00DF` | `U+00DF` | `U+0073 U+0073` |

`lib_name_fold` now names the operation once and is used at all three former `.lower()` sites.

**The follow-through matters more than the naming.** A declared version that nothing consults, beside
a `.lower()` that silently uses whatever the runtime ships, is a determinism claim with no mechanism.
So the fold **gates**: if the running case data is not `UNICODE_CASE_DATA_VERSION`, it refuses to
produce a result at all, raising a **`ReferenceEnvironmentError`** — a new type that is deliberately
**not** an `AdmissionError`, so different Unicode data can never be laundered into an ordinary
refusal about a caller's `lib` selection.

**The cost, stated rather than hidden:** this reference derivation now runs only where the declared
case data is present. That is a real portability restriction. I judged it the right trade, and both
the prose and the docstring say so. Nothing was narrowed to ASCII, no locale parameter was added, and
the accepted `libSelection` value set is unchanged — it is simply *true* that the pinned compiler's
own `lib` vocabulary is ASCII, where all three operations coincide, and that is a fact about the
vocabulary, not a constraint on the field. The TypeScript context identity is unchanged
(`sha256:8ddb7934…`), so naming the fold changed no admitted outcome.

---

## 4. The remaining root points

* **CX-BV5-02.** Step 1 refuses **only** an actual over-bound array, so a missing field, `null`, a
  boolean, a number, a string, an object, and an in-bound array malformed some other way all reach
  the schema step — each measured. And the two routes are **not** the same public termination: the
  cardinality refusal is origin-independent `request-rejected` (2), while the schema refusal keeps
  §10's origin-dependent routing, including **`operational-failed` (4)** /
  `SYSTEM.OUTCOME.ILLEGAL_STATE` with `faultCause: host-invariant` for a host-generated invalid spec.
  Corrected in the prose **and** in the `admit_analysis_spec` docstring.
* **CX-BV5-03.** The guard is **every** `delete` and **every** `replace` — my v1 "replace of an
  exported subject" narrowed a live guard, and delete-only and replace-only plans are now each shown
  guarded while create-only is not. `dynamicDispatch` is target-relative via §4.5 `affected_targets`
  and §4.6, **not** a global veto: measured, `dynamicDispatch=present` alone does not veto an
  otherwise eligible unsafe repair. Per CODEX-PUBLIC-NOTE, `admit_atom` is now described as
  *vocabulary admission* with `sufficiency_v2` and the affected-target evidence owning semantic
  sufficiency, and the "later verification re-reads" claim is replaced with what `repair verify`
  actually does — it seals a **new** Run over the freshly re-snapshotted tree.
* **CX-BV5-05.** Three distinct enforcements, named: two direct `$ref` sites carry the full grammar
  including the per-segment 255 bound; `fact.anchors[].path` additionally has a real snapshot join;
  `finding-fingerprint.subjectKey.logicalPath` has the imperative `ordered()` check and **no**
  snapshot join and **no** 255 bound. Measured: `ordered()` admits a 300-character segment and
  refuses a dot-dot segment. The unsupported "previously enforced for scope-descriptor alone" history
  is removed. No accepted path set changed.
* **CX-BV5-06.** The Windows citation now names security **S8** (the one machine platform vocabulary,
  and where Windows is excluded) and the native matrix `platformFamilies`. The blind review's
  citation is retained only as explicit history; its own bytes are untouched.
* **CX-BV5-07.** RC-1 now states a **determinacy gap** — RC-1 as written refused neither candidate,
  so two conforming implementations could commit different records — and says explicitly that this is
  **not** a digest collision and not a divergence over byte-identical observations, because
  `complete` and `not-attempted` necessarily differ in `attempted` too.

---

## 5. My own v1 new findings

* **BV5A-NEW-1** — **fixed**, not deferred. My v1 scoping was wrong: a contradictory Coverage entry
  closing a sealed Run is not an advisory, and root's full-Run counterexample settles it.
* **BV5A-NEW-2** — addressed proportionately. I accept root's distinction: a workflow helper
  consuming an already-admitted native record is **not** thereby a product host failure, so I added
  no re-validation call on that basis. But the contradiction *was* real and a limitation note would
  have hidden it — both reference fixture records carried six members against a normative
  seven-member record. Both now carry `dynamicDispatch`, and the helper docstring states the
  admitted-input assumption.
* **BV5A-NEW-3** — restated with its limit: the `DOM`/`ES2022` fixture substantiates the *mapping*
  and says nothing about simple-versus-full conversion; CX-BV5-01 is what settles that.

---

## 6. The thing to check hardest: reference Run identities moved

The shared fixture's baseline goes `4e83d795…` (frozen v15) → `e7abd2f4…` (released v1) →
`ca67ad74…` (now). I did not want to assert this was benign, so I attributed it by experiment: the
final v2 tree with **only** `native-evidence.schemas.v2.json` reverted to its v1 bytes — every
behavioural edit still in place — reproduces the v1 baselines **exactly** (`e7abd2f4…` and
`c3117646…`).

So the whole movement is the digest law working as designed: a Coverage `payloadSchemaDigest` is the
raw SHA-256 of that schema document's bytes, so any edit to it, even a description, moves every
`coverage2` and therefore the Run. **None** of it comes from the admission or closure changes.
Evidence: `evidence/run-identity-attribution.json`, `disposable/identity-attribution.v1/`.

---

## 7. Commands, results, disposable roots

Three probes, all passing, each driven through host entry points on full graphs where the claim needs
one:

| Probe | Entry points | Checks |
|---|---|---|
| `probes/probe_coverage_pair_and_na_law.py` | `admit_coverage_result_v3`, `close_run`, `subject_scope_descriptor` | 28 |
| `probes/probe_lib_fold_operation.py` | `lib_name_fold`, `admit_native_context` | 23 |
| `probes/probe_repair_guard_and_prose.py` | `repair_preview`, `admit_analysis_spec`, `ordered`, schema closure | 39 |

Those are **check rows, not a coverage claim**: the coverage probe additionally reports 8 full-Run
closures and a 17-pair producer sweep as data, and the 28 checks are the assertions over them.

Root's three probes re-run on the final source: the full-Run probe now refuses all three defects
while `valid-observed` still closes; `probe-bv5-resolved-classes.py` refuses the contradiction and
admits the valid control; `probe-bv5-scope-membership.py` refuses `enumerated` and still admits
`observed`.

**Preserved failed attempts.** Both probes failed on first run, both from **probe defects, not design
failures**, and both attempts and outputs are retained under `evidence/`: the coverage probe
discarded the producer result when `close_run` raised inside the same `row.update()`; the prose probe
asserted raw substrings against hard-wrapped Markdown (so `digest collision` spanned a line break)
and forbade a string that legitimately survives inside the historical parenthetical.

**One full checker run on the final bytes**, in `disposable/final-checks.v1` (repinned locally only):
native **347/347**, foundation **pass** (1099 files), workflows **pass** (65 files), security
**456/456**, integration **365 passed, 0 failed**. Logs under `disposable/logs/`.

Disposable roots, all under this output directory: `disposable/interim-regression.v1`,
`disposable/final-checks.v1`, `disposable/v15-baseline.v1` (pristine v15, verified 0 mismatches
against the manifest), `disposable/identity-attribution.v1`. The baseline-identity measurement
script is `probes/baseline_run_identity.py`.

**Write custody.** Everything is under this output directory. The released v1 output, the live repo,
frozen subjects and historical evidence were read only; the frozen v15 archive was read to extract a
pristine baseline *into* `disposable/v15-baseline.v1`. Disclosed: three scratch files were briefly
written to `/tmp` during the run (the baseline script and two Markdown table fragments); the script
is retained under `probes/` and all three were deleted.

---

## 8. Not done, and limitations

* Source pins in `work/` are stale by construction — root/Codex refresh them after final records, and
  root runs the six final pinned checks. No published pin, generated report, readiness record,
  crosswalk or disposition file was edited in `work/`.
* Nothing here is product qualification. Every measurement is over reference models and synthetic
  fixtures; no compiler, cargo, provider, repository, ledger or renderer ran, though real Python and
  shell IO did. Where a control "refuses", that is a reference model applying a stated rule.
* This assent is substantive but **not** independent, and confers no readiness, acceptance or blind
  approval.
* **Correcting two statements in my own v1 reporting** that root flagged: v1 said "two schema files
  changed" when the delta carries three schema bundles (identity, native, repair) — this turn's
  counts come from the exact source inventory; and v1's all-writes-under-output sentence was
  qualified by its own transient-scratch disclosure, so this turn every artefact, log and extracted
  baseline lives inside this output directory.
* The assessment file was written after the corrections, not before, and says so in its first
  paragraph.

**No whole-tree acceptance is claimed.** The proposed bytes are exactly the 11 files in §1.
