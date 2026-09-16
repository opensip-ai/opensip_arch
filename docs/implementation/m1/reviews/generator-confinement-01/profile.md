# M1 generator child confinement trial 01 (macOS)

Standing: this is a bounded author/probe trial on a development-trusted host
(TCB-SCOPE-01). It is not approval, not hermetic generation, not product
integration, and not a portable release qualification. It trusts the host
kernel, dyld/libSystem, Apple's `system.sb`, and `/usr/bin/sandbox-exec`.
Generator inputs (the Node scripts, TypeScript package, prepared data and
generator binaries) are treated as untrusted.

Host: macOS 26.6.2 (25G83), arm64. Node v24.16.0 official binary, pinned
`1ee75375…`. Generator: the format-trial prettyplease binary. It links only
libSystem and needs no rustfmt or LLVM.

## 1. Why earlier deny-read profiles aborted Node

This was **resolved** and the cause was reproduced, see `logs/hypothesis/result.txt`.
Every aborting diagnosis profile denied `file-read-data` on the literal `/`.
dyld's libignition opens `/` as its `openat(2)` root. Apple's
`/System/Library/Sandbox/Profiles/dyld-support.sb` says so and allows
`file-read* (literal "/")`.

- Denying it kills even `/usr/bin/true` (exit 134).
- Adding `(require-not (literal "/"))` fixes both.
- `diagnosis-03/root.sb` passed only because `subpath "/"` includes `/`.

This was a dyld bootstrap requirement, not a Node problem.

Two further facts were established under `(deny default)` + `(import "system.sb")`:

- **Ancestor metadata.** Node's CJS loader runs `realpathSync(main)`, which
  `lstat`s every ancestor (`EPERM, lstat '/private'`). The fix is
  `file-read-metadata` on `path-ancestors` of each granted root. That covers
  the ancestor directories only, not their siblings.
- **Stdio.** Node aborted at `InitializeOncePerProcess` whenever its stdio was
  a regular file under `/private/tmp` (`logs/hypothesis/mx.err`). With pipes
  plus `stdin=/dev/null`, as `subprocess.run(capture_output=True)` sets up, it
  starts cleanly. The runner therefore always uses pipes. I did not isolate
  which exact startup operation needs the file path.

Profile paths must be canonical. A `/tmp/...` profile path fails to match
`/private/tmp/...` and even the exec is refused (`runs/symlink-exfil` first attempt).

## 2. Profile (rendered per child step by `scripts/run_confined.py`)

```scheme
(version 1)
(deny default)
(import "system.sb")                         ; trusted dyld/libSystem runtime rules
(deny file-read* (literal "/private/etc/passwd") (literal "/private/etc/master.passwd"))
(deny file-write* (subpath "/cores"))
(allow process-exec (literal EXE))           ; only the step's snapshotted executable
(allow file-read* (literal EXE) (subpath READ...) (subpath WRITE...))
(allow file-read-metadata (path-ancestors EXE) (path-ancestors READ...) (path-ancestors WRITE...))
(allow file-write* (subpath WRITE...))
```

No `network*`, no `process-fork`, and no other exec are granted. Rendered
profiles are in `runs/<step>/profile.sb`. Each step also gets an explicit
`cwd` set to scratch, `env={PATH=/usr/bin:/bin, HOME=scratch/home, LANG=C, LC_ALL=C, TZ=UTC}`,
`stdin=/dev/null` and piped stdout/stderr.

| Step | EXE | READ | WRITE |
|---|---|---|---|
| 1 validate-schemas | `work/bin/node` | `work/snapshot/tools/contracts` | `scratch` (runs on a scratch copy of `options.json`/`raw-schemas.json`, which fixes NA5) |
| 2 Rust generator (in-process prettyplease) | `work/bin/format-generator` | `work/inputs` | `output` |
| 3 generate-ts | `work/bin/node` | `work/snapshot/tools/contracts`, `work/inputs` | `output` |

`work/` is built by `scripts/prepare_snapshot.py`, which reuses candidate-03's
`registry()` read-only. The snapshot has 171 files; hashes are in
`logs/snapshot-manifest.json`. **Caveat:** root was editing candidate-03
during the trial. Six closure file pins were stale and `rustfmt.toml` was
missing, so the snapshot is candidate-03's working tree at that moment, not a
pin-verified closure. The Node pin was verified. The candidate-02 generator
(`ec6bb9d8…`) was copied but not used; the format-trial binary was used instead.

## 3. Results (runs 03 and 04, `logs/results-run-0{3,4}.json`)

**Positive:** all three confined steps exit 0.

- validate: 586 original entry points checked.
- rust: six Rust files.
- ts: 45 provider and 586 report exports, 0 number and 0 any types.

The 8 outputs are byte-identical to the same steps run unconfined, identical
across both runs, and the snapshot tree is unchanged.

**Negative:** these were run inside the step-3 profile shape by
`scripts/probe.cjs`, which stands in for untrusted generator code. Every row
was re-run unconfined with the same probe as a control, and all rows were
ALLOWED there. That shows each denial is real.

| Attempt | Confined result |
|---|---|
| Read outside canary / candidate-03 source / unselected snapshot file / node install sibling | EPERM ×4 |
| `stat` outside canary / node sibling | EPERM ×2 |
| `readdir` trial dir / `work/` / `/private/tmp` | EPERM |
| Write trial root, `/private/tmp`, `/private/var/tmp`, `work/inputs`, `work/snapshot` | EPERM ×5; nothing created (checked by parent) |
| Hard link to outside canary into scratch | EPERM (lstat check: no same-inode entry) |
| Symlink to outside canary: create / read through | **create ALLOWED** / read EPERM |
| `/etc/passwd` read (granted by system.sb, overridden) | EPERM |
| Loopback TCP connect / UDP send / listen | EPERM ×3; parent listeners saw nothing |
| `spawnSync('/bin/sh')` / `execFileSync(node)` | EPERM / EPERM (no `process-fork`) |
| Rust generator given outside input root / outside output root | exit 101 PermissionDenied / exit 101, nothing created |
| `sandbox-exec` of undeclared `/bin/sh` | exit 71, `execvp() … Operation not permitted` |

## 4. Precise remaining effect surface (what confined code can still do)

- **Trusted system reads from `system.sb`.** These cover `/System`,
  `/usr/lib`, `/usr/share`, `/Library/Apple`, `/private/var/db/timezone`, the
  eligibility plist, `/dev/{random,urandom,null,zero}`, `/dev/fd`, `/dev/dtracehelper`
  and `/`. Code can read OS files and learn the exact OS build. None of these
  are project sources.
- **Metadata.** `lstat` works on ancestor directories of granted roots, which
  reveals their existence, mode and mtime. It does not work on siblings.
- **System services.** `system.sb` allows `mach-lookup` to logd, opendirectoryd,
  cfprefsd, trustd and others, plus `sysctl-read`. Observed allowed results:
  hostname, username (`os.userInfo`) and CPU count. That is host identity
  disclosure only, since there is no network or outside write to exfiltrate it.
  Stdout/stderr pipes to the parent are the only outbound channel.
- **Environment.** Keys are the five given plus `__CF_USER_TEXT_ENCODING`,
  which CoreFoundation injects.
- **Descriptors.** Only 0–2 are inherited from the parent (pipes and
  `/dev/null`); Node opens 3–12 itself. The parent must keep
  `close_fds=True`, which is the Python default.
- **Symlinks.** Code can create them inside WRITE roots. The sandbox then
  blocks the child from reading through them, but the **unconfined parent does
  not.** This is demonstrated in `runs/symlink-exfil/`: a confined child wrote
  `generated/mod.rs -> canary`. candidate-03's collector
  (`generate_contracts.py:255`, `p.is_file()`/`read_bytes()`) then returned
  `b'outside secret\n'` as generated output.
- **Resources.** CPU, memory, disk use within WRITE roots, and wall time are
  not bounded by the profile. The runner uses a timeout; there are no rlimits.
- **Durability of the mechanism.** `sandbox-exec(1)` is marked DEPRECATED, and
  `system.sb`/`dyld-support.sb` are "Apple System Private Interface … subject
  to change". The profile is valid for the recorded host build and must be
  re-probed after OS updates. It is a host-profile control, not a portable one.

## 5. Proposal for generator03 (root task; not applied here)

1. **Required, parent-side.** Before reading output, walk it with `lstat` and
   refuse any symlink, hard-linked (`st_nlink != 1`) or non-regular entry.
   Then read with `O_NOFOLLOW`. The sandbox cannot close this; section 4 shows the exfiltration.
2. Run each child as `sandbox-exec -f <rendered profile>` using the grants
   table above. Render from `realpath`s of a fresh snapshot, scratch and
   output. Use pipes, `stdin=DEVNULL`, a timeout and minimal env.
   Fail closed if `sandbox-exec` or `system.sb` is absent.
3. Use the in-process prettyplease generator. That drops `rustfmt` and the
   four Homebrew `nativeLibraries` from the closure. The generator and Node
   then depend only on the trusted macOS runtime.
4. Keep NA5: validation writes only to scratch, and inputs are read-only to every step.
5. Optionally, before generation, run a self-test child with the probe's
   outside-read and loopback checks. That turns "profile applied" into an
   observed fact per host.
6. **Python (separate, untested).** `adapter.py` and `prepare.py` are pinned
   generator inputs but still execute *in* the unconfined parent. Proposal:
   the parent keeps only hash verification, snapshotting and lstat-safe
   collection, and runs prepare as a confined `python3 -I -S` child with the
   same profile shape. That child would get READ on the snapshot, the source
   copies and the Python prefix, and WRITE on `inputs/`. It needs its own
   probe trial because the Homebrew framework Python prefix grants are unknown.
   The external bootstrap/design verifier anchor stays with root.

## Reproduce

```sh
cd /private/tmp/opensip-implementation/m1-generator-confinement-trial-01
python3 -I scripts/prepare_snapshot.py   # builds work/ (records stale pins)
python3 -I scripts/run_confined.py       # writes runs/, logs/results.json
```
