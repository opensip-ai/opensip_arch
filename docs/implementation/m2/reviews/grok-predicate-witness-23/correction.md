# Correction: predicate-witness-23 inherited lock counts

**Not fresh-blind.** Original `report.md` / `report.json` preserved (`9aa0841d…ba2e` / 6281, `1512d0cb…7c3e` / 6541). Frozen subject and trial files unchanged. No source edits. Root remains lead.

Root independently read the source-23 report: **no code findings.** The shared documentation error is that the inherited private `product/design-lock.json` was labeled **18/22**. That label is the live lock **at earlier source freeze**, not the bytes actually inherited in this trial. This review repeated that label. It is not a `proofs.rs` finding.

**Source verdict remains `NO-REQUIRED-FINDINGS`.** No design-unit or runtime acceptance was claimed. No code changed. Live still has no `proofs.rs`.

## Actual inherited lock (private product bytes)

Independently hashed `m2-predicate-witness-subject-23/product/design-lock.json`:

| | |
| --- | --- |
| Bytes | **36241** |
| SHA-256 | `515f092c1c74429397bf215184ffae24af93c892ca546292c05a717bd47fb523` |
| `inventorySuccessors` | **9** |
| `contractSuccessors` | **15** |

Last inventory **candidate:** `docs/implementation/m2/repository-file-inventory.v11.json`  
Last contract **record:** `docs/implementation/m2/capability-totality-reference-selection-v1/successor.json`

The same pin is the inherited lock of frozen run-links-19, glob-21, and policy-admission-22. It is **not** live 18/22 and **not** live 18/24.

Wrong in completed `report.md` line 7 / limits, and `report.json` `standing` / `candidateLockHistorical.note`: “historical 18/22”. The pin, bytes, and “not current live / not runtime acceptance” were already correct.

## Current live lock

Independently hashed `/Users/sb/code/opensip-ai/opensip/design-lock.json`:

| | |
| --- | --- |
| Bytes | **54390** |
| SHA-256 | `f8e47e7ae66e367b61b46a7cdb2b2aef0f4e114c7fb4b5ecec62b3901c502c71` |
| `inventorySuccessors` | **18** |
| `contractSuccessors` | **24** |

Last inventory candidate remains v20. Last contract is runtime **v10**. Live `policy.rs` matches frozen-22; live `lib.rs` has no `proofs` module. Source-23 is **not** installed.

The original report’s **live 18/24** citation was already correct. Only the inherited-lock count was wrong.

## Source-review validity

The scoped source review compared `inspect_predicate_witnesses` to selected reference-v2 I 1829–1852, classified 136/19/0, and did **not** treat the inherited lock as a selected 18/22 or 18/24 runtime base. Mislabeling successor counts does not reopen the owner law, pins, or `NO-REQUIRED-FINDINGS` verdict. It is not design-unit acceptance.

The frozen trial README carries the same 18/22 wording. That file is **not** patched here.

## Runtime-11 candidate (not this source; not acceptance)

A separate composition candidate replaces the product lock with **exact live 18/24** (`f8e47e7a…2c71` / 54390) and keeps frozen-23 `proofs.rs` / `lib.rs` pins (`fd371174…48a0` / 10578, `501a071b…f821` / 1942). Recorded source-only host isolation: **124** sources, workspace tests **106** + evaluator doctest **1** = **107**. Six composed-base preflight commands exit 0. Preflight standing: Base 18/24 composition only; native runtime v11 still unselected. That is **not** runtime acceptance of source-23.

## requiredFindings

None (documentation correction only).
