# B2-C0-REFERENCE-r2 review

Verdict: **ACCEPT-DESIGN-UNIT**

Required findings: none. Non-blocking observations: none. B2C0REF-R1-RF-1 is resolved.

## Exact subject

Rehashed the 1131-byte subject manifest, SHA-256 `1587cde697f4ff4c24eca21ad0f333e98fd4010fd11b1bfdf2d2b342cbb8210e`, and all five members; every pin matches. The successor record is 4895 bytes, SHA-256 `c84c7a25bf6c384c53ceff84568eec28b03c42b628bcf7708bfc6f08af86bc5d`.

Confirmed clean product main `c0e61a4b9ad48467430af8a5cfbe53ed7e6111c5` and architecture HEAD `7c55cdab1bd1c24144e2222496296e10a54dde34`. Reviewed the changes from round 1 against the prior finding and selected authorities.

## Round-1 resolution

Both new semantic checks use the same `_admitted_boundary` predicate. It first applies nested repository/project classification, then the selected custody classifier with no marker name. Directory-custody and DEPTH exclusions therefore cover descendants, while marker-custody does not become a directory boundary. The derivation filter now tests the returned pruned anchor's own path, rather than the marker path.

Independently repeated the prior synthetic reproductions for DIRECTORY_CUSTODY:ACL_UNREADABLE and DEPTH. Derived anchors below the excluded directory and carried .git anchors there now admit; membership still classifies a file below that directory as outside-project-boundary. A missing node_modules anchor outside the directory still refuses. Additional probes confirmed that marker-only custody leaves an unrelated co-located Cargo unit available, and that a pruned anchor outside a boundary is not wrongly withheld merely because its descendant marker lies below the boundary.

The checker adds both directory-exclusion variants, marker-custody controls and the sixth mutation that removes custody/depth classification. These directly cover the previous omission without weakening outside-boundary comparisons.

## Reference and semantic scope

The selected model bytes and pinned loading closure are unchanged. Its __file__ placement supplies the intended historical sibling layout; historical and current executions use separate modules. The current substitutions remain limited to the bound shared rule, V3 inventory admission, deferral of the historical V2 discovery-output check in favor of V3 validation, and memberRepositories output. B-S1 definitions are added without replacing base definitions.

Successful current results validate as UnitDiscoveryV3, including PrunedTreeV3/SX-1 and UnitBoundariesV2. Members remain ordinary directories; member roots are supplied to the shared rule for custody-state pruning. The consistency check covers carried/derived vcs-tree anchors and exempts every admitted directory boundary. Current V2 admission is refused; historical replay remains separate. No additional unsupported behavioral change was found in the reviewed entry points.

LD-B2C0-1 resolves a real composition conflict: security's current walker does not enter nested boundaries, so its inventory cannot reproduce pruned anchors inferred solely from markers inside them. The revised filter exempts those anchors from derivation comparison while retaining membership exclusion and the outside-boundary subset check. The changed historical case keeps its schema-invalid source control and adds an outside-boundary variant that preserves the inventory-mismatch purpose. The other six explained differences are SX-1 scope-prefix additions.

## Independent checker run

Ran only the expressly permitted staged checker, directing its output to this directory's review.json before replacing it with the final review. Its parsed output equals the staged checks.json exactly:

- 26 historical and 26 current cases pass, with seven explained differences.
- All seven member/boundary-control rows pass, including both custody/depth regressions and marker-only custody.
- The current P3 join sweep passes with B2-b0 on the security side, including both crossings and the outside-boundary missing-anchor control.
- All six mutations are caught.

Additional synthetic probes used only the permitted read-only module import and in-memory inputs. No actual source tree or held-out corpus entry was used as a fixture. The checker and probes are sufficient for this design reference; they do not qualify a product implementation.

## Binding

All 13 parent pins match accepted base or selected contract-candidate pins, reconstructed from the accepted application/source manifests and current contract chain. Parents are sorted. The four candidate pins cover exactly the reviewed subject minus its successor record. The sole override names a declared parent and its before text equals NE line 838 exactly; no earlier exact-selector override or supersession occurs in the 165-contract chain.

A passage override is appropriate for this narrow current meaning, preserving immutable parent bytes. The record fits the contract-successor shape for ordinal 166. The supplied scratch summary reports base and synthetic-successor verification passing and identifies this exact subject/record. That support is structural evidence using synthetic acceptance/assent, not actual publication; the reviewer did not execute verify_design.

Lead assent, architecture publication and the separate product lock binding remain subsequent steps. No product code changes or qualification are granted by this acceptance.

## Boundaries

Final outputs are only REVIEW.md and review.json in the requested directory. Neither repository, stage nor control files were edited. No Cargo, builds, lane, network, other panes or delegation were used; execution was limited to the expressly permitted checker and synthetic module probes. No private fixture, installation directory, signing keys, held trees or T2 held-out entry was accessed.
