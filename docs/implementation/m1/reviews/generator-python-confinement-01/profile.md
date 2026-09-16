# M1 Python preparation child confinement trial 01 (macOS)

**Standing.** This is a bounded author/probe trial on a development-trusted host.

- **Not claimed:** approval, hermetic preparation, product integration, or a
  proof of the interpreter's complete native closure.
- **What it establishes:** a real `-I -B -S` Python child can run the stable
  `source/prepare.py` under the same deny-default + `system.sb` host profile
  shape as `m1-generator-confinement-trial-01`, with exact, pinned interpreter
  grants.
- **Trusted:**
  - the host kernel, dyld/libSystem/CoreFoundation, Apple's `system.sb`, and
    `/usr/bin/sandbox-exec`;
  - an explicit trusted host interpreter profile, described below.
- **Untrusted:** `prepare.py`, `runtime/`, and every child output.
- **Root still owns:** external bootstrap anchoring, pin verification of the
  code/inputs, merged-input construction, and output collection.

Host: macOS 26.6.2 (25G83), arm64. Everything was built from `source/`; candidate-03 was only read (its
`collect_outputs`, sha256 `79db5021…`, executed from recorded bytes).

## 1. Interpreter selection and why

| Candidate | Finding | Used |
|---|---|---|
| `/usr/bin/python3` | xcrun shim that re-execs CLT Python 3.9.6, which would need a second exec grant plus xcode-select state | no |
| Homebrew `…/3.14/bin/python3.14` | a launcher stub. It `posix_spawn`s `Resources/Python.app/Contents/MacOS/Python`; confined, that fails with `process-exec*` denied (`logs/discovery/smoke.sb`, `runs/negative-launcher-stub`: exit 71 when exec'd directly). | no |
| Homebrew `…/3.14/Resources/Python.app/Contents/MacOS/Python` | the real interpreter, 3.14.6 (clang 21). It links only the `Python` framework dylib, CoreFoundation and libSystem. | **yes** |

Pins (verified by `scripts/confine.py` before every profile render):

- executable `/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python`
  `0c9a985712bb1235d8fe474a6a99810dc118bcae0dfb429a237aac0c907fa3af` (ad-hoc signed)
- framework dylib `…/Versions/3.14/Python` `696ffa2cf9562522c387f7c2b3a990ef67e574df2d921822fe310ea35587cce0`.
  It links `/System/Library/Frameworks/CoreFoundation.framework` and `/usr/lib/libSystem.B.dylib`.
- The 25 stdlib sources and 3 extension modules below are listed with sha256
  in `logs/python-grants.json` and `logs/summary.md`.

All paths are canonical Cellar paths. `/opt/homebrew` is a real directory, not a symlink.

## 2. Exact grants (rendered per run, e.g. `runs/confined-1/profile.sb`)

```scheme
(version 1)
(deny default)
(import "system.sb")
(deny file-read* (literal "/private/etc/passwd") (literal "/private/etc/master.passwd"))
(deny file-write* (subpath "/cores"))
(allow process-exec (literal PY_APP))
(allow file-read* (literal PY_APP) (literal FRAMEWORK_DYLIB)
       (literal STDLIB_FILE)...        ; 25 .py + 3 .so, exact
       (literal STDLIB_DIR)...)        ; 7 directories: listing only (path finder)
(allow file-map-executable (literal FRAMEWORK_DYLIB) (literal SO)...)   ; see §4: not enforced here
(allow file-read* (literal ENTRY) (literal RAW_SCHEMAS) (literal OPTIONS)
       (literal CODE/prepare.py) (literal CODE/runtime/schema.ts))
(allow file-read* (subpath OUTPUT))
(allow file-write* (require-all (subpath OUTPUT) (require-not (literal OUTPUT))))
(allow file-read-metadata (literal STDLIB/os.py))                        ; getpath prefix landmark
(allow file-read-metadata (path-ancestors EACH_GRANTED_PATH))
```

No `network*`, `process-fork` or other exec is granted.

The run shape is:
`sandbox-exec -f profile.sb PY_APP -I -B -S ENTRY RAW_SCHEMAS OPTIONS CODE OUTPUT`,
with `env={}`, `stdin=/dev/null`, piped stdout/stderr, and a timeout. `cwd` is an
ungranted empty directory, so `getcwd` is denied; nothing needs it.

**Derivation of the grant list** (`scripts/pin_python.py`):
1. It ran the real entry confined under a discovery profile (whole
   `lib/python3.14` readable) with `-X importtime`.
2. It resolved each of the 57 imported names with the same interpreter via `find_spec`.
3. Every located module has to be under the Cellar stdlib, not `site-packages`
   and not a symlink, or the script fails.

Result:
- **Stdlib sources:** `collections/__init__`, `contextlib`, `copyreg`,
  `encodings/{__init__,aliases,utf_8}`, `enum`, `fnmatch`, `functools`, `glob`,
  `json/{__init__,decoder,encoder,scanner}`, `keyword`, `operator`,
  `pathlib/{__init__,_os}`, `re/{__init__,_casefix,_compiler,_constants,_parser}`,
  `reprlib`, `types`.
- **Extensions:** `_json`, `fcntl`, `grp`. Each links only `/usr/lib/libSystem.B.dylib`.
- **Built-in or frozen:** 27 modules, including `os`, `stat`, `io`, `codecs` and
  `posixpath`. They are compiled into the pinned dylib.
- **Not found:** `nt`, `_winapi` (optional imports that are absent on macOS).

What each grant requirement was established by:
- **Exec target:** Python.app must be exec'd directly; the launcher stub needs a second exec.
- **Ancestor metadata:** metadata on the executable's ancestors is required.
  Without it, `realpath: …/bin/: Operation not permitted` and the interpreter exits 1.
- **Directory listings:** literal stdlib directory reads are required, because
  the path finder lists each directory on `sys.path` and each package directory.
- **`os.py` landmark:** without its stat grant, every run printed
  `Could not find platform independent libraries <prefix>` and fell back to the
  compiled prefix. With it, stderr is empty.
- **Runtime vocabulary:** only `runtime/schema.ts` is read. Without that grant,
  preparation fails with EPERM on `schema.ts` (`runs/negative-without-runtime-grant`).
  Reading `runtime/patterns.ts` is denied.

## 3. Entry: `prepare-inputs.py` (author candidate, copied into `work/entry/`)

Hashes as of the final run:
- `prepare-inputs.py`: sha256 `609a40666336dd413fc09a659b5fd6619ff5eff08e7ee13ab463b3e1375ccca2`
- `logs/python-grants.json`: `fede8c5fbe473c362af817bba65244f8d95b63b80e8674557721e1583fc2e32f`
- Stable source pins: `scripts/build_work.py` `PINS`
  (e.g. `prepare.py` `84b465b3…`, `options.json` `1719ef18…`, `runtime/schema.ts` `1e4c2720…`)

- **Flags.** It refuses unless `isolated`, `ignore_environment`, `no_user_site`,
  `no_site`, `dont_write_bytecode` and `safe_path` are all set, optimize is off,
  `site` is not yet imported, and there is no `site-packages` entry on `sys.path`.
  The `-B`, `-S` and `-I` ablations each exit 1 with that message.
- **Inputs.** It reads `RAW_SCHEMAS` and `OPTIONS` with `O_NOFOLLOW`, as regular
  files up to 64 MiB. Decoding matches candidate-03: duplicate keys and
  non-integer numbers are refused.
- **Documents.** `RAW_SCHEMAS` must be a nonempty array of strings. Each string
  decodes to an object with the 2020-12 dialect and a unique nonempty `$id`, and
  that `$id` becomes its key in `documents`.
- **Loading `prepare.py`.** It is executed with `compile`/`exec` from its exact
  bytes into a fresh module whose `__file__` is set. That involves no import
  machinery and no bytecode cache. It then calls
  `prepare.prepare(documents, options, Sink())`.
- **Output names, verified.** `prepare.prepare` writes four names: `rust-projection.json`, `ts-projection.json`,
  `owners.json`, `targets.json`. Consumers read only `owners.json` + `rust-projection.json`
  (`tools/contracts/src/main.rs`, format-trial `src/main.rs`) and `ts-projection.json`
  (`generate-ts.cjs`). `raw-schemas.json` and `provenance.json` are parent-supplied. Nothing
  reads `targets.json`.
- **Sink.** The Sink accepts exactly those four `write_text` calls as ASCII text.
  It requires the set to be complete, drops `targets.json`, and creates the
  three consumed files. The output root must be empty and is opened
  `O_DIRECTORY|O_NOFOLLOW`; files are created `O_CREAT|O_EXCL|O_NOFOLLOW`
  relative to it. The Sink is **not a security boundary**, since untrusted
  `prepare.py` can write the output root directly. The parent collector is the
  boundary.
- **Script mode is required.** Python 3.14 `-c` imports `linecache`, which is
  not granted, so the parent must run the script, never `-c`.

## 4. Results (`logs/results.json`, rendered to `logs/summary.md`)

### Positive

- **Exit codes:** `confined-1`, `confined-2` and the unconfined control
  `unconfined-entry` all exit 0 with empty stderr.
- **Collection:** candidate-03 `collect_outputs(output, {3 names})` succeeded
  for all three runs.
- **Byte parity:** these results are identical to each other, to a direct
  in-process `prepare.prepare` reference (a test oracle only, which also wrote
  `targets.json`), and to trial-01's candidate-03 prepared inputs:

  | file | sha256 |
  |---|---|
  | `owners.json` | `079d02da7aff1ae70fcfab9a30f2e6e5c08967cb359068a21c867dc6a2db4567` |
  | `rust-projection.json` | `0923c4c4d8797586631f78b700cf2b3f7f092f14fff7e374dbd36bd3aeb15f92` |
  | `ts-projection.json` | `2fec47ad98e20ad7788e4724cc755c142c9d8406ccb6f6c30148e7fb01a6b05a` |

- **Unchanged:** the `work/` tree and all grant pins, before and after.
- **Merge demo:** `runs/merged-inputs/` is the collected bytes plus the
  parent's own `options.json`/`raw-schemas.json`. The child never touches those.

### Negative

The probe is `scripts/probe_prepare.py`, loaded by the real entry as
`prepare.py` under the same profile shape. Every row was re-run unconfined with
the same probe (write targets redirected to copies under the control's run
directory), and every kernel-level row was ALLOWED there, so each denial is
real. The exception is the four create targets outside the trial
(`/private/tmp`, `/private/var/tmp`, the stdlib directory and stdlib
`__pycache__`): they were attempted only confined, and the parent verified
afterwards that they do not exist.

| Attempt | Confined |
|---|---|
| Read canary / `source/` copy / candidate-03 file / unselected `runtime/patterns.ts` / unimported `subprocess.py` / stdlib `__pycache__` `.pyc` / Homebrew `site-packages/pip` / framework `include/Python.h` / `Python.app` `Info.plist` / `/etc/passwd` | EPERM ×10 |
| `stat` canary / framework sibling | EPERM ×2 |
| List trial dir / `work/` / `/private/tmp` / output parent | EPERM ×4 (granted stdlib dir lists: ALLOWED) |
| Open-for-write `options.json` / `raw-schemas.json` / `prepare.py` / entry | EPERM ×4 |
| Create in trial root / `inputs/` / `code/` / output parent / `/private/tmp` / `/private/var/tmp` / stdlib dir / stdlib `__pycache__` | EPERM ×8; parent confirmed none exist |
| `rmdir` / `chmod` of the output root itself | EPERM ×2 (`require-not literal`) |
| Hard link canary into output | EPERM |
| Symlink canary as `output/owners.json`: create / read through | **create ALLOWED** / read EPERM |
| Undeclared `output/targets.json` | ALLOWED; the parent collector then **refused** (`undeclared, linked or nonregular generated output`) |
| `os.fork` / `posix_spawn /bin/sh` / `posix_spawn self` | EPERM ×3 |
| `os.system('exit 0')` | returns 32512 (no shell ran); control returns 0 |
| `execv /bin/sh` | EPERM |
| `execv` **self** (exact interpreter) | **ALLOWED**; the replacement entry ran and got EPERM on the canary, so it is still confined |
| Import `subprocess` / `socket` / `_socket` / `_ctypes` / `ssl` | ModuleNotFoundError: the files are not granted |
| Loopback TCP connect / UDP send / TCP listen (profile widened by exactly `_socket.so`) | EPERM ×3; parent listeners saw nothing (control: both received) |
| AF_UNIX connect `/private/var/run/syslog` (same widened profile) | **ALLOWED**, via `system.sb`'s `network-outbound` rule |
| `sandbox-exec` of undeclared `/bin/sh` or of the launcher stub | exit 71 |
| Non-empty output root | entry refuses, exit 1 |

**Map-executable ablation.** The exact profile *without* `file-map-executable`
still ran preparation to parity. `_socket.so` also loaded without it
(`probe-network-widened-without-map`). So on this build, loading of non-system
native code is gated by the `file-read*` literals, not by map-executable. The
line is kept only as a scope statement and is not a required grant.

**`site`.** `import site` inside the child succeeds, because `site` is frozen
into the dylib. Under `-S` it is inert: `sys.path` stays the three stdlib
entries, with no `site-packages`.

**Environment.** Even with `env={}`, the child sees `LC_CTYPE` (PEP 538
coercion) and `__CF_USER_TEXT_ENCODING` (CoreFoundation). Its fds are 0–2 from
the parent plus ones it opens itself.

## 5. Remaining effect surface and limitations

- **Output root contents are fully child-controlled.** The child can create
  symlinks, extra files and large files there. Only the parent's lstat/O_NOFOLLOW
  collection of the three known names makes them safe; that was demonstrated
  with candidate-03's collector.
- **Self re-exec is possible.** `process-exec (literal PY_APP)` is needed for
  `sandbox-exec`'s own `execvp`, and SBPL cannot make it one-shot. The replacement
  inherits the sandbox and has no environment. It can drop `-I -B -S`, but
  `site.py`, `.pyc` and `site-packages` are unreadable and the env is empty, so
  this gains no new reads.
- **The syslog datagram socket** is kernel-allowed by `system.sb`. The exact
  grant set exposes no socket API (no `_socket`/`_ctypes`). That rests on
  import-level absence plus the fact that `posix` has no socket calls, which is
  weaker than a kernel denial.
- **Host identity** is readable: hostname, username (opendirectoryd via
  `system.sb`) and CPU count. So are the OS files `system.sb` allows and the
  names inside the 7 granted stdlib directories. The only exfiltration channels
  are stdout/stderr pipes and the syslog socket noted above.
- **The native closure is not proven complete.** Trust covers the pinned
  `Python` dylib, which includes its frozen/built-in modules, plus
  CoreFoundation and the dyld shared cache as allowed by `system.sb`. I did not
  enumerate libraries loaded lazily by CoreFoundation.
- **TOCTOU on Homebrew files.** The files are owned and writable by the host
  user. Pins are checked at render time, not atomically with exec. The framework
  cannot simply be snapshotted, because of absolute install names
  (`/opt/homebrew/opt/python@3.14/…` in `LC_ID_DYLIB`, Cellar path in the loader).
  The stdlib `__pycache__` was modified today (16:16) by some unconfined run;
  the child never reads it.
- **Denial logs are incomplete evidence.** Kernel sandbox reports are
  deduplicated: positive runs showed 0, although `.pyc` reads are attempted and
  denied, as seen in the ablation. Conclusions rely on return codes and parent
  checks, not on the logs.
- **Brittleness.** Grants are specific to the 3.14.6 bottle and to the
  `prepare.py` import set. A new import in `prepare.py`, or any Homebrew upgrade,
  fails closed and needs `pin_python.py` again. `sandbox-exec` is deprecated and
  `system.sb` is private and subject to change, so re-probe after OS updates.
- **Resources.** CPU, memory, disk use in the output root, and time are not
  bounded by the profile. The only bound is the runner's timeout.

## 6. Integration proposal for root (not applied)

1. **Parent (unconfined)** keeps only these steps:
   - verify code, input and interpreter pins (`logs/python-grants.json` shape);
   - write `raw-schemas.json`/`options.json` read-only into a fresh directory;
   - snapshot `prepare.py` + `runtime/schema.ts` into a separate code directory;
   - create an empty output root;
   - render the §2 profile from `realpath`s;
   - run the entry with the §2 run shape.
2. **Fail closed** on a missing `sandbox-exec`/`system.sb`, any pin mismatch, a
   non-zero exit, or a timeout. There is no unconfined `prepare` fallback.
3. After exit, `collect_outputs(output, {'owners.json','rust-projection.json','ts-projection.json'})`.
   Then build the fresh merged inputs directory from the collected bytes plus
   the parent's own options, raw schemas and provenance.
4. Treat `prepare-inputs.py` as a pinned closure file, run in script mode only.

## Reproduce

```sh
cd /private/tmp/opensip-implementation/m1-generator-python-confinement-trial-01
python3 -I -B scripts/build_work.py    # work/ from pinned source/ (logs/work-manifest.json)
python3 -I -B scripts/pin_python.py    # confined discovery -> logs/python-grants.json
python3 -I -B scripts/run_trial.py     # runs/*, logs/results.json (~1 min, reads `log show`)
python3 -I -B scripts/summarize.py     # logs/summary.md
```
