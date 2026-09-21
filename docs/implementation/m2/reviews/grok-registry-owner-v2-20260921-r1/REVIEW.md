# Formal selection — native ProjectId registry owner v2

**Verdict: `ACCEPT-DESIGN-UNIT`**

Formal **registry contract selection** of exact accepted owner381-r2 (OWNER/REFERENCE `ACCEPT-UNIT` `94e4b5ea…432a`) plus ten passage overrides, physical placement, and the selection README’s project-root filesystem qualification. Does **not** implement a v2 codec, qualify native APFS/Linux, select S9.3 or full binding, grant writers, or close M2. Does **not** relabel 381-r2 OWNER/REFERENCE `ACCEPT-UNIT` as this formal acceptance. Root assent is **not** manufactured.

**subjectManifestSha256** `abfa0cf16ec8f1439b8443612c25aec467e20b4587baab3e9c45f81cac659f0e`  
`docs/implementation/m2/project-registry-owner-selection-v2-subject.json` **10113** B, **46** members, paths **sorted unique**, **0** pin mismatches. `pin_rows` accepts subject (46), candidates (45), parents (6). Candidates cover the subject minus the successor record. Parents are not members of this subject. No candidate path is already accepted on the live lock (lock join will not fail by reuse).

381-r2 trial archive in this subject: **34384 B / 56 members / `6f1548a5…c03f`**, archive-pin matched before private extract. Original 381 **34216 B / 55 members / `f2c11398…2622`** remains preserved as 381-r2 history (`COUNT-CORRECTION.md`); it is not a competing current owner.

---

## Six parents (live lock 33 inventory / 48 contract)

Live `design-lock.json` **94112** B `03560e61…1be9`. Independent `verify_design.py` against architecture **passed** (`productQualification: false`). Last selected contract is runtime27 (`8fdf8fea…c5d7`); this v2 record is **not** on the lock. Runtime27 installation is a **separate** unit (HEAD `c27ffa4`, 587 tracked files; adapters under `crates/platform/src/filesystem/`). This review does not re-judge it.

| Parent | Bytes | SHA-256 | Live class |
| --- | ---: | --- | --- |
| security-lifecycle.schemas.v1.json | 135672 | `f66d2c61…23f4` | lock input (original accepted design) |
| v1 `owner.md` | 27933 | `14181ef7…9c8c` | selected v1 contract candidate |
| v1 `project-registry.schema.json` | 2858 | `545e0006…6294` | selected v1 contract candidate (historical) |
| v1 `successor.json` | 11178 | `0909f44a…28f4` | selected contract record |
| identity-and-evidence.md | 135448 | `c82404f3…d31f` | lock input |
| security-and-lifecycle.md | 119915 | `a319da39…d9d6` | lock input |

Parent paths are lexicographic. All six match accepted sha256/bytes.

---

## Ten exact overrides; 371 identity/S7/S9 inherited

`successor.passageOverrides` **equals** `effective-owner-overrides.json` (10). Nine prior-owner lines **1, 3, 13, 17, 21, 25, 27, 29, 44**; unused identity **line 52** (`before` `""`; parent line still blank). Every `before` string **exactly matches** the cited parent line. Every owner `after` string **equals** the corresponding v2 `owner.md` line.

Selected 371 identity **45/48/51/58** and S7/S9 **619/917** are **not** in this successor. They remain the v1 record’s overrides. Conflicting same-parent replacements on the live lock: **0**. `s93Selected: false`. Identity 52 after-text states S9.3 is not selected by that paragraph.

Overlapping 371 `owner.md`: **114** lines → v2 **128**; **105** unchanged; **9** updated; **14** appended (placement, join, reboot-without-write, clone limit, no same-path rebind).

---

## Exact 381-r2 owner / schema / reference

Private extract of pinned 381-r2 tar; unit bytes are identical:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `owner.md` | 32488 | `2d4b65c9…179f` |
| v2 schema | 3165 | `b7d8340e…db21` |
| `registry_model.py` | 14108 | `3eb3741d…ca08` |
| overrides | 11887 | `1da494b0…3f11` |
| physical-placement | 1328 | `ac657823…b4b3` |

Model is the 379 prefix **12948** B `a4e92df7…c2b7` plus `conditional_native_reuse`. Frozen 381 join results `c03c804b…a101` / faults `1669c3c0…45cb` are subject members; 381 independent replay is **not** rerun. 379 REVIEW/findings/ADDENDUM in this subject are byte-equal this reviewer’s 379 artifacts (`96ce7dbc…`, `109afed9…`, `3410b4fc…`). 381 REVIEW/findings likewise (`94e4b5ea…`, `102f245d…`).

Owner/schema files still carry 381-r2 “proposed / NOT accepted” captions, as v1 kept its DRAFT header. Standing for this unit is review + root assent + lock successor, not a silent caption rewrite.

---

## Current law vs historical v1

`registryProfileReplacement`: current owner/schema/placement are the v2 pins above; former v1 owner/schema remain immutable parents. `legacyNativeReadAllowed: false`. `silentMigrationAllowed: false`. v1 schema keeps `deviceId` / `schemaVersion` const 1; v2 schema has `volumeIdentity` / const 2 / platform `macos` only — no `deviceId`. No other selected contract currently names a registry owner. After assent and lock composition, v2 is the current native registry profile; v1 is historical syntax only.

Live product codec `crates/identity/src/project_registry.rs` is still frozen 373 (**10940** B `f3bb0fb6…`); decode refuses `schemaVersion != 1`. README states that 373 remains inert historical v1 until a **separately reviewed** v2 implementation. That is implementation lag, not a second owner.

Physical placement: sole current name `I/project-registry.v2`; positive `project-registry.v1` absence under the same held parent; **not** a repository inventory row. Inventory57 contains **0** `I/` or `project-registry` source paths. Marker 92-byte frame, namespace lease paths, and fence domain unchanged. `publicCommandsAdded: []`. `newStoredStoreGenerationBinding: false`.

---

## Project-root filesystems vs I same-device/fsid

The selection README adds a qualification **absent** from 381-r2’s README: native project filesystem qualification must use the existing signed profile’s `projectRootFilesystems`, not silently impose installation I’s same-device/fsid predicate on repositories elsewhere. The native producer remains independently outstanding.

Pinned `PlatformProfileSetV1` already requires **both** `installRootFilesystems` and `projectRootFilesystems` (macOS both `const` `apfs`; Linux both enum `ext4`/`xfs`/`btrfs`). That is an existing signed field, not an invented one. Security `platform_admit` currently consumes `installRootFilesystems` for I/boot TCB. Native 350 same-device/`f_fsid` equality is I operational descendants versus retained I-root samples. Owner381 (exact bytes) keeps live device/fsid as **intra-operation** volatile consistency on the admitted project root; those numbers do not enter the durable JSON key and are not specified as equality with I. Root’s 381 source assessment already distinguished `projectRootFilesystems` from installation same-device checks. This unit does not select a Linux profile, a new signed field, or native qualification.

---

## Whole-v2 rules (owner + model, not native proof)

Positive old-v1 absence: present/unavailable old name refuses; two absences are not pristine creation (`carrier_observation`). No implicit first-use or migration. Locator uniqueness `(platform, path)` is separate from durable incarnation `(platform, kind, value, inode, birth)`. Same-present-path durable change is contradiction, not rebind. Coherent indistinguishable copy remains a disclosed limit. Allocation/adoption/kind/recovery/lease/durability text is the retained 105 371 lines. `conditional_native_reuse` conjoins complete v2 document, old-carrier absence, qualified-macos-apfs-uuid-v1 **label**, intra-operation `volatile_consistent`, and durable classify/marker. Labels are not capabilities.

Inspected 381 REVIEW in full (pins, 371 retention, 379 ADDENDUM corrections, join conjunction, carried 274+69+24+19+4 evidence, empty requiredFindings) and 379 ADDENDUM in full (inert 375/378 may integrate before qualification; `I/project-registry.v2` is not an inventory row; inherit 45/48/51/58 and 619/917). Those owner-document items are closed by these exact bytes. Native qualification, v2 codec, writers, S9.3, and M2 remain open.

---

## requiredFindings

None.

---

## Scope / limits

Does not select codec, native producer, Linux kind, S9.3, full binding, writers, current authority, or release. Does not install this successor onto the live lock. Root must still record **substantive assent** and compose the lock successor; this file is not that pin. No Claude concurrence.
