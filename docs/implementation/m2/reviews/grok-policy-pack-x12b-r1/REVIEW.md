# X12b r1 — host policy-pack admission

Code review of law X12 r3 items 1, 5, 7 and 8, with item 10's host cases, at worktree `opensip-x12b` HEAD `0206ce8673ade3689331fe22801458a03646f502`. No repository edits. The OpenSIP support directory is absent. `product.diff` is 28067 bytes, sha256 `e68c5235956ff358512ab015581de366bf3d78f547c9a9914d33b866fd9a7bd0`, five files, 648 insertions and 7 deletions, matching the lead pin. The five product files match `hashes.txt`. Accepted law bytes are `PROPOSAL-r3.md`, 26705 bytes, sha256 `11628912f6bb63de9c8255178f2b5833163179f114b6f7a563c32871d34822ff`. The change sits on X2c's lock entry with no conflict. `Cargo.lock` is unchanged.

## What holds

`admit_policy_selection` is `pub(crate)` and returns the evaluator's `AdmittedPack` directly. `PolicySelectionRefusal` adds only the selection count; a one-source refusal is `Pack(PackRefusal)` unchanged. The module is private. Nothing in the host or the CLI calls it. Admission order is the count, then `embedded_schema_registry()`, then one `admit_pack(&schemas, source)`.

The count match refuses zero or several sources before the registry is built and before any source is read. Two sources, one of them imperative, are `count:2`. A schema-registry error becomes `PackRefusal::HostInvariant` with `PackDefect::Registry` and `host_fault_subject`: `pack:<presented id>` for `Named`, and the supplied digest subject for `Supplied`. The registry is built on each call. `embedded_schema_registry` compiles `include_bytes!` sources through `RegisteredSchemas::from_sources`.

`policy_selection_termination` is an exhaustive match with no wildcard. Rows 1, 2 and 3a are request-rejected, exit 2, `CONFIG.INVALID`, fault `none`, detail `CONFIG.INVALID`. Row 3 is the same class, exit and error code, with detail `POLICY.IMPERATIVE_KEY_REFUSED` and the member pointer. Row 4 is operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, fault `host-invariant`, detail `HOST.INVARIANT_VIOLATED`, subject `pack.subject()`. The generated members parse. `POLICY.UNKNOWN_RULE` and `IMPORT.ABSENT_FOR_PREDICATE` stay inside row 4's cause.

`REMEDY_CONFIG_INVALID` is the X12-0 string: 367 ASCII bytes, sha256 `f6e37558f18fda1af2cde5a06c2f61cb853a22ecfed5e57a92c5a2069cc5bd8e`. `REMEDY_IMPERATIVE_KEY` is `the policy DSL is declarative data only`. `doctor_envelope`'s refused arm is `failure_envelope`, and the exit, correlation and `Envelope7Root` projection are the private `project`. `row_remedy` keys `Detail::ConfigInvalid` and `Detail::PolicyImperativeKeyRefused` to those constants. Row 4 uses the existing `HOST.INVARIANT_VIOLATED` remedy. A 1025-character subject stays verbatim on the termination, and `Envelope7Root` refuses it because `Common4BoundedText` stops at 1024 characters (`MetadataError::Projection`). 1024 characters project. `BoundedText` has no pattern, so a newline subject projects and the existing human renderer writes `Subject: <text>` unchanged.

The evaluator returns `ImperativeMember` only for a `Supplied` document. A `Named` document's imperative member is `HostInvariant` with `PackDefect::Imperative` and subject `pack:<presented id>`. The host maps that arm to row 4. The release registry has zero rows, so every `Named` source through `admit_policy_selection` is `NotBundled`, including `opensip.preview.typescript.pack:1` and `opensip.test.fixture.pack:1`.

`opensip-evaluator` moved from `[dev-dependencies]` to `[dependencies]` by deleting the section header. The inventory's host package row already lists that edge. The resolved kind is a normal dependency.

## Judgment calls

1. **The count comes first.** The `[source]` match returns `Count(n)` before the registry and before `admit_pack`. The two-source case with an imperative document is `count:2`. Holds.

2. **A schema-registry failure is row 4 with the evaluator's subject.** `host_fault_subject` matches X12a call 6: `pack:<presented id>`, or `supplied:<provenance>:sha256:<hex>` of the raw bytes. The supplied form equals `PackRefusal::subject()`. There is no `static` or `OnceLock`. Holds.

3. **The termination shape is `InstallationTerminationV1`.** The existing struct is filled in. Its name stays 468's. Holds.

4. **One remedy path.** Rows render through `failure_envelope` and `row_remedy`. The constants live in `configuration.rs`. Doctor's refused arm calls the same function. Holds.

5. **Row 3's and row 4's remedies.** Command inventory `policy-test-imperative-key` carries `the policy DSL is declarative data only` with `POLICY.IMPERATIVE_KEY_REFUSED`. `policy-test-suite-inadmissible` pairs `CONFIG.INVALID` / `CONFIG.INVALID` with `correct the suite so it satisfies PolicyTestSuiteV2`. No product code emits that suite golden. The route table has one `CONFIG.INVALID` string, the X12-0 text, and this unit emits that string for rows 1, 2 and 3a. Row 4 keeps `OpenSIP reached an internal invariant failure. Report this failure.` The 468 custody rows that use error code `CONFIG.INVALID` keep detail `CONFIG.CUSTODY_REFUSED`, so the new arm does not reach them. Holds.

6. **A subject beyond `BoundedText` is never truncated.** The termination stores the presented ID. Projection deserializes `Common4DomainDetail.subject` as `Common4BoundedText`, which refuses more than 1024 characters. Holds.

7. **Control characters in a presented subject.** Law item 3's trailing newline is kept as the row 1 subject. `BoundedText` admits it. The human renderer is the existing `Subject: ` line. No CLI is wired. Holds.

8. **Item 8's ordering, without an analysis request.** The production text has one `admit_pack(`, the embedded registry, and the termination import. The source pin's forbidden tokens are absent outside comments. A refusal returns before an `AdmittedPack` exists. No analysis request calls the function. Holds.

9. **The host's positive and row 4 cases.** The host tests show `opensip.test.fixture.pack:1` is `NotBundled` here. Row 4 is mapped from a `HostInvariant` built for each of the eight `PackDefect` values, with subject `pack:opensip.test.fixture.pack:1`. Holds.

10. **The host to evaluator edge is a normal dependency.** `check_package_edges --lane host` against v109 passes. The declared edge `opensip-host -> opensip-evaluator` has kind `None`. `Cargo.lock` is unchanged. Holds.

11. **`#[allow(dead_code)]` on the module.** The same attribute sits on unwired modules in `security/src/lib.rs`. The remedy constants are live through `row_remedy`. Holds.

12. **`configuration.rs`'s planned row is kept by value.** The description remains `Resolve admitted configuration layers, registry selections and provenance.` The policy selection is the M2 registry selection. Holds.

13. **The test reads the evaluator's fixture.** `include_bytes!` of `policy-pack-test-fixture.policy.json` is inside `configuration_tests.rs`, included only under `#[cfg(test)]`. Holds.

14. **The source pin is text-based.** Against `configuration.rs` above `#[cfg(test)]`: one `opensip_evaluator` import of `{AdmittedPack, PackDefect, PackRefusal, PackSource, admit_pack}`, one `admit_pack(`, two `crate::` uses (`InstallationTerminationV1` and `embedded_schema_registry()`), the order count < registry < `admit_pack`, and no `_ =>` arm. Holds.

## Inventory v109

v109 is 360591 bytes, sha256 `96df355ac8333940a08402feb21e0065a485cd7fd9f128fd470a83677c639e7c`. Parent v105 is 359222 bytes, sha256 `ebd9cf3361d4f854adcfbe8fcffd8e6e5ca9bd0af38315f950638212b5934a08`, the inventory the worktree lock selects. The successor record is 20123 bytes, sha256 `c1198f43cc5ae0f0309567ac31cad20f75ddd40355440badbce53cad0eeb47a9`. The candidate has 786 files. All 785 v105 rows are equal by value. Packages and pending decisions are unchanged. The standing sentence names X12b. The one added row is `crates/host/src/configuration_tests.rs`, role `test`, sorted between `configuration.rs` and `delivery.rs`. The sixteen description overrides stay bound to v105, with candidate pointers shifted by that one insertion. `verify_projection` against the worktree lock reports 16 rows and 83 corruptions refused. `verify_scratch` appends v109 over that lock and reports 71 inventory successors, 72 contract successors, 16 inheritance rows, and v109 selected.

## Replay

`cargo test --locked --offline -p opensip-host --lib`: 108 passed, 0 failed, including the ten `configuration::tests` and the doctor ingress tests. `cargo clippy --locked --offline -p opensip-host --all-targets -- -D warnings` passed. `rustfmt --edition 2024 --check` on `configuration.rs`, `configuration_tests.rs`, `doctor_ingress.rs` and `lib.rs` passed. `check_package_edges --lane host` against v109 passed. The workspace suite and workspace clippy were not replayed.

## Verdict

ACCEPT-UNIT. Inventory v109 ACCEPT on v105. No required finding.
