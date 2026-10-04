# CR-1 — component roles and closure kinds (contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r3, PROPOSED, not accepted.** It is a design unit: it edits only arch, and changes no product file, code, class, exit code, route or public code. It needs CODEX2's `ACCEPT-DESIGN-UNIT` and the lead's root assent before it can be bound in the product's `design-lock.json`.

**What it is.** Accepted law **M3-C** names successor **CR-1** (MC:1053): "security / DR-103 host vocabulary successor; security owner with D4 | Item 7's role-to-kind table; widening the manifest `role` enum | C2a; F4 and G2 closure manifests". Item 7 (MC:360-396) fixes the table. It says that "Widening the role enum is successor CR-1, owned by security and DR-103, and joined with D4's `components/manifest.rs`" (MC:380). Owner question R2 (MC:1211) asks the security and DR-103 owner to confirm it. Three other units depend on it:
- E1 needs the `grammar` role for E2b's real admission (ME:697);
- M3-D's D4 admits "every `analyzer`-role component, with the role closures of MC item 7's table" at R10a (MD:718);
- CR-1 and CRC-1 must both be accepted before C2a (MC:1076, MC:1086).

**Law standing.** As for CRC-1: this unit was commissioned against r6 (`8274bca1…`), and CODEX2 accepted r7 (`a1ee9386…`) during drafting. r7 leaves item 7 and the successor rows word for word, and this README cites r7's lines.

**Product.** Main `392499e` (CRC-1's binding), read only, with 83 contract successors. CRC-1 is the 83rd. r3's record is built and checked against `392499e`'s lock, read with `git show`. From `cd5958b` to `392499e` only `design-lock.json` changed. r2 was built on `cd5958b` (82) and r1 on `9c11c53` (79).

## r3 changes

CODEX2 reviewed r2 (subject `4e1b169b…`, `reviews/codex2-cr-1-r2`) and returned REQUIRED-FINDINGS, with one new required finding, RF-CR1-2. It resolved RF-CR1-1 and NB-CR1-1. r2's changed members are kept in `reviews/codex2-cr-1-r3/r2-members/` for diffing.

| Item | Change |
|---|---|
| **RF-CR1-2** (name admission must not be gated) | **The lead's direction: split the gate.** r2 told C2a to run the whole `command_checks` function only when `commands` is present. That function also holds component-name and manifest-alias admission, so the gate would have let a closure-only manifest skip the duplicate name and alias, reserved-name and live-name collision checks, which DR-103 keeps for every role. Now only the command-tree checks are conditional, and name and alias admission runs for every manifest. The changes, in CODEX2's exact text:<br>- `materialization-map.json`'s owner instruction for `crates/security/src/component_manifest.rs`, followed by one added sentence that cites the function's line ranges at `cd5958b` and `392499e`: `command_checks` 166-279, its command-tree checks 171-256, its name and alias admission 257-276, called once at 414 for both `validate` and `validate_inventory`;<br>- LD-7's C2a bullet;<br>- the last line of CR-T7;<br>- a new control, **CR-T9**, which adds one sentence for the closure-only collision case.<br>No contract text, schema or passage changes. The four overrides and the copy are r2's, byte for byte. |
| **The base** | Product main moved to `392499e`, which binds CRC-1. The build, check and audit scripts default to it, and the generated reports name it. The parents, the product schema input, the generator, the owner and the fixtures are byte-identical at `9c11c53`, `cd5958b` and `392499e`. |
| **Review path** | The builder and the unit draft name `codex2-cr-1-r3/review.json`. |

Nothing else changes.

## r2 changes

CODEX2 reviewed r1 (subject `f0a5c222…`, `reviews/codex2-cr-1-r1`) and returned REQUIRED-FINDINGS, with one required finding and one non-blocking observation. r1's changed members are kept in `reviews/codex2-cr-1-r2/r1-members/` for diffing.

| Item | Change |
|---|---|
| **RF-CR1-1** (the closure-only command tree) | **The lead's direction (LD-8): closure-only roles declare no command tree.** r1 kept DR-103's required tree for every role and only said it was never mounted. Under DR-103 that tree is still "the declarative command grammar this component asks the host to mount" (DR103 fields/8), and D4's EE-5a (MD:731) refuses a root-command claim at admission. CODEX2 offered an "inert metadata" reading; the lead rejected it, because it leaves a claim-shaped object in the manifest and needs a reading rule at every consumer. Instead:<br>- **the copy** makes `commands` role-scoped: still required and non-empty for `analyzer`, and absent for the four closure-only roles (LD-8 gives the exact shape);<br>- **SL:70** gains a command-tree column in its table, replaces "the host mounts and dispatches none of its commands" with "it carries no command tree", and states **the D4 join**;<br>- **a fourth override**, DR103 `/manifestSchema/fields/8/semantics`, makes the tree role-scoped in DR-103's own words;<br>- **DR103 fields/7's semantics** now reads "it carries no command tree" instead of "none of its commands is mounted".<br>`evidence/audit_schema.py` and `evidence/schema-audit.json` are new. They check the copy with an independent engine (below). |
| **NB-CR1-1** (CR-T4) | **LD-9: CR-T4 is scoped by role**, with CODEX2's exact text. A closure-only entrypoint must be a regular-file entry itself, so a symlink refuses. An `analyzer` entrypoint keeps RJ-3's existing in-tree resolution and executable-file checks. SL:70 now says "never a directory or symlink" for closure-only entrypoints. |
| **Stale names** | r2 pointed the Binding section, the unit draft and the builder at `reviews/codex2-cr-1-r2/review.json`, which cleared CODEX2's note that `--check` differed only on `cr-1-unit.json`. The r2 request named CRC-1's review directories as they then stood. |
| **The base** | r2 moved the scripts' default to `cd5958b`; r3 moves it to `392499e`. |
| **`verify_scratch.py`** | Asserts four overrides, and gains `--before-crc-1` (CR-1 then CRC-1) beside `--after-crc-1`. |

The role-to-kind table, the role vocabulary, the selection form and every r1 lead decision not named above are unchanged. LD-2 and LD-3 are restated where RF-CR1-1 changed them.

## Short names

- **MC** M3-C r7, accepted: `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r7.md` (157,110 bytes, `a1ee9386…`).
- **ME** M3-E1 r3, accepted: `docs/implementation/m3/syntax-e/PROPOSAL-r3.md` (`d71031ff…`).
- **MD** M3-D r3, accepted by GROK2: `docs/implementation/m3/supervisor-d/PROPOSAL-r3.md` (`9679dbc4…`).
- **CRC-1** is the sibling unit, `docs/implementation/m3/snapshot-plan-c/crc-1/`. Grok accepted it at r4, and it is bound at product `392499e` as the 83rd contract successor.
- **CMS** is the completed structural manifest schema, `docs/coop/completion/manifest-schema.completed.v1.json` (24,193 bytes, `a5140714…`). It is **not** a `verify_design` input. The architecture application `docs/coop/completion/architecture-application.v1.json` (an accepted input, `15b3932a…`) pins it in clause `M.SCHEMA`. The product carries the same bytes as its security generation input, `tools/security/inputs/manifest-schema.json`, from which `crates/security/src/generated/component_manifest_shape.rs` is generated.
- **CMC** is CMS's completion contract, `docs/coop/completion/manifest-completion.contract.v1.md` (`da2b00f5…`). It is not a `verify_design` input either.

The parents, both accepted inputs of the lock at `392499e` (and at `cd5958b` and `9c11c53`):
- **SL** `docs/v2/contracts/product-v1/security-and-lifecycle.md` (119,915 bytes, `a319da39…`).
- **DR103** `docs/coop/artifacts/component-manifest-schemas.v11.json` (139,492 bytes, `1c0b8868…`). This is the accepted DR-103 field authority. Its `role` field is `/manifestSchema/fields/7` and its `commands` field `/manifestSchema/fields/8`.

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: the four overrides with exact `before` and candidate `after`, and the copy's diff |
| `successor.json` | the contract successor record: two parents, four passage overrides, no supersession, ten candidates |
| `completion/manifest-schema.completed.v1.json` | generated: the complete successor copy of CMS |
| `materialization-map.json` | generated: the product bytes C2a copies, and the product files C2a changes or checks with them |
| `evidence/copies-report.json` | generated: the copy's parent and selection, its three edits, its serialization, and the role-case audit |
| `evidence/audit_schema.py` | r2: audits the copy with jsonschema 4.25.1 (installed offline under `--deps`) against the product shape fixture, and writes or compares `schema-audit.json` |
| `evidence/schema-audit.json` | r2: the audit's result; the build refuses one that does not audit this copy |
| `evidence/build_cr_1.py` | builds every generated file, the record, the subject manifest and the unit draft; `--check` compares instead of writing |
| `evidence/check_cr_1.py` | read-only, independent content checks |
| `evidence/verify_scratch.py` | runs the real `verify_design` with a synthetic review and assent. It runs alone, or with CRC-1 in either order (`--after-crc-1`, `--before-crc-1`) on a lock that does not yet bind CRC-1, such as `cd5958b`. From `392499e`, CRC-1 is bound, and the plain run binds CR-1 on top of it. |
| `../cr-1-subject.json` | the subject manifest (generated) |
| `../cr-1-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`; not part of the subject |

## What changes

There are four passage overrides, and each only inserts text. There is also one complete successor copy. `PASSAGES.md` has the full texts.

| # | Parent | Line or pointer | Change |
|---|---|---|---|
| 1 | SL `docs/v2/contracts/product-v1/security-and-lifecycle.md` | 70 | After S1's closure-association paragraph (SL:21-70), a new block, **Component roles and closure kinds**:<br>- the closed role-to-kind table, word for word MC:370-376, with a third column for the command tree: required and non-empty for `analyzer`, absent for the rest;<br>- the rules: the kind comes only from `role`; a role/field kind mismatch refuses; `evaluator`, `detector`, `adapter` and `core` are never roles;<br>- the four non-`analyzer` roles are **closure-only** (below);<br>- **the D4 join**. |
| 2 | DR103 `docs/coop/artifacts/component-manifest-schemas.v11.json` | `/manifestSchema/fields/7/type` | appends the M3 vocabulary: `analyzer`, `toolchain`, `stdlib`, `rust-dev-llvm`, `grammar`, each fixing the `closure2` kind through SL S1's table |
| 3 | DR103 | `/manifestSchema/fields/7/semantics` | appends that the four roles beyond `analyzer` are closure-only and carry no command tree |
| 4 | DR103 | `/manifestSchema/fields/8/semantics` | r2: appends that the tree is role-scoped. `analyzer` keeps it as before. A closure-only manifest carries none (`commands` absent), so it asks for no mount and claims no root command, and one that declares a tree is refused, by the closed schema (RJ-6) and at D4/R10a as an EE-5a claim. |

DR103 fields/8 also carries `"required": true`, a boolean. A passage override can change only a text value, so the semantics string states the role-scoped exception, and the copy is its executable form.

**The successor copy.** `completion/manifest-schema.completed.v1.json` is CMS with exactly three edits. It keeps CMS's own serialization (`json.dumps(indent=2)` plus LF, which is byte-identical to the parent). It is 25,128 bytes, `343dc517…`. The three edits are:
1. `/properties/role`: `{"const": "analyzer"}` becomes `{"enum": ["analyzer", "toolchain", "stdlib", "rust-dev-llvm", "grammar"]}`, in the table's order.
2. `/required`: `commands` is removed.
3. A root `oneOf` is added, after `additionalProperties` and before `$defs`, with two branches (LD-8).

`/properties/commands` (an array of CommandSpec, 1 to 4,096 items), `$id` and every other byte are unchanged.

## The rule

| Manifest `role` | `closure2` `kind` | Command tree | Launched by the host as a component? |
|---|---|---|---|
| `analyzer` | `provider` | required, non-empty | yes, as a provider session |
| `toolchain` | `toolchain` | none: `commands` absent | no: closure-only |
| `stdlib` | `stdlib` | none: `commands` absent | no: closure-only |
| `rust-dev-llvm` | `rust-dev-llvm` | none: `commands` absent | no: closure-only |
| `grammar` | `grammar` | none: `commands` absent | no: closure-only |

- **Where the kind comes from.** It comes only from `role`, through this closed table. It is never asserted by a caller, inferred from a path or file name, or taken from any other field (MC:384).
- **Kind mismatch.** A closure whose role maps to a kind other than its selecting field requires (IDS `closureKinds.byField`) refuses (MC:380; MC's control C2-T2).
- **Roles that do not exist.** `evaluator`, `detector` and `adapter` are never manifest roles, and `core` is never a role or an identity closure kind. The in-core closures are CRC-1's and EC1's projections of the authenticated core inventory (MC:378).
- **Closure-only roles.** The host never launches such a component through its manifest; it reads the component's tree only as retained closure bytes. So a closure-only manifest:
  - declares `capabilities: []`, since a capability declaration is an analyzer role subprotocol;
  - requests `permissions: []`;
  - has a platform `entrypoint` that names a committed regular-file entry, never a directory or symlink, under RJ-3's path and presence rules. It need not be executable, and the host never executes it;
  - **carries no command tree.** `commands` is absent, so it asks for no mount and claims no root command.
- **The D4 join.** D4's EE-5a root-command check at R10a (MD:731) examines every manifest that declares a command tree. For a closure-only role, any declared tree is such a claim. It is refused by the closed schema at admission (RJ-6), and at D4 as an EE-5a claim by that existing route. How EE-5a judges an `analyzer` manifest's required tree is M3-D's and unchanged.
- **Tools inside a closure.** A tool the host launches from a closure-only tree, such as C3b's cargo adapter, is launched under its own launch law (the D law), never as a component session.
- **Every other DR-103 rule** applies to every role alike.
- **Refusals.** A violation refuses through the manifest owner's existing schema (RJ-6), capability, permission and path refusals. No code is added.

## Why this form

- **SL:70 is free.** SL's bound overrides are at lines 109, 166-298, 619, 685, 711, 845, 917, 953, 977 and 1323. None is inside S1's lines 19-70.
- **DR103 has no bound override.** Its three strings are fresh JSON Pointer keys. `build_cr_1.py` checks both facts against the lock at `392499e`.
- **CMS cannot be a parent.** `contract_successor` admits a parent only if it is accepted, and CMS is not in the lock's accepted set. So the copy is an ordinary candidate at a new path. The record's `standing` selects it as the completed manifest schema, and CMS becomes historical. This is B-S9's selection form, and I1-L's copy form for the bytes.
- **The copy really is CMS's successor.** `build_cr_1.py` asserts that its parent bytes are exactly the pin in the application's `M.SCHEMA` clause, the product's generation input at `392499e`, and the product `sources.json` row.

## Role-case and schema audit

Neither change may turn an existing case's verdict. The checks are in `evidence/copies-report.json`, which `check_cr_1.py` recomputes, and, new in r2, in `evidence/schema-audit.json`, which `audit_schema.py` recomputes.
- **The arch completion cases** (`manifest-cases.completed.v1.json`). The one role-setting case, `TYPE/role`, sets `builder`, which is still outside the enum.
- **The product shape fixture** (`crates/security/tests/fixtures/manifest268-shape.ndjson` at `392499e`, unchanged since `9c11c53`; 11,010 cases). This is the oracle the generated Rust shape is tested against (`component_manifest.rs`, `generated_closed_schema_matches_entire_exact_schema_oracle`). The audit uses jsonschema 4.25.1's `Draft202012Validator`, an engine independent of the generator:
  - the parent reproduces all 11,010 verdicts;
  - the copy gives the same verdict as the parent on all 11,010, so none flips;
  - all 55 role cases stay invalid and use no CR-1 role.
- **Role variants (r2).** On each of the fixture's five valid base manifests, 100 variants behave as LD-8 requires:
  - `analyzer` is valid only with its non-empty tree. It is invalid with `commands` absent, `[]` or `null`, under both schemas.
  - Each closure-only role, with `capabilities` and `permissions` empty, is invalid under the parent. Under the copy it is valid only with `commands` absent: a tree, `[]` or `null` refuses.
- **Keywords.** The copy uses only keywords that the product's shape generator accepts (`tools/security/generators/manifest_shape.py`, its `allowed` set).
- **The product semantic fixture** (`crates/security/tests/fixtures/manifest268-semantic.ndjson`). Every case is role `analyzer`, and `REQUIRED/role` and `TYPE/role` stay invalid.

## Lead decisions

Each decision is dated 2026-10-04 and made under the owner's standing direction. Each names the alternatives it rejects, and the owner may reverse any of them.

**LD-1. The table lives in SL S1, and the vocabulary in DR-103's role field.** S1 is where a component-manifest closure becomes a `closure2` (SL:27-48). DR-103 makes the role vocabulary host-owned (DR103 `role.type`).
- **Rejected:** the table in BP or IE, since security owns component admission and identity owns kinds, not roles;
- **Rejected:** a new standalone registry file, which would be a second owner of one vocabulary.

**LD-2 (r2 wording). The executable form is a complete successor copy of CMS: `role` widened to a five-role enum, and `commands` role-scoped (LD-8). `$id` and `manifestSchemaVersion` are unchanged.**
- **Why it is safe:**
  - no existing manifest changes verdict (see the audit);
  - an old host still refuses a new role (fail closed);
  - the product generator supports every keyword used. `enum` is emitted as an `||` of constants, and `oneOf` as an exactly-one count.
- **Rejected:**
  - **a schema major bump.** No existing manifest changes, as with I1-L's additive member under an unchanged major.
  - **per-role branches that restate the whole manifest.** They would duplicate twenty fields per role. The r2 branches constrain only `role` and `commands`.
  - **overriding the application's `M.SCHEMA` pin strings.** That would rewrite an application record's evidence pins, and CMS still could not be a parent.

**LD-3 (r2 wording). The four non-`analyzer` roles are closure-only, with four field rules:**
- no capability;
- no permission;
- a regular-file entrypoint that need not be executable and is never executed;
- no command tree (LD-8).

Without these rules the widened roles could not be admitted lawfully:
- **The executable-entrypoint check.** CMC:125 says "Entrypoints resolve to committed executable files", and the product owner enforces it (`crates/security/src/component_manifest.rs:337`, `ENTRYPOINT_NOT_EXECUTABLE_FILE`). Under that rule, a `stdlib` or `grammar` component would have to ship a dummy executable: an execution surface with no purpose. For a grammar closure it is impossible anyway. E1's grammar tree is closed from two declared roots and refuses unrelated files (ME item 4, ME:177-215; its r3 change E-R2-02), so it cannot carry an extra executable.
- **Capabilities.** A toolchain could otherwise declare analyzer capabilities, a claim no host contract serves.
- **The command tree.** A closure-only manifest that carried DR-103's required tree would request a root-command mount, which D4's EE-5a refuses at admission (RF-CR1-1).

**Rejected:**
- (a) **no per-role rule**, for the reasons above;
- (b) **dropping `entrypoint` for these roles.** That is a structural change across DR-103's required platform fields and BP:704's "RJ-3 entrypoint". r1 also rejected dropping `commands`; r2 reverses that under the lead's direction (LD-8), because the tree is a claim, not a structure;
- (c) **a second manifest `kind` for closure components.** `kind` is the constant `component`, so a new kind is a release-format change;
- (d) **executable entrypoints for `toolchain` only.** Nothing launches a toolchain component through its manifest either. The D law launches a tool from the closure tree by its own rules. "Need not be executable" still lets a toolchain name its compiler.

**LD-4. `evaluator`, `detector` and `adapter` never become roles, and `core` never does.**
- **Rejected:** a `detector` role now for third-party detectors. X12 and DR-131 admit no user or third-party packs, and the core's detector is CRC-1's projection.

**LD-5. The selection is declared in the record.** CR-1's copy is the selected completed manifest schema. The following become historical:
- CMS itself;
- CMC's sentence "The initial role vocabulary remains exactly `analyzer`. … no auxiliary/build role is invented." (CMC:19-20);
- CMC:89's "new role";
- for the closure-only roles, CMC:125's executable-entrypoint sentence and CMC's mounted-root command rules (CMC:57-65).

- **Disclosed:** `verify_design` does not enforce selection, so a later unit that edits CMS instead of the copy is caught only by review (B-S9's residual hazard).
- **Rejected:** leaving CMS current, which would leave the product's generation input contradicting SL S1.

**LD-6. No new refusal code.**
- An unknown role is RJ-6 (closed schema), as today, and so is a closure-only manifest that declares `commands`.
- The other closure-only rules use the owner's existing capability, permission and path refusals (`Error::Capability`, `Error::Permission`, `Error::Path`). D4's EE-5a route is M3-D's existing one.
- **Rejected:** new codes, under the owner's no-new-codes rule.

**LD-7. Materialization and binding.** C2a materializes CR-1, because item 7's admission is C2a's (MC:1086). It:
- copies the bytes;
- re-pins `tools/security/inputs/sources.json`;
- regenerates `component_manifest_shape.rs` through `tools/generate_security_tables.py`, with the generator itself unchanged (`materialization-map.json`);
- separates component-name and manifest-alias admission from command-tree validation. The name/alias checks currently at `component_manifest.rs:257-276` remain mandatory for every role, including reserved-list refusal and the existing different-`(stableId, provenance)` live-name collision rule. Only command-tree validation requires `commands`, which the schema guarantees exactly for `analyzer`; analyzer retains mounted-root alias checks;
- makes the executable-entrypoint check role-scoped;
- adds the closure-only checks;
- applies the table in closure admission.

D4 consumes the result at R10a (MD:718). After acceptance the lead binds CR-1 in a binding-only product commit, before C2a.
- **Rejected:** binding inside C2a's commit, which would mix review subjects.

**LD-8 (r2, RF-CR1-1; the lead's direction). Closure-only roles carry no command tree: `commands` is absent, and the schema enforces it.** The copy's shape:
- **The root `/required` drops `commands`.** `/properties/commands` keeps its definition: array, CommandSpec items, 1 to 4,096.
- **A root `oneOf` of two branches,** which are disjoint by `role`:
  - **analyzer:** `role` is `const` `analyzer`; `commands` is required, an array with at least one item. So `analyzer` is exactly as before.
  - **closure-only:** `role` is one of `toolchain`, `stdlib`, `rust-dev-llvm` or `grammar`, and `commands` is typed `null`. The root types `commands` as an array, so no value satisfies both. **`commands` must therefore be absent.**
- **Comments.** Each branch carries a `$comment` saying this.

The schema has no conditional keyword inside the product generator's subset: no `if`/`then`, `not`, `dependentSchemas` or `false` schema. `oneOf` is the conditional form it does have, and absence is expressed as an unsatisfiable type, which is the narrowest lawful shape.

**Rejected:**
- (a) **the inert reading** of a still-required tree (CODEX2's offered fix). It leaves a claim-shaped object in every closure-only manifest and needs a reading rule at every consumer. This is the lead's rejection.
- (b) **"absent or `[]`".** That gives two spellings of one fact in a signed body, and it reopens whether an empty `commands` member is a declared tree, which is the same reading-rule cost. Spelling it `maxItems: 0` would also emit `a.len() <= 0`, a comparison clippy's deny-by-default `absurd_extreme_comparisons` refuses. That would force a generator change for no gain. `type: null` emits `matches!(v, V::Null)`.
- (c) **refusing the tree only in the semantic phase.** The structure would then admit a claim, and refusal would rest on code alone. The lead asked for schema scoping.
- (d) **removing `commands` from the root `properties`,** with per-role property sets. That duplicates the manifest's twenty fields per role (LD-2).

**LD-9 (r2, NB-CR1-1). CR-T4 is scoped by role.** A closure-only entrypoint must be a regular-file entry itself: a directory or a symlink refuses. An `analyzer` entrypoint keeps RJ-3's existing in-tree symlink resolution and executable-file check (`component_manifest.rs:301-341`; CMC:123-125). The rule is in SL:70's text ("never a directory or symlink") and in CR-T4.
- **Rejected:**
  - refusing `analyzer` symlink entrypoints, which would be a new analyzer restriction outside CR-1 and would change existing admitted manifests;
  - resolving closure-only symlinks the way `analyzer` does, which adds a resolution step for an entrypoint nothing executes.

## Controls proposed for C2a

These are for C2a's review. MC's C2-T1 to C2-T5 still apply.
- **CR-T1.** One manifest per role admits through item 7's production path, with the table's kind. Each closure-only manifest has no `commands`.
- **CR-T2.** Role `builder` refuses RJ-6 (existing). Each of `evaluator`, `detector`, `adapter` and `core` as a role refuses RJ-6.
- **CR-T3.** A closure-only manifest with a non-empty `capabilities` or `permissions` refuses.
- **CR-T4** (r2, CODEX2's exact text). A closure-only manifest whose entrypoint is a regular file with mode `0644` admits. The same entrypoint on an `analyzer` manifest still refuses `ENTRYPOINT_NOT_EXECUTABLE_FILE`. A directory entrypoint refuses for every role. A closure-only entrypoint that names a symlink refuses; an `analyzer` entrypoint keeps the existing RJ-3 resolution and executable-file checks.
- **CR-T5.** A role-to-field kind mismatch refuses (C2-T2), for example a `grammar` closure named as a view producer.
- **CR-T6.** A source pin shows two things: the generated role node is the five-role enum, and no closure-only component reaches a launch, command inventory, mount or dispatch.
- **CR-T7** (r2). These cases refuse RJ-6 at manifest admission, before any analysis-attempt ExecutionId:
  - a closure-only manifest with a `commands` tree;
  - a closure-only manifest with `commands: []` or `commands: null`;
  - an `analyzer` manifest without `commands`.

  Command-tree validation never runs on a manifest without `commands`. Component-name and manifest-alias admission still runs for every role without reading an absent tree.
- **CR-T8** (r2, with D4). A complete signed `grammar` manifest with no command tree passes R10a. A tree on a closure-only manifest presented to D4 refuses through EE-5a's existing route. EE-5a's other refusals are unchanged.
- **CR-T9.** For every role, component-name and manifest-alias admission remains enforced independently of command-tree presence. A component name or alias colliding with the reserved list refuses RJ-2; an alias duplicating the component name refuses RJ-2; a name or alias colliding with a live entry of a different `(stableId, provenance)` refuses RJ-2. The same-`(stableId, provenance)` coexistence control still admits when all other rules pass. Closure-only controls have no `commands`; analyzer controls retain their required tree and mounted-root alias checks. (r3) In particular, a closure-only manifest with no `commands` whose name collides with a reserved or live name refuses on that existing route, in both `validate` and `validate_inventory`.

## Cross-law items

1. **E1 (E2b, the grammar bundle).** The real and synthetic grammar manifests use role `grammar`, with `capabilities: []`, `permissions: []` and no `commands`. The lead recommends that the entrypoint name the bundle manifest at its fixed path `opensip-interface/grammar/bundle-manifest.v1.json` (ME:182). That is a committed regular file and a declared root of the closed tree, and it is never executed.
2. **F4 and G2 (toolchain, stdlib and rust-dev-llvm manifests).** They follow the same closure-only rules (MC:1053), with no `commands`.
3. **M3-D (D4 at R10a).**
   - MD:718 already admits "the role closures of MC item 7's table". A closure-only manifest declares no tree, so EE-5a has nothing to find in it, and a declared one refuses (the D4 join).
   - **For M3-D's next revision:** MD:729 (EE-3b) counts "a `commands` entry for role `analyzer`" as an excluded authority claim, and MD:731 (EE-5a) counts a root-command claim. DR-103 still requires an `analyzer` manifest to carry a non-empty tree whose parentless entry is its mounted root command. How D4 admits any `analyzer` manifest under those rows is M3-D's to state. CR-1 leaves the `analyzer` tree exactly as before.
4. **C2a's synthetic signer (MC item 8)** writes manifests that satisfy CR-1 for every role.
5. **CRC-1.** The two units cross-reference each other by name and share no parent. CRC-1 is accepted (r4) and bound at `392499e`, and CR-1 binds on top of it.

## Points for the reviewer

- **R1 (RF-CR1-2).** Do the map, LD-7, CR-T7 and CR-T9 now keep component-name and manifest-alias admission mandatory for every role, with only the command-tree checks conditional? Are the cited line ranges right?
- **R2.** Did anything else change? Diff `reviews/codex2-cr-1-r3/r2-members/` against the r3 members. The four overrides and the copy should be byte-identical to r2's.
- **R3.** Is the record well-formed under `verify_design`'s `contract_successor` and `successor_chain` rules at `392499e`, with CRC-1 bound?

## Binding

CR-1 binds on the `verify_design` at main `392499e`, on top of all 83 contract successors (CRC-1 among them), with no prerequisite. After `ACCEPT-DESIGN-UNIT`:
1. copy the review to `docs/implementation/m3/reviews/codex2-cr-1-r3/review.json`;
2. complete `cr-1-unit.json`;
3. append the four pins to the product lock;
4. run plain `verify_design`.

## Evidence runs

Every run used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, read only, and each was made twice. Nothing ran cargo, a test, a generator or a product tool other than `verify_design` in the scratch harness.
- **`evidence/audit_schema.py --deps <dir>`** (default `392499e`) compares with `schema-audit.json`: identical. It covers 11,010 fixture cases and 100 role variants.
- **`evidence/build_cr_1.py`** writes the files. A second run with `--check` reports identical bytes for every generated file and the unit draft, and confirms that the audit audits this copy.
- **`evidence/check_cr_1.py`** passes at `392499e` (the default), at `--rev cd5958b` and at `--rev 9c11c53`. It includes r3's assertions for RF-CR1-2.
- **`evidence/verify_scratch.py --rev 392499e`**: 83 to 84. There are four overrides and no supersession, and the inventory (`v134`) and inheritance (55) are unchanged. CRC-1 is already bound in this lock, so this run binds CR-1 with CRC-1.
- **`evidence/verify_scratch.py`** on the checkout at `392499e`: 83 to 84, with 40 generation sources and 48 admission sources verified.
- **At r2's base:** `evidence/verify_scratch.py --rev cd5958b`, with `--after-crc-1` and with `--before-crc-1`, still binds: 82 to 83 alone, and 82 to 84 in each order with CRC-1's files on disk, which are now its accepted r4.

## Not changed, and noted

- **`closure2.protocolMajor`.** No accepted text says which manifest field supplies it for any role. CR-1 changes no compatibility field, and C2a's projection applies one rule to every role.
- **BP:701-709** already lists provider, toolchain, stdlib, rust-dev-llvm and grammar artifacts as component manifests with an RJ-3 entrypoint. It is consistent with CR-1, so it is not changed.
- **The product files are unchanged**: `component_manifest.rs`, the generated shape, the security inputs and the fixtures. C2a changes them as `materialization-map.json` records. No existing fixture verdict changes (the audit).
- **Not claimed:**
  - No product code, generator, test or build was run.
  - The audit uses jsonschema, not the generated Rust shape. They agree on the parent across the whole fixture, which is the evidence that they implement the same schema.
