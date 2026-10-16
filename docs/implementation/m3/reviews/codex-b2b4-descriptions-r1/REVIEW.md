# B2-B4-DESCRIPTIONS-r1 review

Verdict: **ACCEPT-DESIGN-UNIT**

Required findings: none. Non-blocking observations: none.

## Exact subject

Independently checked the 492-byte subject manifest, SHA-256 `4c480ecf55e790542657645c1824aab3dddc44e639b62536252ccc24ba0cfe03`, and both member pins:

- `b2-b4-descriptions/README.md`: 1699 bytes, `7fa7bb6ac5229065f9f0cc2650625d1e9140cf7cb8a0af8ef5b90205738a192a`.
- `b2-b4-descriptions/successor.json`: 5201 bytes, `ce2a7f7ca44b99e547f19668909c8b013fe3a6e537ed87a95efbe24f4ae2ea33`.

The sole parent is the accepted v199 candidate: 687868 bytes, SHA-256 `239f95f58513c0d8573c7b837ba460acee1099fc3bf329124f70460d63eadb90`. Its bytes and prior ACCEPT-UNIT review agree. Product main is clean at `ab0eb2c970ea23bd9eb53aac2ec93ccd5b665731`.

## Description accuracy and scope

All three before texts exactly equal the parent descriptions at their JSON Pointers, and the pointers select the README's named files:

| Pointer | File |
| --- | --- |
| `/files/547/description` | `crates/security/src/custody/discovery_census.json` |
| `/files/548/description` | `crates/security/src/custody/discovery_census_tests.rs` |
| `/files/1180/description` | `tools/security/discovery_census.py` |

Read the three product files. The new descriptions correctly cover the byte model, root-length margins, recorded caps, workspace accounting, size-inventory and cost-closure binding, and blind receipt production/composition supported by the accepted units. They describe held-out capabilities and possible states without asserting that a real held-out run occurred. The committed census still reports held-out margins outstanding; the census description expressly preserves design-evidence rather than qualification standing.

Applying the three overrides to an in-memory copy of the parent changes exactly those three description strings. All other row fields, row order, 1255-row count, packages and pending decisions remain equal. No product, schema or law change is introduced.

## Successor mechanism

Rehashed and inspected all 164 existing contract records and checked all 103 inventory-passage-inheritance entries. Resolved inventory selectors to row paths when checking prior overrides and supersessions. None previously restates any of these three rows. These are first passage restatements, so plain passage overrides against v199 are appropriate; a supersession is unnecessary.

Compared the proposed record with the contract-successor rules in `tools/verify_design.py`, without executing it. The record declares the exact v199 parent; its candidates cover precisely the subject members other than the record itself; both member paths are new in architecture HEAD. Each override has the required fields, references the declared parent, uses a unique parent/selector pair, and supplies an exact before text and changed, nonempty after text. With 164 existing contracts, this is suitable for contract successor 165 once v199 is selected in the same lock update.

Acceptance covers the frozen design subject. Lead assent, publication, binding v199 and contract successor 165 in one lock commit, and fresh verification remain the lead's subsequent steps. This review does not claim that those steps have occurred or grant product qualification.

## Review boundaries

Used only read-only file inspection, hashing, JSON parsing and Git queries, plus the two requested review outputs. Did not run the compiler, Cargo, tests, the lane or `verify_design`; did not access the network, private fixture, installation directory, signing keys or held-out stores/overlays. Neither repository, stage nor control files were edited. No delegation or other panes were used.
