# The O1 operability law: proposal M3-O1 r1

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Law for code unit **O1** of the accepted M3 unit plan's M3-O row (M3P:317). It fixes where O1's code lives, how records travel without `tracing`, who mints identities, which sinks run at M3, how the operational record reaches the harness, who registers which event, how enforcement starts, and how S-OP-2 is recorded. It defines O1's code units: **O1-a**, **O1-p**, **O1-b**, **O1-c** and **O1-S**.

**Draft r1, not accepted. Not code.** This law touches no product file. Product main is `b7b87b7` (E2a).

**Why a law.** O1's implementation agent read the accepted operability plan and S-OP-2 r6, then stopped before coding, as instructed, and reported nine gaps, G1 to G9. S-OP-2 leaves several of them to M3-O in so many words: "M3-O chooses its crate" (SOP2:161), and it does not decide "the choice of `tracing`; crate placement" (SOP2:1032). "Problem" restates each gap with its facts.

**Standings.** This law pins accepted snapshots only (Short names).
- **Accepted and pinned:** S-OP-2 r6 (Codex, ACCEPT-DESIGN-UNIT), the operability plan r3, M3-PLAN r10, M3-D r5, J-RW r4, and the Q0 harness design r13 with its envelope schema.
- **Accepted in review, effective with L:** M3-L r5. This law takes no rule from L. It cites L's items 13 and 14 only for the events L needs, and those events are emitted only once L is in effect (item 16).
- **Not yet bound:** S-OP-2 itself. Its item 24 says the lead records it when M3-O's first code unit lands. Item 22 records it, in two design units reviewed in the same request.

**Lead decisions.** Every item marked "lead decision" is dated 2026-10-04. It is made under the owner's standing direction to decide on the lead's recommendation and to block only where no recommendation exists. Each names the alternatives it rejects, and the owner may reverse any of them. Items marked "law" restate what accepted text already requires. Items marked "record" change nothing.

**One finding beyond the brief.** S-OP-2's recording cannot bind as its item 24 writes it. Its two overrides name SDK4 and DRC as parents, and neither file is in the design the product lock selects. Item 22 records S-OP-2 in two units, a parent selection and the recording, and a local binding check confirms both the refusal and the fix.

## Short names

Lines were checked against the files named here on 2026-10-04. Each sha256 prefix is the first 8 hex of the exact file pinned in this law's review request (`reviews/codex-o1-law-r1/hashes.txt`).

| Name | Document | Standing | sha256 |
|---|---|---|---|
| **SOP2** | `docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md` | S-OP-2 r6, accepted by Codex as ACCEPT-DESIGN-UNIT (`reviews/codex-s-op-2-r6`). Its bytes carry r5's title line. | `ce8d3a4b…` |
| **OPP** | `docs/implementation/m3/operability/PLAN-r3.md` | operability plan r3, accepted bytes | `b49035f2…` |
| **M3P** | `docs/implementation/m3/M3-PLAN-r10.md` | M3-PLAN r10, accepted by Codex | `ec8c38f8…` |
| **MD** | `docs/implementation/m3/supervisor-d/PROPOSAL-r5.md` | M3-D r5, accepted by Grok | `224b9228…` |
| **JRW** | `docs/implementation/m3/resume-repair-jrw/PROPOSAL-r4.md` | J-RW r4, accepted by Codex | `9c53bce7…` |
| **ML** | `docs/implementation/m3/provider-protocol-l/PROPOSAL-r5.md` | M3-L r5, accepted in review by GROK2; effective only with L | `f654ee4e…` |
| **Q0** | `docs/implementation/m3/harness/DESIGN-r13.md` | harness design r13, accepted by CODEX2 | `37438317…` |
| **ENV** | `docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1-r13.json` | envelope schema r13, accepted with Q0 | `71f682d1…` |
| **CH14** | `docs/v2/architecture/14-repository-and-module-layout.md` | architecture, classified `current/architecture`; in the selected design base | `c7b10bf6…` |
| **APP** | `docs/coop/completion/architecture-application.v1.json` | the D-369 application; in the selected design base | `15b3932a…` |
| **SDK4** | `docs/coop/artifacts/component-sdk-contract.v4.json` | DR-125's inherited contract; not in the selected design | `c53d541f…` |
| **DRC** | `docs/coop/completion/distribution-runtime-completion.v2.md` | the D.SDK selection of §8; not in the selected design | `9ab2874e…` |
| **SOP2-U** | `docs/implementation/m3/operability/s-op-2/s-op-2-r/README.md` and the two units' records | the S-OP-2 recording, in review in the same request | pinned in the request |
| **VD** | `tools/verify_design.py` at product `b7b87b7` | the design verifier | `7b313de6…` |

Product paths are under `opensip/` at `b7b87b7`. In-flight units' files were read in their own worktrees with read-only `git status` and `git diff` on 2026-10-04.

## Acceptance gate

This law may be reviewed and accepted now.
- **It launches nothing and spawns nothing.** O1 adds host code, a crate and tools. O7 is not a gate item.
- **It relies on accepted text only.** S-OP-2 r6 is accepted. Its binding (item 22) gates O1-a's integration, not this law.
- **Its successor and its in-flight neighbours gate code units, not acceptance.** S-OP-2b (owed, exact text below) gates O1-b. E2s gates O1-c. J3a gates O1-p and O1-b. J3a, J4a and X3c-3 gate O1-S. Item 23 says which files each unit must leave alone while those units are in flight.

## Problem

**What exists at main `b7b87b7`.**
- **No logging code.** There is no event type, no logging crate and no panic hook. The only production stderr output is three fixed coded lines in `apps/cli/src/bootstrap.rs` (`:18-22`, `:43-47`, `:63-68`). `Cargo.lock` has neither `tracing` nor `log`.
- **The dependency policy.** `tools/host/dependency-policy.json` admits only crates "that an accepted M3 law assigns" to a package. Its selection rule requires a pure-Rust crate that "declares #![forbid(unsafe_code)]", with no build script and an allowed licence. No accepted law assigns `tracing`: OPP calls it "proposed, unchosen by law" (OPP:145), S-OP-2 "does not require `tracing`" (SOP2:394), and M3P only recommends it (M3P:743).
- **Who must emit.** Host emits most events. Storage must emit the two `storage.commit.*` events (SOP2:891-892), and components must emit D3a's (MD:681-703). Neither storage nor components may depend on host (inventory v138's package edges).
- **Who owns the identities.** The RequestId is an opaque `RequestContext` inside host's crate-private `RequestAuthority` (`crates/host/src/request.rs:18-55`). J3a, in flight, changes that file and moves `RequestIdentity` and a reserved ExecutionId type into `crates/platform/src/lib.rs` (J3a's worktree). `PublishedCommit` is storage's (`crates/storage/src/commit.rs:66-75`, `:103`).
- **No lawful channel to the harness.** OPP sends the operational record to the log file and the exploratory envelope at M3 (OPP:248). There is no file before S-OP-1, stderr is off by default and its switches are S-OP-6's (OPP:226), the environment is forbidden (SOP2 item 21), and a new sink needs an S-OP-2 successor (SOP2:236).
- **Enforcement sites today.** 306 `let _ =` lines in 150 files, of which 140 lines are in production paths (platform 56, security 70, storage 10, cli 3, lifecycle 1); direct stdio in 30 files; environment reads in 16; `process::Command` in 29; `process::exit` only in `crates/platform/src/crash_barrier.rs`.

**The nine gaps.**

| Gap | What is open | Item |
|---|---|---|
| G1 | Crate placement: storage and components must emit, and cannot depend on host. Platform has no CPU-time call. | 1, 2 |
| G2 | Scopes and mints: S-OP-2 item 9 wants scopes made only by the minting transition, and no owner has a typed mint. | 7, 8 |
| G3 | `tracing` is not admissible under the policy. K10's path tag needs HMAC-SHA-256, and no `hmac` crate is locked. | 3, 4 |
| G4 | The operational record's form and channel: what bytes `recordSha256` hashes, how phases nest, and which channel is lawful at M3. | 13 to 15 |
| G5 | Which sinks run at M3, at which level, selected how, and where finalization runs. | 9 to 12 |
| G6 | The enforcement mechanism, its exception list, the `Disposition` members, and whether tests are in scope. | 19 to 21 |
| G7 | D9 and configuration tables need literal, pinned generated tables, and E2s is regenerating those modules. | 17 |
| G8 | The K6 code-location census: "M3-O chooses the mechanism" (SOP2:274). | 18 |
| G9 | S-OP-2 is not bound (its item 24). | 22 |

## Decisions at a glance

| # | Decision | Rejected |
|---|---|---|
| 1 | **A new crate,** `crates/operability` (`opensip-operability`), `forbid(unsafe_code)`, depending only on platform. Host, storage and components depend on it. CH14 needs only a record note. | the registry inside host; a CH14 contract successor |
| 2 | **Platform gains** a CPU-time call, an inherited-descriptor admission and the `dispose` helper, in one leg, O1-p. | any `unsafe` in operability |
| 3 | **SHA-256 written in-house** inside operability, under HMAC-SHA-256 also written in-house. No new crate, and no new edge. | identity's `raw_sha256`; `sha2-const-stable` or `sha2` directly; platform's macOS-only call |
| 4 | **No `tracing`.** An in-house transport, and a lane check that fails if `tracing` or `log` enters the host lock without a law. | admitting `tracing`; the `log` facade |
| 5 | O1 builds S-OP-2's items 1 to 17 and their controls, except the parts S-OP-2 assigns to S-OP-1, -6, -7, -9 and -10. | none |
| 6 | C-1 uses the existing X8 compile-refusal pattern. | rustdoc `compile_fail`; `trybuild` |
| 7 | **Scope types, a one-time capability set and the storage owner token,** tested with test-only mints. | public constructors; run-time checks |
| 8 | **Owners wire the real mints.** No record carries an identity, and so no production record exists, until its owner has wired the mint. | O1 minting identities it does not own |
| 9 | **Production constants:** file off, stderr off, pre-scope buffer and ring on. | stderr on in production |
| 10 | **A dev-only stderr feature,** refused without debug assertions, at a fixed `debug` level. | stderr in every debug build |
| 11 | **Finalization at the existing termination points.** The frozen summary stays unrendered until S-OP-6. | OPP's example wording now |
| 12 | **Logging-start failure disables logging** and changes no outcome. | starting without the path key |
| 13 | **A harness-only sink** on descriptor 3, under a narrow successor, S-OP-2b. `recordSha256` hashes that stream. | gating phase timings on S-OP-1 |
| 14 | **The phase vocabulary:** plan §4.1's phases under a root `request`; `host.phase.started`; `at` on both phase events; a `not-applicable` outcome. | free-form phase names |
| 16 | **Registrations:** O1 registers its own events and J-RW's; D3a registers the provider and supervision events with a new `tool` domain; other events are registered by their first emitter. | O1 registering all 27 now |
| 17 | **Termination and configuration tables after E2s,** from a generator that emits literal tables. | hand-copied D9 tables |
| 18 | **K6's census goes to S-OP-7's unit.** | choosing a census now |
| 19 | **A source-scan checker** with a per-file count exception list and negative controls. Test-only files are out of scope. | clippy lints now; scanning tests |
| 20 | **`dispose` in platform,** over a closed five-member enum. | `dispose` in operability or contracts |
| 21 | **A later sweep, O1-S,** after J3a, J4a and X3c-3 integrate. | sweeping in O1-a |
| 22 | **S-OP-2 is recorded in two units:** S-OP-2-P selects SDK4 and DRC; S-OP-2-R makes item 24's two overrides. | one unit, which cannot bind |
| 23 | **Units O1-a, O1-p, O1-b, O1-c and O1-S.** | one O1 unit |

---

## A. Placement

### 1. The crate `crates/operability` (lead decision; G1)

- **Decision.**
  - **The package.** A new workspace member `crates/operability`, package `opensip-operability`, library only. It declares `#![forbid(unsafe_code)]` at its root and `unsafe_code = "forbid"` under `[lints.rust]`, as `crates/syntax` and `crates/security` do. It has no build script and no external dependency.
  - **Its one edge** is `opensip-platform`. Every platform mechanism it needs is in item 2: entropy (`request_entropy`, `crates/platform/src/lib.rs:57`), CPU time and the harness descriptor.
  - **Who depends on it.** Host, storage and components:
    - **host**, from O1-a: the capability set, finalization and, later, the request scope;
    - **storage**, for the two `storage.commit.*` events. Its manifest edge arrives with the first unit that emits them (item 8);
    - **components**, for D3a's events. Its manifest edge arrives with D3a, as P0's scaffold note says every edge does (`crates/components/Cargo.toml`).

    O1-a's inventory successor adds the package row (`opensip-operability`, `rust-library`, `crates/operability`, dependencies `[opensip-platform]`) and adds `opensip-operability` to the allowed dependencies of host, storage and components. `check_package_edges.py` checks declared edges, development edges included, against that list (`tools/check_package_edges.py:35-55`).
  - **Who does not.** Security and platform. Security's events reach the registry as typed results that host turns into records; J-RW's completions are the first case (item 16). Platform is below operability. `apps/cli` reaches operability through host and only forwards features to it.
  - **Layout.** Spellings are provisional; O1-a fixes them:

    | Module | Holds |
    |---|---|
    | `lib.rs` | the public API: `start`, scopes, kinds, `emit` |
    | `registry.rs` | the one registry module: `code_tables!`, `registry!`, every event, table and retired descriptor (SOP2 items 1 to 3) |
    | `kinds.rs` | K1 to K15 and their constructors (SOP2 item 5) |
    | `scope.rs` | scopes, markers, mints and the owner token (items 7 and 8) |
    | `wire.rs` | item 13c's encoder, rule E and item 14's static bounds |
    | `readback.rs` | item 13a's reader and its reader-only values |
    | `transport.rs` | item 15's admission and queue, item 16's commit cells and finalization, item 17's marker and gate |
    | `sinks.rs` | the pre-scope buffer, the crash ring, the development stderr sink and, in O1-b, the harness sink |
    | `hmac.rs` | SHA-256 and HMAC-SHA-256 (item 3) |
    | `constants.rs` | the release constants of item 9 |

- **CH14: a record note, not a contract successor.** CH14 is architecture text for this purpose. The facts:
  - its package table "grants no component authority", and its names and edges "are proposals except for the agreed `opensip-cli` name" (CH14:271-275). The table is generated from the architecture's own file inventory (CH14:6), and the chapter is classified `current/architecture`;
  - the product's binding edge list is the **selected repository-file inventory**, which `check_package_edges.py` enforces and which O1-a's inventory successor changes under `ACCEPT-UNIT` review;
  - earlier units overrode CH14 lines only where they selected something CH14 had left open or described differently: `bootstrap-selection-v1` at CH14:105-106, :316 and :550, and `metadata-v2` at CH14:325. M3-H's new paths took a record note (CH14-H).

  O1 contradicts no CH14 sentence. It adds one package row, three edges and one platform file. The record note **CH14-O** (Cross-law items) adds them at the next CH14 refresh.
- **Basis:** SOP2:161; OPP §3.2; CH14:21-23, :269-291; inventory v138's `packages`.
- **Rejected:**
  - **The registry inside host.** Storage and components could not reach it.
  - **The registry inside platform.** Platform is "OS mechanisms ... without policy authority" (CH14:285); a privacy vocabulary is policy.
  - **A CH14 passage successor.** The table is a generated proposal, and the binding list is the reviewed inventory.

### 2. Platform's additions (lead decision; G1, G4, G6)

- **Decision.** Platform gains three mechanisms, in one leg, **O1-p**:
  - **CPU time.** `getrusage(RUSAGE_SELF)`, user plus system time, in `crates/platform/src/clock.rs`, beside the existing clock observations. It feeds `host.phase.completed`'s `cpu` (SOP2:909).
  - **The harness descriptor.** One admission of an inherited write descriptor (S-OP-2b item 4): `fstat` shows a FIFO or a regular file, `fcntl(F_GETFL)` shows it writable, and `fcntl(F_SETFD, FD_CLOEXEC)` keeps it from children. It returns an owned writer. It is a mechanism only; S-OP-2b decides when the host uses it.
  - **`dispose` and `Disposition`** (item 20), in a new `crates/platform/src/disposition.rs`.
- **Why one leg.** Each addition is re-exported from `crates/platform/src/lib.rs`, and that file is in both J3a's and J4a's diffs. O1-a therefore touches no platform file, and O1-p carries every platform change at once.
- **Rejected:** any `unsafe` in operability, including `File::from_raw_fd(3)`. Operability forbids unsafe code, and platform owns OS calls.

### 3. SHA-256 and the keyed path tag (lead decision; G3)

- **The need.** K10's tag is "the first 64 bits of HMAC-SHA-256(*k*, the path's native bytes)" (SOP2:292). No `hmac` crate is locked, so HMAC (RFC 2104) is written in-house. The question is where its SHA-256 comes from.
- **The facts.** Two `sha2`-family crates are locked today, and the workspace has two other SHA-256 sources:

  | Option | Locked? | Admitted for | Effect on operability's edges | Other facts |
  |---|---|---|---|---|
  | (a) identity's `raw_sha256` (`crates/identity/src/lib.rs:31-34`, over `sha2-const-stable`) | `sha2-const-stable` 0.1.0 | `opensip-identity` only (`tools/identity/dependency-policy.json`, subject package `opensip-identity`) | adds operability to identity, and with it identity's external closure: `sha2-const-stable`, `unicode-normalization` (with `tinyvec`), `toml`, `toml_parser`, `toml_datetime`, `serde_spanned` and `winnow` | puts a TOML parser under every emitter |
  | (b) `sha2-const-stable` 0.1.0 directly | yes | identity only; operability would need a policy row | adds one external edge | it contains no `unsafe`, but it does not declare `#![forbid(unsafe_code)]`, so it fails the host policy's selection rule as written |
  | (c) `sha2` 0.11.0 | yes, only as a transitive dependency of `ed25519-dalek` (security) | nobody as a direct dependency | adds `sha2`, `digest` 0.11.3 and their dependencies `block-buffer`, `crypto-common`, `hybrid-array`, `typenum`, `cpufeatures` and `cfg-if` | uses `unsafe` in its SIMD and assembly back ends, so it fails the selection rule |
  | (d) platform's `sha256` (`crates/platform/src/macos_loader.rs:417-430`) | not a crate | crate-private | none | macOS only, through CommonCrypto FFI; AL2023 is in the platform population |
  | (e) **SHA-256 written in-house in `crates/operability/src/hmac.rs`** | no crate | not applicable | **none: the edges stay `{opensip-platform}`** | about 150 lines of FIPS 180-4 under `forbid(unsafe_code)`, and a second SHA-256 in the workspace |

  Options (a), (b) and (c) also add no crate to the lock. Only (e) keeps operability's edges at platform alone, so **(e) is chosen**.
- **Decision.**
  - **The key.** At logging start, *k* is 32 bytes from two `request_entropy()` draws of 16 bytes each. It is held in memory only, never written, never logged, never derived from an identity, and different in every process (SOP2:292).
  - **The tag.** The first 8 bytes of HMAC-SHA-256(*k*, the path's native bytes), as 16 lowercase hex digits. Native bytes come from `OsStrExt::as_bytes`.
  - **The proof is the known-answer tests** (O1-C3), because a defect could leave the tag unkeyed:
    - FIPS 180-4's examples: the empty string, "abc", the 448-bit and 896-bit messages, and one million "a";
    - every length from 0 to 130 bytes, with digests computed by Python's `hashlib` and committed with the test, as identity's own boundary test does (`crates/identity/src/canonical_tests.rs:275`);
    - RFC 4231's HMAC-SHA-256 test cases 1 to 7, including case 5's truncation;
    - SOP2's C-5: tags differ across processes for one path and never equal its SHA-256.
- **Rejected:** (a), because it puts identity's TOML closure under every emitter; (b) and (c), because they fail the host policy's selection rule; (d), because it is macOS only.

## B. Transport

### 4. No `tracing` (lead decision; G3)

- **Decision.** The transport is in-house, as S-OP-2 item 10 permits: "S-OP-2 does not require `tracing` (OPP:147). Whatever transport M3-O picks must keep four rules" (SOP2:394-398). They hold by construction:
  - **(a)** every record is a registry event, because `emit` takes only `registry!` types;
  - **(b)** no `tracing` or `log` callsite exists in the host lock, so none can reach a sink;
  - **(c)** no `log` logger is installed;
  - **(d)** spans are registry entries: the phase events of item 14.
- **The lane check.** `tools/check_operability.py lock` reads the root `Cargo.lock`. It fails if a package named `tracing` or `log`, or any `tracing-*` package, is present, unless a `tools/host/dependency-policy.json` row names it, and a row requires an accepted M3 law. A negative control plants `tracing-core` in a fixture lock.
- **This departs from the M3-O row's wording.** M3P's O1 cell begins "`tracing`, the S-OP-2 vocabulary" (M3P:317), its M3 list says "`tracing` with nonpersistent sinks" (M3P:232), and its logging recommendation is "`tracing` with one host-owned subscriber" (M3P:743). OPP said the same as a proposal (OPP:145, :379). This law departs, as a lead decision, and records it for M3P r11 and OPP's next record (X-O3, X-O4).
- **C-3** (SOP2:940) has no subject while neither crate is locked, so the lock check stands in for it. C-3 becomes a live control if a law ever admits either crate.
- **Rejected:**
  - **Admitting `tracing` by a policy row.** The gap report found that `tracing-core` declares no `#![forbid(unsafe_code)]`; that was not re-checked here, because the crate is not in the local registry. Beyond the policy, every foreign callsite would need `Interest::never()` (SOP2:396), an extra rule to prove, for no capability the registry needs.
  - **The `log` facade,** for the same reasons and rule (c).

### 5. What O1 builds of S-OP-2 (law)

| SOP2 item | What | Unit | Not in O1 |
|---|---|---|---|
| 1 to 3 | the registry, the record shape, names and retirement, `code_tables!`, provenance, templates, and the generated event reference (Markdown and JSON, committed, with a drift test) | O1-a | `generated-contract` tables: O1-c (item 17) |
| 4, 5, 7, 8 | privacy classes; K1 to K15; what is never a field; type-level closure | O1-a | K6's writer (item 18); the owners' mints (item 8) |
| 6 | paths and the keyed tag | O1-a | |
| 9 | scopes and owner-constructed events | O1-a (types) | the real mints (item 8) |
| 10 | foreign events | item 4 | |
| 11 | the guard at every sink | O1-a | |
| 12, 13 | projection and sink rules | O1-a: pre-scope buffer, crash ring (write side), development stderr; O1-b: harness | file (S-OP-1), bundle (S-OP-9), OTLP (S-OP-10), `diagnostics` (S-OP-6), the ring's read path (S-OP-7) |
| 13a | re-admission reader | O1-a | its bundle and doctor uses (S-OP-9) |
| 13b, 13c, 14 | rule E, the wire schema, the full-encoding proof | O1-a | |
| 15 to 17 | admission and queue, pre-scope and ring, commit cells, finalization, loss reasons, marker, gate | O1-a | the file sink's custody and stop rule (S-OP-1) |
| 18 to 22 | the joins | O1-a, through the kinds | provider dispositions are emitted by D3a (item 16) |
| 23 | the initial registry | item 16 | |
| 24 | recording | item 22 | |

- **The stderr sink never takes std's `Stderr` lock** (SOP2:442). It writes through its own duplicate of descriptor 2, made once with std's safe `io::stderr().as_fd().try_clone_to_owned()`. The bootstrap's coded lines keep their ordinary path.
- **The marker** is implemented for every writer-backed sink: the development stderr sink at O1-a and the harness sink at O1-b. So its five outcomes are observable at M3 without S-OP-1 (C-7).

### 6. The compile-refusal harness for C-1 (lead decision)

- **Decision.** C-1 (SOP2:938) uses the pattern law X8 r3 group K already uses in host. Each case under `crates/operability/tests/refusal/cases/` is compiled twice by the pinned `rustc` against a plain `cargo check -p opensip-operability`: once as the lawful control, which must compile, and once with a misuse `--cfg`, which must fail with exactly one error carrying the annotated code, message fragment and line (`crates/host/tests/admission_tests.rs:18-31`). The driver is operability's own test file, so host's `admission_tests.rs`, which J3a holds, is untouched.
- **Rejected:**
  - **Rustdoc `compile_fail`.** It passes on any error, so a case can pass for the wrong reason, which C-1 forbids ("Each must fail for its intended reason", SOP2:934).
  - **`trybuild`.** A new crate.

## C. Scopes and mints (G2)

### 7. Scope types, the capability set and the owner token (lead decision)

- **Scope types.** One type per lawful identity set in SOP2 item 13c's header row (SOP2:541):

  | Scope | Identities |
  |---|---|
  | request | RequestId |
  | project | + ProjectId |
  | plan | + ProjectId, PlanId |
  | attempt | + ProjectId, ExecutionId |
  | plan attempt | + ProjectId, PlanId, ExecutionId |
  | committed Run | + ProjectId, PlanId, ExecutionId, RunId (a `Committed` publish) |
  | stored Run | + ProjectId, RunId (a stored-Run read) |

  Each implements the sealed markers `HasProject`, `HasPlan`, `HasExecution` and `HasRun` it holds. `emit::<E>` is bounded by `E::Requires` (SOP2 item 9).
- **How a scope or a P1 or P2 kind is made.** Only in one of SOP2 item 8's two ways (SOP2:357-361):
  - **(a) a `From` impl from the owning typed value,** where operability can name that type. Only platform's types qualify, because platform is operability's only dependency;
  - **(b) a mint from the one-time capability set,** everywhere else. Most owning types live in host, storage, identity or evaluator, which operability cannot name.
- **The capability set.** `start(constants)` returns the runtime and the capability set **once per process**. A process-wide atomic refuses a second call, which returns nothing. Its members:
  - identity mints: request, project, plan, execution, committed Run and stored Run;
  - kind mints for K5, K9, K10, K11 (a spawned child's pid), K12, K13, K14 and K15;
  - **the storage owner token** for the two `owned(storage)` events (SOP2:383-387).

  A mint's method takes the identity's fixed-width value (16 bytes for `req1_` and `exec1_`, 32 bytes for `prj1-`, `plan2:` and `run3:`) or the kind's grammar-checked value. **The mint is the provenance, not its argument.** No public constructor of a P1 or P2 kind or of an identity takes text, bytes or a parsed value (SOP2:988). Each mint's call sites are listed in the checker's mint list, and C-2's "the constructor and mint list equals the audited exception list" checks the list (SOP2:939).
- **Distribution.** The bootstrap receives the set from `start` and hands each mint to its owner. At O1-a no owner is wired, so host holds the whole set and uses none of it (item 8).
- **The storage owner token.** It builds `storage.commit.published` only from a committed-Run scope, and `storage.commit.not_published` only through an attempt scope. Operability cannot name `PublishedCommit`, so "built only from `PublishedCommit`" (SOP2:384) is held on storage's side: the committed-Run mint and the token are held only by storage's publish path, which holds the receipt. The wiring unit's source pin proves it (item 8).
- **Test-only mints.** A `test-mints` feature, never a default, enabled only from `[dev-dependencies]` tables (storage's `scenario-fixtures` pattern), refused in any build without debug assertions; and `cfg(test)` inside operability. No test mint exists in a featureless build (O1-C7).
- **Rejected:**
  - **A public constructor** from bytes or text, even one that validates the grammar. It is a shape check, not provenance (SOP2:367).
  - **A run-time phase check** (SOP2:390).

### 8. Who wires each mint (lead decision)

**No record carries an identity until its owner has wired the mint.** Every record carries a RequestId (SOP2:540), so **no production record exists until the RequestId scope is wired.** O1-a ships the whole path, tested with test mints, and emits nothing in production. Finalization still runs, over empty tallies (item 11).

| Identity or kind | Owner | Wiring unit | Form |
|---|---|---|---|
| RequestId | J3a's `RequestIdentity` (platform, in J3a's candidate) | **J3a.** J3a's candidate (inventory v139) was built without O1-a. If J3a integrates first, its wiring is a short follow-up leg on J3a's line, **J3a-o**; if O1-a integrates first, J3a takes it in its rebase. The metadata host's `RequestAuthority` (`request.rs:18-55`) is wired in the same leg. | (a) `From<&RequestIdentity>` |
| ExecutionId | J3a's reserved ExecutionId (platform) | J3a, or J3a-o as above | (a) `From` the reserved value |
| ProjectId | project admission | J2b or J3d | mint |
| PlanId | Plan sealing | J2b or J3d | mint |
| attempt and plan-attempt scopes | attempt admission | J2b or J3d | built from the two above |
| committed RunId and the storage owner token | storage's `publish` (`commit.rs:66-75`) | **X3c-3 or J3d.** X3c-3 is in flight without O1-a, so J3d is expected. | mint and token |
| stored-Run read | `query` and `inspect` | the unit that implements stored-Run reads | mint |
| K11, a spawned child's pid | D1a's spawn handle (platform) | D3a | (a) `From` the handle |
| K5, K9, K10, K12 to K15 | catalog, identity, path-handle, discovery, snapshot, admission, policy and manifest owners | the first unit that emits each | mint |

- **Each wiring unit carries its legs of C-1 and C-8** that need its owner's types: a RunId from a candidate, an Execution-requiring event before admission, `storage.commit.published` without the receipt (SOP2:938, :945).
- **Rejected:** O1 minting identities it does not own. That is the forgery S-OP-2 item 9 forbids.

## D. Sinks at M3 (G5)

### 9. Production constants (lead decision)

| Setting | Featureless build (production) | `operability-dev-sinks` | `harness-instrumentation` (O1-b) |
|---|---|---|---|
| file sink | off: never admitted before S-OP-1 | off | off |
| stderr sink | off | on, level `debug`, human form | off |
| pre-scope buffer | on: 64 KiB, 256 records (SOP2:629) | on | on |
| crash ring | on: 64 KiB, 256 records, at or above `info` (SOP2:633, :446) | on | on |
| harness sink | absent | absent | on, level `info`, descriptor 3 (S-OP-2b) |
| level for file projections | `info` (OPP:160) | `info` | `info` |

- **They are release constants** in `constants.rs`. No environment variable, flag or configuration value selects a sink, a level or a bound (SOP2 item 21).
- **What follows in production, and it is intended.**
  - Every file projection goes to the pre-scope buffer, because the file sink is never admitted. At the freeze it is `unpersisted` (SOP2:632, :722), or `prescope-full` if the buffer filled first.
  - The ring holds P0 and P1 copies, and nothing reads it until S-OP-7.
  - No writer thread runs, and operability writes no byte to descriptors 1, 2 or 3.
- **Rejected:** stderr on in production now. Its switches are S-OP-6's, and until then "the stderr sink and timings exist only in development and harness builds" (OPP:226).

### 10. The development stderr sink (lead decision)

- **Decision.** A feature `operability-dev-sinks`:
  - never a default and never enabled from a `[dependencies]` table. `apps/cli` and host only forward it, so it is reached only by an explicit `--features`;
  - refused at compile time in any build without debug assertions, exactly as platform refuses `crash-matrix` (`crates/platform/src/lib.rs:5-8`);
  - its stderr sink runs at the fixed level `debug`, in the human form (SOP2 item 13), through its own descriptor (item 5).
- **Release absence.** `tools/check_operability.py release-absence --binary target/release/opensip` fails if the development sink's or the harness sink's marker string occurs in a featureless release binary, as X9's check does (`tools/check_crash_matrix.py:517`).
- **Rejected:** stderr on in every build with debug assertions. Every debug test's stderr would change, and selection would come from the build profile rather than a stated constant.

### 11. Finalization at the existing termination points (lead decision)

- **Decision.** One finalization per invocation, by SOP2 item 16's steps 1 to 5 (SOP2:652-682), at the point where the command's result is decided and before the envelope is rendered (SOP2:652).
  - **Where, at `b7b87b7`.** The metadata host's `execute`, `doctor` and `delivery_failure` paths (`crates/host/src/outcomes.rs:52-96`; `doctor_ingress.rs:29`) finalize before they project. Each return in `bootstrap.rs` (`:38`, `:41`, `:47`, `:53`, `:56`, `:59`) calls the same finalization as a backstop, which does nothing once the summary is frozen.
  - **The allocation-failure return** (`bootstrap.rs:15-23`) starts no runtime and finalizes nothing. The fixed line stays the only output (OPP:158; SOP2:382).
  - Each later command path (J2c, J3d) finalizes at its own decision point, under the same rule.
- **Step 6 waits for S-OP-6.** The frozen summary is kept in memory and is readable by tests through a test-only accessor. It is rendered nowhere. The envelope's bytes are those of a build without operability (C-11).
- **Rejected:** OPP's example line, "operational log incomplete: 412 records dropped (queue full)" (OPP:201). It is user-visible text without its law (S-OP-6), and at M3 it would report `unpersisted`, which is policy, to users as loss.

### 12. Logging-start failure (lead decision)

- **Decision.** `start` runs after the RequestId is allocated, so an entropy failure for the RequestId still gives the existing fixed line. If `start` then fails, for example on a key draw, logging is disabled for the process:
  - no record is constructed and no sink exists;
  - no summary is frozen;
  - host keeps a typed `LoggingUnavailable` outcome for S-OP-6 to disclose;
  - the command's result, exit code and envelope are unchanged (C-11).
- **Rejected:**
  - **Starting without the path key.** Records with K10 fields would become unbuildable mid-command, which is silent loss.
  - **Failing the command.** Optional observability never changes an outcome (OPP §5.2).

## E. The operational record and the harness (G4)

### 13. The harness sink, under S-OP-2b (lead decision)

- **Decision.** A harness-only instrumentation sink carries the operational record to the harness at M3. Its law is the owed successor **S-OP-2b**, whose exact text is below. In short:
  - feature `harness-instrumentation`, never a default, refused in any build without debug assertions, and absent from release binaries;
  - inherited descriptor 3, admitted once at logging start and kept from every child;
  - JSON lines, class ceiling P0 and P1, fixed level `info`;
  - the stream's first record is `log.stream.opened` with `sink: harness`;
  - **`recordSha256`** in the exploratory envelope (ENV `operationalRecords[].recordSha256`) is the SHA-256 of the exact bytes the harness driver read from descriptor 3 for that invocation. The host computes nothing for it;
  - the harness reads the stream only through SOP2 item 13a's reader.
- **The measured build.** Q6 measures the build that carries the record (Q0:951, "Instrumentation stays at the same preregistered setting"). With this decision the measured host is built with debug assertions on. O1-b adds a Cargo profile, `harness`, that inherits `release` and sets `debug-assertions = true` and `overflow-checks = false`, so the measured code is optimized. At `b7b87b7` production code has 9 `debug_assert!` sites and no other `cfg(debug_assertions)` branch beyond the feature refusals. Open question Q1 asks Q0's owner to confirm.
- **Rejected:** gating phase timings on S-OP-1's file sink and accepting `record-missing` until then. M3-M's exploratory report needs phase timings at M3 (M3P:316).

### 14. The phase vocabulary (lead decision)

- **The `Phase` header table** (`registry-literal`, at most 32 bytes per member; registered by O1-a, because the record header uses it). Members follow OPP's §4.1 phrases (OPP:246) under a root `request`, and each member's parent is fixed:

  | Member | Parent | OPP §4.1 phrase |
  |---|---|---|
  | `request` | none (root) | the whole request |
  | `discovery` | `request` | discovery |
  | `snapshot` | `request` | snapshot and sealing |
  | `plan` | `request` | plan |
  | `provider` | `request` | each provider |
  | `provider.start` | `provider` | start |
  | `provider.analysis` | `provider` | analysis |
  | `provider.teardown` | `provider` | teardown |
  | `admission` | `request` | admission and replay |
  | `evaluation` | `request` | evaluation |
  | `commit` | `request` | commit |
  | `delivery` | `request` | delivery |
  | `reuse` | `request` | cache and reuse decisions |

- **The `PhaseOutcome` table** (`registry-literal`; registered by O1-b). S-OP-2 names the table but not its members (SOP2:870). Members: `completed`, `failed`, `cancelled` and **`not-applicable`**.
- **Two events** (ordinary registrations by O1-b; SOP2:226-230):

  | Event | Level | Requires | Fields | Export |
  |---|---|---|---|---|
  | **`host.phase.started`** (new) | info | none | `phase` K1 (Phase); `parent` K1 (Phase), absent only for `request`; `at` K2 `Elapsed` | no |
  | **`host.phase.completed`** | info | none | as SOP2:870: `phase` K1 (Phase), `wall` K2 `Elapsed`, `cpu` K2 `Elapsed`, `outcome` K1 (PhaseOutcome); **plus `at` K2 `Elapsed`** | cand. |

- **The rules.**
  - **`at`** is monotonic nanoseconds from request start, the instant the request scope was created. It is K2 `Elapsed` (SOP2:270).
  - **A phase that runs** emits `started`, then `completed`, with the same `phase` and the same `component` header. `wall` equals `completed.at` minus `started.at`, and `cpu` is this process's user plus system CPU over the phase (item 2; SOP2:909).
  - **A phase that does not run** emits only `completed`, with `not-applicable`, `wall` 0, `cpu` 0, and `at` set when the host decided it.
  - **Provider phases** carry their provider's `component` slot, so the harness pairs them by phase and component.
  - **`request`** starts at `at` 0 and completes just before finalization's cutoff, so it lies inside the frozen record.
  - A record whose `parent` differs from the table is invalid, and the harness treats it as `record-invalid` (Q0:951).
- **What Q0 checks then has a subject** (Q0:946-951): every phase present or `not-applicable`; nesting by `parent` and by interval; monotonic `at` within each span; unattributed time as elapsed minus the `wall` of `request`'s children.
- **Rejected:**
  - **Free-form phase names.** SOP2 item 3 requires a registered table.
  - **Nesting by emission order alone.** Records from several threads interleave.

### 15. Who emits which phase (record)

O1-b provides the span API and emits `request` and the metadata path's `delivery`. Every other phase is emitted by its owner when that owner integrates:

| Phase | Emitter |
|---|---|
| `discovery` | B's units |
| `snapshot` | C's units |
| `plan` | C4a |
| `provider`, `provider.*` | D3a, once L is in effect |
| `admission` | H5 |
| `evaluation`, `reuse` | J2b |
| `commit` | J3d |
| `delivery` (analysis paths) | J2c, J3d |

Until an owner wires its phase, the phase is absent, and Q0 reports `phase-missing` (Q0:951). Nothing is synthesized.

## F. Registrations

### 16. Who registers which event (lead decision)

- **The rule.** An event is registered by the unit that first emits it, under SOP2 item 23's exact name and fields, as an ordinary registration reviewed in that unit (SOP2:226-230). O1's units register their own events, J-RW's event and the phase events.

  | Events | Registered by | Tables | Emitted |
  |---|---|---|---|
  | `log.stream.opened`, `log.loss.counted` | O1-a | `Platform`, `BuildProfile`, `Sink` (`file`, `stderr`; `harness` by S-OP-2b), `LossCell` (the frozen map of 8 reasons by 5 levels), `IoErrorKind` | by O1's own sinks |
  | `storage.commit.published`, `storage.commit.not_published` (owner-constructed) | O1-a | `CommitNotPublished`; `not_published`'s optional `termination` field is added by O1-c with its generated table | once storage's wiring lands (item 8) |
  | **`host.repair.completed`** (JRW item 7) | O1-a | `RepairKind`, 7 members: `registration`, `store-directory`, `ledger-file`, `ledger-schema`, `carrier-floors`, `trust-directory`, `trust-dependency`. `RepairState`, 14 members: `RW-R1` to `RW-R7`, `RW-P1` to `RW-P3`, `RW-L1`, `RW-T1` to `RW-T3` (JRW:423-436) | by host, from J4's typed completion results, in the first J4 unit after O1-a (JRW:496) |
  | `host.phase.started`, `host.phase.completed` | O1-b | `Phase` (O1-a), `PhaseOutcome` | item 15 |
  | `host.termination.decided`, `config.value.resolved` | O1-c | `generated-contract` tables (item 17) | at the termination decision; by the resolver |
  | the 8 `provider.*` and 6 `supervision.*` events of SOP2 item 23, and D3's own additions | **D3a** | D3's `registry-literal` tables (`TeardownCause`, `LimitKind`, `LimitUnit`, `BoundedWait`, `ForceTrigger`; MD:695) and the `protocol-enum` tables of SOP2 item 22 | provider and supervision events only once L is in effect |
  | `host.request.parsed`, `host.settings.resolved`, `host.signal.received`, `host.reuse.disclosed`, `discovery.path.skipped`, `snapshot.seal.completed` | the first unit that emits each | as SOP2 item 23 names them | |

- **`host.repair.completed`** is level `info`, requires no identity beyond the RequestId, carries no path, ProjectId or bytes (JRW:495), and is not an export candidate. Security returns each completion in its typed result, and host emits the record, so security gains no edge.
- **D3a's additions** are `supervision.teardown.started`, `supervision.tree.swept`, `supervision.scratch.retained`, `supervision.settled`, and **`tool.process.spawned` and `tool.process.reaped`**, which require Project only (MD:687-693). **`tool` is a new domain.** Adding a domain is an ordinary registration (SOP2:228), so it needs no successor.
- **M3-L's events.** The provider-boundary record uses 11 registered events (ML item 14), all of them D3a's registrations here. They are emitted only once L is in effect. D3a waits for L in effect anyway (MD "Units after the law").
- **Sequencing.** D3a and O1-b both edit `registry.rs`. Whichever integrates second rebases.
- **Rejected:** O1-a registering all 27 initial events now. It would fix D3's table members before D3a, giving them a second owner, and it would register events no test can emit.

### 17. The termination and configuration tables, after E2s (lead decision; G7)

- **The need.** `host.termination.decided` (`class`, `exit`, `reason` D9 code, `detail` DomainDetail code) and `config.value.resolved` (`key`, `layer`, `choice`) use `generated-contract` tables (SOP2:216, :872, :874). Such a table records the sha256 of the generated module's reviewed bytes, and its members must be literal.
- **The facts.** D9 and DomainDetail codes are serde enums in `crates/contracts/src/generated/evidence.rs` today (for example `Common1D9ErrorCode` at `:821` and `Common3DomainDetailCode` at `:6262`), not literal `&[&str]` tables. E2s, in flight, is regenerating `evidence.rs` and `identity.rs` and moving the generator's closure pins (`tools/contracts/generator-closure.json`).
- **Decision.** **O1-c**, after E2s integrates:
  1. **A contracts-generator change** emits, beside each closed code enum it already generates, a literal `pub const` table of its members in schema order, plus the configuration keys and enum values the resolver uses. It moves generator pins, so it is reviewed as its own generator successor inside O1-c, in F8b's pattern.
  2. **The registrations:** both events, and `storage.commit.not_published`'s optional `termination` field. Each table's descriptor records the reviewed module's sha256.
  3. **The emission** of `host.termination.decided` at the termination decision, before the freeze.
- **Rejected:**
  - **Hand-copied D9 lists as `registry-literal` tables.** A second source of D9 truth, which SOP2 item 3 rules out.
  - **Registering before E2s.** The pinned bytes would change under it.

### 18. The K6 code-location census, deferred (lead decision; G8)

- **Decision.** No initial event uses K6. Only S-OP-7's crash path needs it (SOP2:274, :1026-1030). O1-a gives K6 its wire spelling and its read-back predicate with an **empty retained census**, so a persisted K6 `file` other than `external` is always dropped (SOP2:483). K6 has **no writer constructor** in O1. S-OP-7's unit chooses the census mechanism, adds the constructor, and carries C-9.
- **Rejected:** choosing a census now. No O1 consumer would test it.

## G. Enforcement (G6)

### 19. The source-scan checker and its exception list (lead decision)

- **The tool.** `tools/check_operability.py source --repository .`, standard library only, read-only. It scans every `.rs` file under `crates/` and `apps/` except test-only paths.
- **The classes** (closed; checker constants), with OPP §7's owners (OPP:363-370):

  | Class | Patterns | Owners that may hold an exception |
  |---|---|---|
  | stdio | `print!`, `println!`, `eprint!`, `eprintln!`, `dbg!`, `io::stdout(`, `io::stderr(`, `libc::write(` | output and terminal, termination, crash path, operability's development sink |
  | environment | `env::var(`, `env::var_os(`, `env::vars(`, `env::vars_os(` | the configuration resolver; platform owners that read process state |
  | process | `Command::new(`, `process::Command`, `process::exit(`, `process::abort(`, `libc::_exit(`, `libc::abort(` | supervision; platform custody owners; termination; crash path |
  | swallowed | `let _ =` | none for long: each moves to `dispose` in O1-S |
  | disposition | `Disposition::TestOnly` outside a test-only file; `Disposition::ShutdownPath` outside the listed termination files | not applicable |

- **The exception list,** `tools/operability/exceptions.json`. One row per (path, class), with the exact count at the commit O1-a integrates on, and the owner class.
  - A file's count must equal its row. A larger count fails. A smaller count also fails until the row is lowered in the same change, so the list only ratchets down.
  - A file with an occurrence and no row fails.
  - Rows are sorted. No product source file changes for the list.
- **Tests are out of scope (decision).** Test-only paths (`*/tests/**`, `*_tests.rs`, `*/benches/**`) are not scanned. Tests are not product behaviour: they print, spawn helper processes and read their fixtures' environment by design, and 166 of the 306 `let _ =` lines are in test-only files. Inline `#[cfg(test)]` modules inside production files *are* counted, because the scan reads text, not `cfg`. They sit in the counts until O1-S's clippy lints, which do see `cfg`, replace the text counts for stdio and environment.
- **The same tool** carries the lock check (item 4) and the release-absence check (item 10).
- **Negative controls** (`tools/tests/test_check_operability.py`), each on a scratch copy of a small fixture tree, each failing for its named reason:
  - a planted direct stderr write, an ambient environment read, a raw spawn and a `process::exit`;
  - a new `let _ =`;
  - a false disposition: `Disposition::TestOnly` in a production path, and `Disposition::ShutdownPath` outside the termination files;
  - a count above its row, a count below its row, and an occurrence with no row;
  - `tracing-core` in a fixture lock;
  - a development-sink marker in a fixture release binary.

  OPP §7's other two controls, an unregistered event and a dynamic event name, are compile-refusal cases (item 6), because no API accepts a name.
- **Rejected:**
  - **Clippy lints now.** They need per-crate manifest edits in files J3a, J4a and X3c-3 hold (item 21).
  - **Scanning tests.** Churn across in-flight units' test files for no product property.
  - **A Rust parser in the checker** to skip `cfg(test)`. It is fragile, and clippy does it properly in O1-S.

### 20. The `dispose` helper (lead decision)

- **Decision.** `dispose(result, why: Disposition)` consumes a `Result` and does nothing else: no record, no I/O and no allocation. `Disposition` is closed:

  | Member | Meaning | Checker rule |
  |---|---|---|
  | `BestEffortCleanup` | cleanup after the outcome is decided; its failure changes no result | none |
  | `AlreadyReported` | the failure is already carried by a typed result or a record | none |
  | `ShutdownPath` | on the termination or crash path, where nothing more can be reported | only in the listed termination files |
  | `TestOnly` | test-support code compiled only under a test `cfg` or a test-only feature | only in test-only files or listed test-support modules |
  | `Infallible` | the callee cannot fail for this receiver, for example `fmt::Write` into a `String` | none |

- **Placement: platform**, in `crates/platform/src/disposition.rs`, delivered by O1-p. 126 of the 140 production `let _ =` lines are in platform (56) and security (70), and neither can depend on operability. Operability re-exports it. It is a code annotation, not policy authority. CH14-O lists the file.
- **Rejected:**
  - **In operability.** Unreachable from platform and security.
  - **A copy per crate.** Five copies of one closed enum.
  - **In contracts.** Contracts holds generated inert carriers (`crates/contracts/src/lib.rs:1-3`).

### 21. The sweep, O1-S (lead decision)

- **Decision.** O1-S runs after J3a, J4a and X3c-3 integrate, because their files hold most sites: security's custody, `private_access.rs` and `journal_store`, storage's ledger and commit files, and platform's `filesystem.rs`, `lib.rs` and `crash_barrier.rs`.
  - **Per-crate lints** under `[lints.clippy]` in each crate's own `Cargo.toml`, with explicit values, because `check_package_edges.py` refuses inherited workspace values (`tools/check_package_edges.py:25-31`): `print_stdout`, `print_stderr`, `dbg_macro`, `disallowed_methods` and `let_underscore_must_use`. A workspace `clippy.toml` lists the disallowed methods: `std::env::var`, `var_os`, `vars`, `vars_os`, `std::process::Command::new`, `std::process::exit` and `std::process::abort`. Each audited site gets an `#[allow(...)]` naming its owner, matching the exception list.
  - **The migration.** Every production `let _ =` on a `Result` becomes `dispose(...)` with its member. The exception list's counts fall to the audited residue.
  - **Library and binary targets only.** Test targets stay out of scope (item 19).
  - **X9's `crash_barrier.rs`** keeps its exit sites as the crash path's lawful sites. O1-S lists them and changes no barrier code.
  - **The TypeScript provider's bans** (`console`, `process.env`, `child_process` and `fs` outside the SDK; OPP:369) go to the TypeScript provider's units, from F1, not to O1.
- **Rejected:** sweeping in O1-a. It would edit files J3a, J4a and X3c-3 hold while they are in flight.

## H. Recording S-OP-2 (G9)

### 22. Two design units (lead decision)

- **The finding.** SOP2 item 24 records S-OP-2 as one verify_design successor with two insertion-only overrides, of SDK4 `/standardizedFamilies/1/rule` and DRC line 576 (SOP2:917-930). Neither parent is in the design the lock selects at `b7b87b7`:
  - neither is a file of the source manifest (`candidate-subject.v45.json`) or of the application manifest (`application-subject.v46.json`);
  - neither is a candidate of any of the 101 bound contract successors.

  APP pins both, at `/rows/12/inheritedContract` and `/evidenceTargets/D.SDK/sources/0`, without carrying their bytes. VD refuses a parent outside the accepted set ("contract parent is not an accepted base or selected inventory"), and a unit cannot select and override the same file. So item 24's one record cannot bind.
- **The lock check.** No bound record names SDK4 or DRC in any override or supersession. Both entries are plain overrides, and VD2 supersession (the SD-7, REG v3, CRC-2 and SD-8 form) does not apply.
- **Decision.** Two design units, in `docs/implementation/m3/operability/s-op-2/`, reviewed in this request:
  - **S-OP-2-P** selects the exact SDK4 and DRC bytes that APP pins, at their own paths, with APP as its only parent and no override. This is `control-source-v1`'s form, which selected the existing, unselected `control-completion.schema.v3.json`. Selection binds bytes only.
  - **S-OP-2-R** is item 24's recording: it pins `PROPOSAL-r6.md`'s accepted bytes as a candidate and makes the two insertion-only overrides, with item 24's sentences character for character.

  Both reviews list `"supersededPassages": []`. Both units bind before, or with, O1-a's integration, S-OP-2-P first.
- **The local binding check** ran in a throwaway detached worktree of product main `b7b87b7`, with a private 0700 TMPDIR, in Python only, serving SCRATCH review and assent pins from memory as CRC-2's check did. The worktree was then removed. The request pins the output. S-OP-2-R alone refuses with exactly that message. S-OP-2-P alone, and S-OP-2-P then S-OP-2-R, pass with and without the implementation check, and leave everything outside the contract chain equal to the baseline. Nine refusal probes refuse, or pass, as expected.
- **Rejected:**
  - **One unit.** It cannot bind.
  - **Complete copies of SDK4 and DRC carrying the insertions.** Item 24 asks for insertion-only overrides, and a copy leaves two texts for each document.
  - **Overriding F02:193-197 instead.** Item 24 rules it out (SOP2:928).

## I. Controls

**S-OP-2's controls, by unit** (SOP2:936-949). Each must fail for its intended reason.

| Control | O1 unit | Legs elsewhere |
|---|---|---|
| C-1 compile refusals | O1-a (item 6) | owners' type legs: J3a-o, J3d (item 8) |
| C-2 registry integrity | O1-a | `generated-contract` legs: O1-c |
| C-3 foreign events | item 4's lock check stands in | live only if a law admits `tracing` or `log` |
| C-4 canaries and re-admission | O1-a: every kind, the reader, the stderr, ring and pre-scope sinks; O1-b: the harness sink | file (S-OP-1), bundle (S-OP-9), OTLP (S-OP-10), crash file (S-OP-7); provider stderr (D3a); K6 legs (S-OP-7) |
| C-5 rule E | O1-a | |
| C-6 the guard | O1-a | |
| C-7 bounds, gate, finalization | O1-a, with the development stderr sink and a test-only stand-in for the file sink's writer, so the pre-scope handoff legs run; O1-b repeats the writer legs on the harness sink | the real file sink: S-OP-1 |
| C-8 run-time identities | O1-a with test mints | real legs with each wiring unit (item 8) |
| C-9 code locations | none | S-OP-7 (item 18) |
| C-10 environment | O1-a | |
| C-11 invariance | O1-a: logging off and on, sink failure, start failure | each later unit extends it |
| C-12 provider dispositions | none | D3a and D5 |

**O1's own controls.**

| ID | Control | Item | Unit |
|---|---|---|---|
| **O1-C1** | `crates/operability` forbids unsafe code; its manifest edges are exactly `{opensip-platform}`; `check_package_edges.py` passes on the inventory successor; host declares the edge; storage and components are only permitted. | 1 | O1-a |
| **O1-C2** | The lock check fails on `tracing`, `tracing-*` or `log` without a policy row, and passes on the real lock. | 4 | O1-a |
| **O1-C3** | SHA-256 and HMAC-SHA-256 known-answer tests (item 3); the tag is the first 8 bytes of the HMAC in lowercase hex. | 3 | O1-a |
| **O1-C4** | `cargo check --release` with each of `operability-dev-sinks`, `harness-instrumentation` and `test-mints` fails with its refusal text; `release-absence` passes on a featureless release binary. | 7, 10, 13 | O1-a, O1-b |
| **O1-C5** | A featureless build writes no byte to descriptors 1, 2 or 3 from operability and starts no writer thread; every file projection ends `unpersisted` or `prescope-full`; the frozen summary exists and is rendered nowhere; envelope bytes equal those with logging disabled. | 9, 11 | O1-a |
| **O1-C6** | Exactly one freeze per invocation on each termination path (metadata, doctor, delivery failure, output failure); the allocation-failure path starts nothing; an emission after the freeze goes only to the post-freeze tally. | 11 | O1-a |
| **O1-C7** | A second `start` refuses; no test mint exists in a featureless build; each mint's call sites equal the checker's mint list; no scope or P1 or P2 kind can be built without a mint or its platform `From` (compile refusals). | 7 | O1-a |
| **O1-C8** | The checker's negative controls (item 19). | 19 | O1-a |
| **O1-C9** | The harness sink: S-OP-2b's C-13; phases nest by the fixed parents; `at` is monotonic within each span; `not-applicable` rows carry zero `wall` and `cpu`; `cpu` comes from `getrusage`. | 13, 14 | O1-b |
| **O1-C10** | Each `generated-contract` table equals its generated module's members, and its descriptor's sha256 equals the module's reviewed bytes; a changed module refuses registration; `host.termination.decided` is emitted once, before the freeze, with the decided class and exit. | 17 | O1-c |
| **O1-C11** | `dispose` compiles to nothing observable; the checker's `TestOnly` and `ShutdownPath` rules hold on the real tree. | 20 | O1-p |
| **O1-C12** | The CPU-time call is non-decreasing across calls and returns a typed error on failure; the descriptor admission refuses a closed descriptor, a read-only one and a directory, and sets close-on-exec. | 2 | O1-p |

## J. Units

### 23. Units

**Files in flight on 2026-10-04,** read in each worktree with `git status`. While a unit is in flight, no O1 unit edits its files:
- **J3a** (candidate v139): `crates/host/src/request.rs`, `crates/host/tests/admission_tests.rs`, new `crates/host/tests/refusal/cases/platform_*` and `security_commit_session_open_reserved.rs`, `crates/platform/src/lib.rs`, `crates/platform/src/crash_barrier.rs`, `crates/security/src/initial_installation.rs`, and twelve files under `crates/security/src/custody/`, among them `commit_session.rs`, `installation_routing.rs`, `installation_stage.rs`, `ordinary_writer.rs` and `read_premise.rs`.
- **J4a** (accepted, integration held for X3c-3 and X9 r17's §RW): `crates/platform/src/lib.rs`, `filesystem.rs` and `filesystem/file_effects.rs`; `crates/security/src/lib.rs`, `private_access.rs`, `store_custody.rs` and three `journal_store/carrier_*` files; `crates/storage/src/ledger_store/project_ledger.rs` and its tests.
- **X3c-3**: `crates/storage/src/commit.rs`, `commit_tests.rs`, `ledger_store.rs`, `ledger_store/project_commit.rs` and its tests, `ledger_store/recovery_material.rs`, `recover_tests.rs`, `tests/commit_tests.rs`, `tests/fixtures/crash-matrix/required-runs.v1.json`; `tools/check_crash_matrix.py` and its test.
- **E2s**: `crates/contracts/src/generated/{evidence,identity}.rs`; six evaluator registries, `coverage.rs` and `execution_inputs.rs`; `crates/host/src/schema_sources.rs`; `crates/identity/src/schema_registry.rs`; the generated TypeScript in `providers/typescript` and `apps/report`; `schemas/**`; `tools/contracts/{dependency-policy,generator-closure}.json`; `tools/identity/dependency-policy.json`.
- **Every inventory unit** appends to `design-lock.json` and the linear inventory chain. Each O1 unit's inventory number is assigned at launch after a `git ls-files` check; v139 is J3a's.

| Unit | Content | Controls | Depends on | Size | Must not touch while J3a, J4a, X3c-3 or E2s is in flight |
|---|---|---|---|---|---|
| **O1-a** | `crates/operability` (items 1, 3, 5 to 7, 9 to 12, O1-a's rows of 16, 18); the workspace member and its `Cargo.lock` entry; host's edge, the capability set held by the metadata host, finalization in `outcomes.rs` and `doctor_ingress.rs` with the bootstrap backstops; feature forwarding in host and `apps/cli`; `tools/check_operability.py`, `tools/operability/exceptions.json`, `tools/tests/test_check_operability.py` and a `tools/README.md` section; the inventory successor | C-1, C-2, C-4 to C-8, C-10, C-11 (O1-a legs); O1-C1 to O1-C8 | P0 (met); S-OP-2 r6 (accepted); this law. S-OP-2-P and S-OP-2-R bound before or with its integration | L (3 days) | every platform file (O1-p's); `request.rs` and `admission_tests.rs` (J3a); every storage and security file; generated contracts, `schemas/**`, `tools/contracts/**`, `tools/identity/**` (E2s); `tools/check_crash_matrix.py` (X3c-3) |
| **O1-p** | platform: CPU time in `clock.rs`; the harness-descriptor admission; `disposition.rs`; the `mod` and `pub use` lines in `lib.rs`; operability's re-export of `dispose` | O1-C11, O1-C12 | J3a integrated (it holds `lib.rs`); J4a: open question Q2 | S (1 day) | `lib.rs` until J3a integrates; `filesystem.rs` and `filesystem/file_effects.rs` (J4a); `crash_barrier.rs` (J3a, X9) |
| **O1-b** | the harness sink under S-OP-2b; `PhaseOutcome`, `host.phase.started` and `host.phase.completed`; the span API; host's `request` and metadata `delivery` phases; the `harness` Cargo profile; feature forwarding; the harness marker in `release-absence` | O1-C4 (its feature), O1-C9; C-4 and C-7 legs on the harness sink | O1-a; O1-p; **S-OP-2b accepted and bound**; the RequestId scope wired (J3a or J3a-o) | M (2 days) | as O1-a; `registry.rs` is shared with D3a, so the second to integrate rebases |
| **O1-c** | the contracts-generator change and its own generator review; the regenerated modules; `host.termination.decided`, `config.value.resolved` and `not_published`'s `termination` field; the termination emission | C-2's generated legs; O1-C10 | O1-a; **E2s integrated** | M (2 days) | it starts only after E2s; until then, every E2s file |
| **O1-S** | the sweep (item 21): per-crate lints, `clippy.toml`, the `dispose` migration, the lowered exception list | O1-C8 rerun on the swept tree; clippy on the lanes' feature sets | O1-a; O1-p; **J3a, J4a and X3c-3 integrated** | M (2 days) | it starts only after all three; then any unit in flight at its start |

- **Review.** Each unit is reviewed `ACCEPT-UNIT`; units that add files carry an inventory successor with an `inventoryCandidateAssessment`. O1-c's generator change is also a generator successor (item 17).
- **Effect on M3P** (M3P:556, :531): M3P sized O1 at 4 days, and D3a needs S-OP-2's registry by day 5. **O1-a's 3 days meet that.** O1-p, O1-b, O1-c and O1-S are off the host chain. O1-b gates M3-M's phase timings (M3P:316). J3d needs O1-a and O1-b (M3P:313 lists "O1" among J3d's waits). M3-X needs every O1 unit (M3P:319).
- **New dependency edges** for M3P r11: D3a on O1-a; J3d on O1-a and O1-b; M3-M on O1-b; O1-b on J3a or J3a-o and on S-OP-2b; O1-c on E2s; O1-S on J3a, J4a and X3c-3.

---

## Cross-law items

Each item names the law or record that must change. None blocks this law's acceptance. Item 23 says which unit each one holds.

- **X-O1. S-OP-2b,** the harness instrumentation sink. An owed contract successor to S-OP-2 r6. Its exact text is the next section. The lead drafts it as its own design unit next; it is not drafted as a unit here. It gates O1-b.
- **X-O2. CH14-O** (record, at the next CH14 refresh). Add the `opensip-operability` package row (`crates/operability/`, "Safe operational records: the event registry, typed fields, sinks and loss accounting", dependency `opensip-platform`); add `opensip-operability` to host's, storage's and components' proposed direct dependencies; add `crates/platform/src/disposition.rs` under platform (item 1).
- **X-O3. M3-PLAN r11** (record). The M3-O row: the in-house transport replaces "`tracing`" (M3P:317, :232, :743); O1's units and edges from item 23; J3a-o; S-OP-2-P and S-OP-2-R; S-OP-2b among the law rounds before O1-b.
- **X-O4. OPP's next record.** §3.1's framework line and §8's M3 row (OPP:145, :379) now read "the in-house transport (M3-O1 item 4)"; §4.1's M3 carrier (OPP:248) is S-OP-2b's harness sink, beside the file sink once S-OP-1 lands.
- **X-O5. M3-D's next record.** Item 21's provider and supervision events are registered by D3a, with the `tool` domain, and D3a wires K11's spawned-pid construction from D1a's handle (items 8 and 16).
- **X-O6. J-RW's next record.** Item 7's `host.repair.completed` is registered by O1-a; J4's units emit it from host (item 16). "The first J4 unit after O1, or O1 itself, adds the event" (JRW:496) is settled: O1 adds it.
- **X-O7. Q0's next record.** §9.4's channel (descriptor 3), the digest's definition, the phase table and outcome members, and the `harness` profile of the measured host (items 13 and 14; open question Q1).
- **X-O8. S-OP-6.** Render the frozen summary, including how `unpersisted` and `prescope-full` read to a user, and the `LoggingUnavailable` state (items 11 and 12).
- **X-O9. S-OP-7.** K6's census and C-9 (item 18); the ring's read path.
- **X-O10. The contracts-generator successor** inside O1-c (item 17).

## S-OP-2b: the owed successor's text

This is the exact successor text the lead owes. It is drafted as its own design unit next, with its own review; nothing here records it.

> **S-OP-2b. The harness instrumentation sink.** Contract successor to S-OP-2 r6 (`docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`, sha256 `ce8d3a4b783328915f0bf550dd111f227aa9901d5efddbcd9ccc8707cd4cb11d`). It adds one sink and changes nothing else.
>
> 1. **The sink.** Item 12's sink table gains one row: `harness`; owner: this successor for the channel and the content, Q0 for the projection; classes P0 and P1; present only in a build with the `harness-instrumentation` feature (rule 2). Item 12's projection rule applies unchanged: the encoder writes a field only if its static class is P0 or P1, and counts every other field in `omitted`.
> 2. **The build.** The feature is never a default and is never enabled from a `[dependencies]` table. It refuses, at compile time, any build without debug assertions. A featureless release binary contains none of the sink's strings, and a release-absence check proves it.
> 3. **Selection and level.** The feature is the release constant that selects the sink (item 21). The sink's level is the constant `info`. No environment variable, flag or configuration value selects or tunes it.
> 4. **The channel.** File descriptor 3, inherited from the harness driver. At logging start the host admits it once: it must be open, a FIFO or a regular file, and writable. The host then sets close-on-exec on it, so no child inherits it. If any check fails, the sink does not exist for the invocation: nothing is projected to it, and no tally counts it.
> 5. **Encoding and bounds.** JSON lines, under item 13c's wire schema, rule E and item 14's bound. The stream's first record is `log.stream.opened` with `sink: harness`. The `Sink` table gains the member `harness`.
> 6. **Accounting.** The sink is a persistent sink under items 15 to 17, with its own direct enqueue tally, writer snapshot, gate and marker. It has no pre-scope partition, because it is admitted at logging start, before any record. Finalization closes its gate as it closes any persistent sink's, and its outcomes are in the frozen summary.
> 7. **The record digest.** The exploratory envelope's `operationalRecords[].recordSha256` (`exploratory-quality-envelope.schema.v1`, r13) is the SHA-256 of the exact bytes the harness driver read from descriptor 3 for that invocation, from the first byte to end of file, a torn last line included. The host computes no digest of the stream.
> 8. **Reading.** The harness projects the stream only through item 13a's reader, at ceiling P0 and P1.
> 9. **Custody.** The stream is harness evidence in Q0's custody. It is never product evidence and never read by recovery. It enters no Run, Plan, Coverage, identity or digest, apart from `recordSha256` in the exploratory envelope.
> 10. **Control C-13.**
>     - (a) A build without debug assertions refuses the feature.
>     - (b) A featureless release binary contains none of the sink's strings.
>     - (c) `recordSha256` equals the SHA-256 the driver computes over the bytes it read.
>     - (d) The stream's first record is `log.stream.opened` with `sink: harness`.
>     - (e) A closed, read-only or wrong-type descriptor 3 leaves the sink absent and the result unchanged.
>     - (f) A reader that stalls or closes its end gives `sink-failed` or `drain-abandoned` within item 16's deadline, with the result unchanged.
>     - (g) No child process inherits descriptor 3.
>     - (h) C-4's canaries never appear in the stream, and no P2 field does.
>
> **What it does not change:** any other sink, ceiling, kind, class, bound, escaping rule or reader rule. The phase events and the `PhaseOutcome` members the stream carries are ordinary registrations (M3-O1 item 14), not successor content.

## Forbidden substitutes

- **Transport:** `tracing`, `log` or any `tracing-*` crate in the host lock without a law and a policy row; a subscriber or logger of any kind; a second registry, or a registry outside `crates/operability`; an event emitted outside the registry.
- **Edges:** an edge from operability to any crate but platform; an edge to operability from security or platform; `unsafe` in operability.
- **Identities:** a scope, mint or owner token constructed outside its owner; a public constructor of a P1 or P2 kind or of an identity; a test mint in a build without its feature; a record carrying an identity before its owner wired the mint; a RequestId synthesized so that records can be emitted before the RequestId scope is wired.
- **Sinks:** an environment variable, flag or configuration value selecting a sink, level or bound; stderr on in a production build; the development or harness sink in a release build; a sink that takes std's `Stderr` lock.
- **The summary:** rendering the loss summary, or any wording of it, before S-OP-6; failing a command because logging could not start.
- **Hashing:** a second SHA-256 dependency for operability; a path tag without the per-process key; the key written, logged or derived from an identity.
- **The harness:** reading the stream without item 13a's reader; a synthesized phase; a phase name outside the table; `recordSha256` computed by the host.
- **Tables:** hand-copied D9, DomainDetail or configuration tables; a K6 writer before S-OP-7.
- **Enforcement:** a sweep edit (lints or `dispose` migration) in O1-a; an exception count that rises; a `TestOnly` or `ShutdownPath` disposition outside its allowed files.
- **Sequencing:** editing a file an in-flight unit holds (item 23); binding S-OP-2-R without S-OP-2-P before it.

## Open questions for the reviewer

**None needs the owner.** Every choice carries the lead's recommendation.

- **Q1 (the measured build).** Under items 10 and 13, Q6 measures a host built with debug assertions on, in the optimized `harness` profile. At `b7b87b7` that activates 9 production `debug_assert!` sites and no other branch. Is that acceptable as Q0's "preregistered setting" (Q0:951)? **Recommendation:** yes, labelled in Q0's next record (X-O7). The alternative, a release-absence check as the only refusal, departs from the lead's decision.
- **Q2 (O1-p and J4a).** O1-p's `lib.rs` hunk, at the clock re-export (`lib.rs:96`), is disjoint from J4a's (`:41-47`). J4a is accepted but held for X3c-3 and §RW, so it is rebased before integration anyway. **Recommendation:** O1-p integrates after J3a and, if J4a is still held, before it, with J4a's rebase-only recheck noting the hunk. The alternative is that O1-p waits for J4a, which delays O1-b and O1-S.
- **Q3 (overlapping provider phases).** At concurrency above 1, sibling `provider` phases overlap, so "elapsed minus the sum of the top-level phases" can be negative. Q6 runs at concurrency 1 (Q0 §9.6). **Recommendation:** no aggregate phase at M3; S-OP-6's `--timings` revisits it. The alternative is a `providers` parent over every `provider` span.
- **Q4 (CH14).** Is a record note enough for a new package (item 1), or does it need a CH14 passage successor?
- **Q5 (S-OP-2-P).** Is selecting SDK4 and DRC in `control-source-v1`'s form lawful, given SDK4's own `CANDIDATE-NOT-APPLIED` header? The recording's README asks the same (R3).
- **Q6 (mint arguments).** Is a mint method that takes an identity's fixed-width value, held only by the owner, within SOP2 item 8(b), given the forbidden substitute "a P1 or P2 constructor that takes text, bytes or a parsed value" (SOP2:988)? **Recommendation:** yes. The mint is the provenance, and no public constructor takes bytes.
- **Q7 (O1-a's size).** O1-a carries most of S-OP-2. Should it integrate as two reviewed commits: the vocabulary, wire schema and reader; then the transport, sinks and wiring?
- **Q8 (the SHA-256 choice).** Is a second, in-house SHA-256, proved by known-answer tests, better than an identity edge (option (a)) or a policy row for `sha2-const-stable` (option (b))?

## Not claimed

- **Nothing was built.** No product code, cargo command or test was run for this law. The only execution was Python: the S-OP-2 recording's build and check scripts and its local binding check, in a throwaway worktree since removed.
- **No measurement.** Every size is M3P's planning duration.
- **No contract, schema, register row, gate or threshold is changed by this law.** S-OP-2-P and S-OP-2-R, S-OP-2b, the generator successor and the record notes carry the changes, each under its own review.
- **No production record at O1-a.** Records begin when the RequestId scope is wired (item 8).
- **No confinement claim.** As S-OP-2 says, the vocabulary keeps free text out of OpenSIP's sinks. It does not stop a provider signalling through its choice of codes, counts or timings (SOP2:1074).
- **No `tracing-core` fact was re-verified.** The gap report's statement about its `unsafe` declaration is cited as the gap report's (item 4).
