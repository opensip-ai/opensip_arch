# Native runtime selection29 + source384/385/386 — design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

One bounded task with distinguished assessments:

1. **Source386** (not previously approved): exact composition of unreviewed 385 (11 product files) plus unreviewed 384 (2 security files). Independent consumer tests **56+32+96** and **1** native helper (**390** filtered) pass on staged source.
2. **Formal integration**: those **13** writes onto selected runtime28 + inventory58 + registry-owner-v2. No passage overrides.

Not release, M2 completion, current authority, writers, five-member binding, S9.3, APFS UUID qualification, or live installation. Root assent is **not** manufactured. Live product was **not** written (`HEAD` `c2e7936`; 587 files; 34 inventory / 50 contract).

**subjectManifestSha256** `02d69e6b3d6116861be9d264bcbc50f7d324c5c60aef235650d85260ba78cde8`  
`docs/implementation/m2/native-runtime-selection-v29-subject.json` **2791** B, **13** members, paths **sorted unique**, **0** pin mismatches. `passageOverrides`: []. `pin_rows` accepts subject (13), candidates (12), parents (3). Candidates cover the subject minus the successor. Parents are not members. Candidate-path reuse on live lock: **0**.

---

## Selected parents (live lock 34 inventory / 50 contract)

Live `design-lock.json` **97091** B `bf1f8788…995e`. Last inventory is v58 `f6c3c307…5806`. Last contract is runtime28 `ec2355e4…9585`. This v29 record is **not** on the lock.

| Parent | Bytes | SHA-256 | Live class |
| --- | ---: | --- | --- |
| runtime28 successor | 3107 | `ec2355e428d4b8fb1f493a6706e534d638b1242c91a4eb3997f21cbb45399585` | selected contract record |
| registry-owner-v2 successor | 24230 | `cf91319a7e83c339000895e11460c3168436d67e5bd35a29289a2f5d87674f04` | selected contract record |
| inventory58 | 280320 | `f6c3c307332bf6bf04994b2ecbf3f2796465587fcd3e9d4c5e6042e13c5d5806` | selected inventory candidate |

---

## Source386 assessment (384+385 composition)

386 archive `5072e6c5…7105` / **7001256 B / 611 members** (591 product); subject.json **115047** B `0d57136f…3665`; **0** member digest mismatches. 385 archive **48** members / **65352** B `f0247e92…fdba`. 384 archive **9** members / **41040** B `43d31cf7…0758`. Every 385 product pin and both 384 security pins are **byte-equal** in 386.

**385 (alloc-only store syntax):** four new identity modules (`store_identity` / `store_selection` / `store_lineage` / `store_marker`) plus seven adapted files. Identity remains `#![no_std]` / `forbid(unsafe_code)`; Cargo.toml/lock **byte-equal** live (no std feature, no package edge). Identity/security Cargo.toml have **no** lifecycle or storage dependency.

- Store-ID: exact 32 lowercase hex; locations/storage map parse errors onto prior owned error tags.
- Selection: decode lives in identity; lifecycle is a facade re-export. Lifecycle **`mod tests` body is byte-identical** to live (7342 B).
- Lineage: identity owns node/walker; OS path moved to `lifecycle::relative_path`, re-exported as `lineage_relative_path`. Lineage tests differ by **one** call site (`selected.relative_path()` → `super::relative_path(&selected)`). 565-case fixture `aa99c66d…56f9` **identical**.
- Marker: 128-byte two-field canonical decode + expected-ID; storage private facade copies `decoded.raw()` once into the prior owned shape; native capture stays in storage.
- Public lifecycle aliases (`DecodedSelectionV1`, `DecodedLineageNodeV1`, `inspect_supplied_lineage`, …) remain.

Initial 385 packaging refused **592 vs 591** because provider import generated `tools/__pycache__/build_contracts.cpython-314.pyc`. `freeze-initial-r1.py` / `freeze-initial-r1-note.json` are preserved; corrected `freeze.py` excludes exactly that path. No source/test failure was hidden.

**384 (project filesystem type):** `NativePlatformEvidence::allows_project_filesystem` checks refusals/local/nonunion/usable fsid, then signed `projectRootFilesystems` membership. It does **not** require I device/`f_fsid` equality. Existing `qualifies_installation_filesystem` still requires install device/id equality. Test: reject `/dev`; System APFS `native_id` differs so installation qualify fails while project-type allows; System is read-only. Type membership is not UUID qualification, custody, tracking, registration, or write authority. Profile/launch TCB standing remains conditional.

**Source386 requiredFindings:** none. This is this review’s source assessment, not a prior lock unit.

---

## Formal integration (map v2 and independent restage)

`stage.py` **5719** B `3a71d80a…b1c4` is byte-identical to selected28. Map: **13** writes + **577** unchanged non-lock; archive `design-lock.json` excluded. `baseProductHead` `c2e7936534246f4294576ca50dfe4a5a02a3a87f`. Independent restage: **611** members verified before output; mapped 13; unchanged non-lock 577; non-lock source **590**; staged lock **byte-equal** live; live product unchanged; `runtimeAcceptance: false`. Staged after-pins equal extract 386.

Independent replay (rustc **1.95.0**, 368 vendor, own target, `HOME=/Users/sb`, Darwin `TMPDIR`, `RUST_TEST_THREADS=1`): identity **56**, lifecycle **32**, storage **96**, all pass; security helper **1** passed / **390** filtered. Author workspace all-targets 17.08s and 385 provider **32** sources / **19** archives (receipt `34058be9…3b63`, carried by 386 equality evidence) were **inspected**, not rerun.

---

## Inventory57 `rootAssessment` field correction

Correction `f563daad…6f77` is **accurate**. Frozen `native-directory-inventory-v57-unit.json` stores a **dict** in `rootAssessment` whose path/bytes/sha256 equal `acceptedInventory` (the peer `inventoryCandidateAssessment` object). `select_inventory57.py` line 6 reads root text into `assessment`, line 21 **overwrites** that name with the peer object, line 40 writes it. `verify_design.py` authenticates `rootSubstantiveAssent` / review / accepted inventory pins, **not** this explanatory field’s type — so selection still verified.

Actual root text exists: `root-assessment.md` **923** B `65726905…9ca1`, **byte-equal** `/tmp/opensip-implementation/inventory57-root-assessment.txt`, and already pinned by selected runtime27 subject. Original unit/selected pins are unchanged (not rewritten). `select_inventory58.py` uses distinct `root_assessment` and `peer_assessment` and asserts the stored field is that string. Remaining residual: the frozen v57 unit still contains the mis-serialized object **by design of this additive correction**. That is recordkeeping, not missing review or assent, and not a source/law change.

---

## requiredFindings

None.

---

## Scope / limits

Does not install source. Does not grant writers, S9.3, full binding, native UUID/profile qualification, or M2–M6. Runtime29 still needs root assent. No Claude concurrence. Root remains lead.
