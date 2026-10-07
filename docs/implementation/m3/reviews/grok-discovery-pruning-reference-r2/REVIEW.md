# Discovery pruning reference r2

ACCEPT-DESIGN-UNIT. requiredFindings empty. DPR-RF-01 and DPR-RF-02 are closed.

Subject manifest `docs/implementation/m3/config-discovery-b/discovery-pruning-reference-r2-subject.json` is 3817 bytes, sha256 `69d5bc075b6770d26243d5abe6cee7e0ecc14982356a68446cb224456bdcd4a9`. All 16 members match. Their paths are sorted and unique, and `successor.json` appears once. Successor `docs/implementation/m3/config-discovery-b/discovery-pruning-reference-r2/successor.json` is 4091 bytes, sha256 `3a379611cebdb8521ec4a39c57f1d8ae5013371421cc9ef292f8dc216b8244bf`. `passageOverrides` is `[]`. The record has no `passageSupersessions` key, so this review omits `supersededPassages`. Standing: "PROPOSED reference-only normative pruning correction; no B2 product start or qualification".

`candidates` is the other 15 subject members. The record path is absent. Each candidate pin equals its subject pin, and the candidate paths are sorted and unique. That is the coverage `contract_successor` requires.

Product HEAD `6eb1e744b072837ac3c565ea2c1d9e06118f2036` and architecture HEAD `f8360b573d0b4192e1a8b6aba22d9cc73ff14af3` are the pinned bases. Product is tracked-clean. Architecture is tracked-clean. Its untracked S-OP and E2s drafts stay outside this unit. `~/Library/Application Support/OpenSIP` is absent. The subject names no product path. `design-lock.json` does not yet contain this successor. The record does not grant native or product qualification, and acceptance does not put M3-L in effect or release the held B2-a product start.

## Closed findings

DPR-RF-01 was a duplicated `successor.json` row in the r1 subject. This subject lists that record once, and `pin_rows` would accept the path list.

DPR-RF-02 was an r1 self-candidate pinned at the digest of the record with that row removed. This record's candidates exclude the record. `evidence/freeze-r2.py` builds the candidate list before it appends the record to the manifest, and it refuses to start when the r2 stage directory already exists. That stage exists, so the same builder cannot freeze it a second time. The builder was not run. Its stage copy is byte-identical to the authoring `freeze-r2.py`. `evidence/freeze-defect.json` records the r1 cause as a second freeze that included the existing successor as a candidate and duplicated the manifest row.

The rejected r1 evidence is frozen and matches the r1 stage and review: subject 2626 / `4c9268ec8dc2c2c6b7b16017812d8debd620c5d51e886ed9a34b39d1dd7f3483`, successor 2900 / `5bf6757c3d1c214d38c9dc1f3b29e58087397352f939cc4ae440b1e30616c675`, and `REVIEW.md` plus `review.json` from `/tmp/opensip-implementation/reviews/grok-discovery-pruning-reference-r1`. The r1 stage is still present and was not overwritten. `author.py` is the same 3424-byte builder as r1.

## Parents and reference

The two parents match the architecture bytes and the current lock.

- Inventory v166 remains the selected inventory candidate, 614780 / `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`. This unit adds no inventory successor.
- Admitted NE `docs/v2/contracts/product-v1/native-evidence.md` is 329013 / `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`. U-4a requires the outermost pruned segment across dependency, VCS, and Cargo-output reasons, and no marker inside a pruned tree as a Cargo root.

`docs/coop/design-corrections/discovery-defaults.py` remains 22344 / `f30b68502b6fb70992eb4e9fe4dbd6919df69180e020d6f2e1538f7fa8cfb28c`, byte-identical to the evidence copy. It is before-image evidence, not a parent.

`reference/discovery-defaults.pruning-r1.py` is 22701 / `7817a4adba5d86d47c8197116ea2293c938cc2fa9fd24f823fc249c0472f2fc5`, byte-identical to the r1 copy. `evidence/checks.json` is 665112 / `cafb7f6a0b3ddfe033e1ad93b29e5db64ab03722672f1978ff113ede449c3993`, also byte-identical. The r1 review loaded those bytes and reproduced 49 controls, 18 changed and 31 unchanged, with AST changes limited to `classify_path` and `cargo_roots_from_markers`. `DISCOVERY_DEFAULTS_VERSION` and `MAX_WORKSPACE_UNITS` stayed 2 and 4096. The stored summary is `passed` true, those same counts and function names, `nativeCensus` false, and `qualification` false. `evidence/check.py` was not run, and the 4200 marker paths were not reprinted.

`classify_path` keeps the first Cargo `target` whose parent is a known Cargo root when that segment is shallower than the dependency or VCS hit. `cargo_roots_from_markers` admits a `Cargo.toml` directory only when that classifier, applied parent-first, returns none. A root workspace with `target/node_modules/...` therefore reports `target` as `cargo-build-output`. `Cargo.toml` inside that tree does not become a second root. The 4200 supplied paths under that tree are one outer anchor, with `markerCount` null on `not-enumerated` and 4201 on observed inventory. The `node_modules` case stays one dependency anchor of count 4200. Both copies agree on the 4096 admission and the 4097 `WORKSPACE_UNIT_LIMIT` refusal.

After this acceptance and root assent, `verify_design` runs on the current main lock, this architecture record lands in one commit, and the product lock bind lands in a separate commit. Nothing is pushed.
