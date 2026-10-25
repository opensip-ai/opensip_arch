# Snapshot path charge-site audit (lead research, 2026-10-25, product e39cee8)

Read-only research by a lead-side search agent; not an independent review. Verify file:line before relying on any row.

I've built the full charge-site table. The main surprise first: nothing in production code ever constructs `WorkLedger::snapshot_profile()`. Every caller is a test, plus one doc comment. The snapshot modules are flagged library-only with no caller yet (`/Users/sb/code/opensip-ai/opensip/crates/host/src/lib.rs:110-122`: "Library only; J2b and J2c compose them", "sealing; library only, no caller"). So the table below describes the path's internal charging, not a live call chain.

## File key (basenames in the table refer to these)

- `work_ledger.rs`: /Users/sb/code/opensip-ai/opensip/crates/platform/src/work_ledger.rs
- `work_reader.rs`: /Users/sb/code/opensip-ai/opensip/crates/platform/src/work_reader.rs
- `snapshot.rs`: /Users/sb/code/opensip-ai/opensip/crates/host/src/snapshot.rs
- `snapshot_seal.rs`: /Users/sb/code/opensip-ai/opensip/crates/host/src/snapshot_seal.rs
- `candidate_custody.rs`: /Users/sb/code/opensip-ai/opensip/crates/host/src/candidate_custody.rs
- `snapshot_source.rs`: /Users/sb/code/opensip-ai/opensip/crates/security/src/snapshot_source.rs
- `snapshot_walk.rs`: /Users/sb/code/opensip-ai/opensip/crates/security/src/snapshot_walk.rs
- `snapshot_read_set.rs`: /Users/sb/code/opensip-ai/opensip/crates/security/src/snapshot_read_set.rs
- `snapshot_vcs.rs`: /Users/sb/code/opensip-ai/opensip/crates/security/src/snapshot_vcs.rs
- `git_tracking.rs`: /Users/sb/code/opensip-ai/opensip/crates/security/src/custody/git_tracking.rs
- `discovery_walk.rs`: /Users/sb/code/opensip-ai/opensip/crates/security/src/custody/discovery_walk.rs
- `discovery_rule.rs`: /Users/sb/code/opensip-ai/opensip/crates/security/src/custody/discovery_rule.rs
- `discovery_export.rs`: /Users/sb/code/opensip-ai/opensip/crates/security/src/discovery_export.rs
- `descriptors.rs`: /Users/sb/code/opensip-ai/opensip/crates/identity/src/descriptors.rs

**Shared cost formulas:**
- `owned(b)` (`discovery_walk.rs:89`) = {1 object, b+128 bytes}. `owned_record` (`snapshot_source.rs:480`) is the same formula.
- `STATUS` (`discovery_walk.rs:79`) = {1 edge, 512 bytes}. `STATUS_COST` is the same.
- `LISTING` (`discovery_walk.rs:60`) = {2 objects, 3 edges, 1024 bytes}.
- `VISIT` (`discovery_walk.rs:66`) = {1 edge}.

## Step 1: who receives the snapshot profile, and the phases

- **Constructed at:** `work_ledger.rs:242-254`.
- **Non-test references:** only the doc comment at /Users/sb/code/opensip-ai/opensip/crates/lifecycle/src/installation.rs:1465. It names the profile as the "interim policy" for component `install`, which is not part of the snapshot path.
- **Test callers:**
  - Snapshot path: `snapshot_tests.rs:486,490,498` (`payload_charge`) and the census test at `snapshot_walk_tests.rs:965`.
  - Outside the snapshot path: `launch_recheck_tests.rs`, `retained_tree_tests.rs`, `installation_tests.rs`, and `work_ledger.rs:718`.
- **Phases and entry points:**
  - Session: `CaptureSession::open` (`snapshot.rs:192`).
  - Pre-walk capture: `capture` (`snapshot.rs:208`), through `SnapshotRoot::open` (`snapshot_source.rs:561`).
  - Layout capture: `capture_pruned` (`snapshot.rs:231`), through `open_pruned` (`snapshot_read_set.rs:152`).
  - Walk: `CaptureSession::walk` (`snapshot.rs:253`), through `walk_snapshot_retaining` (`snapshot_walk.rs:247`), handing files to `read_once` (`snapshot.rs:334`).
  - Read set: only `authorize_read` and `observes_dependency_cargo_root` exist (`snapshot_read_set.rs:97,125`). The read set proper (C1c-1) has not landed.
  - VCS: `observe_vcs` (`snapshot_vcs.rs:171`).
  - Seal: `seal` (`snapshot_seal.rs:365`).
  - Reuse: `CandidateCustody::open` (`candidate_custody.rs:226`) and the walk's compare-and-reuse branch (`snapshot.rs:267-275`).
- **Not on the ledger:** `native_universe.rs` takes `work: usize` (line 146), not a `WorkLedger`.

## Step 2: charge-site table

| phase | site | what grows with input | covering charge | precharge? | cost formula |
|---|---|---|---|---|---|
| session | snapshot.rs:199 | 64 KiB read buffer | snapshot.rs:196 `buffer_cost()` | yes | 1 obj; 4K+8K+16K+32K+64K = 126,976 B |
| session | candidate_custody.rs:160 | custody dir listing (max 4 entries, 4096 B) | :158 LISTING, :161 VISIT per entry | yes | LISTING + 1 edge per entry |
| pre-walk open | snapshot_source.rs:571 | validated path copy | :570 `owned(path.len())` | yes | 1 obj, len+128 |
| pre-walk open | snapshot_source.rs:586 (per segment) | `rel` rebuilt for every segment | :585 `key_cost` | yes | owned(rel+1+part) |
| pre-walk open | snapshot_source.rs:588, :615 | fstatat per segment and the leaf | `observe_child_accounted` (directory_open.rs:146) | yes | 1 obj, 1 edge, name+1+sizeof(stat) |
| pre-walk open | snapshot_source.rs:599 → :410, :426 | openat + status per directory | `open_child_directory_cost` + STATUS | yes | 2 obj, 1+status edges, name+1+status B |
| pre-walk open | snapshot_source.rs:625 → :446, :461 | leaf open | `open_regular_cost` (filesystem.rs:481) + STATUS | yes | 1+2c obj, 1+2c edges, len+c+c·status B |
| custody judge | snapshot_source.rs:302 | ACL capture | `capture_descriptor_acl_accounted` | yes | constant, `descriptor_acl_capture_cost` |
| custody judge | snapshot_source.rs:311-314 | ACL entry Vec | :308 `owned(count·sizeof entry)` | yes | 1 obj, count·size+128 |
| read_once | snapshot.rs:356, :399 | before and after samples | :347 `run(STATUS_COST)` | yes | 1 edge, 512 B each |
| read_once | snapshot.rs:362 → candidate_custody.rs:195, :199 | pending name + create | :194 `owned_record(name)` + `create_exclusive_regular_accounted` | yes | owned(8+digits) |
| read_once | snapshot.rs:378 (read loop) | read calls, about size/64 KiB | :370 ATTEMPT per call, envelope at :68 | yes | 1 edge per call, at most 2·⌈size/64K⌉+2; **0 bytes per content byte** |
| read_once | candidate_custody.rs:342, :353-356 | write + SHA-256 per chunk | :324 WRITE | yes | 1 edge per ≤64 KiB chunk; hashing has no byte term |
| read_once | candidate_custody.rs:403, :406, :413 | hex name, rename, `committed` node | :402 `owned_record(64)`, rename accounted, :412 `owned_record(40)` | yes | as stated |
| read_once | candidate_custody.rs:394 | duplicate-blob unlink | `unlink_entry_accounted` | yes | owner's |
| session map | snapshot.rs:222, :245, :279 | `captures` node | :221, :244, :278 `owned_record(sizeof Capture)` | yes for the node (charged after the read, which is charged on its own) | 1 obj, sizeof+128; key string moved, charged at listing or open |
| reuse (walk) | snapshot.rs:267-275 | stamp compare only | none needed | n/a | n/a |
| walk | snapshot_walk.rs:258 / :521 | `known` Cargo roots | :520 `key_cost(rel,"")` | yes | owned(len+1) |
| walk | snapshot_walk.rs:263, :344 | `levels` frames | :261, :342 `owned(0)` | yes (approximate; Vec reallocation not priced separately) | 1 obj, 128 B per frame |
| walk listing | snapshot_walk.rs:458 | directory stream | :456 LISTING | yes | 2/3/1024 |
| walk listing | discovery_walk.rs:342 | raw entries | VISIT | yes | 1 edge per entry |
| walk listing | discovery_walk.rs:353-354 | path String + validator copy + Vec slot | :348 | yes | 2 obj, 2·(parent+1+name)+256 |
| walk listing | discovery_walk.rs:357 | invalid name bytes | :356 `owned(raw.len())` | yes | owned(len) |
| walk listing | **discovery_walk.rs:390** | `paths.sort()`, O(n log n) | **none** | no | n/a |
| walk | snapshot_walk.rs:432 | `.opensip` classification | :431 `classify_cost` | yes | see next row |
| walk | snapshot_walk.rs:298 | `classify_path` temporaries (segment Vec, `join` per `target`, anchor) | :297 `classify_cost` (:52) | yes | obj 4+t; B = seg·16 + len·(3+t) + obj·128 |
| walk | **snapshot_walk.rs:483** | `paths.remove`, O(n) shift | **none** | no | n/a |
| walk | snapshot_walk.rs:490 | `observed` Vec | :485 `owned(n·sizeof ChildObservation)` | yes | exact capacity |
| walk | snapshot_walk.rs:494 | per-child fstatat | `observe_child_accounted` | yes | as above |
| walk | **snapshot_walk.rs:301** | `ignored()` (:105-112) + `is_boundary` (discovery_export.rs:255 → discovery_rule.rs:392-433), linear scans per child | **none** | no | O(children × (ignorePaths + boundaries)) |
| walk | **snapshot_walk.rs:352, :509** | `boundary_anchor` for markers; `regular_cargo` scan | **none** | no | linear |
| walk | snapshot_walk.rs:325, :326, :359, :361 | dir/file open + custody judgments | open costs, STATUS, ACL | yes | as above |
| walk | snapshot_walk.rs:383, :387 | symlink and special-file report entries | :382, :386 `owned(rel.len())` | yes | owned(len) |
| walk | snapshot_walk.rs:396 | member_roots copy | :395 `owned(len)` | yes | owned(len) |
| extent | snapshot_walk.rs:90 | ignorePaths validation copy | :89 `owned(len)` | yes | owned(len) |
| read set | snapshot_read_set.rs:106 | `read_set_path` (discovery_rule.rs:579) temporaries | :104 `read_set_path_cost` (:58) | yes | obj 2+t; B = seg·16 + full·(1+t) + obj·128 |
| read set | snapshot_read_set.rs:130 | Cargo.toml fstatat | `observe_child_accounted` | yes | as above |
| layout (`open_pruned`) | snapshot_read_set.rs:160, :167, :190, :191, :203, :206, :222, :232 | copy, rule temporaries, per-segment rel/observe/open/judge, leaf | :159 owned; :166 `pruned_capture_cost` (:42); :189 key_cost; owner costs | yes | `pruned_capture_cost` = 2 obj, seg·16+len+256 |
| VCS | snapshot_vcs.rs:323 | `MemberCommit` Vec (at most 64, :184) | :318 `owned_record(n·sizeof)` | yes | exact |
| VCS | git_tracking.rs:1729, :1738, :1743 | `reach_member` per segment (at most 256) and per VCS marker | `open_child_directory_cost`, STATUS, `absent` accounted | yes | as above |
| VCS | snapshot_vcs.rs:371, :394, :398, :417, :430, :434 | `.git`/ref opens, statfs, ACL judgments | `open_child_directory_cost`, `open_regular_cost`, `descriptor_filesystem_observation_cost`, `capture_descriptor_acl_observed` (git_tracking.rs:1162) | yes | owners' |
| VCS | snapshot_vcs.rs:442 → work_reader.rs:146-175 | HEAD / loose ref / packed-refs buffer (≤ INDEX_CAP 4 MiB, git_tracking.rs:38) | work_reader.rs:146 (1 obj), :160 per growth, :170 per attempt | yes | per growth {1 edge, next B}, 4K doubling to cap+1; 1 edge per attempt |
| VCS | snapshot_vcs.rs:457, :522 | `head_form` / `packed_lookup` O(len) scan | :443 `parse_cost(len)` | yes | {1 obj, **1 edge**, len B}: edge count is constant |
| VCS | snapshot_vcs.rs:466 | retained commit | `owned_record(40)` | yes | owned(40) |
| seal | **snapshot_seal.rs:381-394** | count pass over all rows, `string_len` per char | **none** | no | O(total path bytes) |
| seal | snapshot_seal.rs:399 | leftover copy | :398 `owned_record(len)` | yes | owned(len) |
| seal | snapshot_seal.rs:474-482 | canonical inventory Vec (≤ 4 MiB) | :473 `owned_record(inventory_len)` | yes | exact |
| seal | **snapshot_seal.rs:486** | `raw_sha256(&inventory)` | **none** | no | n/a |
| seal | snapshot_seal.rs:329 | VCS record Vec | :328 `owned_record(len)`, checked against `encoded_len` (snapshot_vcs.rs:88) | yes | exact |
| seal | **snapshot_seal.rs:491** | `raw_sha256(&vcs_record)` (≤ about 1.57 MB) | **none** | no | n/a |
| seal | snapshot_seal.rs:495-501 | inventory blob into custody | begin/write/commit charges | yes | 1 edge per 64 KiB chunk |
| seal | snapshot_seal.rs:507-508 | descriptor Vec (≤ MAX_BYTES 4 MiB) | :506 `owned_record(descriptor_bytes)` | yes | exact |
| seal | **snapshot_seal.rs:515** → descriptors.rs:586-607 | JSON parse tree, schema evaluation, `ordered`, `hash_canonical_value` re-encode + SHA, `format!` id | :514 `owned_record(10+64)` only | constant | 1 obj, 202 B; the rest sits under a separate `SCHEMA_BUDGET` (snapshot_seal.rs:43), not the ledger |
| seal | **snapshot_seal.rs:58** | `raw_sha256(&carrier.bytes)` (carrier up to 4 MiB) | none; no ledger parameter | no | n/a |
| reuse (custody open) | candidate_custody.rs:236, :237, :242, :264, :274, :288 | hex name, open, status, verify read + digest, rewind | :235 owned_record(64); open_regular_cost; STATUS; :259 1 edge per read; :283 | yes | 1 edge per ≤64 KiB read; no attempt envelope |

## Step 3: suspected uncharged, late, or constant-charged sites

**Uncharged compute (large):**
1. `snapshot_seal.rs:515` (with `descriptors.rs:597-601`): the biggest gap. Parsing the descriptor builds a full JSON value tree (about 16k rows at 4 MiB, 100k rows max), re-encodes it canonically, and hashes it. None of that is on the ledger. The only charge is a constant 202 bytes at :514, and the real bound is the separate 64 MiB `SCHEMA_BUDGET`.
2. `snapshot_seal.rs:486` and `:491`: SHA-256 over up to about 4 MiB of inventory and about 1.57 MB of VCS record, with no edge or byte charge. The inventory is hashed again, with a charge, when it is written to custody.
3. `snapshot_seal.rs:58`: SHA-256 of the project carrier bytes, with no ledger in scope.

**Uncharged compute (per entry or per row):**
4. `discovery_walk.rs:390`: the listing sort is O(n log n) and uncharged (a listing can hold up to 131,072 entries).
5. `snapshot_walk.rs:301`, `:105-112`, and `discovery_export.rs:255`: every child pays linear scans of `ignorePaths`, nested repositories/projects, and custody rows, all uncharged. Their bounds are unclear.
6. `snapshot_walk.rs:483` (O(n) remove), `:509` (cargo scan), and `snapshot_seal.rs:381-394` / `:397` (full passes over all captures): smaller uncharged scans.

**Constant charge on input-sized work:**
7. `snapshot_vcs.rs:443` (`parse_cost`): edges are fixed at 1 even though `packed_lookup` scans up to 4 MiB line by line.
8. `candidate_custody.rs:353-356` and `:274`: hashing is priced at 1 edge per chunk with no byte term. That is proportional per chunk, not per byte.
9. By design, source content bytes are never charged in the bytes dimension, only as edges at about 1 per 64 KiB. The test `snapshot_tests.rs:518` asserts exactly this. As a result the 2^33 byte cap never sees file content.

**Charged after the work:**
10. `snapshot.rs:221`, `:244`, `:278`: the capture-node charge comes after the custody blob is already committed. If it refuses, a committed blob is left behind with no session entry. It is still charged before the map insert itself.

**Uncharged heap copies on error paths (all terminal, but they contradict the "every heap copy charged first" comments):**
11. `snapshot_walk.rs`:
    - :504 `path.clone()`
    - :91 `path.clone()`
    - :462-470 root spelling and `format!`
    - :200 `format!`
12. `snapshot_source.rs`:
    - :304, :422, :431, :457, :466 `rel.to_owned()`
    - :574 `escape_default().to_string()`
    - :597, :623, :639 `path.to_owned()`
    - :256, :298, :321, :339, :340 `format!` / `to_owned`
13. `snapshot_read_set.rs`: :163, :171, :177, :201, :230.
14. `discovery_walk.rs:386-387`: `parent_abs()` and `escaped`.

**Other notes:**
15. `snapshot_walk.rs:261` / `:342`: the frame charge is 128 bytes, and the `levels` Vec's own reallocation is not priced separately. Whether 128 covers `sizeof(Level)` is unclear.
16. Test helper `insert_reached` (`snapshot_tests.rs:69-91`) inserts captures without charging, so the sealing bound tests under-represent session charges.

## Step 4: the 4 MiB positive test

- **Snapshot descriptor test:** `the_bounds_refuse_one_past_each_and_admit_at_each`. The doc comment is at /Users/sb/code/opensip-ai/opensip/crates/host/src/snapshot_seal_tests.rs:420, the test function at :426, and the exact-4-MiB case at :492-494.
  - Its ledger is built in the `seal_tree` helper with **`WorkLedger::discovery_profile()`** (`snapshot_seal_tests.rs:52`; extent at :46).
  - That is neither `WorkLedger::new()` nor the snapshot profile: discovery caps are 2^22 objects, 2^21 edges, 2^30 bytes.
  - The rows go in through the uncharged `insert_reached`.
- **The VCS 4 MiB test does use `WorkLedger::new()`:** `each_git_file_at_exactly_the_cap_is_read_and_one_over_refuses`, /Users/sb/code/opensip-ai/opensip/crates/security/src/snapshot_vcs_tests.rs:800-830. It goes through `resolved()` (:243) → `vcs(None, None)` → `WorkLedger::new()` (:170-171), which has 131,072 edges. The same file pins those defaults at :22-28.
- **Closure descriptor test (not the snapshot path):** /Users/sb/code/opensip-ai/opensip/crates/security/src/component_closure_tests.rs:833 also uses `WorkLedger::new()`, via `test_ledger()` (:42-43).
- **Tests that do use the snapshot profile:** `payload_charge` (`snapshot_tests.rs:486-498`) and the census test (`snapshot_walk_tests.rs:938-966`).

## Step 5: `used()` and custom caps

- **`used()` accessors:** `WorkLedger::used` at `work_ledger.rs:193` ("never decremented") and `WorkScope::used` at `work_ledger.rs:499`.
- **Custom caps:** the only constructor is `with_limits` (`work_ledger.rs:258-275`). It is public, not `cfg(test)`, and can only lower caps. Anything above the global caps (65,536 / 131,072 / 268,435,456) is refused with `BudgetFailure::Profile`. /Users/sb/code/opensip-ai/opensip/crates/platform/tests/work_ledger_tests.rs:462-470 asserts this for profile-sized caps.
- **No test-only profile constructor exists.** The only fixed-cap constructors are `new` (:204), `discovery_profile` (:223) and `snapshot_profile` (:242). The `#[cfg(test)] mod tests` at :665 can read private fields like `ledger.used` and `ledger.prepaid` directly, but that only works inside `work_ledger.rs`.