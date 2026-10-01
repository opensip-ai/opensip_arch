Grok review: X12b, policy-pack admission on the host side (law X12 r3 items 1, 5, 7 and 8, with item 10's host cases), with inventory v109 on v105. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-policy-pack-x12b-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

Law: `docs/implementation/m2/policy-admission-x12/PROPOSAL.md` r3 (accepted by you on 2026-10-01; the reviewed bytes are `PROPOSAL-r3.md`; the file adds only the "r3 ACCEPTED" note). Its "Units after the law" gives X12b: `crates/host/src/configuration.rs` with `admit_policy_selection`, the termination mapping into 468 r5 item 6's shape, the X12-0 remedy on rows 1, 2 and 3a, and the host tests. Its two dependencies are integrated:
- **X12a** (evaluator, product b642c45, your review `reviews/grok-policy-pack-x12a-r1/`): `admit_pack`, `AdmittedPack`, `PackRefusal`, `PackDefect`, `PackSource`. Its judgment call 1 has the host pass its embedded schema registry; call 6 fixes the row 4 subjects; call 14 hands the selection count, the remedy bytes, the generated-enum mapping and the `configuration.rs` pins to this unit.
- **X12-0** (contract successor, product b880e83, your review `reviews/grok-config-remedy-x12-0-r1/`): the widened `PUBLIC_ROUTE_REMEDIES["CONFIG.INVALID"]` string, which X12b embeds and tests byte for byte.

The routing precedent is 468c (`existing-root-admission-468/PROPOSAL.md` item 6; `host/src/installation_termination.rs`; `host/src/doctor_ingress.rs`).

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x12b`, detached at 0206ce8 (X2c integrated, inventory v105 selected). Nothing is committed; the two new files are intent-to-add. Save `git -C <worktree> diff` as product.diff and report its sha256. Lead's value: e68c5235956ff358512ab015581de366bf3d78f547c9a9914d33b866fd9a7bd0, 28067 bytes, 5 files, 648 insertions and 7 deletions.
- **Arch:** v109 (parent v105): `policy-pack-x12b-inventory-v109-subject.json` and `policy-pack-x12b-inventory-v109/`. These are untracked until acceptance. v106 and v108 are in flight, and v107 is not this unit's.

**Rebase before review.** The change was first built and tested on b880e83 (X12-0's lock entry). X2c then integrated at 0206ce8, touching only `security/custody`, `platform/lib.rs` and the lock, so the same change was moved onto 0206ce8 with no conflict, and v109 was first built there, on v105. `build_v109.py` reads both the parent and the successor record that bound the sixteen inherited rows from the lock, so a later parent needs only a rerun.

## What it does

All new code is in the host. It is pure: no I/O, lock, ledger or callback.

- **`configuration.rs` (items 1, 5 and 8).** The planned owner of the configuration resolver, created with the M2 slice only.
  - `pub(crate) fn admit_policy_selection(selection: &[PackSource<'_>]) -> Result<AdmittedPack, PolicySelectionRefusal>`.
  - It runs, in order: the count (exactly one source, else `Count(n)`, before any source is read); `crate::embedded_schema_registry()` (a failure is row 4); then `admit_pack(&schemas, source)`. The evaluator's `AdmittedPack` is returned unwrapped, and its `PackRefusal` is carried unchanged as `PolicySelectionRefusal::Pack`.
  - `pub(crate) fn policy_selection_termination(&PolicySelectionRefusal) -> InstallationTerminationV1` is item 7's mapping. It is an exhaustive match with no wildcard arm, one arm per row:

    | Refusal | Class / exit | Error code / fault | Detail | Subject |
    |---|---|---|---|---|
    | `Count(n)` (row 1) | request-rejected / 2 | `CONFIG.INVALID` / none | `CONFIG.INVALID` | `count:<n>` |
    | `NotBundled` (row 1) | request-rejected / 2 | `CONFIG.INVALID` / none | `CONFIG.INVALID` | the presented ID |
    | `SuppliedPack` (row 2) | request-rejected / 2 | `CONFIG.INVALID` / none | `CONFIG.INVALID` | `supplied:<p>:sha256:<hex>` |
    | `ImperativeMember` (row 3) | request-rejected / 2 | `CONFIG.INVALID` / none | `POLICY.IMPERATIVE_KEY_REFUSED` | the pointer |
    | `SuppliedInvalid` (row 3a) | request-rejected / 2 | `CONFIG.INVALID` / none | `CONFIG.INVALID` | `supplied:<p>:sha256:<hex>` |
    | `HostInvariant` (row 4) | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `HOST.INVARIANT_VIOLATED` | `pack:<packId>` (or the supplied subject) |

  - `REMEDY_CONFIG_INVALID` is the X12-0 string (367 ASCII bytes, sha256 `f6e37558…5bd8e`). `REMEDY_IMPERATIVE_KEY` is "the policy DSL is declarative data only", the command inventory's remedy for `POLICY.IMPERATIVE_KEY_REFUSED` that law item 7 quotes.
- **The remedy path (`doctor_ingress.rs`).** The only product code that renders a termination row's public remedy is `doctor_ingress::refused_envelope` → `row_remedy` → `detail_json`.
  - `doctor_envelope`'s refused arm becomes `pub(crate) fn failure_envelope(request_id, correlation, row)`, which doctor still calls; the tail (exit from class, correlation, `Envelope7Root` projection) becomes a private `project`. Doctor's output is byte-identical; its tests pass unchanged.
  - `row_remedy` gains two arms: `Detail::ConfigInvalid => REMEDY_CONFIG_INVALID` and `Detail::PolicyImperativeKeyRefused => REMEDY_IMPERATIVE_KEY`. Row 4 uses the existing `HOST.INVARIANT_VIOLATED` remedy. Before this change `row_remedy` refused both details as a projection error.
- **`lib.rs`** declares `#[allow(dead_code)] mod configuration;` (private; nothing calls it before M3).
- **`Cargo.toml`** moves `opensip-evaluator` from dev-dependencies to dependencies. The edge is already in the inventory's host package row; Cargo.lock does not change.

## Judgment calls: please rule on each

1. **The count comes first.** Item 7 puts zero or several sources in row 1 but does not order it against the per-source checks. The count is checked before the schema registry and before any source is read, so two sources, one of them imperative, are `count:2`, not row 3. This is the narrowest reading: the evaluator sees only a well-formed selection. Rejected: admitting each source and reporting the first refusal (it reads bytes the selection never admitted).
2. **A schema-registry failure is row 4 with the evaluator's subject.** `embedded_schema_registry()` cannot fail on the pinned embedded sources; if it does, it is signed-core fault. It becomes `PackRefusal::HostInvariant { subject, defect: PackDefect::Registry }`, the variant whose doc already names "a classifier or schema-registry fault". `host_fault_subject` gives `pack:<presented id>` or `supplied:<p>:sha256:<hex>`, X12a call 6's subjects, and a test checks the supplied form against the evaluator's own `subject()`. The registry is built on each call, with no `static` or `OnceLock`, so admission takes no lock (item 8). Rejected: caching it (a lock), and a host-only refusal variant (a second row 4 shape).
3. **The termination shape is `InstallationTerminationV1`.** Item 7 maps "into 468 r5 item 6's termination shape". That shape is the existing struct (class, exit, error code, fault cause, detail, subject), so it is reused, not copied. Its name is 468's. Rejected: a parallel `PolicySelectionTerminationV1` (two structs for one shape, and two envelope paths).
4. **One remedy path.** The X12 rows render through doctor's `refused_envelope` and `row_remedy`, which are factored into `failure_envelope`, not through a second table. The remedy text constants live in `configuration.rs` as the owner of the rows, and `row_remedy` keys them by detail, as it does every other row. Rejected: a separate X12 renderer, which would let the remedy diverge from the published path.
5. **Row 3's and row 4's remedies.** Row 3 carries "the policy DSL is declarative data only", the text item 7 quotes (`command-inventory.v3.json`, row `policy-test-imperative-key`). Row 4 carries the existing host-invariant remedy. Note: that inventory's `policy-test-suite-inadmissible` row also pairs `CONFIG.INVALID`/`CONFIG.INVALID` with its own remedy. That row is the `policy test` command's golden and no product code emits it; the law and X12-0 fix the remedy these rows carry. I read no contradiction, but please confirm.
6. **A subject beyond `BoundedText` is never truncated.** `DomainDetail.subject` is at most 1024 characters, and a presented ID or pointer can be longer. The termination keeps it verbatim, and `failure_envelope` refuses to project it (`MetadataError::Projection`). This follows doctor's precedent (`a_finding_too_long_for_a_bounded_subject_is_not_producible_never_truncated`). The public outcome of a non-projectable refusal belongs to CLI enablement. Rejected: truncating, or substituting a digest (both change the law's subject).
7. **Control characters in a presented subject.** A row 1 subject can contain a newline (law item 3's own test case). JSON carries it exactly. The human renderer writes `Subject: <text>` unchanged, so a newline there splits the line. That is the existing renderer's behavior for every subject, and no CLI is wired, so I leave it to CLI enablement. Rejected: escaping in this unit, which changes the shared renderer.
8. **Item 8's ordering, without an analysis request.** No analysis request exists in M2 (X11 ends on the not-implemented refusal), so nothing calls `admit_policy_selection` yet. X12b provides what can be shown now: admission is pure (source pin: no I/O, environment, process, lock, `static`, ledger, fence, custody, storage, platform, security, provider, facts, Coverage, Plan, replay or evaluation call), its internal order is count, registry, `admit_pack`, and a refusal returns before any `AdmittedPack` exists. Putting the call first in the request is the M3 analysis request's obligation. Rejected: wiring a call site now.
9. **The host's positive and row 4 cases.** The release registry has zero rows, and the evaluator's test registry is `cfg(test)` in another crate, so through the host every Named source is row 1 and nothing admits. The host tests assert the evaluator's test ID is row 1 here, which shows the test registry is unreachable from the host. The admission itself is X12a's positive test. Row 4 is mapped and rendered from a `PackRefusal::HostInvariant` built directly for each of the eight `PackDefect` causes. Rejected: a host seam to select a registry (forbidden by the law's bundling rules).
10. **The host → evaluator edge becomes a normal dependency.** It was a dev-dependency. The inventory's host package row already lists `opensip-evaluator`, so the package graph is unchanged and `check_package_edges --lane host` passes. Cargo.lock does not change.
11. **`#[allow(dead_code)]` on the module.** Both functions are `pub(crate)` per item 5 and have no caller before M3. The security crate's unwired library modules use the same attribute. The remedy constants are live, because doctor's `row_remedy` uses them.
12. **`configuration.rs`'s planned row is kept by value.** Its description, "Resolve admitted configuration layers, registry selections and provenance.", stays true: the policy selection is a registry selection, and layers and provenance arrive in M3 in the same file (item 1). The only new row is the test file, included the way `doctor_ingress.rs` includes its tests.
13. **The test reads the evaluator's fixture.** `configuration_tests.rs` uses `include_bytes!` on `crates/evaluator/tests/fixtures/policy-pack-test-fixture.policy.json` for item 10's "byte-identical to the test pack's bundled document". It does so in test only.
14. **The source pin is text-based.** On `configuration.rs` without its test module, it asserts:
    - one `opensip_evaluator` import, exactly `{AdmittedPack, PackDefect, PackRefusal, PackSource, admit_pack}`;
    - one `admit_pack(`;
    - exactly two `crate::` uses: `InstallationTerminationV1` and `embedded_schema_registry()`;
    - none of the forbidden tokens, ignoring comment lines;
    - the order count < registry < `admit_pack`;
    - no `_ =>` arm.

## Tests

`configuration_tests.rs` has 11 tests:
- **NT-1, first limb.** Each of 12 IDs is `NotBundled`, giving row 1 with that ID as subject: `opensip.preview.typescript.pack:1` itself, `:2`, the bare name, `:01`, uppercase, mixed case, a trailing newline, a leading space, a wrong name, `:01`, the empty string, and the evaluator's test ID.
- **NT-1, second limb.** The test pack's exact bytes, its canonical re-encoding, and those bytes with a newline, under both provenances, are row 2 with the supplied subject.
- **NT-2.** `script`, `hook`, `exec` and `include` at the top level and in a rule, and a string `emitWhen`, under both provenances, are row 3 with the pointer and `POLICY.IMPERATIVE_KEY_REFUSED`. A WASM blob, a shell script, empty bytes, a duplicate key and policy v1 are row 3a.
- **Selection count.** Zero, two (Named twice, and Named with an imperative Supplied) and three sources are row 1, `count:<n>`.
- **Exhaustive mapping.** Every row (1, the count, 2, 3, 3a, and row 4 once per `PackDefect`) has its class, exit, error code, fault cause and detail. Each parses as its generated `Common4D9Class`, `Common4D9ErrorCode`, `Common4D9FaultCause` and `Common4DomainDetailCode` member. `POLICY.UNKNOWN_RULE` and `IMPORT.ABSENT_FOR_PREDICATE` are members too.
- **Remedy and envelope.** The constant is 367 ASCII bytes with the X12-0 sha256. For every row, `failure_envelope` gives a `kind: failure` envelope that is valid against the selected command-envelope v7 source schema, with an exit equal to the row's. `termination.domainDetail` and `errors[0]` are exactly `{code, remedy, subject}`, with the X12-0 remedy on rows 1, 2 and 3a. `faultCause` appears only on row 4, and the human rendering is exactly the expected lines.
- **Bounds.** A 1025-character ID is kept verbatim in the termination, and the envelope refuses it; 1024 characters render.
- **The host fault subject.** It equals the evaluator's own subject forms.
- **Source pin.** Judgment call 14.

## Checks

- Full workspace on 0206ce8 plus this change (`cargo test --locked --offline --workspace`):
  - 1389 passed, 0 failed, 3 ignored, on two clean runs (runs 3 and 4).
  - Host lib is 108, which is 97 plus the 11 new tests.
  - One earlier run (run 2) had one failure in an untouched security test, `installation_observation::tests::every_capture_phase_refuses_actual_mutations`, with `Capture { component: 6, error: Changed }`. Three other worktrees were running their suites at the same time; it did not recur.
  - Before the rebase, one run on b880e83 plus this change gave 1376 passed, 0 failed, 3 ignored.
- Clippy `--workspace --all-targets -D warnings` is clean on 0206ce8. `cargo fmt --all --check` is clean, and so is `rustfmt --edition 2024 --check` on `configuration_tests.rs`.
- `~/Library/Application Support/OpenSIP` is absent before and after.
- `check_package_edges --lane host` against v109 passes. The host's declared internal edges include `opensip-evaluator` as a normal edge.
- verify_projection against the real lock (0206ce8, which selects v105): 16 rows, 83 corruptions refused.
- verify_scratch (v109 appended over the real lock): passed, 71 inventory successors, 72 contract successors, 16 inheritance rows, v109 selected.
- `build_v109.py` reruns produce the same bytes.

## Decide

- Does X12b implement X12 r3 items 1, 5, 7 and 8, host side, and item 10's host cases, exactly? In particular:
  - `admit_policy_selection` is `pub(crate)`, returns the evaluator's `AdmittedPack` unchanged, and has no host wrapper;
  - the mapping is exhaustive, row for row, with existing codes only;
  - rows 1, 2 and 3a carry the X12-0 string byte for byte, through the product's one remedy path;
  - a bundled imperative member can only surface as row 4;
  - admission is pure and reaches no evaluation, provider, facts, Coverage or custody;
  - no CLI is wired.
- Rule on the judgment calls, in particular 1, 3, 4, 5, 6 and 8.
- Is v109 right on v105?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of `policy-pack-x12b-inventory-v109-subject.json`;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v109, parent (the v105 pin), successorRecord (the pin of `policy-pack-x12b-inventory-v109/successor.json`)}.

Write REVIEW.md and review.json. Do not commit.
