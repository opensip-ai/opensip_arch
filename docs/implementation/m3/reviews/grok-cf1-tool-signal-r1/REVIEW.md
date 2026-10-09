# CF1-TOOL-SIGNAL-PRELIMINARY-R1

ACCEPT. These are preliminary observations of the open tool-profile signal question. CF-1 stays incomplete, the signal policy stays unselected, and the signed launcher, real provider and tool closures, effective L, and product qualification stay unmeasured.

## Subject

`subject.json` is 11151 bytes, SHA-256 `18e9f1771021cba409b0901b22a3231dd2e11de7d140127b708d7fc37d1f34a0`, schemaVersion 1, unit `CF1-TOOL-SIGNAL-PRELIMINARY-R1`. It pins 42 sorted unique members, and every pinned hash matches the staged bytes. The archive path `docs/implementation/m3/confinement-cf/cf1-tool-signal-trial-2026-10-09` is absent at architecture `df7303c1121a4a352c464f67013e66bb4e9a5d45`. Product `37581132d8099b8fb4ad9ef8fb2f90ff8b89d02d` is clean. The architecture tree's only untracked path is `docs/implementation/m3/syntax-e/e2s/`, outside this packet. `design-lock.json` is 615658 bytes, SHA-256 `018dbfe27c1bbba48dedcf88ff6625ce62072b01bfb0fae0aee8c3dc463fc283`, with 139 inventory successors through `repository-file-inventory.v179.json` and 155 contract successors. The four authority pins match that architecture commit: `PROPOSAL-r5.md`, `CF-P-RECORD.md`, the O7 record, and SD-3 `CONTRACT.md`. Accepted CF-P, F-3, SD-3, and the owner decisions stay closed.

## Rows

Each results file has 12 rows. `checks.json` has the same 24 keys, `passed` true, `count` 24, `policySelected` false, `CF1Complete` false, and `platformQualification` false. Recomputed from the two results files, every row agrees with `checks.json`.

On all 24 rows the child and the grandchild have kill rc 0, errno 0, and `received` 1. Receipt is the handler byte `C` or `G`, read by the parent after a successful kill, and stored separately from the kill return. On all 18 constrained rows the observer kill returned -1 with errno 1 (`EPERM`), and the runner recorded no observer byte. On all 6 unconfined rows the observer kill returned 0 with errno 0 and the runner read the observer byte `O`. Constrained rows have `applyRc` 0 and parent `sandboxCheck` 1. Control rows have `applyRc` 0 and `sandboxCheck` 0, because the profile argument is `none` and the apply entry is left uncalled.

The fork-exec rows add `childAfterExecSandboxCheck` and `grandchildAfterExecSandboxCheck`. Both are 1 on the nine constrained rows and 0 on the three control rows, and each equals that row's parent `sandboxCheck`. All 12 fork-exec rows are present, so the fixture's mismatched-check return did not fire. The children exception and the same-sandbox exception match the original `(deny signal (target others))` row for row.

Both results files record macOS 27.0.1, build `26A434`. The top `REPORT.md` and `fork-only/REPORT.md` are one text, 2953 bytes, SHA-256 `0af71058a0a122080e4ff3536fed6bcd05fcee211ba53000050db8f003297751`. The fork-exec set has its rows and no separate report.

## IPC, ownership, and cleanup

The observer is a separate session of the same ad-hoc binary, started in observer mode. It writes `ready` before the root starts. Its pid is lower than the root pid on every row, and the two pids differ. Observer mode returns before profile apply and before any fork, so the signalled observer is outside the sandboxed descendant tree. The root receives that pid as an argument and calls `kill` on it directly.

Descendants write ready records before any signal. Each record carries a marker and a pid. The parent reads both records and continues only when the markers are `C` and `G` in either order and the pids match: the child's `fork` return and the grandchild's `getpid`. Fork-exec records also carry each descendant's own `sandbox_check`, taken after that descendant's `exec`. The parent signals only after that join.

Cleanup sends `SIGKILL` to the root's process group, then `wait4` on that exact root, then the same pair for the observer. The root stays unreaped until that group cleanup. The runners signal only those two recorded groups. Each runner holds the Darwin lane directory across its compile and its twelve rows, and removes that directory only when it created the directory. Nice is 10. The temporary directory mode is `0700`. `HOME` is passed through unchanged. Compiler logs and fixture stderr files are empty. This review did not rerun clang or the fixtures.

The fork-exec helper is a second clang of the same `fixture.c`, written under the closure directory. The child `execl`s that helper, and the helper `execl`s itself as the grandchild. The helper file still beside the recorded executable has a different hash from that executable.

## Profile boundary

The staged profiles are the F-3 tool-profile shape: the provider body with `process-fork` allowed and `process-exec` allowed beneath `CLOSURE_ROOT`, plus the amended `(deny sysctl-read (sysctl-name-prefix "kern.procargs"))` rule. The three constrained profiles differ only in the final signal rule. The fork-only and fork-exec copies are byte-identical at 423, 469, and 473 bytes. The fixture reads that text and passes `SCRATCH` and `CLOSURE_ROOT` through `sandbox_init_with_parameters`, resolved with `dlsym`, with flags 0. The profile text uses those parameter names and contains no absolute path. Every recorded scratch directory is the resolved temporary directory plus the variant and repeat. The closure argument is that resolved temporary directory. Profile paths recorded in the results name the run directories, and the files there are byte-identical to the staged profiles. The recorded executable hashes still match the binaries in those temporary directories, and the recorded source hashes match the staged `fixture.c` files.

The rows measure SIGUSR1 receipt and denial. Network, file-write, file-link, mach-lookup, and procargs effects are outside these rows. The fixture applies the chosen policy to itself before the test. The binary is ad-hoc first-party clang output.

## Remainder

F-3 and CF-P item 3 leave open the expectation that `(deny signal (target others))` would deny a tool signalling its own children, and they assign CF-1 the measurement of a `target children` or same-sandbox alternative. These rows show the original rule delivering SIGUSR1 to the direct child and the grandchild, and denying the unrelated owned observer with `EPERM`. The two named alternatives produced the same pattern, so the packet selects no rule. The next real signed tool-closure control should measure the original rule again before any broader exception. The signed hardened notarized launcher, real provider and tool bytes, other signals and topologies, Linux lanes, and the rest of the CF-1 row remain outstanding. Existing law and the CF-P record stay as accepted.

Archival of this packet is architecture-only, after this acceptance, root assent, and the actual design check. `verify_design.py` was not run. This review binds no lock and pushes nothing. Inventory stays 179. Contract successors stay 155. Product code stays unchanged.
