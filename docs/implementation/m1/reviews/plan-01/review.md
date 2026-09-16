# M1 startup plan review — actual Claude

**Verdict: CHANGES-REQUIRED** (5 required findings, 11 advisories)

**Subject:** the six-item M1 startup implementation-plan / tool-selection proposal supplied with this review request.
**Kind:** implementation-plan and tool-selection review. This is not code acceptance, not acceptance of any trial result, and not a reopening of the completed D-372 architecture review.
**Governing standing:** `root-application46-delivery.v1/README.md` and `completion.json`. The D-372 readiness account governs; dated "author proposal / Claude review pending" headers in the build plan and chapter 14 are historical provenance.

## Overall assessment

The plan is mostly sound, and most of it matches the accepted owners closely:

- **Build lanes.** The root virtual workspace excludes `providers/rust`. There are no inherited workspace fields, and root builds never invoke Node or providers. This matches the Rust workspace policy (build plan L617–643) and chapter 14 (L218–231).
- **Checked-in generation.** Outputs are checked in with a closed registry, all eight inventory outputs and no remote lookup (L654–662, L722–765). Handwritten exact admission stays separate, and numeric fields are never turned into strings (L1067).
- **Tooling trials.** Tools are chosen by trial, and a custom adapter must justify its maintenance cost (L1065–1066, L1073, L1077–1079).
- **Dependency checks.** A dependency graph that passes is not treated as proof of purity (L847–853, L1068).
- **Rust compiler.** The installed stable compiler is kept apart from the future isolated `rustc_driver` closure (L701–717).
- **Version identity.** Release IDs are never invented, and development fixtures are labelled (L840–842; `apps/cli/src/bootstrap.rs` row).
- **Milestones and gates.** M2–M6 keep their dependency order, and all 32 gates and 54 recovery cases stay unperformed.
- **Placeholders.** No 198 placeholder files are created (ch14 L302–305).

It cannot be accepted as written for five reasons:

1. **Help/version JSON has no schema home.** M1's help/version JSON deliverable targets a carrier that the accepted schema bytes do not appear to define.
2. **TypeScript integers.** No representation is given for integers that don't fit in a JS `number`.
3. **Generation trial.** The trial leaves out the report's shape-validator role, offline resolution of the schemas' URN `$ref`s, and how the generator closure digest is computed.
4. **No route for design successors.** The plan freezes the design files but departs from the file inventory, with no way to record a reviewed successor.
5. **Rust provider lockfile.** It is unclear which dependency-source mode the provider's authoritative lockfile records.

Each is bounded and fixable before (or at the start of) the affected M1 work. None requires reopening architecture acceptance.

## Required findings

### RF-01 — Help/version JSON parity fields have no typed carrier (and the release descriptor has no contract shape)

**Proposal item:** 5.

**Evidence:**
- **Coverage requires it.** Help and version must produce human output and CommandEnvelope-major-3 JSON "from shared pure metadata/envelope projection" (`implementation-coverage.v1.json` L1160–1218; build plan L885).
- **Parity fields declared.** `command-inventory.v3.json` L1193–1238 declares `help` parity field `command-names` and `version` parity fields `host-release` and `closure-ids`. Neither entry declares `parityPaths`. The JSON renderer's parity rule (L1708) defines pointers only through `queryDispatch.parityPaths`.
- **No meta kind or field in the envelope.** In `evaluator3/command-envelope.schema.json`:
  - It is closed (`additionalProperties: false`, L7).
  - The `kind` enum is `run|query|mutation|failure|invocation|doctor` (L23–33), with no meta kind.
  - None of its top-level properties (L17–159) or `$defs` (L531–911) carries command names, a host release or closure IDs.
- **Not in the invocation schema either.** `invocation-record.schema.json` has only render step params (L742–783) and core-transition closures (L1930–1934). Nothing there is a version payload.
- **Descriptor defined only in planning records.** "Build-embedded signed release descriptor" appears only in the build plan, chapter 14, the inventory and coverage. I found no contract or schema record for its fields, its signature-verification standing, or a development label.

**Why it blocks:** the only schema-valid ways to emit these values today are untyped `diagnostics[]` / `agentHints[]` text, or stuffing an invocation record. Those are exactly the placeholder or dynamic carriers that item 4 of the proposal rightly forbids. Implementation can't bind to an owner that isn't in the accepted bytes.

**Required correction:** before implementing JSON help/version, or presenting `host-release` / `closure-ids` values as bound, do one of the following in `opensip_arch`:
- **(a) Cite an owner I missed:** give the exact accepted carrier and pointer selector (Codex's binding check may find one; if so this finding closes by that citation); or
- **(b) Get a reviewed successor** that defines:
  - the typed meta payload and its parity pointers;
  - the release-descriptor record: its fields, and what signature verification it gets at M1 versus once security/lifecycle land;
  - how a development build is disclosed.

Until then, M1 may still deliver:
- argument parsing;
- human help and completion;
- pure host outcomes;
- lexical/canonical identity work.

It must not claim help/version JSON parity complete.

**Closure evidence:** the cited selector or the accepted successor, pinned in `design-lock.json`, plus startup tests that read parity values at the declared pointers.

### RF-02 — TypeScript exact integer representation is unspecified for u64/i64 domains

**Proposal items:** 3 and 4.

**Evidence:**
- **Contract.** Integer range is [-2^63, 2^64-1], and exact numeric admission happens before deserialization loses lexical information (`identity-and-evidence.md` L111–120).
- **Selected schemas use the full range.** `identity-schemas.v3.json` defines `U64` with maximum 18446744073709551615 (L24–27). It uses that bound for `bytes`, `generation`, `commitSequence`, `startByte`/`endByte` and `ordinal`, plus a signed range down to -9223372036854775808 (L2845–2848). Some fields are deliberately capped at 9007199254740991 (L592–595), which shows the distinction is intentional.
- **Plan.** Native JSON Number parsing cannot serve as exact admission (build plan L1067).
- **Tool behaviour.** json-schema-to-typescript maps `integer` to `number` and adds no runtime validation; `JSON.parse` rounds values above 2^53−1.
- **Gap.** "Never change numeric wire fields to strings" rules out one wrong answer but chooses no right one. Two TS outputs carry these values: `providers/typescript/src/generated/protocol.ts` (the provider emits frames) and `apps/report/src/generated/report.ts`.

**Required correction:** state the TS integer policy before the generator trial is judged.
- **Type choice.**
  - Any integer field whose schema bounds leave [-(2^53−1), 2^53−1] uses a single named lossless type, `bigint` or an equivalent generated from the bounds.
  - Only fields proven within that interval may use `number`.
- **Parsing and output.**
  - Parse with a lossless lexer before shape validation; it also rejects duplicate keys, exponent/float tokens and `-0`.
  - Serialize as bare integer lexemes, never strings.
- **Fail closed.** The generator (or a checked post-pass) fails the drift trial if any such field comes out as `number`.

**Closure evidence:**
- Trial receipts showing the generated types.
- Round-trip vectors at 2^53−1, 2^53, 2^53+1, 2^64−1 and −2^63.
- Negative controls: an over-range value, an exponent form, and a quoted number where an integer is required.

### RF-03 — The M1 generation trial is incomplete: report shape validator, URN `$ref` resolution and the generator closure digest

**Proposal item:** 4.

**Evidence:**
- **Selection is due at M1.** Generator selection and pin population occur at M1, with a drift trial "that exercises all eight target files" (build plan L762–765).
- **report.ts has two roles.** `apps/report/src/generated/report.ts` has both `carrier` and `shape-validator` roles (L749–750; ch14 L556). json-schema-to-typescript produces declarations only, and the proposal names no validator candidate. The matrix row "Before M4" (L1067) covers browser behaviour; it does not remove the M1 output role.
- **One closure per recipe.** A recipe row pins a single `generatorClosureSha256` (L734–737), and "the initial recipe covers all eight generated inventory files" (L748). A closure producing Rust (Typify), TS declarations and a TS validator in one combined output therefore spans the Rust and Node toolchains plus the composing step. The proposal doesn't say how that digest is computed.
- **Refs are cross-document URNs.** The selected schemas `$ref` each other by absolute URN, for example `urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/...` (`command-envelope.schema.json` L35, L64, L85, L130; `baseline-artifact.schema.json` L119–138). Transitive refs reach `native:evidence-schemas:v2`, `baseline:2`, `comparison:2`, `policy-document` and `graph-query:3`. Default ref resolvers treat such IDs as file or URL locations. "Remote refs forbidden" must therefore be built as an offline `$id` → registered-source map (L738–740).
- **Envelope schemas are outside layer 13.** Planning layer 13's file list includes only the graph-query and policy-test evaluator3 schemas (`implementation-planning-sources.v1.json` L341–350). The envelope, common and invocation schemas M1 needs are pinned only in application46 `files[]` (L782–820).

**Required correction:** the M1 generation plan must:
1. **Validator trial.** Name and trial a shape-validator candidate for `report.ts` at M1, such as Ajv standalone or a registry-specific generated validator. It must have no coercion, default insertion or additional-property removal, and its generated runtime dependencies must be declared in the report lane. It runs after RF-02's lossless parse.
2. **Closure digest.** Define `generatorClosureSha256` as a digest over an explicit, reproducible closure listing. The listing covers tool packages/crates with their lock digests, both toolchains, the composing script and the options, and the digest is recomputed in the trial.
3. **Offline refs.** Resolve refs only through the registry's `$id` map covering the complete transitive schema closure. An unknown or unregistered URN, or any attempt to use a file path or network, fails the trial (negative control required).

### RF-04 — Frozen design files, but no reviewed successor route for implementation-driven layout changes

**Proposal items:** 1 and 3.

**Evidence:**
- **Root package.json.** The inventory row for root `package.json` says "Declare TypeScript workspace membership and common script names" (ch14 L316; inventory L1388–1391). The proposal selects no root pnpm workspace and a coordinator with no runtime dependencies, which is a change of responsibility.
- **Unlisted files.** The proposal also adds files the inventory doesn't list: per-lane pnpm lockfiles and config, `design-lock.json`, and the verification tool.
- **Update rule.** Chapter 14 requires the inventory to be updated "whenever a reviewed split, merge or rename changes their responsibilities" (L150–153). It also leaves tool-specific configuration open until its owning decision (L157–158).
- **Conflict.** Item 1 freezes the original design files and puts progress in `opensip_arch/docs/implementation`, but gives no mechanism for such changes.

**Required correction:** define the successor path before creating those files. The path: a reviewed inventory/plan successor record in `opensip_arch`, preserving the original bytes, that records:
- the tool decisions;
- the changed root `package.json` responsibility;
- the added lockfile, config and tool paths.

`design-lock.json` is then rebound to that successor, and the implementation repo's inventory checks run against the successor, not the frozen v1. Implementation-status notes must not act as an informal second inventory.

### RF-05 — Which source mode does `providers/rust/Cargo.lock` record?

**Proposal item:** 2.

**Evidence:**
- **Plan.** "Each workspace's lockfile is authoritative for that build." The isolated provider build must prove shared packages resolve without the host workspace, and immutable exported source packages may be build inputs (build plan L634–643; ch14 L231).
- **Ambiguity.** The proposal uses exported pure source packages "during offline isolation tests". That implies ordinary provider development may use a different mode, such as path dependencies. Cargo records path and packaged or vendored sources differently in `Cargo.lock`. An isolation proof run in one mode therefore does not prove the checked-in lock used in the other.
- **Timing.** M1 creates the provider manifest and lock (inventory rows `providers/rust/Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`; M1 main files "Root/provider manifests").

**Required correction:** choose one authoritative source mode for the checked-in provider lock, and run the isolation proof in exactly that mode with `--locked --offline` and the host workspace absent. If a development convenience mode exists, it may never write the checked-in lock, and a check must refuse a lock whose sources differ from the declared mode.

## Advisories (nonblocking)

- **A-01 Design-lock binding.**
  - **What to pin.** Pin application46 `files[]` rows, not `beforeImages[]`. The manifest carries both, with different digests for `repository-file-inventory.v1.json` (L1154 vs L1543) and `implementation-coverage.v1.json` (L1052 vs L1523).
  - **Chain to verify.** Activation → manifest → review → Codex assent → completion.
  - **No commit shortcut.** The applied state is uncommitted, so no git commit can stand in for per-file hashes.
  - **Authorization record.** Record the user's separate implementation authorization in the implementation status record. The frozen `completion.json` / activation `implementationAuthorized: false` stays as history.
- **A-02 Registry vs design-lock ownership.**
  - **Keep two owners, no third.** `design-lock.json` owns provenance (architecture path → digest); `schemas/registry.json` owns generation (product path → digest). `schemas/README.md` must not become a third list.
  - **Verifier.** The verifier checks that each registry `sourceSha256` equals a pinned digest and that the migrated copy is byte-identical.
  - **Explicit schema ID/major mapping.** Record `schemaId` / `declaredMajor` / `profile` by explicit reviewed mapping where the `$id` has no major (e.g. `urn:opensip:product-v1:workflows:policy-document`) or uses a `:v3` form (L727–730). Don't parse them from `$id` strings or filenames.
- **A-03 Rust generator trial.**
  - **Regex dialect.** Selected patterns use ECMAScript lookahead `(?![\s\S])` (`common.schema.json` L30, L98). The Rust `regex` crate rejects lookaround, so the trial must show patterns are either enforced with the correct semantics or refused, never dropped.
  - **Silent degradation.** Heavy `allOf`/`if`/`then` usage, `oneOf`, `const` and `x-opensip-order` must not quietly become `serde_json::Value` or unchecked fields.
  - **Dependencies.** Generated-code dependencies (serde and similar) need the "explicitly reviewed pure external library" review for `crates/contracts` (ch14 L199).
- **A-04 TS lane isolation details.**
  - **Lane-local config.** Whatever settings file pnpm 11.10.0 actually reads must live in each lane root. The repo root keeps no `pnpm-workspace.yaml`, lockfile or installed `node_modules`.
  - **Pinning.** Pin `packageManager` exactly.
  - **Negative controls.** Seed a root workspace file and a sibling lane's lock or script and show that the checks refuse them.
  - **Dev Node vs sealed runtime.** Development Node 24.16.0 is not the sealed provider runtime or compiler closure. TS `compilerVersion` joins the admitted toolchain closure (L711–716), mirroring the Rust distinction the proposal already makes.
- **A-05 Rust workspace hazards.**
  - **Explicit per-package fields.** Declare `edition` and `rust-version` explicitly in every shared package (resolver 3 uses `rust-version`).
  - **Provider manifest.** The provider workspace declares its own `[workspace]` and `resolver`.
  - **Hierarchical config.** Cargo discovers `.cargo/config.toml` upward from the working directory. A root `.cargo/config.toml` would therefore silently apply to provider builds run inside the checkout. Avoid one, or prove the provider lane runs from an isolated copy.
- **A-06 Identity vectors.** Say where the independent oracle comes from: pinned architecture reference vectors with digests, not outputs of the code under test. Include:
  - duplicate keys, exponent/float tokens, `-0`;
  - malformed UTF-8 and non-scalar Unicode;
  - the depth-32 rule (root counts as 1, keys and scalars add nothing);
  - the 4 MiB bound;
  - all escaping laws;
  - admitted-order arrays and `x-opensip-order` refusals (identity-and-evidence L113–139).
- **A-07 Meta command precision.**
  - **Completion is human-only.** `completion` is human-only (coverage L1225–1250). A JSON completion request takes the registered not-applicable refusal, not a JSON rendering.
  - **Startup tests.** `apps/cli/tests/startup_tests.rs` should run with project, store and provider resources unavailable, and record a process/module trace. That prepares for DR-G03's evidence method without claiming qualification.
- **A-08 Gates routed to M1.** DR-G03, G15, G16 and G31 route implementation owners to M1 (coverage L4478, L4790, L4815, L5214). Prepare their owners and harness specifications, and reuse lane-isolation receipts as G16 "skipped-lane proof" inputs. Qualification stays M6.
- **A-09 Dependency checkers.**
  - **TS coverage.** Item 6 omits aliases (tsconfig `paths`), generated inputs and scripts (L1069).
  - **TS tool choice.** Record the dependency-cruiser versus compiler-API trial.
  - **Seeded controls.** Seed one forbidden edge per kind: normal, build, dev, target, feature, provider-compiler leakage, type-only, dynamic, export and script. An unsupported resolution must fail rather than count as no edge.
- **A-10 Code-review completion standard.**
  - **Frozen manifest.** It lists paths and SHA-256 for the review subject.
  - **Validation receipts.** Each records argv, cwd, environment allowlist, toolchain and lock digests, exit status, and stdout/stderr digests.
  - **Closing findings.** Required findings close only by rereview of the exact successor bytes.
  - **Behaviour, not names.** Tests are judged on behaviour, including negative boundaries.
  - **Drift checks.** A passing drift check proves byte equality only, never semantics.
  - **Trials.** Trials stay "candidate" until their receipts exist.
- **A-11 Development version labelling.** A SemanticVersion prerelease or build suffix alone is not a sufficient development label. No `closure2:`-shaped IDs may be fabricated for fixtures. Settle the disclosure inside the RF-01 successor, mirroring `HostAssetPinV1.buildChannel` (L814–815).

## Scope limits

- **No commands run.** No command was executed and no file hashes were recomputed (no shell tool available). Digests cited are as recorded by the pinning manifests.
- **Tool versions unverified.** Installed pnpm 11.10.0, Node 24.16.0 and Rust 1.95.0 were not verified, and no trials were run or observed.
- **Bounded reading.** The search for a help/version carrier covered:
  - evaluator3 `command-envelope`, `invocation-record` and `common` schemas;
  - `command-inventory.v3.json`;
  - security-lifecycle schemas;
  - the product-v1 contracts;
  - the design-corrections `workflows/`, `security/`, `foundation/` and top-level records.

  An owner elsewhere would close RF-01 by citation. The historical evidence archive, the prior-review queues, the full native-evidence schemas and the full 12,920-file accepted set were not read.
- **Not code acceptance.** No product code exists in `/Users/sb/code/opensip-ai/opensip` (bare `git init`), so none was reviewed or accepted.
- **Design bindings.** Codex is checking design bindings independently; this review does not replace that check.
- **Accepted design untouched.** Settled D-372 design decisions were not reopened. The findings concern whether this plan can bind to the accepted owners.
