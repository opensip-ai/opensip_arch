# Advisory: private enumeration kernel41 (copied `inspect_enumeration_join`)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Independent consumer-B advisory of the **pinned copied** private enumeration kernel. **Not formal/source approval. Not ACCEPT-DESIGN-UNIT. Not SOURCE38. Not runtime-v18. Not full M2. Not live install. Not complete execution/selection/replay/custody.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-enumeration-kernel-41/review` only (isolated probe under `review/probe`). Copied sources `/tmp/opensip-implementation/m2-grok-enumeration-kernel-41/inputs` and `inputs.json` were not modified. Root draft `/tmp/opensip-implementation/m2-enumeration-join-trial-41/product` was read-only and **evolved during this review**; it is not the reviewed kernel. No frozen/live/history edits. No commit/push.

SOURCE38 / formal runtime-v18 are treated as already root-read. 16 inputs installed 24/36 and paired local commits `6b31e8e` / `3c31b5164` (no push) are user-stated background, not re-hashed here.

## Verdict

**Copied `complete_join` is byte-equal to selected E39 on the 51 frozen map cases and on the join-law mutations that remain schema-reachable. Public `inspect_enumeration_join` is not that map API: reconstruct failures `duplicate snapshot path` and universe `bindResult` return `Err(Refused("ENUMERATION_ADMISSION_PRECONDITION"))` instead of the E39/join REFUSE document. Unused `JoinInputs.snapshot_inventory` is the warned dead field and is not a finding.**

Kernel-check’s 51-case proof is an injected test-only map constructor inside a **different** `enumeration_join.rs` (41956 / `4e736c1598…`). This advisory re-ran those cases against the **copied** kernel (51742 / `3f24610941…`) and independently re-ran selected E39. Map proof does not grant retained-reader or admission authority.

## Scope

| Claim | This note |
| --- | --- |
| Formal/source/runtime unit | No |
| Complete execution input selection | No |
| Predicate replay / Run / custody | No |
| Host maps / `bindResult` / membership derivation as authority | No; API refuses or omits them |
| New enum registry + 48 faults in a live inventory | Needs future inventory 27 (user-stated; not a finding) |
| `snapshot_inventory` unused field | Will be removed; **not a finding** |

## Pins (copied kernel is authority)

| Artifact | Bytes | sha256 |
| --- | ---: | --- |
| This prompt | 1926 | `d223b57642837757de51932191899fa98c6ed1ad40fd9ade5c68a7a0e0fb6c96` |
| `inputs.json` | 810 | `0aead316cc9c946fcb61917f17d74b83e4565f4a8589516f572d819a90c9326b` |
| `crates/evaluator/src/enumeration_join.rs` | 51742 | `3f24610941495e490ccafbb99ab978f127cb9a9cf678bb394ce7d0ccc73ba461` |
| `crates/evaluator/src/enumeration-registry.json` | 11309 | `deecedc9b8472c2b151bcdbce4345aff91eebf9e6b4126474f6b007771918aac` |
| `crates/evaluator/src/enumeration.rs` | 27635 | `e1593cf5a21ab332b6e1369823ccb156cb7403810b040608145b8c14ae6085f3` |
| `crates/identity/src/closure.rs` | 56835 | `1b66d79a65af3418ec6ca9ce037813ecfc0b2f13db8ecfbcaffe04b18c736aa3` |
| `crates/evaluator/src/lib.rs` | 3074 | `b34b0007ccf50205a7e21a9621f8ebf2f7b491ca864d0f020bfbfca948e9e7ed` |

Copied `inputs/` still pin-equal after the probe. Public export is `inspect_enumeration_join`.

### Trees that are not this kernel

| Tree | `enumeration_join.rs` | Note |
| --- | ---: | --- |
| Copied (reviewed) | 51742 / `3f24610941…` | Unused `snapshot_inventory` field still present |
| Root draft at review start | 51687 / `208bfb0918…` | Field already dropped |
| Root draft **now** | 52433 / `fdd856a022…` | Evolved further; not reviewed |
| Kernel-check injection | 41956 / `4e736c1598…` | Test-only maps; `enumeration.rs` / `closure.rs` / `lib.rs` also differ |

Kernel-check proof: `cases.json` 733231 / `bcdac02be353d04bbdeea51bef69453eaff9ceda43064aa3bd05861c3a29717c` (51 cases, 23 ADMIT / 28 REFUSE, 17 refuse tuples); `result.json` 506 / `f8f69c34d3a01253bb6de82698dd25819cc6c2f90c63a24e6f562b059ad5afb4` exit 0.

### Selected E39 overlay (not mutated; not stale physical reference)

Full 38 overlay under `/tmp/opensip-implementation/m2-enumeration-join-trial-41/reference` (159 files). `composition.json` 739 / `ffc036e53572d120922f6480047b88247db61387f16a170a8b15d2fe92b548dc`.

| Overlay file | Bytes | sha256 |
| --- | ---: | --- |
| `enumeration_model.v1.py` | 50447 | `d32883fdfb7a40395169dfb078c1590844a7f6e85e2c15cc2315ab8990626992` |
| `check-enumeration.v1.py` | 50329 | `bdeeb765e9ddbc293f8771af61274ed3da97bd9c1c52085b09611383a6728e41` |
| `enumeration-plan.schema.v1.json` | 19975 | `10627cb6a22a9ff1674c16c5fa4863a58dc86e5df8ac7ae55c45747b0e60197c` |
| `subject-inventory.schema.v1.json` | 16861 | `6ab46925853d26c1a5f7ae1fbd69db5dcc9052fdefdb1b265e53481b4e1cee33` |

Registry `kindMap` list entries, `languageTable`, `internalFaults` (48), and deficiency-cause rows are byte-equal to this overlay. Plan `$defs/DeficiencyV2` enum equals the native owner enum.

## Tool

- CPython **3.12.13** `/tmp/opensip-implementation/native-case15-reference-env/bin/python` `-I -B -X int_max_str_digits=0` (flags and `get_int_max_str_digits()` both 0). jsonschema 4.25.1.
- Homebrew `rustc` / `cargo` **1.95.0** `--offline --locked`, target `aarch64-apple-darwin`.
- Isolated probe: overlay copied kernel onto a kernel-check product copy under `review/probe/product`; adapted the map harness **only there**. Did not edit kernel-check, draft product, frozen, live, or history.

## Independent reproduction

1. **E39 on the 51 cases** (overlay import, hex-decoded `source_blobs`, no model mutation): **51/51** `C.equal_typed` against frozen `expected`. Report `review/probe/e39_replay.json` 9056 / `309a17c98dc0353261896958c8bf6833bffe1d0978063856f5cd8483ffa89e02`.
2. **Copied `complete_join` on the same 51 cases** (empty `RetainedInputs` registry for schema/mint only, maps built as in kernel-check): `selected_reference_join_cases` **ok** in 0.21s.
3. **Retained reader** `inspect_enumeration_join` on root’s 10 owner-opened packets: isolated harness replay **JSON-equal** expected and **byte-equal** root `retained-check/actual.ndjson` 72177 / `a074f4e2a9ed2d3918e7008454536dfc02b4b2f6accd03a1d603dd64df729c4d`. All 10 ADMIT. Root `retained-check/result.json` exit 0, 0 mismatches, standing “not predicate replay or publication custody”.
4. **Limit:** `complete_join` with `TraversalBudget.steps = 1` on case 0 → `EnumerationJoinError::Limit`. E39 has no step budget; this is a local visit bound, not join-law inequality.

## Public API (copied kernel)

`inspect_enumeration_join(inputs, plan_id, evaluation_refs, budget)`:

1. Shape-check every ref as `ProofInputRef`; collect `domain == "subject-inventory"` digests (order of refs). No host inventory map.
2. `read_inputs`: Plan → snapshot → analysis parameters against **source-bound** `import-registry.json` (unregistered / duplicate key refuse) → required enumeration-plan parameter → membership `current_record_shape` UnitMembershipV1 → snapshot `sourceInventory` rows (duplicate **path** → `Err(Refused(ENUMERATION_ADMISSION_PRECONDITION))`; blob rehash + `require_length`) → native retention on contexts, `inspect_plan_native`, then universes (nested TS `configGraph` / rust `sourceUnitOwnership`; `bindResult` key → `Err(Refused(PRECONDITION))`) → closures → inventory records by digest.
3. `complete_join`: PLAN_SCHEMA early `refuse_result`; `retained_membership_checks` then **UNIT_ROOT early abort**; snapshot/scope/membership digest mismatches; `join_cells` then `join_inventories`; any remaining faults → `refuse_result` empty population. ADMIT never carries a partial population.

`snapshot_inventory` is stored on `JoinInputs` and never read (`dead_code` warning). Draft already dropped it. **Not a finding.**

## Semantic parity that held

Against selected E39 `admit_enumeration`, copied `complete_join` matched:

- PLAN_SCHEMA and UNIT_ROOT **early abort** (PLAN_SCHEMA hides UNIT_ROOT; UNIT_ROOT hides FILE_TOTALITY).
- Unique-first `fault()` / `_add` order on collected join faults (e.g. UNAVAILABLE_INVENTORY then CAUSE; PACKAGE_TOTALITY then ROW_PATH; PRECONDITION then EXTENT_PATHS then PACKAGE_NAME on case 32).
- Cell tuples via sorted list equality (same as `sorted(req_tuples) != sorted(cell_tuples)`).
- Kind map / language table / 48 internal faults / cause-carrier registry.
- File vs package totality (sequence `examinedPaths` vs extent for complete; set of row paths vs extent). Reverse `examinedPaths` is **INVENTORY_SCHEMA** first (schema order), not a silent set-equal ADMIT.
- Duplicate nativeSubjectId / path / projection id (schema or `BTreeSet` insert).
- Duplicate universe within a cell.
- `bindResult` on a universe **map** → REFUSE `[ENUMERATION_ADMISSION_PRECONDITION]`.
- Language, file name, unexpected record, missing record vs schema-failed locator, wrong `parameterDigest`, candidate paths on a non-candidate cap.
- Membership ORDER and ROW_DERIVATION (corrupt `reason` → ROW_DERIVATION then MEMBERSHIP_DIGEST_MISMATCH plus follow-on extent faults; reversed rows → ORDER then digest mismatch).
- Evaluation-subject mint `subject3:` + identity schema; package `packageManifestPath` only for `kind==package`.
- Payload reconcile via JSON value equality vs `C.equal_typed` on reachable rows.

Several intended discriminators are **schema-gated** before join law (swapped `kinds`, default-unit ordinal 1, empty enumerator, 129 bindings, duplicate identical cells, extra plan property, integer examined path, duplicate projection). Both sides REFUSE PLAN_SCHEMA or INVENTORY_SCHEMA. Not a kernel/E39 split.

## Required finding

### 1. Reader-layer `Err(Refused(PRECONDITION))` is not the E39 join REFUSE document

**Id:** `reader-refused-precondition-is-not-join-refuse-document`  
**Severity:** actionable  

Public `read_inputs` fail-closes as `EnumerationJoinError::Refused("ENUMERATION_ADMISSION_PRECONDITION")` for:

- duplicate **path** in snapshot `sourceInventory` (identity `uniqueItems` is whole-row, so two rows with the same path and different sha/bytes still reach this check);
- universe descriptor key `bindResult`.

Selected E39 returns a **REFUSE document** (`result: REFUSE`, `refusals` containing that token, empty population). Copied `complete_join` already builds that document for the same token when the map constructor is used (kernel-check 51 cases; mutation `universe-bindresult` matched). `inspect_enumeration_join` never gets there: the harness retained path maps `Err` to `{"result":"error","detail":"Refused(...)"}`.

Duplicate snapshot inventory also **continues** in E39 (PRECONDITION plus later EXTENT_PATHS / EXTERNAL_PATH / PACKAGE_NAME depending on whether `snapshot_paths` is replaced by the derived unique list). The reader stops at the first duplicate path.

**Action:** Either (a) route those two reconstruct refusals through `refuse_result` so `Ok(value)` is document-equal to E39, or (b) freeze the dual envelope (reconstruct `Err` vs join REFUSE) and make retained adversarial tests match `Err(Refused("ENUMERATION_ADMISSION_PRECONDITION"))` without claiming E39 document equality for those packets. Root’s current 10 retained packets are all ADMIT and do not cover this.

## Not findings (probed, classified)

| Probe | E39 | Copied kernel | Why not a finding |
| --- | --- | --- | --- |
| Unused `snapshot_inventory` field | n/a | stored, never read | User: will be removed |
| `inventories` not a list | PRECONDITION + MISSING_RECORD | JoinInputs is always `Vec` from ProofInputRef digests | Public API cannot express a non-list |
| `universe_domains` not a dict | early PRECONDITION | derived from `frame.domain()` | Public API does not take a host domain map |
| `membership_derivation` incomplete | PRECONDITION | ignored; ADMIT on otherwise-good case 0 | API must not take membership derivation |
| Malformed `snapshot_inventory` object in maps | PRECONDITION (+ UNIT_ROOT) | harness `array()` → RegistryLaw before `complete_join`; field unused in join | Snapshot schema type is array; public reader uses admitted snapshot rows |
| Local `steps=1` | no budget | `EnumerationJoinError::Limit` | Local visit bound, not E39 law |
| New enum registry + 48 faults | exact | exact, compiled in | Live install needs inventory 27 |

## Limits of this note

- Not product install, not ACCEPT-DESIGN-UNIT, not SOURCE38/runtime-v18/full M2.
- Not a claim that kernel-check injection bytes equal the copied kernel.
- Not exhaustive E39 case corpus (51 selected + 33 derived mutations).
- Not MIRI / memory-safety of the broader evaluator.
- Draft product may keep moving; this pin is the copied 51742 kernel.
- Retained adversarial mutation corpus was not present in `retained-check/` (10 ADMIT packets only).
- `check-enumeration.v1.py` historical receipts were not this run’s default; overlay model was imported directly.

Root leads. This is advisory, not runtime or design-unit acceptance.
