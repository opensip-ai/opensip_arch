# GROK2 review: M3 unit plan r1 (fact validation)

Verdict: **REQUIRED-FINDINGS**.

Subject: `docs/implementation/m3/M3-PLAN.md`, 28398 bytes, sha256 `65bf6ac57a663707a2eea47fba7e293c595daa3ac9e703b1e4ed511d38496830`. Product HEAD `eb0d50398035fe3532dadc332f88cf1d8bc4cb69`. Read-only. No product build or test. `~/Library/Application Support/OpenSIP` was absent. The 413 fixture was not read.

The plan is a planning record. The build-plan M3 row, the seven M3 gates, the accepted quality-plan M3 row, and the product surprises the drafter lists are largely accurate. The operability line numbers are not the current operability plan, three M3 contract sections are not assigned to a unit, and two module-state or routing sentences point at the wrong text.

## Required findings

### RF-1. Operability citations do not land on the current operability plan

`M3-PLAN.md:32`, `:76`, `:82`, `:89`, `:161`, `:166-168`.

The quoted obligations exist in `docs/implementation/m3/operability/PLAN.md` (r2). The line numbers in the unit plan point at other paragraphs.

| Plan cite | What that line is | Where the claim is |
|---|---|---|
| OPP:333-334, the M3 item list | Cancellation phases B and C | OPP:378-379 |
| OPP:208-214, O1(a) | §3.4 sinks and custody | OPP:232-238 |
| OPP:363, the S-OP-4 record join | An enforcement bullet in §7 | The join sentence is OPP:238; the successor row is OPP:408 |
| OPP:124-135, RequestId and phase-lawful identities | The F1–F11 lesson list | OPP:145-155 |
| OPP:293-294, the two-stage cancellation join | The interrupt row and the host-panic row of the outcome matrix | The two-stage rule is OPP:327; the phase join, which is S-OP-12, starts at OPP:328 |
| OPP:247, supervision and candidate discard | The operational-record paragraph | Supervision is OPP:269-271. Candidate discard is F02:204, which the plan also cites, and OPP:289-290 |
| OPP:222-224, the operational record and INC-8 | The §3.5 heading and the configuration paragraph | OPP:244-248 |
| OPP:316-325, enforcement checks | §5.4 capacity preflight | OPP:361-371 |
| OPP:374-388, the G20/G21 controls | §8 milestones through the start of §9 | The control table starts at OPP:420. OPP:379 is the milestone sentence |
| OPP:335, `--timings` at M4 | Cancellation phase D | OPP:380 |
| OPP:360-370, the S-OP successor table | §7 enforcement checks | OPP:405-416 |
| OPP:123, one host-owned subscriber | The predecessor's two-stage note (K7) | OPP:145 |
| OPP:200, no environment filter | "Never blocks" / the loss marker | "No environment side channel" is OPP:224 |
| OPP:353, the O7 row | Doctor-bundle inputs | §5.6 is OPP:343-345; the decision row is OPP:398 |
| OPP:300, "needed before M3 providers ship" | The §5.3 panic heading | The sentence is OPP:345 |
| OPP:333, O7 before the protocol law | Cancellation phase B | OPP:378 |
| OPP:350, O4 | The §6 Support heading | O4 is OPP:251; the M5 milestone is OPP:381 |
| OPP:354, O9 | A doctor-bundle input bullet | OPP:399 |

Fix: retarget each citation to the row in the third column. Do not treat the current numbers as stable across an operability revision; M3-O already says it follows the accepted revision.

### RF-2. S-OP-12 is missing, and the O7 recommendation does not do what it says

`M3-PLAN.md:32`, `:76`, `:89`, `:166`.

OPP:379's M3 row depends on S-OP-12, and the "once accepted" list includes the cancellation latch join. OPP:415 blocks M3 cancellation on that successor. The unit plan's gated list is S-OP-1, S-OP-2, S-OP-5, S-OP-6, S-OP-7, S-OP-8 and S-OP-11. S-OP-12 does not appear. M3-L's "two-stage cancellation join" cites the wrong lines (RF-1) and does not name the successor.

The O7 paragraph says the lead recommendation is "as OPP proposes" and then says O7 does not block M3-L or the F/G units, only M3-X. OPP:345 says confinement is needed before M3 providers ship. OPP:378 places the O7 decision before the protocol law. Those are different blockers.

Fix: put S-OP-12 on the M3 cancellation unit that owns it, with OPP:327-338. State the O7 recommendation as a departure from OPP:345 and OPP:378, or keep O7 in front of the protocol law and the provider units, as OPP does.

### RF-3. BP:933-945 is the population census, not the M3 routing table

`M3-PLAN.md:15`.

The sentence says the listed populations are routed to M3 by the coverage owner, "generated table BP:933-945". That table is the generated census: commands 45, query operations 20, capability cells 66, gates 32, shared flags 7, renderers 5, workflow goldens 45, contract sections 55, fallow constraints 15, hydra proposals 8, report features 24. Every row's standing is "Ownership/verification routing; not executed". It has no milestone column.

The seven M3 gates are the individual rows BP:1014 (DR-G10), BP:1017 (DR-G13), BP:1018 (DR-G14), BP:1025 (DR-G21), BP:1027 (DR-G23), BP:1029 (DR-G25) and BP:1033 (DR-G29). BP:895 and BP:999-1000 do say gate execution stays at M6. BP:949-995 has no M3 command. Those later cites hold.

Fix: point the opening sentence at the coverage groups and at BP:999-1036. Leave BP:933-945 as the population census only.

### RF-4. Two coverage spans are the whole groups, and BP:1026 is not an M3 row

`M3-PLAN.md:19` and `:180`.

COV:6506-7849 is the entire `contractSections` array, 55 sections. Twelve of them are M3: `security-and-lifecycle:3` (6702), `native-evidence:2` (7066), `:3` (7093), `:4` (7118), `:5` (7144), `:7` (7193), `:9` (7245), `:10` (7270), `:11` (7294), `:14` (7366), `:15` (7390), and `workflows-and-surfaces:2` (7438). The count twelve is right. The span is not those twelve.

COV:7850-8166 is the entire `fallowConstraints` array, 15 constraints. The five named ids are M3, at FW-01 (7852), FW-03 (7894), FW-08 (7999), FW-13 (8104) and FW-14 (8125). The other ten are M5.

The risk bullet says M3 rows name `grants.rs`, `process.rs` and `installation.rs` as owners, citing COV:5266-5287, BP:1018 and BP:1026. `grants.rs` is an owner of four M3 flags (`--allow-backup-custody`, `--trust-group`, `--trust-project-owner`, `--yes-policy`). COV:5266-5287 is only the first of those flags; the other three grants lines are 5317, 5337 and 5377. BP:1018 is DR-G14, milestone M3, owner `crates/lifecycle/src/installation.rs`. BP:1026 is DR-G22, milestone M6, owner `crates/platform/src/process.rs`. No M3 coverage row names `process.rs`. D1's separate statement that `process.rs` is also the DR-G22 owner is accurate.

The other routing cites in that neighbourhood hold: COV:2077-4425 is all 66 cells (57 SUPPORTED-DESIGN, 6 UNSUPPORTED-TYPED, 3 NOT-SELECTED); COV:5266-5407 is all seven shared flags, all M3; COV:4671 is the TS major 2 / Rust major 3 method; COV:8963 is `discovery.rs` at M3; COV:8976 is `installation.rs` at M5; COV:5280, 7865 and 8138 name `discovery_tests.rs`, `workflow_tests.rs` and `tests/qualification/README.md`, and those paths are absent.

Fix: cite the twelve section objects and the five fallow objects. In the risk bullet, keep `grants.rs` and DR-G14, and say DR-G22 / `process.rs` is an M6 row whose module D1 builds early.

### RF-5. The TypeScript provider row says none of CH14:506-525 exist

`M3-PLAN.md:59`.

CH14:506-525 is the typescript-provider inventory from `package.json` through `tsconfig.json`. At `eb0d503` these three paths exist: `providers/typescript/package.json`, `providers/typescript/tsconfig.json`, and `providers/typescript/src/generated/protocol.ts`. The row already cites the package pins (`package.json:7` is Node 24.16.0, `:12` is TypeScript 6.0.3) and `protocol.ts:1` ("Inert types only"). The implementation sources in that span are absent: `src/analysis/*`, `compiler-adapter.ts`, `framework-recognition.ts`, `index.ts`, `program-factory.ts`, `protocol.ts`, `sealed-vfs.ts`, `session.ts`, and `program-factory.test.ts`.

Fix: say those implementation sources are absent, and that `package.json`, `tsconfig.json` and the generated protocol types are the stub that is present.

### RF-6. Three of the twelve M3 contract sections are not on a unit

`M3-PLAN.md:19` and the gates column of the unit table (`:78-91`).

The unit table names SL:3, NE:2, NE:9, NE:3, NE:4, NE:5, NE:14, NE:15 and WS:2. It does not name:

- `native-evidence:7`, "6. Clone equivalence modes" (NE:2562-2647). Coverage owners are `providers/rust/src/clones.rs`, `providers/typescript/src/analysis/clones.ts`, `crates/host/src/syntax.rs`, and the syntax grammar and candidate modules. F3 cites NE:2604 and G4 names `clones.rs`. §6.1–6.3 and §6.5 are not a unit deliverable.
- `native-evidence:10`, "9. Provider protocol successors (wire)" (NE:2781-3316). The coverage owner is `crates/components/src/provider_protocol.rs`. D2, F1 and G1 cite pieces of §9. The section id is not on a unit.
- `native-evidence:11`, "10. Deficiencies, precedence and D9 mapping" (NE:3317 onward). The coverage owner is `crates/host/src/outcomes.rs`. The section fixes the cause carrier per deficiency, the precedence order, and the bridge into the existing D9 codes. J2's phrase "D9 outcomes" does not state that obligation.

NE:2, "1. Supported native cells", is listed only on M3-B. Its coverage owners also include `crates/host/src/syntax.rs`, `crates/syntax/src/grammar.rs` and `crates/syntax/src/candidates.rs`, which are M3-E.

Fix: put NE:7 on E, F and G, NE:10 on D (with the frame work in F and G), and NE:11 on the unit that owns `outcomes.rs`, naming the deficiency-cause registry and the D9 bridge. Split NE:2 so E owns the syntax-only part.

## What held

Build-plan completion (BP:887) matches the plan's deliverable, owners and completion sentence, including CLI analysis at M4 (BP:888) and gate execution at M6 (BP:895, BP:999-1000). The seven gate names and milestones match BP:1014-1033. No command, query operation, renderer, workflow golden, hydra proposal or report feature is M3.

AQP:480-481 matches the plan's before-protocol and at-M3 lists. INC-1 through INC-8 are AQP:370-390. The D-table cites AQP:523-538 match those rows. The 66 = 11×6 split is 33 TS/JS cells, 22 Rust cells, 11 syntax-only cells and 6 `inventory/*` cells, and the 57/6/3 state counts match the coverage cells. Carrier frames are 26 Rust and 17 TypeScript in `schemas/wire/native-carriers-v1.json`. `git rev-list --count d4239a5..eb0d503` is 55. The critical path names 14 steps.

These surprises match the tree and the cited lines: absent `discovery.rs`, `snapshot.rs`, `plan.rs`, `analysis.rs`, `invocation.rs` and `syntax.rs`; `configuration.rs:1-4` and `fact_admission.rs:1-3`; `request.rs:15-19`; finalization present and unwired (`lib.rs:55-62`); `components` and `syntax` not workspace members (`Cargo.toml:3-4`); `grants.rs` absent; `macos_process.rs:1-2` and no `process.rs`; evaluator inspectors and `check_plan_pack` (`lib.rs:9-38`, `:111`, `:122`, `:127`); `pack-registry.json` `"rows": []`; Rust provider `main.rs` exits before a request; `rust-toolchain.toml` is 1.95.0 with only rustfmt and clippy; `installation.rs` absent and first milestone M5; no `tracing` package in `Cargo.lock`; no `std::panic::set_hook`; no `--timings`; default command refusal at `arguments.rs:104`; stderr lines at `bootstrap.rs:19`, `:44` and `:65`; `git_tracking.rs:5-6` is the single-layout / `vcs-unsupported` rule; REG:355 is the stale DR-G10 row and COV:4671 is TS2/Rust3. X11:18 and X11:64-77, X12:191-192, EXIT:61, EXIT:110, EXIT:169, EXIT:180 and EXIT:184-189 match the carry-ins. CH14:37, :41, :284, :288, :372-379, :475, :482, :485, :489, :495, :496 and :614 match the module table. BP:621-622, BP:676-694, BP:699-717, BP:957 and BP:992 match the lane, syntax, closure, import and `native-prepare` claims. The quoted NE paragraphs for families, grammars, contexts, DS-5/DS-6, prepared sets, L-RS1, the host-before-PlanId step, and "independent Claude review pending" (NE:4203) match.

O1(a), the syntax-backend trial, library-level import with the `import` command left at M5, imported prepared sets with `native-prepare` left at M5, the DR-G14 split, no public CLI at M3, no changed-scope ship at M3, `tracing` with one subscriber and no environment filter, macOS-only claims at M3, O4 at M5, and O9 not at M3 are consistent with the text those recommendations rely on. The line numbers for the operability ones are RF-1. O7 is RF-2.

## Non-blocking observations

1. `M3-PLAN.md:17` cites NE:590-601 for the 57/6/3 counts. That table is the capability × mode grid and does not state those integers. AQP:105 does, and it says the table omits the inventory row. NE:154-156 refuses a hand-written count. The coverage cells are the count that matches the plan.
2. `M3-PLAN.md:78` cites AQ:43-53 for `resolvedConfigDigest`. AQ:43-53 is the configuration-section list and does not contain that name. IE:518 defines the digest as the hash of that section's canonical semantic value. `configuration.rs:1-4` does use the name.
3. `M3-PLAN.md:36` lists five of the obligations inside X11:64-77. The same span also requires creator terminations (item 5) and the F0 binary restatement (item 8).
4. `M3-PLAN.md:76` cites F02:222 and F02:269 for one child and no reuse, which those sentences say. F02:220 still says TypeScript protocol major 1, and F02:259 still says Rust major 2. INC-5 and BP:717 are the TS2/Rust3 cites. The law should not copy the majors from those F02 paragraphs.
5. `M3-PLAN.md:58` says every identity domain, `snapshot2` through `run3`, at `descriptors.rs:483-555`. That span is the whole `IdentityDomain` impl. It also has `fact2` before `snapshot2`, and `cache2`, `regen2`, `policy-derivation3` and `subject3` after `run3`.
6. DR-G20's implementation milestone is M5 (BP:1024). M3-O authors its controls at M3, which is what OPP:379 and OPP:422 say (authored at M3, qualified at M6).
7. `providers/rust/Cargo.toml:1-2` is the workspace header. The 1.95.0 channel and the component list are `rust-toolchain.toml:2-4`. `rust-version = "1.95"` is Cargo.toml:8.
8. COV:4764-4771 contains DR-G14's id and `"milestone": "M3"` (4770). The owner path `installation.rs` is the next line, 4772.
