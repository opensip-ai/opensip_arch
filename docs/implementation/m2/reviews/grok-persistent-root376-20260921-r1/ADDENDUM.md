# ADDENDUM — one-host volume UUID ABI probe 377

**Standing:** evidence supplement only. 376 REVIEW.md (`49d2dee…7773`, 8701 B) and findings.json (`e77a8eb…d975`, 4636 B) are **unchanged**. Verdict remains **OWNER-GAP CONFIRMED**. Probe 377 is not product, not qualification, not a selected schema, not a reboot test, and not clone/collision/history proof. No product/design edits.

---

## Frozen probe pins

`docs/implementation/m2/trials/volume-identity-probe-377/subject.json` **1768** B SHA-256 `f7c64acb33866f52e97370109604026c36599109e5c36d06d23082ac06fc2a94`, **8** members, sorted unique, **0** mismatches. Standing: unreviewed read-only one-host ABI exploration.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `README.md` | 1653 | `418b5b30…21a7` |
| `probe.c` | 2370 | `eacf677d…bd51` |
| `native.stdout` | 509 | `9a397433…d67e` |
| `primary-inputs.json` | 592 | `a5b648de…aef8` |

SDK inputs rehashed: `sys/attr.h` 27496 B `5118b924…eefe`; `getattrlist.2` 64385 B `866c79ab…e34b`. Compile/native stderr empty; both commands exit 0 in `commands.json`.

---

## What the log actually shows

`probe.c` calls `fgetattrlist` on an original nested directory FD with `ATTR_CMN_RETURNED_ATTRS` and `ATTR_VOL_INFO|ATTR_VOL_UUID`, 40-byte buffer, `FSOPT_REPORT_FULLSIZE`. Independently decoded `native.stdout`:

- Nested directory and `fstatfs`-discovered mount root both `callResult` 0, `errno` 0, `frameBytes` 40.
- Returned masks `[2147483648, 262144, 0, 0, 0]` = `ATTR_CMN_RETURNED_ATTRS` (common) + `ATTR_VOL_UUID` (vol); dir/file/fork zero. Layout matches `attribute_set_t` after the length word; UUID occupies bytes 24–39.
- Same nonzero UUID `f3232a17b2fb4a89b467c2ca812f005a`; same `device` 16777232; `deviceInodeFsidStable` true on each sample; `sameDevice`/`sameFsid` true across the two FDs.
- The log itself records `qualifiedAdmission: false` and `restartTest: false`.

The SDK manpage lists `EINVAL` when volume attributes are requested and the path “does not reference the root of the volume.” This **one** macOS 26.6.2 arm64 APFS host still returned a UUID from a nested directory FD. That is ABI feasibility for a **direct-descriptor** volume-UUID option on this host/run. It does **not** establish portable support, and any future native implementation must treat unsupported/missing/invalid attributes as unavailable and require an explicit profile gate.

Discovery used `f_mntonname` only to open a comparison FD; that pathname is not custody or admission. The probe prints raw frames and is not a production decoder. Temporary fixture was process-owned and removed.

---

## Relation to 376 (scope unchanged)

This **informs** 376 requirement 2: a platform-qualified persistent volume identity **may** be readable from a retained nested directory descriptor via `fgetattrlist` `ATTR_VOL_UUID` on this APFS host, without treating `st_dev` as durable and without substituting `f_fsid`.

It does **not**:

- prove the UUID survives reboot/remount
- prove CF/`getattrlist` UUID equals `st_dev` (they are different fields; device 16777232 is the known APFS-shared `st_dev` class)
- prove unforgeable history, original repository continuity, or absence of a cloned volume
- qualify Linux (still needs its own native/FS design; no fallback invented)
- authorize silent repair, a new CLI, or a schema change
- close 376; the owner gap and six correction requirements stand

376-r2 model replay and GNU/CFURL primary sources are unaltered.
