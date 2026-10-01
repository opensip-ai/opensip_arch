# Review: store endpoint X3a-1 with inventory v83

Verdict: REQUIRED-FINDINGS. One code finding. Inventory v83 is accepted.

Worktree `/Users/sb/code/opensip-ai/opensip-x3a1` is HEAD `84a8bfd7b4f28a52fc18bc9e66e02d1f40330d2c`, the same commit as the product tree. `product.diff` is `git diff` of that worktree, including the two intent-to-add sources: 86836 bytes, sha256 `53991d82f5f3646aa70ae70b40ed529fb9704518469eb60bc1c13f781f89cf81`. The real OpenSIP support directory was absent before the verifiers, before the tests, and after the tests.

Law is X3a r5. The decide line names r4 items 1 to 7; r5 is the accepted text of those items, and its only amendment is that a creator invocation produces no endpoint. This review judges the code against that text. Item 4's host-reader adoption is X3a-2.

## Required finding

RF-1. A chain that has not ended after 64 nodes is the incomplete row when the pair generation makes G+1 equal 64.

`lineage_bound` returns `(MAX_LINEAGE_NODES, true)` only when `generation + 1` is greater than 64. At generation 63 the bound is `(64, false)`. `inspect_supplied` returns `Limit` once 64 nodes have been read and the last node still has a predecessor. The gate maps that `Limit` through `lineage_limit(false)` to `Incomplete(Chain)`. The observation session records a `Chain` finding on the same flag. A non-doctor writer or reader then ends on `CONFIG.CUSTODY_REFUSED` subject `installation-incomplete`, exit 2. Doctor lists a chain defect and its chain remedy. Item 3 requires the budget row for a chain longer than 64: operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `WORK.BUDGET_EXHAUSTED`, host-invariant. A session-limit stop is that ordinary failure, and it produces no chain finding.

The budget tests select generation 64, which is 65 nodes and takes the greater-than branch. The 64-node cost tests select generation 63 on a chain that ends at a root, so they pay for 64 nodes and then refuse `CurrentStore` because the trust record still names generation 0. They never hit `Limit`. A chain that still has a predecessor after those 64 nodes is untested.

Required: when the walk stops because 64 nodes were read and the chain has not ended, the row is the budget row even when G+1 equals 64. `Chain` remains the row only when the walk stops at a generation bound strictly below 64. A chain that ends within 64 nodes is unchanged.

## What matches the law

`SelectedStoreEndpoint` is borrowed from the fenced session. `validate_endpoint` runs in memory on that session's ledger and checks the receipt closure, the core's state writer, the marker's store id, a single root reached from `(S, G, K)`, and `C.store` against the admitted triple. The module's production text names no file read, and `the_admission_reads_no_file` pins that. `SuppliedChain::into_nodes` only moves the nodes the supplied walk already decoded. `Node::decode` still refuses a bad cap, non-canonical bytes, a split root pair, a self-predecessor, and a mis-bound key.

The gate's step 2 reads the pair, marker, nodes, and `state.v1` once and retains the decoded values plus the full `DescriptorMetadata`. Step 5 and the later admission call `recheck_files` on those samples. An in-place rewrite that changes `changed` is `CustodyRefusal::Changed`, subject `required-files-changed`. `state.v1` is read at `CURRENT_STATE_CAP` (`4_194_304`) and decoded by `decode_current_store`, which uses the same `TrustCapsuleV1` parse as the existing capture. Over-cap, empty, or undecodable bytes are `CurrentStore`.

`OrdinaryWriteAdmission::admit_store_endpoint` charges validation on the gate ledger, then runs the gate recheck and the receipt recheck. A refusal releases the fence and returns that row. `ReadSession::store_endpoint` validates on the session ledger and rechecks; any failure latches the session. The creator route names no endpoint producer, and `the_creator_path_produces_no_endpoint` pins that. `Core` and `CurrentStore` map to the incomplete row. `StateSchemaUnsupported` projects as request-rejected, exit 2, `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` / `STATE.SCHEMA_UNSUPPORTED`. Doctor subjects are `installation-incomplete:core` and `installation-incomplete:current-store`, each with one fixed remedy.

## Judgment calls

1. Acceptable. `DurableInstallation` keeps the observed account so the later recheck can rerun the chain check. The ordinary-writer admission keeps the gate. `recheck` and `charged` share that gate ledger. `charged` refuses only a failed ledger, so the latch taken by the first admission does not block the endpoint charge. A second `admit` on the same gate stays refused.

2. Acceptable. The observation records `Core` from the receipt's closure and continues, so doctor can list it. Non-doctor reads go through `retain`, which calls `complete` and turns the first finding into the incomplete row. Doctor calls `observe_with`, maps the findings, and releases without `complete`. The production read path retains; it does not observe and then ignore findings. `CurrentStore` uses the same split.

3. Acceptable. The selected core has one state writer. Stage 1 is schema 1 and stage 2 is schema 2. A pair schema other than that value is `StateSchemaUnsupported`. K is an admission refusal. It is not a doctor finding.

4. Acceptable. `every_capture_phase_refuses_actual_mutations` now expects `Custody(Changed)` for an in-place rewrite of `selection.pair` after open, and the latched assertion covers that phase. The other phases still require an error. The new gate and read-session tests expect the same `required-files-changed` row.

5. Acceptable. This worktree is already on `84a8bfd`, which contains X10's doctor renderer. The diff adds the two finding arms, their remedies, and the schema-unsupported termination. The unproducible report, the envelope, and `observe_installation_for_doctor` stay in place.

6. Acceptable. v83 carries all 754 v82 rows by value, including descriptions, packages, dependencies, and pending decisions. The pack README names the descriptions that omit X3a's additions and defers the direct rows to a later description-only successor and the inherited overrides to VD1. That is the same shape as a carried description that has not yet been refreshed.

## Inventory v83

v83 is 756 files, 320110 bytes, sha256 `4e32a2c7263b6ddcd938f42885b9e567fb13f759ba6871bf2c713b109894781a`. Parent v82 is 754 files, 318189 bytes, sha256 `f2423742f09beb94364085570e1a5b30f60c220c30932b4d3426b3e3994c1154`. The two added rows are `store_endpoint.rs` and `store_endpoint_tests.rs`. No row was removed, and every carried row is equal by value. The successor record is 20153 bytes, sha256 `eb5bde356e02ee44cddea425234bd288979719748890161542176414dc025ab5`. The subject manifest is 2079 bytes, sha256 `f5117c555e654d0de0725b04f900692ca473dd993645538438ca441c46cb30b0`.

`verify_projection.py` against the architecture tree and the worktree lock printed `{"readOnly": true, "projectionRows": 16, "positive": "PASS", "corruptionsRefused": 83, "directParentOverrideIncluded": true}`. `verify_scratch.py` on the worktree printed `passed: true`, 58 inventory successors, 71 contract successors, 16 inheritance rows, and selected `repository-file-inventory.v83.json`. The real lock still selects v82 and X10b. The scratch verifier's synthetic review is its own fixture.

## Replay

Rust 1.95.0, `cargo test --locked --offline`, target directory under this review directory, packages `opensip-security` and `opensip-host`, lib tests. Host: 4 passed (`every_row_projects_to_its_published_route`, both incomplete-installation doctor tests, `every_unreachable_row_is_a_failure_with_its_detail_and_no_report`). Security: 22 passed, of which 19 are this unit's endpoint, join, rewrite, creator, current-record, session-limit, and capture-phase tests. Three others matched the substrings `current_record` or `sixty` and also passed. The 64-node gate and session tests passed their owner-cap asserts. This run did not capture their printed totals. The workspace suite, clippy, rustfmt, and `check_package_edges` were not replayed. Passing these tests leaves RF-1 open: the mis-rowed input is not among them.
