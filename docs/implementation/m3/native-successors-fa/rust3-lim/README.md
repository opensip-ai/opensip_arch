# RUST3-LIM: the Rust3 request subject list by reference (native contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Status: **PROPOSED frozen candidate.** It needs CODEX2's `ACCEPT-DESIGN-UNIT` and root assent before selection. **It binds after FA-2**, whose handshake copies are its parents.

RUST3-LIM answers M3-L r3's cross-law item **X13**, which L routes to the Rust protocol owner as open question **R12**. Rust3 caps a request's subject list at `maxSubjectsPerStage` = 256, and the list holds every non-empty `.rs` file of the snapshot. So a product Rust provider cannot be spawned for 9 of the 22 Rust-bearing T2 repositories. Those 9 include two of S-M's seven Rust medium workloads, axum and tokio. This unit lets the provider serve a repository up to `snapshot2`'s own bound. It changes no product file, no limit value and no major.

**Base.** Product main `cd5958b` (I1-P bound; 82 contract successors), read-only. FA-2 is in review with Codex. Its r1 returned REQUIRED-FINDINGS on two items: the NE:1927 text and its cascade table. Neither touches its handshake copies, and its r2 is being prepared. **This unit depends only on FA-2's two handshake copies** (`32aeec8c…`, 33,812 bytes), which are the same in FA-2's r1 and its r2 candidate. If a later FA-2 round changes either copy, this unit needs a parent-only rebuild, and `evidence/build_rust3_lim.py` refuses until it gets one. Any other FA-2 change needs nothing here.

## Short names

Every sha256 prefix is the first 8 hex of the exact bytes pinned in `reviews/codex2-rust3-lim-r1/hashes.txt`.

| Name | Document | sha256 |
|---|---|---|
| **L3** | `docs/implementation/m3/provider-protocol-l/PROPOSAL-r3.md`, M3-L r3. These are the bytes at arch `e35272519` that Grok reviewed. Grok returned REQUIRED-FINDINGS (RF-1, item 13's later members; RF-2, FA-2 delta triggers) and confirmed X13's facts (`reviews/grok-provider-protocol-l-r3/REVIEW.md:44`). **Not accepted. Cited as the source of X13/R12, not as authority.** | `6df524a4…` |
| **MC** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r7.md`, M3-C r7, accepted in review by CODEX2 | `a1ee9386…` |
| **M3P** | `docs/implementation/m3/M3-PLAN-r6.md`, accepted | `a6956e88…` |
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md` | `83b99783…` |
| **RPP** | `docs/coop/artifacts/rust-provider-protocol.v2.json`, Rust3's inherited base, pinned by Hello's `expectedProtocolContractSha256` | `6308a98c…` |
| **DLV** | `docs/coop/artifacts/delivery.v2.json`, TS2's inherited base | `47b6cfd1…` |
| **HS** | `docs/coop/design-corrections/native/provider-handshake.schemas.v1.json` (base) | `9090e2ad…` |
| **ST** | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` | `1e35a77b…` |
| **EXC** | `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md` | `22ee2507…` |
| **IDS** | `docs/coop/design-corrections/foundation/identity-schemas.v3.json` | `a76c9e2f…` |
| **FA2** | `docs/implementation/m3/native-successors-fa/fa-2/`: FA-2, in review with Codex (r1 `reviews/codex-fa-2-r1`, REQUIRED-FINDINGS; r2 being prepared). This unit's parents are its two handshake copies, `fa-2/design/native/provider-handshake.schemas.v1.json` and `fa-2/product/schemas/sources/handshake-v1.schema.json`. Its record and subject move between rounds and are read as they stand. **Proposed, not accepted.** | copies `32aeec8c…` |
| **T2M** | `docs/implementation/m3/corpus/t2-corpus-manifest.draft.json` (T2a and T2b accepted by GROK2) | `c8cc48e1…` |

## The facts

### Where the cap lives

The cap is **a protocol constant**. It is not negotiated in Hello, and it is not derived from the frame size, although the frame size interacts with it.

- **The value.** `maxSubjectsPerStage` is 256 in RPP's top-level `limits` (RPP:106). NE §9.3 retains it "with identical values" in `ProtocolLimitsV3` (NE:2934, NE:2936-2941). HS publishes it as `"const": 256` (HS:352-354).
- **The rule.** `planAndDomainProjection.subjectsAlgorithm` (RPP:226-232) works in five steps:
  1. read the sealed manifest;
  2. select every file-kind entry ending in `.rs` with `byteLength` > 0;
  3. sort, and "reject before child spawn if the result is empty or exceeds `maxSubjectsPerStage`" (RPP:229);
  4. emit `SubjectV2` `{subjectOrdinal, subjectId, path, startByte, endByte}`;
  5. give every selected Rust stage "the same exact subjects array".
- **How limits travel.** Limits are not negotiated. `HelloV3.limits` must equal the artifact's map, with exact semantic and deterministic-CBOR equality (RPP:154-159; NE:2939-2941). A "missing, extra, renamed, retyped or changed member refuses Hello before HelloAck" (HS:21). The exact limits map is part of how the major-3 law is identified on the wire (NE:2835; HS:64). For comparison, the Hello-checked stage-1 grace is 5,000 ms (RPP:119).
- **Its neighbours** (RPP:96-121):
  - `maxAnalyzeStages` 256;
  - `maxRequestedCoverageKeysPerStage` 256;
  - `maxRelationsPerStage` 64;
  - `maxSnapshotEntries` 200,000;
  - `maxFramePayloadBytes` 64 MiB;
  - `maxFactCandidatesTotal` 1,000,000;
  - `maxCandidateSpoolBytes` 1 GiB;
  - `maxResponsePayloadBytesTotal` 1 GiB;
  - `maxResponseFrames` 1,000,000;
  - `maxScratchBytes` 2 GiB.
- **History.** RPP v1 had `maxSubjectsPerStage` 1,000,000 (`rust-provider-protocol.v1.json:123`), and v2 lowered it to 256. The v2 adjudication and review files record no reason.
- **Not superseded.** NE §0 supersedes neither the algorithm nor the limit, and FA-2 leaves both alone (FA-2 README F-2).

### What else depends on it

- **Frame size.** `Analyze` is one frame of at most 64 MiB (RPP:97, RPP:168). It carries every selected stage (`AnalyzeV2.stages`, RPP:405-409, at most 256), and each stage repeats the whole inline array.
  - The mean inline row over the 22 entries is **157 to 206 bytes**: exact under source A, estimated under B (`evidence/rust-subject-counts.json`).
  - At 60-byte paths, a 27,000-subject array (`snapshot2`'s descriptor-bound scale) is 5.4 MB per stage, so only 12 stages fit in one frame. A 100,000-subject array is 20.2 MB, so only 3 fit (`evidence/vectors.json` `sizeProjection`).
  - **So raising the constant alone does not work:** the effective bound would depend on the stage count and the path lengths.
  - Even at 256, inline rows with paths longer than about 880 bytes overflow one frame at 256 stages (found in passing, F-1).
- **Memory.** The host builds the array, twice for `independentDerivationRequirement` (RPP:242). The worker decodes it once per stage, out of a frame buffer of up to 64 MiB on each side. Both are O(subjects × stages) today. Under this unit they are O(subjects), with no per-stage copy.
- **Request-key size.** None. Each Coverage key carries a fixed-size `subjectScopeCommitment`: the file-set commitment before FA-2, and §4.1a's per-key scope2 under FA-2's §0 row C. `domainCommitment` is also a fixed-size digest. `maxRequestedCoverageKeysPerStage` does not depend on the subject count.
- **Work budgets.** `deterministicBudget` charges one checked `work-units` increment per `(stage, subjectOrdinal, Coverage entryOrdinal)` tuple (RPP:600-606). A full stage therefore costs subjects × keys work units. Overflow, and every safety bound, is a provider-protocol fault and "cannot manufacture `BudgetExhausted`" (RPP:152).
- **Commitments.** `commitments.subjectScope` and `commitments.analysisDomain` (RPP:210-211) hash the array. Their size is fixed, and their cost is linear in it.

### The counts: non-empty `.rs` files of the 22 Rust-bearing T2 repositories

**All 22 counts are measured. None comes from the manifest alone.** Each is taken at the pinned tree, with nothing fetched (`evidence/count_rust_subjects.py`, output `evidence/rust-subject-counts.json`). The two sources are:
- **Source A**, the E0 probe's bare repositories. It uses `git ls-tree -l` at the pinned commit, after checking that commit's tree against T2M's `gitTree`. It gives exact byte lengths.
- **Source B**, the T2b measurement's per-blob listings. Each listing's commit, tree and QD-22 digest are checked against T2M. A listed `.rs` blob is non-empty exactly when its line count is positive.

Source B covers all 22 entries. Source A covers the nine T2a medium entries, and on each of them it agrees with B.

The counting rule is MC item 6's sealed set (MC:343-346, MC:224): regular files, with symlinks and pruned trees excluded and no `ignorePaths`. No `.rs` path in any of the 22 lies under a pruned segment.

| Entry | Role | Rust class | Non-empty `.rs` | Over 256 | Source |
|---|---|---|---|---|---|
| `poly-small-node-rs` | dev | small | 27 | | B |
| `rs-small-http-body` | dev | small | 27 | | B |
| `rs-small-http` | dev | small | 36 | | B |
| `rs-small-anyhow` | held-out | small | 37 | | B |
| `rs-small-hyper-util` | dev | small | 54 | | B |
| `rs-medium-serde-json` | dev | medium | 71 | | A, B |
| `ts-very-large-vscode` | dev | (TS entry) | 88 | | B |
| `rs-medium-hyper` | dev | medium | 98 | | A, B |
| `rs-medium-ripgrep` | held-out | medium | 110 | | A, B |
| `rs-small-tower` | dev | small | 133 | | B |
| `rs-medium-aws-lambda-rust-runtime` | dev | medium | 192 | | A, B |
| `rs-medium-serde` | dev | medium | 208 | | A, B |
| `poly-medium-napi-rs` | dev | medium | 239 | | A, B |
| **`rs-medium-axum`** | dev | medium | **301** | yes | A, B |
| **`poly-medium-tauri`** | held-out | medium | **327** | yes | A, B |
| **`rs-medium-tokio`** | dev | medium | **808** | yes | A, B |
| **`poly-very-large-deno`** | dev | large | **1,052** | yes | B |
| **`rs-large-smithy-rs`** | dev | large | **1,084** | yes | B |
| **`poly-large-rspack`** | dev | large | **1,384** | yes | B |
| **`rs-large-rust-analyzer`** | held-out | large | **1,483** | yes | B |
| **`rs-very-large-sui`** | dev | very-large | **3,318** | yes | B |
| **`rs-very-large-aws-sdk-rust`** | dev | very-large | **242,187** | yes | B |

- **Agreement with the manifest.** The measured counts equal T2M's `lines.rust.files` in 21 of 22 entries. The exception is rust-analyzer, which has two empty `.rs` files (1,485 → 1,483). L r3 X13's "9 of 22" stands.
- **aws-sdk-rust is beyond every bound here.** It has 242,187 subjects in 245,250 blobs, which exceeds both `snapshot2`'s 100,000 rows and `maxSnapshotEntries`. No protocol change serves it whole. It needs a narrower root or `ignorePaths`, through the scope-limit route (F-5).

## The design in brief

A new optional, non-identity `rust-semantic` capability token, **`subject-scope-reference-v1`**, changes one thing: the element type of the existing `Analyze` payload's `stages` array.
- **What changes.** Under the token each stage is a `StageRequestV3`. Its `analysisDomain` names the subject array by **`RustSubjectScopeV1` `{scopeKind: "nonempty-rs-files", subjectCount, subjectScopeCommitment}`** instead of carrying it inline.
- **Who builds the array.** Host and worker each rebuild it from the `SnapshotManifest` the worker has already accepted, with RPP's own algorithm without the 256 comparison.
- **What stays.** The commitment recipes are unchanged, so `domainCommitment` keeps its value. TS2 already works this way (`delivery.v2` `SubjectScopeV1`, DLV:739-748, "without repeating file rows in Analyze"), and M3-C's S-R makes the same move for `snapshot2`. Here no new identity or retention is needed, because the referenced set is already on the wire.
- **Bounds.** The subject scope is bounded by the manifest (`maxSnapshotEntries`) and, before that, by `snapshot2`'s own bounds. `ProtocolLimitsV3` keeps every member and value.
- **When it is required.** The token is a token the Plan needs exactly when a snapshot has more than 256 subjects.
- **Majors.** No frame, phase, terminal, limit member or value, identity version or major changes.

## Decisions (lead decisions, 2026-10-04)

Each is made under the owner's standing direction to decide on the lead's recommendation and to block only where no recommendation exists. Each names the alternatives it rejects. The owner may reverse any of them. None needs the owner.

### LD-R1. The fix: the subject array by reference, under an optional token

- **Decision.** Candidate 4 below.
- **Why it is the least-cost lawful change:**
  - it is the pattern NE already uses inside the majors (`target-attribution-v2`, NE:2799-2814) and FA-2's;
  - it reuses TS2's own design and RPP's own algorithm and commitments;
  - it changes no limit, so `native-cases.v2.json`'s Hello-limit vectors, `check_native_evidence.v2.py`'s `ProtocolLimitsV3` check (`:480-483`) and the product's generated limit constants all stay valid;
  - it removes the frame-size coupling instead of adding a refusal for it.
- **The test the brief sets:**
  - every bound stays finite and typed (LD-R3);
  - refusals stay typed (LD-R4 to LD-R6);
  - the work budgets are charged per subject (LD-R3).
- **Rejected:** candidates 1, 2, 3, 5, 6 and 7 below.

### LD-R2. The record: per stage, count and commitment only, recipes unchanged

- **Decision.**
  - `StageRequestV3` = `{stageOrdinal, planStage, analysisDomain}`.
  - `StageAnalysisDomainV3` = `{subjectScope, requestedCoverageDomain, domainCommitment}`.
  - `RustSubjectScopeV1` = `{scopeKind, subjectCount, subjectScopeCommitment}`.
  - `subjectScopeCommitment` is RPP `commitments.subjectScope`, and `domainCommitment` is `commitments.analysisDomain` over `{subjects, requestedCoverageDomain}`. Both are computed over the rebuilt array.
  - `stageOrdinal`, `planStage` and `requestedCoverageDomain` are the V2 members, unchanged.
- **Rejected:**
  - **A `snapshotId` in the scope, as DLV's `SubjectScopeV1` has.** `Analyze` already carries it, and every `subjectId` hashes it. A second echo would be a new identity-bearing wire position that L's item 13 would have to list (L3 item 13; Grok's r3 RF-1).
  - **One scope per `Analyze` instead of per stage.** It saves about 140 bytes for each stage after the first, but it makes `StageAnalysisDomainV3` depend on its parent `Analyze`, unlike DLV's per-stage `RequestedCoverageDomainV1`.
  - **New commitment domains.** The recipes and values already exist, and IE:1291-1292 forbids a second recipe for one spelling.

### LD-R3. Bounds: the limits map unchanged, the scope bounded by the manifest

- **Decision.**
  - `ProtocolLimitsV3` keeps all 32 members and values, and Hello still checks it by exact equality.
  - Under the token, `maxSubjectsPerStage` bounds only the historical inline array, which is then never sent.
  - `subjectCount` is at least 1 and at most the accepted `SnapshotSeal.entryCount`, which is at most `maxSnapshotEntries` (200,000). The schema states the bounds `minimum: 1`, `maximum: 200000`.
  - `snapshot2`'s 100,000 rows, its 4 MiB descriptor and its 8 GiB total apply first, at sealing, as the typed `SnapshotBound` (MC item 5).
  - Every response bound and `semanticBudgetSeparation` (RPP:152) is unchanged.
  - `deterministicBudget`'s per-tuple charge is unchanged, so a stage budget still pays for every subject, and its exhaustion is a clean `BudgetExhausted`.
- **Rejected:**
  - **A new limit member such as `maxSubjectScopeCount`.** Tokens add no limit member (NE:2811; FA-2), and adding one changes the Hello map.
  - **Leaving the scope unbounded.** That would fail the brief's test, since the manifest bound must be stated.

### LD-R4. Negotiation: iff the token, for every count

- **Decision.**
  - With the token negotiated, every stage is `StageRequestV3`, whatever the count, including 256 or fewer. The rule holds in `AnalyzeV2` and in FA-2's `AnalyzeV3` alike.
  - Without it, `StageRequestV2` remains.
  - A `StageRequestV3` without the token, or a `StageRequestV2` with it, is `PROVIDER.PROTOCOL_VIOLATION`.
  - The three optional tokens are independent.
- **Rejected:** choosing the shape by subject count within a negotiated session. That would give one negotiated session two request shapes and add a count threshold to the codec.

### LD-R5. When the token is needed (Plan time), and the route without it

- **Decision.**
  - The host knows the count before spawn, from the sealed snapshot.
  - The token is "a token the Plan needs" (NE:2848-2853) for a `rust-semantic` worker exactly when the array is longer than `maxSubjectsPerStage`.
  - A signed row without the token is then never spawned, and the affected keys are `unknown / provider-unavailable`, cause `capability-missing`. That route already exists and is typed.
  - At or below 256, the token is optional.
- **Rejected:**
  - **Needing the token unconditionally.** It would make every token-less release unusable even for small repositories, for no protocol reason.
  - **Splitting the array across stages or children, or truncating it.** That breaks RPP's same-array rule (RPP:231) and one child per universe (L3 item 2), and is forbidden sharding (NE:4280).

### LD-R6. The worker's duty

- **Decision.**
  - After `SnapshotAccepted`, the worker rebuilds the array from the manifest it accepted.
  - Before any analysis, it requires `subjectCount`, `subjectScopeCommitment` and `domainCommitment` of every stage to equal its own recomputation.
  - On a difference it ends with `ProviderFault` `input-rejected` (RPP:445). That is `PROVIDER.PROTOCOL_VIOLATION` with no facts, no Coverage and no Run (NE:3837-3843).
  - This is DLV's worker rule for `SubjectScopeV1` (DLV:758), in Rust3's fault vocabulary.
- **Rejected:** trusting the host's count. A worker that analyzes a domain it cannot reproduce could answer the wrong file set under a matching commitment.

### LD-R7. Form of the successor

- **Decision.** Every passage below is listed by exact path and line under "What changes".
  - **NE:** six insert-only line overrides. One of them appends §9.3a (`section-9-3a.md`) after §9.3.
  - **HS and its product copy:** complete successor copies of **FA-2's** two copies. A token enum append cannot be a pointer override, as I1-L's LD-L1 found.
  - **A new stage-record schema document,** and a byte-identical product copy for D2b.
  - **ST and its product copy:** no override. FA-2 holds the only pointer that names `StageAnalysisDomainV2`.
  - **A reading rule in §9.3a** covers that pointer, EXC:276 and FA-2's `AnalyzeV3.stages` description.
- **Rejected:**
  - **Copying the base HS in parallel with FA-2.** Two "current" handshake schemas would fork, and `verify_design` cannot see the fork.
  - **Editing RPP.** Hello pins its bytes (`expectedProtocolContractSha256`, NE:2819-2822).
  - **Editing the registered `native-evidence.schemas.v2.json`.** Its raw SHA-256 is a registered `payloadSchemaDigest` (NE §10).
  - **Overriding EXC:276 too.** It would widen the parent set for one parenthetical that the reading rule already covers.

### LD-R8. Binding

After acceptance, and after FA-2 is bound, the lead appends this unit's `contractSuccessors` entry to `design-lock.json` in a binding-only product commit, D3's form. Selecting it changes no product byte. D2b copies the handshake candidate, which already contains FA-2's edits, and the new schema source (`materialization-map.json`). Nothing is staged tonight.

### LD-R9. TS2: no change

TS2 has no subject cap. Its requested domain already carries `SubjectScopeV1` by reference: `all-snapshot-files`, a count and a commitment, rebuilt by both sides from the manifest (DLV:739-759). Its ten limits have no subject member (NE:2961-2967). See "The TS2 analogue".

## Candidates evaluated

| # | Change | Verdict | Why |
|---|---|---|---|
| 1 | **Raise `maxSubjectsPerStage` within major 3**, for example to 100,000, and keep the array inline | Rejected | Lawful in form, because the exact limits map identifies the major-3 law (NE:2835), and mismatched peers refuse Hello, typed. But:<br>- the array stays repeated per stage inside one 64 MiB frame, so the real bound depends on the stage count and path lengths (3 stages at 100,000 subjects) and needs a new pre-spawn frame refusal;<br>- every Rust3 peer must change in lockstep;<br>- it invalidates NE's "identical values" (NE:2934), four `native-cases.v2.json` limit vectors, the checker's `ProtocolLimitsV3` check and the generated product constants. |
| 2 | **A token-gated larger cap** with the array inline, in the FA-2 style | Rejected | A token cannot change a value of the exact limits map, so it would need a "read the cap as X" rule, and it keeps candidate 1's frame coupling. |
| 3 | **Chunking the array across existing frames** | Rejected | No existing frame can carry it. `Analyze` is one frame, and one `Analyze` is allowed per child (RPP:89). A new frame name is forbidden inside the majors (EXC:270). Splitting across stages or children breaks RPP:231 and one child per universe. |
| 4 | **The array by reference, under a token** (TS2's `SubjectScopeV1`; MC's S-R) | **Chosen** | See LD-R1. |
| 5 | A Rust4 major | Rejected | A full cascade (F02:271-273; QG DR-G10's "Rust protocol major3"; BP:717; NE §9; L3 item 1), and not needed. |
| 6 | Fold the change into FA-2's `symbol-census-v1` | Rejected | It couples independent features, reopens a unit in review, and would make every census-capable release by-reference-capable and the reverse. |
| 7 | Host-side workarounds: truncation, a subset per stage, or one Plan per 256 files | Rejected | Forbidden (NE:4280; IE:119-120); a partial domain under a complete-looking commitment. |

## Within the current majors

Yes. RUST3-LIM changes none of these:
- a protocol major;
- a frame name, phase, terminal kind or transition row;
- `ProtocolLimitsV3`, in members or values;
- an identity token or `identityVersions`;
- `expectedProtocolContractSha256`;
- a commitment recipe or `H` domain.

It adds:
- one optional, non-identity Rust token, echoed under the existing exact-echo rule;
- one stage-request version under that token.

That is NE's `target-attribution-v2` change, and FA-2's: "Protocol major stays 3" (NE:2811). F02:271-273's "explicit successor from the owning V1 surface" is this unit, and AQP:402's "reviewed successor" is its review.

## What changes

| Kind | Where | Count |
|---|---|---|
| Text passage overrides (line selectors, insert-only) | NE | 6 |
| Complete JSON successor copies | FA-2's `fa-2/design/native/provider-handshake.schemas.v1.json` → `design/native/provider-handshake.schemas.v1.json`; FA-2's `fa-2/product/schemas/sources/handshake-v1.schema.json` → `product/schemas/sources/handshake-v1.schema.json` | 2 (identical bytes) |
| New schema document | `design/native/rust-subject-scope.schemas.v1.json` and the product copy `product/schemas/sources/rust-subject-scope-v1.schema.json` | 2 (identical bytes) |
| Appended section | NE §9.3a = `section-9-3a.md` | 1 |

### The NE overrides: `docs/v2/contracts/product-v1/native-evidence.md`

Each `before` is the parent line exactly, as `verify_design` reads it (`splitlines`). Each `after` keeps `before` word for word and only inserts.

| NE line | Where | Inserted |
|---|---|---|
| 123 | §0, after the Rust `FactBatch` row | Two rows:<br>- **E:** RPP `AnalyzeV2.fields.stages`, `StageRequestV2`, `StageAnalysisDomainV2` and `subjectsAlgorithm[2]`'s cap comparison are retained without the token and replaced by §9.3a's records with it. Everything else in the algorithm, the commitments, `deterministicBudget` and `ProtocolLimitsV3` is retained.<br>- **F:** the registered `CapabilityToken` is extended for the Rust token arrays. |
| 2790 | §9.1 token list | `` optional negotiated `subject-scope-reference-v1` (Rust; §9.3a), `` |
| 2883 | §9.2 Rust frame table, after `FactBatch` | an `Analyze` `stages` row |
| 2942 | end of §9.3 | appends §9.3a |
| 3028 | §9.6 stage correlation | `StageRequestV3` keeps `stageOrdinal` and `planStage` |
| 3070 | §9.6 stage-id echo | `StageRequestV3.planStage.stageId` |

**Conflicts.** None. At `cd5958b` the only bound NE overrides are B-S1's: lines 714, 719, 730, 731, 822, 824, 863, 931, 939, 940 and 4135. FA-2's thirteen are lines 93, 138, 1913, 1927, 2791, 2814, 2884, 2990, 3235, 3279, 3292, 3313 and 4195. All are disjoint from this unit's six, and the build checks this.

**Adjacent lines.**
- **Lines 2790 and 2791.** This unit changes 2790 and FA-2 changes 2791. Together they read: "…, `native-context-v2`, optional negotiated `subject-scope-reference-v1` (Rust; §9.3a), and optional negotiated `target-attribution-v2` and `symbol-census-v1` (§9.8)."
- **Lines 2883 and 2884.** This unit's row follows `FactBatch` (2883), and FA-2's `Analyze` and `Complete` rows follow `CoverageV3` (2884). Both are in the same table, and neither row restates the other.

### The handshake copies

Each copy is FA-2's copy's raw bytes with exactly these edits, in place. `evidence/copies-report.json` lists every hunk.
- `subject-scope-reference-v1` is appended **last** to `RustCapabilityToken.enum`, so no member moves.
- `RustCapabilitiesV3.maxItems` goes from 14 to 15.
- Three strings are extended, insert-only:
  - the document `description`;
  - the `RustCapabilityToken` description;
  - FA-2's `CapabilityToken` entry in `x-opensip-wire-law.supersedes`.
- `x-opensip-wire-law.subjectScope` is added after FA-2's `symbolCensus`. It covers the negotiated and not-negotiated payloads, the violation, the limits, the Plan need and the majors.
- The `TypeScript*` records, `ProtocolLimitsV3`, `HelloV3` and `HelloAckV3` are byte-for-byte unchanged, and the build asserts it.

FA-2's copies carry no bound passage override at `cd5958b`, and no other unit overrides them (checked), so nothing is carried.

### The stage-record schema

`rust-subject-scope.schemas.v1.json` (`$id` `opensip.product.rust-subject-scope.1`) publishes these records, closed, in JSON-vector form:
- `RustSubjectScopeV1`;
- `StageAnalysisDomainV3`;
- `StageRequestV3`.

`planStage` and `requestedCoverageDomain` are named by selector and not restated, as FA-2 does for `StageRequestV2`. Its `x-opensip-subject-scope-law` restates §9.3a and names six internal diagnostic keys. None of them is a `DomainDetailCode` member.

### Consequential passages read through §9.3a's reading rule, not overridden

| Passage | Names | Why not overridden |
|---|---|---|
| ST and its product copy `/x-opensip-startup-law/preAnalyzeUnavailable/hostConversion` | "(coverageDomain.authority; StageAnalysisDomainV2)" | FA-2 overrides that exact pointer, and a second override would conflict. |
| EXC:276 | `StageRequestV2.planStage.stageId` | One parenthetical; the reading rule covers it without widening the parent set. |
| FA-2 `symbol-census.schemas.v1.json` `AnalyzeV3.stages.description` | "StageRequestV2 … Not restated" | A candidate of a unit in review. Its `items` is `{"type": "object"}`, so a `StageRequestV3` validates. |

## FA-2 coordination

- **Order.** This unit's handshake parents are FA-2's candidates, so it binds after FA-2. `verify_scratch.py` shows that this unit alone on the 82-successor lock is refused ("contract parent is not an accepted base or selected inventory"). FA-2 then this unit passes, as 84 successors.
- **Lines.** Disjoint, as above. ST is untouched by this unit.
- **Census members.** There is no wire conflict.
  - `symbolCensus` sits on `Analyze` and `Complete`. This unit changes only the element type of `Analyze.stages`, so the two compose in any combination.
  - FA-2's §0 row C retains `subjects` and `commitments.subjectScope` as "inherited proofs of the sealed file set". Under this token the proof is the same commitment over the rebuilt array.
  - D∅ and the census commitments are per key, so they are unaffected.
- **One interaction to measure.** Lifting the subject cap makes FA-2's census bound the next ceiling for symbol-kind Coverage on large repositories. Above 100,000 rows, 100,000 examined paths or 4 MiB, the census is sent `over-bound`, which takes the scope-limit route (FA-2 LD-F5). S-M measures census rows per subject (SM-13e below).
- **A non-blocking wording note for FA-2.** It does not need to block FA-2. FA-2's NE:2814 sentence "The two optional tokens are independent" stays true of the two it names. §9.3a says the three are independent. If FA-2 takes another round, "The optional tokens are independent of one another" would read better.
- **If Codex changes FA-2's handshake copies,** this unit takes a parent-only rebuild (`build_rust3_lim.py` pins the copies' bytes and refuses on a change) and a re-review of the copies only.

## What S-M must measure

No number in this successor depends on S-M: the bound is structural (`maxSnapshotEntries`, then `snapshot2`). S-M's figures set what the Plan and the provider's budget profile must carry, so that large repositories end in a clean `BudgetExhausted` or the scope-limit route, never in a safety-bound fault. They also set the largest repository the M3 Rust provider is expected to complete.

These are proposed as additions to L's item 9 table, through L's next revision or the S-M delta round (X-RL-L3):

| ID | Figure | Unit | Value |
|---|---|---|---|
| SM-11 | Rust analysis cost per subject: SM-4's time, SM-10's peak RSS and the worker's peak scratch bytes, each divided by the measured subject count | ms/subject; bytes/subject | `⟨SM-11⟩` |
| SM-12 | Rebuilding the subject scope: time and peak memory to derive the array, `commitments.subjectScope` and `domainCommitment` from the accepted manifest, on the host (both independent derivations) and on the worker | ms; bytes | `⟨SM-12⟩` |
| SM-13 | Response volume per subject, per Rust stage: (a) fact candidates, (b) spool bytes under RPP `candidateSpoolAccounting`, (c) response payload bytes, (d) response frames, (e) FA-2 census rows and census CBOR bytes | count/subject; bytes/subject | `⟨SM-13⟩` |
| SM-14 | Work-unit tuples per run: Σ over the workload's Rust stages of subjects × requested keys | work-units | `⟨SM-14⟩` |

**Workloads.**
- L3 item 9's Rust medium dev workloads, axum (301) and tokio (808) included: serde, serde-json, aws-lambda-rust-runtime, hyper, axum, tokio, napi-rs, plus `mr-rs-medium-serde-json`.
- The large dev Rust entries: smithy-rs (1,084), rspack (1,384) and deno (1,052).
- sui (3,318) if S-P permits.
- Held-out entries are excluded, as L3 item 9 requires: tauri, ripgrep, rust-analyzer.

**What they set.**
- The effective subject ceiling of the M3 Rust provider:

  `S_eff = min(snapshot2's admitted rows, ⌊1,000,000 / ⟨SM-13a⟩⌋, ⌊2^30 / ⟨SM-13b⟩⌋, ⌊2^30 / ⟨SM-13c⟩⌋, ⌊1,000,000 / ⟨SM-13d⟩⌋, ⌊2^31 / ⟨SM-11 scratch⟩⌋)`

  It is recorded with the S-M delta round. It is not a protocol constant.
- The Rust stage budget that G's budget profile and C's Plan carry: a `work-units` or `items` limit at or below `⟨SM-14⟩`-derived values, so that the semantic budget exhausts before `maxFactCandidatesTotal` or the spool bound (X-RL-C2, X-RL-G2).
- SM-12 confirms that rebuilding the scope costs nothing material. If it does not, that is a finding for the G and D units, not a reason for a cap.
- SM-13e shows where FA-2's census `over-bound` route starts to bind.

## The TS2 analogue

**TS2 does not have this problem.**
- **The subject set.** It is DLV's `SubjectScopeV1` `{scopeKind: "all-snapshot-files", snapshotId, subjectCount, subjectScopeCommitment}`. Both sides rebuild it from the accepted manifest, "without repeating file rows in Analyze" (DLV:739-748, DLV:957-962).
- **The limits.** `TypeScriptProtocolLimitsV1` has ten members and no subject member (NE:2961-2967). `maxRequestedCoverageKeysPerStage` 128 and `maxAnalyzeStages` 1,024 do not grow with the repository.
- **What bounds a TS repository.** `maxSnapshotEntries` 200,000, which is above `snapshot2`'s 100,000 rows, and `snapshot2` itself (MC item 5).

**What the TS2 limit successor that L anticipates must do.** That is L3's "SM-6 may raise a TS2 limit question" (L3:136, L3:907).
- **It is needed only if both of these hold:**
  - SM-6 shows a TS read set with `node_modules` above 200,000 entries;
  - S-R lifts `snapshot2` above that.

  Until then, `snapshot2` binds first, and the answer is S-R, not a TS2 successor.
- **If it is needed, it must:**
  - change `TypeScriptProtocolLimitsV1.maxSnapshotEntries`, which is an exact-equality change to TS2's limits (candidate 1's form, with no inline array to repeat);
  - and also solve the same single-frame problem found here for the manifest. TS2's `SnapshotManifestV1` is one frame (DLV:850), at roughly 125 bytes plus the path per entry. 200,000 entries reach 64 MiB at average paths of about 210 bytes, and long `node_modules` paths make that plausible. So it needs a chunked or by-reference manifest. That is a frame change unless it is done by reference to bytes the worker already holds.

**Rust3 has the same manifest frame** (`SnapshotManifestV2`, RPP:357-361). Under today's 4 MiB descriptor the manifest stays within about 5.5 MiB in both languages. This is recorded for S-R (F-3; X-RL-C3).

## Found in passing

- **F-1. An inline Analyze can exceed one frame even under the cap.** RPP states no pre-spawn refusal for an `Analyze` over `maxFramePayloadBytes`. At 256 stages × 256 subjects, rows with paths longer than about 880 bytes pass 64 MiB, and IDS `LogicalPath` allows 4,096 characters. Under the token this unit removes the subject term. The residual `Analyze` is at most 256 stages × (`planStage` + at most 256 keys). The token-absent path keeps the gap. **For:** the Rust protocol owner and D2b, as a host invariant refused before spawn.
- **F-2. The empty-subject refusal is untyped.** RPP:229 "reject[s] before child spawn if the result is empty" and names no route. It is unchanged here. **For:** the Rust protocol owner.
- **F-3. The `SnapshotManifest` is one frame in both protocols.** Under `snapshot2`'s 4 MiB descriptor it is at most about 5.5 MiB, because a manifest entry is at most about 1.36 times its inventory row. S-R would make the 64 MiB frame the binding bound: about 280,000 to 380,000 entries at 40- to 100-byte paths, and about 16,000 at 4,096-byte paths. **For:** C's S-R, and TS2's limit successor.
- **F-4. Lifting the cap exposes the response safety bounds.** These are `maxFactCandidatesTotal` 1,000,000, the spool's 1 GiB, the response's 1 GiB and `maxResponseFrames` 1,000,000. They fault and never become `BudgetExhausted` (RPP:152). With at most 256 files they were out of practical reach. **For:** C's Plan budgets and G's budget profile (X-RL-C2, X-RL-G2), sized by SM-13.
- **F-5. aws-sdk-rust exceeds `snapshot2` and `maxSnapshotEntries`.** It has 242,187 subjects. No protocol successor serves it whole. It takes the snapshot bound's typed refusal and the S-B scope-limit remedy (MC item 5).
- **F-6. L3 item 13 and Grok's r3 RF-1.** Rust `Analyze` `subjectId` is an identity-bearing wire member only when this token is absent. Under the token, stages carry `subjectScope`, which holds no identity (X-RL-L2).

## Cascade and cross-law items

| ID | For | Item | Gates |
|---|---|---|---|
| **X-RL-L1** | M3-L's next revision (r4 is being drafted) | X13 and R12 are answered by this unit. Item 1 names RUST3-LIM beside FA-2 as a native successor that M3's protocols include, and item 1's forbidden substitute "FA-2's census member … is the one member M3 adds" becomes "the members FA-2 and RUST3-LIM add". **Recommended: add G11, "RUST3-LIM accepted",** for the reason G10 has: L in effect fixes Rust3 for M3, and without this unit it fixes a Rust3 that refuses two of S-M's seven Rust medium workloads and nine of the 22 T2 Rust entries before spawn. "Not in this gate" (L3:125) then drops X13. | L in effect |
| **X-RL-L2** | M3-L item 13 (Grok r3 RF-1's fix) | Rust `AnalyzeV2` stages carry `subjectId` only without `subject-scope-reference-v1`. Under the token, each stage carries `analysisDomain.subjectScope` `{scopeKind, subjectCount, subjectScopeCommitment}`, which holds no identity. No new identity position is added (LD-R2). | — |
| **X-RL-L3** | M3-L item 9 and the S-M run set | Add SM-11 to SM-14 and the large Rust workloads above. | S-M |
| **X-RL-FA2** | FA-2 | Binds before this unit. Optional wording at NE:2814 ("The optional tokens are independent of one another"). If FA-2's handshake copies change, this unit takes a parent-only rebuild. | binding order |
| **X-RL-C1** | M3-C's next revision (after r7) | At Plan time, `subject-scope-reference-v1` is a token the Plan needs for a Rust worker whose snapshot has more than `maxSubjectsPerStage` non-empty `.rs` files (C4a; NE:2848-2853). | C4a |
| **X-RL-C2** | M3-C's next revision | Rust stages should carry a semantic stage budget (C-2 `StageBudgetV1`, `work-units` or `items`) sized from SM-13 and SM-14, so that a large repository ends in `BudgetExhausted`, not in a safety-bound fault (F-4). | C4a, after S-M |
| **X-RL-C3** | S-R, when drafted | S-R's referenced-inventory bounds must keep each protocol's one-frame `SnapshotManifest` within `maxFramePayloadBytes`, or name its typed pre-spawn refusal (F-3). | S-R |
| **X-RL-D** | M3-D (accepted r3): D2b | Decode and encode `StageRequestV3` under the token. Build `RustSubjectScopeV1` with the host analysis-domain constructor, refuse the token and shape mismatch, and keep the token-absent inline path, closing F-1 on it. D3 is unchanged. | D2b |
| **X-RL-G1** | M3-G: G1a, G3 | **G1a:** rebuild the array after `SnapshotAccepted` and verify count and commitments before analysis (LD-R6), conformance-tested on `evidence/vectors.json`. **G3:** signed capability rows of releases that implement it carry `subject-scope-reference-v1`. | G1a, G3 |
| **X-RL-G2** | M3-G: budget profile | The Rust provider's default stage budget follows X-RL-C2. | G3 |
| **X-RL-F** | M3-F | None. TS2 already names its file set by reference (LD-R9). | — |
| **X-RL-H** | M3-H | None. Admission, Coverage and census law are unchanged. | — |
| **X-RL-P** | M3-PLAN's next revision | RUST3-LIM joins the pre-day-0 native successors beside FA-2, and is accepted before D2b and G1a start. | the day count |

## Lead decisions flagged for the owner

None needs the owner. Two are worth knowing:
1. **A Rust release without the new token can still serve repositories of 256 subject files or fewer,** but never more. M3's own G releases carry the token, so the cost lands only on hypothetical older releases.
2. **Lifting the cap moves the practical ceiling to the response bounds and the stage budget.** S-M measures where that ceiling is (SM-13). If it is below a repository the owner's team needs, the remedy is a scope (`ignorePaths`, a narrower root), not a protocol cap.

## Evidence and checks

All runs used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`. Nothing ran cargo, a product build, a test or a provider, and nothing was fetched.

**`evidence/build_rust3_lim.py --product <opensip> [--deps DIR] [--check] [--lock-commit SHA]`** rebuilds every generated file of this unit and the subject. It reads the product's `design-lock.json` and one base blob at `cd5958b` with `git show`. `--check` compares instead of writing. It restates `verify_design`'s `contract_successor` and `successor_chain` rules for this record, with FA-2 emulated as bound next, as its record and subject currently stand (the build output names their shas):
- every parent is accepted at its pinned bytes, FA-2's copies only once FA-2 is bound;
- every `before` equals its parent line, and every `after` is a single insertion;
- line selectors are used only on the Markdown parent;
- no selector is already bound, FA-2's thirteen included;
- the copied parents carry no bound override;
- the candidates equal the subject minus the record;
- no candidate path is already accepted.

**Other checks in the build:**
- **The copies.** Each copy must parse to its parent with exactly the stated edits, the two copies must be byte-identical, and every TS and limits record must be unchanged. The product's `schemas/sources/handshake-v1.schema.json` at `cd5958b` must equal the selected base copy.
- **The counts.** `rust-subject-counts.json` must reproduce from the E0 trees and the T2b listings, when they exist on the machine.
- **The vectors.** They are built with an independent encoder of RPP `canonicalCbor`, with length-first map-key order. They show:
  - the rebuilt array equals the inline algorithm's under the cap;
  - `domainCommitment` is equal across `StageRequestV2` and `StageRequestV3`;
  - the worker's rebuild reproduces count and commitments;
  - the refusal cases and the size projection.
- **The schema cases.** With `--deps` (jsonschema 4.25.1, offline), it validates 11 cases against the new schema using the design encoder's `ExactValidator`: 3 valid and 8 refused. All pass.

**`evidence/count_rust_subjects.py [--check]`** recounts all 22 entries (above).

**`evidence/verify_scratch.py [PRODUCT] [--rev cd5958b]`** runs the product's **real** `tools/verify_design.py` over the lock with FA-2 and then RUST3-LIM appended. The reviews and assents are synthetic and held in memory; nothing is written. It asserts:
- the base lock passes (82);
- this unit alone is refused, for FA-2's parents;
- FA-2 passes (83);
- FA-2 then this unit passes (84), with six passage overrides;
- the selected inventory and the inheritance projection are unchanged;
- no bound successor, FA-2 included, overrides any of this unit's selectors.

It passed in both modes: the checkout `cd5958b`, with generation and admission sources, and `--rev cd5958b`, design only.

## Not claimed

- No product, inventory, registry, generated-code or review file is touched.
- No protocol major, frame, phase, terminal, limit member or value, identity version, `H` domain, relation or public code is added.
- No measurement of analysis cost. The counts are file counts at pinned trees. Every cost figure is a placeholder `⟨SM-n⟩`.
- No decision on F-1 to F-5's owners' questions, on S-R, or on L's gate (X-RL-L1 is a recommendation).
- No change to FA-2, L, C or H, which are being revised separately.
