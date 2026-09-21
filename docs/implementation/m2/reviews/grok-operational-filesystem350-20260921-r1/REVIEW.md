# Advisory — operational same-filesystem source/ABI (before 350 freeze)

**Standing:** source-and-ABI adjudication only. Not a review of frozen 350, not product approval, not a rewrite of 349. 349 REVIEW `fa46225d…464c` (10157 B) is **unchanged**. No candidate/frozen/history edits.

Independent C probe this session (same `probe.c`, compiled separately) matches the saved `probe.stdout`. Live `mount`: `/dev/disk3s1s1 on / (apfs, sealed, local, read-only)`; `/dev/disk3s5 on /System/Volumes/Data (apfs, local, journaled, … root data)`.

---

## 1. Same-filesystem law — what is inherited, what S3 replaced

**Host-foundation-completion.v2.md §1 is two roots, not one volume for the whole host.**

- **Core payload root** is the immutable installed release (`bin/opensip` …). macOS `.pkg` lives under `/Library/OpenSIP/core/…`.
- **Operational install root** (`installRoot`) is account-private (`~/Library/Application Support/OpenSIP/preview-v1` on macOS). Quote: this root is local APFS (or Linux ext4) **“independently of the core payload's location and the source project's filesystem observation.”**
- Quote: **“All lifecycle publication paths and SQLite sidecars are on this root's one filesystem.”**

That layout rule is about **operational descendants of I** (lifecycle fence, SQLite sidecars, `generations/`, and — by 222 — `I/trust` current/records/events/publications). It is **not** a requirement that `/usr/lib/dyld` or the sealed System volume share that filesystem.

**S3 does not withdraw that layout rule.** Current `docs/v2/contracts/product-v1/security-and-lifecycle.md` S1 table:

| Reviewed source | Selector | Disposition |
|---|---|---|
| host foundation v2 §§1–3 **discovery** | nearest-ancestor `opensip.json` walk to `/` | replaced by S3 |

The replaced selector is **project discovery** (host-foundation §2 walk). S3 restates that walk (custody, VCS/home/root/**mount-change** boundaries). A mount-change **stops project search**; it does not authorize splitting lifecycle/trust publication across mounts. `security-and-lifecycle.md` never restates “one filesystem” and never contradicts it. Compatible inherited §1 layout remains applicable to operational publication paths.

**222 / 203.** 222 places `state.v1`, records, events, and predecessor-keyed publications under **I**, with 203 exclusive no-replace publication and **file/parent durability barriers**. That is within-I physical custody, not a second volume. 222 does not mention `st_dev`/`f_fsid` and does not withdraw host-foundation §1. Cross-volume bind-mount of `I/trust/publications` while `state.v1` stays on I-root would still be a layout violation of §1 and would make 203 parent-durability refer to the wrong filesystem.

**Applicability map**

| Pair | Same operational filesystem required? |
|---|---|
| I-root ↔ `lifecycle.fence`, `I/trust/stores/S/state.v1`, records, events, publications, census descriptors under that I | **Yes** (host-foundation §1 + 222/203 under I) |
| I-root ↔ `/usr/lib/dyld` (348 loader / v8 §8.3) | **No** (host-foundation §1: operational root independent of core/system payload; 349 loader is host TCB) |
| I-root ↔ source **project** root | **No** (host-foundation §2: project FS observed independently) |

Root inference that “every APFS descriptor in the 349 observation must share one id” is **wrong**. The law is **operational I descendants**, not I-root vs dyld.

---

## 2. `st_dev` vs `f_fsid` on this host

Independent live probe:

```
/                    dev=16777232 fsid=16777235,26 type=apfs mount=/                      flags=4480d001  (RDONLY)
/usr/lib/dyld        dev=16777232 fsid=16777235,26 type=apfs mount=/                      flags=4480d001
/private/tmp         dev=16777232 fsid=16777232,26 type=apfs mount=/System/Volumes/Data   flags=04909080  (writable)
/System/Volumes/Data dev=16777232 fsid=16777232,26 type=apfs mount=/System/Volumes/Data   flags=04909080
```

All four share **`st_dev` 16777232**. System (`/`, dyld) and Data (`/private/tmp`, typical I/test trees) **differ in `f_fsid`**. A same-`st_dev` gate cannot tell sealed System from writable Data here, so a “same-device negative” using System vs Data **must fail honestly**. 346/349 `DescriptorFilesystem.device` is `stat` `st_dev`; that remains correct for **inode identity `(dev,ino)`** and for 349’s “do not require I-root.device == loader.device.” It is **not** a mounted-volume identity on this APFS split.

**`f_fsid` is the correct additional native observation** for “this held descriptor is on the same mounted volume as I-root,” with these limits:

- Sample **`fstatfs` on the already-held File/directory**, not a path remount table.
- Record **two `i32` words**. SDK `sys/_types/_fsid_t.h`: `typedef struct fsid { int32_t val[2]; } fsid_t`. libc-0.2.189 BSD `fsid_t` is `repr(C)` with **private** `__fsid_val: [i32; 2]` — layout-compatible, not a public `.val` API. Pins in the audit tree match live SDK/registry hashes; this advisory does not freeze 350.
- Compare operational descriptors’ fsid **to I-root’s fsid**. Do **not** compare them to dyld’s fsid.
- Keep **type / local / non-union on each** descriptor. Equality of fsid is not profile qualification, not `apfs` admission, not a seal.
- **Not** a persistent volume UUID, mount generation, or hostile-kernel proof. Sequential samples, not an atomic snapshot. `vfs_getnewfsid` assigns ids for `statfs`; they can be reused after unmount in principle.
- Refuse unspecified/degenerate ids if the kernel returns them; do not treat “same `st_dev`” as a fallback that reintroduces the System/Data collision.
- Linux `f_fsid` is a different ABI; do not silently reuse the Darwin two-word compare as Linux qualification.

Device remains useful **alongside** fsid for `(dev,ino)` object identity inside a volume. For operational same-filesystem, **fsid is the volume observation `st_dev` failed to provide on this host**.

---

## 3. Correction to the 349 remaining-suggestion

349 remaining said 350 should qualify contributing census descriptors and the held carrier with **type/local/non-union, not device-id equality**.

**Keep:** do **not** require I-root `st_dev` (or fsid) **equal to the 348 loader / `/usr/lib/dyld`**. That was the 349 `filesystems()` split and host-foundation §1 independence of core/system location. Type/local/non-union (loader also read-only APFS) stay.

**Correct:** that “not device-id equality” sentence **must not** be read as licensing **operational I/trust paths** on a different mounted volume from I-root. Inherited §1 “one filesystem” still applies to fence, `state.v1`, records, events, publications, and census files under I. On this Mac, that identity is **`f_fsid` of held descriptors vs I-root**, not `st_dev`.

The draft350 same-`st_dev` negative failing on System vs Data is **evidence**, not a reason to drop same-filesystem for operational paths.

---

## Verdicts

- [x] **§1 one-filesystem layout still applies** to operational I publication/sidecar/trust paths; S3 replaced discovery walk, not that layout.
- [x] **`/usr/lib/dyld` must stay off the I-volume requirement.**
- [x] **`st_dev` is insufficient** here (shared 16777232); **`f_fsid` two `i32` words** are the right additional operation-local observation, with the limits above.
- [x] **349 remaining-suggestion narrowed:** no I-root↔loader device/fsid equality; **yes** I-root↔operational descendants fsid (+ type/local/non-union). 349 REVIEW bytes not edited.
- [ ] **Not** frozen-350 review or approval.
