**J4a r1 — REQUIRED-FINDINGS**

Codex reviewed the product diff against J-RW r4, X3c r9 and X3b r11. One required finding, **J4A-RF-01**, prevents ACCEPT-UNIT. P-ACL/C-ACL and its RW-P1, RW-P2 and RW-P3 uses have no further required findings.

Subject: `4fbe89f1684846c70f1da639549669a31ee98775e526760f65bfcdede69f8bda` (125557 bytes; 11 existing files, +2567 / −42), against `d2c00a96c3136fe45b901bc067b6d0ca51f0c9c1` in `/Users/sb/code/opensip-ai/opensip-j4a`. The live diff and all 29 supplied pins matched. [Pin verification](pin-verification.json), [reviewed diff](subject.diff), [final worktree verification](output-state.json).

**J4A-RF-01 (P2): Perform C-SUFFIX's capped byte read-back after both barriers**

complete_private_suffix calls write_regular_suffix_reserved, whose verify_written reads and compares every byte and confirms the end before calling the file barrier. The security helper then takes the parent directory barrier, reopens the name, and compares only device, inode and length. It returns success without a capped byte read-back after both barriers. J-RW r4 item 3.2 explicitly orders the missing suffix write, F_FULLFSYNC, the directory barrier, and then exact-length capped read-back on the same device and inode. Same-inode and same-length confirmation does not perform that byte confirmation. This is a mismatch in J4a's assigned shared primitive even though J4b and J4d own its later production callers.

Evidence: [complete_private_suffix](product/crates/security/src/private_access.rs), lines 869–888; [verify_written](product/crates/platform/src/filesystem/file_effects.rs), lines 319–353; [J-RW r4 item 3.2](pins/docs/implementation/m3/resume-repair-jrw/PROPOSAL-r4.md), line 247. The existing byte/end verification completes at platform line 352, before the file barrier at line 353. After the directory barrier, security lines 878–884 observe only metadata. No final byte read follows.

After the file and parent directory barriers, perform the law's capped read-back and exact byte/end comparison through the confirmed same object. Reserve all work for that confirmation before the first effect and keep the fresh write_new_regular path's behavior unchanged. The existing early write verification may remain, but cannot replace this final check. Add a focused regression that establishes byte verification after both barriers and refuses a mismatch or failed final read; update the exact-reservation and one-edge-short C-SUFFIX cases so all final confirmation work is covered before mutation.

Static call order in the exact pinned subject; existing C-SUFFIX tests check final content, prefix/inode preservation and budget refusal, but do not establish the required post-barrier byte observation. No concurrency or power-loss counterexample is claimed. Both independently rerun lanes passed; those passes do not close this finding.

**Answers to the ten judgment calls**

| Call | Decision | Reason |
|---|---|---|
| 1 | ACCEPT | RW-P2's no-WAL clause and result belong in project_ledger.rs. Honor S1: X3c-3 integrates first; no new inventory file is needed. |
| 2 | ACCEPT | The four innermost repair component names distinguish completion from ordinary creation and fit item 10's examples. Accept x3c.ledger-create.projects.repair, x3c.ledger-create.namespace.repair, x3c.object.objects.repair and x3c.object.sha256.repair. X9 r17 section RW must record these exact names. |
| 3 | ACCEPT | The ACL-omitted zero-length file with a WAL is outside RW-P2 and keeps Custody("private") before any append. N-P2's LEDGER.CORRUPT applies to the already-private zero-length file with a WAL that the unchanged existing test admits through open_store_file. |
| 4 | ACCEPT-WITH-REQUIRED-CORRECTION | C-ACL uses exactly the fresh step's sample/append/resample reservation; the owner's remaining steps retain their existing charging. C-SUFFIX reserves all operations it currently performs, but RF-01's required final read must also be included in that reservation. |
| 5 | ACCEPT | Completion is returned through directory dispositions, StoreFileAdmission/AdmittedLedger and FloorStep/OperationFloor, with the closed kind/state table. Further joining is J4e's; O1 has not landed, so no event or new dependency is required here. |
| 6 | ACCEPT | Unproved extra P-ACL clauses and owner clauses keep the original omitted-ACL custody refusal; budget failures remain budget failures. Ordinary private and non-omission refusals use the ordinary first sample. |
| 7 | ACCEPT | RW-P3 runs after busy probing and carrier classification, before floor observation, and confirms exact name/filesystem and both directory barriers within x3b.floor.directory.repair. Failure retains the host I/O row. |
| 8 | REQUIRED-FINDING | A pre-barrier byte read followed by post-barrier inode/length checks omits the post-barrier byte read-back required by item 3.2. See J4A-RF-01. J4a owns this shared primitive even before it has a production caller. |
| 9 | ACCEPT | Honor S2: integration is held until X9 r17 section RW is accepted, then includes exactly the six RW-F00 storage row re-transcriptions and a full storage lead set in the same commit. No run set is part of this code review. |
| 10 | ACCEPT | For RW-P2 repair wraps the C-ACL create/admit completion; that step has no durability point. The pre-existing resumable-empty WAL/DDL/barrier/verification path follows under its existing names. RW-K5's repair kill set is therefore empty, and section RW must record it; expanding the repair scope into that existing path is not required. |

**Assigned controls and owner boundaries**

No further required finding in P-ACL/C-ACL or RW-P1, RW-P2 and RW-P3. Only NotReturned qualifies, other clauses precede mutation, the fresh zero-rights owner allow is reused, inode/mode/bytes are preserved, and read admissions remain effect-free.

The omitted candidate is checked for fixed name/filesystem, owner, exact mode, kind/link count, and bounded directory emptiness or zero length before mutation. C-ACL uses the fresh sample/append/resample step. RW-P1/RW-P2 retain the namespace writer lease boundary; RW-P3 retains the fence boundary and LD11-1 ordering. Failed extra native observations leave a clause unproven and retain the omitted-ACL refusal; a budget failure retains its budget row. Read-only admissions are unchanged.

P-PREFIX and positioned suffix-only writing are implemented, including empty strict prefixes, ACL completion when omitted, exact early verification and whole-operation reservation. Final confirmation order requires RF-01.

The current three C-ACL production call sites and their remaining barriers are enclosed in repair scopes. The source pin is adequate for J4a together with the unchanged lawful-first-commit census pins. J4's completion-driver census and release absence remain J4e's.

All 22 new tests are additive. They cover RW-C1, C2, C3, C6, C7, C10 and C12 at the assigned primitive/owner seams, subject to RF-01's final-confirmation regression. End-to-end Committed cells remain RW-F00 evidence. Platform adds 1 test, security 18, storage 3. [New test names](new-test-names.json), [unchanged existing test verification](existing-tests-verification.json).

**Independent validation**

| Lane | Passed | Failed | Ignored | Result |
|---|---:|---:|---:|---|
| `cargo test -p opensip-platform -p opensip-security -p opensip-storage --lib --locked --offline --no-fail-fast` | 1400 | 0 | 3 | [log](lanes/libs.log), [exit/time](lanes/libs.result) |
| `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast --locked --offline` | 1658 | 0 | 3 | [log](lanes/feature.log), [exit/time](lanes/feature.result) |

Each lane independently passed all 22 new tests. The feature lane also passed the unchanged security/storage census pins, feature-site allowlist pin and no-manifest-enable pin. Every Cargo invocation used nice -n 19, --locked --offline, a private 0700 Darwin-user TMPDIR, isolated HOME/CARGO_HOME and a target directory under this output directory. Each waited for the lane lock, acquired it by mkdir, and released only its owned lock immediately after Cargo finished. [Validation details](validation.json).

Pinned lead results report the workspace, doc, fmt, build, clippy, drift/design/policy lanes; those broader lanes were inspected as evidence, not independently rerun. No crash-matrix run set ran.

**Lead rulings and integration**

S1 accepts the file overlap and requires X3c-3 first. S2 holds J4a product integration until accepted X9 r17 §RW, then requires the six RW-F00 re-transcriptions and full storage lead set in the same integration commit. This review judges the code; it does not judge those six rows. S5 owes RW-K5’s empty set to §RW. S6 owes the three descriptions to the next description batch. S8 is met by releasing only an acquired lane lock.

- X3c-3 integrates first.
- Hold J4a integration until accepted X9 r17 section RW.
- Integrate with exactly the six RW-F00 storage row re-transcriptions and a full storage lead set in the same commit.
- Section RW records the exact repair scope names and RW-K5's empty kill set.
- Record the three stale descriptions in the next description batch.
- After correction and acceptance, rebase onto the integration base; this verdict binds only the supplied diff.

No file added, removed or renamed; no inventory successor, manifest assessment or inventoryCandidateAssessment is required. S6's three descriptions remain owed to the next description batch.

The stated binding-only main movement is integration context; Git was used only in the named worktree. No repository edit, commit, push or delegation was performed. The real OpenSIP home and private 413 UUID fixture were not accessed. Review artifacts are under the requested output directory. This review does not qualify Linux or power-loss variants.
