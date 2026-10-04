**ACCEPT-UNIT — I1-a r1.** Its contract-successor assessment is **ACCEPT-DESIGN-UNIT**. No required findings in either assessment.

The exact product diff is 3,612,849 bytes, SHA-256 `fa7f4fda73b3eb213da91921ca868f3fa4feaf5e75c72f982704ebb849bd36c4`, on `5e25d04b3bfa85a244f5d958fe089e9626fd33fa`. The 26-member architecture subject is `3c89d7da193e25d5c8c6dcb8a5410b2d2be4fe0b6133402349e55b14e2fd7bcf`. The record is `docs/implementation/m3/preview-pack-i1/i1-a/successor.json`, 8,748 bytes, `7d6c04e9914809409e01027e63d7b9cde670c6e8757538a13b743b9d0af5a03d`.

The two schema source files equal I1-L's accepted copies byte for byte. The remaining edits are their source/admission/registry/closure/native pins, dependency-policy pins, mechanical regeneration, one schema-admission test and the staged binding. I found no I1-b1, I1-b2 or I1-c behavior added. The three Rust enums append the member with exact serde, Display and FromStr spellings. The two description comments, three TypeScript unions and provenance comments follow the selected sources. Only the two intended documents change in the 40-document TypeScript schema table, and those raw bytes equal the product sources.

The materialization map covers every changed product file except the expressly excluded staged lock. All 15 targets equal their architecture candidates; the two schema candidates remain owned by I1-L. All 62 request pins match. The record has 25 candidates and 12 selected accepted parents, with no candidate already selected and no passage override or supersession. The staged lock equals its base plus the one I1-a entry. Scratch verification passes with 87 → 88 contract successors, 95 inventory successors, v135, 100 inheritance rows and 21 supersessions unchanged. The admission registry is selected through both I1-a copies and the generator closure through its single copy.

| Judgment call | Answer |
|---|---|
| 1 — Inventory | **No inventory successor.** None of the 15 changed files needs a new row or meaning. Existing v135 owners, roles and descriptions remain accurate. A zero-addition successor is invalid. |
| 2 — Review split | **Yes: two review files.** `review.json` records ACCEPT-UNIT; `review-contract.json` supplies the top-level ACCEPT-DESIGN-UNIT required by the lock. This follows 458b and assesses one frozen subject. |
| 3 — Extra mechanical members | Accept the closure and both dependency-policy updates. They repair required byte consumers, and stale-policy controls refuse. The corrected widened-enum reference is Policy2AtomOp; Policy1AtomOp stays unchanged. |
| 4 — Schema authority | Accept the map's direct I1-L references. Both maps point at the same accepted byte strings; duplicate I1-a schema copies are unnecessary. |
| 5 — Fixture locator | **Keep `scannerIdentitySchema.fixturePath`; no replacement value is required.** It is a disclosed historical reference-fixture locator with no present Rust or Python tool consumer. Current source authority is carried by the exact pins and RegisteredSchemas. It does not prove that the historical fixture has the new bytes. |
| 6 — Interim policy admission | **Agree with the documented schema-first boundary.** The file-shaped pack form still fails the unchanged source-kind check; evaluation still refuses ATOM_OP. The broader symbol-shaped admission is documented, but an empty release registry/documents and unconditional Supplied refusal prevent a production AdmittedPack containing it. The next two units retain their admission-law and graph-semantics work. |
| 7 — Parents | Accept the 12 selected parents: available base copies plus I1-L's three schema authorities. Where no selected base copy exists, the exact product before/after pins and this unit review ground the new candidate; inventing a parent is unnecessary. |

The new host test demonstrates **token shape admission** through the real embedded RegisteredSchemas at the current Atom, program-predicate and proof-bundle selectors, plus the three generated enums. Existing members are positive controls; policy v1 and its enum are negative controls; all four near spellings are refused by the widened selectors and enums. It does not claim graph semantics or full policy-law acceptance.

| Independent rerun | Result |
|---|---|
| fmt, workspace all-targets build | Pass |
| Workspace, crash-matrix and scenario-fixtures clippy, −D warnings | All pass |
| Workspace all-targets tests, twice | Each: 1732 passed, 0 failed, 3 ignored, 20 binaries |
| Workspace doc tests | 18 passed |
| Crash-matrix feature test lane, no lead run set | 1630 passed, 0 failed, 3 ignored |
| Scratch design verification | Pass, staged mode |
| Real public generation via scratch overlay and separate regeneration replay | Each: 40 sources, 8 outputs, changed: [] |
| Plain verify_design and public generator on the staged lock | Expected refusal at SCRATCH-I1A/review.json |
| Package-edge lanes | Host and Rust provider pass; 14 checker tests pass |
| Dependency checks and suites | Both checks pass; 9 contracts-policy tests and 5 identity-policy tests pass |
| Both dependency checks with base policies | Expected stale-source refusal |

One nonblocking observation remains: **I1A-NB-1**, the historical scanner fixture locator described in judgment call 5. Keep it in this unit; do not cite it as verification of current fixture bytes. Align or relabel it when that reference metadata is next maintained.

Cargo used `--locked --offline`, a review-local target directory and copied Cargo cache. Native lanes ran serially with an owned 0700 Darwin user TMPDIR. Generator checks were clear before each invocation. The feature lane was initially deferred while another worktree ran cargo tests, then started only after its required process check was clear. The real OpenSIP home stayed absent. No private 413 fixture, crash-matrix lead run set, delegation, repository edit or commit was involved.

This is macOS arm64 development validation. The offline TypeScript lanes remain unavailable because esbuild 0.28.2 is absent, as the request discloses. Integration must replace the two synthetic pins with the actual contract review and root assent, then pass plain verify_design and public generation with changed: []. The scratch overlays do not constitute that integration or assent.

Evidence: [review.json](review.json), [review-contract.json](review-contract.json), [pin-audit.json](pin-audit.json), [semantic-audit.json](semantic-audit.json), [native-lanes.json](native-lanes.json) and [tool-lanes.json](tool-lanes.json).
