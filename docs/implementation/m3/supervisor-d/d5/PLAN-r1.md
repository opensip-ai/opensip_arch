# D5 implementation plan r1: the DR-G21 controls, the fake providers and the escape controls (M3-D r5 items 18 and 27; F-7)

**Lead plan, 2026-10-17. Proposed; it needs Codex review (round 1).**

**Bases:**
- product main `7a4be0b` (D2b-3b's TS2 participant integrated at `f16f50d`; inventory v231 bound; D4-1 integrated at `114d2ac`; D3a-3 integrated at `2fbb779`);
- D3a-4 r2, accepted by Codex (`codex-d3a-4-r2`, ACCEPT-UNIT), whose integration is in progress;
- architecture `cc96a357`, and the files the subject manifest names.

Product lines are cited at `7a4be0b`. Pinned sources are given with the first 12 hex digits of their SHA-256:

| Short name | File | SHA-256 | Standing |
| --- | --- | --- | --- |
| **MD** | `supervisor-d/PROPOSAL-r5.md` | `224b9228e9d7` | M3-D r5, accepted by Grok; the authority the O7 record pins |
| **D3BP** | `supervisor-d/d3b/PLAN-r3.md` | `d67c5af02336` | Codex ACCEPT (`codex-d3b-plan-r3`) |
| **D4P** | `supervisor-d/d4/PLAN-r2.md` | `fddf67e55305` | Codex ACCEPT (`codex-d4-plan-r2`) |
| **OPP** | `operability/PLAN.md` | `4eca344b0c6a` | r3 accepted; a live file, unchanged since 2026-10-02 |
| **SOP2** | `operability/s-op-2/PROPOSAL-r6.md` | `ce8d3a4b7833` | Codex ACCEPT-DESIGN-UNIT |
| **HD** | `harness/DESIGN.md` | `1f1083993dce` | Q0 r13 accepted; a live file, unchanged since 2026-10-03 |
| **QG** | `docs/coop/design-corrections/qualification-gates.applied.v1.json` | `33b8d13c63b4` | applied |
| **M3P** | `M3-PLAN-r6.md` | `a6956e88c94f` | the accepted r6 bytes MD cites |
| **O7** | `owner-decisions/2026-10-09/O7-OWNER-DECISION-2026-10-09.json` | `625caf46fcbe` | the owner adopted the existing proposal; `cf1Accepted` and `d1bImplemented` are false |
| **CFP** | `confinement-cf/CF-P-RECORD.md` | `6323a1b4df5a` | a record, not law |
| **D3A3-CO** | `supervisor-d/d3a-3-r2/carried-obligations.json` | `d97b553e4827` | accepted with D3a-3 r2 |

## 0. What D5 delivers, and what it does not

**What precedes it.** MD's units table gives D5 as "items 18's and 27's controls, the fake TS2 and Rust3 providers, and the G21 specification rows; F-7 after CF-1", depending on "D3b, D4; CF-1 for F-7", size L (harness), control "DR-G21 controls (S-OP-11)" (MD:1263). The gates are "D5's escape controls wait for CF-1" (MD:1250) and the order "D3b ∥ D4 → D5" (MD:1265). Earlier units placed three things on D5:
- **D3b:** "D3b runs item 18's D5-T1 to D5-T5 scenarios, item 19's D3-T17 to D3-T21 and D3-T9 against its fixture child and fixture participant, as fixture-scoped unit controls. D5 re-runs them with the real codecs and records the G21 rows (item 27). D5-C5 (a terminal `SIGINT`) and D5-T8 (under the harness, Linux, with K1c) are D5's" (D3BP:67).
- **D3a:** each D3a SCOPE says "D5 re-runs them with D2b-3's and D2b-4's codecs". D3A3-CO's `D3A3-D5-codecs-and-timing` asks D5 to "re-run the gate, records and D3a-1/D3a-2 controls with D2b-3's and D2b-4's codecs; and widen or justify the tests' shortened 2 s handshake, which missed under the lane's parallel load at base".
- **O7 and S-OP-11:** F-7's three escape controls, which M3P says "extend OPP §10, which does not contain them" (M3P:509), plus MD's E-PROC and E-TREE (MD:1080-1094).

**Delivers:**
- **Item 27's control set** (MD:882-918):
  - G21's required evidence (QG:428), each a named group;
  - G21's corpus (REG:366);
  - OPP §10's areas as they touch supervision (OPP:422-437);
  - CPC's hostile dual-channel classes as D5-C1 (MD:415, CPC:496-517);
  - the harness specification `tests/qualification/README.md`'s G21 section (COV:4964).
- **Item 18's controls** with the real codecs: D5-T1 to D5-T5, D5-T2b and D5-T2c (MD:619-625).
- **The structural controls** D5-S1 to D5-S3 (MD:202, :222, :239), D5-C5 (MD:262), D5-T6 (MD:679) and D5-T7 (MD:703).
- **The first-party fake TS2 and Rust3 providers** (MD:884), which S-OP-2's C-12 also uses (SOP2:949).
- **The codec re-run and the handshake margin** (D3A3-CO).
- **F-7's escape controls**, E-NET, E-WRITE, E-ENV, E-PROC and E-TREE, once CF-1 allows (MD:1080-1094).

**Not delivered:**
- **Qualification.** Every control is "authored at M3, qualified at M6" (MD:912). QG:432 stands ("REQUIRED PRODUCT QUALIFICATION UNPERFORMED").
- **Linux.** Every Linux row is "not run" on this host (MD:345-347). Linux rows land as **D5-L**, after D1a-L and D3b-L, on a Linux lane (§1).
- **Any confinement claim.** F-7's outcomes feed CF-1's enforcement matrix (MD:1093). D5 claims nothing as enforced (MD F-8).
- **The public projections and the emitted records.** Item 22's Coverage, D9, UI and exit goldens are host workflow tests (MD:1286, COV:7284-7289), owned by J. D5's G21 table cites them. S-OP-2's sink-level canary checks (C-4) need J2b's emission (LD-D3A3-1). D5 owns their supervision half: stderr, `fault` detail and environment never reach a record (§5).
- **E's syntax-pass controls** (E2-T5, E2-T23). They are E's units; D5 lists the syntax pass as a G21 subject and cites them (MD:909).
- **The Rust3 participant.** That is D2b-4b's (D2b PLAN-r3-A2). D5's Rust3 rows wait for it.

## 1. The split (LD-D5-1): seven sub-units, each its own review and lane

| Sub-unit | Content | Controls | Depends on |
| --- | --- | --- | --- |
| **D5-0** | The margin and the structure:<br>• LD-D5-4's waits rule in `supervisor_tests.rs`: release waits except the one a control exercises;<br>• D5-S1 to D5-S3 as workspace-wide structural checks extending the existing censuses (LD-D5-6) | D5-S1, D5-S2, D5-S3; the margin evidence (LD-D5-4) | D3a-4 integrated (it edits the same test file) |
| **D5-1** | The **fake TS2 provider**, a `TestFixture` binary (LD-D5-3); its frame corpus as test-support source shared with D2b-3a's in-process worker; the fake's own replay check; the **TS2 codec re-run** of D3a's controls through `Ts2Participant` (LD-D5-5); S-OP-2 C-12's TS2 half at the fact level | the re-run table (§5); the fake self-check; C-12 (TS2) | D5-0; D2b-3b (met) |
| **D5-2** | The **fake Rust3 provider**, the same way, and the **Rust3 codec re-run** | the re-run table (Rust3); C-12 (Rust3) | D5-1; **D2b-4b** (the Rust3 participant) |
| **D5-3** | **Kill, reap, cleanup and cancellation** through the real codecs:<br>• item 18's D5-T1 to T5, T2b and T2c;<br>• item 19's D3-T17 to D3-T21, D3-T20b and D3-T9;<br>• D5-C5;<br>• G21's "recovery" (LD-D5-8);<br>• D5-C1, CPC's dual-channel classes 0 to 10 | as listed | D5-1; **D3b-1, D3b-2**; D5-2 for the Rust3 rows |
| **D5-4** | **The G21 specification:**<br>• `tests/qualification/README.md`'s G21 section, with DR-G29's section citing D4's controls;<br>• the machine-checked coverage table (LD-D5-7);<br>• D5-T6 (sealed-evidence preservation) and D5-T7 (correlation);<br>• the supervision halves of OPP §10's privacy, custody, bounds and overhead rows | the coverage check and its pinned-source equality; D5-T6; D5-T7; §5's OPP rows | D5-1, D5-3; **D4** (D4-1 to D4-4 accepted, so the G29 rows name real controls) |
| **D5-5** | **F-7's escape controls**, E-NET, E-WRITE, E-ENV, E-PROC and E-TREE, under the launcher's provider and tool profiles, each outcome fed to CF-1's matrix (LD-D5-9) | F-7's table | **D1b integrated; CF-1 accepted**; O7 (met, 2026-10-09) |
| **D5-L** | The Linux rows: item 18's Linux outcomes, F-7 on Ubuntu 24.04 and AL2023, and **D5-T8** jointly with K1c under the harness (HD:909-910) | as listed | D1a-L, D3b-L, the K1c lane; D5-5 for F-7 |

**Order:**
- D5-0 first. D5-1 follows it.
- D5-2 when D2b-4b is on main. D5-3 when D3b-1 and D3b-2 are.
- D5-4 after D5-1, D5-3 and D4's four sub-units. Its Rust3 cells fill in when D5-2 lands.
- D5-5 when D1b and CF-1 allow.
- D5-L on the Linux lane.

**D's completion is claimed only with D5** (D3BP:418): with D5-0 to D5-4 on macOS, D5-5 once CF-1 allows, and D5-L's rows reported as run or as "not run".

**What is gated on what, today:**
- **D3b:** D3b-0 is in review (`codex-d3b-0-r1`, round 2 packaged). D3b-1 and D3b-2 are not started. They gate D5-3, and so D5-4's kill and cancellation cells.
- **D4:** D4-1 is integrated. D4-2 is in review. D4-3 and D4-4 are not started, and D4-4 waits for CI-A3 (D4P §1). D4 gates only D5-4, whose DR-G29 section names D4's controls. No D5 control runs a D4 path.
- **CF-1:** not accepted, and D1b is not implemented (O7: `cf1Accepted` and `d1bImplemented` false). They gate D5-5 alone. O7 itself is met: section F is binding (O7 `sectionFSelectedAsRecommended`).
- **D2b-4b:** not on main. It gates D5-2 and every Rust3 cell.

## 2. Lead decisions

- **LD-D5-1. The split** (§1). Each sub-unit has its own scope record, lane and review, as D3a's, D3b's and D4's do.
- **LD-D5-2. macOS first; Linux as D5-L.** D1a, D3a and D3b implement only this host's macOS family (D3BP LD-D3B-2). Item 8 runs and claims only that family at M3 (MD:345). A Linux row is "not run" until a Linux lane runs it (MD:347), never "passed by not running" (MD:917). Rows where macOS's stated limits are the expected outcome report them as such (MD:911, item 18).
- **LD-D5-3. The fake providers are first-party test binaries over shared lawful frames.**
  - **The binaries.** Each fake is a `[[test]]` with `harness = false` in `crates/components` (`tests/fake_ts2.rs`, then `tests/fake_rust3.rs`), like `supervisor_fixture` (`crates/components/Cargo.toml`:36-39). It is launched only through `LaunchSpec::fixture` under the `test-fixture` feature (MD:189). Its script is a closed name in argv, as the fixture's is. It never reads repository bytes (MD:884).
  - **The frames.** The fake answers each host frame with **D2b-3a's lawful worker frames**: the ones `ts2_send_tests.rs`'s in-process `Worker` already uses (`ts2_send_tests.rs`:1046-1075). D5-1 moves those builders into one test-support source file that both the unit tests and the fake include (`#[path]`). There is no new crate, feature or dependency. So the fake and D2b-3b's own controls agree by construction on what a lawful frame is, and that agreement has already been reviewed with D2b-3a and D2b-3b.
  - **Misbehaving on cue.** The scripts add exactly the G21 corpus's faults (REG:366):
    - crash, panic, abort and `SIGSEGV` at each phase;
    - a timeout (silence) at each wait;
    - resource growth;
    - a malformed, truncated or duplicate frame;
    - EOF;
    - a forked tree;
    - a frame split at every byte offset of its length prefix, and 1-byte chunks (MD:415).
  - **The fake's self-check.** Before any supervision row uses a script, a unit control replays the script's frames through D2b-3a's receiver alone, with no supervisor and no process. It asserts that every lawful frame is admitted and every fault frame refused, with its expected class. A supervision failure then cannot be a fake defect.
  - **Rejected:**
    - **Real providers** at M3 (MD:915);
    - **in-process "children"** (MD:916);
    - **a fake that writes its own encoder.** It would duplicate D2b-1's encoder and test only its own agreement with it.
- **LD-D5-4. The handshake margin: release waits, except the one under test.**
  - **The evidence.** Every control in `supervisor_tests.rs` runs with `quick()`'s shortened waits: a 2 s handshake and a 4 s wall clock (`supervisor_tests.rs`:420-431 in D3a-4 r2; `:408-419` at `7a4be0b`). The release handshake is 30 s (`supervisor.rs`:63; item 14).
    - Under the lanes' parallel load, the base's supervisor tests failed `HandshakeDeadline`:
      - 9 to 12 times in D3a-3's lanes;
      - 22 in D3a-4 r1;
      - 21 in D3a-4 r2's second attempt.
    - Each failed test passed 6 of 6 alone (D3a-4 r2 SCOPE, Checks).
    - Run serially, the same base passed 66 of 66 (`supervisor-serial.json`, at `f31206e` and at `7a4be0b`).
    - D3a-4 r2's lane of record had no parallel failures at all.

    The failures are therefore load timing on a 2 s budget, not a defect.
  - **The rule.**
    - `quick()` becomes `Waits::RELEASE` (item 14's constants, MD:479-508).
    - Each control shortens **only the waits it exercises**, through a named helper per wait, and states which wait in its doc comment. For example, `silent-handshake` keeps a 2 s handshake because it waits for that expiry, and a deadline control keeps a short wall clock.
    - No new duration is invented: every other wait is the law's own.
  - **Cost.** A broken test can wait up to its release bound (30 s for a handshake) rather than 2 s, under its existing 20 s outcome cap. The cap is raised to the largest release wait the control leaves unshortened, plus the drain and reap ceilings (item 14). That cap is the law's sum, not a new figure.
  - **Evidence for the review.** D5-0's lane runs the full parallel components suite **three times** on the candidate and records each failure set. The pass rule is no `HandshakeDeadline` in any of them. The base's counts are recorded beside them.
  - **Rejected:**
    - **Serializing the supervisor tests.** It hides the margin instead of fixing it, and every other parallel lane would still fail.
    - **A wider shortened handshake** (for example 10 s). That is an invented constant with no law line.
- **LD-D5-5. The codec re-run is a table over participants, not a copy of the tests.**
  - **The mechanism.** D3a's controls drive `Supervision<FixtureParticipant>` (`supervisor_tests.rs`:75-330). D5-1 parameterises the controls whose assertions do not depend on the fixture double's type-only frames over a participant **kind**: the fixture (kept unchanged) and `Ts2Participant` with the fake TS2. D5-2 adds Rust3. Each re-run row names its original test, so a fixture-only row and its codec row can be compared.
  - **Rows that do not re-run are listed with the reason.** For example, the fixture double's fixed `Unavailable` reason (D3a-4 LD-D3A4-2) becomes the payload's own admitted reason under the codec, which is a stronger assertion. Seams on `Supervision` (`Seams`, `supervisor_tests.rs`:27-70) apply to every participant.
  - **The rows:**
    - D3a-1: the joins, D3-T1's triggers, D3-T2, D3-T3 and the waits;
    - D3a-2: item 16 and the tool class, where a tool has no participant and runs once;
    - D3a-3: discard, release, records and the owner route;
    - D3a-4: the stage records. Under the codec the participant pushes `Boundary::Phase`, `AnalyzeSent` and `Unavailable` itself. That is D2b-3b's carried obligation `D3A4-participant-boundaries`, and D5-1 checks it is met before its stage rows run.
- **LD-D5-6. The structural checks extend the existing censuses; there is no new checker.**
  - **D5-S1.** No production `Command::new` or `posix_spawn` outside `platform/process.rs` (MD:202). This extends `tools/check_operability.py`'s `process` class (`:30-33`) with `libc::posix_spawn(`, `posix_spawn_file_actions_` and `fork(`, owner `platform`.
  - **D5-S2.** No `posix_spawnp` or `exec*p` anywhere in production code (MD:222). That is `process_rs_spawns_by_path_only` (`process_tests.rs`:743-760) widened from one file to the workspace.
  - **D5-S3.** No `std::env::var*` outside the resolver and platform owners (MD:239, OPP:367). This extends `tools/tests/test_environment_exceptions.py`'s crate list (`:18`, today `crates/host` and `crates/security`) to every workspace crate, with the current exceptions held exactly.
  - **Why.** Each class already has an owner tool and exception file. A second checker would let the two disagree.
  - **Negative controls:** each check gets a planted copy in a temporary tree, as the existing tests do (`test_environment_exceptions.py`:1-8).
- **LD-D5-7. The G21 coverage table is data, checked mechanically against its pinned sources.**
  - **The data.** `tests/qualification/g21-controls.v1.json` maps each of:
    - QG:428's six required-evidence groups;
    - REG:366's ten corpus classes;
    - OPP §10's ten areas (OPP:426-437);
    - MD item 27's other rows (CPC classes, the syntax pass, the escape controls)

    to named controls: a test path and function, with its sub-unit and platform. A row whose control is another unit's (J's goldens, E's syntax controls, D4's G29 rows) names that unit and its control id, and is marked `cited`.
  - **The check** (a Python test, in the repository's tools tests):
    - **Requirements:** the requirement lists equal their pinned sources member for member and in order. QG:428's `requiredEvidence` is split on its commas; REG:366's corpus on its slashes; OPP §10's area column is read as written.
    - **Controls:** every `owned` control resolves to an existing `#[test] fn` at the named path.
    - **Coverage:** every requirement has at least one control.

    It never trusts a handwritten list (checklist item 4).
  - **Why.** MD:918 asks the lead to keep this as "a table in D5's review". A checked table cannot drift from QG, REG and OPP, or from the tests.
- **LD-D5-8. Recovery is a fresh attempt, never a restart.** G21's "recovery" (REG:366) is controlled as two supervisions in sequence over one script that faults the first time. The second gets a new process id, a new scratch directory and new spool state, and the first's settlement is unchanged (ML item 2; MD:896). No supervision restarts a child.
- **LD-D5-9. The escape controls' outcome rule** (MD:1093).
  - **Where outcomes go.** Each F-7 case's pass or fail is written to the lane's evidence as a CF-1 matrix input. A failing case moves that platform's cell to `DISCLOSURE-ONLY`. It is never hidden, retried into a pass or worked around in the test.
  - **What counts as a denial.** Each attempt records the call's name and `errno`, cleared before the call. Only the platform's denial class counts as denied: `EPERM` or `EACCES`, or the sandbox's stated equivalent per CFP. A failure for any other reason (`ENOENT`, `EINVAL`, a missing listener) **fails the case**, because nothing was shown denied (checklist item 3).
  - **Canaries.** They are synthetic and test-created. The real home and real credentials are never touched (MD:1082).
- **LD-D5-10. Where the lanes run.** D5's lanes take the one lane lock, as every lane does, so they never run concurrently with a crash-matrix lead set (MD:911; M3P:421).

## 3. Bounds and charging (summary)

D5 adds test code, test binaries, data and structural checks. No production path gains work, so no ledger, charge or bound changes. The fakes' resource-growth scripts exercise item 16's existing bounds. D3a-2's controls already measure them, and D5 re-runs them (LD-D5-5).

## 4. Cross-law items

- **X-D5-1 (S-OP-11).** The three escape controls extend OPP §10, which does not contain them (M3P:509). OPP §10's table should gain an "Escape (O7)" row naming E-NET, E-WRITE and E-ENV, with D5-5 as their controls. That edit is S-OP-11's owner's (OPP:418). D5-4's coverage table holds the row meanwhile, marked `extends-OPP-10`.
- **X-D5-2 (CF-1).** D5-5's outcomes are CF-1's matrix inputs (MD:1093). CF-1 owns the matrix's format; D5-5 writes only the per-case results.
- **X-D5-3 (J2b).** S-OP-2 C-4's sink-level canary checks need J2b's emission. D5-4 delivers the supervision half: no canary reaches a `RecordFact`. The sink half is J2b's.
- **X-D5-4 (K1c, HD:909-910).** D5-T8 is joint with K1c and Linux-only. It is D5-L's.
- **X-D5-5 (E).** The syntax pass is listed as a G21 subject. E2-T5 and E2-T23 are cited (MD:909).
- **X-D5-6 (D2b-3b, D2b-4b).** The participants' stage boundaries (`D3A4-participant-boundaries`) must be met before D5-1's and D5-2's stage rows run (LD-D5-5).

## 5. Controls and mutations (each sub-unit's lane)

Every mutation must fail its focused tests **at run time**. The lane runner does not count a compile failure as caught (D3a-4 r1, Checks). Each lane also runs the full suites at base and candidate, Clippy, rustfmt, the workspace check, the censuses, the closure check and verify_design, as D3a's lanes do.

- **D5-0:**
  - **Controls:**
    - D5-S1, D5-S2 and D5-S3 with planted negatives;
    - the waits rule. Each shortened wait is named by its control, and a structural test asserts that `quick()` equals `Waits::RELEASE`;
    - three parallel candidate runs with no `HandshakeDeadline`.
  - **Mutations:**
    - a planted `Command::new` in `crates/components`;
    - a planted `posix_spawnp` in `crates/host`;
    - a planted `env::var` in `crates/components`;
    - `quick()`'s handshake set back to 2 s. The structural test catches it. The parallel runs are evidence, not the catch.
- **D5-1:**
  - **Controls:**
    - the fake's self-check (LD-D5-3);
    - the TS2 re-run table (LD-D5-5);
    - C-12 (TS2) at the fact level: a registered and an unregistered `detailCode`, health, nonces, refusals, asserted resources that never become progress, and `max_rss_bytes` with its conversion (SOP2:949).
  - **Mutations:**
    - a participant `HostFault` mapped to `Fault`;
    - a discard skipped on a non-clean settlement;
    - a split-prefix frame admitted early;
    - the fake answering one host frame with an unlawful frame, which its self-check must refuse.
- **D5-2:** as D5-1, for Rust3.
- **D5-3:**
  - **Controls:** D5-T1 to T5, T2b and T2c with their item 18 outcomes on macOS, as D3BP:312-322 states them, and the test's out-of-band checks; D3-T17 to D3-T21, D3-T20b and D3-T9; D5-C5; recovery (LD-D5-8); D5-C1's classes 0 to 10, with the provider byte stream compared byte for byte (MD:415).
  - **Mutations:**
    - the identity check skipped before a by-pid kill;
    - a second `SIGKILL` after the root's reap;
    - stage 1 skipped;
    - a recovery attempt reusing the first scratch;
    - a control frame reordered against a split provider frame.
- **D5-4:**
  - **Controls:**
    - the coverage check (LD-D5-7);
    - **D5-T6:** a test store tree's bytes and metadata are identical before and after every G21 case, and no child receives its path;
    - **D5-T7:** no RequestId, RunId or log path in any child's environment or argv, observed by the fake reporting its own environment (OPP:429-430);
    - the supervision halves of OPP §10:
      - **privacy:** canaries in stderr, `fault` detail and environment never reach a `RecordFact`;
      - **bounds:** the 10× stderr flood;
      - **overhead:** the same scripts' facts are identical at supervision concurrency 1 and at several concurrent supervisions (OPP:437).
  - **Mutations:**
    - **in the data:** a QG requirement substituted at the same cardinality, and a requirement added to the pinned QG copy the check reads, each caught by the check;
    - **in the code:**
      - a coverage row pointing at a renamed test;
      - a canary passed into a fact;
      - a child environment given a RunId.
- **D5-5:**
  - **Controls:** F-7's five cases on macOS with the signed launcher (MD:1084-1090).
  - **Mutations:**
    - the profile's network deny removed;
    - the `kern.procargs` rule removed (CFP:185-187);
    - the scratch write rule widened;
    - an attempt whose failure is `ENOENT` counted as denied (LD-D5-9);
    - a case that skips without running, caught by the runner's executed-case count.

## 6. Inventory

The new paths are listed below. Each sub-unit carries its own inventory successor, numbered by the lead at launch after `git ls-files` (MD:1251).
- `crates/components/tests/fake_ts2.rs` and `fake_rust3.rs`;
- the shared frame-builder source (D5-1);
- `tests/qualification/README.md` and `g21-controls.v1.json` (D5-4);
- `crates/components/tests/escape.rs` and its escapee binary (D5-5).

The `Cargo.toml` `[[test]]` entries change no dependency.

## 7. Not claimed

- No qualification (QG:432). No confinement claim (MD F-8). No Linux row as run (LD-D5-2). No codec conformance beyond the re-run's assertions: D2b's controls own conformance. No real provider, and no repository bytes.
- **Untested here, and owned elsewhere:**
  - item 22's public goldens (J);
  - S-OP-2 C-4's sinks (J2b);
  - D5-T8 (D5-L with K1c);
  - E's syntax controls;
  - the Rust3 rows until D2b-4b.

## 8. Self-review (the lead's pre-submission checklist)

1. **Charge before work.** Not applicable: D5 adds no charged production work (§3). The re-run controls exercise existing charged paths unchanged.
2. **Exact charges vs bounds.** Not applicable, for the same reason.
3. **System-call error conventions.** This applies to D5-5's attempts and to D5-3's out-of-band checks. LD-D5-9: errno is cleared per call and recorded with the call's name, and only the denial class passes. A wrong-reason failure fails the case.
4. **Pinned-source equality.** LD-D5-7. The coverage table's requirement lists are compared member for member and in order with QG:428, REG:366 and OPP §10, and controlled by a same-cardinality substitution and a source-side addition (§5, D5-4).
5. **Immutable context pins.** The plan pins accepted bytes (MD, D3BP, D4P, SOP2, QG, M3P, O7, D3A3-CO). OPP and HD are live files, unchanged since 2026-10-02 and 2026-10-03. They are pinned at the hashes above and re-checked at each sub-unit's packaging.
6. **Time and measurement provenance.** LD-D5-4: no invented duration. Every wait is item 14's constant or the single shortened wait a control exercises, and the margin evidence is measured over three runs. Item 18's 1 s TERM-to-KILL (D5-T5) and the reap ceilings are the law's.
7. **Failure latching.** LD-D5-9: a failing escape case latches its platform's cell to `DISCLOSURE-ONLY`, never retried. LD-D5-8: a recovered attempt never alters the first settlement.
8. **Disclosure.** §0's "not delivered", §7's untested list, and each sub-unit's SCOPE will list its own.
9. **Mutations.** §5: every finding class above that applies has at least one runtime-caught mutation per sub-unit.

## 9. Questions for the reviewer

- **Q1.** Is LD-D5-3's shared frame source (D2b-3a's lawful worker frames, used by both the unit tests and the fakes) acceptable? The alternative is an independent frame corpus for the fakes. The shared source means the fakes test supervision and codec integration, not conformance; conformance stays D2b's.
- **Q2.** LD-D5-4 replaces the shortened 2 s handshake with release waits except the wait each control exercises. Is that the right answer to `D3A3-D5-codecs-and-timing`, or should D5 justify a shortened figure from a measured distribution instead?
- **Q3.** Is D4's gate on D5-4 alone (§1) the right reading of MD:1263's "D3b, D4"? No D5 control runs a D4 path; D4's controls are cited in the G29 section.
- **Q4.** LD-D5-6 extends the existing censuses rather than adding a supervision checker. Is widening `test_environment_exceptions.py` to every crate acceptable as D5-S3, given that it is M3-B's check?
- **Q5.** Should D5-5 wait for CF-1's acceptance, as MD:1250 says, or may it run on the D1b launcher as unclaimed evidence before CF-1, feeding CF-1's trials?
