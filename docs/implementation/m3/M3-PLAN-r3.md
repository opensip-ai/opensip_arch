# M3 unit plan

Draft r3. Claude Opus 5.5, implementation lead. **Planning record: not law, not code, not a contract successor.** It is the M3 counterpart of [m2/EXIT-PLAN.md](../m2/EXIT-PLAN.md). It orders M3's obligations into reviewable units and changes no accepted contract, gate, threshold or register row. Product baseline: main `eb0d503` (X9-3 integrated). M2's tail (X9-4, X9-5, X9-6 exit gate, D3, licence unit) is still in flight, so no unit below touches product crates before X9-6.

r1 (`M3-PLAN-r1.md`, sha256 `65bf6ac5…`, 28,398 bytes) was reviewed by GROK2 (facts; `/tmp/opensip-implementation/reviews/grok2-m3-plan-r1/`, 6 required, 8 non-blocking) and CODEX2 (method; `…/codex2-m3-plan-r1/`, 5 required, 4 non-blocking). r2 answers all of them. r2 (`M3-PLAN-r2.md`, sha256 `add49e25…`, 35,300 bytes) was reviewed by GROK2 (`…/grok2-m3-plan-r2/`, 4 required, 6 non-blocking) and CODEX2 (`…/codex2-m3-plan-r2/`, 2 required, 3 non-blocking). r3 answers them.

Short names: **BP** `docs/v2/architecture/implementation-boundaries-and-build-plan.md`; **COV** `docs/v2/architecture/implementation-coverage.v1.json`; **CH14** `docs/v2/architecture/14-repository-and-module-layout.md`; **F02** `docs/v2/architecture/02-distribution-and-components.md`; **REG** `docs/v2/architecture/08-decision-and-readiness-register.md`; **NE / IE / AQ / WS / SL** `docs/v2/contracts/product-v1/{native-evidence,identity-and-evidence,admission-and-qualification,workflows-and-surfaces,security-and-lifecycle}.md`; **AQP** `docs/implementation/m3/analysis-quality/PLAN.md` (r4, accepted); **OPP** `docs/implementation/m3/operability/PLAN-r3.md` (r3, sha256 `b49035f2…`, accepted by Codex; the live `PLAN.md` carries the acceptance note). OPP is cited **by section**, so that a later revision doesn't silently move a citation; M3-O follows the accepted revision. **PTT** `docs/coop/artifacts/permission-truth-tables.v9.json`; **TES** `docs/coop/design-corrections/workflows/schemas/test-execution.schema.json`; **NEM** `docs/coop/design-corrections/native/native_evidence_model.v2.py`. **EXIT** `docs/implementation/m2/EXIT-PLAN.md`; **X11 / X12** `docs/implementation/m2/{cli-enablement-x11,policy-admission-x12}/PROPOSAL.md`. Product paths are under `opensip/`.

## r3 changes and review responses

| Finding | Change |
|---|---|
| GROK2 RF-1, CODEX2 C2-M3-R2-01 (the DAG and critical path) | **Missing edges added:**<br>- K1 → M3-M;<br>- CF-P → D-law acceptance;<br>- CF-1 → D5 and D's enforcement claim;<br>- D1's confinement primitive → every provider launch.<br>**Authoring and launch are separate.** G2 is authored before day 0. Its lawful launch, G2-v, runs after O7 and D1.<br>**Every M3-M and M3-X prerequisite has a duration or a finish bound,** with three exceptions: K2, R and O2. Those are unbounded until Q0 sizes K2 and their successors are accepted.<br>**26 days is now only the conditional host-chain duration.** The whole-M3 total is left uncomputed. |
| GROK2 RF-2 | M3-M cites AQP:236 only for too few findings. Closing an exploratory report with gating or repair-eligible adjudication still pending is **this plan's rule**. Any later Q2 use still needs AQP:228 and AQP:246. |
| GROK2 RF-3 | OPP §10 is cited for its ten areas. The three escape cases are new D5 and S-OP-11 controls. |
| GROK2 RF-4, CODEX2 C2-M3-R2-02 | A gated **M5 successor package, M5-EX**, must be accepted before M5's `execution.rs` claims any enforcement:<br>- the native §5.2 admission and disclosure join (NE:2440-2444, NE:2480-2487; NEM:2170-2182);<br>- the WS §7 test-execution schema join (WS:1071-1081; TES:7-14);<br>- a measured truth-table profile succeeding PTT.<br>Repository-code execution stays out of M3. The worker prohibition (NE:2534-2535) and the closed DR-128 untrusted-code scope (AQ:344; REG:317) are preserved. |
| GROK2 NBO-1..6 | Adopted:<br>- the citations are now `policy.rs:1087`, `policy.rs:1401`, X12:134, NE:2534-2535 and COV:4772 with 8976;<br>- the r2 response wording for S-OP-4 is clarified below: S-OP-4 is law content, not a gate item;<br>- CF's gates add G09 and G30 (AQ:344);<br>- launch rules have one owner, the D law, and M3-L cites it. |
| CODEX2 N01..N03 | Adopted:<br>- S-P and S-M state their launch boundary;<br>- the escape controls are labelled as an extension;<br>- the NE:2534-2535 span. |

## r2 changes and review responses

| Finding | Change |
|---|---|
| GROK2 RF-1 (OPP citations) | Every OPP citation is now a section of r3 (§3.1, §3.6, §4.1, §5.1, §5.5, §5.6, §7, §8, §9, §10). No OPP line number remains. |
| GROK2 RF-2 (S-OP-12; O7) | S-OP-12 (OPP §5.5, §9) is on M3-J, the unit that owns the commit-phase cancellation join, and is named in M3-L. O7 is now a hard prerequisite of M3-L and of provider launch, as OPP §8 and the coordinator direct. The lead's recommendation and the units it needs are in "O7". |
| GROK2 RF-3 (BP:933-945) | The routing sentence now cites the COV groups and BP:999-1036. BP:933-945 is cited only as the population census. |
| GROK2 RF-4 (spans; process.rs) | The twelve contract-section objects and the five Fallow objects are cited individually. The risk bullet names DR-G22/`process.rs` as an M6 row (BP:1026) whose module D1 builds early. All four `grants.rs` flag rows are cited. |
| GROK2 RF-5 (TS provider) | The row now says `package.json`, `tsconfig.json` and the generated types are present, and the implementation sources in CH14:507-517 and CH14:519-524 are absent. |
| GROK2 RF-6 (NE:7, :10, :11; NE:2) | NE:7 (clone equivalence) is on E, F and G. NE:10 (provider wire) is on D, with frame work in F and G. NE:11 (deficiencies and the D9 map) is on J2, the `outcomes.rs` work. NE:2 is split: B owns §1.4, and E owns the syntax-only part. |
| CODEX2 C2-M3-R1-01 | M3-L has an explicit **acceptance gate**. It covers complete T2 (with multi-repo and Python), Q0, D3, D13 and the D2 draft, S-OP-2 drafted, the S-OP-4 join, O1, O7 and the measured spike. Drafting stays parallel. |
| CODEX2 C2-M3-R1-02 | M3-S is split. **S-P** is a labelled feasibility probe with no Q6 claim. **S-M** is the measured INC-7 spike. S-M's report waits for the Q0 envelope and D13, and its Q6-labelled samples wait for D12. |
| CODEX2 C2-M3-R1-03 | New **M3-I1**: the X12c preview pack, meaning the rule-IR freeze, the contract successor, the bundled bytes and self-checks, and any conditional policy-language successor. It has no dependency on H. X12d moves into C4, and J2/J3 depend on I1 and X12d. The catalog stays separate as M3-I2. |
| CODEX2 C2-M3-R1-04 | O7 is held before M3-L, as above. |
| CODEX2 C2-M3-R1-05 | The critical path is recomputed from a sub-unit DAG with stated durations ("Critical path"). The determining branch is the host chain. The estimate is marked provisional. |
| GROK2 NBO-1..8 | Adopted:<br>- the counts cite COV and AQP:105;<br>- `resolvedConfigDigest` cites IE:518;<br>- J1 adds the creator terminations and the F0 restatement;<br>- the F02 major-1/2 text is flagged as stale;<br>- the identity-domain wording is corrected;<br>- DR-G20 is noted as M5 (BP:1024);<br>- the Rust pin cites `rust-toolchain.toml:2-4` and `Cargo.toml:8`;<br>- DR-G14 cites COV:4770-4772. |
| CODEX2 N01..N04 | Adopted:<br>- C3 and G4 name PO-1..PO-4 and the harness recipe for prepared sets;<br>- M3-M is not held for late adjudication;<br>- B names FW-14's outputs and preserves U-8 and U-9;<br>- the OPP references are refreshed to r3. |

## What M3 exit means

The build plan's milestone row (BP:887) defines M3:

- **Deliverable:** "M2 and provider build lanes; discovery/configuration, sealed snapshot/Plan, supervised TS/JS and Rust analysis and the guarded durable host pipeline".
- **Owners:** "Host discovery/snapshot/plan/analysis; components protocols; both providers and evaluator".
- **Completion:** "Selected native matrix/corpora, missing-role disclosures, cancellation, semantic admission and host-boundary durability checks; neither language silently dropped. Complete CLI analysis delivery follows at M4 with every advertised renderer".

**Routed to M3 by the coverage groups** (COV), with the gates in the qualification routing table (BP:999-1036). BP:933-945 is only the population census.

- **All 66 capability cells** (COV:2077-4425): 57 SUPPORTED-DESIGN, 6 UNSUPPORTED-TYPED and 3 NOT-SELECTED (AQP:105). That is 33 TS/JS, 22 Rust and 11 syntax-only cells.
- **Seven gates, to be prepared, not qualified:** DR-G10 (BP:1014), G13 (BP:1017), G14 (BP:1018), G21 (BP:1025), G23 (BP:1027), G25 (BP:1029) and G29 (BP:1033). Execution stays at M6 (BP:895, BP:999-1000).
- **All seven shared flags** (COV:5266-5407).
- **Twelve contract sections:**
  - security-and-lifecycle:3 (COV:6702);
  - native-evidence:2, :3, :4, :5, :7, :9, :10, :11, :14 and :15 (COV:7066, 7093, 7118, 7144, 7193, 7245, 7270, 7294, 7366, 7390);
  - workflows-and-surfaces:2 (COV:7438).
- **Five Fallow constraints:** FW-01 (COV:7852), FW-03 (7894), FW-08 (7999), FW-13 (8104) and FW-14 (8125).
- **No command.** Every analysis command is M4 or later (BP:949-995). Complete CLI delivery is M4 (BP:887-888).

**The accepted quality plan's M3 obligations.**

*Before the provider protocol is fixed* (AQP:480):
- INC-1 to INC-8 in the M3 law, plus the INC-7 spike;
- pinned T2 manifests, including the multi-repo approximation and Python;
- the harness design and the rule-catalog draft.

*At M3* (AQP:481):
- T1 for all 57 supported cells per mode, typed refusal for 6 and non-advertisement for 3;
- Q1 and Q4 on T1;
- draft catalog rules run non-authoritatively, for exploratory Q2–Q4 on T2;
- the determinism suite and exploratory Q6 workloads;
- the multi-repo workspace shapes in discovery;
- the third-language readiness review;
- an internal-harness dogfood checkpoint, "not CLI `analyze`".

**The operability plan's provisional M3 items** (OPP r3 §8).

*Before the protocol law:*
- O1 decided, with S-OP-4's record join under (a);
- O7 decided by the owner;
- the S-OP-2 vocabulary drafted.

*At M3:*
- `tracing` with nonpersistent sinks, the vocabulary and allowlists, the bounds and loss marker;
- phase spans and the operational record as harness instrumentation;
- the supervision primitive and liveness;
- the outcome matrix in tests;
- two-stage cancellation;
- the enforcement checks.

*Once their successors are accepted* (OPP §9): the file sink (S-OP-1), crash records (S-OP-7), capacity preflight (S-OP-8), public switches (S-OP-5 and S-OP-6), and the cancellation and commit join (S-OP-12). The G20/G21 controls are authored now (S-OP-11). DR-G20 itself is an M5 implementation row (BP:1024).

**M2 carry-ins:**

- **X11 successor law.** No creator command went live in M2 (EXIT:180; X11:18). The successor must fix:
  - the order;
  - the creator's host entry;
  - the one-RequestId rule;
  - how the creator command ends;
  - the creator terminations;
  - the F0 binary restatement;
  - the backup-status successor (X11:64-81).
- **X12c and X12d.** X12c is the DR-131 preview pack: its row and bundled bytes. X12d is the Run-closure `check_plan_pack` join in replay, which must land before any producer reaches X5 (X12:191-192).
- **The resume/repair writer** for crash states M2 leaves refused (EXIT:184-189).
- **An X3c successor**, because re-commit is refused at staging (EXIT:169).
- **The product licence unit** (AQP:536).

## Product state at eb0d503, by M3 owner module

| Owner (BP:887; CH14) | State | What exists |
|---|---|---|
| `crates/host/src/discovery.rs` | **absent** | First milestone M3 (COV:8963). |
| `crates/host/src/configuration.rs` | partial | Only X12's pack admission. "Layer merge, discovery, profiles, capabilities, waiver IDs and `resolvedConfigDigest` arrive with M3" (`crates/host/src/configuration.rs:1-4`). The digest is defined at IE:518. |
| `crates/host/src/snapshot.rs`, `plan.rs`, `analysis.rs`, `invocation.rs`, `syntax.rs` | **absent** | Planned owners at CH14:495, 489, 475, 485 and 496. |
| `crates/host/src/fact_admission.rs` | partial | The replay join only. "The M3 syntax, context, occupancy and Coverage joins arrive in this module" (`fact_admission.rs:1-3`). |
| `crates/host/src/request.rs`, `outcomes.rs` | partial | A process-custody `RequestAuthority` for the nonpersistent metadata host (`request.rs:15-19`). |
| `crates/host/src/finalization.rs`, `crates/storage/src/commit.rs` | present (M2) | The finalization and commit library. No command reaches it (`crates/host/src/lib.rs:53-62`). |
| `crates/components/*`, `crates/syntax/*` | **absent** | Not workspace members (`Cargo.toml:3`). CH14:37 and CH14:41 mark them "proposed". |
| `crates/security/src/component_manifest.rs` | present | The structural manifest owner, "no runtime or artifact authority" (`component_manifest.rs:1-2`). `components/manifest.rs` (the DR-G29 owner, BP:1033) is absent. |
| `crates/security/src/grants.rs` | **absent** | Yet it owns four M3 flags (COV:5277, 5317, 5337, 5377). |
| `crates/platform/src/process.rs` | **absent** | The only process module is a read-only translation query (`crates/platform/src/macos_process.rs:1-2`). |
| `crates/evaluator` | largely present | Inspectors (`crates/evaluator/src/lib.rs:9-38`), pack admission (`lib.rs:111`), derivation (`lib.rs:122`) and replay (`lib.rs:127`). The pack registry has **zero rows** (`pack-registry.json:3`). Named admission returns `NotBundled` (`policy.rs:1087`), and `check_plan_pack` refuses an unbundled Plan policy (`policy.rs:1401`). |
| `crates/identity`, `crates/contracts` | present | The `IdentityDomain` enum and its prefixes, `fact2` through `subject3` (`crates/identity/src/descriptors.rs:483-555`). Generated TS2 and Rust3 frame carriers (`crates/contracts/src/generated/protocol.rs:5422`, `:6111`) from a carrier input that is "not a production wire decoder" (`schemas/wire/native-carriers-v1.json:4`). |
| `providers/typescript` | stub | Present: `package.json`, `tsconfig.json` and the inert generated types (`src/generated/protocol.ts:1`), pinning Node 24.16.0 and TypeScript 6.0.3 (`package.json:7`, `:12`). Absent: every implementation source in CH14:507-517 and CH14:519-524. |
| `providers/rust` | stub | `main.rs` exits failure before reading a request (`providers/rust/src/main.rs:1-14`). It has its own workspace (`Cargo.toml:1-2`) and `rust-version = "1.95"` (`Cargo.toml:8`). The 1.95.0 pin has only rustfmt and clippy, no `rustc-dev` (`rust-toolchain.toml:2-4`). |
| `crates/lifecycle/src/installation.rs` | **absent** | The DR-G14 owner (BP:1018; COV:4770-4772), whose first milestone is M5 (COV:8976). |
| Tests | partial | `crates/host/tests/admission_tests.rs` exists. These named owners are absent: `discovery_tests.rs` (COV:5280), `workflow_tests.rs` (COV:7865) and `tests/qualification/README.md` (COV:8138). |
| Operability | **absent** | No `tracing` in `Cargo.lock`. No `std::panic::set_hook`. No `--timings` in `apps/cli/src/arguments.rs`. Three coded stderr lines (`apps/cli/src/bootstrap.rs:19`, `:44`, `:65`). The default command refuses (`arguments.rs:104`). |

Also in place:
- the M1 provider lane checks (`tools/check_typescript.py`, `tools/typescript-lanes.json`);
- the Rust provider, excluded from the host workspace (`Cargo.toml:4`), as BP:621-622 requires.

**Stale text that the M3 laws must not copy.** F02:220 still says TypeScript major 1, and F02:259 says Rust major 2. The current protocols are TS2 and Rust3 (BP:716-717).

## Units, in dependency order

Sizes follow EXIT:61:
- **S:** about one review round of a single file.
- **M:** several files with one inventory successor.
- **L:** a law plus two or three code units.
- **XL:** a law plus four or more units and a harness.

Each sub-unit (B1, C2 …) is reviewed on its own; the row is the planning unit.

| Unit | Scope | Depends on | Law / successor? | Size | Gates and quality items |
|---|---|---|---|---|---|
| M3-T2 | **T2 corpus manifests** and a harness-only `corpus fetch` (AQP:207, AQP:211-219).<br>- **T2a:** the medium repositories.<br>- **T2b:** the rest: Rust, TS/JS, polyglot, the multi-repo approximation (D15), Python (D9), size classes, the held-out set, and licence and size checks.<br>- **FW-14 outputs** (COV:8125-8145): pinned shapes, reproducible workarounds, manual-correction counts, and positive and negative fixtures. | — | none; D3 sign-off (AQP:524) | M | O1, D3, D9, D15, FW-14 |
| M3-Q0 | **Harness design record**:<br>- the case model (AQP:130-135) and the label ledger (AQP:249-263);<br>- the confidence rule (AQP:233-237);<br>- the exploratory envelope (AQP:419-425) and the D12 runner;<br>- the rule-catalog draft specs (AQP:167-191). | — | D13 and the D2 draft (AQP:523, 535); D12 (AQP:534) | M | Q1–Q8 definitions |
| M3-S | **S-P, feasibility probe:** can the pinned toolchain host the `rustc_driver` sidecar? Can Node and TypeScript load from a closure path? It is labelled preliminary and makes no Q6 claim.<br>**S-M, the measured INC-7 spike:** one-shot startup, sealing and replay costs on medium T2 (AQP:389), from a throwaway harness outside the product. S-M is a lead run set.<br>**Launch boundary:** S-P and S-M are lead-run throwaway tooling over public, pinned T2 bytes. They are not the product supervisor. They execute no repository code: no build script, proc-macro or package script. Their samples are labelled preliminary, and they make no production or confinement claim. | S-P: — . S-M: T2a, Q0 envelope, D13. D12 for Q6-labelled samples (AQP:534-535). | none | M | INC-7, Q6 |
| M3-CF | **Confinement work for O7** (see "O7").<br>- **CF-P, the confinement-feasibility probe:** a lead trial with a trivial test child, with no provider and no repository bytes. It covers the programmatic Seatbelt trial on macOS 27 (network denial and write-outside-scratch denial) and a desk check of the Linux primitives. It runs before D-law acceptance and needs no O7 decision, because it launches nothing that analyzes.<br>- **CF-1 and CF-2,** the successors, start once O7 is decided. | CF-P: — . CF-1/CF-2: O7. | SL S10 and S6 successor; AQ §5 item 4 and DR-128 disposition; disclosure-carrier successor | L | G09, G21, G29, G30 (AQ:344); O7 |
| M3-L | **M3 provider-protocol and reuse law.** It carries:<br>- INC-1 to INC-8 (AQP:370-390), with TS2/Rust3 unchanged (INC-5; BP:716-717) and one child per universe with no reuse (F02:222, F02:269);<br>- O1(a) and the S-OP-4 record join (OPP §3.6, §9);<br>- RequestId as correlator and phase-lawful identities (OPP §3.1);<br>- the provider-side two-stage cancel (OPP §5.5), with the commit-phase join referred to S-OP-12 and M3-J;<br>- a reference to the D law, which alone owns the launch rules under O7;<br>- a record correcting DR-G10's selector (REG:355 against COV:4671).<br>**Acceptance gate:** S-M, complete T2 (T2b), Q0, D3, D13 and the D2 draft, S-OP-2 drafted, O1 and **O7 decided**. The S-OP-4 join is the law's content, not a gate item. Drafting is parallel. | the gate | **law**; D5a successors only if an INC needs one (AQP:527); S-OP-4 | L | G10, G21; INC-1..8; O1, O7 |
| M3-P0 | **Package scaffolds:**<br>- `crates/components` and `crates/syntax` (CH14:284, CH14:288) as members;<br>- the provider source layout;<br>- dependency-policy rows.<br>One inventory successor, so that parallel lanes don't race the linear chain. | X9-6; licence unit | inventory successor | S | — |
| M3-B | **Configuration and discovery.**<br>- **B1, the resolver:** Config2 layers and provenance (AQ:43-53), `resolvedConfigDigest` (IE:518) and FW-13.<br>- **B2, discovery:** the S3 boundary (SL:105-332); NE:2's discovery part, §1.4 U-0..U-9, which keeps U-8's admitted boundaries (NE:816) and U-9's zero-config syntax fallback (NE:879); FW-01; and the host side of framework recognition, NE:9 (NE:2750).<br>- **B3, multi-repo workspaces (D15):** an X2 successor, because M2 "admits one closed, conventional Git layout" (`crates/security/src/custody/git_tracking.rs:5-6`). Also the consent flags and a new `security/grants.rs`. | P0 | **law**; X2 successor; SMAP successor if D15 needs one (AQP:537) | XL | FW-01, FW-13, FW-14, D15; 6 `inventory/*` cells; 7 flags; SL:3, NE:2 (§1.4), NE:9 |
| M3-C | **Sealed snapshot and Plan.**<br>- **C1, `snapshot.rs`:** exact read-set bytes under custody and `snapshot2` (IE:179).<br>- **C2, native contexts and closure admission:** NE:1430-1645 and BP:699-713. Tests use synthetic signed closures.<br>- **C3, dependency sources and prepared outputs:** DS-1..DS-6 (NE:1646-1698), with a library-level import of user-named sources (DS-5, NE:1688). Prepared sets are admitted under PO-0..PO-4 (NE:1803-1870): inert kinds, PO-1 staleness, PO-2 failed rows, PO-3 imported declared provenance, and PO-4 generated-file bounds. A harness recipe produces, pins and regenerates the imported prepared sets.<br>- **C4, `plan.rs`:** `plan2` (IE:182), the prospective-Plan bounds (NE:4276), and X12d (X12:192). | B, L. C4 also needs I1. | **law**; X12d inventory successor | XL | NE:3, NE:4; L-RS1, L-RS4 |
| M3-D | **Supervisor and common control.**<br>- **D1, `platform/process.rs`:** spawn with an explicit environment, no PATH, a process group and fd channels. It also builds the O7 confinement primitive. This module is the M6 DR-G22 owner (BP:1026), built early.<br>- **D2, the codecs:** `control_protocol.rs` and `provider_protocol.rs`, which own NE:10's dispatch (NE:2781-3316) with no translation (F02:168-169).<br>- **D3, `supervisor.rs`:** deadline, health, resources, tree kill, single settlement, provider cancel and candidate discard (F02:199-214; OPP §5.1).<br>- **D4, `manifest.rs` and `session_factory.rs`:** DR-G29 refusals with no ExecutionId (REG:374).<br>- **D5, the G21 controls.** OPP §10's control areas (privacy, correlation, custody, bounds, outcomes, crash, capacity, cancellation, liveness and overhead), plus three **new** confinement escape controls that extend S-OP-11 and are not in OPP §10: a network attempt, a write outside scratch and an ambient environment read.<br>**D-law** acceptance needs CF-P. D1's enforcement claim and D5's escape controls need CF-1. | P0, L, CF-P (law); CF-1 (D1 claim, D5) | **law** | XL | G10 (control), G21, G29; NE:10 |
| M3-E | **Syntax crate and grammar registry.**<br>- **E1, law:** the backend choice (CH14:614); the `SyntaxGrammarBundleV1` closure (BP:684-688); seven languages and fourteen suffixes (NE:260-263); NE:2's syntax-only part (NE:178, NE:218-306).<br>- **E2:** `grammar.rs`, `parser.rs`, `normalization.rs` and `candidates.rs` (CH14:372-379), plus NE:7's grammar-body clones (NE:2562-2647).<br>- **E3:** `host/syntax.rs` (CH14:496).<br>The crate is pure (BP:676-680). | P0, C2 | **law** | L | G13 (syntax); 11 `*/syntax-only` cells; NE:2 (syntax), NE:7 |
| M3-I1 | **The X12c preview pack:** freeze the preview rule IR; a contract successor for `opensip.preview.typescript.pack:1`; its bundled bytes and registry row, with self-checks; and the conditional policy-language successor (X12:191). Forbidden substitutes apply (X12:196-202). No live facts are needed. | — | X12c contract successor; a policy-language successor if needed | M | G25 path; X12c |
| M3-F | **TS/JS provider (TS2).**<br>- **F1, transport:** NE:2944-3002 and NE:3151-3316.<br>- **F2, facts:** imports, references, calls, unresolved edges, types (NE:2347), symbols and Coverage, across three modes.<br>- **F3:** reachability and framework recognition (L-FW1), syntax facts, and NE:7's clone modes including cross-tsjs (NE:2562-2647).<br>- **F4, runtime closure:** signed Node and TypeScript with no ambient Node (F02:252), running under the O7 profile.<br>Code can be authored earlier; a provider is **launched** only after O7 and D1's primitive. | Authoring: C1, C2, D2. Launch: D1 primitive, D3, O7. | none expected (BP:717) | XL | G10, G13, G14 preparation; 33 TS/JS cells; NE:7, NE:10 frames |
| M3-G | **Rust provider (Rust3).**<br>- **G1a:** snapshot transport and `context.rs`.<br>- **G1b:** dependency and prepared frames (NE:2872-2943).<br>- **G2:** `compiler_adapter.rs`, the `rustc_driver` sidecar (`12-architecture-completion-goal.md:145`) with the rust-dev-llvm closure (NE:1445). It is **authored** after S-P. **G2-v**, its lawful launch and validation under the O7 profile, runs after O7 and D1's primitive.<br>- **G3:** inventory, facts and Coverage for L-RS1..L-RS3 (NE:1793).<br>- **G4:** prepared-mode consumption (L-RS4, PO-1..PO-4) and NE:7's clones. | G1a: C1, C2, D3. G1b: C3. G2 authoring: S-P. G2-v: O7, D1. | none expected (BP:717) | XL | G10, G13, G14 preparation; 22 Rust cells; NE:7, NE:10 frames |
| M3-H | **Fact admission:** the syntax, context, occupancy and Coverage joins (`fact_admission.rs:1-3`); relation-registry and Coverage-domain refusals (REG:368); a missing rung is indeterminate (REG:370). Framing grants no fact authority (CH14:482). | C4; E3 or F1 | **law** | L | G23, G25; NE:5 |
| M3-J | **Guarded durable host pipeline.**<br>- **J1, law:** the X11 successor (X11:64-81), the invocation DAG (WS:76-256), the backup-status successor, and the commit-phase cancellation join S-OP-12 with the X3D and X7 owners (OPP §5.5, §9).<br>- **J2, `invocation.rs`, `analysis.rs` and the `outcomes.rs` NE:11 work:** the deficiency-cause carriers, precedence and D9 bridge (NE:3317-3858); the ephemeral path end to end. No durable write.<br>- **J3, durable:** through X7 finalization and the commit; `workflow_tests.rs`; the re-commit limit (EXIT:169).<br>- **J4, the resume/repair writer** (EXIT:184-189). | B, C (with X12d), D, H, I1; producers | **law**; backup-status successor; X3c successor; S-OP-12 | XL | G25; NE:11, NE:14, NE:15; FW-03, FW-08; WS:2 |
| M3-I2 | **Draft catalog, non-authoritative.** `PolicyDocumentV2` rules (AQP:165-191), evaluated only in the harness over admitted facts (AQP:481). The product pack stays at M5 (D2, AQP:523). | H, Q0 | none at M3 | M | Q2–Q4 exploratory |
| M3-K | **Quality harness and T1.**<br>- **K1:** the harness core and determinism driver (AQP:316-319).<br>- **K2:** T1 in three lanes (TS/JS, Rust, syntax-only per grammar): 57, 6 and 3 cells (AQP:481; AQ:233-234). K2 is authored before the producers, because expected answers must be independent (AQP:104). | Q0, T2b | D13 | XL | Q1, Q4, G13 |
| M3-M | **Exploratory measurement and the dogfood checkpoint:** Q1/Q4 on T1; Q2–Q4 through I2; the determinism suite; Q6 core analysis kept separate from first use and from preparation-invalidating edits (AQP:340-347); T3 after the licence unit (AQP:536). **This plan's rule, not AQP's:** the exploratory report may close while adjudication of gating and repair-eligible findings is still pending. Those strata are reported as not yet adjudicated. Strata with too few findings are INSUFFICIENT-EVIDENCE (AQP:236). Any later Q2 use still requires every such finding adjudicated (AQP:228), with unclear labels resolved by the human expert (AQP:246). | J3, G4, F3, E3, I2, K1, K2, O1 | none | L | Q1–Q6 exploratory |
| M3-O | **Operability.**<br>- **O1:** `tracing`, the S-OP-2 vocabulary, nonpersistent sinks, the bounds, phase spans and the operational record with INC-8's reuse disclosure (OPP §3.1-§3.3, §4.1), plus the enforcement checks (OPP §7).<br>- **O2, each part gated:** S-OP-1, S-OP-7, S-OP-8, S-OP-5 and S-OP-6. **Lead rule:** M3-X requires each O2 part whose successor is accepted by then. A part whose successor is not yet accepted is recorded as carried to M4. M3-X is not held for it.<br>- **O3:** the G20/G21 controls (OPP §10, plus D5's escape extension). | P0; S-OP-2 | S-OP-1, -2, -5, -6, -7, -8, -11 (OPP §9) | L | G21; G20 controls (M5 row, BP:1024) |
| M3-R | **Third-language readiness review** with Python, and the onboarding kit (AQP:448-470). | L, F2, G3, K2 | record only | M | O8, D9 |
| M3-X | **Exit gate.** BP:887's completion checks on this host's profile: the seven gates prepared, both languages present, and the O7 implementation in place. | M3-M, B3, D4, D5, E, F4, CF-2, J4, O1, O3, R; O2 parts per the O-row rule | none | L | all M3 gates |

**Why these splits.**

- **B and C:** discovery answers to SL S3 and D15's successor; the snapshot answers to identity.
- **C kept whole:** `plan2` binds all of its inputs (IE:182), and the host owns resolved inputs before the PlanId (NE:2497-2499).
- **C3 and G1b/G4:** the host admits dependency and prepared sets (NE:1704-1712); the provider consumes them.
- **G1a and G1b:** splitting the snapshot frames from the dependency frames lets the Rust transport start on C1 instead of waiting for C3.
- **I1 and I2:** I1 is a mandatory input of every real Plan (X12:125, X12:134; `policy.rs:1401`). I2 is exploratory only.
- **CF:** O7's successors have different owners from supervision (REG:317).

## Critical path and parallel lanes

**Day 0 is M3-L's acceptance.** Because O7 and S-M are in L's gate, both are done by then.

**Assumed done before day 0** (not sized here):
- the B, C, D, E, H and J laws and the X2 successor accepted, with D-law acceptance after CF-P;
- P0 landed;
- I1 done;
- G2 authored.

**Durations are planning assumptions:**
- a code sub-unit takes 1 day for S, 2 for M, 3 for L and 4–5 for a hard XL part, including build, review and integration;
- a successor law takes about 3 rounds, bounded at 5 days;
- one lead run set at a time.

| Sub-unit | Days | Starts after | Finishes (day) |
|---|---|---|---|
| B1 → B2 → B3 | 2 + 3 + 3 | — / B1 / B2 | 2 / 5 / 8 |
| C1 | 2 | B2 | 7 |
| C2 | 3 | — | 3 |
| C3 | 3 | C1 | 10 |
| C4 + X12d | 2 | C1, C2, C3, B1, I1 | 12 |
| CF-1 → CF-2 | ≤ 5 + 2 | O7 (≤ day 0) / CF-1 | ≤ 5 / ≤ 7 |
| D1 (with the primitive) → D2 → D3 | 2 + 2 + 3 | — | 2 / 4 / 7 |
| D4; D5 | 2; 3 | D3; D3 and CF-1 | 9; 10 |
| E2 → E3 | 3 + 1 | C2 / E2 | 6 / 7 |
| F1 → F2 → F3 | 3 + 4 + 3 | C1, C2, D3 (launch: D1, O7) | 10 / 14 / 17 |
| F4 | 2 | F1, D1 | 12 |
| G2-v (launch and validation under the profile) | 1 | D1 (O7 is done by day 0) | 3 |
| G1a → G1b | 3 + 2 | C1, D3 / G1a, C3 | 10 / 12 |
| G3 → G4 | 5 + 3 | G1a, G2-v / G3, G1b | 15 / 18 |
| H | 3 | C4, F1 | 15 |
| I2 | 2 | H, Q0 | 17 |
| J2 → J3 → J4 | 3 + 3 + 2 | H, C4, D3, CF-2 / J2, F2, G3 / J3 | 18 / 21 / 23 |
| K1 | 3 | Q0, T2b | 3 |
| **K2 (T1, three lanes)** | **not yet sized** | Q0 | **unbounded until Q0 sizes it** |
| O1; O3 | 4; 3 | P0 and S-OP-2; O1 and D5 | 4; 13 |
| O2 parts | successor-gated | each S-OP | carried to M4 if unaccepted (O-row rule) |
| R | 2 | F2, G3, K2 | max(15, K2) + 2 |
| M3-M | 3 | J3, G4, F3, E3, I2, K1, K2, O1 | max(21, K2) + 3 |
| M3-X | 2 | M3-M, B3, D4, D5, F4, CF-2, J4, O3, R | max(M3-M, R, 23) + 2 |

**Conditional host-chain duration: 26 days.**

> B1 → B2 → C1 → C3 → C4 → H → J2 → J3 → M3-M → M3-X

It holds only if K2 finishes by day 21. Every other bounded branch finishes earlier:
- the Rust branch at 18, 3 days of slack against J3;
- J4 at 23;
- O3 at 13;
- CF-2 at 7.

If K2 runs past day 21, K2 is the critical path.

**The whole-M3 total is left uncomputed.** Three things are unbounded: the O7 decision date (outside the lead's control), the parallel pre-day-0 law rounds, and K2's size.

**The bounded pre-day-0 work:**
- T2a (1);
- Q0 (3), then S-M (2), with T2b (2) in parallel;
- S-P (1), then G2 authoring (4);
- CF-P (2);
- L acceptance (about 2).

Recompute the total when Q0 sizes K2 and O7 is decided, and again after S-M or if S-P or CF-P fails.

**Calibration only:** M2's exit integrated 55 product commits from `d4239a5` to `eb0d503` (`git rev-list --count d4239a5..eb0d503`). Those were mostly smaller mechanism units.

**Effort:**
- about 20 law, successor or record units: L, CF-1, CF-2, the B/C/D/E/H/J laws, X2, X12c, X12d, backup-status, X3c, S-OP-1/2/7/8/12, D13 and the policy-language successor if one is needed;
- about 43 code, harness or probe sub-units (CF-P, G2-v, J4 included).

That is roughly 63 reviewed units. M5-EX (below) is M5 work.

**Lanes:**

| Lane | Units | Reviewer (suggested) |
|---|---|---|
| Host core (the critical path) | B → C → H → J | Grok (facts) |
| Components and confinement | D, CF, F1/G1 conformance | Codex (method) |
| Rust compiler | S-P → G2 → G3 → G4 | CODEX2 |
| Syntax and TS analysis | E → F2/F3/F4 | GROK2 |
| Pre-law gate, then quality and operability | T2, Q0, S-M, I1, then K, I2, O, R | the next free reviewer. Pre-law items take priority because they gate L. |

**Lead run sets stay serialized.** The crash matrix has a 5000 ms timing guard (subject of product commit `eb0d503`), and measurement needs a quiet machine. S-M and M3-M wait for X9's lead sets.

**Recommended start.** No product crate is touched before X9-6.

1. **M3-T2** (T2a, then T2b).
2. **M3-Q0** (it gates both S-M and L).
3. **M3-S-P** and **CF-P**, the two feasibility probes.

**Also immediate:**
- **M3-I1**'s rule-IR freeze;
- drafting M3-L;
- **asking the owner for O7 now** (done; see below).

## Choices left open, with lead recommendations

**Already decided; cite, don't reopen:**

- **Owner decisions:** D4, D5, D6, D9 timing, D10, D11, D14, D15 and D16 (AQP:525-538).
- **Evaluation and dogfood:** catalog evaluation is non-authoritative at M3 (AQP:481), and CLI dogfood is at M4 (AQP:483; BP:887).
- **Protocols and crates:**
  - the protocols are TS2 and Rust3 (BP:717);
  - the Rust substrate is `rustc_driver` (`12-architecture-completion-goal.md:145`);
  - `crates/syntax` is pure (BP:676-678).
- **Carried in from M2:** no creator command in M2 (X11:18); X12c and X12d at M3 (X12:191-192).
- **Python:** the support decision comes after M3's review (AQP:446).

The lead decides each choice below in the named unit's law, and a reviewer checks it.

- **O1 (M3-L).** Recommendation: (a), existing admitted observations only (OPP §3.6). Rejected: a new frame, which needs S-OP-3 and both protocol joins.
- **Syntax backend (E1; CH14:614).** Recommendation: a trial between tree-sitter and hand-written parsers. The lead leans to tree-sitter for Rust, TS and JS: one `grammarVariant` and anchor model, and retained grammar bytes that fit the `kind=grammar` closure (BP:684-688). Its C runtime joins the host TCB (BP:680-682).
- **Dependency sources at M3 (C3).** Recommendation: a library-level import of user-named sources (NE:1681-1691), driven by the harness. The `import` command stays at M5 (BP:957). Without it, T2 registry dependencies are `input-closure-incomplete` (NE:1693-1698).
- **Prepared mode at M3 (C3, G4).** Recommendation: `imported-descriptor` sets from the harness recipe (NE:1806; NE:2533-2537). `native-prepare` stays at M5 (BP:992). No repository code runs at M3.
- **DR-G14 placement (M3-L).** The gate is M3 (COV:4770), but its owner module is M5 (owner string COV:4772; first milestone COV:8976). Recommendation: M3 prepares closure manifests and no-ambient-runtime refusals (F4, G2); installation stays at M5.
- **Public CLI (J1).** Recommendation: nothing is wired. J1 fixes the order and identity rules (BP:887-888).
- **Changed-scope (M3-L).** Recommendation: none ships. The obligations go into the law, and M4 decides with S-M data (AQP:483).
- **Logging (O1).** Recommendation: `tracing` with one host-owned subscriber and no environment input (OPP §3.1, §3.5).
- **Platform scope (M3-X).** Recommendation: run and claim only this host's macOS family (NE:157-160). The Linux confinement code is built but exercised only on Linux lanes.

## O7: hostile-input confinement (owner decision, pending)

**Status.** O7 is an owner decision (OPP §5.6, §9) and is **pending**. It is a **hard prerequisite of M3-L and of provider launch**: No provider (F, G, G2-v) launches until O7 is decided and D1's primitive exists. Authoring may start earlier. This keeps OPP §8's schedule.

**The lead's recommendation, as put to the owner:**

1. **Analysis never executes repository code by default.** Existing law already says this: "Repository execution is disabled by default" (SL:1059), and the Rust worker's `workerExecutesRepositoryCode` is the constant `false` (NE:2534-2535).
2. **Providers run under OS confinement:**
   - on Linux and AL2023: Landlock, seccomp and no network;
   - on macOS: a Seatbelt profile that denies network access and any write outside the provider's scratch space.
3. **Where confinement is unavailable,** the result discloses it, and the documentation requires containers for untrusted pull requests.
4. **Executing repository code** (Rust build scripts and proc-macros in prepared mode) requires the existing `RepoExecutionGrantV2` (SL:1071) and runs only inside confinement or a container.

**Why it needs successors.** Accepted law currently disclaims confinement:
- "confinement is never claimed" (SL:1113);
- "No confinement is claimed" for unconfined children (SL:497);
- "No process/WASM boundary is claimed as a sandbox" (AQ:344);
- "No sandbox is claimed" (NE:2554);
- G21 "does not claim security confinement" (REG:366);
- DR-128 holds the sandbox boundary (REG:317).

Items 2 to 4 add enforced hardening and a disclosure. They must stay distinct from a sandbox claim for untrusted code, which only DR-128 could open.

**Units and successors it needs (all in M3-CF unless noted):**

- **CF-P, the feasibility probe,** before D-law acceptance: a programmatic Seatbelt trial on macOS 27, plus a desk check of the Linux primitives.

- **CF-1, the confinement successor** (owners: product security and platform owners, the DR-128 row's owners, REG:317):
  - an SL S10 and S6 successor with the per-platform enforcement matrix and the honest wording;
  - an AQ §5 item 4 disposition;
  - a DR-128 record saying this opens no untrusted-code scope.
- **CF-2, the disclosure carrier:** a WS output successor, or an S-OP-6 join, for "provider ran unconfined: <reason>". It sits beside Coverage and never inside it.
- **D1, the confinement primitive:**
  - a macOS Seatbelt profile applied at spawn;
  - Landlock, seccomp and a network namespace on Linux, built at M3 and exercised on Linux lanes.
- **D-law:** the single owner of the launch rules under O7. M3-L cites it.
- **D5 and S-OP-11:** three new escape controls (a network attempt, a write outside scratch and an ambient environment read). They extend OPP §10, which does not contain them.
- **F4 and G2:** the provider closures run inside the profile (Node, the `rustc` temporary directories).
- **M4:** the container guidance in the runbook (OPP §6).
- **M5-EX, a gated M5 successor package for item 4.** All three successors must be accepted before M5's `execution.rs` (`native-prepare`, `test-run`; BP:974, BP:992) claims any confinement or container enforcement:
  1. **The native §5.2 admission and disclosure join.** Today, `AuthorizedExecutionV2` effects are copied from PTT, and a record claiming more is refused: network, subprocess and filesystem write are `DISCLOSURE-ONLY` (NE:2440-2444; the reference admission is NEM:2170-2172). The mandatory human and JSON sentence says OpenSIP "does not prevent network access or other effects on this platform" (NE:2480-2487; NEM:2181-2182). The successor moves only the measured platform and effect cells and the sentence that depends on them.
  2. **The WS §7 test-execution schema join.** `ENFORCED-PLATFORM` is not in `EnforcementValue`, and admitting it "requires a successor truth-table profile and test-execution schema" (WS:1071-1081; TES:7-14). The test pre-spawn sentence also changes.
  3. **A measured permission truth-table profile succeeding PTT,** owned by the security owner (S10). Only cells measured on a platform move (NE:2480-2481).

  No new native carrier major is assumed where the existing vocabulary suffices. Until M5-EX is accepted, M5 execution keeps today's disclosure-only behaviour.

**Boundaries kept:**
- **No repository-code execution in M3.** Prepared sets are imported (C3).
- **The worker prohibition stands:** `workerExecutesRepositoryCode` is constant `false` (NE:2534-2535).
- **DR-128's untrusted-code scope stays closed.** Untrusted native or WASM components are not admitted, and no process boundary is claimed as a sandbox (AQ:344; REG:317). Items 2 to 4 are hardening and disclosure for first-party providers and trusted repository code, not an admission path.

**Risk.** Whether Seatbelt can be applied programmatically on macOS 27 is unverified. CF-P decides it before the D law is accepted. If it fails, item 3's disclosure path applies on macOS, and the D law records that.

## Owner decisions

- **O7:** pending, as above. It blocks M3-L and provider launch.
- **O4, OTLP** (OPP §4.2, §9): an M5 matter.
- **O9, raw provider stderr capture** (OPP §9; owner sign-off). Recommendation: not at M3.
- **Sign-offs:** D2, D3, D12 and D13 (AQP:523-535). D13 and D12 are on S-M's path.
- **Owner actions:**
  - adjudication expert time (AQP:246). It does not hold M3-X.
  - T3 after the licence unit (AQP:536).
  - signing keys for real-machine runs (EXIT:110). They are not needed for M3 exit, where tests use labelled synthetic closures.

## Risks

- **The Rust compiler integration.** It needs rustc-dev and rust-dev-llvm (NE:1445). The pin has neither (`providers/rust/rust-toolchain.toml:2-4`). Stable-toolchain hosting is unverified. S-P probes it first.
- **Imported dependency sources.** Real Rust repositories need them (NE:1688-1698), and the `import` command is M5 (BP:957). C3 covers this.
- **D15 against M2's single-layout VCS rule** (`git_tracking.rs:5-6`). B3's X2 successor is needed.
- **Missing owners.**
  - `security/grants.rs` owns four M3 flags (COV:5277, 5317, 5337, 5377).
  - `lifecycle/installation.rs` owns DR-G14 (BP:1018), but its first milestone is M5.
  - `platform/process.rs` is the M6 DR-G22 owner (BP:1026); D1 builds it early.
- **Record drift.**
  - DR-G10's register row is stale (REG:355).
  - NE §14 says "independent Claude review pending" (NE:4203).
  - F02:220 and F02:259 still state the old majors.
  - M3-L records all three.
- **O7 sits outside the lead's control,** and it gates L. A late decision moves the whole schedule. The confinement successors also reverse existing "never claimed" wording, which needs careful review.
- **Contention.** One linear inventory chain and a single quiet machine for measurement. P0 and the lanes reduce this; they don't remove it.
- **Budgets.** The one-shot design may miss the §5.2 budgets (AQP:357-359). S-M exists to find that out before L.
- **Adjudication capacity** (AQP:241-247) limits exploratory Q2 depth, not exit.
- **Operability r3 is still in review.** M3-O and M3-L follow the accepted revision.

## Not claimed

- No unit has started, and no measurement, spike or test was run for this record.
- No gate is prepared or qualified. No contract, schema, gate, register row or threshold is changed.
- Durations and effort are assumptions.
- M3 does not claim:
  - CLI analysis (M4);
  - changed-scope or resident analysis;
  - `import`, `native-prepare` or repository-code execution (M5), or any confinement or container enforcement of it before M5-EX;
  - Linux or AL2023 runs;
  - Q2–Q8 qualification (M6, via D13);
  - T3 before the licence unit;
  - any O7 outcome before the owner decides.
- This record was written from code reading at `eb0d503` only.
