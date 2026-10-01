# X12a r1 — bundled policy-pack admission, evaluator side

Code review of law X12 r3 items 2 to 7 and 9, evaluator side, at worktree `opensip-x12a` HEAD `9dbefb918aa2fb10848e6203fb0cb79338c7ce2f`. No repository edits. The OpenSIP support directory is absent. `product.diff` is 71108 bytes, sha256 `aa57d1e68c78e911e20532a3c068ad23478dd1519ac29629c3e6f57dec3a7ea8`, matching the lead pin. The seven product files match `hashes.txt`. Accepted law bytes are `PROPOSAL-r3.md`, 26705 bytes, sha256 `11628912f6bb63de9c8255178f2b5833163179f114b6f7a563c32871d34822ff`.

## What holds

The release registry is `pack-registry.json` compiled with `include_bytes!`, zero rows and an empty documents table. `RELEASE_PACKS` is the only registry the two public functions pass. The synthetic row `opensip.test.fixture.pack:1` lives in `policy_pack_tests.rs`, which `policy.rs` includes only under `cfg(test)`. A source pin on `policy.rs` requires the release literal, seven `include_bytes!(` calls, one `PackRegistry {` literal, `&RELEASE_PACKS` exactly twice, and none of the test-registry or runtime-read spellings. `opensip.preview.typescript.pack:1` is `NotBundled` with that exact subject.

`Named` matches `packId` with `==`. A wrong name, `:2`, a bare name, `:01`, `:+1`, an empty version, case changes, a newline, spaces, NUL and the empty string stay `NotBundled`. `Supplied` always returns after items 6.1 to 6.3, including the bundled document's exact bytes, its canonical re-encoding and those bytes plus a newline. The subject is `supplied:<user|third-party>:sha256:<hex>` of the raw presented bytes.

The document checks run in order: `parse_json`, the classifier, then `PolicyDocumentV2` admission. A caller document's undeclared member or string expression is `ImperativeMember` with that pointer. The same defects in a bundled document are `HostInvariant` with subject `pack:<packId>` and `PackDefect::Imperative`, which is row 4 (RF-1). A `Named` failure of lexical, schema, digest, rule law, contribution or the step budget is the same row. `AdmittedPack` has private fields, no `Clone`, `Default`, deserialization or public constructor, and the `compile_fail` doctest refuses a field literal. `check_plan_pack` reads the retained Plan and its analysis-spec, requires exactly one bundled `policyPackIds` entry, and requires `plan.policyDigest` to equal that row's `policySha256`. `replay_run` does not call it.

The `Meter` move preserves `step`: depth 0 or an exhausted step count is `Limit`, and depth is not decremented. `compile_program` takes the policy digest the Plan already carried. `inspect_policy_program`, `inspect_evaluator_parameters` and `compile_plan_policy` keep that value.

## Judgment calls

1. **`admit_pack` takes `&RegisteredSchemas`.** Item 6.3 needs closed-schema validation, and the evaluator owns no registry. `from_sources` refuses any source whose length or SHA-256 differs from `source_requirements`, and it is the public constructor. The parameter gives the caller no schema authority. X12b keeps `admit_policy_selection(selection)` and passes the host registry. Holds.

2. **The classifier includes the three pinned schema sources.** `RegisteredSchemas` does not expose the document publicly (`document` is crate-private). `policy.rs` includes `policy-v2`, `common-v1` and `imported-v1`, rechecks each length and SHA-256 against `source_requirements`, and rechecks the policy document digest against the supplied registry's `PolicyDocumentV2` handle. A mismatch is row 4. Holds.

3. **Position is the closed `PolicyDocumentV2` alternative.** The classifier roots at `$defs/PolicyDocumentV2` and expands `$ref`, `oneOf` and `anyOf`. `if`/`then` in this schema only refine properties the parent already declares (`cmp`, `value`, `n`, `ordinal`), so leaving them out of the declaration set admits a lawful document and leaves the refinement to schema validation. An object at a non-object position declares nothing, so `/rules/0/severity` holding `{"exec": …}` yields `/rules/0/severity/exec`. A string is imperative when at least one alternative exists and every alternative is object-typed: `emitWhen`, `ruleProgramRef`, `subjectEnumeration`, a rule and `operands/1`. A string at an array position, including `subjectEnumeration.include`, is a shape failure (row 3a). A numeric `emitWhen` is row 3a. A root string is row 3 with pointer `""`. `script`, `hook`, `exec` and a top-level or in-rule `include` are undeclared. Object keys are visited in `BTreeMap` order, and `/` and `~` are escaped as `~1` and `~0`. Holds.

4. **The classifier runs before `schemaMajor`.** A policy document whose members are the four `PolicyDocumentV2` names and whose `schemaMajor` is 1 passes the classifier and fails closed-schema validation, so it is row 3a. A member that definition does not declare is row 3. The schema-major rule in workflows-and-surfaces §5 governs `policy test` and candidate admission. This boundary follows item 6's order. Holds.

5. **The supplied subject hashes raw bytes.** Rows 2 and 3a share `supplied:<provenance>:sha256:<hex>`. Row 3a bytes need not be JSON, so the digest is of the presented bytes. Holds.

6. **A host fault on `Supplied` is row 4 with the supplied subject.** A classifier pin mismatch, a schema-registry fault or the closed-schema work limit can be reached while classifying caller bytes, and those bytes have no `packId`. The variant is `HostInvariant` and the subject is the supplied digest subject. On `Named`, including a registry that fails self-consistency before a row matches, the subject is `pack:<presented id>`. A byte-exact match makes that the row's `packId`. Holds.

7. **Registry self-consistency fails closed.** The keys, the ascending `packId` order, the name syntax `[a-z][a-z0-9._-]*`, version `1..=2^32-1`, `packId == name + ":" + decimal(version)`, lowercase digest, non-empty strictly ascending contributions, and the one-to-one document table are all required. Any failure is row 4 for every `Named` source. An empty registry with an empty table is consistent and returns `NotBundled`. Holds.

8. **Item 6.6 checks `RuleProgramV2`.** `compile_program` output is admitted against `#/$defs/RuleProgramV2` and then `check_program_laws`. A shape failure is row 4. The test pack's program digest is `41f496a3b9f4d7ada615e517f9bcfb0a3c439323328f3ba19205a7a8a4fb7048`. Holds.

9. **The limits cover a schema-valid document.** `PACK_TRAVERSAL_STEPS` is `2^27`. One rule's first pass is at most 5 evidence rows and 64 predicate nodes, and each atom is at most `1 + 16 × (1 + 64)` steps; the program pass repeats the predicate walk. 512 rules over both passes, plus compilation and the contribution walk, stay under `2^27`. `PACK_SCHEMA_WORK` is `2^30`, more than 250 units per byte of a 4 MiB document. The 512-rule, 61-node fixture admits. A hit is row 4. Holds.

10. **The corpus id is `fixture.file-observed`.** The plan fixture's analysis-spec record, copied from `budget-one-packet`, has `policyPackIds` equal to that one string. The law's `"fixture"` does not appear in that record. The test refuses the unchanged corpus Plan as `PLAN_POLICY_PACK_NOT_BUNDLED` and derives test-pack Plans by rewriting the ids and recomputing `analysisSpecDigest`, `policyDigest` and the Plan id. Holds.

11. **The test schema registry reads pinned sources.** `schemas()` is inside the `cfg(test)` module. It reads paths from `source_requirements()` and `from_sources` rechecks every pin. `policy.rs` has no `std::fs`. Holds.

12. **`AdmittedPack` has item 5's four fields.** `pack_id`, `policy_digest`, `program` and `program_digest`, with accessors only. The bundled policy bytes have no accessor. Item 5 does not require one. Holds.

13. **The source pin matches the release text.** The assertions listed in the request hold against `policy.rs` and `pack-registry.json`, including seven `include_bytes!(` calls: `import-registry.json`, `atom-registry.json` twice, the pack registry and the three schema sources. Holds.

14. **Evaluator side only.** `PackRefusal` is the row, not a termination record. Selection count, the `CONFIG.INVALID` remedy, the generated-enum mapping and the `configuration.rs` pins are absent here. Holds.

## Inventory v104

v104 is 355127 bytes, sha256 `1c8dbb12bbede3304b66e378b8565f51811660cd9e8836f0e05729eb721eda7c`. Parent v101 is 351480 bytes, sha256 `929729cec92e383bdc8e571bf45179ac518bf96082e4244ff941808e157c7f18`, the inventory the worktree lock selects. The successor record is 20426 bytes, sha256 `cdfb34bb4fb44ad24c884519c7ac1209aa13377ae5b757cba80fc2b5a8c5ad01`. The candidate has 783 files. The 778 shared paths are equal by value, packages and pending decisions are unchanged, and the standing sentence names X12a. The five added rows are the release registry, the `cfg(test)` tests, and the three fixtures. No crate edge is added: `check_package_edges --lane host` against v104 passes, and the evaluator's only internal edge is `opensip-identity`. `verify_projection` against the worktree lock reports 16 rows and 83 corruptions refused. `verify_scratch` appends v104 over that lock and reports 69 inventory successors, 71 contract successors, 16 inheritance rows, and v104 selected.

## Replay

`cargo test --locked --offline -p opensip-evaluator --lib`: 31 passed, 0 failed, including the 12 pack tests and the 512-rule admission. `cargo test --doc -p opensip-evaluator`: 3 passed, including the `AdmittedPack` compile_fail doctest. `cargo clippy --locked --offline -p opensip-evaluator --all-targets -- -D warnings` passed. `rustfmt --check --edition 2024` on `lib.rs`, `policy.rs` and `policy_pack_tests.rs` passed. The workspace suite and workspace clippy were not replayed.

## Verdict

ACCEPT-UNIT. Inventory v104 ACCEPT on v101. No required finding.
