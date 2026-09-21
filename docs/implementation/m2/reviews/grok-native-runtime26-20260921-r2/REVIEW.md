# Native runtime selection26-r2 — design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Metadata-only sort correction of runtime26. Original frozen subject `05a44e60…bec7` / 7794 B and successor `bdf45e2d…4c9a` / 8329 B remain **byte-unchanged** and historically `NEEDS-CHANGES`. This unit does **not** re-select source, inventory, or stage.py. Not release, not M2 completion, not current authority, not writers, not five-member binding, not S9.3, not native registry admission, not directory-birth375, not product installation. Root assent is **not** manufactured. Live product was **not** written (`HEAD` `c57b816`).

**subjectManifestSha256** `2c36c1a65e841c570e6b880457ddd673dbed7f412daf729a1c2829771b605dbd`  
`docs/implementation/m2/native-runtime-selection-v26-r2-subject.json` **7797** B, **36** members, paths **sorted unique**, **0** pin mismatches. `passageOverrides`: [].

r1 REVIEW (arch and `/tmp`, SHA `bc115ef8…1ed1` / 4227 B) and root-assessment were read. Root agrees the r1 finding was pathlib-component vs serialized-path sort. This r2 is that sort-only successor.

---

## r1 finding closed

`pin_rows` (`tools/verify_design.py` 146–152) now accepts:

| List | n | sorted unique |
| --- | ---: | --- |
| subject `files` | 36 | **yes** |
| successor `candidates` | 35 | **yes** |
| successor `parents` | 3 | **yes** |

Original v26 lists still refuse (frozen). Parents order is now runtime25 successor, owner-selection-v1 successor, inventory56 — lexicographic serialized paths. Trial members list `checkpoint-373-r2/` before `checkpoint-373/` (`-` < `/`).

---

## Original comparison (36 minus 1)

| Path | Role |
| --- | --- |
| `native-runtime-selection-v26/successor.json` | original only; still on disk `bdf45e2d…` / 8329 B |
| `native-runtime-selection-v26-r2/successor.json` | r2 only; `353581fe…` / 8329 B; subject row matches |
| 35 shared paths | **identical** path/bytes/sha256; 0 diffs |

r2 successor standing, schemaVersion, `passageOverrides` `[]`, parent pin-set, and candidate pin-set equal the original. Only array order changed. Candidates cover the subject minus the new record; each candidate pin equals the subject row and the file on disk. Parents are not members of this subject.

---

## Selected parents and prospective composition

Three **selected** live bases (lock 32 inventory / 46 contract):

- runtime25 successor `1d51c00c…deab` / 8692 B
- registry-owner-selection-v1 successor `0909f44a…828f4` / 11178 B
- inventory56 `8935bf9d…786c` / 277494 B / 699 files

Feasible `contract_successor` checks **without** manufacturing assent: pin_rows pass; record is in the subject; candidates cover the rest; parents are accepted inventory/contract pins; parents would not be overwritten; overrides empty. Review tokens here are `ACCEPT-DESIGN-UNIT` / `requiredFindings: []` / this subject SHA. The fifth bind (`assent`) remains root’s. Map/stage/archive composition is unchanged from r1 (stage.py still `3a71d80a…`; 3 writes / 581 unchanged non-lock; 374 archive 615). Metadata-only: restage and native suites were **not** rerun.

---

## requiredFindings

None.

---

## Scope / limits

Does not install source. Does not activate this contract. Does not discharge S9.3, full binding, native registry admission, or directory-birth375. Persisted `deviceId` across reboot/remount remains the next task. Historical r1 stays `NEEDS-CHANGES`.
