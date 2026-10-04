# CR-1 r4 — ACCEPT-DESIGN-UNIT

Reviewer GROK2. Design unit CR-1, law M3-C item 7, the security and DR-103 host-vocabulary successor. This round answers r3's RF-CR1-3. The review directory keeps the name the builder emits.

Subject `docs/implementation/m3/snapshot-plan-c/cr-1-subject.json`, 2266 bytes, sha256 `e9e1a406dcf9e75d2359b609087e80327ab1f47554eb094425b2e3ae8ef781ba`. Eleven members. Successor `docs/implementation/m3/snapshot-plan-c/cr-1/successor.json`, 10694 bytes, sha256 `0f1e187b0af676bb3face09a5d0055a75a77a0d898071763a2952d487a3ce9f8`. `cr-1-unit.json` is the lead draft and is not part of the subject. No cargo. `~/Library/Application Support/OpenSIP` is absent.

## Verdict

ACCEPT-DESIGN-UNIT. No required findings.

RF-CR1-3 is resolved. CR-T9's added sentence is the r3 replacement, word for word. It matches the two entry points in `component_manifest.rs`. The other sentences that name those entry points already matched, and they are unchanged. Nothing else in the contract, the schema, the four overrides, or the map instruction moved.

## RF-CR1-3

README.md:248 keeps CODEX2's CR-T9 paragraph and replaces only the sentence r3 added. The new sentence is:

> (r3) In particular, a closure-only manifest with no `commands` whose name collides with a reserved name refuses on the existing reserved-name route in both `validate` and `validate_inventory`. A collision with a live name of a different `(stableId, provenance)` refuses on the existing live-name route in `validate` only; `validate_inventory` receives reserved names and no live-name context, and that collision stays inventory-valid.

The r3 sentence, "collides with a reserved or live name refuses on that existing route, in both", is gone. `check_cr_1.py` asserts the replacement and the absence of that sentence.

`component_manifest.rs` is the same blob at `9c11c53`, `392499e`, `5e25d04` and `5214350` (`2ece3789…`). The lines r3 cited still hold:

- Lines 268-270 refuse a key that is in `reserved_names`. Both entry points pass that set.
- Lines 271-276 refuse a live name of a different `(stableId, provenance)`. The loop is `context.map_or(&[][..], |c| c.live_names.as_slice())`.
- `validate` (395-397) calls `validate_inner` with `Some(context)`, so both checks run.
- `validate_inventory` (398-403) calls `validate_inner` with reserved names and `None`, so the live-name loop checks nothing and the collision stays inventory-valid.
- Both reach `command_checks` at line 414.

The inventory oracle at `5e25d04` is the same fixture. `CUSTODY/different-owner-name` and the host-live-name cases are inventory-valid and host-invalid. `catalog-reserved-name` is invalid on both flags. The production caller passes the catalog reserved-root set and no live names.

That is the existing route. A closure-only manifest with no `commands` keeps the reserved-name refusal on both entry points and the live-name refusal on `validate` only.

## Entry-point audit

The other sentences that name an entry point:

- The map's `component_manifest.rs` instruction is byte-identical to r3, including the line-range sentence. It says `validate_inner` calls `command_checks` at 414 for both `validate` (395-397) and `validate_inventory` (398-403), so the split applies to both. It does not say a live-name collision refuses in `validate_inventory`.
- The r3 history row in the README says the same call at 414, and it now notes that r4 corrects CR-T9's sentence.
- LD-7's C2a bullet and CR-T7's last line name no entry point. Both are the r3 text.
- The new r4 table states the split the product has: `validate` runs both checks, and `validate_inventory` passes context `None`.

## Diff against r3

Frozen r3 members are `reviews/codex2-cr-1-r4/r3-members/`, subject `24c880b4…`.

Unchanged byte for byte: the completed-schema copy (`343dc517…`, 25128), `evidence/verify_scratch.py` (`f30ac855…`, 6264), the four passage overrides, the parents, `standing`, and the map's five `alsoChangedByC2a` instructions.

`successor.json` differs only in candidate pins. `materialization-map.json` differs only in `baseProductHead` (`5e25d04b3bfa85a244f5d958fe089e9626fd33fa`). `PASSAGES.md` differs only in the header (`5e25d04`, 87 successors). `schema-audit.json` and `copies-report.json` differ only in the product revision. `audit_schema.py` and `build_cr_1.py` change the default revision, and the builder's unit template names `codex2-cr-1-r4` and the r4 assessment. `check_cr_1.py` adds the RF-CR1-3 assertions and defaults to `5e25d04`. README.md adds the r4 section, rewrites the r3 rows as history, and retargets the status, base, parents, binding, reviewer points and evidence runs. The CR-T9 bullet changes only in the added sentence.

## What r3 checked, at 5e25d04

The security inputs, the generator, `component_manifest.rs`, the generated shape, both manifest fixtures and `tools/verify_design.py` are unchanged from `392499e` to `5e25d04`. The lock at `5e25d04` is 501382 bytes, sha256 `9afddcbe…`, 87 contract successors. CRC-1 remains the 83rd. Its selectors are still disjoint from CR-1's four (SL line 70 and the three DR-103 field pointers). The schema copy, the oneOf role split, and the 11,010-case audit are the r3 bytes.

`build_cr_1.py --check` reports identical bytes, including the unit draft. `check_cr_1.py` passes at `5e25d04`, `392499e`, `cd5958b` and `9c11c53`: four overrides, the five-row table, copy `343dc517…`, 55 product shape role cases. `audit_schema.py --deps` the r2 jsonschema 4.25.1 directory, without `--write`, reports identical, 11,010 cases and 100 variants.

`verify_scratch.py --rev 5e25d04` passes, design-only: 87 to 88, four overrides, no supersession, inventory `repository-file-inventory.v135.json`, 100 inheritance rows. `--rev 392499e` is 83 to 84, inventory v134, 55 rows. `--rev cd5958b` is 82 to 83 alone and 82 to 84 with `--after-crc-1` and with `--before-crc-1`.

Current product main is `52143504e1e1b20faa607ef9179be825882664f0`. From `5e25d04` to that commit the only product change is `design-lock.json` (22 insertions), the S18 binding. `component_manifest.rs` is the same blob. `verify_scratch.py --rev 5214350` passes: 88 to 89, the same four overrides, no supersession, inventory v135, 100 inheritance rows. S18 does not take a CR-1 selector. Checkout-mode verify was not rerun, because the checkout is `5214350` rather than the unit's base `5e25d04`. The design-only runs are the checks against those locks. All 51 pins in `hashes.txt` match.
