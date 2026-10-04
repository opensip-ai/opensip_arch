# CR-1 r3 — REQUIRED-FINDINGS

Reviewer GROK2. Design unit CR-1, law M3-C item 7, the security and DR-103 host-vocabulary successor. CODEX2 reviewed r1 and r2. This round answers RF-CR1-2. The review directory keeps the name the builder emits.

Subject `docs/implementation/m3/snapshot-plan-c/cr-1-subject.json`, 2266 bytes, sha256 `24c880b436a48848d36c0e3a005ed8b5ec96ea7f66018c99b2fe49119de7d82f`. Eleven members. Successor `docs/implementation/m3/snapshot-plan-c/cr-1/successor.json`, 10694 bytes, sha256 `728fbcc84e60850c842d56ac5c9c6867b2dec2da3de7967886d1337c1918b12b`. `cr-1-unit.json` is the lead draft and is not part of the subject. No cargo. `~/Library/Application Support/OpenSIP` is absent.

## Verdict

REQUIRED-FINDINGS. One finding, RF-CR1-3.

RF-CR1-2 is partly resolved. The map, LD-7, CR-T7, and the required CR-T9 paragraph make only command-tree validation conditional on `commands`. Component-name and manifest-alias admission stays mandatory for every role, in both `validate` and `validate_inventory`. The cited line ranges are right. The sentence the lead added to CR-T9 is not: it sends a live-name collision through `validate_inventory`, and the existing inventory route admits that collision.

## RF-CR1-3

CR-T9 at README.md:235 ends with:

> (r3) In particular, a closure-only manifest with no `commands` whose name collides with a reserved or live name refuses on that existing route, in both `validate` and `validate_inventory`.

`command_checks` at `component_manifest.rs@392499e` (the same bytes at `cd5958b` and `9c11c53`) has two name checks after the command tree:

- Lines 268-270 refuse when any key is in `reserved_names`. Both entry points pass that set. `validate` passes `context.reserved_names`. `validate_inventory` takes `reserved_names` as its second argument.
- Lines 271-276 refuse when a live name of a different `(stableId, provenance)` hits a key. The loop is `context.map_or(&[][..], |c| c.live_names.as_slice())`. `validate` (395-397) passes `Some(context)`. `validate_inventory` (398-403) passes `None`. With no context the loop is empty, and the collision admits.

Both functions call `validate_inner`, which calls `command_checks` once at line 414. That is why the split applies to both entry points. It does not give `validate_inventory` a live-name input. The production caller in `trust_ordinary_metadata.rs` passes the catalog `reservedRootCommands` set.

The inventory oracle records the split. In `inventory293.ndjson` (301 rows), `host-live-name-conflict` and `CUSTODY/different-owner-name` are inventory-valid and host-invalid. `catalog-reserved-name` and `COMMAND/reserved` are invalid on both flags.

CODEX2's required CR-T9 paragraph is already on that line, immediately before the added sentence, and it already states the live-name rule and the same-`(stableId, provenance)` coexistence exception. The added sentence is the part that puts a live-name refusal on the inventory entry point. That would change inventory-body admission. RF-CR1-2 said to preserve the existing admission.

Replace only the added sentence with:

> (r3) In particular, a closure-only manifest with no `commands` whose name collides with a reserved name refuses on the existing reserved-name route in both `validate` and `validate_inventory`. A collision with a live name of a different `(stableId, provenance)` refuses on the existing live-name route in `validate` only; `validate_inventory` receives reserved names and no live-name context, and that collision stays inventory-valid.

The map's added line-range sentence stays. It says `validate_inner` calls `command_checks` at 414 for both entry points, so the split applies to full host admission and to inventory-body validation. That is the right claim, and it is within the r2 fix.

## What r3 got right

The map's `/alsoChangedByC2a` owner instruction starts with CODEX2's exact `after` text. LD-7's C2a bullet and CR-T7's last line match the exact replacements. The old sentence that gated all of `command_checks` on `commands` is gone. `build_cr_1.py` emits that map string as `OWNER_CHANGE`.

Line ranges at `392499e`, identical at `cd5958b` and `9c11c53`:

| Citation | Lines | What is there |
|---|---|---|
| `command_checks` | 166-279 | The function, from the signature through the closing brace |
| Command-tree checks | 171-256 | Line 171 indexes `m["commands"]`. Roots, root-name match, command names, scopes, command aliases, options, arguments, and the parent walk |
| Name and alias admission | 257-276 | Keys from `manifest.name`, manifest aliases, and the mounted-root aliases; duplicate-key refusal; `reserved_names`; live names of a different `(stableId, provenance)` |
| `validate` | 395-397 | Calls `validate_inner` with `Some(context)` |
| `validate_inventory` | 398-403 | Calls `validate_inner` with reserved names and `None` |
| Call | 414 | The single `command_checks` call |
| Executable entrypoint | 337 | Inside `tree_checks`, still the check the r2 text names |

For a closure-only manifest the name set is formed without reading `commands`. Analyzer still includes mounted-root aliases. The executable-entrypoint check stays analyzer-only. A closure-only entrypoint names a regular-file entry directly. Closure-only roles still require `capabilities []` and `permissions []`. Duplicate keys, the reserved list, a different-`(stableId, provenance)` live name, and the same-identity coexistence exception all stay in the admission the r2 text required.

## Diff against r2

Frozen r2 members are `reviews/codex2-cr-1-r3/r2-members/`, subject `4e1b169b…`. Against the r3 members, the only differences are the ones the request lists.

Unchanged byte for byte, matching the r2 pins: `completion/manifest-schema.completed.v1.json` (`343dc517…`, 25128) and `evidence/verify_scratch.py` (`f30ac855…`, 6264).

`successor.json` differs only in candidate pins. `passageOverrides` (four), `parents` (DR-103 v11 and security-and-lifecycle.md), and `standing` are byte-identical to r2. There is no supersession.

`materialization-map.json` differs in `baseProductHead` (`392499e3a42ab9f45d517b8c267a83031abf3863`) and in the `component_manifest.rs` change string. The other four `alsoChangedByC2a` entries are unchanged.

`PASSAGES.md` differs in the header line that names the lock (`392499e`, 83 contract successors). The passage texts are unchanged.

`audit_schema.py`, `schema-audit.json`, and `copies-report.json` differ only in the product revision pin (`cd5958b` to `392499e`). The audit still records 11,010 verdicts and 100 variants.

`build_cr_1.py` defaults to `392499e`, emits `OWNER_CHANGE`, and points the unit template at `codex2-cr-1-r3` with the r3 assessment. `check_cr_1.py` defaults to `392499e` and adds the RF-CR1-2 assertions. README.md carries the r3 changes section, the r2 rows as history, the new base, the `verify_scratch.py` Files row, the binding path, and the reviewer points, plus the LD-7, CR-T7, and CR-T9 text above.

No contract text, completed schema, or passage override changed.

## r2 acceptances at 392499e, with CRC-1 bound

The product files the request pins match `git show 392499e3a42ab9f45d517b8c267a83031abf3863`. From `cd5958b` to `392499e` the only product diff is `design-lock.json` (22 insertions). The security inputs, the generator, `component_manifest.rs`, the generated shape, and both manifest fixtures are byte-identical at `9c11c53`, `cd5958b`, and `392499e`. The lock at `392499e` is 335667 bytes, sha256 `d1b2a5d1…`, 83 contract successors, CRC-1 the 83rd. CRC-1 on disk is the accepted r4 subject `ec896801…` and successor `29df5f5e…` (21493 bytes).

CRC-1's nine overrides are on identity-and-evidence, the I1-L identity schema, the evaluator composition contract, workflows-and-surfaces, the effective-workflows reference, and the detector-manifest description. CR-1's four overrides are SL line 70 and DR-103 fields 7 type, fields 7 semantics, and fields 8 semantics. The parent-and-selector sets are disjoint. CRC-1's binding does not take a passage r2 accepted for CR-1.

The completed-schema copy, the oneOf role split, the 11,010-case audit, and the four insert-only overrides are the r2 bytes. LD-8 and LD-9 are unchanged. Nothing r2 accepted about the schema or the role table fails at this base.

## Evidence rerun

`python3.14 -I -B` at `nice -n 19`, scratch under this review directory. The r2 deps directory supplied jsonschema 4.25.1. `--write` was not passed.

- `build_cr_1.py --check`: identical, empty differs list.
- `check_cr_1.py` at the default `392499e`, at `--rev cd5958b`, and at `--rev 9c11c53`: passed, four overrides, the five-row table, copy `343dc517…`, 55 product shape role cases, arch role value `builder` only.
- `verify_scratch.py --rev 392499e`: passed, 83 to 84, four overrides, no supersession, inventory v134, 55 inheritance rows.
- `verify_scratch.py --rev cd5958b`: 82 to 83. With `--after-crc-1` and with `--before-crc-1`: 82 to 84 each.
- `audit_schema.py --deps` the r2 directory: identical, 11,010 cases, 100 variants.

The product checkout is `5e25d04`, five commits after `392499e` (RUST3-LIM, FA-2, SD-5, FA-1, and the M3 package scaffolds, with inventory v135). Checkout-mode `verify_scratch.py` was not run, because that mode reads the checkout's lock. The design-only `--rev 392499e` run is the check against the base this unit names. In that mode generation and admission source counts are unset; the lead's checkout figures of 40 and 48 were not remeasured.

## Finding resolution

RF-CR1-2 is partly resolved, as `review.json` records. The required replacements and the line ranges do the split. RF-CR1-3 is the added CR-T9 sentence.
