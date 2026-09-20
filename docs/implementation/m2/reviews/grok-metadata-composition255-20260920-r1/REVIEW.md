# Independent review — metadata composition reference 255 r1

**Standing:** bounded frozen-byte review of `metadata-composition-reference-wip-255-r1`. **Not** full metadata admission, current registry/time/floors, staging, command-to-authenticated-closure join, native publication, or source selection. Archived 254 review (`133979ba…1905`), 254 owner assistance (`OWNER.md` `8b148484…5e36`, `CORRECTION.md` `480bacd9…91cf`), 253 (`dcb6b43b…3169`), and 251 (`1d4d9875…0dce`) were not edited.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Nested 251/252/253/254 archives pin-verified; 247/246/243/248/215/225 siblings reused from already-verified extracts. Frozen fixture/key/result directories were not overwritten. Hardcoded `/tmp/opensip-implementation` test-driver paths were redirected in the review copy only. Candidate helpers have no `/tmp` siblings.

This is **resource-context relocation**: 252/253/254 algorithms become lower security helpers; `Operation` alone owns public `recovery_payload` / `recovery_quorums` / `recovery_metadata` wrappers and outer fail-stop on the same `input_work`/budget. Sharing that budget does not bind the command to the authenticated closure.

---

## Verification

Frozen archive: **16499132 B, 1539 members, SHA256 `335b7b47a25afebd531ba8071b27f093aa5bbab241f5e63138e75782a3d806a5`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 1539/1539. Standing: Incomplete WIP, not approval or source selection.

Included predecessor tars match reviewed pins: 251 r1 `edc0125f…c64b`, 252 r2 `3816972f…ccff`, 253 r1 `164dd2fa…f8b7`, 254 r1 `a22c65bd…5a01`.

Candidate: **1369** files, **16** SHA deltas vs 251 r1 (8 new, 8 changed), **59** pin updates. New subjects: `trust_payload_reference.py`, `trust_quorum_reference.py`, `trust_metadata_reference.py`, four completed manifest/schema/SemVer files, `trust-metadata-composition.v1.md`. Changed: `trust_operation_reference.py` plus five global inventories, operation pins, and current pins.

Included keys are **TEST ONLY**.

---

## What 255 relocates

Three lower helpers import authorization/input/schema/crypto only. Independent AST dump after the documented normalizations (`M.A`→`A`, `M.I`→`I`, `R.prepare`→`R._prepare`, `Q.prepare`→`Q._prepare`): payload/quorum/metadata function and class bodies match 252 `payload_reference.py` and 254 `quorum_reference.py` / `metadata_reference.py`. Helpers expose **`_prepare` only** (no public `prepare`). They do not import `Operation` or `workflows/`, do not construct `Operation()`, and contain no `/tmp` paths. Injected `load()` on payload/quorum is the local module loader, not a production monkeypatch.

The 254 one-member quorum adapter is preserved: `'retainedMetadata': prepared` over 254 source `fce841ec…7c5a` (253 production `d708990d…e788` unchanged). Metadata helper still calls the full completed checker `check_manifest_completed_v1.validate` from `docs/coop/completion/` (pins `48951bd4…7f7a` / `a5140714…90af` / `4931e728…3e93` / `2a7e97a6…9968`).

`Operation` loads `MD = module('metadata255', 'trust_metadata_reference.py')` and owns:

- `recovery_payload` → `self.budget.guard(lambda: MD.Q.R._prepare(self, ...))`
- `recovery_quorums` → `self.budget.guard(lambda: MD.Q._prepare(self, ...))`
- `recovery_metadata` → `self.budget.guard(lambda: MD._prepare(self, ...))`

No class-cache trick or workflow dependency. Failures latch the same budget.

Historical schemas (26 files) and the 49-row inventory (old 45 preserved) are unchanged. Six current workflow modules still contain no temporary paths.

---

## Reproduction

Fresh `metadata-check-live` and `shared-fixtures-live`. Frozen `metadata-check-r1/`, `shared-fixtures-r1/`, `envelope-r1/` were not overwritten.

| Corpus | Result |
|---|---|
| Relocated 254 metadata | **48/48** equal frozen 255 and 254 cases; counters **14 / 40 / 21470** |
| Helpers while minting TEST-ONLY keys | **250 42 / 252 32 / 253 35** |
| Relocated 247 delivery + isolated import/schema/inventory | **38 + 5**, counters 9 / 17 / 6723 |
| Shared metadata + command | **13/13**, combined counters **23 / 57 / 28193** |
| Shared omission controls | **2/2** core-equal frozen variants |

Shared 13: both producer orders; exact/short combined budget; signed-body failure then closed command; command failure then closed metadata; repeated metadata **edges +40** (raw-byte recapture, objects/bytes unchanged); explicit non-join case; helper AST relocation. Isolated candidate import works; local pin tamper still fails.

Two controls alter `Operation.recovery_metadata` on the **same** class and restore it: omit outer `budget.guard`, or call `MD._prepare(Operation(), ...)`. Baseline refuses subsequent command (`operation-budget-closed` / `operation-edge-budget`); mutant wrongly prepares it. Real crypto stays enabled. No native exploit is claimed.

Root suites **inspected, not rerun**: foundation 231, native 477, workflows 2193, security 580, carrier 479, integration 1787; envelope 168 explicit / 147 composition / 1803 historical / 47 payload-dispatch deltas / 55 actual replay-crypto / 6000 fuzz. Pin-file after hashes matched candidate bytes (59/59). Those receipts do not qualify native effects.

---

## Independent probes

| Probe | Result |
|---|---|
| Helper AST vs 252/254 after alias/`_prepare` | equal (extra `load` on payload/quorum only) |
| Helper public `prepare` / Operation import / workflows / `/tmp` | absent |
| `Operation` wrappers | outer `budget.guard` only; no monkeypatch |
| 254 `retainedMetadata` adapter | present in quorum helper |
| Unpresented catalog release / deferred floors / self-class / extra context | same 254 dispositions |
| Repeat metadata | edges +40, objects/bytes unchanged |
| Resource sharing ≠ command-closure binding | explicit passing case |
| Isolated import + source tamper | pass / refuse |
| 254/253/251 reports | hashes unchanged |

v8 `solve` minima and current activation remain **outside** this slice (215 B.5). Unpresented catalog rows are still allowed. Owner-assistance reports are not approval evidence.

---

## Remaining (do not count closed)

Host context custody and current registry identity/retirement; policy/repair/artifact closure; retained revocation population and non-key subjects; other-root chain context; held-root ancestry, floors, current compatibility, S4; command/role/batch effects and native publication; semantic command-to-authenticated-closure join. Fixture policy/artifact bodies remain unverified. GC, evidence commands, mutating transport, native writers, source/runtime selection, M3–M6. 255 is not installed runtime source.

---

## Verdict

- [x] Archive/pins/members verified. **48 / 38+5 / 13+2** reproduced. Helpers 42+32+35 observed. Combined counters 23/57/28193. Relocated 48 cases/counters identical to 254.
- [x] Three lower helpers match reviewed 252/253/254 bodies after documented alias/`_prepare` moves; `Operation` owns public wrappers and outer fail-stop. 254 `retainedMetadata` adapter preserved. Isolated import and tamper hold.
- [x] Independent checks: no helper Operation import, no extra capture class, host-context lock retained, unpresented releases allowed, resource sharing is not command-closure binding.
- [ ] **Not** full member admission, staging, current trust, semantic command join, or native authority.
