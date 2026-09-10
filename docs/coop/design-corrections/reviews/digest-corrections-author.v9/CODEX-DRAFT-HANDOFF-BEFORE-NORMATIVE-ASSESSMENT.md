# HANDOFF — actual Claude coauthor, v9 (p02/p03 same-path order dependence)

**Standing: not accepted, not qualified, not promoted. No implementation authority claimed.** The
actual independent reviewer (session `4628c693-7a5e-4567-a1c8-e2f7ae322651`) is still reviewing
frozen v10 and **has issued no verdict or severity; I infer none, and nothing here claims their
agreement.** Root remains responsible for review reconciliation, applying any released delta, root
checks, fixture/pins/six commands, and a new freeze plus fresh independent review, new blind B and
application/readiness reconciliation.

**Nothing was written to the real repository, to any frozen snapshot, or to the reviewer's
directory.** Verified after the work: the live repo's two files are still
`f200232b9ccc…` / `a7f7d393d3b1…`, all five captured reviewer inputs still carry their custody
hashes, and `post-reset-review.v10/work/` was never touched.

| Input read | Bytes | SHA-256 |
|---|---|---|
| `digest-corrections-author.v9/CODEX-PUBLIC-NOTE.md` (read in full before handoff; absent at launch) | 1188 | `374c2bc5355863f7c2ae1bc78c7d2fb4e49dc0c4b5f2e74b3adf537c68287394` |
| `reviewer-p02-input/p02_order_independence.py` | — | `d1c85d61504a009bb5aa227b80d70da2f83aaa57c0037eb7eb537d8f0abdc92b` |
| `reviewer-p02-input/harness.py` | — | `d390200e412f54748a4e6ec06fc0ef0f8a8c63e0ac8a5f34b8c9ed06375c78f9` |
| `reviewer-p02-input/p02.json` | — | `f11079f282b8fec6142d0ba2965a161a58cc38dd7c7c22224295d9323fc4a993` |
| `reviewer-p02-input/p03_order_hardened.py` | — | `c58b7ccc35cf7bd2013d81555726597e7b9e6458ef6eb09602279afb2b19bd50` |
| `reviewer-p02-input/p03.json` | — | `db281a0d91b6f78495a7fe9a1bec894e1a298e626ac6563514e344aa2e01a039` |

`sourceRoot = /tmp/opensip-design-corrections/digest-corrections-author.v9/work` (exact copy of
frozen v10 `82c1be11d3b61908b2a45ebb6e59e71bb5cb31d8450a96a61857ced430e786fd`).

---

## 1. Assessment: the reviewer is right, and their source reading is exact

`record()`'s docstring claimed "never let an annotated sighting erase an unannotated one at the same
path … so admissibility cannot depend on branch order". The code was:

```python
annotations=previous['annotations']+[a for a in annotations if a not in previous['annotations']]
if not previous['annotations'] or not annotations:annotations=[]
```

`annotations` is **rebound to the merged list before it is tested**, so `not annotations` is true
only when both sides were empty — a no-op. The effective rule collapsed to *poison iff the
first-recorded sighting was unannotated*, which is precisely a visit-order dependence. Their p02
does not argue from source: it builds two documents with the **same multiset of sightings at one
path** and compares admission. p03 hardens it — every hypothetical document is metaschema-valid, and
case B is shown to be a pure JSON key-order swap of identical content.

I reproduced both against the frozen v10 bytes and got their results exactly: **case A and case B
each REFUSE unannotated-first and ADMIT annotated-first**, with both controls behaving. The defect is
real and it is mine.

**Scope, stated as they state it:** the shipped document has **no same-path collision at all**
(7 governed sightings, 7 distinct paths), so no current relation, payload or Run is affected. This is
a hypothetical schema/reference consistency defect under supported traversal, **not** a payload or
Run attack, and I claim no runtime security property.

## 2. The correction: missingness as an explicit monotonic fact

```python
missing=not annotations                       # THIS sighting contributed none
if previous is not None:
    missing=previous['missing'] or missing    # monotonic; no later sighting undoes it
    merged=list(previous['annotations'])
    for a in annotations:
        if not any(C.equal_typed(a,other) for other in merged):merged.append(a)
    annotations=merged
```

"No new annotation" and "already merged" are now **separate facts**, which is exactly what the old
single-list test could not express. The merged list is kept **alongside** `missing` rather than
replaced by it, so a conflict between two annotations at one path stays diagnosable even when the
path is also poisoned. Coverage reporting and the closure both read
`missing or not annotations`, so all three effective-annotation limbs agree.

Deduplication now uses `C.equal_typed` rather than `in`, matching the conflict limb's own comparison.

**No new cause and no new semantics.** Causes, limb order, the three annotation locations, the
conflict rule, top-level join addressing, the no-blanket-terminal rule and the `previousPath`
exemption are all unchanged. **Only the two owned files changed** — verified by hashing every file of
the work tree against frozen v10.

## 3. Evidence

**The reviewer's p02 and p03, adapted to my own paths and run PRE vs POST** (their vector builders
reproduced unchanged; their `harness.emit` writes into their live directory, so only loading and
emitting were replaced — their originals were never executed and never overwritten):

| Vector | frozen v10 | corrected |
|---|---|---|
| case A container, unannotated-first | REFUSE | REFUSE |
| case A container, **annotated-first** | **ADMIT** | **REFUSE** |
| case B key order, items-first | REFUSE | REFUSE |
| case B key order, **additionalProperties-first** | **ADMIT** | **REFUSE** |
| control single unannotated | REFUSE | REFUSE |
| control single lawful annotated | ADMIT | ADMIT |

`caseA_orderDependent` and `caseB_orderDependent` go `true → false`; every p03 hypothetical document
is metaschema-valid in both images; the shipped document has no same-path collision either way.

**The two kinds are distinguished rather than lumped**, as root asked: case B's two documents are
**canonically equal** (`C.canonical` identical), so a verdict difference there could only ever be an
implementation artifact; case A's two documents genuinely differ, and what must match is the
multiset of sightings at the path. The suite asserts both facts.

**New regressions are discriminating, not decorative** — each construction run against frozen v10 and
the corrected model (`probes/result-new-regressions-are-discriminating.v1.json`):

- flip ADMIT → REFUSE: `container-annotated-first`, `keyorder-annotated-first`,
  `three-missing-at-1`, `three-missing-at-2`
- identical on both: the two unannotated-first vectors (they already worked — retained as controls
  that the correction did not break the direction that did), `three-missing-at-0`, and the
  all-annotated positive control which **admits on both**.

**A third sighting after a missing one.** Root asked for this and it needed a shape the first
attempt did not produce: three schemas on **one** path via a two-level `$ref` chain plus the field's
own refinement. An `allOf` branch does **not** work — it gets its own path, so it is a different
sighting rather than a third arrival. All three positions of the missing one refuse, and frozen v10
admitted two of them.

**Every prior class preserved** (`probes/result-prior-classes-preserved.v1.json`): 0/39 injections
admitted; root's nine inherited-limb vectors give `RESIDUE / RETENTION / ADMIT` identically at field,
alias and branch; annotation locations `nowhere → UNANNOTATED`, `field → ADMIT`, `alias → ADMIT`,
`terminal → UNANNOTATED`; `previousPath` still `not-joined`; shipped coverage 7/7/none; all 13
relations coherent.

## 4. Owned files changed, relative to the work root

`sourceRoot = /tmp/opensip-design-corrections/digest-corrections-author.v9/work`

| Path (relative to sourceRoot) | SHA-256 | frozen v10 |
|---|---|---|
| `docs/coop/design-corrections/foundation/identity-model.py` | `de3ae06bac169cf3b41b9cea43c2b0c7113ed2de6b4a3ae164fc8b4d9cc77557` | `f200232b9cccc06f280db284280932646baaae050418521ee3f03eafece1b226` |
| `docs/coop/design-corrections/foundation/check-identity.py` | `90a3b590eec305ad72b839e2135fe46de7a6789e3f7218cf20ddc108a35993c8` | `a7f7d393d3b1c9284ce1109b0458b9cb63708794c371365be22e8c5afc4f053c` |

Both frozen-v10 files are retained verbatim as `PRE-identity-model.py` / `PRE-check-identity.py`.
No other file in the work tree differs. No report or pin was regenerated in the work tree; native
and security ran in a separate disposable sandbox that was then deleted.

## 5. Development checks (all in the disposable copy)

| Suite | Result |
|---|---|
| `foundation/check-identity.py` | **673 / 673**, 0 failed (661 at v10; +12) |
| `foundation/check-foundation.py` | PASS, 231 / 231 |
| `foundation/check-array-orders.py` | 65 / 65 |
| `foundation/check-product-configuration.py` | 28 / 28 |
| `foundation/check-product-quality.py` | 24 / 24 |
| `workflows/check_workflows.v1.py` | 1290 / 1290 |
| `native/check_native_evidence.v2.py` | PASS, 151 / 151 — sandbox copy, regenerated pins |
| `security/check-security-lifecycle.v1.py` | 456 / 456 — same sandbox |
| `check-integration.py` | 363 / 363, builder unedited |

## 6. Limitations and honest record

- **A failed edit attempt is preserved rather than hidden.** My first insertion asserted on an anchor
  and left the file untouched, but I then discovered the anchor comment was **already doubled in the
  frozen v10 bytes** — a cosmetic artifact I introduced in v8 (`s.replace(anchor, add+anchor)` where
  `add` itself ended with the anchor text). I briefly "repaired" it, then **restored the frozen byte
  exactly** and anchored elsewhere, because silently tidying frozen bytes would put an unrequested
  change into a delta root must reconcile. The doubled comment is still there, in both the frozen
  file and my delta. It is harmless — one comment repeated on one line — and it is mine.
- My first three-at-one-path fixture used an `allOf` branch, which lands on a **different** path, so
  one position asserted the wrong cause. Corrected to a two-level `$ref` chain and re-measured; the
  wrong construction is not shipped.
- **The shipped document is unaffected**, so this closes no current payload or Run defect. Reaching
  any of these causes requires a reviewed design-time edit to a registered document.
- The monotonic rule is deliberately **conservative**: if any schema reaching a path declares no
  annotation, the path is unannotated, even though another schema at that path did annotate it. That
  is the strong-law reading (no defaults, no residue) and it is what `record()` always claimed; it is
  not a new semantic.
- I am **not** the independent reviewer and this handoff makes no statement about their conclusions.
  p04 is described in root's note but was not captured here, so I assessed only p02 and p03.
- Owned files are stable as of this response and will not be touched further.

---

**No acceptance, no readiness, no implementation authority.** Root applies the released delta only
after both current passes finish, then integrates, freezes a successor, and obtains a new independent
review, a new blind B and the application/readiness reconciliation. This bounded correction is
complete.
