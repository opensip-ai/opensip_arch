# Independent review — corrected directory-publication inventory v59, revision 2 (layout only)

Reviewer: Claude Opus 5 (1M context), `claude-opus-5[1m]`. Capacity available; substantive review
performed. **Layout only** — no source396, owner397 or runtime assessment is made or implied.

**Top verdict: ACCEPT-UNIT. `requiredFindings: []`.**

RF-1 from my r1 review is closed. The correction is well made, and my independent re-derivation of the
projection — from the *selected* checker's own algorithm rather than from the author's verifier — agrees
with the frozen record exactly.

I also need to correct my own r1 reasoning, and I do that in §3 before anything else. Root's position
that this was a clarity gap and **not a demonstrated live bug** is right; I verified it, and my r1
wording overstated the risk.

---

## 1. Verification

### Subject

`docs/implementation/m2/directory-publication-inventory-v59-r2-subject.json`, **1 299 B**, sha256
`fce48e71ade6eabdfe88a64857bbd3851d71227ebfdf9a899b9a9acc8ff09e60` — matches the declared pin.

**6 / 6 members** verified byte-for-byte and by sha256; sorted; unique:

| Member | Bytes | sha256 |
|---|---|---|
| `…/directory-publication-inventory-v59-r2/README.md` | 1 653 | `77bad5df…` |
| `…/directory-publication-inventory-v59-r2/successor.json` | 5 131 | `9503e52e…` |
| `…/directory-publication-inventory-v59-r2/verification.json` | 459 | `04cfa468…` |
| `…/directory-publication-inventory-v59-r2/verifier-anchor.json` | 508 | `19e8c0b9…` |
| `…/directory-publication-inventory-v59-r2/verify_projection.py` | 2 147 | `3038ed71…` |
| `…/repository-file-inventory.v59.json` | 280 949 | `c2400990…` |

### The candidate is byte-unchanged, and the whole unit still holds

I re-verified the layout from scratch rather than carrying r1's result forward:

| Check | Result |
|---|---|
| Candidate sha256 vs the value I verified in r1 | **identical** — `c2400990cf4f9ec0c6c4e4331e2194313dea272f17ad04c83866a23c9c1cb815`, 280 949 B |
| Rows | 705 → **706** |
| Added / removed / existing rows changed | **1 / 0 / 0** — only `crates/platform/src/filesystem/directory_publication.rs` |
| Inherited row order preserved | yes |
| `packages` | 20 → 20, byte-identical |
| `pendingDecisions` | 9 → 9, byte-identical |
| New row index | 187, between `directory_open.rs` and `directory_volume.rs` |
| Parent | selected v58, 280 320 B, `f6c3c307…` — matches live **and** the lock at five sites |
| Carried obligations | the two checkpoint‑211 / ‑218 entries, text and standing unchanged |

### Lock state and prior unit

- Live lock: 46 inputs, **34** inventory successors, **53** contract successors, 4 passage-inheritance
  entries — matching the stated 34/53 (contract successors went 52 → 53 with the runtime32 selection).
- v59, the r1 record and the r2 record are **none of them in the lock**. Correct for an unselected
  candidate.
- The r1 unit is untouched: its subject (`c262dffa…`) and successor (`6971d194…`) are byte-identical to
  the values in my r1 review. Its NEEDS-CHANGES stands and its record must not be selected.

### Verifier anchor

`verifier-anchor.json` pins product HEAD `ef3b1b51cba879151e58220e64975c5c3a7af441` with
`tools/verify_design.py` (33 654 B, `2764cf7b…`) and `design-lock.json` (99 846 B, `80c555ef…`). **Both
match live exactly**, and the declared head is the current product head. Pinning the enforcing checker
alongside the starting lock is the right instinct: it makes "the selected tooling already does this"
a checkable claim rather than an assertion.

---

## 2. RF-1 closure

### The record now carries the projection

`successor.json` gains `projectionRule` and `descriptionOverrideProjection`, four rows sorted by file
path, each with the stable path, both selectors, the unchanged `before` text and the effective
inherited text:

| File path | Parent selector | Candidate selector |
|---|---|---|
| `apps/cli/src/bootstrap.rs` | `/files/7/description` | `/files/7/description` |
| `apps/report/package.json` | `/files/13/description` | `/files/13/description` |
| `package.json` | `/files/502/description` | **`/files/503/description`** |
| `schemas/sources/imported-v1.schema.json` | `/files/569/description` | **`/files/570/description`** |

That is exactly the mapping I derived independently in r1 — 7→7, 13→13, 502→503, 569→570.

### Independently re-derived, not taken from the author's verifier

Running the author's own verifier only establishes that it agrees with itself. So I re-implemented the
projection **from `tools/verify_design.py`'s algorithm** (resolve the selector in the ancestor, look the
row up in the final inventory *by path*, refuse a changed row, rebuild the pointer at the new index) and
compared the result to the frozen record: **agrees on all four rows**, and no override target row
changed (`anyRowChanged: false`). Evidence in `evidence/crosscheck.json`.

### The frozen verifier replays

`python3 -I -B verify_projection.py --architecture A --lock P/design-lock.json` →
`{"projectionRows": 4, "positive": "PASS", "corruptionsRefused": 18, "readOnly": true}` — reproducing
the author's `verification.json` exactly. The 18 are 4 rows × 4 mutated fields, plus a dropped row and a
duplicated row. It writes nothing; both repositories were clean afterwards (the architecture entries
present are root's own in-flight files, not mine).

**RF-1 is closed.**

---

## 3. Correcting my own r1 finding

Root says the projection gap "was not demonstrated live bug". I checked, and root is right.

`tools/verify_design.py` — selected, and pinned in this unit's own verifier anchor — already does the
whole thing at lines ~316-346. For each override it reads the ancestor document **by pinned bytes**,
resolves the selector there, looks the row up in the final inventory **by path** (`final_rows[row['path']]`),
raises `'inherited inventory passage row changed'` if the row content differs, rebuilds the pointer at
the new index, and finally refuses the whole selection with
`'inventory passage inheritance differs from reviewed ancestor meaning'` if the recomputed list does not
equal `lock['inventoryPassageInheritance']`.

So the two halves of my r1 finding fare differently:

- **Holds.** The unit's own artefacts did not record the projection; `inheritedRowsEqualByValue` is about
  row values, not selector positions, and the requirement lived only in README prose. r2 fixes exactly
  that, and the unit is better for it.
- **Overstated, and I withdraw it.** I wrote that the outcome could be "a silent retarget of two
  selected description overrides onto unrelated files… and a reviewer cannot tell which from the
  artefacts." A silent retarget was never possible, and a reviewer *could* tell — by reading the
  selected checker in the product repository, which I had access to and did not consult. I verified
  `design-lock.json` and both inventories and stopped at the data, without checking the tool that
  consumes them.

The honest characterisation of RF-1 is therefore: **a self-containment gap in the unit, not a latent
correctness hazard.** ACCEPT-UNIT here is for a genuine improvement in reviewability, not for a
near-miss averted.

---

## 4. Machine projection coverage and forward selection binding

Root invited this challenge. Six adversarial mutations against the frozen verifier
(`evidence/crosscheck.json`), beyond the author's 18:

| Probe | Mutation | Result |
|---|---|---|
| **X1** | swap a row's `parentSelector` for another real selector | **refused** |
| **X2** | reverse the projection row order | **refused** |
| **X3** | corrupt the record's `parent` sha256 | **refused** |
| **X4** | corrupt the record's `candidate` sha256 | **accepted** |
| **X5** | falsify `addedFiles` | **accepted** |
| **X6** | falsify `inheritedRowsEqualByValue` | **accepted** |

**X1 and X2 are good news beyond the author's claim.** `parentSelector` is the one row field the 18
variants never mutate, and row order is never permuted — yet both are caught, because the final check is
a whole-list equality against a sort. Coverage is better than the count of variants suggests.

**X4 is worth recording.** `verify_projection.py` loads the parent and candidate **by path** from
`--architecture`, never comparing them with the `bytes`/`sha256` the record declares. So a record that
names the right path with a wrong digest still passes. The contrast is instructive: the selected
`verify_design.py` reads the same documents through `pinned_bytes(...)`, so it *is* pin-checked at
selection. The consequence is narrow but real — the frozen `PASS` proves the projection is correct for
*whatever bytes are on disk under `--architecture`*, not for the pinned bytes the record names. A
one-line digest check would make the helper's result self-contained. I am not raising this as a required
finding: the pins are verified independently in this review, and by the selected checker at selection.

**X5/X6 are scope, not defects.** The verifier's stated job is the projection; the additivity assertions
are checked by me directly in §1 and by `verify_design.py` at selection.

**Forward selection binding.** `verify()` asserts `old['parent'] == record['parent']` for *every* entry
in `lock['inventoryPassageInheritance']`. Today all four share the v58 parent, so it passes. Two
consequences: the verifier is a **pre-selection instrument by construction** — after v59 is selected the
lock's entries carry the v59 pin as parent and this script would no longer match — and if the lock ever
gains an inheritance entry for a *different* ancestor, the script fails on a change unrelated to this
unit. The README already states the first ("an unrelated later lock change requires fresh
selection-baseline validation, not editing these historical anchors"), which is the correct posture; the
second is worth knowing before the script is reused as a template.

---

## 5. Limits

- **Layout only.** No source assessment: private 396 exists and was not read, built or tested; no source
  acceptance is implied. No owner397 assent — that unit is separately NEEDS-CHANGES and neither review
  depends on the other.
- **No selection script run** and **no native build**, as instructed.
- **Not re-reviewed on their merits:** v58 (only currency, pin, lock presence and assent status),
  runtime30/32, registry-v2.
- The added row remains a **planned** file entry; as the carried obligation itself says, no planned file
  entry proves implementation, custody or product readiness.
- My re-implementation of the selected projection algorithm is a reading of `verify_design.py`, not an
  execution of it; I did not run the selected checker.

---

## 6. Context HEADs — as of 2026-09-21T15:56:09-07:00

Stated as of that sample only; the byte pins above, not these labels, are the authority.

| Repository | HEAD | Subject | Committed |
|---|---|---|---|
| architecture | `f657f2a40038c3c87d0133ed969147a054e85cc7` | "Select reviewed directory barrier runtime and freeze exclusive publication source" | 2026-09-21T15:40:11-07:00 |
| product | `ef3b1b51cba879151e58220e64975c5c3a7af441` | "Expose retained directory barrier observations with explicit limits" | 2026-09-21T15:36:08-07:00 |

Product tree clean. The architecture worktree carries root's own in-flight files; none of my work
touched either repository.

---

## 7. Attestation

Read-only against live, frozen, history, product and lock. No byte was edited, no pin was edited, no
selection script was run, no native build, no commits, no pushes. All writing went into this review
directory. The r1 inventory review, the owner397 review and every earlier report and hashes file are
untouched and keep their own standing.

This grants no root assent, no formal selection, no source396 acceptance, no owner397 acceptance, no
native authority or qualification, no M2 completion and no release qualification. Actual selection
requires root's full read, assent and private/live validation.

Reviewer: Claude Opus 5 (1M context).
