Grok review: unit X3a-2 r1, the read side adopts the selected store endpoint, with inventory v136 on v135 and the unit's description successor. Claude Opus 5.5 leads, and you are the single reviewer. You reviewed law X3a (r1 to r5) and unit X3a-1. Verdicts wanted:
- **ACCEPT-UNIT** on the code and inventory v136, with an `inventoryCandidateAssessment` (`review.json`);
- **ACCEPT-DESIGN-UNIT** on the description successor `read-endpoint-x3a2-descriptions` (`descriptions/review.json`). Law X3a r5 item 8 puts "description overrides for the changed host and storage readers" in X3a-2, and verify_design admits a description change only as a contract successor with its own subject. One review cannot map two subjects, so there are two review files.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-x3a2-r1.
- You own the native lane for this review:
  - Use a CARGO_TARGET_DIR under that directory.
  - Use a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder.
  - Run cargo `--locked --offline`.
- Run git read-only, and only against the worktree named below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- No crash-matrix lead run set is needed or wanted (see "Pins checked", X9).

## Inputs

All inputs are pinned in `hashes.txt`. Laws and plans are pinned by their accepted bytes.

### Law, record and plan

- **The law: X3a r5** (`m2/store-admission-x3a/PROPOSAL.md`). r5 has no `PROPOSAL-r5.md` snapshot, because no r6 was ever written. Its accepted bytes are at arch `dab5881db`: `git show dab5881db:docs/implementation/m2/store-admission-x3a/PROPOSAL.md` is 14850 bytes, sha256 `310197d3…8ba3`, your r5 review's `subjectSha256`. The live file differs only by the acceptance note on line 3 (14885 bytes).
  - **Item 4** (:51-55): the host's `installation_lineage`, `installation_records` and `installation_selection` take the pair, the marker and the chain from the session's `SelectedStoreEndpoint` instead of re-capturing them through `capture_descendant`. Storage's `ProvisionalStoreMarker::read_existing` takes the marker the same way. "Their public behavior is unchanged except that they now inherit item 2's full-sample recheck and item 3's bound. The 458c-b2 source pin is extended so that none of them captures a required endpoint file a second time."
  - **Item 8** (:68-71), X3a-2: "read-side adoption (item 4), the extended source pin, and description overrides for the changed host and storage readers, including `installation_lineage.rs`, whose description owner §9 requires to stop promising per-node markers. Plus an inventory successor."
  - Also used: item 1 (the endpoint is private, not Clone, not serializable, borrowed from one held session; it grants only the base of a later §8 binding), item 2 (one read per session; every session recheck compares the full sample) and item 3 (at most 64 nodes; the budget row past it), and the forbidden substitutes (:73-75).
- **M2-COMPLETE r3** (`m2/M2-COMPLETE-r3.md`, accepted): §3.3's X3a-2 row (:331) and §5 row 13 (:401), the deferral: "a post-M2 unit, due before M3-C1a, by M3 day 10 ... because C1a's snapshot reads go through the selected endpoint". §3.3 also records that `installation_lineage.rs:68` still re-captured through `capture_descendant` at main, and "The description half is already true through an inherited override."
- **M3-PLAN r9** (`m3/M3-PLAN-r9.md`, accepted by GROK2): the carry-in row (:279), "M (inventory successor), before C1a, so by day 10"; and the r7 timing row (:425), where C1a integrates after "B2-c (SX-1, X3a-2)".
- **M3-C r7** (`m3/snapshot-plan-c/PROPOSAL-r7.md`, accepted). It names no X3a-2 requirement. C1a's capture walks the project root (item 2), and "OpenSIP's store and installation ... lie outside the project root" (:349). X3a-2 is a C1a integration dependency through the plan (:425), not through the C law, and C1a needs nothing from it beyond integration.
- **X3a-1** (product `99f1c35`; your `m2/reviews/grok-store-endpoint-x3a1-r1` and `-r2`; inventory83's README). r1 says: "Item 4's host-reader adoption is X3a-2."

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-x3a2`, detached at main `3f6f9a5` (S21). It was cut at `218465f` and moved as main advanced, through `6190e66` (SYN-NS) to `3f6f9a5`. Each of those two commits changes only `design-lock.json`: one more contract successor, with no passage on v135. Nothing is committed. The two new files are intent-to-add, so `git diff 3f6f9a5` includes them.
- **Diff:** `git diff 3f6f9a5` is 238838 bytes, sha256 `068a57816f5a69f3175a5576587210434158e4cea471cce2727c7cf075811dc8`. It covers 12 files, +1062 −809. Of that, the staged `design-lock.json` is +395 −346, and the 11 source files are +667 −463.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, Python `python3.14`.

### Inventory and descriptions

All under `docs/implementation/m2/`, untracked in arch:
- `repository-file-inventory.v136.json` (candidate; parent v135, which the lock at `3f6f9a5` selects);
- `read-endpoint-x3a2-inventory-v136/` (README, builder, lock stager, scratch verifier, projection verifier and its outputs, verifier anchor, successor record);
- `read-endpoint-x3a2-inventory-v136-subject.json`, sha256 `b9d1c0dd14d0ebac3c43337124d01682967fcc9de2ac8a864202008f118f6f20`;
- `read-endpoint-x3a2-descriptions/` (README, builder, `evidence/descriptions.json`, successor record);
- `read-endpoint-x3a2-descriptions-subject.json`, sha256 `23770a586cc9a077c0c7610597499669625f393f817939041f141ce6a6a428f2`;
- `read-endpoint-x3a2-inventory-v136-unit.json` and `read-endpoint-x3a2-descriptions-unit.json`, drafts the lead completes at integration.

## What X3a-2 changes

| File | Change |
|---|---|
| `crates/security/src/installation_endpoint.rs` (new) | `InstallationReadFence::store_endpoint` and `ReadStoreEndpoint<'fence>`, the read side's lent endpoint (below). |
| `crates/security/src/installation_endpoint_tests.rs` (new) | Five native tests on scratch homes (below). |
| `crates/security/src/lib.rs` | Declares `pub mod installation_endpoint` (macOS), beside `installation_observation`. |
| `crates/security/src/custody/installation_read.rs` | `ReadSession::required_filesystem`: the charged sample behind the readers' filesystem samples. |
| `crates/security/src/custody/store_endpoint.rs` | `SelectedStoreEndpoint::selection`, an accessor for the decoded pair. Nothing else. |
| `crates/security/src/installation_observation.rs` | The session-error constructor `session` becomes `pub(crate)`. Nothing else. |
| `crates/security/src/custody/installation_read_tests.rs` | The extended source pin (below). |
| `crates/host/src/installation_selection.rs` | Holds a `ReadStoreEndpoint` instead of a capture. |
| `crates/host/src/installation_records.rs` | Composes the endpoint-backed selection and marker; one session recheck. |
| `crates/host/src/installation_lineage.rs` | The chain is the endpoint's; the caller's bound applies to it. |
| `crates/storage/src/store_root/native_marker.rs` | Holds a `ReadStoreEndpoint` and decodes its marker bytes against the requested S. |
| `design-lock.json` | The staged inventory136 binding and description binding (see "The staged lock"). |

Nothing else changes. No crate gains a dependency or a feature. No crash point, crash scope, `cfg` feature predicate, clock sample, file write, or write-path behavior is added, removed or moved. `installation_trust.rs` is unchanged (judgment call 8).

### The lent endpoint (security)

- **`InstallationReadFence::store_endpoint(&self) -> Result<ReadStoreEndpoint<'_>, Error>`** runs X3a-1's `ReadSession::store_endpoint`: the retained values are validated in memory on the session ledger against the read receipt's selected core, and then one full session recheck runs. It reads no file. A refusal latches the session, and `Error::termination` gives its row.
- **`ReadStoreEndpoint<'fence>`** holds the fence and the `SelectedStoreEndpoint`. It has no public constructor, no `Clone` and no serialization, and it borrows the fence. Two `compile_fail` doctests pin it: `E0505`, use after the fence is dropped, and `E0599`, no `clone`. It lends, with no native step, the decoded pair (`selection`), S from the opened marker (`store_instance`), the marker bytes (`marker_raw`) and the admitted chain (`nodes`, at most 64). These are the session's one read: two lends return the same addresses (test 1).
  - **`recheck`** is the session's full recheck (458c item 5 step 4): the receipt's rechecks, the account, the chain to I, the held fence, and every required file by its full sample. That set includes the pair, the marker, each node and `state.v1`. This is item 2's full-sample recheck.
  - **`selection_filesystem`** and **`marker_filesystems`** run the full recheck, then take charged samples. `selection_filesystem` samples the pair. `marker_filesystems` samples I, the fence carrier and the marker. Each file is reopened no-follow by its name under the retained I and judged private, as the full recheck's required-file limb does. It must still carry the session's full sample, else `required-files-changed`, and its filesystem must be H's. No byte is read, and nothing joins the recheck set.

### The readers (host and storage)

| Reader | Before | After |
|---|---|---|
| `ProvisionalSelection::read_existing` | `capture_leaf("selection.pair")`, decode, recheck | `fence.store_endpoint()` |
| `ProvisionalStoreMarker::read_existing(fence, S)` | `capture_descendant(["stores", S], "store-instance.v1")`, decode, then post-check | Parse S, which refuses before any native step; `fence.store_endpoint()`; then decode the lent marker bytes against S with storage's decoder |
| `ProvisionalInstallationRecords::read_existing` | selection capture, then marker capture, then rechecks | Endpoint-backed selection, then marker bound to the pair's S |
| `ProvisionalInstallationLineage::read_existing(fence, max_nodes)` | Records, then one `capture_descendant` per node, each with a full session recheck | Records, then the endpoint's chain. More than `max_nodes` nodes is `Chain(Limit)`, and `max_nodes == 0` is `Limit` before any native step, as before. No final recheck: the marker's admission ended on one. |
| every `recheck` | The capture's own recheck: held fence, retained edges, file | The session's full recheck: one per operation, never one per node |
| `filesystem` / `contributing_filesystems` | The capture's samples: I, fence, every retained edge, file | I, fence, file, after a full recheck, as above |

Every public type, method, signature and error enum is kept. Two variants are no longer produced and are kept for source compatibility: `installation_selection::Error::Decode` and lineage's `ReadError::Decode`. Lineage's `ReadError::Marker` was already in that state. A pair, marker or node that the session cannot read or decode refuses the fence itself, so it never reaches a reader: a missing or undecodable one is the incomplete row, and an I/O failure keeps its own row.

### Rechecks and cost (item 2's recheck, item 3's bound)

Each reader construction costs one endpoint admission (validation plus one full recheck), and each reader operation costs one full recheck. Records and lineage take two admissions, their selection's and their marker's. Measured on the session ledger (test 1, a one-node fixture home; test 5, a 64-node chain, G 0 to 63, on a 48-deep home), cumulative:

| | Objects | Edges | Bytes |
|---|---|---|---|
| One node: session read | 460 | 9,881 | 14.06 MB |
| One node: + one admission | 624 | 13,206 | 14.54 MB |
| One node: + a second admission | 788 | 16,531 | 15.01 MB |
| One node: + one reader recheck | 952 | 19,851 | 15.48 MB |
| 64 nodes, deep: session read | 3,162 | 49,949 | 17.44 MB |
| 64 nodes, deep: + one admission | 4,474 | 69,682 | 19.15 MB |
| 64 nodes, deep: + a second admission (lineage built) | 5,786 | 89,415 | 20.87 MB |
| 64 nodes, deep: + two reader rechecks | 8,410 | 128,745 | 24.31 MB |

The owner's caps are 65,536 objects, 131,072 edges and 256 MiB. A full recheck costs about 3.3k edges on the fixture home. At the session limit on the deep home it costs about 19.7k, because it reopens and judges all 64 node files. Before X3a-2, each node's capture paid a full recheck, which bounded the readable chain at about 35 nodes (law X3a, Problem). Judgment call 2 is about what is left at the session limit.

### The extended source pin (item 4)

`installation_read_tests.rs`:
- **`no_installation_reader_reaches_i_through_the_uncharged_fence`** (458c item 8's pin) now also covers `installation_endpoint.rs`.
- **`no_endpoint_reader_captures_a_required_endpoint_file_again`** (new) reads the production text of the host's selection, records and lineage readers, storage's marker reader and `installation_endpoint.rs`:
  - None contains `capture_leaf`, `capture_descendant`, `capture_with`, `.capture(`, `ProvisionalHeldFile`, `open_regular`, `read_bounded` or `std::fs`.
  - `.store_endpoint()` appears in exactly the selection reader, the marker reader and the lending module. The lending module calls it once, as `self.session().store_endpoint()`.
  - Records and lineage obtain their endpoint through those readers.

### Tests added, adapted and retired

- **Added, security (`installation_endpoint_tests.rs`):**
  1. `the_fence_lends_the_endpoint_of_its_one_read`: the files' bytes as read, S from the marker, the root node; a second lend at the same addresses; a charged admission; prints the one-node costs.
  2. `an_in_place_rewrite_of_any_endpoint_file_fails_the_readers_recheck`: pair, marker, root node and `state.v1`, each rewritten in place with its own bytes after the read. Each ends `required-files-changed` and latches, and a later `store_endpoint` refuses.
  3. `the_readers_samples_are_hs_and_carry_the_sessions_full_sample`: the samples equal I's sample. After a rewrite, a sample refuses on the custody row before sampling, and latches.
  4. `a_replaced_endpoint_file_refuses_the_sample_itself`: a marker renamed away and replaced at its name. The sample's own check, with no full recheck before it, is `required-files-changed`, and latches.
  5. `a_chain_of_the_session_limit_is_lent_whole_within_the_owners_caps`: the 64-node deep-home table above.
- **Added:** the security pin above, and host `the_callers_bound_on_the_admitted_chain_is_the_supplied_walks`. For rooted synthetic chains of one to four nodes and bounds one to five, `within` passes exactly when `inspect_supplied_lineage` over the same nodes ends at the root, and otherwise both give `Limit`.
- **Adapted, storage:** `native_marker_decode_uses_existing_exact_marker_binding` is the old decode test without its post-check count.
- **Retired, nine synthetic sequencing tests,** whose seams no longer exist because the readers no longer capture:
  - selection: `provisional_selection_decode_rechecks_on_valid_invalid_and_oversize_bytes`, `provisional_selection_changed_observation_wins_even_after_decode_failure`;
  - records: `provisional_records_recheck_first_owner_after_success_and_failed_second_owner`, `provisional_records_failed_final_custody_never_returns_partial_bundle`;
  - lineage: `retained_chain_needs_immutable_nodes_not_intermediate_store_markers`, `missing_intermediate_node_is_a_failure_not_reclaimed_store_success`, `earlier_owner_change_overrides_later_failed_observation`, `final_recheck_cannot_be_skipped_by_cycle_or_limit_refusal`;
  - marker: `native_marker_failed_postcheck_wins_over_valid_mismatched_or_malformed_syntax`.

  Their properties now belong to the session's one read and the admission:
  - an undecodable, oversize or missing pair, marker or node is the session's finding, the incomplete row (`installation_session_tests.rs`: `an_incomplete_installation_reports_every_finding_and_other_reads_end_on_incomplete`, the X3a-1 chain and limit tests);
  - a changed file fails the full recheck, which the admission runs before any decode (tests 2 and 4 above; `store_endpoint_tests.rs`);
  - no intermediate marker is read: the endpoint holds only the opened endpoint's marker, and the pin keeps every capture out of the readers.

Net: workspace tests −2, doc tests +2.

## The staged lock

The lock change is staged in the worktree, as P0 staged inventory135 (`m3/reviews/codex-p0-scaffolds-r1/REQUEST.md`, "The staged lock"). `read-endpoint-x3a2-inventory-v136/evidence/stage_lock_x3a2.py` writes HEAD's `design-lock.json` plus:
- one `inventorySuccessors` entry: parent v135, candidate v136, record `read-endpoint-x3a2-inventory-v136/successor.json`, all real pins. Its review `SCRATCH-X3A2/review.json` (763 bytes, `04c27eed…bcdc`) and assent `SCRATCH-X3A2/assent.json` (620 bytes, `7fe53052…c5bb`) are placeholders.
- `inventoryPassageInheritance` replaced by the one hundred rows re-parented to v136, exactly as the record projects them;
- one `contractSuccessors` entry, last: the description successor, with real record and subject pins. Its review `SCRATCH-X3A2/descriptions-review.json` (150 bytes, `a0ee6b81…44f6`) and assent `SCRATCH-X3A2/descriptions-assent.json` (646 bytes, `676f9267…fc4a`) are placeholders.

The staged lock is 508400 bytes, sha256 `636aa4fc142b5c34c51d6c8a93dcf0d2a349f65de2bcff357affb54c76d35ac9`, in the lock's canonical formatting. The placeholder bytes are those of `evidence/verify_scratch.py`'s synthetic overlay. At integration, the lead:
1. copies your two reviews in, to `m3/reviews/grok-x3a2-r1/review.json` and `.../descriptions/review.json`;
2. completes the two unit records;
3. replaces exactly the four placeholder pins;
4. runs plain `verify_design`;
5. commits.

**Plain `verify_design` on the staged lock refuses,** with "missing or escaping regular file: SCRATCH-X3A2/review.json", which is correct until review. `verify_scratch.py` asserts this refusal. `design-lock.json` stays outside both units' `sourceBoundary`, as in every earlier inventory unit. Its staged bytes are pinned here, and the diff sha covers them.

## Pins checked

- **X9: no row moves, so no run set.**
  - The X9 harness sources (the checker and its test, `crates/platform`, storage's and host's `tests/` with both `required-runs.v1.json`, `commit_tests.rs` and `commit_matrix_tests.rs`, and security's `crash_matrix_sites.rs`, `crash_matrix_census.rs` and `crash_matrix_support`, plus storage's and host's `crash_matrix_support`) are byte-identical between X9-6's C `3d2d5b5` and `3f6f9a5`, and the diff touches none of them (`git diff --stat`, empty both ways).
  - The diff adds no `crash_barrier!`, `crash_scope!`, clock sample, file write or `cfg(feature …)` site. X9-1's `every_test_feature_site_is_on_the_pinned_list` and X9-0's `no_manifest_enables_the_crash_matrix_feature` pass in both workspace runs.
  - **Exercised paths.** Every X9 row drives the write path: `InstallationAt::operation`, the gate, X2, X3a's `admit_store_endpoint` / `join_store_endpoint`, X4, X3b, X2e, commit, recovery and the sweep. None of them reaches `InstallationReadFence`, `ReadSession`, `installation_endpoint.rs`, the host provisional readers or `native_marker.rs`; a grep of every crash-matrix support, census and test source finds no such call. On the write path the diff adds only `SelectedStoreEndpoint::selection`, an accessor that only the read-side module calls. So this diff cannot move the census, the traces or the kill sets that X9-6 accepted and X4-F1 re-confirmed.
  - Security's own census pin, `the_integrated_path_reaches_only_scoped_points_and_its_census_is_pinned`, passes in the crash-matrix feature lane.
- **Dependency policies.** No manifest, lock or feature changes. Both checkers and their suites pass (Lead results).
- **Package edges.** Both new rows are in `opensip-security`. No crate declares a new edge.
- **Generators and lanes.** No generator input, schema or TypeScript lane source changes. verify_design's generation (40) and admission (48) source checks pass in `verify_scratch`.

## Lead results

All lanes ran serially with this diff, a private 0700 TMPDIR and `--locked --offline`. The cargo lanes ran on `6190e66`, and the design, package-edge and dependency lanes on `3f6f9a5` with the staged lock. `6190e66..3f6f9a5` changes only `design-lock.json`, which no Rust source or test reads. `~/Library/Application Support/OpenSIP` was absent before and after. CODEX2 was running I1-a's workspace tests in its own worktree and target directory during the test lanes.

| Check | Result |
|---|---|
| `cargo fmt --all --check` | Clean |
| `cargo build --workspace --all-targets` | Pass |
| Clippy `-D warnings`, workspace `--all-targets` | Clean |
| Clippy `-D warnings`, platform, security, storage and host with `crash-matrix` | Clean |
| Clippy `-D warnings`, security, storage and host with `scenario-fixtures` | Clean |
| `cargo test --workspace --all-targets --no-fail-fast`, run 1 | 1729 passed, 0 failed, 3 ignored (20 test binaries). That is P0's 1731 (`cd5958b` plus P0) less the nine retired tests, plus the seven added. No commit since P0 adds or removes a Rust test. |
| The same, run 2 | 1729 passed, 0 failed, 3 ignored |
| `cargo test --workspace --doc` | 20 passed: P0's 18 plus the two `ReadStoreEndpoint` `compile_fail` doctests |
| `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast` | 1627 passed, 0 failed, 3 ignored (P0's 1629, less two). Includes storage's `commit_tests` (8), host's `commit_matrix_tests` (5), and security's and storage's census pins, without a run set. |
| `installation_endpoint` tests with `--nocapture` | 5 passed; the cost lines in the table above |
| `evidence/verify_scratch.py` (staged mode, `3f6f9a5`) | Passes. Inventory successors 95 → 96 with v136 selected; contract successors 93 → 94; inheritance 100 → 100, equal to verify_design's own projection; 21 supersessions unchanged; the three overrides on rows 122, 123 and 747. The lock with inventory136 alone also passes. Plain verify_design refuses the staged lock at `SCRATCH-X3A2/review.json`, as asserted. |
| Plain `verify_design.py --architecture ../opensip_arch --implementation .` on the staged lock | Refuses: "missing or escaping regular file: SCRATCH-X3A2/review.json" (exit 1). Correct until integration. |
| Plain `verify_design.py` on HEAD's lock (`3f6f9a5`, same product sources) | Passes: v135 selected, 95 inventory and 93 contract successors, 100 inheritance rows, 21 supersessions, 40 generation and 48 admission sources |
| `verify_projection.py` against the real lock at `3f6f9a5` | PASS: 100 rows, 503 corruptions refused |
| `evidence/build_v136.py` and `build_descriptions.py` reruns | Same bytes |
| `check_package_edges.py --lane host`, against v136 and against v135 | Both pass: 12 workspace packages, 22 declared and 20 resolved internal edges, none new |
| `check_package_edges.py --lane rust-provider` against v136 | Passes: `opensip-rust-provider` only |
| `tools/tests/test_package_edges.py` | 14 run, OK |
| `check_dependencies.py --feature-profile security-crypto-workspace` | Passes: 11 dependencies, 8 local sources |
| `check_identity_dependencies.py` | Passes: 8 dependencies, 305 sources |
| `tools/tests/test_dependency_policy.py` | 9 run, OK |
| `tools/tests/test_identity_dependencies.py` | 5 run, OK |

Commands, from the worktree, with `PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`, `CARGO=/opt/homebrew/Cellar/rust/1.95.0/bin/cargo`, `AR=~/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f`, `U=../opensip_arch/docs/implementation/m2/read-endpoint-x3a2-inventory-v136` and `V=../opensip_arch/docs/implementation/m2/repository-file-inventory.v136.json`:

```sh
cargo fmt --all --check
cargo build --workspace --all-targets --locked --offline
cargo clippy --workspace --all-targets --locked --offline -- -D warnings
cargo clippy -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline -- -D warnings
cargo clippy -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline -- -D warnings
cargo test --workspace --all-targets --no-fail-fast --locked --offline   # twice
cargo test --workspace --doc --locked --offline
cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast --locked --offline
cargo test -p opensip-security --lib --locked --offline -- installation_endpoint --nocapture   # the cost lines
nice -n 19 $PY -I -B $U/evidence/verify_scratch.py .
nice -n 19 $PY -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .   # refuses at SCRATCH-X3A2
git show HEAD:design-lock.json > head-lock.json
nice -n 19 $PY -I -B tools/verify_design.py --architecture ../opensip_arch --lock head-lock.json --implementation .
cargo metadata --locked --offline --format-version 1 > host.json
(cd providers/rust && cargo metadata --locked --offline --format-version 1) > provider.json
nice -n 19 $PY -I -B tools/check_package_edges.py --repository . --metadata host.json --inventory $V --lane host
nice -n 19 $PY -I -B tools/check_package_edges.py --repository . --metadata provider.json --inventory $V --lane rust-provider
nice -n 19 $PY -I -B tools/tests/test_package_edges.py -v
nice -n 19 $PY -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --feature-profile security-crypto-workspace
nice -n 19 $PY -I -B tools/check_identity_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --archives $AR --policy tools/identity/dependency-policy.json
nice -n 19 $PY -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo $CARGO -v
nice -n 19 $PY -I -B tools/tests/test_identity_dependencies.py --target aarch64-apple-darwin --cargo $CARGO --archives $AR -v
```

`verify_projection.py` ran against the real lock at `3f6f9a5` (the product checkout's, unstaged): `$PY -I -B $U/verify_projection.py --architecture ../opensip_arch --lock ../opensip/design-lock.json`. `evidence/build_v136.py ../opensip/design-lock.json` and `../read-endpoint-x3a2-descriptions/evidence/build_descriptions.py` were rerun and reproduce the same bytes.

## Inventory v136

- **Contents:** v135 plus two rows, both in package `opensip-security`, not generated, standing `proposed`:
  - `crates/security/src/installation_endpoint.rs`, role `composition`;
  - `crates/security/src/installation_endpoint_tests.rs`, role `test`.

  That gives 971 files, with the 969 v135 rows equal by value. The packages, their edges and the pending decisions are unchanged. Check the two descriptions against the code.
- **Planned rows changed, by value unchanged:** the nine changed source files in the table above. Their bytes change and their rows do not. The description successor gives three of them new text.
- **Projection: one hundred rows**, the lock's one hundred inheritance rows on v135, re-parented by stable file path: sixteen carried from inventory81 onward, D1's thirty-nine with D2's four supersessions folded, and D3's forty-five with its seventeen folded. No bound contract successor has a passage on v135, and none is folded here. The forty-six projected rows sorted after the two inserted paths move by two.
- **Pins:**
  - candidate: 555473 bytes, sha256 `ba124e21d23c8cd100eb2031203fd5c04fd8aeaab056872af54d1fa8c92bacea`;
  - successor record (`read-endpoint-x3a2-inventory-v136/successor.json`): 304956 bytes, sha256 `e93b44a6a77261c0d510f1bb6ee23135fcad0e82f6a5bf2c1f06bb383a5afda0`;
  - parent v135: 553173 bytes, sha256 `ac66ee3bd75ace8f21e3122daacfdb2619fe8bb8a432b083414c14cbe3a0c887`.
- **Order:** the lock at `3f6f9a5` selects v135. Since P0's `5e25d04`, six commits have landed (S18, CR-1, SYN-1, SYN-1F, SYN-NS and S21), none with an inventory successor. The lead reserved v136 for X3a-2.

## The description successor

`read-endpoint-x3a2-descriptions/successor.json` (4933 bytes, sha256 `1e1a1f736db1d387f742626be49bd2c96275c3838b31ba88e5f8f84891096b0e`) has one parent, v136. It carries three `passageOverrides` in D1's form, on plain rows, each `before` being the raw v136 text, and no supersessions. Its candidates are the README, `evidence/build_descriptions.py` and `evidence/descriptions.json`.

| v136 | File | What was false |
|---|---|---|
| 122 | `installation_records.rs` | "S equality is not full S/G/K ... admission": the bundle's values now come from the admitted endpoint. |
| 123 | `installation_selection.rs` | "selection capture", "Does not admit a selected store": no capture remains; the pair comes through the session's admission. |
| 747 | `native_marker.rs` | "on the original native-fenced descendant capture": no capture remains. |

**`installation_lineage.rs` (row 121) is not overridden.** It is an inherited row, so any change would be a VD1 supersession. Its effective meaning, carried from inventory81 onward, already reads "the physically opened selected endpoint store marker ... Admit complete node ancestry ... recheck all contributing original descriptors and latch failures under one operation budget". That stops promising per-node markers (owner §9) and describes the adopted reader, which matches M2C §3.3. Rows that stay true but understate the unit's security additions are listed in that unit's README and left to the next description batch, as X3a-1 left its own.

## Judgment calls

The lead accepts each as a lead decision (2026-10-04). Calls 1 to 3 are where a reviewer could most reasonably differ.

1. **The read-side surface.**
   - **Decision:** a new public module `installation_endpoint.rs` with `InstallationReadFence::store_endpoint` and `ReadStoreEndpoint`. It keeps item 1's properties: no public constructor, not Clone, not serializable, borrowed from the one fence. It lends only the decoded syntax the readers already exposed.
   - **Why:** item 4's readers live in other crates, and X3a-1's `SelectedStoreEndpoint` is `pub(crate)` and shared with the write side. A new module keeps `installation_observation.rs`'s inherited meaning true ("no selected store ... admission") and gives the inventory successor that item 8 requires its added rows. verify_design admits only an additive inventory successor.
   - **Rejected:** making `SelectedStoreEndpoint` public, which would widen a type the write side also holds; and adding the method inside `installation_observation.rs`, which would need a supersession of its inherited meaning and would leave no file to add.
2. **A reader's recheck is the session's full recheck.**
   - **Why:** item 2 makes every session recheck compare the full sample, and item 4 says the readers inherit it.
   - **Rejected:** a new, lighter per-file primitive (the held fence plus the reader's own files by full sample). That would be new surface, and at the session limit the 64 node files dominate either way.
   - **Consequence:** one operation costs one full recheck, never one per node. At the limit on the 48-deep home, a lineage reader's construction and two operations reach 128,745 of 131,072 edges, so a third operation would end on the budget row. Before X3a-2 a chain past about 35 nodes could not be read at all. On the one-node fixture home, about thirty operations fit.
   - **Question:** is that acceptable at the session limit, or do you require the lighter primitive?
3. **The readers' filesystem samples are kept.**
   - **Decision:** each sample runs after a full recheck and reopens the file by name, with its full sample unchanged and on H's filesystem.
   - **Why:** "public behavior is unchanged". The session's one read retains no directory below I, so the intermediate edges are not sampled. A file's own sample shows the filesystem it lies on, the innermost mount on its path.
   - **Rejected:** returning only I's and the fence's samples, which would misreport the file; and dropping the methods, which would change the public API.
   - **Question:** is the reopen, which reads no bytes, consistent with "a second capture of a required endpoint file" being forbidden?
4. **The minimum number of rechecks.**
   - **Decision:** each construction admits once. Lineage has no trailing recheck, and the marker has no post-decode recheck, because the admission's full recheck precedes the pure decode, so a changed file still wins.
   - **Rejected:** caching the admission in the session, which saves only about 70 validation edges.
5. **The caller's bound.** `max_nodes` applies to the admitted chain with the walk's own `Limit` semantics (the host test proves the equivalence). `max_nodes == 0` still refuses before any native step.
6. **The description overrides form a contract successor in this unit, reviewed with it.**
   - **Rejected:** deferring them to the next description batch, because item 8 assigns them here; and changing rows through the inventory successor, which verify_design refuses.
7. **Another store's S.**
   - **Decision:** `ProvisionalStoreMarker::read_existing` with an S other than the endpoint's refuses on the binding row (`MarkerError::Binding`). Before X3a-2 it captured `stores/<S'>/store-instance.v1`.
   - **Why:** the endpoint holds only the opened endpoint's marker, and owner §7 forbids reading an intermediate store's marker. The only in-tree caller passes the pair's S, so its behavior is unchanged.
8. **`installation_trust.rs` is unchanged.**
   - **Why:** it is not in item 4's list. Its pair and marker now come through the endpoint-backed records, so it inherits the adoption.
   - **What stays:** its `NativeTrustReadSession` still captures `trust/stores/S/state.v1`. That is X4T's provisional read-side trust reader. X4T item 8 governs the fenced first read's reuse of X3a's read, and X3a item 1 says trust admission is not X3a's.
   - **Question:** do you agree this is outside X3a-2? The lead will carry it as an X4T item if you do not.
9. **What stays public.** `capture_leaf` and `capture_descendant` stay on `InstallationReadFence` for files outside the endpoint; after X3a-2 no production code calls them. Item 4 asks for a source pin over the named readers, not a runtime guard, and the pin is that.

## Decide

- **Faithfulness:** does X3a-2 do exactly what X3a r5 item 4 asks? That means each reader taking the pair, marker and chain from the session's endpoint, no second capture, the full-sample recheck, item 3's bound, public behavior otherwise unchanged, and the extended pin. Does it do what item 8 asks: adoption, pin, description overrides and an inventory successor? Check against items 1 to 3 and the forbidden substitutes too.
- **Rerun:** run the lanes above yourself:
  - fmt, the workspace build and the three clippy lanes;
  - the workspace tests (twice if time allows), the doc tests and the crash-matrix feature lane;
  - the `installation_endpoint` tests with `--nocapture` (the cost lines);
  - `verify_scratch.py` in staged mode, and plain `verify_design`, which must refuse at `SCRATCH-X3A2/review.json`;
  - both package-edge lanes against v136, `verify_projection.py`, and both dependency checkers with their suites.

  Also rerun `evidence/build_v136.py ../opensip/design-lock.json` and `build_descriptions.py`. They write only their own untracked paths, so run them on a scratch copy of arch if you prefer, and confirm the same bytes.
- **Judgment calls:** are calls 1 to 9 acceptable? Answer the questions in 2, 3 and 8 directly.
- **Inventory v136:** pin it, and assess it as an inventory candidate.
- **Descriptions:** are the three new texts true of the code, and is leaving `installation_lineage.rs` on its inherited meaning right?

Write REVIEW.md, review.json and descriptions/review.json under the output directory.

review.json needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectSha256": `068a57816f5a69f3175a5576587210434158e4cea471cce2727c7cf075811dc8`, the diff's sha256, as a single string;
- "subjectManifestSha256": `b9d1c0dd14d0ebac3c43337124d01682967fcc9de2ac8a864202008f118f6f20`, as a single string;
- "inventoryCandidateAssessment": verdict, requiredFindings, the candidate's path, bytes and sha256, parent (v135's pin), and successorRecord (the pin of `read-endpoint-x3a2-inventory-v136/successor.json`).

descriptions/review.json needs:
- "verdict": ACCEPT-DESIGN-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectManifestSha256": `23770a586cc9a077c0c7610597499669625f393f817939041f141ce6a6a428f2`, as a single string;
- "successor": the pin of `read-endpoint-x3a2-descriptions/successor.json`.

Do not commit.
