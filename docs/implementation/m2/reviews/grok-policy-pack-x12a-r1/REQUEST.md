Grok review: X12a, bundled policy-pack admission on the evaluator side (law X12 r3 items 2 to 7 and 9, with item 10's evaluator cases), with inventory v104 (parent v101). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-policy-pack-x12a-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

Law: `docs/implementation/m2/policy-admission-x12/PROPOSAL.md` r3 (accepted by you on 2026-10-01; the reviewed bytes are `PROPOSAL-r3.md`). Its "Units after the law" splits X12 into X12-0 (the `CONFIG.INVALID` remedy text), X12a (this unit), X12b (the host: `configuration.rs`, the termination mapping, the remedy, the host tests), and X12c and X12d at M3. X12a depends on nothing beyond the current product. X12-0 and X12b are not in this request.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x12a`, detached at 9dbefb9 (X3b-2 integrated, inventory v101 selected). Nothing is committed; the five new files are intent-to-add. Save `git -C <worktree> diff` as product.diff and report its sha256. Lead's value: aa57d1e68c78e911e20532a3c068ad23478dd1519ac29629c3e6f57dec3a7ea8, 71108 bytes.
- **Arch:** v104 (parent v101), `policy-pack-x12a-inventory-v104-subject.json` and `policy-pack-x12a-inventory-v104/`. These are untracked until acceptance. v104 was first built on v102 at 920941b; X3b-2 (v101) then integrated, so the product change was rebased onto 9dbefb9 (the diff is byte-identical) and v104 rebuilt on v101 with the same five rows. Succession is by the lock's parent pin, not by number. v103 is unassigned.

## What it does

All new code is in `crates/evaluator/src/policy.rs` (the law names it as the evaluator owner and rejects a separate `packs.rs`), exported from `lib.rs`. It is pure: no I/O, lock, ledger or callback.

- **The bundled registry (items 2 to 4).** `pack-registry.json` is compiled in with `include_bytes!`, with an empty documents table. In M2 it has **zero rows**, so every named pack, including `opensip.preview.typescript.pack:1`, is refused as not bundled. Rows are `{packId, name, version, policyDocument, policySha256, contributions}`, and each document is a sibling `include_bytes!` entry in a static table. The registry's self-consistency is checked on every `Named` admission (judgment call 7).
- **The boundary types (item 5).**
  - `PackSource<'a>` is `Named(&str)` or `Supplied { bytes, provenance }`, with `SuppliedProvenance { User, ThirdParty }`.
  - `AdmittedPack` has private fields (packId, policy digest, compiled `RuleProgramV2`, program digest) and accessors only. It has no `Clone`, `Default`, deserialization or public constructor, and a `compile_fail` doctest guards it.
  - `PackRefusal` has one variant per row of item 7: `NotBundled` (row 1), `SuppliedPack` (2), `ImperativeMember` (3), `SuppliedInvalid` (3a) and `HostInvariant { subject, defect }` (4). `subject()` gives the row's subject. `PackDefect` is the diagnostic cause inside row 4.
  - The termination shape, codes, details and remedy are X12b's.
- **`admit_pack(schemas, source)` (item 6).**
  - A `Supplied` source runs 6.1 (`parse_json`), 6.2 (the classifier) and 6.3 (closed-schema validation against `#/$defs/PolicyDocumentV2`). It is then refused whatever its bytes, including the bundled document's exact bytes: row 2, or row 3 or 3a on a failure.
  - A `Named` source is matched byte for byte (no trim, case-fold or zero-stripping), otherwise row 1. Then, on the bundled bytes, it runs 6.1 to 6.3, 6.5 (canonical bytes hash to `policySha256`), 6.6 (`compile_program`, the program's `RuleProgramV2` shape and the existing `check_program_laws`) and 6.7 (every `contributionId` is in the row's set). Any failure there is row 4 with subject `pack:<packId>`, never row 3 (RF-1).
- **The imperative classifier (item 6.2).** This is workflows-and-surfaces §5's rule, read positionally from the pinned policy schema closure.
  - The alternatives at a position are the leaves of `$ref`, `oneOf` and `anyOf`.
  - A member is imperative when no object alternative there declares it in `properties`.
  - A string is imperative when every alternative there (at least one) is object-typed.
  - The subject is the JSON Pointer of the first such member in canonical (BTreeMap) order.
  - The classifier refuses to run (row 4) on a schema node it cannot read as closed.
- **`check_plan_pack(inputs, plan_id, budget)` (item 9).** It reads the retained Plan and its analysis-spec record, then requires that `policyPackIds` is exactly one ID, that the ID is a bundled row, and that `plan.policyDigest` equals that row's `policySha256`. It uses the existing `PolicyAdmissionError`:
  - `Refused("PLAN_POLICY_PACK_COUNT" | "PLAN_POLICY_PACK_NOT_BUNDLED" | "PLAN_POLICY_PACK_DIGEST")`;
  - `RegistryLaw`, `Limit` and `Record`.

  Choosing row 4 or `EVALUATION.INPUT_REFUSED` is the caller's job. It is not wired into `replay_run` or `replay_candidate`.
- **Refactor.** The private step counter moves out of `PolicyReader` into a `Meter`, so the rule and atom laws (`atom_law`, `rule_law`, `check_program_laws`) and `compile_program` (which now takes the policy digest rather than the Plan) run without retained inputs. `inspect_policy_program`, `inspect_evaluator_parameters` and `compile_plan_policy` behave the same; their host tests pass unchanged.
- **Test-only registry.** The synthetic registry has one row, `opensip.test.fixture.pack:1` (contribution `fixture`), over the golden-typescript policy blob of `plan-policy-fixtures.json` (raw SHA-256 `24e41265…`). It is declared only in `policy_pack_tests.rs`, which policy.rs includes as `#[cfg(test)] #[path] mod pack_tests;`. Internal `admit_from` and `check_plan_pack_in` take the registry. The public functions pass `&RELEASE_PACKS` and nothing else.

## Judgment calls: please rule on each

1. **`admit_pack` also takes `&RegisteredSchemas`.** Item 5 writes `admit_pack(source)`, but item 6.3 requires closed-schema validation, and the evaluator owns no schema registry: it is host-owned, as for every other evaluator owner that receives it through `RetainedInputs`. `RegisteredSchemas::from_sources` refuses any source that is not the exact pinned bytes, so the parameter gives the caller no authority over the law. X12b's `admit_policy_selection(selection)` keeps its signature and passes the host's embedded registry. Rejected:
   - the evaluator compiling its own registry: all 49 sources at every call;
   - a hand-written shape check: a second schema source.
2. **The classifier's schema closure.** The classifier needs the schema document itself, which `RegisteredSchemas` does not expose publicly. policy.rs therefore includes `schemas/sources/policy-v2`, `common-v1` and `imported-v1` with `include_bytes!` (the host's own include path). It rechecks each one's length and SHA-256 against `RegisteredSchemas::source_requirements()`, and the policy schema's digest against the supplied registry's `PolicyDocumentV2` handle. A mismatch is row 4. Rejected:
   - a new public accessor in identity: another crate's surface;
   - a hand-written member table: a second source of the DSL.
3. **The classifier's reading of "at that position".**
   - `if`/`then` conjuncts are conditional refinements under a closed parent, not declarations.
   - An object at a position with no object alternative declares nothing, so its members are imperative. For example, `/rules/0/severity: {"exec": …}` gives `/rules/0/severity/exec`.
   - A string is a string expression only if at least one alternative exists and all are object-typed. So a string at an array position is not imperative, but a string `emitWhen`, rule, `ruleProgramRef`, `subjectEnumeration`, or a string inside `operands` is.
   - A non-string scalar at an object position, such as `emitWhen: 7`, is a shape failure, row 3a.
   - A JSON root that is a string is row 3 with the empty pointer `""`.
   - The classifier is positional, so `subjectEnumeration.include` (the DSL's glob list) is declared: a wrong type there is row 3a. A top-level or in-rule `include` is row 3. The law's "covers script, hook, exec and include keys" holds at every position where the schema does not declare that name.
4. **Classifier before `schemaMajor`.** Item 6 runs 6.2 before 6.3, and 6.3 assigns a `schemaMajor` other than 2 to `CONFIG.INVALID`. So a policy-v1 document that uses only v2-declared members is row 3a, but one carrying a member v2 does not declare is row 3. workflows-and-surfaces §5's "another major … is never grammar-classified" (`REQUEST.SCHEMA_MAJOR_UNSUPPORTED`) governs `policy test` suite and candidate admission, not this boundary, so I read no contradiction with X12. Please confirm.
5. **Supplied subject digest.** `supplied:<provenance>:sha256:<hex>` hashes the presented raw bytes, not canonical bytes, because row 3a bytes need not be JSON. Rows 2 and 3a share the one form.
6. **Row 4 on a `Supplied` source.** A host fault can be reached with supplied bytes: a classifier pin mismatch, a schema-registry fault, or the closed-schema work limit. It is row 4 with the supplied subject, because there is no packId. On a `Named` source the subject is `pack:<presented id>`, including a registry self-inconsistency found before matching. Because matching is byte-exact, that equals the row's packId whenever a row matches.
7. **Registry self-consistency.** The registry is self-consistent only if all of these hold; any failure is row 4 for every `Named` source:
   - the keys are exactly `{schemaVersion: 1, standing, rows}` and the row's six keys;
   - rows are strictly ascending by packId;
   - `name` matches `[a-z][a-z0-9._-]*`, with no colon, so `<name>:<version>` parses one way;
   - `version` is an integer from 1 to 2^32-1;
   - `packId == name + ":" + decimal(version)`;
   - the digest is lowercase hex;
   - contributions are non-empty and strictly ascending, with the same name syntax;
   - every row names exactly one table document, and every table document is named by exactly one row.
8. **6.6 also checks the compiled program's `RuleProgramV2` shape,** as `compile_plan_policy` does. A failure is row 4.
9. **Limits.** The classifier has no step counter: parse_json already bounds it to 4 MiB and depth 32, and `$ref` expansion is bounded to depth 32. Two named private constants cover the rest:
   - `PACK_TRAVERSAL_STEPS` = 2^27, for 6.6 and 6.7. The bound is 512 rules × (5 evidenceUse rows + 65 nodes × (1 + 16 × 65)), over two passes, which is about 6.8 × 10^7;
   - `PACK_SCHEMA_WORK` = 2^30, for 6.3, which is over 250 units per byte of a 4 MiB document.

   A test admits a 3.79 MB document of 512 rules, each a 61-node predicate, through all seven steps.
10. **The corpus value.** The law says the corpus names `"fixture"`. Its analysis-spec records actually name `"fixture.file-observed"`, and the test uses that value. `plan-policy-fixtures.json` Plans carry no analysis-spec record, so the `check_plan_pack` fixture copies a Plan and its analysis-spec unchanged from `evaluator-parameter-fixtures.json` case `budget-one-packet`. The test-pack Plans are derived in the test: rewrite `policyPackIds`, then recompute `analysisSpecDigest`, `policyDigest` and the Plan ID through `IdentityCandidate`.
11. **The test schema registry.** The evaluator cannot depend on host, so its test module reads the pinned schema sources from the repository with `std::fs`, under `cfg(test)` only. The paths come from `source_requirements()`, and `from_sources` rechecks every pin. It reads repository files only.
12. **`AdmittedPack` holds exactly item 5's four fields.** It has no accessor for the bundled policy bytes, which the M3 Plan builder will need to retain as the policy blob. That accessor belongs with X12c/M3, if the law adds it.
13. **The source pin is on policy.rs text.** It asserts:
    - the release literal `rows: include_bytes!("pack-registry.json"), documents: &[]`;
    - exactly 7 `include_bytes!(` (the existing atom and import registries, the pack registry and the three schema sources);
    - exactly one `PackRegistry {` literal;
    - `&RELEASE_PACKS` exactly twice, once in each public function;
    - no `TEST_PACKS`, `tests/fixtures`, `opensip.test`, `std::`, `fs::`, `env::`, `getenv` or `home_dir`;
    - the `cfg(test)` module declaration;
    - zero rows and no `opensip.test` in `pack-registry.json`.
14. **Evaluator side only.** These item 10 cases need the host and are X12b's: the selection count (zero or two sources), the `CONFIG.INVALID` remedy bytes, the exhaustive mapping to generated enums, and the "no evaluation" pins on `configuration.rs`. Item 7's rows are represented here as `PackRefusal` variants, not as termination records.

## Tests

`policy_pack_tests.rs`, 12 tests, plus the `compile_fail` doctest:
- **NT-1, first limb.** Each of these is `NotBundled` with the exact presented ID as subject:
  - under the test registry: a wrong name, `:2`, the bare name, `:01`, `:+1`, an empty version, `:1`, `:01`, upper and mixed case, a trailing newline, leading and trailing spaces, NUL and the empty string;
  - under the release registry: `opensip.preview.typescript.pack:1` and its variants, and the test ID itself.
- **NT-1, second limb.** The test pack's exact bytes, its canonical re-encoding and its bytes with a newline are `SuppliedPack` for both provenances under both registries. The subject is `supplied:<p>:sha256:<hex>`.
- **NT-2.**
  - `script`, `hook`, `exec` and `include` at the top level, in a rule, as an object value in a rule, and under `emitWhen` and `ruleProgramRef` are `ImperativeMember` with the pointer. `script`, `hook` and `exec` under `subjectEnumeration` are too.
  - String expressions at `emitWhen`, `ruleProgramRef`, `subjectEnumeration`, a rule and `operands/1` are `ImperativeMember`.
  - Canonical-order selection and pointer escaping (`/a~1b~0c`) are checked.
  - These are `SuppliedInvalid`: a WASM blob, a shell script, empty bytes, a duplicate key, a float, policy v1, a bad severity, a numeric `emitWhen`, and a string `subjectEnumeration.include`.
- **Positive.** The test pack admits. Its policy digest is `24e41265…`, and its program digest is `41f496a3…`, the same as `compile_plan_policy`'s golden digest for that blob. Admission is deterministic.
- **Bundled defects.** Each of these is `HostInvariant { subject: "pack:opensip.test.fixture.pack:1" }` and never `ImperativeMember`: a digest mismatch, an unregistered contribution, a rule-law failure (unknown relation), imperative bundled members (`/rules/0/exec`, a string `emitWhen`, `/script`), lexical, schema (v1) and a limit (1 step).
- **Self-inconsistent registries.** 14 cases are row 4. An empty registry with an empty table is consistent and gives `NotBundled`.
- **Release self-check.** There are zero rows and the table is empty; every release row would run all seven steps. The same loop admits the test row.
- **Source pin** (judgment call 13).
- **Classifier.** It loads the pinned three-document closure; the root alternative declares exactly the four members; the test document is clean; an object at a scalar position is flagged; a root string is flagged.
- **DSL bound** (judgment call 9).
- **`check_plan_pack`.**
  - The corpus Plan is `NOT_BUNDLED` under both registries.
  - The test-pack Plan with the matching digest joins.
  - The same Plan is `NOT_BUNDLED` under the release registry.
  - Two other digests are `DIGEST`.
  - Zero and two IDs are `COUNT`; the bare name is `NOT_BUNDLED`.
  - Zero steps is `Limit`, and a broken registry is `RegistryLaw`.

## Checks

- X12a tests: 12/12 and the doctest pass.
- Full workspace, two runs on 920941b plus this change: 1354 passed, 0 failed, 3 ignored, each time (baseline 1341, plus 12 tests and 1 doctest). After the rebase, one run on 9dbefb9 plus this change: 1366 passed, 0 failed, 3 ignored (9dbefb9 adds X3b-2's tests; this change adds the same 12 tests and 1 doctest).
- Clippy `--workspace --all-targets -D warnings` and fmt are clean.
- `~/Library/Application Support/OpenSIP` is absent.
- `check_package_edges --lane host` against v104 passes on 9dbefb9.
- verify_scratch (v104 appended over the real lock at 9dbefb9, which selects v101) passes: 69 inventory successors, 71 contract successors, 16 inheritance rows, v104 selected.
- verify_projection against the real lock: 16 rows, 83 corruptions refused.
- `build_v104.py` reruns produce the same bytes.

## Decide

- Does X12a implement X12 r3 items 2 to 7 and 9, evaluator side, exactly? In particular:
  - zero release rows, and no test row or test registry reachable from a release build;
  - byte-exact identity, with no normalization;
  - no `Supplied` bytes admitted, including the bundled bytes;
  - a caller's imperative member or string expression is row 3 with the pointer, and a bundled one is row 4 (RF-1);
  - the declarative order 6.1, 6.2, 6.3, then 6.4 to 6.7;
  - `AdmittedPack` cannot be forged;
  - `check_plan_pack` is provided but not wired into replay.
- Rule on the judgment calls, in particular 1, 2, 3, 4 and 6.
- Is v104 right on v101?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `policy-pack-x12a-inventory-v104-subject.json`;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v104, parent (the v101 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.

**Lead note on ordering.** X3b-2 (inventory101) integrated at product 9dbefb9 before this request was sent, so this request already judges v104 on v101. `build_v104.py` maps both v102 and v101 to the records that bound their sixteen rows, and reads the parent from the lock.
