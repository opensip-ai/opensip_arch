# S12 F01 correction binding r2

ACCEPT-DESIGN-UNIT. requiredFindings empty.

This accepts the design-law bind only. It grants no implementation, inventory, product code, or J3b qualification.

Subject manifest `docs/implementation/m2/crash-matrix-x9/s12-f01-r2-subject.json` is 7417 bytes, sha256 `f641cf7ee3bacbbaded5c6ef75f656b155539ee9c0cfde135f7f3bd3e5dbdd95`. All 31 members match the stage bytes. Their paths are sorted and unique, and `successor.json` appears once. Successor `docs/implementation/m2/crash-matrix-x9/s12-f01-r2/successor.json` is 7730 bytes, sha256 `70d54d1348595bdaa8189d6c7e14fe176e031bffeeeb3f3606d16662e1a1485f`. Keys are `schemaVersion`, `standing`, `parents`, `passageOverrides`, and `candidates`. `passageOverrides` is `[]`. The record has no `passageSupersessions` key, so this review omits `supersededPassages`. Standing: "PROPOSED S12 F01 law correction binding only; no product/inventory/J3b implementation acceptance".

`candidates` is the other 30 subject members. The record path is absent. Each candidate pin equals its subject pin, and the candidate paths are sorted and unique. Neither parent path is a member, so the record does not overwrite a parent.

Product HEAD `66c82df22c7f8425c1a5c99c661ff0c7c025af9b` and architecture HEAD `7e76bc3757dba065bc330c6192c857217f34e450` are the pinned bases. Product is tracked-clean. Architecture is tracked-clean. Its untracked drafts stay outside this unit. `design-lock.json` does not yet contain this successor. `~/Library/Application Support/OpenSIP` is absent.

## Wording

The r17 prefix stays byte-exact. Against the accepted r1 proposal, the r2 proposal changes two lines and nothing else.

The status line now says the narrow correction was accepted in r1, that this revision corrects the clock spelling and supplies the successor binding, and that it is not yet bound or in effect.

The clock sentence now states X9 r2 item 3's script: the n-th wall reading of ordinal k is `E + 3600*k + n`, n runs from 0 through 3599, the candidate child is ordinal 1, and the finalize child is ordinal 2. Every finalize wall reading is later than every candidate reading. The first samples are E+3600 and E+7200. That is the script the r1 review checked: a 3600th reading is the harness error, and ordinal 2's first second is the first second after ordinal 1's last. The expectation table, the two `stateUnchanged` cells, the journal-floor account, and the passage precedence are the same text as r1.

## Parents and provenance

Two parents, both current design-lock inputs, and both matching architecture HEAD:

- `docs/v2/architecture/implementation-boundaries-and-build-plan.md` is 112850 / `8e6e8babd30bc3421f605efea9aae4b2d4a5c3c4cbfa4315bbf74cbe4ccbd33b`.
- `docs/v2/contracts/product-v1/security-and-lifecycle.md` is 119915 / `a319da39b9f90aff4483a295af3fe004540c71861fb2bd34e84c7e1318bad9d6`.

Accepted r17, X4T r12, and the r1 review stay in the provenance archive. They are not parents. The proposal text still carries the narrow precedence: only S12.3's whole-post-state reading, the two F01 `stateUnchanged` cells, and LD-S12-8 as applied to those cells. No passage override rewrites either parent.

The 28 provenance files match the accepted r1 tree byte for byte, including the 25-member manifest `d9fd0c628ccc9630a3bad15c04cc305f35cc6c6407ae62713c5fbc99e98fd560`, its proposal, evidence, context, `REVIEW.md`, and `review.json`. That review is ACCEPT-DESIGN-UNIT with empty requiredFindings. The pinned 98-row fixture is that same file, and both F01 `stateUnchanged` cells there remain `true` until this correction is bound.

Inventory v166 remains 614780 / `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`. This record adds no inventory candidate.

J3b stays halted. The two F01 cells may become false only after this bind. Every other original cell stays protected. Development checks and both exclusive two-target lead sets remain owed. The lead gives root assent, stages these accepted bytes, runs `verify_design`, and commits the architecture record and the product lock separately. Nothing is pushed.
