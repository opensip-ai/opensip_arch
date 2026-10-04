# GROK2 review: M3-L r5, provider protocol and reuse

**Verdict: ACCEPT.** Recorded as accepted in review. The law takes effect only when L-G1, L-G4, L-G5, L-G9 and L-G10 are met, L-G11 still holds, and S-M's delta round is accepted.

Subject: `docs/implementation/m3/provider-protocol-l/PROPOSAL.md`, 172,198 bytes, sha256 `f654ee4e9149e62693ebae8177adcc1f3a8a595b745c1e7503e5f279b80e3e88`. That matches `hashes.txt`. Base: `PROPOSAL-r4.md`, 145,405 bytes, sha256 `261db4b91f5a527de55cb3d4fca5e4729240f891b7086f75a5f68598cb914758`, the r4 subject. Also part of r5: `evidence/wire_identities.py` (`50d8a35a…`, 32,573 bytes) and `evidence/wire-identities.json` (`9fdff61c…`, 50,554 bytes). L-C1 `--check` exits 0. No cargo was run. `~/Library/Application Support/OpenSIP` was absent. The private 413 fixture was not read.

Grok's r4 RF-1 and NBO-1 are closed. RUST3-LIM is joined, not re-reviewed.

## RF-1

R7's record list is the four records the r4 fix named, each with its sentence.

- DLV `CoverageKeyV1` (DLV:804-817) is closed and required on `relation`, `resolution`, `sourceUniverseId`, `targetUniverseId`, `subjectScopeCommitment`, `producer`, `producerVersion` and `schemaVersion`. Its join is the field-for-field copy of `c2-plan-stage-schema.v3.json#coverageKey.key`. DLV:726 is the "full requested key" sentence.
- C-2 `coverageKey.key` is that key. RPP:544-548 is `CoverageKeyV2`'s external of the same eight fields.
- The returned key is REG `CoverageKeyV2`, required on `relation`, `resolution`, `sourceUniverse`, `subjectScopeCommitment` and `targetUniverse`. NE:3278 says `entries[i]` answers `requestedCoverageDomain.keys[i]`. NE:1929-1930 requires `key.relation`, `key.resolution`, `key.sourceUniverse` and `key.targetUniverse` to equal `D`. NE:3281 leaves `producer`, `producerVersion` and `schemaVersion` as request coordinates, so they are not members of the returned key.
- `ViewEntryV3.relation` and `ViewEntryV3.resolution` are required, and NEM:1566-1567 refuses `native.coverage-entry-key-mismatch` when either differs from the key. NE:3529 names that cause. No other entry member is required to equal a key member. `examinedUniverse.subjectScopeCommitment` is already R1.

R1 to R6 keep their labels. R7 fires only after them. The other composite keys are classified as item 13 says: the fact identity is host-only (`factIdContract.owner` is "Rust host only"); commitment preimages stay content except the keys inside `requestedCoverageDomain`; a view is not on the wire; `OccupancyCompanionV1` is associated by `candidateOrdinal`; correlation tuples are exchange ordinals (`stageId` stays R1); scope summaries contribute the commitment (R1) and not `scopeKind` or `subjectCount`.

The 33 R7 paths are only `relation`, `resolution` and, on a request key, `schemaVersion`. Per language the existing rows gain 15: three on the Analyze request key, and `relation` plus `resolution` on the returned key and the entry in Coverage, post-Analyze Unavailable and BudgetExhausted. The new RUST3-LIM row adds the same three request-key members. Nothing outside that set is marked R7.

## Counts

The regenerated report is 52 payload rows and 278 identity-bearing paths: TypeScript 21 rows and 121 paths, Rust 31 rows and 157 paths. By rule: R1 200, R2 23, R3 4, R4 15, R5 3, R7 33. The +43, with none removed, is those 30 R7 paths plus the RUST3-LIM row's 13, of which 3 are R7. L-C1 reproduces the table and the report.

## RUST3-LIM

L-G11 is a lawful second addition, on the same ground as L-G10: L in effect would otherwise fix a Rust3 that refuses before spawn two of S-M's seven Rust medium workloads and nine of T2's 22 Rust entries. Its state is met in review, held on FA-2. `reviews/codex2-rust3-lim-r1/status.json` is `ACCEPTED`. The review is ACCEPT-DESIGN-UNIT with no required findings, on subject `5dfd3cd9…` (3,123 bytes) and successor `70f494d9…` (17,130 bytes), the bytes this law pins. Both FA-2 handshake parents still hash to `32aeec8c…`. The unit binds after FA-2. The lead's completion of `rust3-lim-unit.json` is recorded as the lead's, and it is not an acceptance of the design.

The fourth trigger matches both statements and both NBOs. NBO-1 is two copy-line annotations in the evidence (`copyLine` 179 and 219, eight lines above the finished copy) and needs none. NBO-2 closes in the two ways the review named. Adding `RustFactBatchV2Vector.stageId` to the reading-rule list edits §9.3a (lines 74-80: §9.6, the execution-inputs echo, startup `hostConversion`, and FA-2 `AnalyzeV3.stages`) and the schema's copy of that rule, so it takes the round. Giving that description the NE:3070 parenthetical edits a handshake-copy description outside the `subjectScope` entry and enum, and needs none. The reopening parts are the ones the successor actually overrides: the token at NE:2790, §0 rows E and F, and the §9.2, §9.6 and §9.3a overrides at NE:2883, NE:3028, NE:3070 and NE:2942.

The AnalyzeV2 condition is the token-absent `stages[]` path. Under `subject-scope-reference-v1` the stage is `StageRequestV3` and carries `analysisDomain.subjectScope.subjectScopeCommitment` (R1) instead of per-file `subjectId`. That row is on the wire only once RUST3-LIM is bound after FA-2. SM-11 to SM-14 match RUST3-LIM's table, including `S_eff`, and they are placeholders for measured budgets, not protocol constants. `ProtocolLimitsV3` is unchanged. X13 and R12 are closed by pointing at that accepted successor. What remains is its binding, not the cap.

## Rename, NBO-1, re-pins

Operative gate references are L-G1 to L-G11. The kept r2 to r4 tables still say G1 to G10, and each table says so. Left as they were: F2 and G3, F4 and G2, "a G2 plan", "bears on G4", the DR-G gates, and the REG:342 quotation "G10 uses TS protocol major2/Rust major3". Open question R7 is still the L-G6 draft question.

The opening paragraph now states four triggers, with the same FA-2 and RUST3-LIM boundaries as the operative trigger.

The H1 to H3 map is the same passages: X-H1 is H3:850-858, X-H4 is H3:867, item 17 is H3:613-643, "Without FA-2" is H3:705, and the round-timing line is H3:841. H3 is `7a562720…`, 115,470 bytes. M3-PLAN r9 (`72bc7a13…`, 150,586 bytes) records the review rule and "FA-2 accepted (G10, P7-2)" on the M3-L row (`:255`) and day 0 as "L in effect" (`:385`). Its NBO-1 row (`:70`) asks M3-L to rename the gate "L-G1 onwards". X9 is right that r9 has not yet recorded L-G11, RUST3-LIM among the pre-day-0 rounds, or that rename: day 0 there is still "every gate item G1 to G10".

Product main is `392499e`. From `cd5958b` only `design-lock.json` changed. The lock is 335,667 bytes, sha256 `d1b2a5d1…`, and it has 83 contract successors. The one added successor is CRC-1 (`29df5f5e…`). Its parents and overrides are the identity contract, workflows-and-surfaces and the selected effective copy, the composition contract, the detector-manifest description, and I1-L's identity schema. None of those selectors is a line this law cites, and none is a parent of FA-2 or RUST3-LIM. The core-provider sentence agrees with items 1 and 5: syntax-universe work only, never a TypeScript or Rust record.

## Dependence

- **O7:** L-G9; item 17; a delta round only if the outcome lets a provider execute repository code, needs a new wire signal or member for confinement, or makes the provider resident or pooled.
- **S-M:** item 9, every placeholder, F, T, and every outcome, including SM-11 to SM-14 as measured figures; O3 and O4, including both when (B) and (C) hold together; X6 through SM-8; a TS2 limit question only a successor can answer, through SM-6; MC's conditional S-R, through SM-5 and SM-6.
- **FA-2:** L-G10; items 1, 13 and 22, and item 10's census sentence; a delta round for any forced change to a wire member, a key's commitment (every §0 row, A to D), the admission point, or the reuse treatment. None for the NE:93 header sentence, schema layout, vectors, evidence, README prose, or the materialization map.
- **RUST3-LIM:** L-G11; items 1 and 13 (its row and the AnalyzeV2 condition); item 9's SM-11 to SM-14; X13 and R12; a delta round for a later change to a part that sets a wire member or a commitment, including a rebuild forced through FA-2's handshake copies. None for README prose, evidence, vectors, scratch verify, or the materialization map. NBO-1 needs none. NBO-2 reopens this law only if it is closed by editing §9.3a's reading rule.
