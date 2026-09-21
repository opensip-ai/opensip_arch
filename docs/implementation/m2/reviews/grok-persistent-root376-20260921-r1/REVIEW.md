# Persistent native root identity 376 — owner-gap audit

**Verdict: OWNER-GAP CONFIRMED** (question, not a selected proposal)

Selected NativeProjectRootV1 persists raw descriptor `deviceId` (`st_dev` / canonical Linux device encoding) as part of live incarnation. GNU C Library 2.30 Attribute Meanings documents that `st_dev` need not stay consistent across reboot or crash. The selected reference then classifies an otherwise identical same-path observation as `CONTRADICTION`, and the selected move rule cannot repair it because the locator is still present. That is a real **owner-law availability gap** for legitimate restart/remount on supported profiles. It is **not** proof this host rebooted, **not** a deployed native-registry defect, **not** a codec373 bug, and **not** authorization to change law.

This trial is a question. No owner/schema/codec successor is accepted here. Root assent is **not** manufactured. No code, CLI, product, commit, or push. Frozen 373 implements current exact-equality law correctly and is not native root authority. Runtime26 selection is separate. Directory-birth375 remains unreviewed and excluded.

---

## Subject pins

`docs/implementation/m2/trials/persistent-root-audit-376-r2/subject.json` **1811** B SHA-256 `cb1fbb284c070e30fb559c0de3c34bee3724e80b34d73546d15da9ceb2091895`, **8** members, sorted unique, **0** mismatches. Standing: unreviewed owner availability question; corrected executable fixture.

Original frozen 376 is preserved: `reproduce.py` SHA `9f1fb41f…78a3` still supplies `birthSeconds` as a string; `reproduction.json` is empty `e3b0c442…`. Independent replay of that script exits 1 at `validate_root`/`exact_int` (`Refused: integer`) inside the first `classify` call — before either semantic assertion completes. 376-r2 changes only that fixture to integer `1700000000`. Independent replay exits 0; stdout is **byte-equal** frozen `reproduction.json` `57967ac2…910e` / 919 B: baseline `MATCHED_ACTIVE`, after `deviceId` `2049`→`2050` `CONTRADICTION`, `sameLocator` true. `counterexample.json`, `QUESTION.md`, `primary-source-followup.md`, and `local-source-pin.json` are byte-identical to original 376.

Selected pins used: owner.md `14181ef7…9c8c` / 27933 B; schema `545e0006…6294` / 2858 B; `registry_model.py` `b9c1a19a…6e19` / 11440 B; identity-and-evidence.md `c82404f3…d31f` / 135448 B. CFURL.h pin `4c398dc7…d5ce` / 82776 B matches `local-source-pin.json`.

---

## Selected law (identity + registry owner)

Identity §2 (lock after-image, including owner-v1 passage overrides): marker and private registry must agree; missing both is first use; agreement is reuse; unilateral or contradictory presence refuses and needs explicit recovery/adoption; never a silent choice. A root **move** preserves ProjectId only through an authenticated registry move with **no live reader or writer**, EXCLUSIVE on that N; duplicate simultaneous roots refuse.

Registry owner NativeProjectRootV1 is closed `{platform, canonicalPathBytesHex, deviceId, inodeId, birthSeconds, birthNanoseconds}`. macOS takes device/inode/birth from the **retained directory descriptor**; Linux takes `statx` identity with `STATX_BTIME` present and canonical Linux device encoding. Live uniqueness is ProjectId, locator `(platform, path)`, and incarnation `(platform, deviceId, inode, birth)`. `classify` requires the observed root **object** to equal the row (`row['root']!=root` → `CONTRADICTION`). `locator_key` is `(platform, path)` only. Move: ACTIVE→ACTIVE, root bytes change, **old locator positively absent** (not inaccessible), identical admitted marker, fresh native admission. Same-object rename may preserve incarnation; cross-filesystem relocation may bind a new incarnation **only under that move**. No implicit move from matching marker bytes or a new pathname. Adoption is portable-bundle / fresh local N, not same-path device rebind. Recovery must re-prove recorded root incarnation/locator; it does not rewrite `deviceId` because `st_dev` changed.

Codec373 decodes that closed root and preserves exact `deviceId` spelling. That is correct for **current** law.

---

## Is persisted raw `st_dev` an availability gap?

**Yes, as selected-law availability**, conditional on GNU’s documented instability — not as an executed reboot on this host.

Independently fetched https://sourceware.org/glibc/manual/2.30/html_node/Attribute-Meanings.html : `st_dev` “is not necessarily consistent across reboots or system crashes.” The search PDF snapshot is **not** claimed fetched (follow-up: 404).

Installed SDK CFURL.h lines 831–832: `kCFURLVolumeIdentifierKey` “is not persistent across system restarts.” Lines 1090–1091: `kCFURLVolumeUUIDStringKey` is “the volume’s persistent UUID as a string, or NULL if a persistent UUID is not available.” That **does not** prove the CF identifier equals `st_dev`. Product observer already states `f_fsid`/`native_id` is an operation-scoped mounted-filesystem ID, **not** a persistent UUID, and that APFS volume groups may share `st_dev` while those IDs differ. Replacing stored `st_dev` with `f_fsid` would not make a durable key.

Conditional model (376-r2): same ProjectId, marker, path, inode, birth; only `deviceId` changes; locator still present → `CONTRADICTION`. Move cannot apply. Ordinary read must not write. Identity §2 would treat this as contradictory presence, i.e. refuse reuse. After a real reboot that actually changed `st_dev`, a still-present project at the same path would be unavailable for MATCHED_ACTIVE until an owner that does not yet exist. Native registry reuse is not implemented, so this is **not** a live production incident.

---

## Already-selected same-path repair?

**No.**

| Existing act | Why it does not cover same-path `st_dev` change |
| --- | --- |
| Move | Old locator must be positively absent; path still present |
| Same-object rename | Path/locator change; may *preserve* incarnation, not rewrite device at the same path |
| Cross-FS relocation | New incarnation only under move, still needs old locator absent |
| Adoption | Portable bundle + new local N; marker/caller flags are not authority |
| Reservation recovery | Must agree with **recorded** incarnation; would still CONTRADICT |
| Codec/classify weakening | Would confuse clones, replacements, and two live roots |

There is no selected “deviceId-only same-path rebind.”

---

## Smallest complete owner correction

Not approved by this audit. Smallest **complete** successor (owner + schema + model + later codec), **before** native reuse is built:

1. **Stop persisting raw `st_dev` as durable incarnation.** Keep capturing `st_dev` and `f_fsid` on the **held** descriptor for intra-session identity (APFS System/Data already share `st_dev` on this platform). Do not drop those live checks.

2. **Durable MATCHED_ACTIVE / live-uniqueness key** = locator + inode + birth + a **platform-qualified persistent volume identity** obtained only through the retained descriptor. macOS: persistent volume UUID **when present**; NULL is unavailable, not a fallback to `st_dev`. Restart-scoped `kCFURLVolumeIdentifierKey` must not be the durable key. Linux: an independently specified descriptor-native volume/superblock identity, or this profile refuses persistent reuse. Missing qualification refuses ordinary reuse after the descriptor is gone.

3. **If that durable identity is unchanged**, identity §2 “agreement is reuse” can MATCHED_ACTIVE without a registry write and without treating reboot as a move.

4. **If durable identity is missing or disagrees**, UNAVAILABLE or CONTRADICTION as appropriate — never silent MATCHED_ACTIVE, never auto-adoption, never a fake OLD_LOCATOR_ABSENT.

5. **Independently authorized same-path continuity / rebind** is only for cases where durable volume identity itself must change (new disk, copy, restore onto another qualified volume). Prove continuity from reacquired descriptors + exact marker + ProjectId + locator + inode/birth/custody; UUID or marker bytes alone are not unforgeable history. Not a new CLI; existing operation owners authorize. Not ordinary read.

6. **Clone/collision:** same volume identity plus copied inode/birth/marker still refuses or requires explicit fork/adopt. Complete descriptor-native acquisition, FS gate, and updated schema/model/codec reviews are mandatory. 373 stays the current-law codec until that successor. 375 birth mutability is a separate reason the current tuple is not authority; it is not reviewed here.

---

## requiredFindings

None against this question artifact. The next owner unit must carry the six requirements above. This file does not select them.
