# B2-c2b r1: item 14a's record bounds and the S10b remedy carrier (M3-B r10)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 1.**

It implements M3-B r10 (`../PROPOSAL-r10.md`; Codex `codex-m3b-r10-r2`, ACCEPT, after `codex-m3b-r10-r1`): item 14a's two new bounds and its remedy control. It also writes the product carrier of S10b (contract successor 172; Codex `codex-s10b-remedy-r1`), whose row in item 25 names B2-c2b as its consumer. That closes O-1, which B2-c2 routed to the lead before C2 emits graphs (`../b2-c2-r2/SCOPE.md`, "Open items").

**Base:** product main `00ec649` (S10b bound; 172 contract successors; inventory v212); architecture `6d360470`.

**Why a unit, and no plan step.** The B2-c plan r2 gave item 14a to B2-c2, and B2-c2 is bound. r10 amends item 14a, and its row S10b names B2-c2b. So this unit is the law's own consumer. It edits only B2-c2's files and the remedy carrier, and adds no step to the plan.

## What it changes

| File | Change |
| --- | --- |
| `crates/host/src/typescript_config.rs` | Two bounds:<br>• `MAX_EXTENDS_ENTRIES` (64), `TypeScriptConfigGraphV1`'s `extendsResolved` `maxItems`;<br>• `MAX_NODE_PATH_CHARS` (4,096), `CanonicalPath`'s `maxLength`, counted in characters.<br>In `visit`, a node whose canonical path has more than 4,096 characters refuses as `bound` at that node, before its bytes are judged. That is the same line as the 64 KiB check, and both refusals carry the same key and subject. A file whose `extends` array holds more than 64 entries, repetitions included, refuses as `bound` at that file. The count is checked after its JSONC and types and before any entry is classified or resolved. The order is r10's: for a new base, the 32-node check in the caller; then path, bytes, JSONC and types, the entry count, and the edges. |
| `tools/host/typescript_config_vectors.py` | The independent Python reading gains the same two checks in the same places. Its pins move to S10b's native-model copy (the D9 row, remedy and graph schema now come from it) and to `PROPOSAL-r10.md`. Eleven new law controls (121 to 132 cases):<br>• `extends` arrays of exactly 64 entries (all 64 edges kept) and of 65;<br>• 65 entries with a malformed specifier, and with a missing base: both are still `bound`, before any read;<br>• 65 with an entry of the wrong type, which is `malformed`, since types come first;<br>• a base with 65 entries;<br>• entry and base paths of exactly 4,096 and of 4,097 characters;<br>• a non-ASCII base path of 4,096 characters, which is more than 4,096 bytes.<br>Every admitted graph is still validated as `TypeScriptConfigGraphV1` by the model, so the 4,096-character paths are checked against `CanonicalPath`. |
| `crates/host/src/typescript_config_vectors.json` | Regenerated: the new cases, and S10b's remedy in `d9.remedy`. |
| `crates/host/src/typescript_config_tests.rs` | **Schema admission.** Every replayed result's graph must now also be admitted by the product's embedded native schema (`urn:opensip:product-v1:native:evidence-schemas:v2`, `/$defs/TypeScriptConfigGraphV1`).<br>**New test `the_record_bounds_are_the_graph_schemas_own`:**<br>• both constants equal the schema's own `maxItems` and `maxLength`, read from its bytes;<br>• the 64-entry graph and both 4,096-character graphs, ASCII and non-ASCII, are admitted;<br>• one more edge, or one more path character, is refused by the schema. |
| `crates/host/src/outcomes.rs` | `REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED` is S10b's string, byte for byte (LD-S10B-1). The doc comment cites S10b. |
| `crates/host/src/outcomes_tests.rs` | The remedy's pinned length (568 to 646) and SHA-256 (`aea1585b…`), and the doc comment. Row 59's existing test (`typescript_config_tests.rs`) still compares the carrier with the vectors' remedy, which now comes from S10b's model. |

**Unchanged:**
- the public record, the four alias rows and the D9 row (S10's);
- the other refusals and their order;
- `jsonc.rs`;
- every caller (there is none: J1 and C1).

## Lead decisions

- **LD-B2C2B-1. One guard for the two node-level bounds.** The path check and the 64 KiB check share one `if`, with the path first. Both refuse as `native.typescript-config-bound` with the node as the subject, so their relative order cannot be observed. r10 puts the path first, and the code reads that way.
- **LD-B2C2B-2. Admission in the Rust test, not in the reader.** The reader enforces r10's bounds itself. It does not call the schema at run time, because C2 emits the record and admits it there. The test admits every replayed graph against the embedded schema. It also ties the two constants to the schema's numbers, so a schema change cannot silently leave the reader behind.

## Checks

Lane r1, `evidence/b2c2b-checks-r1/`:
- **the host suite** at base and candidate, with equal failure sets (8 at base) and one new passing test;
- **rustfmt** on the edited files (all clean at base) and warning-denied all-targets Clippy;
- **the TypeScript configuration and remedy tests;**
- **the vector checks:** the TypeScript configuration vectors (`--check`), and the framework recognition and YAML subset vectors;
- **FW-01,** the environment exceptions, the operability source census and verify_design;
- **seven mutations,** each failing those tests:
  - the entry bound skipped, off by one, or widened to 65;
  - the path bound skipped, off by one, or counted in bytes;
  - the remedy carrier left at S10's string.

## Not claimed

- No caller (J1, C1) and no C2 graph emission: C2 still owns `TypeScriptConfigProjectionV2`.
- No public record, alias, D9 or vocabulary change.
- No TypeScript limit is claimed for either bound (M3-B r10).
- No qualification.

## Inventory

**No new paths.** Four inherited descriptions name the r9 reading or S10's model copy:
- `typescript_config.rs` ("as r9 amends it", and "cycle, 32-node and 64 KiB checks");
- `typescript_config_tests.rs`;
- `typescript_config_vectors.json` ("the S10 native model copy (contract successor 167)");
- `tools/host/typescript_config_vectors.py`.

After acceptance, a description successor (inventory v213) brings them up to date.
