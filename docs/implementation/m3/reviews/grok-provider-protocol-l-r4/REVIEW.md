# M3-L r4

Verdict: **REQUIRED-FINDINGS**.

Subject `docs/implementation/m3/provider-protocol-l/PROPOSAL.md` is 145405 bytes, sha256 `261db4b91f5a527de55cb3d4fca5e4729240f891b7086f75a5f68598cb914758`. An ACCEPT would be recorded as accepted in review and would take effect only when G1, G4, G5, G9 and G10 are met and S-M's delta round is accepted. The gate is not met.

## RF-1

r3's named corrections are in the derived table. `subjectScopeCommitment` sits on `CoverageKeyV1`. `stageId` is on Analyze stage requests and on the FactBatch and Coverage wrappers. Rust `subjectId` and anchor `factId` are included. Snapshot, dependency-source and prepared frames carry `snapshotId`, `dependencySourceSetId` and `planId` respectively. `analysisOrdinal` and `phase` are named in the non-identity column.

The ceiling is still short of the coverage key. `CoverageKeyV1` and C-2 `coverageKey.key` require `relation`, `resolution` and `schemaVersion` beside the members the Analyze rows list. `CoverageKeyV2` requires `relation` and `resolution` beside `sourceUniverse`, `targetUniverse` and `subjectScopeCommitment`. `ViewEntryV3` requires `relation` and `resolution`. NE:3279-3281 says `relation`, `resolution` and `subjectScopeCommitment` equal the requested key, and that the request key's `producer`, `producerVersion` and `schemaVersion` stay request coordinates. The rules admit the producer fields and omit `relation`, `resolution` and `schemaVersion`.

R1 is a name suffix. Those three names miss it. Their descriptions do not name an identity type or an R1 member, so R4 and R5 do not fire. Returned keys are JSON Schema, and that walker classifies only by the designated list, the R1 suffix and an identity pattern. `L-C1` exits 0 and reproduces the omission. Admit every required member of those key records, and `ViewEntryV3.relation` and `ViewEntryV3.resolution`, in both walkers, and regenerate the table.

A mechanical rule set is the right form for the ceiling. r3 showed a hand-written list drift. The frame map, the record identities and the child map match the payloads they cite. R4 rightly admits `dependsOn`, `producerVersion` and the prepared `logicalPath`. R5 rightly admits `producer` where its description is the same constant as `providerId`. `SCALAR_START` keeps scalar digests and ordinals from being read as nested records. `planRow` belongs: RPP:579 says PlanId commits the rust-v1 rows and each row supplies owner and configuration identity. The gap is the key record, not the choice of a generator.

## RF-2 is resolved

Every FA-2 §0 row reopens this law. A and B replace the Analyze and Complete payloads, C sets the commitment every key carries, and D extends the Hello token arrays. The trigger, G10, the dependence paragraph, the summary table and X15 state that map. The parts that need none are the NE:93 header sentence while §9.8 is unchanged, schema layout, vectors and evidence, README prose, and the materialization map.

## The earlier notes

ME:478 is the sentence "The crate never mints `fact2`". Item 5 and the ME joins row cite it.

`git diff --name-only e093e90 cd5958b` lists `design-lock.json` and X4-F1's ten `crates/security` files. The lock moves from 77 contract successors to 82. Both copies contain the register pin `de21a7e0`.

Item 22.3 lists every class item 6 names, including dependency source sets and prepared outputs, and says per-file dirtiness is never sufficient by itself.

## FA-2 r2

Applying the third trigger to FA2-R1-01 and FA2-R1-02 in this round is right. NE:1927 is on the reopen list. Items 1, 13 and 22 already speak only of TypeScript and Rust workers, and the census schema bytes are unchanged. X16 and the M3-C joins row state FA-2 r2's narrowed X-FA2-C: the enumerator of a TS or Rust binding that owes a symbol inventory, excluding host-derived inventories and syntax universes; a worker for every such universe; and the Plan-time token need.

## What depends on what

**O7.** G9 and item 17. A delta round only if the outcome lets a provider execute repository code, needs a new wire signal or member for confinement, or makes the provider resident or pooled.

**S-M.** Item 9 entirely: every placeholder, F, T, and every outcome. O3 and O4, including both when (B) and (C) hold together. X6 through SM-8. A TS2 limit question, through SM-6, that only a successor can answer. MC's conditional S-R, through SM-5 and SM-6.

**FA-2.** G10, items 1, 13 and 22, and item 10's census sentence. A delta round for a forced change to a wire member, a key's commitment (including every §0 row, A to D), the admission point, or the reuse treatment. None for the NE:93 header sentence, schema layout, vectors, evidence, README prose, or the materialization map.

The opening paragraph still calls the third round any change that FA-2's acceptance forces. The operative map is narrower. That sentence should follow the map.
