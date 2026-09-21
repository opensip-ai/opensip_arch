# Independent review — native lineage bundle 368

**Standing:** bounded **host-owned native lineage observation** of frozen `native-lineage-checkpoint-368`. `ProvisionalInstallationLineage` privately owns 359-style records (pair + selected marker), every original lineage-node capture, a store marker per observed store, and the lifecycle367 walker under **one** `InstallationReadFence`. Start triple is parsed from the actual selection pair. Paths and 4096-byte cap follow physical-owner203. This is **not** five-member `StoreGenerationBindingV1`, namespace/registry/core, qualified profile, current trust, intent authorization, whole-root rollback, or ABA proof. Native capture failures are **unavailable**, not absence-based initialization. Product remains `fa72e50`. Inventory **v55** is a separate later review.

Prior 367 REVIEW `d7416012…3fb7` and ADDENDUM `cf02b1f1…9de7` were read and are **unchanged**. 54 remains **NEEDS-CHANGES**. No 367 security rerun (unchanged security files).

Python 3.12.13 `-I -B`. rustc/cargo **1.95.0**. `RUST_TEST_THREADS=1` and `TMPDIR=$(getconf DARWIN_USER_TEMP_DIR)` (`/var/folders/…/T/`, **not** under `/tmp`). Isolated `grok-out/`; freeze workdir **not** overwritten. Root `native-review-clear368.json` present; no other native suite overlapped. **This review reproduced:** isolated 24-case synthetic-home integration; three compiled targeted faults + three restored cases; host **68**; workspace Clippy `-D warnings`; `cargo fmt --all --check`. Security native observation suite **not rerun**.

---

## Verification

Archive-pin and every `subject.json` member matched **before** extract. Frozen archive: **6928824 B, 644 members, SHA256 `f01f6ef1650d2e58cf9f831221e6c37d0d88cb708de06724531703e4b99eecf9`**. Standing: “Private retained native lineage bundle; synthetic account home validation, not full binding authority”. Parent 367 rehashed first: **640 / 6942100 B / `20ace56e…742a`**. Extract rehash: 0 mismatches; **583** product files.

Vs 367:

| Class | Count |
|---|---|
| Unchanged | **581** (lifecycle367 + security366 included) |
| Changed | **1** (`crates/host/src/lib.rs` 538 → 597, SHA256 `bf14c167…2d93`) |
| Added | **1** (`crates/host/src/installation_lineage.rs` 6104 B, SHA256 `e0581cd4…438c`) |
| Removed | **0** |

Dependencies and inherited fixtures unchanged. `lib.rs` only adds `pub mod installation_lineage` (macos). No supplied-handle constructor; no `File`/`root` escape; no create/repair/publish.

`read_existing` requires `max_nodes > 0` (`Error::Limit`). Walker uses lifecycle `inspect_supplied_lineage` with the pair-derived start key. Each hop: `check_all` older owners, capture descendant at `transitions/lineage/S/G/K.node` with `LINEAGE_NODE_CAP`, decode, recheck capture even on decode failure, read store marker, recheck capture even on marker failure, `check_all` again, then retain capture+marker+node. `check_all` rechecks records, all captures, all markers, then captures again, then records. `recheck` / `nodes` / `selection` latch `failed` permanently (`Error::Closed`). Caller node bound is an engineering limit, not a shared authoritative budget.

---

## Live native (this review)

Isolated runner adapted to grok-out paths, Darwin user `TMPDIR`, and `/Users/sb/code/opensip-ai` synthetic-home prefix. TEST-ONLY: only returned home bytes substituted; credentials/`getpwuid_r` protocol unchanged. Not actual home provenance.

| Run | Result |
|---|---|
| integration-r1 baseline 24 cases | **24 PASS** (134.5s). Names match author r1. Failed admission leaves fixture bytes unchanged (`valid` snapshot-equal). |
| integration-r2 skip-retained-nodes | compiled; intended panic (`replace-predecessor` / retained-node check) |
| integration-r2 skip-retained-markers | compiled; intended panic (`replace-marker`) |
| integration-r2 skip-failure-latch | compiled; intended panic (`latch-after-repair`) |
| integration-r2 restored three cases | **PASS** replace-predecessor, replace-marker, latch-after-repair |
| `cargo test -p opensip-host` | **68 passed** (244.10s), actually run |
| workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |

r2 compared all **583** source pins to this review’s r1 baseline (no redundant 24-case rerun). Production extract pins unchanged; shadow restored; both synthetic homes **removed**. Freeze `integration-r1` not overwritten. 24 cases include nonmonotonic generation / repeated intent digest, zero/exhausted limits, missing target/predecessor/marker, wrong marker, malformed/oversized/noncanonical/misbound node, cycle/self-edge, unsafe node/marker, hard link, wrong selection, identical-byte replacements, ancestor-directory replacement, selection getter checking old nodes, and latch after permission repair.

---

## Findings

368 is the host same-fence join of retained pair/markers/original node files with the 367 walker. Rechecks and the `failed` latch are exercised by the 24 cases and the three compiled faults.

**Actionable 368 source defect:** none that make one-fence construction, post-failure recheck, Closed latch, or “failed read does not create/repair” self-contradictory with the 24 cases, 3 intended panics, restored 3, and 68 host tests.

**Must not be counted closed:** five-member binding; namespace/handle/registry; core/profile; current authority; intent authorization; writers; whole-root rollback/ABA; OS-home qualification; inventory v55.

---

## Remaining (do not count closed)

Selected inventory still 32. Inventory 55 (direct v32 successor) is a later review after this FINAL/root-read. Security 388 not rerun. M2–M6 open.

---

## Verdicts

- [x] **368 as frozen host native lineage bundle:** 644-member archive verified; 581/1/1 vs 367; 24-case isolated integration; 3 compiled faults + restored 3; host **68**; Clippy/fmt. TEST-ONLY synthetic home. Private/uninstalled.
- [ ] **Not** five-member binding, current authority, inventory 55, or product installation.
