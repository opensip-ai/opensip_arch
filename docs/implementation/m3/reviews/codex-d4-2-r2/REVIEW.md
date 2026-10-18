# Review: D4-2 r2

**Verdict: ACCEPT-UNIT**

The frozen subject manifest has the requested SHA-256 (`2de6b8d35db9452502bfe232b219255107fc00619fa0e271c81c7f9ad1215eee`). All 130 listed members match their recorded sizes and digests, and every declared source authority and stacked-unit pin matches architecture base `1f529ac9c7a0f78ccbc902d5963cf380a40f4ce7`.

## Required findings

None.

## Resolution of D4-2-R1-RF-1

The corrected lookup charge is conservative for the pinned Rust 1.95 implementation. The pinned `alloc/src/collections/btree/search.rs` is 10,822 bytes with SHA-256 `687b99a6f5f146591738c8039371499d5c5ca9adfdb47b9519694aba62387021`. Its lookup visits one root-to-leaf path, and each visited node scans keys with one ordering comparison per tested key. Because those nodes are visited once and contain disjoint subsets of the map's `m` keys, the lookup performs at most `m` key comparisons. `member` now charges `max(m, 1)` edges before its sole `BTreeMap::get`, retaining a conservative one-edge charge for an empty map.

The new control uses the real nine-key release-row shape and covers `publisher`, `sourceClass`, and the final key `version`. A nine-edge allowance succeeds and records nine charged edges; an eight-edge allowance refuses at the charge, records no partial charge, and latches the ledger before the source-ordered `get`. The `lookup-underpriced` mutation restores the former five-edge sorted-slice price and is caught by runtime test failures. The independent `lookup-uncharged` control also remains caught. This resolves the prior underpricing finding without changing D4-1's separate sorted-slice policy.

## Verified evidence

- The product map contains exactly 13 paths and exactly the two declared new paths. Every parent pin matches product base `4e475c753002d21ed99e0d53e64218e55af0cb1f`; every current candidate file matches its candidate pin and archived copy. The worktree has no changed or untracked path outside the map. The product lock at the declared base has the recorded 709,024 bytes and SHA-256 `230fcd25449e5c5a84675bf9d62a6b9ebb7429a222e67929a17dddb41bee8a0d`; accepted D4-1 and CI-2 precede that base.
- The complete R1 subject and review are preserved byte-for-byte. Relative to R1, only `crates/host/src/component_admission.rs` and `crates/host/src/component_admission_tests.rs` changed; the other 11 product members are identical.
- Reuse is confined to evidence whose inputs did not change. The base remains the exact R1 product base, the security source closure is unchanged, and the reused base host, base security, and candidate security logs are byte-identical to the archived R1 logs. The candidate host suite is fresh. Security records 1,281 base and 1,283 candidate passes with the same 14 inherited failures; host records 418 base and 428 candidate passes with the same nine inherited failures. No fresh whole-suite pass is claimed.
- Every required lane row records success. The focused D4-2 tests pass, and all 14 mutations produce runtime test failures with no compile-failure credit. The new underpricing mutation is among them. The earlier generic typed-allocation survivor is covered by the broadened source guard, and the child-parent control exercises validated fixture data through the admission view and real judge and catches `parent-dropped`.
- The trust owner retains and lends the reader's reserved set and authenticated release association. The host adapter borrows that view, performs the three-pass projection, uses the exact nine-member provider projection and empty explicit-trust set, and invokes the integrated excluded-form judge with charge-before-work behavior. Fixture gates, package edges, invariants, and disclosures remain represented in the frozen subject.
- The unit remains library-only with no production caller or production wiring. The scope discloses the later wiring and record work and the separate inventory successor required for the two new paths. This verdict does not qualify the product or close full D4.

## Non-blocking observations

None.
