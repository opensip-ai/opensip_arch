# CF-P — the confinement-feasibility probe: record

**Record, not law.** CF-P is a lead trial with a trivial test child: no provider, no repository bytes, and no product code. It feeds D-law acceptance (M3P:85, M3P:208, M3P:213, M3P:526) and section F of the M3-D draft (DP:758-940). It claims nothing as **enforced**. Under DP F-8 only CF-1 may make that claim, per measured matrix cell.

2026-10-04. Run by a lead-dispatched agent for Claude Opus 5.5, the implementation lead, during the overnight autonomous run. Nothing was committed.

## Short names

- **M3P** `docs/implementation/m3/M3-PLAN.md` (r6, live).
- **DP** `docs/implementation/m3/supervisor-d/PROPOSAL.md` (M3-D r1 draft). DP items, DP F-n, MX-n and LX-n are the ids defined there.
- **SDK27** `/Library/Developer/CommandLineTools/SDKs/MacOSX27.0.sdk/`. **SDK26.5** `…/MacOSX26.5.sdk/`.
- **LOG** `probe/cfp-run.log`, the final full run's output, cited by line (`LOG:n`). Each trial is a block headed `=== RUN rNN-…`:
  - `H` lines are the host (harness) side;
  - `| L` is the launcher;
  - `| T` lines are the confined child's tests;
  - `| E` lines are the child's own environment.
- **PROBE** `probe/`. It holds:
  - `cfp.c`, the harness, launcher and test child;
  - `provider.sb` and `tool.sb`, the DP F-3 profile drafts;
  - `t_named.c` and `t_reason.c`, the side tests;
  - `run.sh`;
  - `build.log`, the compiler's deprecation diagnostics;
  - `mach-denials.txt`, launchd's denied-lookup lines for the final run, from the unified log.

## Host

| Fact | Value | Evidence |
|---|---|---|
| OS | macOS 27.0, build 26A428; Darwin 27.0.0, `xnu-13432.1.9~1/RELEASE_ARM64_T6050`, arm64 (Apple M5 Max) | LOG:1-4 (`sw_vers`, `uname -a`) |
| SDK | MacOSX27.0.sdk, SDK version 27.0, SDK build 26A425 | LOG:5-6; SDK27 `System/Library/CoreServices/SystemVersion.plist` |
| `libsystem_sandbox` | current-version 3051.0.52 (SDK26.5: 2680.120.12) | SDK27 `usr/lib/system/libsystem_sandbox.tbd:6`; SDK26.5 same file `:5` |
| Compiler | Apple clang 21.0.0 (clang-2100.3.34.2), Command Line Tools 27.0.0.0.1788430756 | LOG:7 |
| Probe | C, built with `clang -O1 -Wall` and run at `nice -n 10`, under `$(getconf DARWIN_USER_TEMP_DIR)cfp-probe` (canonical `/private/var/folders/rq/…/T/cfp-probe`) | `probe/run.sh` |
| Real home | `~/Library/Application Support/OpenSIP` was absent before and after. The only home paths touched were the pinned Node binary under `~/.nvm`, executed by r15 and r16, and a name-only listing of `~/Library/Logs/DiagnosticReports`. One OS side effect is disclosed under "Side effects". | `ls` before and after the run |

## Method

1. **`cfp harness` is the host.** It runs unconfined, with a synthetic canary `CFP_CANARY_HOST` in its exec-time environment. It does the following:
   - spawns a same-user **sibling** (`cfp sleeper`) holding the canary `CFP_CANARY_SIB`;
   - picks a closed loopback TCP port and a closed loopback UDP port;
   - runs each trial in a fresh run directory. That directory holds:
     - `scratch/` (0700), planted with a symlink `link` to `outside/existing.txt` and a hard link `prehl` to `outside/prelinked.txt`;
     - an `outside/` sibling directory, with `existing.txt`, `victim.txt`, `prelinked.txt` and a canary `readable.txt`;
     - an AF_UNIX listener the test creates in the run base.
2. **It spawns the launcher as DP items 4-7 specify.** The spawn uses `posix_spawn` with `POSIX_SPAWN_SETSID | POSIX_SPAWN_CLOEXEC_DEFAULT | POSIX_SPAWN_SETSIGDEF | POSIX_SPAWN_SETSIGMASK`, with every signal defaulted and an empty mask. Fresh pipes are `dup2`ed onto fds 0 to 4, the cwd is set with `posix_spawn_file_actions_addchdir(scratch)`, and the environment is constructed from empty as `{OPENSIP_PROBE_CLASS=provider, LANG=C}`. The host itself ignores `SIGPIPE` and blocks `SIGUSR2`, so the reset flags are observable.
3. **`cfp launch` is DP F-1's launcher in miniature.** It is single-threaded. It:
   - sets `RLIMIT_CORE` to 0;
   - reads the SBPL profile;
   - applies it through the API under test, timing the call;
   - prints `rc`, the error text and `sandbox_check(getpid(), NULL, 0)`;
   - calls `execve` on `TARGET`.
4. **`cfp child <set>` is the trivial test child.** It runs the sets below and prints `ALLOWED`, or `DENIED`/`FAILED` with errno, for each attempt:
   - state: ids, tty, fds, signals and rlimit;
   - network: TCP, UDP, DNS, AF_UNIX and mach-lookup;
   - writes: 19 variants, plus one outside read;
   - environment: `KERN_PROCARGS2`/`KERN_PROCARGS` and `proc_pidinfo`;
   - signals;
   - process: fork, `posix_spawn`, exec and re-apply.

   **A control trial (r01, no profile) runs the same tests,** so every denial is distinguished from an ordinary failure. For example, TCP fails with `ECONNREFUSED` in the control and `EPERM` when confined.
5. **After each trial the host records:**
   - the `EVFILT_PROC` event;
   - `waitid(WNOWAIT)`;
   - the `wait4` status;
   - its own `SIGUSR1` count;
   - the listener's accepted connections;
   - the bytes and mode of the outside files, and a listing of `outside/`.
6. **Network traffic** was limited to:
   - a TCP connect to a **closed** port on 127.0.0.1;
   - a 1-byte UDP datagram to a **closed** port on 127.0.0.1;
   - a DNS lookup of `example.com`, which actually resolved only in the unconfined control (LOG:28);
   - an AF_UNIX connect to the test's own listener;
   - two bootstrap look-ups, which send no message.

**Trials** (`probe/cfp.c`, `harness_main`):

| Trial | API | Profile | What it isolates |
|---|---|---|---|
| r01 | none | — | control |
| r02 | `sandbox_init_with_parameters` | `provider.sb` | the F-3 provider profile (main trial) |
| r03 | `sandbox_init(text, 0)` | `provider.sb`, params substituted textually | the declared function in its undocumented inline-SBPL mode |
| r04 | `sandbox_init(kSBXProfileNoNetwork, SANDBOX_NAMED)` | named | the only **documented** mode |
| r05 / r06 | `…_with_parameters` | provider without the `file-link` line / without `(deny mach-lookup)` | which rule does what |
| r07 | `…_with_parameters` | provider, with `SCRATCH` as `/var/…` rather than `/private/var/…` | path canonicalization |
| r08 / r09 | `…_with_parameters` | `tool.sb` | inheritance across fork and exec, `setsid`, MX-7's group tree |
| r10-r14 | `…_with_parameters`, `sandbox_init` | malformed or parameter cases | failure behaviour |
| r17 / r18 | `…_with_parameters` | provider plus a `sysctl-read` deny, exact name / prefix | the MX-5 amendment |
| r19-r22 | `…_with_parameters` | single `file-link` or `file-write*` rules | the hard-link operation name (MX-3) |
| r15 / r16 | `…_with_parameters` | provider / provider without the mach deny; `TARGET` = pinned Node 24.16.0 | MX-6 (optional) |
| side | `sandbox_init(…, SANDBOX_NAMED)` | named | the exit reason of r04's kill (`t_named`, `t_reason`) |

## The API surface on macOS 27

| Symbol | Declared | Exported | Behaviour measured here |
|---|---|---|---|
| `sandbox_init` | SDK27 `usr/include/sandbox.h:46-49`: `API_DEPRECATED("No longer supported", macos(10.5, 10.8), …)`. The header comment (`sandbox.h:6-10`) says the header "is deprecated and may be removed in a future release". `flags` "Must be SANDBOX_NAMED. All other values are reserved" (`sandbox.h:32-33`). | `libsystem_sandbox.tbd:65` | **Documented mode** (`SANDBOX_NAMED`, `kSBXProfileNoNetwork`): **the process is SIGKILLed inside the call and it never returns.** Exit reason namespace 25 = `OS_REASON_SANDBOX` (XNU `bsd/sys/reason.h`), code 0x1 (LOG:211-216; side test LOG:632-635). `kSBXProfileNoInternet` dies the same way. **Undocumented mode** (`flags = 0`, inline SBPL): it works, with behaviour identical to r02 (LOG:144-208). It has no parameters: a `(param …)` evaluates to `#f`, and the apply fails with "invalid data type of path filter; expected pattern, got boolean" (r13, LOG:454). |
| `sandbox_init_with_parameters` | **No SDK27 header declares it.** It appears only in `usr/lib/system/libsystem_sandbox.tbd:66` and the `libSystem.B` re-export stubs. It carries no availability attribute, so the compiler emits no deprecation diagnostic (`probe/build.log` warns only for `sandbox_init` and `sandbox_free_error`). | yes, in SDK27 and SDK26.5 | **It works** (r02, LOG:80-134). Parameters are a NULL-terminated key/value `const char *const[]`, and a NULL array is accepted (r14, LOG:578). A missing parameter **fails closed** at apply (r12, LOG:441). |
| `sandbox_free_error` | `sandbox.h:66-68`, deprecated the same way | `tbd:64` | It frees the error buffer. |
| `sandbox_check` | undeclared | `tbd:42` | `sandbox_check(getpid(), NULL, 0)` is 1 confined and 0 unconfined (LOG:15, LOG:80). It is usable as the launcher's self-check. |
| `kSBXProfile*` constants | **Removed from SDK27's `sandbox.h`.** SDK26.5's `sandbox.h:57-87` still declares all five. | still exported (`tbd:27-28`) | They are the strings `no-network`, `no-internet` and so on (LOG:633). They are usable only through the killed named mode. |
| `sandbox_compile_string`, `sandbox_apply`, `sandbox_create_params`, `sandbox_set_param` | undeclared | `usr/lib/libsandbox.1.tbd`. Not loaded by default (LOG:9, `dlsym` = 0). | **Not tested.** A private second path, noted for CF-1 only. |
| `/usr/bin/sandbox-exec` | `sandbox-exec(1)`: "DEPRECATED" | present | Not used. DP F-1 rejects it. |

**Failure behaviour** (r10-r14, LOG:391-460):
- **The return code and errno.** `rc` is −1 and **`errno` stays 0**. The error text is only in `*errorbuf`; for syntax errors it includes a "Backtrace" with a line and column.
- **The library also writes `sandbox initialization failed: <msg>` to fd 2 by itself** (LOG:126-127, LOG:394, LOG:417, LOG:440, LOG:453). For F-1 this means fd 2, the provider's stderr channel, can carry launcher-failure text. fd 6's one-byte status stays the only authoritative signal.
- **Unknown operations** are compile errors (`(deny process-setsid)` gives "unbound variable: process-setsid", LOG:423). A typo in a closure-member profile therefore fails closed at apply, never silently.

**Apply cost.** 3,983–5,970 µs per `sandbox_init_with_parameters` call, including SBPL compilation of the 11-line profile (the `apply_us` values on the LOG `| L` lines).

**No re-confinement from inside.** A confined child calling `sandbox_init` or `sandbox_init_with_parameters` again gets −1, "Operation not permitted" (LOG:128-129). The profile cannot be replaced or loosened from within.
- **Observation, not relied on:** in the unconfined control, applying `(allow default)` twice returned 0 both times (LOG:62-63).

## MX checklist

### MX-1: `sandbox_init_with_parameters` from a single-threaded launcher applies a profile that persists across `execve` and is inherited — **PASS**

- **Applies:** `rc=0`, `sandbox_check=1` (LOG:80).
- **Persists across `execve`:** the exec'd child reports `sandbox_check=1` (LOG:82), and every denial in LOG:84-134 happens in the post-exec image. It also persists across exec of a different binary outside the probe directory, the pinned Node (LOG:603-608).
- **Inherited by children and their exec'd images** (tool profile, r08):
  - a forked grandchild runs under the profile;
  - a grandchild that `execve`s `cfp child inherit` reports `sandbox_check=1`, with TCP connect `EPERM`, an outside write `EPERM` and an inside write allowed (LOG:349-354).
- **Parameters must be canonical paths (finding).** With `SCRATCH=/var/folders/…`, the symlinked spelling of `/private/var/folders/…`, a write **inside** scratch is denied (r07, LOG:328). Seatbelt matches resolved vnode paths. The launcher record's `SCRATCH`, `TARGET` and `CLOSURE_ROOT` must be `realpath`-canonical. The same applies to `TARGET`'s `literal` exec rule.

### MX-2: TCP, UDP and DNS are denied under `(deny network*)` — **PASS**

| Attempt | Control r01 | Provider r02 |
|---|---|---|
| `socket(AF_INET, SOCK_STREAM)` | allowed | **allowed**: denial happens at use, not at creation (LOG:89) |
| TCP connect to 127.0.0.1, closed port | `ECONNREFUSED` (LOG:25) | **`EPERM`** (LOG:90) |
| UDP `sendto` to 127.0.0.1, closed port | sent (LOG:27) | **`EPERM`** (LOG:92) |
| `getaddrinfo("example.com")` | resolved, 2 addresses (LOG:28) | **`EAI_NONAME`** (LOG:93) |
| AF_UNIX connect to the test's listener | connected; listener accepted 1 (LOG:29, LOG:72) | **`EPERM`**; listener accepted 0 (LOG:94, LOG:139) |
| `bootstrap_look_up` of `com.apple.dnssd.service` and `com.apple.SystemConfiguration.configd` | `KERN_SUCCESS` (LOG:30-31) | **1100**, `BOOTSTRAP_NOT_PRIVILEGED`, under `(deny mach-lookup)` (LOG:95-96) |

- **DNS is denied by `(deny network*)` alone.** With mach-lookup allowed (r06), DNS still fails `EAI_NONAME`, while the look-up of `com.apple.dnssd.service` succeeds (LOG:299-302). libinfo reaches mDNSResponder over a socket that `network*` covers.
- **The daemon-mediated residual (DP F-3) is real.** Without `(deny mach-lookup)`, a child can obtain send rights to network-capable daemons (LOG:301-302). With it, it cannot (LOG:95-96). This probe sent no messages to any daemon.

### MX-3: writes outside `SCRATCH` are denied, writes inside succeed, and hard-link creation into scratch can be denied — **PASS, with one residual**

- **Denied outside scratch, every one `EPERM`** (LOG:100-114):
  - create, `O_TRUNC` open, append and `truncate`;
  - `chmod`, `utimes` and `setxattr`;
  - `mkdir` and symlink creation;
  - rename scratch to outside, and rename outside to scratch;
  - a write through a symlink planted in scratch, because Seatbelt resolves the target;
  - `unlink`.

  Afterwards the outside files' bytes and modes are unchanged, and no entry was added (LOG:140, LOG:142).
- **Allowed:** create and `mkdir` inside scratch, and writes to `/dev/null` (LOG:97-99). A `/dev/tty` open is also denied (LOG:84), because it is a write open outside scratch; unconfined, it fails `ENXIO` anyway (LOG:19).
- **The hard-link operation name is `file-link`** (r19-r22, LOG:507-572). It is evaluated against **both** the source and the destination path:

  | Rule alone | out→in | in→in | in→out |
  |---|---|---|---|
  | `(deny file-link)` | denied | denied | denied |
  | `(deny file-write* (require-not (subpath SCRATCH)))` | **denied** | allowed | denied |
  | `(deny file-link (subpath SCRATCH))` | denied | denied | denied |
  | `(deny file-link (require-not (subpath SCRATCH)))` | denied | allowed | denied |

  So the F-3 write rule alone already denies linking an outside file into scratch (r05, LOG:222-286, is the provider profile without the `file-link` line). The explicit `(deny file-link (require-not (subpath SCRATCH)))` gives the same result under its own name. **The recommendation is to keep both.**
- **Residual (finding): a hard link that already exists is a write path.** The host planted `scratch/prehl`, a hard link to `outside/prelinked.txt`, **before** confinement. The confined child's append through it **succeeded**, and the outside file's bytes changed (LOG:112, LOG:141). Seatbelt checks the path used, not the inode. The child cannot create such a link (above), so the exposure is limited to links that an unconfined same-user process, or the host itself, places in scratch. D1 must:
  - create scratch fresh (DP item 6's `mkdirat` 0700 already does);
  - never link into it.

  E-WRITE's "a hard link of an outside file into scratch, then a write" passes at the creation step. CF-1's wording must carry the pre-existing-link case.

### MX-4: `process-fork` and `process-exec` work, and Seatbelt has no `setsid` filter — **PASS**

- **`(deny process-fork)`:**
  - `fork()` fails `EPERM` (LOG:130);
  - **`posix_spawn` is also denied** (`EPERM`), both of the `TARGET` binary itself and of `/usr/bin/true` (LOG:131-132), so the fork check covers `posix_spawn`;
  - Node's `child_process.spawnSync` also gets `EPERM` (LOG:607).

  A provider's tree is therefore its root, as DP F-5 needs.
- **`(deny process-exec (require-not (literal TARGET)))`:** `execve("/bin/echo")` fails `EPERM` (LOG:134). The launcher's own exec of `TARGET` succeeds (every run).
- **Tool profile:** fork is allowed (LOG:345); exec beneath `CLOSURE_ROOT` is allowed (LOG:349); `/bin/echo` outside it is denied (LOG:356).
- **There is no `setsid` filter.**
  - SBPL has no such operation: `(deny process-setsid)` is "unbound variable" (LOG:423).
  - A tool grandchild's `setsid()` succeeds and leaves the group (pgid 94010 → 94011, LOG:346-348).
  - DP F-5's tool residual on macOS is confirmed.
  - The provider's `setsid` `EPERM` (LOG:133) is POSIX's, because the child is already a session leader under `POSIX_SPAWN_SETSID`. It is not Seatbelt's.

### MX-5: `process-info*` denial blocks reading another process's `KERN_PROCARGS2` — **FAIL as written; PASS with an amendment**

- **What `(deny process-info* (target others))` covers.** It denies `proc_pidinfo(PROC_PIDTBSDINFO)` and `proc_pidpath` of the host (LOG:120-121). It does **not** cover `sysctl` `KERN_PROCARGS2` or `KERN_PROCARGS`: the confined child read the host's and the sibling's environment, with the canary **found** (LOG:117-119). `proc_listpids(PROC_ALL_PIDS)` also remains allowed (LOG:122); it enumerates pids, not environments.
- **What closes it: `(deny sysctl-read (sysctl-name-prefix "kern.procargs"))`.** The host's and the sibling's `KERN_PROCARGS2` and `KERN_PROCARGS` are then `EPERM` with no bytes, while the child's **own** `KERN_PROCARGS2` stays readable (r18, LOG:491-494). The exact name `(sysctl-name "kern.procargs2")` does **not** match (r17, LOG:469-472). The kernel evaluates a per-pid name below `kern.procargs2.` (the system profiles' `(sysctl-name-prefix "kern.proc.pid.")` follows the same pattern).
- **Amendment for DP F-3 r2:** add `(deny sysctl-read (sysctl-name-prefix "kern.procargs"))` to the provider and tool profiles. Without it, E-ENV (b) and (c) fail on macOS.
- **E-ENV (a) passes.** The confined child's environment is exactly the constructed set, `OPENSIP_PROBE_CLASS=provider` and `LANG=C` (LOG:87-88). Neither the launcher nor libSystem adds anything.
- **Reads are unrestricted, as F-8's residual intends.** The child read the outside canary file (LOG:115).
- **Signals.** `(deny signal (target others))` denies `kill(host, SIGUSR1)` and `kill(host, 0)` (LOG:123-124), and the host received 0 signals (LOG:139; 1 in the control, LOG:72). `kill(self, 0)` is allowed (LOG:125).

### MX-6 (optional): the pinned Node 24.16.0 starts a trivial script under the provider profile; the mach-lookup allowlist — **PASS for a trivial script, with the allowlist empty**

- **r15:** `TARGET` = `~/.nvm/versions/node/v24.16.0/bin/node` under the full provider profile, `(deny mach-lookup)` included, with `node -e <script>`:
  - it prints `v24.16.0` (LOG:604);
  - it writes inside scratch (LOG:605);
  - an outside write is `EPERM` (LOG:606), `spawnSync` is `EPERM` (LOG:607) and a TCP connect is `EPERM` (LOG:608);
  - it exits 0, with a peak resident set of 47.9 MB (LOG:611).
- **r16, without the mach deny,** also starts (LOG:621).
- **launchd's denied look-ups** (`probe/mach-denials.txt`):
  - **Node:** `com.apple.system.notification_center` and `com.apple.system.opendirectoryd.libinfo`;
  - **the C child:** those two plus `com.apple.logd`, and the test's own `dnssd` and `configd` look-ups.

  None was needed for these trivial programs. **A trivial allowlist is therefore empty.** The real allowlist, for the TS2 SDK under BBC's argv including `--no-addons`, and for Rust3's `rustc_driver` sidecar and its `rustc` temporaries, is CF-1's (F4, G2).
- **Logging.** Only mach-lookup violations appeared as `Sandbox: … deny(1)` reports in the unified log at default level, with backtraces. File-write and network denials produced no report there in the 20-minute window checked.

### MX-7: `EVFILT_PROC`/`NOTE_EXIT` on an unreaped child, and `proc_listpids(PROC_PGRP_ONLY)` enumeration, behave as DP items 4 and 18 assume — **PASS**

**Spawn attributes (DP items 4-7):**
- `getsid` and `getpgid` of the child both equal its pid (LOG:78, LOG:83).
- There is no controlling terminal: `/dev/tty` fails `ENXIO` in the control (LOG:19).
- `POSIX_SPAWN_CLOEXEC_DEFAULT` leaves exactly fds 0 to 4 (LOG:85).
- `SETSIGDEF` resets the host's ignored `SIGPIPE` to default, and `SETSIGMASK` clears the host's blocked `SIGUSR2` (LOG:86).
- `RLIMIT_CORE` is 0/0 (LOG:86).
- `posix_spawn_file_actions_addchdir`, the non-`_np` form that is macOS 26+ (SDK27 `usr/include/spawn.h:72-73`), sets the cwd to scratch (LOG:83).

**Exit observation:**
- `EVFILT_PROC` with `NOTE_EXIT|NOTE_EXITSTATUS` registers on the unreaped child. It fires with fflags `0x84000000` and the wait status in `data`: 0x0 on a normal exit, 0x9 on SIGKILL (LOG:136, LOG:377).
- `waitid(P_PID, …, WEXITED|WNOWAIT)` then returns `CLD_EXITED` or `CLD_KILLED` (LOG:137, LOG:378). The child stays waitable, and `kill(pid, 0)` still succeeds on the zombie, so its pid stays reserved until `wait4` (LOG:137). `wait4` returns the rusage (LOG:138).

**The group tree** (r09, tool profile; the root forks gc1, which stays in the group, and gc2, which `setsid`s):
- `proc_listpids(PROC_PGRP_ONLY, root)` lists root and gc1 and **excludes** gc2 (LOG:372).
- `proc_listchildpids(root)` lists gc1 and gc2 (LOG:373).
  - **API note:** it returns a **count of pids** (2), whereas `proc_listpids` returns **bytes**.
- `pbi_start_tvsec`/`pbi_start_tvusec` are read for identity (LOG:374).
- `killpg(root, SIGKILL)` while the root is unreaped returns 0, and `NOTE_EXIT` fires (LOG:376-377).
- After the kill, `proc_listpids(PGRP)` lists **only the zombie root** (LOG:379).
- **`killpg(root, 0)` on a group whose only member is the zombie returns `EPERM`, not `ESRCH`** (LOG:380). D3 must not read a `killpg` error as "group empty"; it uses the enumeration.
- **The escaped gc2 survives the group kill**, reparented to launchd (ppid 1) with its start time matching the snapshot (LOG:381-382). The identity-checked best-effort kill removes it (LOG:383-384). This is DP item 18's macOS table as written: guaranteed for group members, best effort for escapees.

## Verdict (macOS 27)

**Programmatic Seatbelt confinement is feasible on macOS 27.0 (26A428) through `sandbox_init_with_parameters`,** called by a single-threaded launcher before `execve`.
- **It enforces, on a trivial child:**
  - denial of direct-socket network and DNS;
  - denial of writes outside scratch, with writes inside scratch working;
  - denial of process creation and of foreign exec;
  - denial of signals to, and process-info of, other processes;
  - persistence across exec and inheritance.

  The pinned Node runtime starts under it with an empty mach-lookup allowlist.
- **Use `sandbox_init_with_parameters`. Use neither mode of `sandbox_init`:**
  - the **documented** mode (`SANDBOX_NAMED`) is SIGKILLed by the OS on 27;
  - the inline-SBPL mode (`flags = 0`) is outside the header's contract ("All other values are reserved") and has no parameters. Paths would be spliced into SBPL text, which is an injection hazard for any path containing `"` or `\`.
- **Before D-law acceptance, DP r2 must change F-3:**
  1. **Add `(deny sysctl-read (sysctl-name-prefix "kern.procargs"))`** (MX-5); otherwise the ambient-environment read of other processes is open.
  2. **Require `realpath`-canonical** `SCRATCH`, `TARGET` and `CLOSURE_ROOT` (MX-1).
  3. **Name `file-link`** as the hard-link operation, keeping the `file-write*` rule (MX-3).
  4. **State the pre-existing hard-link residual** (MX-3).
  5. **Account for `libsystem_sandbox`'s own fd 2 message** on apply failure, with `errno` 0 (F-1).
- **MX-1, MX-2, MX-3, MX-4 and MX-7 pass. MX-5 passes only with amendment 1.** MX-6 passes for a trivial script; the real allowlist is CF-1's.

## Deprecation risk

**High in principle, and moving on 27.** Measured, not assumed:
- **The whole `sandbox.h` is deprecated and "may be removed".** `sandbox_init` and `sandbox_free_error` have been `API_DEPRECATED("No longer supported")` since macOS 10.8 (SDK27 `sandbox.h:6-10`, `:46-49`, `:66-68`).
- **macOS 27 actively retired part of the surface.** SDK27 dropped the `kSBXProfile*` declarations that SDK26.5 still carried (SDK26.5 `sandbox.h:57-87`), and the named-profile mode now kills the caller with `OS_REASON_SANDBOX`. Whether 26 also killed it was not measurable on this host.
- **`sandbox_init_with_parameters` is a private, undeclared export.** It is still present in 27 (`libsystem_sandbox.tbd:66`, library 3051.0.52) and in SDK26.5. Apple makes no promise about it. Its absence of a deprecation attribute only reflects that it has no declaration.
- **Ecosystem precedent lowers short-term risk but is not support.** Chromium's `sandbox/mac/seatbelt.cc` declares and uses `sandbox_init_with_parameters`, as well as `sandbox_compile_string`/`sandbox_apply` (read from chromium.googlesource.com, 2026-10-04), and `/usr/bin/sandbox-exec` still ships.
- **Mitigation, already in DP F-3 and F-4.** Each macOS release major needs its own CF-1 measured row. An unmeasured major, an unresolvable symbol, or an apply that kills or fails takes F-4's path:
  - a missing symbol or an unmeasured major means **unavailable → disclose**;
  - an apply failure means **refuse**.

  **Recommendation for D1:** resolve the symbol with `dlsym` at availability-probe time, not with a link-time import. A future removal then degrades to disclosure instead of a launcher that fails to load. And run the apply only inside the launcher, so that an OS-side SIGKILL (as with r04) kills the launcher, which the host settles as `confinement-refused`, never the host itself.

## Linux desk check (LX-1..LX-14)

**A desk check only.** There is no Linux host here. Every row is a documented fact with a citation, never a measurement. DP item 8's rule applies: Linux rows are "not run" until a Linux lane runs them. The sources were read on 2026-10-04.

**Platform facts:**
- **AL2023 glibc is 2.34** (docs.aws.amazon.com/linux/al2023/ug/core-glibc.html).
- **AL2023 now ships three kernels: 6.1, 6.12 and 6.18.** AWS: "Starting August 17, 2026, the default kernel for AL2023 will change from 6.1 to 6.18". 6.1, 6.12 and 6.18 all remain supported (docs.aws.amazon.com/linux/al2023/ug/kernel-update.html). **This corrects DP's "AL2023's 6.1, and 6.12 where offered"** (DP:927).
- **AL2023 kernels have had Landlock only since August 2025.** "The Landlock feature `CONFIG_SECURITY_LANDLOCK` is now enabled for kernel 6.1 & 6.12" (release notes 2023.8.20250804, which ship kernel-6.1.147 and kernel6.12-6.12.40). That release was later **recalled** for an `auditd` soft lockup.
- **Ubuntu 24.04:** glibc 2.39 and kernel 6.8 GA. The HWE kernels are 6.11, 6.14, 6.17 and 7.0 (documentation.ubuntu.com/release-notes/24.04; canonical-kernel-docs HWE table).

| Id | Fact (source) | AL2023 | Ubuntu 24.04 |
|---|---|---|---|
| LX-1 | `POSIX_SPAWN_SETSID` arrived in glibc 2.26 (glibc NEWS 2.26; posix_spawn(3)) | yes (2.34) | yes (2.39) |
| LX-2 | `pidfd_open` arrived in Linux 5.3 and `waitid(P_PIDFD)` in 5.4, and `WNOWAIT` is accepted with any idtype. The glibc **wrapper** and `P_PIDFD` arrived in **2.36** (pidfd_open(2), waitid(2), glibc NEWS 2.36). | kernel yes. **glibc 2.34 has neither the wrapper nor `P_PIDFD`.** D1 must use the raw syscall (434 on x86-64 and aarch64) and define `P_PIDFD` = 3 itself. | yes. 2.39 also adds `pidfd_spawn` (CF-1 may consider it). |
| LX-3 | `posix_spawn_file_actions_addclosefrom_np` arrived in glibc 2.34. It uses `close_range`, which needs Linux 5.9, and falls back if that fails (glibc NEWS 2.34) | yes (exactly 2.34) | yes |
| LX-4 | `posix_spawn_file_actions_addchdir_np` arrived in glibc 2.29 (NEWS) | yes | yes |
| LX-5 | `/tmp` as the scratch root. The `fs.protected_*` semantics are in docs.kernel.org admin-guide `sysctl/fs`. | **tmpfs**, "limit of 50% of RAM and a maximum of one million inodes" (AL2023 ug `compare-al2-al2023-tmp`). The `protected_*` defaults depend on systemd 252's `50-default.conf` being unmodified: **UNVERIFIED**. | on disk. `99-protect-links.conf` ships in procps; noble's exact values are **UNVERIFIED** |
| LX-6 | core(5): "The RLIMIT_CORE limit is not enforced for core dumps that are piped to a program." In `fs/coredump.c`, an `RLIMIT_CORE` of exactly **1** aborts before the pipe handler starts ("RLIMIT_CORE is set to 1, aborting core"). `execve` resets dumpable to 1, so `PR_SET_DUMPABLE` set before exec does not persist (PR_SET_DUMPABLE(2const)). | `|/usr/lib/systemd/systemd-coredump … %c …`. systemd-coredump keeps no core when `%c` is below the page size, but it logs to the journal. | apport (`|/usr/share/apport/apport … -c%c …`). With a limit of 0 it writes no user core, and it ignores binaries outside any package, such as closure binaries. |
| LX-7 | `/proc/[pid]/stat`: field 2 (comm) is user-controlled, can contain `)`, spaces or newlines, and is truncated to 15 bytes. Field 4 is ppid and field 5 is pgrp. Safe parsing splits after the **last** `)` (proc_pid_stat(5)). Cost: one `getdents` plus open, read and close per pid, so it is linear in the process count; there is no authoritative figure. | same | same |
| LX-8 | `PR_SET_CHILD_SUBREAPER` arrived in 3.4. Orphans go to "the nearest still living ancestor subreaper", so the host beats a harness subreaper above it (PR_SET_CHILD_SUBREAPER(2const)). | yes | yes |
| LX-9 | `statm` resident is in pages and is documented as "inaccurate"; `smaps_rollup` is accurate but slower (proc_pid_statm(5)). `RLIMIT_RSS` "has effect only in Linux 2.4.x, x < 30" (setrlimit(2)). | same | same |
| LX-10 | Landlock ABI: 1 = 5.13; 2 = 5.19 (REFER); 3 = 6.2 (TRUNCATE); 4 = 6.7 (TCP bind and connect); 5 = 6.10 (IOCTL_DEV); 6 = 6.12 (abstract-socket and signal scoping); 7 = 6.15 (logging). Later ABIs, up to UDP at ABI 10, are on newer kernels (docs.kernel.org `userspace-api/landlock`; landlock(7) VERSIONS). The availability probe is `landlock_create_ruleset(NULL, 0, LANDLOCK_CREATE_RULESET_VERSION)`: `ENOSYS` means not built, and `EOPNOTSUPP` means built but disabled (`lsm=`). | **6.1 → ABI 2; 6.12 → ABI 6; 6.18 → ABI 7**, but only on kernels built from 2023.8.20250804 onward. The AWS kernel-hardening page lists `CONFIG_SECURITY_LANDLOCK=y`. That landlock is in the **active** LSM list is attested only by a third-party report on 6.1.155 (`lockdown,capability,landlock,yama,safesetid,selinux,bpf`). It is **UNVERIFIED for 6.12 and 6.18.** | 6.8 → **ABI 4**; HWE kernels 5-8. Landlock has been in the default `CONFIG_LSM` since Jammy (LP#1953192). A backport raising the ABI on 6.8 is UNVERIFIED. |
| LX-11 | Landlock: "the tracee must be in a sub-domain of the tracer". The hook applies in every ptrace access mode, so it gates both `/proc/<pid>/environ` (`PTRACE_MODE_READ_FSCREDS`, proc_pid_environ(5)) and `/proc/<pid>/mem` (`PTRACE_MODE_ATTACH_FSCREDS`, proc_pid_mem(5)). This has held since 5.13. | yes, wherever Landlock is active | yes |
| LX-12 | Ubuntu 24.04 release notes: an AppArmor default "allows the use of user namespaces for unprivileged and unconfined applications but will deny the subsequent use of any capabilities within the user namespace" (`kernel.apparmor_restrict_unprivileged_userns=1`). **Creation succeeds; capabilities inside it do not.** So `unshare(CLONE_NEWUSER\|CLONE_NEWNET)` fails, by inference: CF-1 runs `unshare -Urn true`. | unprivileged user namespaces appear to be allowed (third-party report: `user.max_user_namespaces=62209`); **UNVERIFIED** | restricted as quoted |
| LX-13 | PR_SET_PDEATHSIG(2const): the parent is "the thread that created this process". The setting is cleared on fork, on set-user-ID, set-group-ID or file-capability execs, and on credential changes. "If the parent thread and all ancestor subreapers have already terminated … no parent-death signal is sent", hence DP F-1's `getppid()` check after setting it. | same | same |
| LX-14 | seccomp(2), docs.kernel.org `seccomp_filter`: the filter needs `no_new_privs` (otherwise `EACCES`), cannot dereference pointers, and must check `arch`. x32 shares `AUDIT_ARCH_X86_64`, so the filter must also refuse `__X32_SYSCALL_BIT`. `clone` `flags` is argument 0 on both x86-64 and arm64 (arm64's `CLONE_BACKWARDS` swaps only tls and child_tid). `clone3` (435) keeps its flags in user memory and **cannot be argument-filtered**. glibc 2.34's `__clone_internal`, used by `posix_spawn` and `pthread_create`, falls back to `clone` **only on `ENOSYS`**; 2.39's `posix_spawn` falls back on `ENOSYS` or `EINVAL`. `EPERM` breaks spawning (LWN 1035182). `socket` and `socketpair` are separate syscalls (x86-64: 41 and 53; aarch64: 198 and 199). | `CONFIG_SECCOMP_FILTER=y` on all three kernels. `CONFIG_X86_X32_ABI=n` but `CONFIG_IA32_EMULATION=y`, so the arch check is load-bearing. | available. x32 status is UNVERIFIED, so the filter covers it anyway. |

**F8 (the network namespace) is confirmed by the desk check.**
- On Ubuntu 24.04 an unprivileged host cannot obtain a working network namespace, because the namespace needs `CAP_SYS_ADMIN` inside the user namespace, which AppArmor denies (LX-12).
- DP F-2's seccomp socket denial gives "no network" without one: `socket()` returns `EPERM` for every domain, and `socketpair(AF_UNIX)` is allowed as a separate syscall.
- Landlock's own network rules would cover only TCP on these kernels: ABI 4 or later, and UDP needs ABI 10.
- M3P:509's next revision should follow F-2.

**Corrections for DP r2** (no outcome changes):
- **LX-2:** AL2023's glibc has no pidfd wrapper and no `P_PIDFD`; use the raw syscall.
- **LX-6 and DP item 7.** On Linux, `RLIMIT_CORE` 0 does not stop a pipe `core_pattern` handler from being invoked. Two consequences:
  - The launcher should set **`RLIMIT_CORE` to 1** on Linux, the kernel's documented abort value, which suppresses both file and pipe dumps.
  - `PR_SET_DUMPABLE(0)` cannot substitute, because `execve` resets it.
- **LX-10:**
  - AL2023's kernel set is now 6.1, 6.12 and 6.18, with 6.18 the default for new instances since 2026-08-17.
  - On 6.1 (ABI 2), F-2's "`truncate` where the ABI is below 3" seccomp rule is required, not optional.
  - On ABI 2, F-2's signal and abstract-socket scoping (ABI 6+) is absent; F-2's seccomp `kill` rules cover signals.

**Linux desk-check verdict for AL2023: feasible, conditionally on the kernel build. Not measured.**
- **Kernel 6.1.147, 6.12.40 or 6.18, or later:**
  - F-2's three layers are available: `no_new_privs`, Landlock at ABI 2, 6 or 7, and seccomp.
  - The ptrace restriction (LX-11) holds wherever Landlock is active.
  - The spawn and supervision primitives (LX-1..LX-4, LX-8) are present, using the raw `pidfd_open` syscall on glibc 2.34 (LX-2).
- **Earlier AL2023 kernel builds have no Landlock at all.** For those, DP F-4's probe returns **unavailable → disclose**, which is exactly F-4's design.
- **The one open AL2023 fact is whether `landlock` is in the *active* LSM list** on the 6.12 and 6.18 kernels; 6.1.155 is attested only by a third-party report. It is CF-1's first AL2023 measurement.
- **The verdict is limited by AL2023's own status.** AL2023 remains reachable only through DR-126's successor (DP item 8, OPP:384).

**Ubuntu 24.04** (GA kernel 6.8):
- F-2 is available at Landlock ABI 4, with landlock in the default LSM list.
- The user-namespace restriction (LX-12) confirms seccomp over a network namespace (F8).

## What CF-1 must still measure

**CF-P establishes feasibility on a trivial child.** CF-1 must measure the rest before D1's enforcement claim and D5's escape controls (DP F-8, M3P:85, M3P:213):

1. **F-7's five controls on real launches, on each platform family.**
   - **macOS:** E-NET, E-WRITE, E-ENV, E-PROC and E-TREE, under the **amended** F-3 profile: with the `kern.procargs` sysctl rule, canonical parameters and `file-link`.
   - **Linux:** all of them, on the Ubuntu 24.04 lane and on the AL2023 kernels 6.1, 6.12 and 6.18.

   No Linux row is "passed" until it runs on a Linux lane.
2. **The mach-lookup allowlist for the real closures (MX-6 proper):**
   - the TS2 SDK under BBC's argv, including `--no-addons`;
   - the Rust3 `rustc_driver` sidecar with `rustc` temporaries directed to scratch (F4, G2);
   - the tool profile with `cargo metadata` (MC item 12).

   CF-1 must also decide **`(with no-report)`** on deny rules. In this probe, mach-lookup violations reached the unified log at default level with backtraces. Path-bearing file or network reports were not seen there, but that is not established in general (OPP §3.2 privacy).
3. **The tool profile's signal rule.** `(deny signal (target others))` would also deny a tool signalling its **own** children (`cargo` → `rustc`). CF-1 must measure `(target children)` or `same-sandbox` alternatives. CF-P did not exercise this.
4. **A signed launcher.** The probe binary is ad hoc. CF-1 must measure the apply under the **signed, hardened-runtime, notarized** `opensip-launch` from the release closure (SD-3), including the launcher-to-target exec of the Node and Rust closure binaries.
5. **The macOS per-major row** (F-3): this record is the row for **27.0 (26A428), `libsystem_sandbox` 3051.0.52**. Each new major, and any update that changes `libsystem_sandbox`, needs a re-run before its cell moves. D1's availability probe should resolve `sandbox_init_with_parameters` with `dlsym` and treat absence as unavailable.
6. **The hard-link residual (MX-3).** CF-1 must state that a hard link already present in scratch is a write path. It must decide whether D1 adds a defensive check, such as refusing to run on a scratch whose entries have `st_nlink > 1` at creation, or whether the fresh-0700 discipline (DP item 6) suffices.
7. **D3 and item 18 notes from MX-7.**
   - `killpg(pgid, 0)` on a zombie-only group returns `EPERM`, so emptiness comes from `proc_listpids(PROC_PGRP_ONLY)`, never from `killpg`'s error.
   - `proc_listchildpids` returns a pid **count**; `proc_listpids` returns bytes.
   - The E-TREE macOS limit was observed exactly as item 18 states: the escapee is reparented to launchd, and only the start-time-checked kill reaches it.
8. **Overhead.** The apply costs about 4 ms per launch here. CF-1 measures the profile's runtime cost on real provider and tool workloads, against D3's budgets.
9. **The Linux UNVERIFIED rows:**
   - Landlock in the active LSM list on AL2023 6.12 and 6.18 (`/sys/kernel/security/lsm`; the `LANDLOCK_CREATE_RULESET_VERSION` probe);
   - AL2023's `fs.protected_*` and user-namespace defaults;
   - Ubuntu 24.04's `unshare -Urn true` refusal;
   - each lane's `core_pattern`, with `RLIMIT_CORE` 1;
   - the cost of the `/proc` scan at a realistic process count (LX-7);
   - the accuracy of `statm` (LX-9).
10. **The interface risk statement in CF-1's wording.** The macOS enforcement rests on an undeclared Apple interface whose documented sibling the OS kills on 27 (see "Deprecation risk"), so every macOS cell is per-major.

## Side effects and deviations

- **The OS wrote crash reports into the real home's log directory.** The killed named-mode runs (r04 in three probe runs, plus the `t_named` side test) caused ReportCrash to write five `.ips` files under `~/Library/Logs/DiagnosticReports/` (`cfp-2026-10-04-0339*.ips`, `cfp-…-0340*.ips`, `t_named-…-034121*.ips`). They were seen by name in the unified log and a directory listing. **They were not opened and not deleted.** The lead may delete them. `~/Library/Application Support/OpenSIP` stayed absent.
- **The private 413 UUID fixture was not read.** No repository bytes were used, and no product code was touched.
- **The AF_UNIX test** is a local listener the test created in its own temp tree. It was not network traffic.
- **The probe ran between run sets** at `nice -n 10`, with no cargo build or test of its own (P5-8, M3P:595).
- **Not done here:**
  - LX items on a Linux host: none is available;
  - a signed or hardened-runtime launcher: the probe is linker-signed ad hoc;
  - real providers.
