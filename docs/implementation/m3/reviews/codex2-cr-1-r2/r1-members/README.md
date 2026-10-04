# CR-1 — component roles and closure kinds (contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted.** It is a design unit: it edits only arch, and changes no product file, code, class, exit code, route or public code. It needs Codex's `ACCEPT-DESIGN-UNIT` and the lead's root assent before it can be bound in the product's `design-lock.json`.

**What it is.** Accepted law **M3-C** names successor **CR-1** (MC:1053): "security / DR-103 host vocabulary successor; security owner with D4 | Item 7's role-to-kind table; widening the manifest `role` enum | C2a; F4 and G2 closure manifests". Item 7 (MC:360-396) fixes the table. It says that "Widening the role enum is successor CR-1, owned by security and DR-103, and joined with D4's `components/manifest.rs`" (MC:380). Owner question R2 (MC:1211) asks the security and DR-103 owner to confirm it. Three other units depend on it:
- E1 needs the `grammar` role for E2b's real admission (ME:697);
- M3-D's D4 admits "every `analyzer`-role component, with the role closures of MC item 7's table" at R10a (MD:718);
- CR-1 and CRC-1 must both be accepted before C2a (MC:1076, MC:1086).

**Law standing.** As for CRC-1: this unit was commissioned against r6 (`8274bca1…`), and CODEX2 accepted r7 (`a1ee9386…`) during drafting. r7 leaves item 7 and the successor rows word for word, and this README cites r7's lines.

**Product.** Main `9c11c53`, read only, with 79 contract successors. Main has since moved to `cd5958b` (82); see "Evidence runs".

## Short names

- **MC** M3-C r7, accepted: `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r7.md` (157,110 bytes, `a1ee9386…`).
- **ME** M3-E1 r3, accepted: `docs/implementation/m3/syntax-e/PROPOSAL-r3.md` (`d71031ff…`).
- **MD** M3-D r3, accepted by GROK2: `docs/implementation/m3/supervisor-d/PROPOSAL-r3.md` (`9679dbc4…`).
- **CRC-1** is the sibling unit, `docs/implementation/m3/snapshot-plan-c/crc-1/`.
- **CMS** is the completed structural manifest schema, `docs/coop/completion/manifest-schema.completed.v1.json` (24,193 bytes, `a5140714…`). It is **not** a `verify_design` input. The architecture application `docs/coop/completion/architecture-application.v1.json` (an accepted input, `15b3932a…`) pins it in clause `M.SCHEMA`. The product carries the same bytes as its security generation input, `tools/security/inputs/manifest-schema.json`, from which `crates/security/src/generated/component_manifest_shape.rs` is generated.
- **CMC** is CMS's completion contract, `docs/coop/completion/manifest-completion.contract.v1.md` (`da2b00f5…`). It is not a `verify_design` input either.

The parents, both accepted inputs of the lock at `9c11c53`:
- **SL** `docs/v2/contracts/product-v1/security-and-lifecycle.md` (119,915 bytes, `a319da39…`).
- **DR103** `docs/coop/artifacts/component-manifest-schemas.v11.json` (139,492 bytes, `1c0b8868…`). This is the accepted DR-103 field authority. Its `role` field is `/manifestSchema/fields/7`.

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: the three overrides with exact `before` and candidate `after`, and the copy's one edit |
| `successor.json` | the contract successor record: two parents, three passage overrides, no supersession, eight candidates |
| `completion/manifest-schema.completed.v1.json` | generated: the complete successor copy of CMS |
| `materialization-map.json` | generated: the product bytes C2a copies, and the product files C2a changes with them |
| `evidence/copies-report.json` | generated: the copy's parent and selection, its one edit, its serialization, and the role-case audit |
| `evidence/build_cr_1.py` | builds every generated file, the record, the subject manifest and the unit draft; `--check` compares instead of writing |
| `evidence/check_cr_1.py` | read-only, independent content checks |
| `evidence/verify_scratch.py` | runs the real `verify_design` with a synthetic review and assent, alone or after CRC-1 (`--after-crc-1`) |
| `../cr-1-subject.json` | the subject manifest (generated) |
| `../cr-1-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`; not part of the subject |

## What changes

There are three passage overrides, and each only inserts text. There is also one complete successor copy. `PASSAGES.md` has the full texts.

| # | Parent | Line or pointer | Change |
|---|---|---|---|
| 1 | SL `docs/v2/contracts/product-v1/security-and-lifecycle.md` | 70 | After S1's closure-association paragraph (SL:21-70), a new block, **Component roles and closure kinds**. It holds the closed role-to-kind table, word for word MC:370-376, and its rules: the kind comes only from `role`; a role/field kind mismatch refuses; `evaluator`, `detector`, `adapter` and `core` are never roles; and the four non-`analyzer` roles are **closure-only** (below). |
| 2 | DR103 `docs/coop/artifacts/component-manifest-schemas.v11.json` | `/manifestSchema/fields/7/type` | appends the M3 vocabulary: `analyzer`, `toolchain`, `stdlib`, `rust-dev-llvm`, `grammar`, each fixing the `closure2` kind through SL S1's table |
| 3 | DR103 | `/manifestSchema/fields/7/semantics` | appends that the four roles beyond `analyzer` are closure-only |

**The successor copy.** `completion/manifest-schema.completed.v1.json` is CMS with exactly one edit, at `/properties/role`. `{"const": "analyzer"}` becomes `{"enum": ["analyzer", "toolchain", "stdlib", "rust-dev-llvm", "grammar"]}`, in the table's order. It keeps CMS's own serialization (`json.dumps(indent=2)` plus LF; the parent is byte-identical to that form). It is 24,293 bytes, `ef991be7…`. `$id` and every other byte are unchanged.

Nothing else changes: no code, class, exit, public code, inventory, registry, generated file or product file. C2a materializes the copy (`materialization-map.json`).

## The rule

| Manifest `role` | `closure2` `kind` | Launched by the host as a component? |
|---|---|---|
| `analyzer` | `provider` | yes, as a provider session |
| `toolchain` | `toolchain` | no: closure-only |
| `stdlib` | `stdlib` | no: closure-only |
| `rust-dev-llvm` | `rust-dev-llvm` | no: closure-only |
| `grammar` | `grammar` | no: closure-only |

- **Where the kind comes from.** It comes only from `role`, through this closed table. It is never asserted by a caller, inferred from a path or file name, or taken from any other field (MC:384).
- **Kind mismatch.** A closure whose role maps to a kind other than its selecting field requires (IDS `closureKinds.byField`) refuses (MC:380; MC's control C2-T2).
- **Roles that do not exist.** `evaluator`, `detector` and `adapter` are never manifest roles, and `core` is never a role or an identity closure kind. The in-core closures are CRC-1's and EC1's projections of the authenticated core inventory (MC:378).
- **Closure-only roles.** The host never launches such a component through its manifest; it reads the component's tree only as retained closure bytes. So a closure-only manifest:
  - declares `capabilities: []`, since a capability declaration is an analyzer role subprotocol;
  - requests `permissions: []`;
  - has a platform `entrypoint` that names a committed regular file under RJ-3's path and presence rules. It need not be executable, and the host never executes it;
  - has its commands never mounted or dispatched.
- **Tools inside a closure.** A tool the host launches from a closure-only tree, such as C3b's cargo adapter, is launched under its own launch law (the D law), never as a component session.
- **Every other DR-103 rule** applies to every role alike.
- **Refusals.** A violation refuses through the manifest owner's existing schema (RJ-6), capability, permission and path refusals. No code is added.

## Why this form

- **SL:70 is free.** SL's bound overrides are at lines 109, 166-298, 619, 685, 711, 845, 917, 953, 977 and 1323. None is inside S1's lines 19-70.
- **DR103 has no bound override.** Its two role strings are fresh JSON Pointer keys. `build_cr_1.py` checks both facts against the lock at `9c11c53`.
- **CMS cannot be a parent.** `contract_successor` admits a parent only if it is accepted, and CMS is not in the lock's accepted set. So the copy is an ordinary candidate at a new path. The record's `standing` selects it as the completed manifest schema, and CMS becomes historical. This is B-S9's selection form, and I1-L's copy form for the bytes.
- **The copy really is CMS's successor.** `build_cr_1.py` asserts that its parent bytes are exactly the pin in the application's `M.SCHEMA` clause, the product's generation input at `9c11c53`, and the product `sources.json` row.

## Role-case audit

Widening the enum must not turn an existing negative case positive. The checks are in `evidence/copies-report.json`, and `check_cr_1.py` recomputes them:
- **The arch completion cases** (`manifest-cases.completed.v1.json`): the one role-setting case, `TYPE/role`, sets `builder`, which is still outside the enum.
- **The product shape fixture** (`crates/security/tests/fixtures/manifest268-shape.ndjson` at `9c11c53`): all 55 role cases are invalid, and none uses a CR-1 role. They are `null`, booleans, numbers, `""`, `[]`, `{}`, `invalid` and an absent role, across five base manifests.
- **The product semantic fixture** (`crates/security/tests/fixtures/manifest268-semantic.ndjson`): `REQUIRED/role` and `TYPE/role` stay invalid.

## Lead decisions

Each decision is dated 2026-10-04 and made under the owner's standing direction. Each names the alternatives it rejects, and the owner may reverse any of them.

**LD-1. The table lives in SL S1, and the vocabulary in DR-103's role field.** S1 is where a component-manifest closure becomes a `closure2` (SL:27-48). DR-103 makes the role vocabulary host-owned (DR103 `role.type`).
- **Rejected:** the table in BP or IE, since security owns component admission and identity owns kinds, not roles;
- **Rejected:** a new standalone registry file, which would be a second owner of one vocabulary.

**LD-2. The executable form is a complete successor copy of CMS that widens `role` to a five-role enum, with `$id` and `manifestSchemaVersion` unchanged.**
- **Why it is safe:**
  - the change is additive, and no existing manifest changes meaning (see the audit);
  - an old host still refuses a new role (fail closed);
  - the product generator supports `enum` (`tools/security/generators/manifest_shape.py`, which emits an `||` of constants).
- **Rejected:**
  - **a schema major bump.** No existing manifest changes, as with I1-L's additive member under an unchanged major.
  - **per-role `oneOf` branches in the root.** They would duplicate twenty fields per role. CMS's `$comment` already puts cross-field and host-policy checks in separate semantic phases, which is where the closure-only rules belong.
  - **overriding the application's `M.SCHEMA` pin strings.** That would rewrite an application record's evidence pins, and CMS still could not be a parent.

**LD-3. The four non-`analyzer` roles are closure-only, with four field rules: no capability, no permission, a regular-file entrypoint that need not be executable and is never executed, and no mounted command.** Without these rules the widened roles could not be admitted lawfully:
- **The executable-entrypoint check.** CMC:125 says "Entrypoints resolve to committed executable files", and the product owner enforces it (`crates/security/src/component_manifest.rs:337`, `ENTRYPOINT_NOT_EXECUTABLE_FILE`). Under that rule, a `stdlib` or `grammar` component would have to ship a dummy executable: an execution surface with no purpose. For a grammar closure it is impossible anyway. E1's grammar tree is closed from two declared roots and refuses unrelated files (ME item 4, ME:177-215; its r3 change E-R2-02), so it cannot carry an extra executable.
- **Capabilities.** A toolchain could otherwise declare analyzer capabilities, a claim no host contract serves.

**Rejected:**
- (a) **no per-role rule**, for the reasons above;
- (b) **dropping `entrypoint` or `commands` for these roles.** That is a structural change across DR-103's required fields, RJ-2's root-name binding and BP:704's "RJ-3 entrypoint";
- (c) **a second manifest `kind` for closure components.** `kind` is the constant `component`, so a new kind is a release-format change;
- (d) **executable entrypoints for `toolchain` only.** Nothing launches a toolchain component through its manifest either. The D law launches a tool from the closure tree by its own rules. "Need not be executable" still lets a toolchain name its compiler.

**LD-4. `evaluator`, `detector` and `adapter` never become roles, and `core` never does.**
- **Rejected:** a `detector` role now for third-party detectors. X12 and DR-131 admit no user or third-party packs, and the core's detector is CRC-1's projection.

**LD-5. The selection is declared in the record.** CR-1's copy is the selected completed manifest schema. CMS and CMC's sentence "The initial role vocabulary remains exactly `analyzer`. … no auxiliary/build role is invented." (CMC:19-20) become historical, as do CMC:89's "new role" and CMC:125's executable-entrypoint sentence where they apply to closure-only roles.
- **Disclosed:** `verify_design` does not enforce selection, so a later unit that edits CMS instead of the copy is caught only by review (B-S9's residual hazard).
- **Rejected:** leaving CMS current, which would leave the product's generation input contradicting SL S1.

**LD-6. No new refusal code.**
- An unknown role is RJ-6 (closed schema), as today.
- The closure-only rules use the owner's existing capability, permission and path refusals (`Error::Capability`, `Error::Permission`, `Error::Path`).
- **Rejected:** new codes, under the owner's no-new-codes rule.

**LD-7. Materialization and binding.** C2a materializes CR-1, because item 7's admission is C2a's (MC:1086). It:
- copies the bytes;
- re-pins `tools/security/inputs/sources.json`;
- regenerates `component_manifest_shape.rs` through `tools/generate_security_tables.py`;
- makes the executable-entrypoint check role-scoped;
- adds the closure-only checks;
- applies the table in closure admission.

D4 consumes the result at R10a (MD:718). After acceptance the lead binds CR-1 in a binding-only product commit, before C2a.
- **Rejected:** binding inside C2a's commit, which would mix review subjects.

## Controls proposed for C2a

These are for C2a's review. MC's C2-T1 to C2-T5 still apply.
- **CR-T1.** One manifest per role admits, through item 7's production path, with the table's kind.
- **CR-T2.** Role `builder` refuses RJ-6 (existing). Each of `evaluator`, `detector`, `adapter` and `core` as a role refuses RJ-6.
- **CR-T3.** A closure-only manifest with a non-empty `capabilities` or `permissions` refuses.
- **CR-T4.** A closure-only manifest whose entrypoint is a regular file with mode `0644` admits. The same entrypoint on an `analyzer` manifest still refuses `ENTRYPOINT_NOT_EXECUTABLE_FILE`. A directory or symlink entrypoint refuses for every role.
- **CR-T5.** A role-to-field kind mismatch refuses (C2-T2), for example a `grammar` closure named as a view producer.
- **CR-T6.** A source pin shows that the generated role node is the five-role enum, and that no closure-only component reaches a launch or command mount.

## Cross-law items

1. **E1 (E2b, the grammar bundle).** The real and synthetic grammar manifests use role `grammar`, with `capabilities: []` and `permissions: []`. The lead recommends that the entrypoint name the bundle manifest at its fixed path `opensip-interface/grammar/bundle-manifest.v1.json` (ME:182). That is a committed regular file and a declared root of the closed tree, and it is never executed. The one root command is declared as the schema requires and is never mounted.
2. **F4 and G2 (toolchain, stdlib and rust-dev-llvm manifests).** They follow the same closure-only rules (MC:1053).
3. **M3-D (D4 at R10a).** MD:718 already admits "the role closures of MC item 7's table". D4's exclusions EE-1 to EE-5a (MD:728-731) apply to closure-only manifests too. Because closure-only commands are never mounted, a closure-only root command is never a mounted root command.
4. **C2a's synthetic signer (MC item 8)** writes manifests that satisfy CR-1 for every role.
5. **CRC-1.** The two units cross-reference each other by name and share no parent, so they bind in either order.

## Points for the reviewer

- **R1 (MC R2).** Is SL's table exactly MC item 7's, and are its rules MC:368-385, nothing more?
- **R2 (LD-3).** Are the closure-only rules right and minimal? In particular: the role-scoped executable entrypoint; `capabilities: []` and `permissions: []`; commands never mounted. Is any field rule missing that a closure-only manifest needs?
- **R3 (LD-2, LD-5).** Is the CMS copy, with its selection declared in the record, a sound successor of a schema that `verify_design` does not track? Is the role-case audit complete?
- **R4.** Well-formedness under `verify_design`'s `contract_successor` and `successor_chain` rules, alone and after CRC-1.

## Binding

CR-1 binds on the `verify_design` at main `9c11c53`, on top of all 79 contract successors, alone or after CRC-1, with no prerequisite. After `ACCEPT-DESIGN-UNIT`:
1. copy the review to `docs/implementation/m3/reviews/codex-cr-1-r1/review.json`;
2. complete `cr-1-unit.json`;
3. append the four pins to the product lock;
4. run plain `verify_design`.

## Evidence runs

Every run used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, read only. Nothing ran cargo, a test, a generator or a product tool other than `verify_design` in the scratch harness.
- **`evidence/build_cr_1.py`**, twice. The second run's `--check` reported identical bytes.
- **`evidence/check_cr_1.py`**: pass.
- **`evidence/verify_scratch.py --rev 9c11c53`**: 79 to 80, passes, with three overrides, no supersession, and the inventory (`v134`) and inheritance (55) unchanged. With `--after-crc-1`, 79 to 81, it passes.
- **Against main `cd5958b`** (B-S2, B-S9, I1-P and X4-F1 bound since; 82 successors), all pass:
  - `evidence/verify_scratch.py` on the checkout: 82 to 83, with generation and admission sources verified;
  - `evidence/verify_scratch.py --rev cd5958b`;
  - `evidence/check_cr_1.py --rev cd5958b`.

  The record stays built on `9c11c53`, the review base.

## Not changed, and noted

- **`closure2.protocolMajor`.** No accepted text says which manifest field supplies it for any role. CR-1 changes no compatibility field, and C2a's projection applies one rule to every role.
- **BP:701-709** already lists provider, toolchain, stdlib, rust-dev-llvm and grammar artifacts as component manifests with an RJ-3 entrypoint. It is consistent with CR-1, so it is not changed.
- **The product files are unchanged**: `component_manifest.rs`, the generated shape and the security inputs. C2a changes them.
- **Not claimed:**
  - No product code, generator, test or build was run.
  - No manifest was validated with a JSON Schema engine. The copy's structural change is proved by its diff and by the audit.
