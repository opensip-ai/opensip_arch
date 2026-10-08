# O1-PKG-TOOLS r1 package-boundary tooling

**Verdict: ACCEPT-UNIT.** Required findings: none.

This unit accepts the two existing developer files that enforce the bound O1-PKG policy. Acceptance is a code commit of those files onto product `f9d37cceaf3b752cf386568b8499a33cc4bd6650`. It does not bind the product lock, author an inventory successor, or qualify O1-a. `productQualification` is false, `fullO1aComplete` is false, and `inventoryChanged` is false.

## Subject

`subject.json` is 404 bytes, sha256 `598731d52e3b41f420c679c7837d52a2d963a09442df74c97a26c0ca9c1fcd0c`. Its two paths are sorted and unique, and both match the candidate:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `tools/check_package_edges.py` | 13704 | `0c27e38c24e6747b5701d00a5c6ecefac2dbe28515c22cd6fddf87aa89c1ae4a` |
| `tools/tests/test_package_edges.py` | 19745 | `252959bf9a12f5a77a0ab5d75247c86a23a5fc286d44db05c0b8aa1c3323c66c` |

The candidate tree is the product snapshot `2fc3e4dd0b21d980ee64a4c5bb359b4d3cd2935a` plus these two files. Every other candidate file matches that snapshot, including `tools/verify_design.py` (43946 bytes) and `tools/tests/test_design_binding.py` (87065 bytes). Those helpers are unchanged on current main as well. The candidate `design-lock.json` is the pre-policy lock and is outside this subject.

On current main, the same two paths are still the `2fc3e4dd` bytes (`check_package_edges.py` 8274 / `95b373666abc9abe7acce9fff21a0a8a79e601352ef17bc2968b48e079216716`, `test_package_edges.py` 11366 / `277842807aaec80bf45834ae2e7f55c2069c4fe374e10401b17304c56ad1e609`). No commit between those bases edits them. The commit from `2fc3e4dd` to `f9d37cce` changes only `design-lock.json`.

## Bound authority

Product HEAD `f9d37cceaf3b752cf386568b8499a33cc4bd6650` and architecture HEAD `ec32440475ec9cafef0afb6dc9eef45121472db3` are the named bases. The lock remains schemaVersion 4 with the same root fields. It has 127 inventory successors and 137 contract successors. The selected inventory tail is still `repository-file-inventory.v167.json`, 618550 bytes, sha256 `718cde32c35771b11527e45715a662c0850228d82b7bf611bfca541553bbbf2b`.

Contract 137 is O1-PKG r1:

- record `o1-package-policy-r1/successor.json`, 4405 bytes, sha256 `5f821758a5508119243282582d62d672361e4e0591c9718b41cdbacbfe758886`
- subject `o1-package-policy-r1-subject.json`, 682 bytes, sha256 `1dbf58ce82cc5245cb68e3471da2e29fb7ecc918893da73078be7df46be3519a`
- review `reviews/grok-o1-package-policy-r1/review.json`, 281 bytes, sha256 `bd7978994d5476e993d3b2d0b0e222ecbe45d510cae650baccd9637738c22bc5`, verdict `ACCEPT-DESIGN-UNIT`, required findings empty
- assent `o1-package-policy-r1-unit.json`, 1816 bytes, sha256 `fb47fa2f1243a3b9f68bd1e917d4e3c7be18083430079b4c775a67c7620c4b50`, status `ACCEPTED-DESIGN-UNIT`

The record parents are v167 and then `PROPOSAL-r2.md` (80638 / `987153221b913fc1c4cc729ecfabad397670502c8dc95a4bb292ebe0506bbbf0`). The selected candidate `package-policy.json` is 7741 bytes, sha256 `0961c2fd544f1288c72f1a0eda2dd581df85d10f3cb45e902503b1a754af8463`. Its `baseInventory` and `authority` are those two parent pins. The tool constants `OPERABILITY_ROW` and `OPERABILITY_EDGES` equal `packageAddition`, the final effective row, and `dependencyAdditions`: one `opensip-operability` library at `crates/operability` depending only on `opensip-platform`, plus the three appended edges from components, host, and storage, in that order.

## Checker

`BoundaryError`, `require`, `explicit`, `manifest_internal_edges`, and `check` are unchanged. Without `--package-policy`, `--architecture`, and `--lock`, `main` still parses the supplied inventory and calls that same `check`. Setting any one of the three calls `authenticated_package_policy`, which refuses a missing member of the group.

That function resolves the architecture, loads the sibling `verify_design.py`, and calls `verify` on the supplied lock before it trusts policy bytes. `DesignError` remains a `ValueError`, so a failed chain exits through the existing refusal path. It then requires the policy path to lie inside the architecture and to be exactly one contract-candidate input. The file length and SHA-256 must equal that input pin. The successor path in the verify result is re-read, its SHA-256 must equal the result's record digest, and `parents` must equal `[baseInventory, authority]` in that order. Both parent files are read back and checked against those pins. The base inventory is the parent used for derivation. The caller-supplied inventory path must be the lock's current `selectedInventory` file, with equal length and digest.

`derive_package_policy` accepts only the bound policy's field set, schemaVersion 1, profile `opensip.o1a-package-admission.v1`, `rawInventoryPackagesMustRemainEqual` true, and `runtimeOrComponentAuthorityGranted` false. Current `packages` and `pendingDecisions` must equal the base by value. `packageAddition` and `dependencyAdditions` must equal the fixed row and the three edges. Derivation deep-copies the base rows, appends `opensip-operability` to those three dependency lists, appends the one new row, and requires `effectivePackages` to equal that result. The object passed to `check` keeps the current inventory's other fields and replaces `packages` with those derived rows. `check` still returns `productQualification` false.

A later additive inventory can pass once it is the lock's selected tail and its packages and pending decisions still equal v167. A stale path, a raw package or pending-decision change, an unselected or rewritten policy, a broken chain, or a record whose parents are not the policy pins refuses. Extra fields, a weakened flag, another profile, security, platform, or CLI edges, a reordered edge or row, and a changed new-package kind, path, or dependency fail the fixed derivation. `verify_design.py` is not edited. No root lock field is added.

## Controls and boundary evidence

`test_package_edges.py` keeps the previous boundary cases and adds `EffectivePackagePolicyTests`. The file contains 20 test methods. The supplied `test.log` reports 20 tests OK in 0.586s, with no skips. The two real Cargo cases use disposable lockfiles and `cargo metadata --locked --offline --format-version 1` on the fixture workspace. The policy class builds a miniature schemaVersion 4 lock through the unchanged `Fx` helper: one additive inventory hop and two four-pin contracts, then calls `authenticated_package_policy`, which calls `verify`. Those tests cover a later file-only inventory, a stale inventory path, an unselected policy path, rewritten policy bytes, a contract binding with its review removed, a record whose parent list is not the policy's two pins, each missing authentication argument, and the derivation expansions above. This review did not rerun Cargo.

`o1a-metadata.json` is 261487 bytes, Cargo metadata version 1, from the separate tree `/tmp/opensip-implementation/o1a-code-preparation-v167-contract135-whole-unit-controls-r3/product`. `opensip-operability` has one dependency, a normal path dependency on `opensip-platform`. Its features `operability-dev-sinks` and `test-mints` add no dependency. `opensip-host` has a normal path dependency on `opensip-operability`. Storage, components, security, platform, and CLI do not. `o1a-boundary.stdout` is a host-lane pass with `productQualification` false and `sourcePurityQualified` false. Its declared and resolved internal edges match that graph, including host to operability and operability to platform. `o1a-boundary.stderr` is empty. v167 does not name `opensip-operability`, so this pass is the effective-policy result. It does not accept the O1-a tree.
