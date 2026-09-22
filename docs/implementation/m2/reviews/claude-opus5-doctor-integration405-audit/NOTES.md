# Integration audit 405 — reconciling the owner402 doctor/schema change with the current workflow reference

Auditor: Claude Opus 5 (1M context), `claude-opus-5[1m]`. **Read-only. This is advice, not formal
acceptance, not an owner-body review, and not a review of any working draft outside frozen 402.**
No native jobs; nothing edited; no commits or pushes. Pins in `evidence/source-pins.json`.

Frozen 402 verified before reading: archive **95 948 B / `92d8b3f45ba5d6910c5b39eb4564b5dfafbb2b693844c1ed764df31dd3fa301b`**,
manifest **8 137 B / `ebbef2b3945c46d457b8c321780cc1e42f467ab2ae506fe05816f625a8ca7302`**, 52 members.
Context as of 2026-09-21T16:4x: arch `8d7ffd60b`, product `883f963` clean.

---

## A. Are the named checker and vectors selected inputs, or only historical?

**Selected — but not through the channel the phrasing implies.** This is the single most important
thing to get right in the reconciliation, and it has three layers.

| Artefact | Channel | Live vs that pin |
|---|---|---|
| `workflows/command-inventory.v3.json` | **direct lock input** `/inputs/23` | match |
| `workflows/check_workflows.v1.py` | `approvals.sourceManifest` → `candidate-subject.v45.json` (12 920 paths) | **match** |
| `workflows/workflow-cases.v1.json` | `approvals.sourceManifest` | **match** |
| `workflows/workflows_model.v1.py` | `approvals.sourceManifest` | **match** |
| `workflows/check-workflow-projection.v3.py` | `approvals.sourceManifest` | **match** |
| `import-totality-reference-selection-v1/reference/workflows_model.v1.py` | `/contractSuccessors/29` candidate | match; **not in `sourceManifest`** |

So: none of `check_workflows.v1.py` / `workflow-cases.v1.json` appears at any `/inputs/*` site, and a
lookup that only scans `inputs`, `inventorySuccessors` and `contractSuccessors` will wrongly report them
as historical. They are selected **through `approvals.sourceManifest`**, at pins the live files
currently match.

**Correction to my own owner399 RF-1.** I wrote that those two files "are selected" without naming the
channel, and root's 401/402 text inherited that framing. The claim is true, but the successor must say
*selected via `approvals.sourceManifest` at `candidate-subject.v45.json`*, because the amendment has to
move a manifest-pinned file, not a lock input — a different mechanical act.

---

## B. Exact parents, and three divergent-current-source risks

### B-1 (highest) — two selected workflow models, which differ

| Copy | Bytes | sha256 | Channel |
|---|---|---|---|
| `docs/coop/design-corrections/workflows/workflows_model.v1.py` | 142 811 | `be37023f…` | `approvals.sourceManifest` |
| `…/import-totality-reference-selection-v1/reference/workflows_model.v1.py` | 142 991 | `60dc11e2…` | `/contractSuccessors/29` |

Both are selected, through different channels, and **they are not identical** — they differ in
`run_invocation`, `registry_row` and `glob_match` (the import-totality fixes). Draft402 extends the
**import-totality reference**, which is correct, and its `check_diagnostics.py` sets `BASE` to that file.

*Risk:* any successor sentence saying "the selected workflow model" is ambiguous today. It must name
the import-totality reference by path and digest, and state what becomes of the coop copy — superseded
for this purpose, or left as the manifest-pinned artefact it is. Do **not** resolve this by freezing the
stale full model.

### B-2 — the two approvals manifests pin different versions of the same three files

`approvals.applicationManifest` (`application-subject.v46.json`, 522 paths) pins **older** bytes for
`check_workflows.v1.py` (114 055 / `5c64b593…`), `workflow-cases.v1.json` (243 554 / `22b74430…`) and
`workflows_model.v1.py` (139 660 / `b83f910f…`). Live matches the **sourceManifest** pins, not these.
`command-inventory.v3.json` matches in both.

This is probably deliberate layering — the application manifest records the state at application-46 —
but a reconciliation that amends "the selected checker" must say **which manifest governs**, or a later
verifier will compare against the wrong pin.

### B-3 — `check-workflow-projection.v3.py` is a selected consumer and is not named

Owner401/402 names the v1 checker and vectors. `check-workflow-projection.v3.py` (275 083 B,
sourceManifest-pinned, live matching) asserts at **lines 4355-4356** exactly the mapping the doctor work
touches:

```python
{g["id"]: g.get("domainDetail") for g in _inv3["goldens"]
 if g["id"] in ("doctor-report-not-producible", …)}
 == {"doctor-report-not-producible": "DOCTOR.REPORT_NOT_PRODUCIBLE", …}
```

It must be in the reconciliation list alongside the v1 artefacts.

---

## C. The `DOCTOR.REPORT_NOT_PRODUCIBLE` promise — a pre-existing divergence, not one 402 creates

Root asked what the existing selected assembly/render promise actually is. It is inconsistent **today**,
independently of the doctor count work.

- **Selected golden** (`command-inventory.v3.json`, `/inputs/23`), id `doctor-report-not-producible`:
  `class: operational-failed`, `exitCode: 4`, `errorCode: HOST.IO_FAILURE`,
  **`domainDetail: DOCTOR.REPORT_NOT_PRODUCIBLE`**.
- **Selected reference model** (`import-totality…/reference/workflows_model.v1.py`), `terminate()` for
  `doctor-report` when `reportProduced` is false:
  `{'class':'operational-failed','errorCode':'HOST.IO_FAILURE','faultCause':'host-io'}` — **no
  `domainDetail` at all.** The string `DOCTOR.REPORT_NOT_PRODUCIBLE` does not appear in that model.
- **Selected projection checker** asserts the golden's mapping (B-3).

So the owner sentence "a report that cannot be produced retains `HOST.IO_FAILURE` /
`DOCTOR.REPORT_NOT_PRODUCIBLE`, exit 4" matches the **golden and the projection checker**, and the
reference model is the artefact that lags.

**Narrow reconciliation, inventing nothing:** add the `domainDetail` to that one false-branch in the
reference successor so the model matches the already-selected golden. It is one additive dict key, it
is *required by selected law* rather than proposed by the owner, and it is unrelated to the count
amendment. The helper's own signature — `doctor(store_openable, defects)` — is untouched; the detail
belongs to `terminate()`, which is where the golden's `domainDetail` has always lived. Flag it in the
successor as closing a pre-existing gap so it is not mistaken for new doctor behaviour.

---

## D. Does the same-ID common:4 extension reach every relevant alias?

**Yes for the doctor path, no for the sibling majors — and that asymmetry is the thing to protect.**

| Carrier | `$id` | Enum | Role |
|---|---|---|---|
| product `schemas/sources/common-v1.schema.json` | `…:workflows:common` | **315** | namespace `Common1` |
| product `schemas/sources/common-v3.schema.json` | `…:evaluator3:common:3` | **315** | namespace `Common3` |
| product `schemas/sources/common-v4.schema.json` | `…:evaluator3:common:4` | **317 → 319** | namespace `Common4`, the extension target |
| arch `workflows/schemas/common.schema.json` | `…:workflows:common` | 315 | — |
| arch `workflows/schemas/evaluator3/common.schema.json` | `…:evaluator3:common:3` | 315 | — |

**There is no architecture-side common:4 carrier.** The extension is product-only, which supports 402's
"same unreleased ID, not a new public major" framing.

**Consumers that must change:**

1. `schemas/sources/common-v4.schema.json` — the enum itself.
2. `tools/contracts/generator-closure.json` — 349 pinned entries; it pins common-v4 at
   **64 866 B / `6af81f35…`**, so the closure pin moves with the bytes.
3. `crates/contracts/src/generated/evidence.rs` — regeneration.

**Consumers that must NOT change, and the concrete hazard:** `evidence.rs` carries **all three** enums
in one file — `Common1DomainDetailCode` (315), `Common3DomainDetailCode` (315),
`Common4DomainDetailCode` (317). A regeneration that re-derives every alias from a single "current"
enum would silently widen the two older majors, breaking both the closed-enum rejection property and
the explicit no-old-decoder-compatibility stance. **Require a diff assertion that the regenerated
`evidence.rs` adds exactly two variants, both inside `Common4DomainDetailCode`, and that the Common1 and
Common3 enums remain at 315 with unchanged order.**

**The doctor record is on the right alias:** `Invocation5DoctorResult { defects: Vec<Common4DomainDetail>,
defects_found: Common4Uint53 }`. Its sibling `Invocation3DoctorResult` is on `Common3*` and must stay at
315. `Common4DomainDetail` is `{code, purgeDisclosure, remedy, subject}` — **no severity field**, matching
402's "no envelope/severity change".

**Maps need no edit:** `schemas/source-map.json` and `schemas/admission-source-map.json` both map the
three ids to their files and namespaces by path; extending the enum changes neither mapping. Worth
noting that common:4 appears in **both** maps, so it is a generation *and* an admission source — the
new codes become admissible at the same moment they become generatable, which is the coordination 402
already requires.

**No missed live emitter:** nothing outside `crates/contracts/src/generated/` references `DoctorResult`
at all. There is no product code today that would start emitting the new codes, which bounds the blast
radius to schema + closure + bindings.

**Corroborating the closure defect root reported:** `generator-closure.json` pins `tools/verify_design.py`
at **28 690 B / `76d7f509…`** while live is **33 654 B / `2764cf7b…`**. I confirm the mismatch from the
closure file itself; I did not audit the generator or the rebuild.

---

## E. Minimal additive reference successors and tests

Scoped to what the above actually requires — no redesign.

**Successor 1 — reference model (additive, two edits).** Extend the import-totality reference:
(a) the doctor count/termination join excluding exactly the reserved informational code, as 402
specifies; (b) the `domainDetail: DOCTOR.REPORT_NOT_PRODUCIBLE` on the `reportProduced == false` branch,
labelled as closing the pre-existing golden divergence in §C. Preserve all other statements; the AST
check 402 already carries is the right guard.

**Successor 2 — schema + closure + bindings, as one coordinated act.** common-v4 317→319 preserving the
original 317 positions; closure re-pin; regeneration with the Common1/Common3-unchanged diff assertion
from §D.

**Successor 3 — checker and vectors.** Amend `check_workflows.v1.py` and `workflow-cases.v1.json` at
their `sourceManifest` pins, and add `check-workflow-projection.v3.py` to the same act.

**Tests to add, by behaviour:**

| Case | Assert |
|---|---|
| healthy complete-I | `defectsFound == 0`, one informational entry present, `class: success`, exit 0, **no** `DOCTOR.DEFECTS_FOUND` |
| mixed | `defectsFound == 1` with two entries, `DOCTOR.DEFECTS_FOUND` present |
| count cap | 255 actual + 1 info = 256 entries admitted, `defectsFound == 255` |
| overflow | 256 actual refuses and latches; no truncation |
| unproducible | `doctor(False, [])` → `operational-failed`, exit 4, `HOST.IO_FAILURE`, `DOCTOR.REPORT_NOT_PRODUCIBLE` |
| unknown code | refused by the closed enum — **keep this rejection; do not weaken it** |
| non-complete-root | 256 bound unchanged, no informational entry |
| trust doctor / store status | no informational entry, no count field invented |
| human / JSON / agent | the same numeric count and complete list on every format; the informational entry rendered with its fixed label |

The existing two-defect no-note fixture must be **retained unchanged** — 402's helper/assembler split is
what makes that possible, and it is the regression guard that the count change did not leak into the
helper.

---

## F. Trusted AST/helper tests versus real product renderers

Keep these separate in the successor's claims:

- **Trusted-input tests** (402's 22 composition checks, the AST guard, the surface assembler) take
  already-admitted details as premises. They prove *composition and arithmetic*. They do not bound
  arbitrary ingress and they are not renderer evidence.
- **Real product renderers** are the `human`/`json`/`agent` formats declared in the selected inventory,
  with the parity rule that every parity field is printed verbatim or by a documented fixed label. No
  renderer implementation exists to test today, and the audit found **no non-generated product consumer
  of `DoctorResult`**. The successor should say plainly that renderer behaviour is specified by golden,
  not demonstrated by the Python composition checks.

---

## G. Limits

Read-only; no native jobs; no edits, commits or pushes. Advice only — this is not formal acceptance,
not an owner-body review, and grants nothing. Working drafts outside frozen 402, the private 404
generation run, the 403 generator rebuild and `M/initial-root-binding-reconciliation` are context, not
authority, and were not reviewed. I did not audit the generator, the rebuild or the 349-file closure
beyond reading the one pin cited in §D. Selection status was determined from `design-lock.json` and the
approvals manifests it names; sha prefixes are shown where noted, with full digests in
`evidence/source-pins.json`.

Auditor: Claude Opus 5 (1M context).
