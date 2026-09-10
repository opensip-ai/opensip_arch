# Fresh independent review — frozen candidate v10

**Verdict: CHANGES_REQUIRED** — zero MUST, **one SHOULD (v10-S1)**, three advisories.

`subject.manifestSha256 = 82c1be11d3b61908b2a45ebb6e59e71bb5cb31d8450a96a61857ced430e786fd`

Reviewer: actual Claude, fresh independent session. I authored none of these bytes and am neither
coauthor `5dec928a-6357-4726-9ea8-49a3079fb726` nor prior independent reviewer
`93403103-b133-4d69-8700-627712411137`. Every handoff, custody record, technical review and prior
review was read as an **assertion to test**, not as a result to adopt.

This is not acceptance, readiness, application, blind reconstructability, Codex assent or product
qualification, and it authorizes no implementation, commit or push.

---

## 1. The short version

The prior finding **v9-S1 is genuinely resolved**, and I confirmed it by the strongest available
means: re-running the v9 reviewer's exact experiment against **both real frozen source images**.
With a byte-identical relation document, v9 admitted 39 of 39 injected unannotated governed fields;
v10 refuses 39 of 39 at the intended cause. The three-limb unification that root's v8 counterexample
demanded is sound across all supported annotation locations. All six reference commands reproduce
with byte-identical logs and byte-identical regenerated reports. No normative contract, schema or
registry byte changed, and nothing was removed.

But the traversal that resolves v9-S1 carries a **residual order dependence of the same class root
found in the draft**. `record()` states in its own docstring that admissibility cannot depend on
branch order; in one of the two orders it can, and an unannotated governed field is admitted. I
reached this behaviorally, including with a document that differs from a refusing one **only in JSON
key order**.

The gate is strict, so this is CHANGES_REQUIRED. It is a narrow, well-bounded finding — no shipped
byte, identity, count or Run is affected — but it is the same kind of finding, with the same
"two conforming implementations would disagree" rationale, that made v9-S1 and v8-S1 SHOULDs and was
corrected in both cases. Downgrading it to a nonblocking advisory to reach ACCEPT would be exactly
the move this gate forbids.

---

## 2. Custody, before and after

I verified the manifest and every declared file twice — before touching anything and again after all
probes — and the two verifications are byte-for-byte the same object.

| Check | Before | After |
|---|---|---|
| Manifest sha256 matches instruction | yes | yes |
| Declared files verified (digest **and** length) | 2502 / 2502 | 2502 / 2502 |
| Missing / digest mismatches / length mismatches | 0 / 0 / 0 | 0 / 0 / 0 |
| **Undeclared files** under the snapshot root | 0 | 0 |
| Symlinks or non-regular entries | 0 | 0 |
| `totalBytes` reconciles (62,909,767) | yes | yes |

Independently recomputed and confirmed:

- predecessor manifest `288ac214…` — matches both the instruction and v10's own claim;
- v9 review `13b4a471…` — matches, and the file is retained unchanged;
- original user v1 manifest `e7403b70…`, 1192 files;
- the 31 protected historical files, all unchanged (`openingSha256 == currentSha256 == recomputed`).

I wrote only under `/tmp/opensip-design-corrections/post-reset-review.v10`, ran no subagents, made no
source edit, and ran no commit, push, reset, checkout or clean. Reports were never regenerated inside
the frozen source; every execution ran against a disposable copy I first proved byte-identical.

> **Harness error I corrected.** My first pass checked the 31 protected files *against the frozen
> subject* and reported 21 missing. That was my mistake: the frozen subject is a **scoped** 2502-file
> snapshot that contains only 10 of them. The correct oracle is the live repository, where all 31
> verify unchanged. I record this as a corrected assumption, not as a subject defect.

---

## 3. The exact delta

Recomputed from the two manifests: **214 added, 0 removed, 15 changed.**

Only two of the changed files are implementation:

| File | v9 → v10 |
|---|---|
| `foundation/identity-model.py` | `1a563aa1…` → `f200232b…` |
| `foundation/check-identity.py` | `d07cfe7f…` → `a7f7d393…` |

The other thirteen are generated reports, four source-pin sets, the crosswalk, the README, the resume
guide and the validation summary. Every pin diff is exactly the repin of those changed inputs — no
historical repin, no unexplained churn.

**The authors' claim that current normative contracts, schemas and registry bytes are unchanged is
true.** I classified 244 normative-ish files and checked the schema/registry set explicitly: zero
changed. Zero files under `docs/v2/` or `docs/catalog/` changed. Nothing was removed.

---

## 4. Reproducing the six reference commands

I ran `run-final-v10.py` against my own verified copy. All six exit zero.

| Command | Result | Log vs frozen |
|---|---|---|
| foundation | 1009 = 231+661+24+28+65; 1099 pins | **byte-identical** |
| security | 456 cases + 10 invariant sweeps | **byte-identical** |
| native | 151/151; 60 cells; **0 qualified** | **byte-identical** |
| workflows | 1290 | **byte-identical** |
| workflow-surface | 1290 | **byte-identical** |
| integration | 363 | **byte-identical** |

After the run, **0 files in the tree differ from frozen and 0 new files were created** — the
regenerated in-tree reports are byte-identical to the frozen ones, and mtimes confirm they were
genuinely rewritten rather than skipped. The validation summary's arithmetic reconciles against the
executed reports.

**Pins authenticate transitive inputs.** I appended a single comment line to `identity-model.py` — a
transitive import, not the entry script — in a throwaway copy. Result: `sourcePinsValid: false`, the
file named in `changedOrMissing`, `checksExecuted: false`, **exit code 1**.

---

## 5. v9-S1 — resolved, and how I know

v9-S1 was that the residue law declares three inadmissible conditions and only two were consumed.
`relation_annotation_closure` built its working set *from* the annotations, so an unannotated field
was invisible by construction. v10 inverts the direction with a schema traversal.

I did not rely on a neutralisation stub — the author's own stub failed and is honestly retained as
such. Instead I loaded **both real frozen source images** and ran identical inputs:

| Experiment | v9 image | v10 image |
|---|---|---|
| 39 injections (13 relations × 3 governed forms) | **ADMIT 39/39** | **REFUSE 39/39** at `RELATION_DIGEST_UNANNOTATED` |
| The relation document itself | byte-identical across both | byte-identical across both |
| Shipped document, all 13 relations | ADMIT | ADMIT |
| The authored check's own assertion, on a document carrying an unannotated `CanonicalPath` | still evaluated **True** | now **refuses** |

Coverage beyond the original experiment, all refusing at the intended cause:

- 39/39 inline-`pattern` injections (copying the pattern instead of referencing it);
- 39/39 transitive alias `$ref` injections;
- 15/15 nested, array, nullable-`oneOf`, `additionalProperties` and array-of-object shapes;
- 7/7 removals of the existing shipped annotations.

And the refusals are **discriminating**, not blanket:

- 39/39 lawful annotated `not-joined` controls still ADMIT;
- 13/13 non-governed unannotated fields (`integer`, plain `string`) still ADMIT;
- `vcs-change.previousPath` keeps its declared not-joined exemption.

**Three-limb consistency** (root's v8 counterexample class) is closed. A 12-cell matrix — three
effective annotation locations × four cases — behaves identically across all locations with the exact
intended causes:

| | field-local | intermediate alias | branch parent |
|---|---|---|---|
| lawful `not-joined` | ADMIT | ADMIT | ADMIT |
| invalid retention | `RELATION_DIGEST_RETENTION` | same | same |
| annotated, no join | `RELATION_DIGEST_LAW_RESIDUE` | same | same |
| unannotated | `RELATION_DIGEST_UNANNOTATED` | same | same |

Also verified: an annotation on the **terminal** governed `$def` is *not* a blanket exemption;
disagreeing annotations refuse rather than acquiring an invented precedence; identical annotations are
lawful; and an unjoinable nested/array location must declare `not-joined` rather than claim a join the
vocabulary cannot reach.

---

## 6. v10-S1 — the new SHOULD

### What the code says it does

```python
def record(path, form, field, joinable, annotations):
    """One sighting. Never let an annotated sighting erase an unannotated one at the same path -
    ... so admissibility cannot depend on branch order."""
    previous = seen.get(path)
    if previous is not None:
        ...
        annotations = previous['annotations'] + [a for a in annotations if a not in previous['annotations']]
        if not previous['annotations'] or not annotations: annotations = []
```

`annotations` is **rebound to the merged list** on the line above the test. So `not annotations` can
only be true when both sides were already empty — a no-op. The effective rule collapses to *poison iff
the **first-recorded** sighting was unannotated*, which is a branch-order dependence, not order
independence.

### What it actually does

I did not argue from source. Two metaschema-valid draft-2020-12 documents, controls included:

**Case A** — a node carrying both a `$ref` to a container `$def` and a sibling `properties`
refinement (idiomatic in 2020-12, where `$ref` has siblings; the walker deliberately follows the
`$ref` first and then the node's own keywords). Both land on the same path.

| Arrangement | Verdict |
|---|---|
| container leaf unannotated, sibling annotated | **REFUSE** `RELATION_DIGEST_UNANNOTATED:file:file.probe.leaf:DigestHex` |
| container leaf annotated, sibling unannotated | **ADMIT** |

**Case B** — `items` and `additionalProperties` on one node both map to `path + '[]'`. The two
documents contain the **identical pair of subschemas** and differ *only in which JSON key is written
first*.

| Arrangement | Verdict |
|---|---|
| `items` (unannotated) written first | **REFUSE** `RELATION_DIGEST_UNANNOTATED:file:file.probe[]:DigestHex` |
| `additionalProperties` (annotated) written first | **ADMIT** |

Positive controls, all as declared: the unmodified shipped document ADMITs; a single unannotated leaf
behind a container `$ref` REFUSEs; a single lawful annotated leaf behind a container `$ref` ADMITs.
All hypothetical documents pass `Draft202012Validator.check_schema`.

### Why this was not caught

I instrumented `record()` in a throwaway copy to log every same-path collision and ran the **full
authored suite**:

- collisions during all 661 authored checks, including all 59 new annotation checks: **0**
- collisions during my counterexample: **2**, logged as
  `('file.probe[]', False, True)` → REFUSE and `('file.probe[]', True, False)` → ADMIT.

Root's original counterexample was fixed **structurally**, by giving each `oneOf` branch its own path
suffix. That removed the collision rather than exercising the merge. So the authored check literally
named `branch-order-does-not-decide-admissibility`, and all four retained root rechecks, pass without
ever reaching the code that carries the order-independence claim.

### Why it is a SHOULD

The declared law — not merely a docstring — states *"There is no default and no residue: a new such
field added without an annotation is inadmissible"*, and `residueRule` names an unannotated
digest/path field as inadmissible. In cases A and B such a field is present and is **admitted**. An
implementer building from the law, or from `record()`'s stated rule, would implement order
independence; the reference does not, so two conforming implementations would disagree on
admissibility. That is precisely the rationale that made v9-S1 and v8-S1 SHOULDs, both of which were
accepted and corrected.

### Scope — deliberately bounded

This is a **hypothetical registered schema edit only**, exactly like v9-S1, and **not** a current
payload or Run attack. Measured, not asserted:

- the shipped document has 7 governed sightings, all annotated, all at **distinct paths** — no
  shipped relation can collide;
- `relation-payload-schemas.v2.json` is pinned in **all four** pin sets with matching digests, and pin
  drift is a hard exit-1 failure;
- both `relation_digest_annotation_coverage` and `relation_annotation_closure` are **pure schema-only**
  functions — no file I/O, no snapshot, Run, cache or memo reference — so owning-Run admission and the
  payload decode memo are untouched, consistent with the law's own `enforcement` text.

I propose no patch text and made no source edit. The direction is to test the *incoming* annotations
before rebinding, so a sighting is uncovered if **either** side was unannotated, and to add an authored
check that actually reaches the merge.

---

## 7. Preservation of what v9 confirmed

I used the exact diff plus targeted probes rather than re-deriving every v9 confirmation.

- **Identity checks:** 602 → 661. Zero removed, zero shared ids with a changed result, 59 added, all
  passing. Every previously confirmed identity assertion is byte-identically present.
- **Byte-identical across the delta:** `integration-report.v1.json` (363),
  `native/native-evidence-report.v2.json` (151 cases, 60 cells, 0 qualified),
  `security/security-lifecycle-report.v1.json` (456 + 10). A report identical across the delta cannot
  contain a changed identity, count or verdict.
- **Recomputed on both source images and stable:** frame prefix, domain prefix table, framed body
  identities (TypeScript, JavaScript-through-the-TS-engine, Rust, empty and Unicode bodies),
  `identifier()` across every registered domain, and admission of all 13 shipped relations.

The long list of v9-confirmed behaviours — own-snapshot file joins, owner-specific admission outside
the payload decode memo, complete `file@enumerated` Coverage with non-applicable resolution, the 13
registered relations, body grammar and level-specification custody, L0 recomputation versus L1–L3
custody/framing only, raw32 compiler/dialect body version, JavaScript through the TypeScript engine,
target-specific Rust edition and shared-path selection, `#paths`/maxsizes/`derivedUnitIdentity`, stable
body ids under unrelated ownership changes, empty-view Coverage prerequisites preserving honest partial
and healthy empty results, all four CVE1 gates, native Coverage producer admission, Plan enumerator
membership, TS custom config and ordered repeated `extends`/jsconfig provenance, typed array order
separate from canonical encoding, cache lookup versus hit validation, workflow required-output failure
and Run preservation, the complete leased pin inventory versus pure projection, and generic mutation
versus repair apply replay — each is asserted by a check whose id and result are byte-identical across
the delta, or lives in a report that is byte-identical across the delta.

Preserved caveats, unchanged: no-clone-facts alone still does not authorize complete clone Coverage
with absent or partial dialect prerequisites; the owning Coverage law still applies. Level-specification
fixture bytes are not qualified FACT-IDENTITY implementation content. Suffix variants remain
deliberately conservative. Whole-manifest integration custody, multiple contexts per language and
frozen-snapshot application remain intentional. Every historical source and scope is preserved, and
prior failed harness attempts remain honest historical evidence rather than universally passing checks.

---

## 8. Carried advisories

All 11 v9 advisories and the 25-item carried v5–v9 account are **CARRIED, not discharged**. Three I
re-tested rather than restated:

- **v9-A1 (723 bytes).** Independently re-derived: canonical wrapping adds exactly **12** bytes (I
  measured bare 105 vs wrapped 117 on a synthetic four-edition map), which is exactly 723 − 711. So
  `C({'edition': map}) = 723` and bare map `= 711` are arithmetically consistent; original conclusion
  unchanged, and the advisory to state the wrapping stands.
- **v9-A6 (fixture).** Provenance is exact — `integration-fixtures.py` declares checker SHA256
  `a7f7d393…`, equal to the released checker, and that line is the *only* change to the file. It is
  still copied from the checker, so it remains synthetic composition and **not** an independent oracle.
- **v9-A10 (pin truncation).** Reproduced: deleting one row from the 1099-row inventory leaves every
  remaining row verifying, so a pure projection cannot detect truncation.

### New advisories (genuinely nonblocking)

- **v10-A1** — the implemented cause set (six causes) has outgrown the three conditions the law text
  declares; `RELATION_DIGEST_ANNOTATION_CONFLICT` is a new inadmissible condition the law does not
  name. Nonblocking because both additions only ever *refuse* more, never admit more.
- **v10-A2** — the effective-annotation inheritance rule (an annotation anywhere on the path covers a
  governed leaf, including an intermediate alias `$def` but deliberately not the terminal one) appears
  only in reference implementation docstrings; the `x-opensip-digest-law` object contains none of
  *alias, inherit, branch, nested, array, container, oneOf, precedence*. Relevant to DR-011-R10, which
  remains open.
- **v10-A3** — check-count growth is not coverage growth, measured: the suite grew 602 → 661 while the
  `record()` merge was executed **0** times across all 661 checks.

---

## 9. Registers

- **AR-01 … AR-16:** ACCEPT, except **AR-15 = CHANGES_REQUIRED**. No crosswalk defect was found —
  routing is correct and honest, `currentReviewBinding` stays PENDING-INDEPENDENT-REVIEW with no
  embedded future digest, the crosswalk does not contain its own digest (no self-hash cycle), and
  `latestCompletedReview` correctly cites the v9 review hash with its unresolved SHOULD. AR-15 is
  graded CHANGES_REQUIRED for the same structural reason as v9: this review carries an unresolved
  SHOULD that the one effective integration narrative must absorb.
- **FW-01 … FW-15:** ACCEPT, on unchanged bytes.
- **Inherited residuals:** DR-001 … DR-011 and DR-011-R01 … R16, keyed individually — ACCEPT as
  *routing*, no SATISFIED grade granted, inherited history unedited. **DR-011-R10 remains open** (no
  Bv3 exists). DR-011-R12 carries all 30 evaluation subresiduals (19 RES, 7 NB, 4 measured escapes)
  with individual dispositions whose own standing does not close the parent row.
- **Scoped review owners DR-201 … DR-205:** **ACCEPT_SCOPED** — scoped strictly to whether the
  crosswalk and source map *route* each owner without claiming or re-opening its historical
  acceptance. Verified per key: each is an `ownerRow` of AR-15; AR-15 status is
  `PROPOSED-SOURCE-MAP-PENDING-REVIEW-AND-APPLICATION`; and
  `docs/v2/architecture/08-decision-and-readiness-register.md` is byte-unchanged across the delta, so
  the historical grades are preserved as history and neither extended nor re-litigated.
- **32 product qualification gates:** all remain **undemonstrated**; this review demonstrates and
  grants none. Every native, compiler, OS, storage and crypto observation remains a synthetic TCB
  assumption and qualifies nothing.
- **D-371 / D-372:** not applied. The central readiness/application act remains intentionally
  unapplied; condition 5 remains NOT MET.

---

## 10. Limitations and what is not claimed

Not product qualification; no OS, compiler, cargo, rustc, linker, crypto, SQLite, filesystem, clock or
lease measurement was performed. Not the blind consumer review — reconstructability from the normative
subset remains for a **new** fresh blind session and is not granted here. Not application and not
readiness. No implementation authority. Historical grades are not extended and no old grade is treated
as blanket acceptance. This review's own digest is not embedded in the subject it reviews, so it
creates no self-hash acceptance cycle.

The v10-S1 counterexamples are hypothetical, metaschema-valid schema documents exercising forms the
implementation explicitly claims to support. They demand no future schema feature beyond the declared
language; they detect a silent gap in what this implementation says it supports.

## 11. Required next acts

1. Correct v10-S1's same-path aggregation, and add an authored check that actually reaches the merge.
2. Freeze the successor; fresh independent review at **zero** unresolved MUST and SHOULD.
3. Actual Codex assent covering all 25 carried advisories and the 3 new v10 advisories.
4. A **new** fresh blind consumer B on the accepted normative bytes.
5. Complete, independently reviewed application and readiness reconciliation, with activation last.
