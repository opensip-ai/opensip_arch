# J-BS admission-source selection r1

Verdict: ACCEPT-DESIGN-UNIT. Implementation verdict: ACCEPT-UNIT.

This accepts the two exact admission files and the contract selection that publishes them. It leaves the accepted J-BS design, eight-path code review, and binding attestation unchanged.

Those pins remain exact. Design review `/tmp/opensip-implementation/reviews/grok-jbs-design-r1/review.json` is 159 bytes, sha256 `bbbe00df12e466f456536926f482b4914f55f779bff15bc9e5fcbab6bbfc43cf`, ACCEPT-DESIGN-UNIT. Code review `/tmp/opensip-implementation/reviews/grok-jbs-product-r1/review.json` is 152 bytes, sha256 `85bf241138901bd9bc41f6fe48e44989ed82e9afbfa1163ca898445a44d716e7`, ACCEPT-UNIT. Binding attestation `/tmp/opensip-implementation/reviews/grok-jbs-product-bind-r1/review.json` is 159 bytes, sha256 `fdc201596c5c69a908f0478166718203ba47def45cbe934319ad98e31c702f61`, ACCEPT-DESIGN-UNIT. The accepted schema is 71837 bytes, sha256 `63f97dfcb77d3065c4a5f4af3194fbe0e874cc89a8b9e2533728da2a4af28ec0`, with `$id` `urn:opensip:product-v1:workflows:evaluator3:invocation:5` and `schemaMajor` 5.

Product HEAD is `2146910cca62e2dce492e7b637e4c2d11390c419` with an empty porcelain. Architecture HEAD is `23bfb5d1dab2acc079d1ab9e34b7156807839ce1` with no tracked changes. The earlier product candidate still holds the old admission pins. The OpenSIP support directory is absent.

## Why this join exists

`evidence/strict-preflight-refusal.txt` is 869 bytes, sha256 `a2cd008d158cdf50ee65f89f0b6360554d718bfced07a51223e60be6fb3f6ee0`. `generate_contracts.py` called `verify_design.py`, and `admission_sources` raised `admission source bytes differ from accepted architecture` before generation. That is the comparison at `verify_design.py` lines 601–602: the implementation bytes must equal the architecture pin selected by the admission map. The current map still names `docs/implementation/m1/source-selection-v2/schemas/sources/invocation.v5.schema.json` at 71161 bytes, sha256 `28aa0c42b05fa3ad13ae4d9aed1bac17983453577306b8e15678dc74af63f4fb`. This unit is the exact source join for the accepted schema. This review did not rerun the generator.

## Two product files

`schemas/admission-registry.json` stays 17170 bytes. Its only change is the invocation5 row, from 71161/`28aa0c42…` to 71837/`63f97dfc…`. `schemaId` stays `urn:opensip:product-v1:workflows:evaluator3:invocation:5` and `sourcePath` stays `schemas/sources/invocation-v5.schema.json`. The other 47 sources, the sorted schema-id order, the profile, and all 15 aliases are equal to the product file. No alias uses that source path or that schema id. The new file is 17170 bytes, sha256 `a4a02c4271245c7a0c3a401fea95dc93f1849004bee41c4c7b1a433e5ed19c30`.

`schemas/admission-source-map.json` changes in two places. `registryArchitectureSource` moves from the bound I1-a registry `15457b75…` to this proposed copy, `docs/implementation/m3/host-pipeline-j/j-bs-admission-r1/schemas/admission-registry.json`, 17170 bytes, sha256 `a4a02c42…`. The invocation5 `architectureSource` moves from the old source-selection pin to `docs/implementation/m3/host-pipeline-j/j-bs-r1/schemas/invocation-v5.schema.json`, 71837 bytes, sha256 `63f97dfc…`. Schema id, implementation path, schema version, and the other 47 source rows stay equal. The new map is 20066 bytes, sha256 `0bd63f99f1c1d5c781e43c7cc6fc19cf283932d7d5c4d61f048a5e6996899dca`.

Restoring those coordinates reproduces both current product documents. The 349-member generator closure, both at product HEAD `22fcd1f8…` and in the accepted product candidate `2d6ece9e…`, contains neither admission file. This unit changes no generator input, provenance, generated output, alias, host, or emitter byte.

The read-only checker was run as named, with `nice -n 10` and `python3.14 -I -B`. It passed: 48 current sources joined, 15 aliases unchanged, zero invocation aliases, and the closure unchanged. It ran no generator and reported no product qualification. Its result matches `evidence/checks.json`.

## Contract selection

Subject manifest sha256 `a5cdd49a9bd4fb4f79006d07e89132cb6488cb7a9f91016031124170f3e23818` (1808 bytes). All eight members match. Successor `docs/implementation/m3/host-pipeline-j/j-bs-admission-r1/successor.json` is 2285 bytes, sha256 `ea927d49211a9df0f1893e4ddc843b7363b7a4308bdc1734f7d4d7c95f8191ee`. `passageOverrides` is empty and `passageSupersessions` is absent. Its candidates are the other seven subject members, including this registry copy, so the successor is what selects that registry.

The I1-a parent `docs/implementation/m3/preview-pack-i1/i1-a/schemas/admission-registry.json` is already a candidate of bound successor `7d6c04e9914809409e01027e63d7b9cde670c6e8757538a13b743b9d0af5a03d`, at 17170/`15457b75…`. The schema parent is a candidate of the accepted J-BS design successor and is not in the architecture repository yet. It becomes an accepted parent when that design successor binds. Bind design, then the product materialization successor, then this registry selection. Inventory v166 stays the bound inventory, 614780 bytes, sha256 `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`, and already contains both product paths.

Strict public no-bypass generation drift and source/dependency checks are still required before integration. They may only corroborate these frozen bytes. Product code commits and the final design-lock bind stay separate. Nothing is pushed. Full M3, J3d, and qualification remain outside this unit.

No required findings.
