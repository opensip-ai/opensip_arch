# X3a-2 r1

Verdicts: **ACCEPT-UNIT** on the code and inventory v136 (`review.json`), and **ACCEPT-DESIGN-UNIT** on the description successor (`descriptions/review.json`).

Product worktree `/Users/sb/code/opensip-ai/opensip-x3a2`, detached at `3f6f9a5a2543b70c0c259e041dc65d7e29164a0d`. `git diff 3f6f9a5` is 238838 bytes, sha256 `068a57816f5a69f3175a5576587210434158e4cea471cce2727c7cf075811dc8`, twelve files, +1062 −809. Law X3a r5 accepted bytes (`dab5881db:docs/implementation/m2/store-admission-x3a/PROPOSAL.md`) are 14850 bytes, sha256 `310197d33f4851eb0c198073e2516a6ea14192cebde751f64a0861f5f98f8ba3`. The live proposal differs by the acceptance note on line 3.

## Subjects

Inventory subject `docs/implementation/m2/read-endpoint-x3a2-inventory-v136-subject.json` is 2348 bytes, sha256 `b9d1c0dd14d0ebac3c43337124d01682967fcc9de2ac8a864202008f118f6f20`. Every file it names matches that pin. Candidate `repository-file-inventory.v136.json` is 555473 bytes, sha256 `ba124e21d23c8cd100eb2031203fd5c04fd8aeaab056872af54d1fa8c92bacea`. Parent v135 is 553173 bytes, sha256 `ac66ee3bd75ace8f21e3122daacfdb2619fe8bb8a432b083414c14cbe3a0c887`. Successor record `read-endpoint-x3a2-inventory-v136/successor.json` is 304956 bytes, sha256 `e93b44a6a77261c0d510f1bb6ee23135fcad0e82f6a5bf2c1f06bb383a5afda0`.

Description subject `read-endpoint-x3a2-descriptions-subject.json` is 881 bytes, sha256 `23770a586cc9a077c0c7610597499669625f393f817939041f141ce6a6a428f2`. Its four files match those pins. Successor `read-endpoint-x3a2-descriptions/successor.json` is 4933 bytes, sha256 `1e1a1f736db1d387f742626be49bd2c96275c3838b31ba88e5f8f84891096b0e`. Its only parent is the v136 candidate pin.

The staged lock in the worktree is 508400 bytes, sha256 `636aa4fc142b5c34c51d6c8a93dcf0d2a349f65de2bcff357affb54c76d35ac9`. Its review and assent pins are the `SCRATCH-X3A2` placeholders. Plain `verify_design` refuses that lock with `missing or escaping regular file: SCRATCH-X3A2/review.json`.

## What the diff does

`InstallationReadFence::store_endpoint` runs `ReadSession::store_endpoint`: in-memory validation on the session ledger, then one full session recheck, and no file read. `ReadStoreEndpoint` borrows that fence, has no public constructor, is not `Clone`, and is not serializable. Two `compile_fail` doctests pin `E0505` (use after the fence drops) and `E0599` (no `clone`). It lends the decoded pair, S from the opened marker, the marker bytes, and the admitted chain. A second lend returns the same addresses. `recheck` is the session's full recheck. `selection_filesystem` and `marker_filesystems` run that recheck, then take charged samples.

`ReadSession::required_filesystem` opens the named file no-follow under the retained I through `private_file` (`open_regular` plus `capture_descriptor_acl_accounted`), requires the metadata to equal the retained full sample, and samples a filesystem that `sample_admitted` requires to be H's. A missing file is remapped to custody `Changed`. No `read_bounded` of file bytes runs, and nothing joins the recheck set.

The four readers take the pair, the marker, and the chain from that endpoint:

- `ProvisionalSelection::read_existing` is `fence.store_endpoint()`. `record` rechecks, then returns the decoded pair.
- `ProvisionalStoreMarker::read_existing` parses S first, so an invalid S refuses before any native step, then admits the endpoint and decodes the lent marker bytes. Another store's S is `MarkerError::Binding`.
- `ProvisionalInstallationRecords::read_existing` admits the selection, then the marker bound to the pair's `store_instance()`. `recheck` is the selection's one full session recheck. `contributing_filesystems` calls the marker samples and then the pair sample, so that one method pays two full rechecks. The description says each sample follows a full recheck.
- `ProvisionalInstallationLineage::read_existing` returns `Error::Limit` when `max_nodes == 0`, before any native step. Otherwise it builds the records and applies `within` to the admitted chain. A longer chain is `Chain(Limit)`. There is no trailing construction recheck and no per-node recheck.

`SelectedStoreEndpoint::selection` is `pub(crate)`. `installation_observation::session` is `pub(crate)`. `lib.rs` declares `pub mod installation_endpoint` on macOS. The diff adds no manifest, lock, feature, `crash_barrier!`, `crash_scope!`, `SystemTime`, or `cfg(feature)`. `installation_trust.rs` is unchanged.

The extended pin `no_endpoint_reader_captures_a_required_endpoint_file_again` reads the production text of the host selection, records, and lineage readers, storage's marker reader, and `installation_endpoint.rs`. None contains `capture_leaf`, `capture_descendant`, `capture_with`, `.capture(`, `ProvisionalHeldFile`, `open_regular`, `read_bounded`, or `std::fs`. `.store_endpoint()` appears in the selection reader, the marker reader, and the lending module, and the lending module calls it once as `self.session().store_endpoint()`. `capture_leaf` and `capture_descendant` remain on the fence for files outside the endpoint. Production readers no longer call them. The remaining uses are the method definitions, doctests, security tests, host refusal compile-fail cases, and the pin's own forbidden-string list.

## Judgment calls

1. **Accepted.** A new public macOS module keeps `SelectedStoreEndpoint` `pub(crate)` for the write side and leaves `installation_observation.rs` without a selected-store admission. The module lends only the decoded syntax the readers already returned, borrowed from one fence.

2. **The full recheck is acceptable at the session limit.** Item 2 requires every session recheck to compare the full sample, and item 4 says the readers inherit it. A lighter per-file primitive would be new surface. Measured on this machine (`installation_endpoint --nocapture`): one-node session read 460 objects / 9881 edges / 14061577 bytes; one admission 624 / 13206 / 14536026; second admission 788 / 16531 / 15010475; one reader recheck 952 / 19851 / 15484924. A 64-node chain on the 48-deep home: session read 3162 / 49949 / 17435402; one admission 4474 / 69682 / 19152895; lineage built 5786 / 89415 / 20870388; two reader operations 8410 / 128745 / 24305374. The caps are 65536 objects, 131072 edges, and 256 MiB. At that limit the two operations sit at 128745 edges, so a third operation reaches the budget row. On the one-node home one recheck adds 3320 edges, and about thirty such operations fit. That is the headroom item 2 and item 3 leave, and it is enough to accept.

3. **The reopen is consistent with the forbidden second content capture.** The sample opens the file by name after the full recheck, judges it private, and requires the retained full sample and H's filesystem. It reads no file bytes. The source pin keeps `open_regular`, `read_bounded`, and the capture helpers out of the five reader and lending sources. `a_replaced_endpoint_file_refuses_the_sample_itself` refuses on the sample's own check, with the session latched. Returning only I's and the fence's samples would misreport the file's filesystem. Dropping the methods would change the public API.

4. **Accepted.** Each construction admits once per reader that holds an endpoint. Selection and the marker each call `store_endpoint` once. Records and lineage take those two admissions. Lineage has no trailing recheck. The marker has no post-decode recheck because the admission's full recheck precedes the pure decode. A changed file still fails that recheck, which tests 2 and 4 pin as `required-files-changed` followed by a latch.

5. **Accepted.** `max_nodes == 0` is `Error::Limit` before any native step. `within` returns `LineageWalkError::Limit` when the admitted chain is longer than the bound. `the_callers_bound_on_the_admitted_chain_is_the_supplied_walks` compares `within` with `inspect_supplied_lineage` on synthetic rooted chains of one to four nodes and bounds one to five: `within` passes exactly when the walk ends at the root, and otherwise both return `Limit`.

6. **Accepted.** The three description changes are a contract successor whose parent is v136. verify_design checks them as overrides on plain rows. Changing the inventory rows themselves is the path verify_design refuses, and item 8 assigns the overrides to this unit.

7. **Accepted.** A requested S other than the opened marker's refuses `MarkerError::Binding` after admission. An invalid S refuses in `StoreInstance::parse` before any native step. The only in-tree production caller, `installation_records.rs`, passes the pair's S. A successful `store_endpoint` has already joined that S to the opened marker, so the binding check passes for that caller. The endpoint holds only the opened endpoint's marker.

8. **`installation_trust.rs` is outside X3a-2.** It is absent from item 4's list and from this diff. `read_existing` still builds `ProvisionalInstallationRecords` and then `NativeTrustReadSession::capture` for `trust/stores/S/state.v1`. The pair and marker now come through the endpoint-backed records, so the trust reader inherits that adoption. The state capture remains X4T's provisional read-side trust reader. X4T item 8 governs reuse of X3a's read, and X3a item 1 leaves trust admission outside X3a. Carry the state capture as an X4T item.

9. **Accepted.** Item 4 asks for a source pin over the named readers. The pin is that pin. The fence methods stay for files outside the endpoint.

The forbidden substitutes stay out of the production readers. There is no new public code. `installation_selection::Error::Decode` and lineage's `ReadError::Decode` remain and are no longer produced. A pair, marker, or node the session cannot read or decode refuses the fence on the incomplete row.

## Inventory v136

v135 plus two proposed, non-generated rows in `opensip-security`: `crates/security/src/installation_endpoint.rs` (`composition`) and `crates/security/src/installation_endpoint_tests.rs` (`test`). 971 files. The 969 inherited rows are equal by value. Packages, edges, and pending decisions match v135. The nine changed source files were already planned rows. The successor projects 100 inheritance rows; 46 selectors move by the two inserted paths; zero supersessions are folded; zero direct parent overrides are included. A scratch rerun of `build_v136.py` against HEAD's lock reproduced the candidate and the successor byte for byte. The candidate's two descriptions match the module: the lend, the full-sample recheck, the charged samples, and the five tests.

Assessment: **ACCEPT**.

## Description successor

Three `passageOverrides`, no supersessions. Each `before` is the raw v136 description, and each matches `evidence/descriptions.json`:

- `/files/122/description`, `installation_records.rs`. The after states the endpoint-backed pair and marker, the marker bound to the pair's S, one full session recheck for the bundle, and the sample order I, fence, marker, then pair, each after a full recheck and on H's. That matches `read_existing`, `recheck`, and `contributing_filesystems`.
- `/files/123/description`, `installation_selection.rs`. The after drops the capture, takes the pair through endpoint admission, rechecks the full sample before the pair is handed out, and reopens the pair by name. That matches `read_existing`, `record`, and `filesystem`.
- `/files/747/description`, `native_marker.rs`. The after takes the endpoint marker bytes, refuses another S on the binding row, refuses an invalid S before any native step, and samples I, the fence carrier, and the marker after the full recheck. That matches `read_existing`, `decode`, `recheck`, and `contributing_filesystems`.

`installation_lineage.rs` is v136 row 121 and is inherited, so an override would be the wrong form. Its effective meaning, projected from inventory81 onward, is: "Retain the selected pair, every immutable lineage node and the physically opened selected endpoint store marker under the ordinary binding owner. Admit complete node ancestry without requiring reclaimed intermediate physical stores; recheck all contributing original descriptors and latch failures under one operation budget. Separate observation-only from durable/write capabilities; structural values alone grant no namespace/current authority." That is the README quote plus its closing sentence. It describes the adopted reader and stops promising a marker per node. M2-COMPLETE r3 §3.3 already recorded that the description half was true through an inherited override. Leaving the row inherited is right.

`build_descriptions.py` on the scratch arch reproduced the successor and the subject byte for byte, with overrides on rows 122, 123, and 747.

## Evidence this review ran

Private `CARGO_TARGET_DIR` under this review directory, private 0700 `TMPDIR`, `CARGO_HOME=/Users/sb/.cargo`, `--locked --offline`. No crash-matrix run set.

| Check | Result |
|---|---|
| `cargo fmt --all --check` | exit 0 |
| `cargo build --workspace --all-targets` | exit 0 |
| Clippy `-D warnings`, workspace, crash-matrix, scenario-fixtures | exit 0, 0, 0 |
| `cargo test --workspace --all-targets --no-fail-fast`, run 1 | 1729 passed, 0 failed, 3 ignored, 20 binaries |
| The same, run 2 | 1729 passed, 0 failed, 3 ignored, 20 binaries |
| `cargo test --workspace --doc` | 20 passed, 0 failed |
| Crash-matrix feature lane | 1627 passed, 0 failed, 3 ignored |
| `installation_endpoint --nocapture` | 5 passed; cost lines above |
| `verify_scratch.py` staged | pass. Inventory successors 95 → 96, v136 selected. Contract successors 93 → 94. Inheritance 100 → 100. Supersessions 21. Overrides on rows 122, 123, 747. Generation sources 40, admission sources 48. Plain refusal `SCRATCH-X3A2/review.json` |
| Plain `verify_design` on the staged lock | exit 1, `missing or escaping regular file: SCRATCH-X3A2/review.json` |
| Plain `verify_design` on HEAD's lock | pass. v135 selected, 95 inventory successors, 93 contract successors, 100 inheritance rows, 21 supersessions, 40 generation and 48 admission sources |
| `verify_projection.py` on HEAD's lock | PASS, 100 rows, 503 corruptions refused |
| `build_v136.py` and `build_descriptions.py` on a scratch arch | same bytes as the live files |
| Package edges, host, v136 and v135 | both pass: 12 workspace packages, 22 declared and 20 resolved internal edges |
| Package edges, rust-provider, v136 | pass: `opensip-rust-provider` only |
| `test_package_edges.py` | 14 tests, OK |
| `check_dependencies.py` security-crypto-workspace | pass: 11 dependencies, 8 local sources |
| `check_identity_dependencies.py` | pass: 8 dependencies, 305 sources |
| `test_dependency_policy.py` | 9 tests, OK |
| `test_identity_dependencies.py` | 5 tests, OK |

X9 harness paths are byte-identical between `3d2d5b5` and `3f6f9a5` (`git diff --stat` empty). The census pin runs inside the feature lane. No run set was launched.

## Non-blocking

NBO-1. `crates/host/src/installation_records.rs:2` still carries the pre-adoption "S equality is not full S/G/K" sentence, and line 36 still says decoded G/K remain claims "despite S match." The description successor states the corrected records meaning, and the code admits through the endpoint before the bundle exists. The replacement is in `review.json`. It does not block this unit.
