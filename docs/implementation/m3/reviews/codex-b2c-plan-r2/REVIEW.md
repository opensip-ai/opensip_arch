# B2C-PLAN-r2 review

Verdict: **ACCEPT**

Required findings: none. Non-blocking observations: none. Both round-1 required findings and both observations are addressed at plan scope.

## Exact subject and bases

Rehashed subject.json: 449 bytes, SHA-256 `e9f94322d9c1f8c59cc94f58734b981ad374512b63a4e3e78fca5ea5d2c72a42`. Its sole member, `docs/implementation/m3/config-discovery-b/b2-c/PLAN-r2.md`, is 19985 bytes, SHA-256 `126252206c7c971c482b74dc3fa507726319b23b1be2c4d54cecc1f6ef0af1a3`; the manifest pin matches.

Confirmed clean product main `c0e61a4b9ad48467430af8a5cfbe53ed7e6111c5` and architecture HEAD `ecd3c5a52a2faa10c91ac1ef96b62cde5a8152a0`. Inventory is v200; there are 165 contract successors. Rechecked selected contract 81/163/164 record, subject, review and assent pins against actual bytes. Read the earlier review and revised plan, and compared the revisions with the selected registry, B-S1 V3 schemas/passages, native model, NE/M3-B rules and current product sources.

## Earlier-round resolutions

**RF-1 resolved.** Section 2.3 withdraws the vocabulary gap and public enum additions. Its four alias pairs exactly match the registry:

| Internal key | Public detail |
| --- | --- |
| native.explicit-root-grammar | PROJECT.EXPLICIT_PATH_INVALID |
| native.explicit-root-crosses-boundary | PROJECT.EXPLICIT_PATH_INVALID |
| native.boundary-inventory-mismatch | PROJECT.DISCOVERY_INVENTORY_MISMATCH |
| native.too-many-units | PROJECT.WORKSPACE_UNIT_LIMIT |

The stated CONFIG.INVALID, REQUEST.PRECONDITION_FAILED and REQUEST.UNSATISFIABLE classes agree with the owning routes. All public targets already exist in product vocabulary. The public `native.explicit-root-without-marker` passes unchanged. The planned closed, registry-pinned map and per-route controls preserve internal decisions without publishing their spellings. B2-c0 is now design only, and the sequence no longer depends on an unauthorized vocabulary expansion.

**RF-2 resolved.** Both wrapper and product now emit UnitDiscoveryV3, with PrunedTreeV3 and UnitBoundariesV2.memberRepositories. The plan explicitly preserves SX-1 at the project/member roots, carries admitted members, excludes no member merely for being a member, checks nested vcs-tree parent membership, and preserves explicit-root/U-9 behavior. It adds the three requested current vectors and keeps historical V1/V2 replay separate. This consumes B3-b's future admitted inputs without implementing its readers or admission.

**NBO-1 addressed.** The plan correctly identifies the subset algorithm as already present and the equality wording as stale commentary. The wrapper supplies and pins the complete model loading closure while preserving accepted model bytes. A wrapper remains needed for the relocated dependencies, selected rule and V3 admission/output adaptation. Exact implementation and complete replay remain B2-c0 review obligations.

**NBO-2 addressed.** The proposal specifies path/package candidate order and name/subpath forms, excludes exports and package.json tsconfig-field evaluation, and drops partial-settlement disclosure. Every unresolved edge now refuses; there is no invented unresolvedChoices field in the closed discovery output. This is an explicit change from r1's recommendation and remains a proposal for separately reviewed r8, not a current-law change.

## Scope, design and sequencing

The plan covers item 14's instrument obligations: root admission, modes, workspace folding, exact membership, shared pruning, ordering/digests, caps, boundary agreement, fallback, Config2 roots, scope descriptor, default selection and the JSONC/effective-allowJs function shared with C2. U-5/U-6 host joining remains with H/J; B supplies the records. C1 snapshot custody/inventory, J1 production callers, B2-d recognition/YAML and B3-b reader/member admission remain outside this unit.

The shared security rule is currently crate-private; a narrow typed public surface is an explicit API addition and avoids copying it. The pinned identity TOML dependency supports the recommended pure identity helper. V3 is the operational boundary type; the standalone no-inventory lane is limited to fixtures. FW-01 already names discovery.rs as planned coverage, so the proposed structural pin and planted negatives fit the current check. The 26 units-* cases, cap/scope sweeps, generated/order mutations and scenario-seam joint U-8 sweep provide an appropriate planned validation set.

The missing-inventory decision remains `native.admitted-boundaries-required` internally. It has neither a public registry row nor an alias; retaining it in operational diagnostics with absent DomainDetail is consistent with the alias rule and host-composition fault interpretation. It does not authorize a new public detail or an unknown-key fallback. No r8-dependent renamed invariant is needed before B2-c1.

A separate law step is warranted for the previously unspecified pre-Plan extends lookup and proposed new public refusal details. A bounded data-only resolver under C1 custody, with cycle refusal and no provider launch or fetch, is a sound direction. All-unresolved-edge refusal is conservative and avoids the unsupported partial graph carrier. Acceptance here concerns the implementation plan; it does not establish complete TypeScript compatibility or accept unpublished r8 text, its exact limits, routes or resolver implementation. Those require the stated independent law review before B2-c2.

B2-c0 can precede B2-c1, while the latter takes effective allowJs as a supplied observation and can proceed alongside r8 review. B2-c2 waits for the law and remedy-route work. C1/J1 later provide custody/composition. Workspace full-ledger margins remain a B3-b dependency; this plan does not close B2-b, M3 or qualification.

## Boundaries

No product code was written, no binding was made and no law changed. Wrote only REVIEW.md and review.json in the requested directory. Neither repository, stage nor control files were edited. Used read-only inspection, hashing, JSON parsing and Git queries; no Cargo, tests, builds, lane, network, other panes or delegation. No private fixture, installation directory, signing keys, held trees or T2 held-out entry was accessed.
