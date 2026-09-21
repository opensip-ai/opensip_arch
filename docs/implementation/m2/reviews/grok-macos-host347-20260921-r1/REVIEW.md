# Independent review — native macOS boot/kernel observations 347

**Standing:** bounded native-**platform** review of frozen `macos-host-checkpoint-347`. `MacosBootObservation` is an unprivileged libSystem sample of `kern.uuid`, `kern.osversion`, and two CSR relaxation flags (`ALLOW_UNRESTRICTED_FS` / `ALLOW_UNAUTHENTICATED_ROOT`). It implements the **read-only observation interface** required by incorporated security-v8 §8.3. It does **not** admit a signed profile, measure loader CodeDirectory, classify all SIP / Full vs Reduced Security, or grant current/writer authority. Product remains `fa72e50`; M2–M6 open. 346 REVIEW `6b3e9351…b9bc` and 345 REVIEW `4e3718f5…7157` were read and are **unchanged**. The 346 missing BSD `MNT_RDONLY` source pin is subsequent 346 evidence and is **not** part of this freeze.

Python 3.12.13 `-I -B` for pin/extract. Rust 1.95.0 `--offline --locked`. Frozen mutant dirs not overwritten. **One** stable `CARGO_TARGET_DIR` for platform/Clippy/fmt; mutants used a **separate** live dir after that finished. **This review reproduced:** platform **84**, Clippy `-D warnings`, rustfmt of **27** security includes plus `macos_boot.rs`. Independent C probe agrees with integrated Rust. **No 347 whole-workspace rerun**; parent 346 workspace-r2 **658 / 0 / 2** is historical. Parent 346 workspace-r1 concurrent-rebuild rustdoc `E0463` remains a recorded non-pass.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Independent rehash of live tar, all 574 tar members, and the extract: 0 mismatches.

Frozen archive: **6840540 B, 574 members, SHA256 `9b8023933ace4ca20f71b1047685319d954d2ddeda3e56bc9b0de84873fe12ff`**. Extract 574/574. Parent 346 live tar SHA `483a9b19…b70e` (6884940 / 568 / 493).

Product vs 346: **492** unchanged, **1** changed (`lib.rs` `cf0c2daa…ceb6` / 3197), **1** added (`macos_boot.rs` `64326566…9c72` / 14066). No security/fixture/dependency deltas. FFI is confined to this adapter (`#[allow(unsafe_code)]` on `macos_boot` under crate `#![deny(unsafe_code)]`).

---

## ABI (source, not installed TCB)

Pinned XNU `f6217f891ac0bb64f3d375211650a4c1ff8ca1ea` files were rehashed from the **immutable URLs** and match `api-source-pins.json` and the local copies:

| File | SHA256 prefix | Role |
|---|---|---|
| `bsd/sys/csr.h` | `1787401f…d5a3` | `CSR_ALLOW_UNRESTRICTED_FS (1<<1)=2`, `CSR_ALLOW_UNAUTHENTICATED_ROOT (1<<11)=2048`; `int csr_check(...)` |
| `libsyscall/wrappers/csr.c` | `45562f7c…12cf` | userspace `csr_check` **returns `__csrctl(CSR_SYSCALL_CHECK, &mask, sizeof)`** — not the kernel function |
| `bsd/kern/kern_csr.c` | `1ca6675b…0a99` | kernel `csr_check` returns **`0` or `EPERM` (positive)** |

SDK 27.0 `libSystem.tbd` / `libsystem_kernel.tbd` hashes match live files; `_csr_check` is exported. Public `sys/csr.h` is **absent**. Upstream is **not** asserted byte-identical to the installed kernel/libSystem.

**Userspace contract independently observed on this host** (compiled frozen `probe.c`, no policy change):

```
csr mask=2 return=-1 errno=1
csr mask=2048 return=-1 errno=1
sysctl kern.uuid return=0 errno=0 length=37 value=8D3E13A0-01FC-381D-9DA3-7F0AF537CB32
sysctl kern.osversion return=0 errno=0 length=6 value=25G83
```

That matches frozen `native.stdout`, `integrated-native-agreement.json`, and live Rust `MACOS_BOOT347 kernel=8D3E13A0-01FC-381D-9DA3-7F0AF537CB32 build=25G83 unrestricted=false unauthenticated=false`. Agreement is **not** release qualification.

Product `csr_with`: clear errno; `(0, _)` → allowed (stale errno ignored); `(-1, EPERM)` → denied; `(EPERM, _)` and other pairs → unavailable. Private `observe_with` / `csr_with` **cannot** replace `observe_macos_boot()` → `native::observe()` (always `sysctlbyname` / `csr_check`). Non-macOS returns `Unsupported`. No Linux run.

Sysctl: fixed 37/10-byte stack buffers, `newp=NULL`/`newlen=0`, length 2..=cap, terminal NUL, no interior NUL, then uppercase UUID / 4..=9 build grammar **before** owning strings. Unknown sysctl and 2-byte `kern.osversion` return `Native` (`ENOMEM` for the short buffer). Failure at any of the four steps returns no object.

---

## Failure history

No 347 production or test failure while implementing. Standalone-r1 five tests, then r2 six (added real unknown-sysctl + short-buffer `ENOMEM`; before-image `before-native-sysctl-error-test347.rs` retained). Integrated platform-r1 **84**. Parent 346 workspace-r1 overlapping-target rustdoc `E0463` is **not** suppressed. This review did not mix rebuilds in one target.

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| Independent C probe | `-1/1` both masks; UUID 37; build `25G83` |
| `cargo test -p opensip-platform` | **84 passed / 0 failed / 0 ignored**; 0.33s; all 6 `macos_boot_*` ok |
| Native println vs C | exact kernel/build; both relaxations false |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **27** includes + `macos_boot.rs` | exit 0 |
| Full workspace | **not rerun** |

---

## Mutants

Eleven compiled controls + six-test `macos_boot_` baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`81f1c56cdd4aa051730fc436ebf2815feba691c2bbdf591e258e0b593c1b3276`**, **byte-identical** to frozen r1. All **12** compiled. Baseline source pin matches product `macos_boot.rs` `64326566…9c72`.

Actual first failures (live stdout):

| Control | First failure |
|---|---|
| `wrong-kernel-identity-source` (`kern.bootsessionuuid`) | fixture `response` panics unexpected query |
| `wrong-build-source` (`kern.osrelease`) | actual native `MalformedResponse("kern.osversion")`; fixture panic |
| `wrong-filesystem-relaxation-mask` (`0`) | fixture `panic!("wrong mask")` |
| `wrong-root-relaxation-mask` (`1<<1`) | calls `[2, 2]` vs `[2, 2048]` |
| `accept-kernel-positive-eperm` | `(EPERM, 0)` no longer `is_err()` |
| `skip-csr-errno-clear` | stale `EPERM`: `errno` 1 vs 0 before success-0 |
| `invert-csr-denial` | `-1/EPERM` treated as allowed |
| `accept-unterminated-sysctl` | unterminated build `25G83x` accepted into later steps |
| `skip-kernel-uuid-shape` | lowercase UUID reaches CSR (`badUUID reachedcsr`) |
| `skip-os-build-shape` | `25g83` reaches CSR |
| `ignore-sysctl-error` | unknown `opensip.nonexistent.readonly347` not `Native` |
| baseline | 6 `macos_boot_` tests |

---

## Findings

347 is a **sequential native sample**, not an atomic boot snapshot and not “all SIP enabled.” Two booleans are individual relaxation-allowed flags from userspace `csr_check`, which is a thin `__csrctl` wrapper. Kernel `csr_check` returning positive `EPERM` is **refused** as a userspace denial — independently required by `kern_csr.c` vs `csr.c` vs this host’s `-1/1` probe.

**Reproduction of the ABI split:** treating `(EPERM, 0)` as denied makes the userspace matrix test fail. Skipping errno clear makes success-0 with leftover `EPERM` fail the `errno()==0` assertion. Inverting `-1/EPERM` reports allowed when the C probe on this host is denied.

**Reproduction of query identity:** `kern.osrelease` fails actual `observe()` on this host (`MalformedResponse`). Mask `0` / `1<<1` for root break the pinned `2`/`2048` call order.

**Not defects vs stated standing:** matching `25G83` / kernel UUID on this development host is not TCB or profile qualification. `from_utf8` after ASCII grammars is belt-and-suspenders. Linux observer is `Unsupported`.

**Actionable defects in this freeze:** none that make `csr_with` / `sysctl` / `observe_macos_boot` self-contradictory with those bounds on the reproduced 84 tests, C probe, and eleven compiled controls.

**Must not be counted closed:** loader CodeDirectory; signed-profile join; native FS/current authority; original T/action; writers; selected I/S; Linux; M2–M6.

---

## Remaining (do not count closed)

Loader CodeDirectory acquisition/hash and composing actual native boot **and** filesystem observations with admitted signed-profile evidence. All original core/authority/history/T/action and native writer/census admission obligations remain separate.

---

## Verdicts

- [x] **347 as frozen private macOS boot observations:** archive verified; 346/345 preserved; userspace `csr_check` ABI (`0` / `-1+EPERM`) vs kernel positive `EPERM` independently sourced and probed; fixed 37/10-byte sysctl; live platform 84; Clippy/fmt27; C/Rust agreement; 11 compiled controls + 6-test baseline frozen-r1-equal; no 347 production fail; 346 r1 rustdoc mixup not counted as a pass.
- [ ] **Not** selected-I, profile/loader/SIP-complete/current authority, writers, or product installation.
