# M1 generator adapter review 03 (fresh, independent)

**Verdict: CHANGES-REQUIRED.** There is one required finding, RF1, a small confinement fix. Once RF1 is corrected and a real-sandbox regression test is added, the evidence supports **ACCEPT-UNIT** for the concrete adapter and the fixed macOS development host profile. That acceptance needs only a narrow delta review. This review does not find the unit hermetic, product-integrated, runtime-ready or release-qualified.

`subjectManifestSha256` is `ff8c39858d4ff2cc52449c897a99c7b58dd281415f2f17d14b0ca033eef1f4ef`. All 87 files match exactly, with none unlisted or linked. This held before probing, mid-review and after all probing.

## Prior findings

| ID | Disposition | Evidence |
|---|---|---|
| NR1 | **resolved** | The real `--write` refuses P5 (a HelloV3 subpath entrypoint), outputs unchanged. A nested `$ref` into `HelloV3/properties/protocolMajor`, injected into a selected native definition, is refused *inside the confined Python child*. The facade also refuses direct, nested and trailing-slash denied refs. |
| NR2 | **resolved** | Real `cargo metadata` refuses `reviewer-rc = ["serde/rc"]` and an empty local feature. The unmodified workspace passes with 11 dependencies. |
| A1 / A2 | addressed within the declared TCB | `nativeLibraries=[]`; the generator links only libSystem. The receipt join is observed-build, not reproducible: my clean vendor rebuild has hash `6b35cbaf…`, not `0a49cfc4…`, yet all 8 output bodies are **byte-identical**. |
| A7 / A8 / NA1 / NA5 | resolved | One JSON stdout line. Stub tests exist, and real steps were independently exercised. Nested `$id`/`$schema` are compared. Runtime transpilation goes to scratch. |
| NA2 | resolved (ADV1) | The frozen facade refuses all 9 probe refs and all 4 unselected definitions. |
| NA3 | partial (ADV2) | All 28 pins match the architecture checkout, but only its worktree bytes. |

## Required finding

**RF1 — the step-4 grant is derived from child-mutable state.**

- **Where:** `generate_contracts.py:72-81` and `:394-405`.
- **Cause:** the Node/Rust profile grants `(subpath output)`, which includes the root literal, and each later profile is rendered with `Path(output).resolve(strict=True)`.
- **What a child can do:** the generator child (step 3) can remove `work/output` and replace it with a symlink to any directory. The TypeScript child (step 4) is then granted read and write on that target.
- **Demonstrated:** with a symlinking generator stub and a probe TS child, the child read an outside canary, created a file and **overwrote the canary**. The same TS child under the real generator got EPERM on all three.
- **Parent behaviour:** it still refuses publication (O_NOFOLLOW), but after the outside effect has happened.
- **Limits of the attack:** an honest `generate-ts.cjs` got EPERM when writing through the symlink path, so exploitation needs a hostile step-4 child. The Python profile already excludes its root literal.
- **Related:** the step-2 child can likewise replace `runtime-scratch`. That is currently harmless because scratch is only used as the working directory.

*Correction:*
1. Exclude the root literal from Node/Rust write grants.
2. lstat-verify the parent-created dev/ino of each root before rendering the next profile.
3. Preferably give each step its own fresh output root, with all grants resolved before any child runs.
4. Add a real `sandbox-exec` regression test.

*Fix check:* I applied `(require-all (subpath p) (require-not (literal p)))` in a rebound copy. It blocks the escape, and real generation still produces the frozen bodies (`probe-G`).

## Independent evidence (real code, real binaries)

- **Tests:** 75 OK on a byte-identical copy. This is the claimed 22+9+4+11 = 46, plus 29 design-binding tests.
- **Drift check:** a fresh 8-output drift check with the pinned generator, node and Python is clean.
- **Pins:** the TS tree (140 files), generator, node and python match the closure. build-04 `receipt.json` equals the frozen receipt.
- **Direct Node/Rust profile (native probe, unconfined control vs confined):**
  - Denied: outside read/create/write, input writes, `$HOME` and `/etc/passwd` reads, `/dev/tty`, hardlinks, reads through symlinks, TCP loopback (listener saw 0 connections), UDP, DNS, `mDNSResponder` and the syslog datagram socket, fork and exec.
  - Allowed but refused afterwards: symlinks and fifos in the output root, which the collector then refused.
- **Python child (real parent):**
  - Denied: rmdir/chmod of its root, outside reads/writes, code and input writes, hardlinks, fork and exec.
  - Strict imports: an unpinned `csv.py` is unreadable, and `import csv` / `import socket` fail.
  - A variant that leaves a symlink and a fifo and exits 0 is refused by the collector, with the canary intact.
- **Node step 2 (real parent):** outside access, writes to inputs/code, reading the parent profile, `spawnSync` (sh and self), hardlinks, TCP and DNS are all denied.
- **Guards:** 16 Python-profile mutations and 7 confinement mutations are refused, as are `hostProfile`, `nativeLibraries` and a rebound extra directory grant. All are controlled `GenerationError`s before any child runs.
- **Publishing:**
  - A hard-linked destination is replaced, leaving the outside bytes intact and the destination with nlink 1; the following drift check is clean.
  - A symlinked generated directory refuses before any write.
- **Build:**
  - An ancestor `.cargo/config.toml` is refused.
  - The clean vendor build succeeds with network denied. Receipt fields equal the frozen receipt except temp paths, logs and the executable.
  - All 25 archives match the receipt and lock.
  - The prettyplease 0.2.37 `build.rs` and source are benign: no fs, process, net or env use at runtime.
- **Witnesses:** strict `tsc` passes. Frozen outputs match 1338/1338 witnesses in the TS original-schema check, with 12 denied-ref probes refused. The Rust roundtrip over 1338 rows has 0 failures. The corpus is the declared source minus the 5 superseded rows.

## Selected-input generation obligations

These are **met within the explicit TCB**, except RF1. The TCB is the parent/admission Python, macOS kernel, sandbox-exec/system.sb, dyld/system frameworks, and the Homebrew Python and nvm Node binaries, integrity-checked before and after use.

## Remaining bootstrap check before integration

An external reviewed anchor must select the following. These are the inventory/design-lock successor rows, not self hashes.

- Registry `4cf6dbd5…` with recipe `contracts-v1`.
- That recipe's closure `3473abef…`, which covers:
  - options `1719ef18…`
  - source-map `561cf9ef…`
  - the build receipt and executable `0a49cfc4…`
  - node `1ee75375…`
  - python `b502cb4c…`
- The 28 architecture sources, pinned at a **committed** architecture revision. Today 22 are untracked and 3 are modified at HEAD `c3856824…`.

`verify_design` still selects the predecessor lock. After that come the complete protocol/report source-closure owners and other platform/release qualification.

## Advisories

- **ADV1:** `report.ts` still exports the generic `SchemaRegistry`, `parseExact` and `canonical`.
- **ADV2:** architecture pins are bound to worktree bytes, not a commit.
- **ADV3:** the parent should compare the child's `owners.json` with its own options.
- **ADV4:** the receipt join is narrow. Its tools/versions fields are not checked, and nine build scripts and three proc-macros run unconfined at build time.
- **ADV5:** there are no CPU, memory or disk limits before the 128 MiB collection check. The timeout was reviewed, not triggered.
- **ADV6:** the witness provenance record should name the derived corpus digest.

## Limits

- Only the macOS 26.6.2 aarch64 development host was examined; Seatbelt semantics were observed empirically.
- No hermetic, reproducible or release claim is made. Host-user races on native files are out of scope.
- Clippy/fmt were not re-run.
- NA4 was not re-assessed.

Evidence is in `logs/`, scripts and copies are in `work/`. All mutations were confined to this directory. Nothing was committed or pushed.
