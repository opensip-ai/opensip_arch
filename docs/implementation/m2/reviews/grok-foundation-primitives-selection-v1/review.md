# Independent Grok review: foundation-primitives-selection v1

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m2/foundation-primitives-selection-v1-subject.json`
**Manifest SHA-256:** `87ec90665949e7a9dfe604f1bb3148039c1113d9a61c07bf0500b70b57f3162b`
**Members:** 25
**Verdict:** **ACCEPT-DESIGN-UNIT**

M2 preparation of two bounded primitives in existing inventory-owned files. Not complete M1, not complete M2, not Linux qualification, not a repository sandbox, not release, not a fresh blind consumer. Genuine 8/8 live successors approve existing design/schema sources, not these seven new implementation bytes. Host-build-isolation-01 is prior-source evidence and was not re-run; it does not prove these bytes.

## Custody and joins

25/25 selection members match before and after. Frozen implementation subject `docs/implementation/m2/trials/foundation-primitives-01/subject.json` SHA `511eff69af377af48be171b0687823d21f97bbebfa9cb937e5fa13cf4bcba3d0` — **196/196** members match the tree at `/tmp/opensip-implementation/m2-foundation-primitives-subject-01`. Adjacent archive `subject.tar.gz` matches `archive-pin.json` (`fc8df13b…d1d4` / 1316856). Evidence `implementation-subject.json` is the same 196-file manifest. Execution used a private copy under `review/copy/frozen-subject`, not the frozen tmp tree and not live product.

Candidates are exactly the subject minus `successor.json` (24). `passageOverrides: []`. Parents pin-match architecture and live lock:

| Parent | SHA / bytes | Live |
| --- | --- | --- |
| contracts-dependency-selection-v1 successor | `c9a74172…3561` / 5972 | accepted contract successor |
| inventory v10 | `6608fabd…8bc9` / 121810 | accepted inventory |

All **7** materialization-map rows match frozen product bytes, candidate product bytes, and inventory v10 paths (`filesystem.rs` already planned). Live product does not yet contain these seven bytes (expected; not installed). `crates/identity/src/canonical.rs` and `crates/platform/build.rs` are byte-identical to live. Generated contract megabytes were not re-reviewed; no concrete concern required it.

## Identity: `parse_hash_preimage`

`unframe` (exported as `parse_hash_preimage`) takes a caller-selected `expected_domain` and a frame. It never infers the domain from the frame. Checks, in order: domain charset (existing encoder rule), exact `opensip.product.v1\0` prefix, exact expected-domain bytes plus NUL, big-endian u64 payload length equal to remaining bytes, existing bounded lossless JSON parse, then `encode(value) == payload`. New errors: `FramePrefix`, `FrameDomain`, `FrameLength`, `FrameNoncanonical`. Encoder `frame` / `identity` / `raw_sha256` behavior is unchanged except domain validation is shared. Success is not a registered descriptor, blob-digest check, schema admission, or Run.

Five new permanent groups in `canonical_tests.rs` cover external frame/hash vectors, domain/prefix mismatch, every truncation and declared-length mismatch, noncanonical-but-parseable JSON, and lexical refusals. Independent probes (mutant copy only) re-asserted wrong expected domain → `FrameDomain`, truncation/`u64::MAX` length → refuse, and admitted noncanonical JSON (` true`, `{"b":1,"a":0}`, `"\u0041"`) → `FrameNoncanonical`. **3/3 extra identity probes pass.**

## Platform: `RetainedDirectory`

Adapted from actual Claude-accepted report-assets02 `platform/src/lib.rs` SHA `54bb15d968c9034a52a7fb5ae552d168995b3e49ed58e712cc012c5927f5cadf` / 2952 (`ReleaseDirectory`). Production walk is the same: caller-supplied retained `File`; `fstat` directory check; per-segment `openat` with `O_RDONLY|O_CLOEXEC|O_NOFOLLOW|O_NONBLOCK` and intermediate `O_DIRECTORY`; leaf must be a regular file; no create. Renames, expanded trusted-root docs, and three in-module RAII tests (unique `0o700` temp trees, `Drop` cleanup). Flags are advisory (`F_GETFL`/`F_GETFD`). Tests qualify macOS here; Linux cfg is API presence, not Linux qualification.

**Localized unsafe:** crate `forbid(unsafe_code)` becomes `deny(unsafe_code)`. Only `filesystem.rs` is `#[allow(unsafe_code)]` and only under `cfg(any(macos, linux))`. That module `deny(unsafe_op_in_unsafe_fn)`. Production unsafe is two FFI sites (`openat`, `File::from_raw_fd`) with ownership comments; `File` closes the descriptor on every error path. Entropy `request_entropy` and `build.rs` backend guard are unchanged.

Documented limitations, independently accepted as stated scope: trusted installation root; device open can have effects before `fstat` rejects it; no mount/hardlink/immutable-tree/concurrent-mutation refusal; not a general repository sandbox; returned `File` is not a security capability.

Independent filesystem probes: returned flags (`O_RDONLY`, `FD_CLOEXEC`, `O_NONBLOCK`); symlink/FIFO/directory/traversal refusals; retained fd still reads `pinned` after root rename and leaf symlink replacement, while a new `open_regular` refuses. **3/3 extra filesystem probes pass.**

## Lock, DAG, inventory

`libc 0.2.189` checksum `3eaf3ede…12f2` was already in the live lock (getrandom). The only lock *edge* change is `opensip-platform` now lists `libc`. Internal package-edges vs inventory v10 `--lane host` pass and match the frozen fixture. Contracts dependency checker 11 deps / 8 local sources pass (`productQualification: false`). No new package, no inventory addition, no schema/generated output, no reporting→platform edge, no entropy-guard change.

Resolved **libc features** are not identical: live metadata has libc features `[]` (getrandom’s `default-features = false`); the candidate direct `libc = "=0.2.189"` unifies `default`+`std` onto libc for the workspace. Version/source/checksum unchanged. Disclosed as **S2**, not a primitive functional defect.

## Reproduction (private copy, Cargo/rustc 1.95 Homebrew)

PATH `/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin`; Node excluded; six compiler variables absent; Python `3.14.6 -I -B`.

| Check | Result |
| --- | --- |
| `cargo test --locked --offline --workspace --all-targets` with short `TMPDIR=/tmp/osip-m2g` | **30/30 pass** (6 CLI + 2 host + 15 identity + 3 filesystem + 4 reporting) |
| `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` | pass |
| `cargo fmt --all --check` | pass |
| selected contracts dependency check | pass, 11/8 |
| internal edges `--lane host` vs inventory v10 | pass |
| candidate `Cargo.lock` after commands | unchanged `c06da7ac…e17c` / 4262 |
| live `Cargo.lock` | unchanged |

First test run used a long isolated `TMPDIR` under the review directory; `UnixListener::bind("socket")` panicked `path must be shorter than SUN_LEN` before the socket-refusal assertion. That is test-path fragility (**S1**), not an adapter failure. Short temp dir: all three filesystem tests pass, matching the frozen log.

## Must-fix / should-fix

Must-fix: none. `requiredFindings` remain empty.

**S1 (should-fix):** Filesystem tests bind a Unix socket under `std::env::temp_dir()` with no `SUN_LEN` bound. A long `TMPDIR` panics the test harness before refusal is checked. Use a short private directory or treat bind failure as a skipped setup, not an adapter crash.

**S2 (should-fix):** Direct `libc = "=0.2.189"` enables default `std` and unifies libc resolved features from live `[]` to `["default","std"]`. If host-graph feature identity is required besides the declared edge, pin `default-features = false` (plus any needed features). Version/checksum were already selected.

## Limits (not fulfilled M1/M2 duties)

- M2 preparation only. Neither M1 nor M2 is complete.
- Not Linux runtime qualification, compiler authenticity, sandbox, release, or fresh blind consumer.
- `parse_hash_preimage` does not select a registered domain, verify a blob digest, admit descriptor schema, or replay.
- `RetainedDirectory` does not authenticate the root, refuse mounts/hardlinks/concurrent mutation, or provide immutable source custody.
- Inventory `filesystem.rs` description still mentions publication/durability; this unit implements retained-directory regular reads only.
- Host-build-isolation-01 (53 members, SHA `071cf047…99fd`) is over **prior** source bytes and does not prove these seven files.
- RF05 checked-in provider workspace/lock remains open; isolation02 was a probe, not that duty. HostAssetPin / `buildChannel` agreement remains open.
- Public/live installation waits for genuine successor/review/root assent and private activation. No fake approval.
