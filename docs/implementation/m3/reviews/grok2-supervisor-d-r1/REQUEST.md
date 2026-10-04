GROK2 review: **M3-D r1**, OpenSIP's supervisor and common control law (D1 spawn primitive, D2 codecs, D3 supervisor, D4 manifest and session factory, D5 G21 controls), with an **O7 placeholder section**. This is a **law and fact** review, round 1. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok2-supervisor-d-r1.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs. A timing-sensitive crash-matrix run may be using this machine, so run no `cargo`, no tests, no probes and no lead sets. In particular, do **not** run CF-P or any Seatbelt or Landlock trial yourself; the law lists what CF-P must establish.
- Never touch the real home. `~/Library/Application Support/OpenSIP` must stay absent. If you run `git` anywhere, redirect `HOME` to a private 0700 scratch directory and turn hooks off.
- Never read the private 413 UUID fixture.
- If you compute digests, use read-only scratch scripts under your review directory.

## Subject

The pins are in `hashes.txt`. The subject is untracked in arch until acceptance.
- `docs/implementation/m3/supervisor-d/PROPOSAL.md` (r1) is the subject of `subjectSha256`. It is a law with a unit breakdown; there is no separate UNITS file.

**The unit.** M3-D is the accepted M3 plan's row at `M3-PLAN.md:213` (r6, live). Its gate is CF-P (`M3-PLAN.md:85`, `:213`, `:261`), which has **not run**. The law cannot be accepted until CF-P has run and r2 records its outcome. **Review r1 now anyway**: an ACCEPT verdict here means "accept subject to CF-P's outcome being recorded in r2 with no other change", and the lead will say so when recording it.

**O7 is pending** (owner blocker B1). Section F is written against the lead's O7 recommendation and is marked "binding only once O7 is decided as recommended", with the alternatives in F-0. Everything outside section F is ordinary law and must not depend on O7. Please check that separation.

**Governing and dependent records, and their status (2026-10-04):**
- **Accepted:** M3-PLAN r6; the operability plan r3; the harness design Q0 r13; the analysis-quality plan r6; M3-B r2; M3-C r5 (CODEX2; effective once M3-L and X12 r4 are accepted).
- **Required findings, next round in review:** S-OP-2 (r4 had findings, r5 is with Codex); M3-E1 (r1 had findings, r2 is with Codex); M3-J1 (r1 had seven findings from CODEX2, r2 is drafted).
- **Draft, not sent:** M3-L r1.

D cites S-OP-2 by its r4 snapshot (`operability/s-op-2/PROPOSAL-r4.md`) and J1 by its r1 snapshot (`host-pipeline-j/PROPOSAL-r1.md`), with their lines; it cites M3-C and M3-E1 by item. The S-OP-2 names and kinds D uses are unchanged in r5. If any of these changes before you finish, judge against the pinned bytes and note the drift.

**The product** is `/Users/sb/code/opensip-ai/opensip` at main `3e64266`, read-only. The law's product citations were read at that commit. Every child process in the product today is test-only.

**The macOS 27.0 SDK** on this host (`/Library/Developer/CommandLineTools/SDKs/MacOSX27.0.sdk/`) is cited for API declarations and exports only (`sandbox.h`, `spawn.h`, `sys/spawn.h`, `libproc.h`, `sys/proc_info.h`, `sys/event.h`, `sys/wait.h`, `sys/fcntl.h`, `unistd.h`, `usr/lib/system/libsystem_sandbox.tbd`). Reading them is fine. Linux facts cannot be checked on this host; the law lists them as LX-1..LX-14 for CF-P's desk check and treats none as established. Please check that no item silently relies on an unlisted Linux fact.

## What the law decides (in brief)

1. **D1, `platform/process.rs` (items 1-8).**
   - One production spawner and three closed launch classes: `Provider` (after Plan binding and attempt admission), `Tool` (MC item 12's `cargo metadata` adapter, before PlanId) and `TestFixture` (tests only). No `RepositoryCode` class at M3.
   - `posix_spawn` by absolute path, never `posix_spawnp`; exact argv per class (BBC for TS2, DRJ2 for Rust3); verification bound to spawn by the closure owner's recheck in D4.
   - The environment is built from empty per class (BBC:119-131; DRJ2:102-108; NE CC-1..CC-5). The host reads no environment variable to build it.
   - **A new session per child** (`POSIX_SPAWN_SETSID`), and the **reap-last rule**: the group is signalled only while the root is unreaped.
   - Exactly fds 0-4 for providers (CPC:252-258) and 0-2 for tools, all fresh pipes; `CLOEXEC_DEFAULT` on macOS, `addclosefrom_np` on Linux.
   - Per-child scratch as cwd, under a per-invocation 0700 directory found without the environment (macOS `confstr`; Linux `/tmp`), with a lock-file sweep of dead owners' scratch.
   - Default signals, empty mask, `RLIMIT_CORE` 0 (lead decision: source bytes are P3).
   - A macOS-against-Linux table.
2. **D2, the codecs (items 9-11).**
   - `control_protocol.rs`: CC v5 exactly, 16 messages; the host offers a 65,536-byte frame bound; its own JSON reader keeps integer lexemes for CC's RF2/RF7 precedence; the CC v5 corpus as a conformance test.
   - **The select tuple** (lead decision, ML X5/R3): `analyzer` / provider id / protocol major (2 or 3).
   - `provider_protocol.rs`: one codec per protocol, fixed before spawn; a first-party strict deterministic-CBOR reader with a re-encode canonicality check; serde never over wire bytes; P3T and T2O read as data.
   - Item 11 spells out what "no translation" forbids.
3. **D3, the supervisor (items 12-23).**
   - A state machine with **single settlement** (taken by value; `Drop` on unwinding kills and settles `abandoned`), closed causes, and a `userInterrupted` flag.
   - **Item 13, an EOF and exit delivery join** (lead decision): RPP:170 needs zero-exit before EOF, while CPC J-3 appends EOF before death. An fd1 EOF observed after the terminal is held until the exit is observed.
   - The constants table: Rust3's protocol 5,000 ms grace and exit grace (RPP:119-120); TS2's 2 s provisional; liveness 5 s with an SM-8 floor; a 1,800 s safety deadline; TERM to KILL 1 s; reap 10 s, or 5 s under revocation.
   - Liveness by nonce-matched health; progress only from admitted transitions; no progress is never a fault.
   - **A sampled 8 GiB per-tree memory ceiling** (OS sample or asserted value), process-count bounds, and the byte-bound table, including **a TS2 aggregate response bound** (lead decision; 1 GiB, mirroring Rust3).
   - **stderr counted, never kept** (lead decision), reduced to K7 `{bytes, truncated}`, with **no digest**. The brief's "digest" is OPP r2 wording that r3 withdrew (finding F1).
   - **Tree kill** (item 18): Linux makes the host a subreaper and sweeps its own unreaped children by pid. **macOS has no subreaper**: the group kill is guaranteed; a best-effort, start-time-checked kill covers escaped descendants still in the tree at a pre-kill snapshot; descendants orphaned to `launchd` before the snapshot are neither found nor killed; tree settlement is not claimed on macOS.
   - Cancellation follows ML item 16. The fault ladder follows CPC J-5. Revocation follows SL S6's marks.
   - Candidate discard and admission gated on a clean settlement.
   - Records: S-OP-2 events only, plus ordinary registrations.
   - Outcome joins to J1's existing routes, with no new code.
   - **Harness coexistence** (item 23): no cgroup interface at all; nested subreapers and sessions.
4. **D4, DR-G29 (items 24-26).**
   - Manifest-class refusals (EE-1, EE-3b, EE-4, EE-5a) and request-class refusals (EE-2, EE-4, EE-6a) **before attempt admission**, so no ExecutionId exists.
   - Post-admission substitutions (closure recheck, RF3 echo, tuple, HelloAck identity, any `effectRequest`) are rejected before any source byte.
5. **D5 (item 27).** DR-G21's controls mapped to QG:428's evidence list and OPP §10, run against first-party fake providers, never concurrently with a crash-matrix lead set.
6. **Section F, the O7 placeholder.**
   - F-1: a trusted launcher `opensip-launch` in the host's closure, which applies the profile in a single-threaded context and then calls `execve`.
   - F-2 (Linux): `no_new_privs`, a Landlock write and exec ruleset, and a seccomp denylist with no sockets, no process creation for providers, no `setsid`/`setpgid`, no `ptrace` and no io_uring. **No network namespace** (LX-12; finding F8).
   - F-3 (macOS): `sandbox_init_with_parameters`, which the SDK exports but does not declare; `sandbox_init` is declared "No longer supported". The profile denies `network*`, writes outside scratch, `process-fork`, other `process-exec` and `process-info`/`signal` against others, and `mach-lookup` beyond a measured allowlist.
   - F-4: an unavailable platform means disclose (CF-2); a failed apply step means refuse the launch.
   - F-5: providers have a one-process tree under the profile.
   - F-6: RepoExecutionGrantV2 at M5-EX only.
   - F-7: the three escape controls plus E-PROC and E-TREE.
   - F-8: the CF-P checklist (MX-1..MX-7, LX-1..LX-14) and what CF-1 must measure.
7. **Successors** SD-1..SD-5 (item 29), **findings** F1-F10 (item 30), and **units** D1a, D1b (O7), D2a, D2b, D3a, D3b, D4 and D5, with no change to the 33-day critical path.

## Decide

1. **Facts.** Check the citations, especially:
   - CPC:251-258, :267, :298, :460-494; CC:17-41, :104-140, :171-237;
   - BBC:21-26, :100-140; DRJ2:90-127; DRJ4:42-58; DLV:566-587, :1111-1193; RPP:84-170, :585-601;
   - NE:1724-1741, :2781-3316 (especially :2846-2866, :2929-2942, :2961-2984), :3529, :3837-3850;
   - SL:470-497, :1059-1113, :1306-1311; WS:224-229, :1355-1375; AQ:341-346;
   - REG:317, :366-367, :374; QG:423-461, :583-601; PPBS:665-745; COV:4953-4987, :5162-5176, :7270-7292;
   - OPP:171, :232-238, :273-300, :329-347, :418, :426-437; SOP2:205-218, :254, :775-855; ML items 2, 11-17; HD:813, :844-910;
   - the product lines in the Problem section, and the SDK27 lines.
2. **R1, tree kill.** Is the reap-last rule (item 4) with the Linux sweep (item 18) a sound guarantee? Is the macOS table exactly what can and cannot be guaranteed, with nothing over-claimed?
3. **R2, stderr.** Is count-only capture (item 17) a lawful reading of DLV:1133, given that no lawful reader of the bytes exists at M3 (OPP:401; SOP2:238)?
4. **R3, item 13.** Is the EOF and exit join a host join that F02:171-177 permits, or a reordering that F02:168-169 forbids?
5. **R4, the TS2 aggregate bound.** Is a host safety bound with no wire member lawful under ML item 1 and DLV:1163?
6. **R5, routes.** Item 22, especially WS:1375 over DLV:1170 for spawn failure, and `spawn-refused` as `PROVIDER.PROTOCOL_VIOLATION`.
7. **R6, DR-G29.** Are the EE-class representations (items 24-26) the right mapping from PPBS's prose to the manifest shape and the control plane? Is "no ExecutionId" achieved by the ordering stated?
8. **R7, the harness.** Is anything in D incompatible with HD §9.3's leaf, namespace, subreaper or settlement rules?
9. **R8, section F.** Is the ordinary-law and O7 separation clean? Is F-4's split right (unavailable means disclose; a failed apply means refuse)? Are F-7's controls the right minimum for CF-1, and is F-8's CF-P checklist complete for the claims section F would make?
10. **New errors.** Does anything contradict an accepted law, contract or plan, or claim confinement, measurement or qualification anywhere?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. The design successors SD-2 and SD-3 will each need an `ACCEPT-DESIGN-UNIT` review of their own, and D's code units an `ACCEPT-UNIT` with an `inventoryCandidateAssessment`. Do not commit.
