# Independent review — complete registry-v2 owner381 r2

**Verdict: `ACCEPT-UNIT`** (substantive complete owner/reference)

Bounded OWNER/REFERENCE successor to selected 371 for the 376 durable-root gap. **Not** `ACCEPT-DESIGN-UNIT`, **not** selected law, **not** codec/runtime/inventory, **not** native qualification, **not** S9.3. Formal unit/assent still required. Root remains lead. Live product/codec v1 unchanged.

---

## Pins

381-r2 archive `6f1548a5…c03f` / **34384 B / 56 members**; subject standing unselected complete proposal with corrected caption count; paths sorted unique; **0** pin mismatches. Original 381 archive `f2c11398…2622` / **34216 B / 55 members** is preserved. r2 adds only `COUNT-CORRECTION.md` and retitles README/`freeze.py`/`prepare.py` captions (**10** total overrides = **9** owner + **1** identity, not 11/10). `owner.md`, schema, model, selectors, and case outputs are byte-identical to original 381.

`owner.md` **32488** B `2d4b65c9…179f`. Overrides **11887** B `1da494b0…3f11`. Placement **1328** B `ac657823…b4b3`. Model **14108** B `3eb3741d…ca08` (379 body prefix **12948** B `a4e92df7…c2b7` identical). Source-pins **0** mismatches (includes 379 REVIEW/findings).

---

## 371 retention and 379/ADDENDUM

Overlapping 371 `owner.md` **105** lines unchanged. Exactly **9** updated lines: 1, 3, 13, 17, 21, 25, 27, 29, 44 (title/standing, v2 carrier and v1-absence, schemaVersion 2, NativeProjectRootV2, volumeIdentity, live device/fsid, separate locator/incarnation, unavailable table). `before` texts match selected 371; `after` texts match this `owner.md`. Fourteen appended lines state placement, join, reboot-without-write, clone limitation, and no same-path rebind.

Identity **line 52** is still blank in the parent; the override `before` is `""` and adds the volumeIdentity / v2-carrier / no-rebind bridge. Selected 371 identity **45/48/51/58** and S7/S9 **619/917** are **explicitly inherited**, not replaced (`overlap selectors` empty; verifier-conflicting same-parent rewrites avoided). `s93Selected: false`.

Physical placement names `I/project-registry.v2` and positive `project-registry.v1` absence under the same held parent; standing **not** a repository source-file inventory path. Matches 379 ADDENDUM correction.

Native join `conditional_native_reuse` conjoins complete v2 document, old-carrier absence, qualified-macos-apfs-uuid-v1 profile label, intra-operation `volatile_consistent`, and durable `classify`/marker. Labels are not capabilities; `caller-approved` refuses. Durable MATCHED_ACTIVE does not bypass live device/`f_fsid` mismatch; volatile match does not bypass durable/marker disagreement. Linux remains unavailable until a real qualified kind. No new CLI, implicit rebind, reboot claim, or coherent-clone guarantee.

This closes 379 remaining **owner-document** items (additive identity/placement/S7-S9 inheritance, native join). Codec/runtime/inventory/qualification stay **separate**, as required.

---

## Independent replay (clean copy)

Excluded frozen results and `native-join-faults-r1`. Extract not overwritten.

| Check | Independent | Frozen |
| --- | --- | --- |
| Inherited registry | **274/274** unique ids | byte-equal |
| Persistent 379 cases | **69/69** | byte-equal `a788b509…` |
| Schema + extra-rule | **24/24** | byte-equal |
| Native join | **19/19** unique names | byte-equal `c03c804b…a101` |
| Join faults | baseline 19 + **4** semantic (omit old-carrier / profile / live volatile / durable+marker) | byte-equal `1669c3c0…45cb` |

379 **7** persistent faults, **8** inherited faults, and capacity **320555** remain **carried** (same checker scripts as 379); not counted as fresh 381 native proof. 379 r1 false-negative stays in frozen 379.

---

## requiredFindings

None against this owner/reference artifact.

Still **out of this unit** (not findings): formal design-unit + root assent; v2 codec; native binding/profile qualification; inventory57/runtime27 selection; Linux kind; S9.3.

---

## Scope

No native suite, product edits, commits, push, or manufactured assent. 379 REVIEW/findings/ADDENDUM unchanged.
