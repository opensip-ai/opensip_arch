# Independent review — proposed registry owner379 (root persistence)

**Verdict: `ACCEPT-PROPOSAL-DIRECTION`**

Coherent working proposal for the 376 availability gap. **Not** formal design-unit acceptance, **not** selected law, **not** codec/runtime/inventory, **not** native qualification, **not** S9.3. The draft itself says version/placement overrides are unfinished and it cannot be selected without them. Root remains lead. Assent is **not** manufactured. Live product/runtime26 unchanged.

---

## Pins

Archive `1a953961…792e0` / **24504 B / 106 members**; subject standing unselected working proposal; paths sorted unique; **0** pin mismatches. `owner-draft.md` **8890** B `e1676adb…299b`. Source-pins (371 owner/schema/model/successor, 376 REVIEW+ADDENDUM+root-assessment, identity, S9) **0** mismatches vs architecture.

Independent replay in a **clean copy** that omitted frozen results and `persistent-faults-r1`/`r2` / `fault-runs-*`. Frozen extracts were **not** overwritten.

| Check | Independent | Frozen |
| --- | --- | --- |
| Inherited `check_registry.py` | **274/274**, unique caseIds | byte-equal `f7792067…ea0e` |
| Persistent `check_persistent_root.py` | **69/69** unique names | byte-equal `a788b509…cc52` |
| Schema + extra-rule | **24/24** | byte-equal `f8a8b60f…c3ef` |
| Persistent faults r2 | baseline 69 + **7** semantic detections | byte-equal `c3716a66…a7d8` |
| Inherited 371-style faults | 8 detections after baseline | (copy-local; frozen r1 partial retained) |
| Capacity max wrapper | **320555** | same bound as 371 |

r1 fault classification false-negative (Python `repr` double quotes vs required single quote) is preserved under `persistent-faults-r1/`; r2 `ast.literal_eval` of the assertion tuple against the 69-case baseline is the counted evidence.

---

## vs selected 371 and audit 376/377

371 five-member entries, statuses, allocationKind, marker 92-byte frame, fence/lease/recovery/adoption/move (old locator absent) remain. Durable root **substitutes** `volumeIdentity` for `deviceId`; envelope **schemaVersion 2** on a **new** `I/project-registry.v2` name. Old v1 present / unreadable / both / missing-v2-in-established → unavailable; no silent migration. Matches “no device-only automatic rewrite.”

376 six correction points: (1) raw `st_dev` not durable, live device/`f_fsid` kept; (2) qualified APFS UUID from held descriptor, NULL/zero/unsupported unavailable, Linux not invented; (3) unchanged durable fields MATCHED_ACTIVE with **no write**; (4) durable change at still-present path CONTRADICTION, not fake move; (5) **no implicit same-path rebind** (deferred; root’s 376 assessment allows refuse rather than invent); (6) coherent indistinguishable clone stated as a **limitation**, not universal detection. Locator uniqueness `(platform,path)` stays **separate** from incarnation `(platform,kind,value,inode,birth)` — combining locator into incarnation is a detected fault (`locator-inside-incarnation`). 377 remains one-host ABI feasibility only; draft does not treat 375/378 as qualification.

This is the **smallest coherent** owner-direction: new v2 carrier (avoids reinterpreting frozen v1/codec373), one initial kind, retain 371 gates, refuse rather than add a rebind CLI.

---

## Remaining requirements (before any formal selection)

Draft §Required next work is accurate. Exact work still missing:

1. **Effective-owner passage overrides** on selected identity-and-evidence (371 currently lines 45/48/51/58): native incarnation is no longer `(deviceId,inode,birth)`; agreement/reuse must name durable `volumeIdentity` + separate locator/incarnation uniqueness; no silent v1 read.
2. **Physical placement:** sole live carrier `I/project-registry.v2`; positive **absence** of `I/project-registry.v1` under the same held parent/custody before ordinary v2 admission; unreadable old name is unavailable, never init. Closed-directory/inventory successor for the new name.
3. **S7/S9:** 371 overrides at security-and-lifecycle 619/917 likely still apply (NamespaceList strings unchanged) but must be **re-pinned** or explicitly inherited; S9.3 stays proposed.
4. **Native admission join:** `classify` durable equality **AND** intra-operation `volatile_consistent` (device/`f_fsid`); missing UUID/birth/profile unavailable; 375/378 remain unselected samples until a qualified profile.
5. **Codec/inventory/runtime** successors after this owner is selected; 373 stays current-law v1 codec until then.
6. **Linux** remains unsupported until an actual qualified kind exists.
7. **Same-path durable-identity change** (new disk at the same path) stays CONTRADICTION; existing adoption/move/fork only within their scope. Do not add a CLI. Birth mutability is still in the durable tuple (375), out of this unit.

`requiredFindings` against this **proposal-direction** artifact: none. Those seven items block **ACCEPT-DESIGN-UNIT**, not this verdict.

---

## Scope

No native suite, product edits, commits, push, or law selection. 375/378 ACCEPT-UNIT reviews unchanged. 376 OWNER-GAP CONFIRMED unchanged.
