# Review: D4-2 inventory v232 r1

**Verdict: ACCEPT-UNIT**

This review is limited to the additive inventory successor. It does not reopen or extend the accepted D4-2 code review, and it does not qualify the product.

## Required findings

None.

## Inventory candidate assessment

The subject manifest is 683 bytes with SHA-256 `4c8bf623c07f150d3a388e7807065fe4e133c56bf823b8e0708dadae32dc1207`. All three members match their recorded byte counts and SHA-256 digests. The v231 parent at architecture commit `f43fb7713c8b44c7e1c1bd732a8004622a7ce043` is 760,618 bytes with SHA-256 `f93e6e821788f81dcefcffebeb715f18e096b154d16287c3e2d5ff44a78cfcd3`.

The v232 candidate is a sorted, unique strict superset of v231. It adds exactly these two rows, removes none, and changes no inherited row by value:

- `crates/host/src/component_admission.rs`: package `opensip-host`, role `composition`, `generated: false`. Its description is confined to the accepted trust-view adapter, three-pass projection, provider table, empty explicit-trust list, real judge, charge-before-work behavior, and disclosed absence of a production caller.
- `crates/host/src/component_admission_tests.rs`: package `opensip-host`, role `test`, `generated: false`. Its description is confined to the accepted D4-2 controls, including the child-parent, late-key, one-unit-short, and work-site controls.

Neither path existed as a v231 row, so no planned row was realized. The 20 package rows and nine pending decisions are unchanged. The same 91 planned but absent paths remain in both inventories, and `inheritedPlannedFilesRetained` lists that set exactly. Every one of the 1,270 paths tracked at integrated product commit `a7839a14aa755495592a4063657e78959be97f43` has a v232 row.

The eleven inherited rows changed by D4-2 retain exactly their v231 values. Their descriptions remain true at the accepted unit's recorded scope: the generic host manifest, lockfile, and module descriptions still apply; the security API, trust, authenticated-component bridge, ordinary-reader, fixture, root-payload, bootstrap-control, and fixture-gate descriptions are not contradicted or expanded into new authority claims.

## Integration and successor evidence

- Product main is clean at `a7839a14aa755495592a4063657e78959be97f43`. Its commit records exactly the two added paths above and the same eleven modified paths in `successor.json`.
- The accepted D4-2 review, subject manifest, and lead assent match the successor's exact byte and digest pins. The assent is `ACCEPTED-UNIT`, names the same two new paths and integrated product commit, carries no required findings, and expressly records no product qualification.
- The permitted operability source check reproduces 114 rows, no findings, and `passed: true`. Its checker and exceptions files match the census pins. The exceptions record contains 447 mint-audit rows. The accepted D4-2 closure evidence records 19 census-bound files and an empty intersection with the unit's changed paths. The inventory adds no census or mint-authority claim.
- `addedFiles`, `changedFiles`, `realizedPlannedFiles`, and `inheritedPlannedFilesRetained` are exact. The successor points its candidate to v232, not v231, and all parent, candidate, census, and accepted-unit pins match.
- The current product lock ends at inventory successor 191 with v231 and retains 177 contract successors, matching the declared parent state. Binding v232 as successor 192 remains a separate publication step.

## Non-blocking observations

None.
