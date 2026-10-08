# O1-PKG r1 effective package policy

**Verdict: ACCEPT-DESIGN-UNIT.** Required findings: none.

This unit selects a separate effective package policy. Raw inventory packages and pending decisions stay unchanged. The policy adds one package row and permits three dependency edges. It grants no O1-a integration, no tooling acceptance, no runtime or component authority, and no product qualification. The earlier advisory package-policy assessment remains a historical recommendation. It is not this acceptance.

## Subject

Frozen stage: `/tmp/opensip-implementation/o1-package-policy-r1/architecture`.

`docs/implementation/m3/operability/o1-package-policy-r1-subject.json` is 682 bytes, sha256 `1dbf58ce82cc5245cb68e3471da2e29fb7ecc918893da73078be7df46be3519a`. It lists three members. The paths are sorted and unique, and every stage pin matches:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m3/operability/o1-package-policy-r1/CONTRACT.md` | 4005 | `c4e76de24dc7e192087cc4c1fe1a097c10f982fd55c2aa23753eefb0bd8f4c66` |
| `docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json` | 7741 | `0961c2fd544f1288c72f1a0eda2dd581df85d10f3cb45e902503b1a754af8463` |
| `docs/implementation/m3/operability/o1-package-policy-r1/successor.json` | 4405 | `5f821758a5508119243282582d62d672361e4e0591c9718b41cdbacbfe758886` |

These three paths are absent from architecture HEAD `8d54d3a44efc5ce23efb1eda394054f42a12d186`. That is the expected state before this unit is bound. Prepared product base `2fc3e4dd0b21d980ee64a4c5bb359b4d3cd2935a` is product HEAD, and the prepared architecture base is architecture HEAD.

## Parents and the eligible-parent finding

The record's candidates are `CONTRACT.md` and `package-policy.json`, in that order, with the same pins as the subject. The record itself stays in the subject and out of the candidate list. The parent paths are sorted, and neither parent is a subject member.

The two parents are:

- `docs/implementation/m2/repository-file-inventory.v167.json`, 618550 bytes, sha256 `718cde32c35771b11527e45715a662c0850228d82b7bf611bfca541553bbbf2b`
- `docs/implementation/m3/operability/o1/PROPOSAL-r2.md`, 80638 bytes, sha256 `987153221b913fc1c4cc729ecfabad397670502c8dc95a4bb292ebe0506bbbf0`

Both architecture HEAD blobs match those pins. Product HEAD `design-lock.json` is still schemaVersion 4, with the same root fields `schemaVersion`, `architectureRepository`, `approvals`, `inputs`, `inventorySuccessors`, `contractSuccessors`, and `inventoryPassageInheritance`. It has 127 inventory successors and 136 contract successors. The inventory tail candidate is the v167 pin above. v167 is the candidate of the v166 successor. It is an accepted inventory path.

The last contract successor is the bound O1-L-P r1 selection:

- record `o1-law-selection-r1/successor.json`, 2218 bytes, sha256 `5d0d9034d06b2917c45064a45fb009ef4f7729000fe8452b379f8a8afb0048f4`
- subject `o1-law-selection-r1-subject.json`, 866 bytes, sha256 `aea7f6c0d6ea5ce3de9c066ea3c696023e84fb73eeefd9ba011775280d7ab641`
- review `reviews/grok-o1-law-selection-r1/review.json`, 249 bytes, sha256 `4b7aa53caca843430451d20557a50cbb4fb6e23867dcb1245dac53112708225c`
- assent `o1-law-selection-r1-unit.json`, 1500 bytes, sha256 `81ea4e523db4d77cc72751b0ab4a33e684e0b44590e8dfd5a92709c25451a5c2`

That review is `ACCEPT-DESIGN-UNIT` with empty required findings and the same subject digest. The assent status is `ACCEPTED-DESIGN-UNIT`, with root substantive assent and no unit findings. Its candidate list contains `PROPOSAL-r2.md` at the parent pin above. Its passage overrides are empty. The product commit that bound it changes only `design-lock.json`. The architecture commit adds only the law-selection files. `tools/verify_design.py`, `tools/check_package_edges.py`, and `tools/tests/test_package_edges.py` are unchanged from `28fbdec` to this product base.

`PROPOSAL-r2.md` is therefore an accepted contract candidate from that earlier four-pin unit. This successor parents that already selected path. It does not introduce the path in the same unit that overrides it, and it does not treat the citation inside `o1-definitions-r2/source.json` as selection. That closes advisory RF-O1A-PKG-01 for this successor. `package-policy.json` names the same two pins as `baseInventory` and `authority`.

## Passage overrides

`passageOverrides` contains three entries. `passageSupersessions` is an empty list. Each override parents the `PROPOSAL-r2.md` pin, and each selector is a single line. The parent is markdown: JSON decoding raises `JSONDecodeError`, so the current v4 checker keeps the reviewed line selectors. No earlier contract record overrides this parent or lines 130, 149, or 558.

The verifier compares `before` with `splitlines()` of the parent. All three match the architecture bytes, and each `after` differs from its `before`:

| Line | Role |
| --- | --- |
| 130 | The package row and the three permissions move from an O1-a inventory-package edit to the selected O1-PKG policy. Raw packages and pending decisions stay unchanged. |
| 149 | The binding edge list is the current selected inventory plus this policy, after full lock and pin verification. The O1-a file inventory stays additive. |
| 558 | O1-C1 still forbids unsafe code, keeps manifest edges at exactly `{opensip-platform}`, has host declare the edge, and leaves storage and components permitted. The checker runs on the raw inventory plus this accepted policy. |

Lines 123, 152, and the rest of O1 r2 stay in the parent bytes. O1-D1 definitions, O1-p, and the accepted S-OP-2 drafts are outside this subject.

## Effective rows

v167 has 20 package rows. `effectivePackages` has those same rows, in the same order, plus one final row. The only inherited changes are appended dependencies:

- `opensip-storage` appends `opensip-operability`
- `opensip-components` appends `opensip-operability`
- `opensip-host` appends `opensip-operability`

Every other field of those three rows is unchanged. `opensip-cli`, `opensip-platform`, `opensip-security`, and `opensip-lifecycle` are unchanged. `dependencyAdditions` is exactly those three pairs, sorted by source. `packageAddition` equals the final row: id `opensip-operability`, path `crates/operability`, kind `rust-library`, dependencies `[opensip-platform]`, standing `proposed`, purpose `Safe operational records: the event registry, typed fields, sinks and loss accounting`. That purpose is the X-O2 package text at O1 r2 line 601. Rebuilding the 20 rows by those three appends and then appending that row equals `effectivePackages`.

v167 `pendingDecisions` remains nine unrelated strings. The policy artifact does not carry a replacement list. The contract requires a later checker to prove the supplied inventory's packages and pending decisions equal this pinned base by value.

## Checker shape this design requires

Current `check_package_edges.py` reads `inventory['packages']` and checks declared, development, build, optional, target, and resolved internal edges against those dependency lists. It has no `--package-policy` option. `inventory_successor` still refuses a package or pending-decision change. This subject does not edit either tool.

`CONTRACT.md` keeps that profile. A later tooling unit must extend `check_package_edges.py` and `tools/tests/test_package_edges.py`. `--package-policy`, `--architecture`, and `--lock` are optional only as a group. Absent that group, the raw-inventory check remains. Present, the checker validates the complete lock with `verify_design.verify` before trusting policy bytes. `verify` authenticates pins and returns each contract's selected record, record digest, and candidate inputs. It does not echo parent pins, so the tooling unit has to load the authenticated successor record and prove `baseInventory` and `authority` are that record's exact parents, then check both parent byte pins.

The supplied raw inventory must be the lock's current `selectedInventory`. Its packages and pending decisions must equal the policy base by value, so a later additive file inventory can use this policy while a raw package change refuses it. The checker derives the fixed one-row, three-edge result itself and requires equality with `effectivePackages`. Caller-supplied paths or policy-shaped JSON do not admit the boundary. Negative controls named for that same path cover missing inputs, unselected or changed policy bytes, wrong profile or parents, stale inventory, modified raw packages or pending decisions, extra or reordered rows or edges, security, platform, or CLI additions, a changed new-package kind, path, or platform-only dependency, and extra feature or external permissions. Locked offline Cargo metadata against the O1-a candidate is a post-tooling check. None of that tooling or O1-a code is accepted here.

## What remains owed

Design assent and the lock bind of this unit come next. Tooling acceptance and its code commit are separate. O1-a whole-unit acceptance, its additive file inventory, and that inventory's lock bind come after the checker exists. S-OP-2-P, S-OP-2-R, and S-OP-2b stay after O1-a. Timing qualification stays at M6. `productQualification` is false, `inventoryChanged` is false, `fullO1aComplete` is false, and `productCodeUnchanged` is true.
