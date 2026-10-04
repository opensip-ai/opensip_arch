# FA-2 — the provider symbol census carrier (native contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Status: **PROPOSED frozen candidate, r2.** It needs Codex's `ACCEPT-DESIGN-UNIT` and root assent before selection.

FA-2 answers cross-law item **X-H1** of the fact-admission law M3-H: a TypeScript or Rust provider's symbol census has no carrier on TS2 or Rust3. It is joined by **M3-L** (r3 introduced the join; r4 is in review), which makes FA-2's acceptance a gate item for L taking effect. It changes no product file.

**Base.** Product main `e093e90`, the base this unit was assigned on. Main has since moved to `cd5958b` (I1-L, B-S1, B-S2, B-S9, X4-F1 and I1-P; 82 contract successors). None of those commits touches a file FA-2 copies, and none binds a selector FA-2 uses. B-S1 binds eleven NE line overrides (NE:714-940 and NE:4135), all disjoint from FA-2's thirteen. `evidence/build_fa2.py` checks the locks at `e093e90`, `15c0779` and `cd5958b`.

## r2 changes

Codex reviewed r1 (`reviews/codex-fa-2-r1`): REQUIRED-FINDINGS, two P2 scoping findings and two observations. Every other decision was assessed as lawful. r1's changed members are kept in `reviews/codex-fa-2-r2/r1-members/`.

| # | Finding | Change | Where |
|---|---|---|---|
| 1 | **FA2-R1-01** | The NE:1927 insertion, §4.1a step 1's census source, is restricted to a `symbol`-kind key **in a TypeScript or Rust universe**, as the NE:1913 insertion already was. A syntax universe's symbol keys keep their in-host census, which needs no carrier (§9.8, "Not this section"). This is Codex's exact text. | `evidence/build_fa2.py` (the NE:1927 entry); `successor.json`; the table row for 1927; LD-F2's host bullet |
| 2 | **FA2-R1-02** | X-FA2-C is narrowed to LD-F6's scope: TS and Rust bindings that **owe the worker's symbol census**. It now excludes host-derived file and package inventory bindings and the inventory relations, whose producer and enumerator are H's X-H3, routed to M3-C r8 and CRC-2. It also excludes syntax universes, which have no child (X-FA2-E1). Codex's exact row is used, with that routing and the syntax-universe clause added. It now agrees with LD-F6 and with §9.8's "When a census is owed". | X-FA2-C |
| 3 | **FA2-N1-01** (observation) | **Recorded, not changed.** The design-evidence references `native/provider_wire_model.v1.py` and `native/provider_startup_model.v1.py` still load the original handshake and startup schemas. The startup model also compares every entry's `subjectScopeCommitment` with the requested key unconditionally. They are not updated, for three reasons: they are neither parents nor members of this unit, and editing them would make them new successor members of a different reference contract; their stated scope is historical design evidence, not FA-2's acceptance evidence, which is this unit's own build script and vectors; and Codex asked for no byte change. The implementing owners (D2b's codec and H's admission) track successor-aware schema loading and the conditional symbol-key check through clean settlement, and keep the old no-token refusal controls (X-FA2-D, X-FA2-H). | "Design-evidence references" below |
| 4 | **FA2-N1-02** (observation) | The evidence count is corrected: seven valid payloads, five payload refusals, and two projected-SIS cases. It is Codex's exact text. | "Evidence and checks" |
| 5 | — | **Re-pinned and re-verified.** Every generated file is rebuilt byte-reproducibly. The build checks three locks. The product's own `tools/verify_design.py` at `cd5958b` is run on a scratch lock: `cd5958b`'s 82 successors plus FA-2 r2 as the 83rd, with a labelled synthetic review and assent that exist only in scratch (`reviews/codex-fa-2-r2/scratch-verify.txt`). | `fa-2-subject.json`; request |

No carrier, commitment, wire member, admission point or reuse treatment changes.

## Short names

Every sha256 prefix is the first 8 hex of the exact bytes pinned in the review request (`reviews/codex-fa-2-r1/hashes.txt`).

| Name | Document | sha256 |
|---|---|---|
| **H1** | `docs/implementation/m3/fact-admission-h/PROPOSAL-r1.md`, M3-H r1. Reviewed by Grok (REQUIRED-FINDINGS on an unrelated item, RF-1, the anchor routing). r2 is being drafted and keeps X-H1 and the FA-2 row unchanged in substance. **Not accepted; cited as the source of the obligation, not as authority.** | `69f50bb1…` |
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md` | `83b99783…` |
| **IE** | `docs/v2/contracts/product-v1/identity-and-evidence.md` | `c82404f3…` |
| **ENC** | `docs/coop/design-corrections/foundation/enumeration-contract.v1.md` | `b7858bc8…` |
| **EXC** | `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md` | `22ee2507…` |
| **SIS** | `docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json` | `6ab46925…` |
| **RPS** | `docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json` | `53380a24…` |
| **IDS** | `docs/coop/design-corrections/foundation/identity-schemas.v3.json` | `a76c9e2f…` |
| **HS / PHS** | `docs/coop/design-corrections/native/provider-handshake.schemas.v1.json` and its selected product copy `docs/implementation/m1/source-selection-v2/schemas/sources/handshake.v1.schema.json` (identical bytes) | `9090e2ad…` |
| **ST / PST** | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` and `.../source-selection-v2/schemas/sources/startup.v1.schema.json` (identical bytes) | `1e35a77b…` |
| **DLV** | `docs/coop/artifacts/delivery.v2.json`, TS2's inherited base | `47b6cfd1…` |
| **RPP** | `docs/coop/artifacts/rust-provider-protocol.v2.json`, Rust3's inherited base | `6308a98c…` |
| **NEM** | `docs/coop/design-corrections/native/native_evidence_model.v2.py` (bound copy since B-S9; cited lines unchanged) | `7d1c0acf…` |
| **MI** | `docs/implementation/m3/preview-pack-i1/PROPOSAL-r2.md`, M3-I1 r2, accepted | `1eb47d1e…` |
| **L3** | `docs/implementation/m3/provider-protocol-l/PROPOSAL.md`, M3-L r4, in review with Grok beside this unit; its r3 bytes are `PROPOSAL-r3.md` | see request |

## The problem, exactly

Three facts make the census unreachable today (H1 item 17, H1:507-514; X-H1, H1:724-732).

1. **The census is the provider's to produce, and only the provider's.**
   - A symbol inventory is "a provider's explicit population assertion" (NE:88-91).
   - Its rows are "native attestations; the host does not recompute symbol extraction" (SIS:5; ENC:186).
   - Symbol-scope subjects are census rows (RPS:15 `subjectKindLaw`; SIS `InventoryRowV1.nativeSubjectId`; ENC:93). "Inventing symbol-to-path parsing would be fabricated evidence" (RPS:15; NE:507-515).
2. **No TS2 or Rust3 frame carries it.**
   - Candidates are closed `FactCandidateV1` values (NE:2883).
   - Coverage frames carry `CoverageResultV3` entries only (NE:3270-3276).
   - Terminals carry counts and commitments (DLV `StageResultV1`, `CompleteV1`; RPP `CompleteV2`).
   - "Do not add a new protocol3 frame name" (EXC:270).
3. **The request key would need the census before it exists.**
   - A symbol scope's commitment is scope2 over `D`, whose `subjects` are the census (NE:1897-1915).
   - The returned key must equal the requested key (NE:3279).
   - The request is built before spawn (NE:3230-3233).

The consequence, per H1: no TypeScript or Rust symbol-kind Coverage can be admitted; F2 and G3 cannot deliver "symbols and Coverage" lawfully; and I1's `cycle-representative` rule can never decide on a real Run (H1:582; MI:113-127, MI:155-165).

The reference model already knows the gap. `admit_coverage_result_v3` says the `symbol` branch "needs the committed inventory" (NEM:1585). The pre-Analyze conversion assumes a host scope descriptor for every requested key (NEM:4586-4590), which no symbol key can have.

## The design in one paragraph

A new optional, non-identity capability token, **`symbol-census-v1`**, negotiates **one added member, `symbolCensus`, on the existing `Analyze` and `Complete` payloads** of both protocols. This is exactly the `target-attribution-v2` / `FactBatchV3` pattern (NE:2797-2814, NE:3061-3069). On Analyze it is the census request: the enumerator's `closure2`. On Complete it is the census: examined paths and rows. **Phase 1:** before spawn, every symbol-kind key commits to the census **rule**, the scope2 of its descriptor with `subjects: []` (D∅). **Phase 2:** on return, every symbol-kind Coverage entry commits to the census **values**, the scope2 of the same descriptor with the census as `subjects`. The host projects the census into `SubjectInventoryV1` records at clean settlement, exactly as it projects `TargetAttributionV2` (NE:3118-3126; EXC:259). No frame, phase, terminal, limit, identity version or major changes.

## Decisions (lead decisions, 2026-10-04)

Each is made under the owner's standing direction to decide on the lead's recommendation and to block only where no recommendation exists. Each names the alternatives it rejects. The owner may reverse any of them.

### LD-F1. The carrier: one negotiated member on Analyze and Complete

- **Decision.**
  - Token `symbol-census-v1` (NE §9.1 as amended).
  - Under it, `Analyze` carries `TypeScriptAnalyzeV2` / `AnalyzeV3` and `Complete` carries `TypeScriptCompleteV2` / `CompleteV3`. Each is the inherited payload with every inherited member unchanged, plus `symbolCensus`.
  - The census rides on `Complete` only. Clean `BudgetExhausted` and post-Analyze `Unavailable` carry none, and their owed inventories are host-derived outcomes, as H1 item 4 already designs them (H1:213-234).
- **Why `Complete`.**
  1. **Cardinality.** A census is per universe and one child serves one universe (NE:3166-3189; ML item 2). `Complete` is once per Analyze. A per-stage frame would carry the census once per stage, or need a "first stage carries it" rule.
  2. **Admission.** H admits atomically at clean settlement, and only `Complete` is admitted with candidates (H1 items 3-4; DLV:1517 "admits facts only after Complete+matching commitments+zero-exit+EOF"). A census on any other terminal would be discarded by H1 item 4's own rule.
  3. **Cost.** Two payload versions per language (Analyze, Complete), against six for the per-stage route (Coverage, `BudgetExhausted` and `Unavailable`, in each language).
- **Why a member on Analyze at all.** The worker must compute the census commitment (LD-F2), and D's `enumeratorClosure` is the one coordinate no existing request member carries. The C-2 stage carries no closure id (`c2-plan-stage-schema.v4.json` `stageSchemas.kinds.fact-derivation`), and neither do `StageRequestV1` or `StageRequestV2`.

### LD-F2. The ordering problem: commit to the rule, then to the values

- **Decision.**
  - **Request (before spawn).** A `symbol`-kind key's `subjectScopeCommitment` is the NE §4.1a commitment of **D∅** = `{schemaVersion 2, snapshotId, sourceUniverse, targetUniverse, relation, resolution, enumeratorClosure, subjects: []}`.
  - **Return (on `Complete`).** Each symbol-kind entry carries, as `key.subjectScopeCommitment` and `examinedUniverse.subjectScopeCommitment`, the commitment of D∅ with `subjects` set to the census's `nativeSubjectId`s, in canonical-set order; `subjectCount` is the row count.
  - **The host.** It runs §4.1a's six steps unchanged, with "its own enumeration" read, for a symbol scope of a TypeScript or Rust universe, as the admitted census (r2, FA2-R1-01). A syntax universe's symbol scope keeps its in-host census.
  - **The worker.** It computes the commitment with the foundation encoder and `H` frame (IE §3), and checks each request commitment before analysis.
- **Why it is lawful against §4.1a and NE:3279.**
  - **One recipe.** D∅ and D_census are the same closed `subject-scope` record (IDS:620-680, `subjects` has no `minItems`) under the same recipe, so no second recipe or `H` domain is added (NE:1913-1915).
  - **The Plan already commits the rule.** "The Plan selects programs and expected inventory locators before facts or findings exist" (IE:1464-1465). The EnumerationPlan binding commits the universe, the enumerator and the symbol extent (ENC:24, ENC:53, ENC:172). D∅ is that commitment spelled as a key.
  - **The Join with scope2 survives.** The returned payload's commitment is still the identical digest of the `scope2` that `coverage2` binds (NE:1917-1922). So `coverage2`, `view2`, Run closure and replay are unchanged, and `inspect_coverage_producer` needs no new branch.
  - **One equality changes, for one class of key.** NE:3279's "equal the requested key" gains a symbol-key exception under the token. Relation, rung and universes still must equal the request.
  - **Three cases need no change.** Terminal entries, the pre-Analyze conversion (H1:377, H's own recommendation (c)) and a zero-row census all carry D∅, so their keys equal the request byte for byte.
- **The vectors.** `evidence/vectors.json` gives worked commitments for both phases. Its encoder is checked first against NE's own oracle case (`subject-scope-commitment-is-the-scope2-identity-in-native-sha256-text-form`, scope2 `2c5f653d…`). It also includes a pair of ids whose UTF-8 row order differs from their canonical-set order.

### LD-F3. What the census carries, and what the host fills

- **Wire row** `SymbolCensusRowV1`: `{nativeSubjectId, path, qualifiedName, exported, signatureTokens}`, strictly ascending by the UTF-8 bytes of `nativeSubjectId`. These are exactly SIS's provider-attested symbol members (SIS:276-313, SIS:506-579).
- **Wire census** `SymbolCensusV1`: `complete` `{examinedPaths, rows}` or `over-bound` `{rowCount, examinedPathCount}`.
- **Host-filled**, as the occupancy companion leaves `planId`, `sourceFactId` and `producerClosure` to the host (NE:3092-3093, NE:3118-3126):
  - the locator `planId`, `parameterDigest`, `cellOrdinal` and `programOrdinal`;
  - `kind`;
  - the state carrier, always `complete`, `null`, `null`;
  - per row, `kind`, `subjectLanguage` (SIS's suffix table, a pure function of `path`) and `projections: []`.
- **One census, many records.** The census is per universe, and a universe binds one extent (ENC:24). So the host projects one census onto every owed `(cellOrdinal, programOrdinal, symbol)` locator at that universe. Rows are byte-equal across locators, as ENC:180 requires.
- **Rejected:**
  - **The full `SubjectInventoryV1` on the wire.** The worker knows neither `parameterDigest` nor the cell ordinals, and asking it to echo them adds worker-minted identities (DLV:572).
  - **Worker-supplied `projections`.** Detector closures are Plan-selected rule closures the worker never sees. `[]` is SIS's "projection unavailable" (SIS:577; ENC:137).

### LD-F4. Complete only; no partial census on the wire

- **Decision.** No `partial` or `unavailable` variant exists. A worker that cannot attest its complete symbol extent does not send `Complete`.
  - Partial work ends in `BudgetExhausted`, where H1 item 4 records `partial` / `budget-exhausted` with no rows.
  - Unavailability ends in `Unavailable`, recorded `unavailable` / `provider-unavailable`.
- **Rejected:** a partial census on `BudgetExhausted` carrying its known rows (ENC:120 would admit them). It contradicts H1 item 4's discard rule, which rests on the uncommitted pre-terminal stream (DLV:1138, DLV:1171). It needs two more payload versions per language. And it decides nothing: every Coverage entry of that Analyze is already `unknown`.
- **Open for F2 and G3.** If a provider meets a real case where analysis completes but the symbol extent cannot be attested, it reports it to the native owner. A later additive successor can add the variant.

### LD-F5. Bounds: never truncate; over-bound is a scope limit, not a fault

- **Decision.** A census of more than 100,000 rows, more than 100,000 examined paths, or more than 4 MiB of deterministic CBOR is sent as `over-bound`, with no rows. Those are SIS's and IDS's bounds (SIS:96, SIS:106; IDS:674; IE:117).
  - The host takes the subject-scope scope-limit route, which H1 item 9 routes through C's S-B successor (X-H6; H1:327-329). It never truncates or shards (NE:4280).
  - A projected record or a `D` that crosses its 4 MiB `C` ceiling takes the same route.
  - The 4 MiB CBOR bound also keeps `Complete` far inside `maxFramePayloadBytes`, 64 MiB in both languages (NE:2962; RPP:97).
- **Rejected:** letting an over-large census fail schema validation, which would turn a large repository into `PROVIDER.PROTOCOL_VIOLATION` (operational-failed 4), a false fault.

### LD-F6. When a census is owed, and who the enumerator is

- **Decision.**
  - A census is owed to a worker exactly when an expected symbol inventory's available binding names that worker's universe.
  - All such bindings name one enumerator, the worker's provider closure, which also produces the worker's stages.
  - The host asks for a census exactly when it asks for a symbol-kind key.
  - Where a census is owed, the token is "a token the Plan needs" (NE:2848-2853): a signed row without it is never spawned, with that step's consequence.
- **Why.** NE says enumerator and producer are "not blanket-identical" (NE:3054-3059), which is true in general. But a census carried by a worker can only be that worker's enumeration, and D∅'s `enumeratorClosure` must be the closure that produced the subjects (NE:1910-1911).
- **Cross-law (C).** C r6 leaves the TS/Rust enumerator implicit (MC:893). Its next revision states it (X-FA2-C below).

### LD-F7. Close the inherited key-commitment gap for every key (finding F-1)

- **Finding.** NE §0 never names the inherited request-key commitment rules as superseded:
  - DLV `coverageDomain.keyConstruction.subjectScopeCommitment` ("exact reconstructed SubjectScopeV1.subjectScopeCommitment");
  - DLV `RequestedCoverageDomainV1.workerRule` ("requires every key.subjectScopeCommitment to equal subjectScope.subjectScopeCommitment");
  - RPP `planAndDomainProjection.coverageDomainAlgorithm[3]`.

  Under them, every key of a stage carries one file-set commitment, under a different recipe. Under §4.1a every key carries scope2 over its own `D`, which names its relation and rung. Both cannot hold for any stage with two keys. And §4.1a step 3 refuses a key whose commitment is not scope2(D). So the conflict exists for **every** key, not just symbol keys, and §0's C-2 row already makes §4.1a "the successor producing recipe" of that field (NE:136).
- **Decision.** FA-2's §0 row C names the three selectors superseded for the key commitment only, in both languages and with or without the token. The inherited file-set records (`SubjectScopeV1`, `subjects`, `analysisDomain`, `domainCommitment`, `commitments.subjectScope`) stay as transport proofs, and the worker still recomputes them.
- **Rejected:** superseding them for symbol keys only. That leaves source-path and package keys under a rule §4.1a contradicts.

### LD-F8. Form of the successor

- **Decision.**
  - NE: thirteen insert-only line overrides, one of which appends §9.8 (`section-9-8.md`).
  - ST and PST: three JSON Pointer string overrides each, the same text on both, as LD-L5 overrode both WS copies.
  - HS and PHS: complete successor copies. A token enum append cannot be a pointer override, which is I1-L's LD-L1.
  - A new census schema document, and a byte-identical product copy for D2b.
  - The token is appended **last** in both enums, so no member moves (I1-L's LD-L3).
- **Rejected:**
  - Editing the registered `native-evidence.schemas.v2.json`, whose raw SHA-256 is a registered `payloadSchemaDigest` (NE §10). §0 row D records the extension instead.
  - Restating `StageRequestV1` and `StageRequestV2` in the new schema. A second transcription of closed inherited records invites drift. The new schema names them by selector and restates only `Complete`'s simple inherited members.

### LD-F9. Binding

After acceptance the lead appends FA-2's `contractSuccessors` entry to `design-lock.json` in a binding-only product commit (D3's form). Selecting FA-2 changes no product byte and no generation source. D2b copies the two product schema sources later (`materialization-map.json`). Nothing is staged tonight: the product is read-only for this run.

## Candidates evaluated

| # | Carrier | Verdict | Why |
|---|---|---|---|
| 1 | **An additive member on an existing frame, under a negotiated token** | **Chosen**, on `Analyze` and `Complete` | It is the precedent path inside the majors (NE:2797-2814; EXC:270-272) and needs no new frame. See LD-F1 for why these two frames. |
| 1a | The same on the per-stage `Coverage`/`CoverageV3` frames and on the terminals (H1's recommendation (a)) | Rejected | The census would repeat per stage or need a "first stage" rule, and it needs six payload versions. A census on `BudgetExhausted` would be discarded by H1 item 4. |
| 1b | The same on `FactBatch` | Rejected | `FactBatch` is per batch and capped at 4,096 candidates, and it is already versioned by `target-attribution-v2`, which gives four payload combinations. A census is not a candidate stream. |
| 1c | The same on `NativeContextVerified`, so the census arrives before Analyze | Rejected | Pre-Analyze compiler work escapes every work budget, which are per stage and start at Analyze (DLV `ProviderWorkBudgetV1`, "the sole semantic-budget authority"). It also moves the request-domain construction from "before spawn" (DLV:916; RPP `wireRule`) to after a worker frame, and still needs D∅ for the pre-Analyze mismatch path. |
| 2 | **The census as records of an existing fact relation** (`declares`) | Rejected | A fact carries no population assertion: no `examinedPaths`, no completeness, and symbol relations owe no totality (NE:395-407). The census is owed for every symbol cell, including ones that request no `declares`, and a candidate must be a relation the stage requested (DLV `FactCandidateV1.relation`; H1 F3). I1 forbids inferring the census from facts (MI:492), and so does RPS:15. A `declares` scope whose subjects were its own facts would be circular. |
| 2a | **The census as records of an inventory relation** | Rejected | The three inventory relations are `file`, `package` and `vcs-change`, which are source-path or package-name kinds. A symbol inventory relation would be an RPS registry successor, and it would still be facts, not a census. |
| 3 | **The census values committed in the stage spec or request key ahead of execution** | Rejected as values; **adopted as the rule** (LD-F2) | The host cannot extract symbols ("Host does not recompute native symbol rows", ENC:186; SIS:5). The Plan already commits the rule (IE:1464-1465), and D∅ spells it as a key. |
| 3a | A two-phase key with a different request coordinate, H1's (b), the "symbol extent commitment" | Rejected for D∅ | An extent commitment needs a new recipe, or a scope2 whose subjects are paths for a symbol relation, which is the confusion NE:507-515 forbids. D∅ is the same recipe, and it already equals the terminal and pre-Analyze keys. The extent is checked at census admission (ENC:119). |
| 3b | An echo-only rule commitment: the entry keeps the request's D∅ commitment, and `coverage2.scopeId` alone names the census | Rejected | It breaks §4.1a's "Join with scope2" (NE:1917-1922) and IE §3's restatement of it, so it needs an identity-owner successor and a new branch in the product's `inspect_coverage_producer`. It also loses the in-band partition commitment that CB-M1 created. |
| 4 | **The host computes the census from admitted facts** | Rejected | Forbidden: NE:89-91 ("never manufactures symbols"), RPS:15, ENC:186, MI:492, H1 item 9 (H1:332-333). |
| 5 | A census-only first stage, or a second child | Rejected | The keys of every stage are fixed in the one Analyze request. A second child breaks one child per universe (DLV:556-565; ML item 2). |
| 6 | A new frame, or TS3/Rust4 | Rejected | EXC:270; F02:271-273; ML item 1. Not needed: (1) stays inside the majors. |

## Within the current majors

Yes. FA-2 changes no:
- protocol major (2 and 3);
- frame name;
- phase;
- terminal kind;
- transition row (P3T and the TS2 order table name neither payload type);
- limit member (`TypeScriptProtocolLimitsV1` and `ProtocolLimitsV3` are untouched);
- identity token or `identityVersions`;
- `expectedProtocolContractSha256`.

What it adds:
- one optional, non-identity token, echoed under the existing exact-echo rule;
- two payload versions per language, gated by that token.

That is the change NE made for `target-attribution-v2`, with the sentence "Protocol major stays 3 / TypeScript major 2" (NE:2811). F02:271-273's "explicit successor from the owning V1 surface" is this unit.

## What changes

| Kind | Where | Count |
|---|---|---|
| Text passage overrides (line selectors, insert-only) | NE | 13 |
| JSON Pointer string overrides (insert-only) | ST, PST | 3 + 3 |
| Complete JSON successor copies | HS → `design/native/provider-handshake.schemas.v1.json`; PHS → `product/schemas/sources/handshake-v1.schema.json` | 2 (33,812 B, `32aeec8c…`, identical) |
| New schema document | `design/native/symbol-census.schemas.v1.json`, and the product copy `product/schemas/sources/symbol-census-v1.schema.json` | 2 (19,045 B, `95d84054…`, identical) |
| Appended section | NE §9.8 = `section-9-8.md` | 1 |

### The NE overrides

Each `before` is the parent line exactly, as `verify_design` reads it (`splitlines`). Each `after` keeps `before` word for word and only inserts.

| NE line | Where | Inserted |
|---|---|---|
| 93 | header | the census reaches the host only on §9.8's payloads, projected into `SubjectInventoryV1`, never inferred |
| 138 | §0, after its last row | four rows: **A**, DLV `AnalyzeV1`/`CompleteV1` replaced under the token; **B**, RPP `AnalyzeV2`/`CompleteV2` likewise; **C**, the inherited key-commitment rules superseded for every key (LD-F7); **D**, the registered `CapabilityToken` extended for the Hello token arrays |
| 1913 | §4.1a inputs | for a symbol relation `subjects` is the admitted census, and it is empty (D∅) before one |
| 1927 | §4.1a step 1 | "its own enumeration" is, for a symbol key in a TypeScript or Rust universe, the census admitted under §9.8 |
| 2791 | §9.1 token list | `` and `symbol-census-v1` (§9.8)`` |
| 2814 | §9.1 | the token paragraph: optional, non-identity, needed where a census is owed, the payloads, the violation rule, majors unchanged |
| 2884 | §9.2 Rust frame table | `Analyze` and `Complete` rows |
| 2990 | §9.4 | the TypeScript `Analyze` and `Complete` payloads |
| 3235 | §9.7 pre-Analyze conversion | a symbol key's host scope is D∅ |
| 3279 | §9.7 entry attribution | the symbol-key commitment exception |
| 3292 | §9.7 terminal coverage | no census on those terminals; symbol entries keep D∅ with `subjectCount` 0 |
| 3313 | end of §9.7 | appends §9.8 |
| 4195 | §13, after H-7 | join **H-9** with the enumeration and execution-input owners: the census is a host-derived typed input under their ownership law; no foundation document changes |

No other unit binds any of these lines. B-S1's NE lines (714, 719, 730, 731, 822, 824, 863, 931, 939, 940 and 4135) are disjoint.

### The ST and PST overrides

The same three strings are overridden in both copies:
- `/x-opensip-startup-law/coverageFrames/entries`: the symbol-key exception;
- `/x-opensip-startup-law/coverageFrames/terminals`: no census on those terminals; D∅ with `subjectCount` 0;
- `/x-opensip-startup-law/preAnalyzeUnavailable/hostConversion`: a symbol key's host scope is D∅.

### The handshake copies

Each copy is its parent's raw bytes with exactly these edits, in place (`evidence/copies-report.json` lists every hunk):
- `symbol-census-v1` appended last to `TypeScriptCapabilityToken.enum` and `RustCapabilityToken.enum`;
- `TypeScriptCapabilitiesV2.maxItems` 11 → 12 and `RustCapabilitiesV3.maxItems` 13 → 14, since each counts its language's tokens;
- both token descriptions gain one sentence: the token is a member although the registered `CapabilityToken` does not list it;
- `x-opensip-wire-law.supersedes` gains the registered `CapabilityToken`, for the Hello and HelloAck arrays only;
- `x-opensip-wire-law.symbolCensus` is added beside `factBatch`: negotiated, not negotiated, violation, Plan need, majors;
- the document `description` names §9.8.

HS and PHS carry no bound passage override at either lock commit (checked), so nothing is carried.

### The census schema

`symbol-census.schemas.v1.json` (`$id` `opensip.product.symbol-census.1`) publishes these records, closed, in JSON-vector form:
- `SymbolCensusRequestV1`, `SymbolCensusRowV1`, `CompleteSymbolCensusV1`, `OverBoundSymbolCensusV1` and `SymbolCensusV1`;
- `TypeScriptAnalyzeV2`, `AnalyzeV3`, `TypeScriptCompleteV2` and `CompleteV3`;
- the two inherited stage-result records, restated exactly.

Its `x-opensip-symbol-census-law` restates §9.8's joins and names nine internal diagnostic keys. None is a `DomainDetailCode` member.

## Found in passing

- **F-1. The inherited key-commitment rules** conflict with §4.1a for every key (LD-F7). FA-2 closes the gap.
- **F-2. Rust3's request subject cap.** RPP's `planAndDomainProjection.subjectsAlgorithm` puts every non-empty `.rs` snapshot file into `analysisDomain.subjects` and rejects the request before spawn above `maxSubjectsPerStage`. That limit is 256 (RPP:106, RPP:229), retained with an identical value in `ProtocolLimitsV3` and checked by exact equality in Hello (NE:2929-2941; HS `ProtocolLimitsV3.maxSubjectsPerStage` const 256).
  - **Size of the problem.** The T2 manifest records more than 256 Rust files for 9 of its 22 Rust entries. Two of them are S-M medium workloads: `rs-medium-axum` (301) and `rs-medium-tokio` (808). The lead did not recount non-empty `.rs` entries.
  - **Not FA-2's decision.** FA-2 does not change it: a limit change alters the Hello-checked limits map. It is routed to the Rust protocol owner through M3-L (X13, R12; since r3).
- **F-3. C r6 leaves the TS/Rust enumerator implicit** (MC:893). Routed as X-FA2-C.

## Cascade and cross-law items

| ID | For | Item | Gates |
|---|---|---|---|
| **X-FA2-H** | M3-H's next revision (H r2 is being drafted; not edited here) | Item 17's provider leg admits the projected records of §9.8. Item 9's symbol D is the admitted census, or D∅ before one. Item 11's symbol-key pre-Analyze entries are D∅, as H recommended, so the leg H1:377 gates opens. Item 12's bijection reads NE:3279 as amended. H-C17 gains: an over-bound census; one census projected onto two locators with byte-equal rows; a census path outside the extent; a request/return commitment pair from `vectors.json`. | H3's provider leg; H5's symbol-scope legs |
| **X-FA2-I1** | I1-L (accepted) and I1-b2 | No text change. The cycle atom reads retained inventory rows and exact scope subjects (MI:113, MI:155-165), which FA-2 makes producible. H-C19 moves from fixture-level to provider-produced once FA-2, H3 and F2 land. **Limit, disclosed:** `projections: []` means symbol-subject findings have no detector projection (GR6). I1's findings are on `file` subjects, so it is unaffected. | I1 deciding on a real Run |
| **X-FA2-J1** | J1's next revision | J1 r3:192 and J1 r4:207 forbid "any identity on a provider's wire beyond M3L:377's". L item 13 (r4: derived from the schemas by its control L-C1) lists the members the contracts carry, including FA-2's `symbolCensus.enumeratorClosure` under the token. J1 re-cites L's item 13. **Not folded into J1 r4**, which is accepted. | — |
| **X-FA2-E1** | E1 | None. Syntax universes have no child, and E3's census is in-host (H1:515). | — |
| **X-FA2-C** | M3-C's next revision (after r7) | (i) The enumerator of every available TS or Rust binding that owes a symbol inventory is that universe's worker provider closure, which also produces that worker's stages (LD-F6). This rule does not select enumerators for host-derived file/package inventories or for the inventory relations (X-H3, routed to M3-C r8 and CRC-2), and it does not reach syntax universes, which have no child (X-FA2-E1). (ii) Every TS or Rust universe that an expected symbol inventory binds through an available binding has a worker; otherwise that inventory has no producer, and J2b's full join refuses it as `ENUMERATION_INVENTORY_MISSING_RECORD` (ENC:111). (iii) At Plan time the token is a "token the Plan needs" wherever a census is owed. | C4a |
| **X-FA2-D** | M3-D (accepted r3): D2b and D3 | D2b decodes the four payload versions under the token, enforces §9.8's wire refusals and bounds, and builds the Analyze census request and the D∅ request commitments from C4a's Plan. The symbol-key commitment check at the wrapper moves to H at settlement. D3 is unchanged: the census arrives in `Complete` and settles with it. | D2b (day 2) |
| **X-FA2-FG** | F2, G3 and the F4/G2 closure manifests | The emission duty of §9.8: the census in the same compiler pass; rows for every first-party symbol, including those with no fact; every source-side subject of the worker's symbol-kind candidates has a row; no external symbol is a row; scope2 computed with the foundation encoder, conformance-tested on `vectors.json`. Signed capability rows of releases that implement it carry `symbol-census-v1`. | F2, G3 |
| **X-FA2-L** | M3-L (r3, then r4) | L joins FA-2: what crosses the wire, when it is admitted, and how INC treats it. FA-2 accepted is L's gate item G10. | L in effect |
| **X-FA2-P** | M3-PLAN's next revision | FA-2 joins the pre-day-0 law rounds and must be accepted before D2b starts (day 2), as H1 item 25 already says (H1:715). | the day count |

## Lead decisions flagged for the owner

None needs the owner; each has a recommendation. Two are worth knowing:
1. **TypeScript and Rust semantic analysis now needs the new token wherever a symbol census is owed.** That is almost every semantic cell, since nine of the thirteen relations are symbol-kind. A provider release without the token is never spawned for such a Plan. M3's own F2 and G3 releases carry it, so the cost lands only on hypothetical older releases.
2. **No partial census on the wire** (LD-F4). A provider that finds a cycle and then exhausts its budget still cannot decide I1's rule on that Run, which already holds under H1 item 4.

## Evidence and checks

All runs used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`. Nothing ran cargo, a product tool or a test.

**`evidence/build_fa2.py --product <opensip> [--deps DIR] [--check] [--lock-commit SHA]`** rebuilds every generated file of this unit and the subject. It reads the product's `design-lock.json` at `e093e90`, `15c0779` and `cd5958b`, plus one base blob, with `git show`. `--check` compares instead of writing. It restates `verify_design`'s `contract_successor` and `successor_chain` rules for this record:
- every parent is an accepted base at its pinned bytes, at every lock commit;
- every `before` equals its parent line or pointer value;
- line selectors are used only on the Markdown parent;
- no FA-2 selector is already bound, and the copied parents carry no bound override;
- the candidates equal the subject minus the record;
- no candidate path is already accepted.

It also checks each copy: it must parse to its parent with exactly the stated edits, and the two copies must be byte-identical. The product's `schemas/sources/handshake-v1.schema.json` at `e093e90` must equal PHS. The vectors' encoder must reproduce NE's oracle bytes and scope2 before any vector is written.

With `--deps` it validates 14 cases against the new schema using the design encoder's `ExactValidator` (`foundation/canonical.py`, jsonschema 4.25.1 installed offline into a scratch directory). Seven are valid payloads, five are payload refusals, and two check the projected record against SIS (one valid, one refused). All pass.

**Scratch verify (r2).** The product's own `tools/verify_design.py`, read from `cd5958b` with `git show`, was run against the real arch tree, read-only, with a scratch lock: `cd5958b`'s lock (82 contract successors) plus FA-2 r2 appended as the 83rd. FA-2's review and assent are labelled synthetic ACCEPT records that exist only in scratch. The run only redirects the reads of those two paths, and nothing in arch or the product is written. It passes; the log is `reviews/codex-fa-2-r2/scratch-verify.txt`. This shows the record is selectable once accepted. It is not acceptance.

**Design-evidence references (r2, FA2-N1-01).** `native/provider_wire_model.v1.py` and `native/provider_startup_model.v1.py` still load the original handshake and startup schemas. The startup model's `admit_coverage_frame` also compares every entry's `subjectScopeCommitment` with the requested key unconditionally. They are deliberately **not** updated:
- they are neither parents nor members of this unit;
- they are historical design evidence, while FA-2's evidence is its own build script and vectors;
- Codex requested no byte change.

The implementing owners track successor-aware loading and the conditional symbol-key check through clean settlement (X-FA2-D, X-FA2-H), and keep the old no-token refusal controls.

**Not run:** any wire codec. Nothing here exercises a provider, a compiler or a frame.

## Not claimed

- No product, inventory, registry, generated-code or review file is touched.
- No protocol major, frame, phase, terminal, limit member, identity version, `H` domain, relation or public code is added.
- No measurement. The bounds are SIS's and IDS's, cited.
- No decision on F-2 (Rust's 256-subject cap) or on X-H6's scope-limit route.
- No change to H, which is being revised separately. H1 is cited as the source of the obligation only.
