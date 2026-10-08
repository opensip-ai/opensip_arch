# O1-L-P r1 existing-law parent selection

**Verdict: ACCEPT-DESIGN-UNIT.** Required findings: none.

This unit selects the unchanged O1 r2 bytes at `docs/implementation/m3/operability/o1/PROPOSAL-r2.md` as a contract candidate. The parent is the already selected O1-D1 r2 source receipt. The selection supplies the eligible-parent prerequisite of advisory RF-O1A-PKG-01. It leaves the law text, inventory, and package policy unchanged. Selection admits that path for a later unit. It grants no O1-a code integration and no package permission.

## Subject

Frozen stage: `/tmp/opensip-implementation/o1-law-selection-r1/architecture`.

`docs/implementation/m3/operability/o1-law-selection-r1-subject.json` is 866 bytes, sha256 `aea7f6c0d6ea5ce3de9c066ea3c696023e84fb73eeefd9ba011775280d7ab641`. It lists four members. The paths are sorted and unique, and every stage pin matches:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m3/operability/o1-law-selection-r1/README.md` | 1240 | `162d01d0d3192e8b5ec228533d8aaa6a9e282e74685138313e38cf716ae85298` |
| `docs/implementation/m3/operability/o1-law-selection-r1/selection-proof.json` | 1571 | `e884f7f2a0a42b4b7023adb2e5037c99703ea324f9a5898647a05bec2b12cca0` |
| `docs/implementation/m3/operability/o1-law-selection-r1/successor.json` | 2218 | `5d0d9034d06b2917c45064a45fb009ef4f7729000fe8452b379f8a8afb0048f4` |
| `docs/implementation/m3/operability/o1/PROPOSAL-r2.md` | 80638 | `987153221b913fc1c4cc729ecfabad397670502c8dc95a4bb292ebe0506bbbf0` |

Architecture HEAD `eb940b99eaca370301a626bcf998f97e5199d5c4` holds the same `PROPOSAL-r2.md` bytes. The README, selection proof, and successor are stage files and are absent from that HEAD, which is the expected state before this unit is bound.

## Record, candidates, and parent

The record is `docs/implementation/m3/operability/o1-law-selection-r1/successor.json`. Its three candidates are the other subject members, in sorted path order, with the same byte counts and digests. There is one parent:

`docs/implementation/m3/operability/o1-definitions-r2/source.json`, 2776 bytes, sha256 `a5ea85fd8a8a9375e2e85195a46e3553da06927f2dbb02bf310eac8986f2cf09`.

That parent path is outside the subject, so the parent bytes stay in place. `passageOverrides` is empty. The record has no `passageSupersessions` field. The parent pin uses `path`, `bytes`, and `sha256`.

`selection.sourceReceipt` equals that parent pin. `selection.sourcePointer` is `/authorities/2`. `selection.selectedArtifact` equals the `PROPOSAL-r2.md` candidate. The selection proof repeats the same law pin, parent pin, pointer, and earlier-review pin.

## Why this parent is eligible

Product HEAD `28fbdec37a42c9a32efebce6fa9b5aa58fa5c806` binds O1-D1 r2 as the last contract successor in `design-lock.json`:

- record `docs/implementation/m3/operability/o1-definitions-r2/successor.json`, 12771 bytes, sha256 `caccf73411972b7b583c18669e36e338a082ceaa9f6e1452679789a484d7f060`
- subject manifest `o1-definitions-r2-subject.json`, 9846 bytes, sha256 `639780d5c69300c695aba0e3476e28f92f91121cb1ff6e5f8072b1c6a19c2bb7`
- review `docs/implementation/m3/reviews/grok-o1-definitions-r2/review.json`, 497 bytes, sha256 `4f903475a6e5c30c79a7034cbb5f881d7be213a38ef7da9d78eb943faf7e5f28`
- assent `o1-definitions-r2-unit.json`, 2826 bytes, sha256 `c748ed51a6760a8c20640d4f737fa4c7de161b5ac574784de752ca2772187704`

The architecture blob of that successor matches the lock pin, and its candidate list contains `source.json` at the parent pin above. The architecture blob of `source.json` matches the parent pin and the evidence receipt. Its `authorities` index 2 is the `PROPOSAL-r2.md` pin. The lock text contains neither the string `PROPOSAL-r2.md` nor the `source.json` path. The receipt is selected because it is a candidate of the bound successor. The law path is only a citation inside that receipt until this unit lists it as its own candidate.

That is a sound v4 contract shape: one already selected parent, a new path admitted as a candidate, empty passage overrides, and no supersession. Extra record fields (`standing`, `scope`, `selection`, `acceptanceDoesNotQualifyProduct`) carry the unit's stated limits. They do not add a passage, an inventory row, or a package edge.

## Historical review alias

`docs/implementation/m3/reviews/codex-o1-law-r2/review.json` is 5866 bytes, sha256 `a7bd0067b6b49b312ec5feab1b2e30ace3ca7320d1b0cede642c6e6f3f94ad0c`. Architecture HEAD and the evidence copy match that pin. The review verdict is `ACCEPT`. Its subject path is `docs/implementation/m3/operability/o1/PROPOSAL.md`, 80638 bytes, subject sha256 `987153221b913fc1c4cc729ecfabad397670502c8dc95a4bb292ebe0506bbbf0`.

That digest is the `PROPOSAL-r2.md` pin. `historicalPathAliasBytesEqualBySha256` records this hash identity between the historical review subject and `PROPOSAL-r2.md`. The Codex `ACCEPT` remains law-text context for those bytes. It is context for this unit, and it is law-text acceptance of that historical subject. It is not an acceptance of O1-a code.

The file now at `docs/implementation/m3/operability/o1/PROPOSAL.md` on architecture HEAD is 80922 bytes, sha256 `6267e40b90a28e190330f34d6958910ed4450a83496fa1a1caec8e484798e5fa`. Its third line points at `PROPOSAL-r2.md` for the reviewed bytes. This front door is outside the subject. The selected artifact is `PROPOSAL-r2.md`.

## Scope that stays closed

The four subject paths are the README, the selection proof, the successor, and `PROPOSAL-r2.md`. No S-OP draft and no O1-p file is a member. `packagePolicyAdopted` is false. `inventoryUnchanged` is 167. `runtimeOrComponentAuthorityGranted` is false. `productQualification` is false, `inventoryChanged` is false, and `fullO1aComplete` is false. The law file is 673 lines, so raw lines 130, 149, and 558 exist in the selected bytes. This successor does not override them.

## What remains owed

After this unit is bound, a later exact policy unit can parent this `PROPOSAL-r2.md` path together with inventory v167 and use `passageOverrides` on raw lines 130, 149, and 558. That policy unit is still owed. Separate checker-code acceptance is still owed. Neither follows from this selection.
