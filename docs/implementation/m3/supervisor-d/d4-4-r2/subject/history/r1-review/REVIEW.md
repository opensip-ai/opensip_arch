# CODEX2 review — D4-4 r1

## Verdict

**REQUIRED-FINDINGS**

The frozen subject manifest SHA-256 is `5d129b0f2ad4b6563b7f6f15a7403b24c54a699135a3ff135be4cd8ed2f886e4`. All 645 declared members rehash exactly, all 32 candidate paths match the frozen product map, the 21 existing paths are based on product commit `c31809cb4993c5c2bbba3d004d9337f12f18d17b`, and the 11 new paths are absent from that parent. The architecture authority resolves at `a70566340747162650b863693e1ab3d887845b18`.

The native adapter, member ordering and association checks, actual `Entrypoint` requirement, optional directory digest handling, typed refusal partition, final recheck ordering, same checked sender transfer, closed launch specifications, fixture confinement, provider-spoken observations, mutation restoration, and repository/census evidence are consistent with the reviewed authorities and stated scope. The operation-pin lifetime remains a production-composition obligation: the library does not claim that its adapter borrow keeps the operation alive, and the archived actual-child controls keep the retained trees alive through settlement.

## Required finding

### D4F-R1-RF-1 — TS2 `identityVersions` lacks an independent factory authority

`IdentityAuthority::TypeScript` supplies independent provider/runtime descriptor digests and descriptor fields, but it supplies no identity-version projection. In `session_factory/spec.rs`, the factory reads `identityVersions` from the actual sender Hello, checks only that its length equals `DispatchContext::identity_versions.len()`, and compares its members with that same bundled receiver context. Both sides are assembled codec outputs carried by `Provider::TypeScript`; neither is the separate admitted or pinned authority required by D4F-03 and the request's independent-authority boundary.

Consequently, a sender Hello and receiver context that agree on the same wrong, missing, or substituted identity-version map pass lines 227–238 of `spec.rs`. The frozen component control changes descriptor digests, descriptor fields, and sender realization, but has no case where the sender and receiver agree on a wrong identity-version projection while an independent authority stays correct. The provider-spoken `identity` case changes `providerBuildId`; it does not close this host-side gap.

Required correction: add the exact independent TS2 identity-version projection to the factory authority (or use an equivalently independent pinned constant projection), check the actual sender Hello and the actual receiver context against it with exact count, keys, and values before any recheck, and add an affected control in which both codec outputs agree on a wrong projection yet the independent authority causes a pre-recheck refusal. Freeze fresh affected evidence and any corresponding mutation/restoration evidence in the successor subject.

## Inventory candidate assessment

**ACCEPT**

The proposed `repository-file-inventory.v239.json` is 809,382 bytes with SHA-256 `26ca2b0ab73dc8454f609e349ae07bcba058a790a54bb10b65fcf5f026fced5a`. Against v238, all 1,422 parent file rows are preserved by value, all non-file fields are unchanged, and exactly 10 sorted, unique rows are added. `crates/components/src/session_factory.rs` remains its pre-existing planned row and is not duplicated.

The meaning projection has 161 distinct physical paths and valid candidate pointers: 150 inherited meanings plus 11 current direct meanings. Every pointer resolves to the stated path and raw `before` text. All six current supersessions are folded to their current `after` meanings, including the provider-protocol dispatch chain, while the raw inventory descriptions remain unchanged. The successor record and its archive-qualified `codeProductMap` and `integrationCensus` pins resolve to the frozen bytes.

This inventory assessment accepts the additive inventory mechanics and meaning projection only. It does not accept the D4-4 code unit, bind or integrate v239, supply description contract 187, or establish product qualification.

## Acceptance boundary

No production C4/native selection or signed-descriptor producer, J2 caller, spawn/effect/settlement wiring, source39 registration, D5 general structural gate, Linux/platform completion, integration, binding, status publication, or qualification is accepted by this review.
