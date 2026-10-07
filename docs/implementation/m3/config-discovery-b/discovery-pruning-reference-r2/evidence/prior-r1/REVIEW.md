# Discovery pruning reference r1

REJECT-DESIGN-UNIT. requiredFindings: DPR-RF-01, DPR-RF-02.

Subject manifest `docs/implementation/m3/config-discovery-b/discovery-pruning-reference-r1-subject.json` is 2626 bytes, sha256 `4c9268ec8dc2c2c6b7b16017812d8debd620c5d51e886ed9a34b39d1dd7f3483`. Every listed member matches its pin. The list contains `successor.json` twice. Successor `docs/implementation/m3/config-discovery-b/discovery-pruning-reference-r1/successor.json` is 2900 bytes, sha256 `5bf6757c3d1c214d38c9dc1f3b29e58087397352f939cc4ae440b1e30616c675`. `passageOverrides` is `[]`. The record has no `passageSupersessions` key, so this review omits `supersededPassages`. Standing: "PROPOSED reference-only normative pruning correction; no B2 product start or qualification".

Product HEAD `6eb1e744b072837ac3c565ea2c1d9e06118f2036` and architecture HEAD `f8360b573d0b4192e1a8b6aba22d9cc73ff14af3` are the pinned bases. Product is tracked-clean. Architecture is tracked-clean. Its untracked S-OP and E2s drafts stay outside this unit. `~/Library/Application Support/OpenSIP` is absent. The subject names no product path. `design-lock.json` does not yet contain this successor. The record does not grant native or product qualification, and acceptance would not put M3-L in effect or release the held B2-a product start.

## Parents

The two parents match the architecture bytes and the current lock.

- Inventory v166 remains the selected inventory candidate, 614780 / `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`. This unit adds no inventory successor.
- Admitted NE `docs/v2/contracts/product-v1/native-evidence.md` is 329013 / `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`, an accepted design input. U-4a governs where it disagrees with the discovery reference. The outermost pruned segment is the only anchor across dependency, VCS, and Cargo-output reasons. A marker inside a pruned tree is never a unit and never a Cargo root. `markerCount` is exact over a supplied inventory when the basis is `observed-inventory`, and null when the basis is `not-enumerated`. The first-party cap stays 4096. `PrunedTreeV2` and discovery version 2 stay the current records.

`docs/coop/design-corrections/discovery-defaults.py` is 22344 / `f30b68502b6fb70992eb4e9fe4dbd6919df69180e020d6f2e1538f7fa8cfb28c`, byte-identical to the evidence copy. It is before-image evidence. It is not a parent.

## Reference correction

The separate copy is `reference/discovery-defaults.pruning-r1.py`, 22701 / `7817a4adba5d86d47c8197116ea2293c938cc2fa9fd24f823fc249c0472f2fc5`. AST comparison, with attributes excluded, shows two changed declarations: `classify_path` and `cargo_roots_from_markers`. Every other function and class dumps equal, and every module-level statement dumps equal. `DISCOVERY_DEFAULTS_VERSION` and `MAX_WORKSPACE_UNITS` remain 2 and 4096. No schema, reason vocabulary, or numeric bound changes.

`classify_path` still takes the outermost dependency or VCS hit, then the first `target` segment whose parent is a known Cargo root. It keeps the Cargo anchor when that segment index is shallower than the dependency or VCS anchor. `cargo_roots_from_markers` sorts markers by slash count, then UTF-8, and admits a `Cargo.toml` directory only when `classify_path` against the roots already admitted returns none. A root `Cargo.toml` therefore suppresses `target/Cargo.toml`. A `Cargo.toml` whose parent is not already a Cargo root, and which is not inside a dependency or VCS tree, remains a root.

`evidence/check.py` was not run. An independent read-only load of the two stage copies reproduced its 49 controls: 18 changed and 31 unchanged, with no failure. The 18 changes are the five `target` before dependency or VCS segments at the root and under `workspace`, the three Cargo-marker orders at each of those roots, and both 4200-marker Cargo enumerations. For a root `Cargo.toml` plus `target/Cargo.toml` plus 4200 `target/node_modules/pkgN/package.json` paths, the result is one unit at the root and one pruned tree `target` / `cargo-build-output`. With `not-enumerated` and observed directories `target` and `target/node_modules`, `markerCount` is null. With the default observed-inventory basis, `markerCount` is 4201. The same shape under `node_modules` stays one `dependency-tree` anchor with count 4200. Both copies agree on the 4096 admission and the 4097 `WORKSPACE_UNIT_LIMIT` refusal. The stored `checks.json` summary matches that reproduction: `passed` true, 49 controls, 18 changed, the same two functions, `nativeCensus` false, `qualification` false, `productEdited` false. The marker arrays were not reprinted.

## Required findings

DPR-RF-01. The subject `files` array repeats `successor.json`. `pin_rows` accepts a pin list only when its paths equal the sorted unique paths. This subject fails that check.

DPR-RF-02. `candidates` ends with `successor.json` at 2678 / `759d70f318c809ed03313b06e5aaa9dfe947768d43a6379398db2bbb9425291e`. Removing that one row and dumping the same indentation produces exactly those bytes. `contract_successor` requires the candidate paths to be the subject members excluding the record, with each pin equal to the subject pin. The self row is outside that set, and its digest is not the record's digest.

The pruning correction above can be retained. The subject must name the corrected record once, and `candidates` must be the other nine members only.
