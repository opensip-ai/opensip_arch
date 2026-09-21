# Independent investigation — directory enumeration qualification 337

**Standing:** qualification-boundary investigation, **not** code acceptance, profile admission, or authority. Frozen packet `native-enumeration-qualification-investigation-337`. Product remains `fa72e50`. 336 REVIEW was read and is **unchanged**. 330–336 product code is **not** in this packet and is not re-accepted here.

Python 3.12.13 `-I -B` for pin/extract. Independent host probe and upstream fetch are **development observations**, not release qualification.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **121732 B, 20 members, SHA256 `8ffdbfe69eeb8240211eccb49d439576d9d034e266c4040ddc75105639948a7b`**. Extract 20/20. 336 REVIEW `2c317a30…afc5` unchanged. Candidate-context pins match live 330/334/336 archives.

Local source pins rehashed equal: `security-completion.v8.md` `54f3a690…8c2d`; `security-freeze.v8.json` `33dad5ec…44ca` (same pin as `architecture-application.v1.json` security.freeze). Independent fetch of pinned Apple Libc `71bbe350…1a64` `readdir.c` / `opendir.c` SHA-equal packet (`b6ba492f…4c6d` / `7d81f6cc…d951`). **Not** a match to installed `libsystem_c.dylib`.

Independent read-only probe (open `/private/tmp/opensip-implementation`, `fstatfs`/`dladdr`): macOS **26.6.2 / 25G83**, Darwin **25.6.0** arm64, **APFS local=1 union=0**, `readdir` in `/usr/lib/system/libsystem_c.dylib`, SDK **27.0**, `dirent.h` SHA `46d55897…196d` (8703 B) matching `sdk-pin.json`. `getdirentries` is a **link-error** spelling under 64-bit inodes; **no** public `getdirentries64`. Do not invent a private syscall or `scandir` whole-dir allocator.

Issue 8 POSIX URL was not retrieved (same failure the packet discloses). Issue 6 / IEEE 1003.1-2004 `readdir` was read.

---

## Incorporation and threat boundary (adjudication)

`security-freeze.v8.json` still labels itself `FROZEN-PROPOSED; awaiting LEAD-CORRECTION-REVIEW 3`. `architecture-application.v1.json` is `WORKING-INTEGRATION-NOT-FROZEN-OR-ADOPTED` but records security **ACCEPT** with that freeze pin and `security-lead-review.v3.json` ACCEPT / mustFix 0. **Do not** read the old freeze header as current standing; **do not** treat the whole architecture application as frozen. The incorporated **security v8 text** is the threat-model source for this question.

**§1 assumed TCB:** OS kernel and distribution signing chain, platform loader and libc, first-party trusted code with the invoking user’s ambient authority. **Out of scope:** compromised kernel/signing chain, local root, hostile kexec kernel, coherent unmarked whole-root rollback. Nothing claims confinement of first-party code or hostile-kernel detection.

**§8.8:** macOS verify-to-spawn residual window “can be raced only by same-UID code, which is inside the explicitly trusted first-party boundary of §1.” That **scopes** same-UID races **into the TCB**; it does **not** make a permission sample an enduring grant. First-party locking, correct lifecycle, no extra write-capable principals, and retaining the right objects through consumption remain **implementation** obligations (physical 203: parent admission, no-follow open, retained name identity, local FS qualification, **exclusion through use**).

**Answer:** this does **not** require an impossible raw-slot / hostile-TCB completeness theorem. It requires a **declared supported profile**, **native custody constructors**, and a **held cooperative installation fence** through enumeration, content, and dependency consumption. Recurring “libc holes / enduring exclusion” language is **overbroad** if it is read as “prove every on-disk slot including deleted remnants against a malicious kernel.” It is **not** overbroad if it means “do not treat EOF as census without fence + profile + constructors.”

---

## POSIX / Apple / upstream vs supported non-union APFS

POSIX Issue 6: a directory stream is an ordered sequence of **directory entries representing files**. After `opendir`/`rewinddir`, whether `readdir` returns an entry for a file **added or removed** is **unspecified**. NULL + unchanged errno is EOF; NULL + errno is error. That is an **API contract**. Concurrent mutation is a **missing fence**, not a libc bug and not a TCB-compromise theorem.

Apple archived `getdirentries(2)`: skip `d_fileno = 0` because those are **deleted but not yet removed**. Unused raw slots are **not** extra live candidates. Historical page; not a modern ABI proof.

Pinned `readdir.c` (verified): `readdir()` calls `_readdir_unlocked(..., RDU_SKIP)`. Skips `d_ino == 0` when `RDU_SKIP`; skips `DT_WHT` when `DTF_HIDEW`. Malformed alignment/`d_reclen` returns **NULL without setting errno**. Pinned `opendir.c` / `fdopendir`: flags `DTF_HIDEW | DTF_NODUP`; **union stack** uses `_filldir` whole-directory cache. 330 already refuses `MNT_UNION` (and UNION|LOCAL) **before** `fdopendir`. Ordinary non-union path is buffered `readdir`, not `_filldir`.

**In-scope live-canonical hide?** Packet and this review have **no constructive repro** of a **live regular canonical file** omitted on **valid non-union APFS** via inode-zero, whiteout, or malformed-buffer NULL. Those skip paths map to: deleted remnants; **union** whiteouts (already refused); **corrupt buffer / kernel-libc failure** (hostile or broken TCB, §1 out of scope unless empirically seen on the declared profile). **Do not** assert whiteouts impossible. **Do not** silently widen the threat model to require defeating them.

**Genuine in-scope namespace issue (already observed, not a whiteout):** 334’s case-insensitive APFS collision (`A64` vs `a64`) is a **supported-profile alias**, not TCB compromise. A declared profile must either require a case-sensitive volume or treat canonical-name collisions as **unavailable**, not as two live descriptors.

Malformed-buffer EOF-without-errno on a **planted complete** non-union directory (missing planted name, errno 0, `fstatfs` ok) would be an **empirical profile fail**. **Not observed** here.

---

## Concrete minimum producer / qualification checklist

Keep public `fdopendir` / `readdir` / `closedir` and 330’s errno/cap/union checks. **Do not** add private `__getdirentries64` or `scandir` as a completeness workaround.

| Item | Owner | Status here |
|---|---|---|
| Declare FS profile: local, non-union, APFS (or named other), **case-sensitivity** | qualification | **unqualified** for release |
| `fstatfs` refuse UNION; record fstype/local | 330 constructor | implemented; **not** host-certified |
| Held installation fence from root through enum + content + deps | 203 / protocol | **owed**; 332/333 samples are **not** that fence |
| Root-to-leaf native policy + no-follow opens | 331–333 | implemented as samples |
| Charge **all returned names** before materialization; 64 canonical; foreign untouched | 222 PERSISTENCE 125 / 334 | implemented for **OS-returned** names |
| Planted canonical round-trip under fence on the **declared** volume | empirical | **not done** (this probe only `fstatfs`/`dladdr`) |
| Case-fold / collision policy | profile | **owed** (334 collision is the warning) |
| Wrong native errors, mutating first-party writers, ancestor/path constructors | product tests | still owed; not “API therefore done” |
| Loader/libc **binary** pin, boot/runner class, durability | v8 §8.7/§8.8 | **not** this Mac 26.6.2 observation |
| Linux ACL/enumeration | 332+ | unsupported; no Linux run |

336 structural successor output stays **non-authoritative** until these native producers and gates are joined.

---

## Findings

The investigation’s disposition (1–5) is **sound** against incorporated v8 §1/§8.8, POSIX live-entry semantics, Apple’s inode-zero-as-deleted instruction, pinned skip/whiteout/union-preload source, and 330’s UNION refuse. Recurring review caveats should be **narrowed** to: (a) missing fence ⇒ unspecified membership; (b) undeclared FS/case profile; (c) empirical planted-name failure on that profile; (d) still-unimplemented constructors. They should **not** be repeated as a demand to enumerate deleted slots or to survive hostile kernel/root.

**No actionable source/reproducer** in this packet for a supported valid non-union APFS state hiding a live canonical regular descriptor via whiteout or malformed-buffer EOF. Evidence limit: upstream source ≠ installed libc; this host ≠ release runner.

**Actionable defects in this freeze:** none in the investigation packet’s source standing. This review does **not** install code, qualify the environment, or change accepted law.

---

## Remaining (do not count closed)

Release-class TCB/FS qualification; case-sensitivity policy; fence-through-consumption constructors; planted-name empirical suite; 336→authority join; Linux; M2–M6.

---

## Verdicts

- [x] **337 adjudication:** incorporated v8 TCB does **not** demand a raw-slot/hostile-TCB theorem; it demands supported-profile + custody constructors + held cooperative fence. POSIX concurrent mutation is unspecified without that fence. No in-scope whiteout/malformed hide repro for live canonical on non-union APFS; case-insensitivity **is** in-scope. Host probe is not release qualification. 336 reports preserved.
- [ ] **Not** profile admission, environment qualification, code selection, or product installation.
