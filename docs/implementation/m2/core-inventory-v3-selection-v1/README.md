# CoreInventoryV3 release-record successor (463b)

PROPOSED. This unit adds `CoreInventoryV3`, the core-inventory successor that proposal 463 r5 item 6 names. Each platform row carries two signed members: `stateWriter` (K) and `requiredCodeSigningFlags`. The unit changes 7 product files, listed in materialization-map.json, against product 6f39619. It needs an actual independent review and root assent before selection.

## Law

- docs/implementation/m2/initial-core-launch-463/PROPOSAL.md, r3 with the accepted r5 amendment. Item 6: K and the code-signing flags are signed members of `CoreInventoryV3`, per platform row. `stateWriter` is 1 or 2. `requiredCodeSigningFlags` is the set the running image's `CS_OPS_STATUS` must include. A missing or unknown value refuses. This supersedes owner.md §1a step 3's "adds no metadata member".
- The r3 "K" section: K=2 only when the admitted member names the stage-2 writer, K=1 only for the stage-1 writer, and any other or missing value refuses. There is no default.
- S9 (docs/v2/contracts/product-v1/security-and-lifecycle.md, "Stage transition, schema bridge and floor continuity"): stage 1 writes with state decoder v1, stage 2 with `state-decoder.v2`. The reference model names the member `stateWriter` (security_lifecycle_model_v1.py `SCHEMA_BRIDGE`, `'stateWriter': 1` and `'stateWriter': 2`).

## Decisions

1. `CoreInventoryV3` is `CoreInventoryV2` with `inventorySchema` const 3 and `platforms` items `CorePlatformV3`. Every other member, bound and rule is unchanged.
2. `CorePlatformV3` is `CorePlatformV2` plus two required members:
   - `stateWriter`: integer, enum [1, 2].
   - `requiredCodeSigningFlags`: an array of 1 to 16 names. The names are unique and sorted ascending by string (`x-opensip-order: utf8`, which is strict). Each name comes from the closed set in the table below, and the array must contain `CS_VALID`. Because the set has 7 names and the order is strict, the 16 bound cannot be reached. It is kept as the decided bound.
3. `CoreInventoryV2` and `CorePlatformV2` are unchanged. The existing reader `core_inventory::project` still admits exactly `CoreInventoryV2`, so the 318, 322 and 323 corpora keep their results. V3 is an opt-in reader: `core_inventory::project_v3` admits exactly `CoreInventoryV3`. Neither reader accepts the other schema, so a V2 inventory never gets a default K or default flags.
4. `project_v3` runs the same binding as V2: semantic version, protocol membership, platform order and presence, the tree, layer and requires checks for every row, and the embedded bootstrap frame. The descriptor has the same shape (`schemaVersion` 2, `kind` "core"), and the closure is `closure2:` over it by the same rule. Only `manifestDigest` changes, because the body changes. For the selected platform row, it exposes `state_writer()` (1 or 2) and `required_code_signing_flags()` (the OR of the named bits, always including `CS_VALID`).
5. The two definitions are appended after the last existing `$defs` entry (`WalkRecord`), not in alphabetical position. The shape generator numbers fragments depth-first in `$defs` order. The record270 fragment fixtures and the generated visitor file (`trust_record_visit_nodes.rs`, via `fragment_matches(<index>)`) pin those numbers. Appending keeps nodes 0 to 554 byte-identical. The new definitions occupy nodes 555 to 562. `stateWriter` reuses the existing identical node 401, and the V2 `layers` and `requires` fragments are shared. The generated visitor file does not change.

## Code-signing flag bits

| Name | Bit | Header comment |
|---|---|---|
| CS_VALID | 0x00000001 | dynamically valid |
| CS_HARD | 0x00000100 | don't load invalid pages |
| CS_KILL | 0x00000200 | kill process if it becomes invalid |
| CS_RESTRICT | 0x00000800 | tell dyld to treat restricted |
| CS_ENFORCEMENT | 0x00001000 | require enforcement |
| CS_REQUIRE_LV | 0x00002000 | require library validation |
| CS_RUNTIME | 0x00010000 | Apply hardened runtime policies |

Source: `kern/cs_blobs.h` in the macOS 27.0 SDK, /Library/Developer/CommandLineTools/SDKs/MacOSX27.0.sdk/System/Library/Frameworks/Kernel.framework/Versions/A/Headers/kern/cs_blobs.h (sha256 b3ecf166337427329bd9e8df90d08f1403e08191401ac0ad8b54b71052dd775d), lines 36, 44, 45, 47, 49, 50 and 54. The MacOSX26.5 SDK header has the same seven values. They are also the values in the XNU open-source `osfmk/kern/cs_blobs.h`. The SDK's usr/include has no cs_blobs.h. The header is only in Kernel.framework. `CS_OPS_STATUS` is the `csops` operation that returns this flag word. No `CS_OPS_STATUS` define was found in the SDK usr/include, and this unit does not call `csops`. The table is `core_inventory::CODE_SIGNING_FLAGS`, and the same values are in the `CorePlatformV3` description.

## Pins changed

The trust-record schema is a pinned generator input:

- tools/security/inputs/trust-record-schema.json: 178125 B, sha256 359345411d91585f76bbbad276b6bc2d774ba3e167aeb0bb2b70bfabb44d902f (was 173336 B, a043130057d2e388…).
- tools/security/generators/record_shapes.py and record_visits.py: the asserted schema sha256.
- tools/security/inputs/reference-registry.json: `schemaSha256` only. `referenceSha256` and the registry rows are unchanged. The file becomes sha256 383a7d5a62729d34a9e4a0206f8e207554ccff99ad564a628028be61108e71c5 (26308 B, unchanged length).
- tools/security/inputs/sources.json: the schema bytes and sha256, and the registry sha256.
- crates/security/src/generated/trust_record_shape_nodes.rs: regenerated by `tools/generate_security_tables.py --write` with rustfmt 1.9.0. Its header names the new schema sha256.

`python3 -I -B tools/generate_security_tables.py --check` then reports all five outputs unchanged against the pinned inputs. No design-lock input, generation source (schemas/source-map.json), admission source or contracts generator-closure file changes. None of these 7 product files is in the contracts generator closure.

## Tests

In crates/security/src/trust/core_inventory.rs:

- `v3_projects_both_release_members_of_the_selected_row`: the V3 form of the 318 baseline projects. The selected row's `stateWriter` and flag mask are returned, and each name maps to its own bit. The descriptor equals V2's except `manifestDigest`, the closure follows the same rule, and the files are identical.
- `v2_and_v3_readers_do_not_cross`: V2 bytes still project through `project` and refuse through `project_v3`. V3 bytes refuse through `project`. V3 keeps V2's binding refusals.
- `v3_release_member_shapes_refuse_missing_and_unknown_values`: each of these refuses, both at shape and through `project_v3`: a missing `stateWriter`; `stateWriter` 0, 3, -1, "2" or null; missing flags; flags empty, unsorted, duplicate, unknown, lower-case, without `CS_VALID`, 17 members, an integer mask, or an integer member. A single row without the members refuses the whole inventory. A row carrying an extra member refuses.

The existing 318 corpus (125 cases, 53 positive) and the record270 fragment, pattern and record corpora still pass. `cargo test -p opensip-security --lib` passes 455 tests, with 2 ignored. Workspace clippy with `-D warnings` and `cargo fmt --check` pass.

## Parents

No accepted architecture unit selects any of these 7 product files, so there is no product-copy parent. The two parents are the accepted, unchanged law documents this unit implements: security-and-lifecycle.md (S9) and security_lifecycle_model_v1.py (`stateWriter`). There are no passage overrides. The 463 proposal is not a design-lock-selected path, so it cannot be a parent.

## Not in this unit

It does not add a caller of `project_v3`, compare the mask with a live `CS_OPS_STATUS`, derive `InitialCore`, or change the anchor, envelope or profile readers. It makes no release, signing or qualification claim.
