# M3-L r3 — provider-protocol and reuse law

**Verdict: REQUIRED-FINDINGS.** Two findings. RF-1 is the remainder of r2's wire inventory: the later-member ceiling still mis-states payloads the contracts put on the wire. RF-2 is the third delta-round trigger, which treats FA-2's §0 row C as an internal. An ACCEPT would have been "accepted in review" only. The law takes effect only when G1, G4, G5, G9 and G10 are met and S-M's delta round is accepted. Those gate items are open.

Subject: `docs/implementation/m3/provider-protocol-l/PROPOSAL.md`, 121776 bytes, sha256 `6df524a46461b9be784427d48bc821ee05b91c0f6d74d91596567a98c3e20971`. Read against `PROPOSAL-r2.md` (`5bd4025e…`). No cargo, no product build, no test run. The real OpenSIP home is absent. Product main at this review is `cd5958b`.

## RF-1. Item 13's later-member ceiling is still not the cited payloads

The handshake and OpenUniverse halves close r2 RF-1. `TypeScriptHelloV2`, `TypeScriptHelloAckV2`, `HelloV3` and `HelloAckV3` match the handshake schema's required members, including HelloAck's fourteen inherited members plus `identityVersions`. `TypeScriptOpenUniverseV2`, `TypeScriptUniverseAcceptedV2`, `OpenUniverseV3` and `UniverseAcceptedV3` match NE:3166–3189, including `planIntentCommitment`, `providerId`, the universe object, TS `universeKey`, and Rust `repositoryResolution` with `dependencySourceSetId`, `preparedOutputSetId`, `authorizationId` and `effects`. RequestId, RunId and ProjectId stay off both OpenUniverse payloads. FA-2's two members, `symbolCensus.enumeratorClosure` and the census rows' `SubjectIdV1`s, match §9.8.

The same item then says it names every identity-bearing member exactly, and forbids any identity beyond that list (line 547, line 570, line 594). The later-member bullets do not match the payloads they cite.

- Line 556 says candidates and Coverage keys carry `subjectScopeCommitment`, citing `FactCandidateV1` and `CoverageKeyV1`. `CoverageKeyV1` has that field (DLV:804–817). `FactCandidateV1` does not (DLV:770–787). Its anchors do: `AnchorRefV1` carries `snapshotId`, and a fact-ref anchor carries `factId` (DLV:760–766).
- Line 554 says `Analyze` echoes `executionId`, `snapshotId`, `planId` and `universeKey`. `AnalyzeV1` also carries `stageRequests` (DLV:854). Each `StageRequestV1` carries `stageId` (DLV:715–727). Rust `AnalyzeV2` carries `executionId`, `snapshotId`, `planId` and `stages`, and has no `universeKey` field (RPP:405–409). Each stage's `analysisDomain.subjects` carries a `subjectId` (RPP:226–231, RPP:538–542). `FactBatch` and Coverage wrappers carry `stageId` (DLV:855–856; RPP:411–420).
- Line 563 says the custody frames carry `snapshotId`, `dependencySourceSetId` and the prepared set's id. Snapshot payloads carry `snapshotId` (RPP:357–379). `DependencySourceManifest`, `DependencySourceChunk` and `DependencySourceSeal` carry `dependencySourceSetId` and no `snapshotId` (NE:2876–2878). RPP prepared payloads carry `planId` (RPP:381–403).
- Lines 557 and 566 say Cancel, Cancelled and `ProviderFaultV2` echo `executionId`. Those payloads also require `analysisOrdinal` (DLV:860–861; RPP:441–457). `ProviderFaultV2` also requires `phase`.

A ceiling that omits `stageId`, Rust `subjectId` and anchor `factId` forbids members the cited contracts already put on the wire. A sentence that puts `subjectScopeCommitment` on `FactCandidateV1` names a member that payload does not have.

**Fix.** Keep the four correlation identities, the Hello and HelloAck members, the OpenUniverse members, and FA-2's two members. In the later-member bullets, name the identity-bearing members of each cited payload as that payload defines them. `CoverageKeyV1` carries `subjectScopeCommitment`; `FactCandidateV1` carries the universe ids, `producer` and `producerVersion`, and its anchors carry `snapshotId` and, for a fact-ref, `factId`. TS `AnalyzeV1` carries the four echoes and `stageRequests`, and each request carries `stageId`. Rust `AnalyzeV2` carries `executionId`, `snapshotId`, `planId` and `stages`, and each stage's subjects carry `subjectId`. Split the custody sentence by frame family: snapshot frames carry `snapshotId`; dependency-source frames carry `dependencySourceSetId`; prepared frames carry `planId` under the inherited RPP payloads. On Cancel, Cancelled and `ProviderFaultV2`, name `analysisOrdinal` beside `executionId`, and name `phase` on the fault. The prohibition on RequestId, RunId, ProjectId, a log path, a pid and a record key stays.

## RF-2. The third delta-round trigger drops §0 row C

Trigger 3 (line 80) reopens this law when FA-2's acceptance changes what crosses the wire, when the census is admitted, or how reuse treats it. The dependence section (line 150) and the summary table (line 160) then say a change confined to FA-2's §0 rows needs no delta round.

§0 row C is the row that supersedes the inherited key-commitment selectors for every key, with or without the token (FA-2 LD-F7). X15 (lines 848–851) adopts that row, and item 1 (line 251) says that once FA-2 is accepted, "TS2 and Rust3" means NE §9 with FA-2's successor. The commitment a key carries is on the wire: DLV `keyConstruction.subjectScopeCommitment` and `RequestedCoverageDomainV1.workerRule` put one file-set commitment on every key of a stage (DLV:758, DLV:984), and NE:1927–1945 requires each key's own scope2. A Codex change to row C changes that wire value and changes what item 1 and X15 say, and the dependence section records no delta round for it.

**Fix.** Keep schema layout and vectors as internals. A change to §0 row C, or to any other §0 row that changes a wire member, the commitment a key carries, the admission point, or the reuse treatment, takes the third delta round. Say the same thing in the dependence paragraph and in the summary table. Item 10's census sentence follows item 22, so a reuse-treatment change that moves that sentence is part of the same round.

## What holds

r2's three observations are answered. "Review and effect" cites the pinned gate at MC:88–89, and that text is the review-now / accept-when-M3-L-is-accepted rule. Item 9 records (B) and (C) together, and both O3 and O4 arise in that case; (A) is recorded only when neither holds. M3-D r3 is the accepted snapshot `9679dbc4…`. The short name, item 17 and the joins row say so, and the law still cites D by role. R8 is closed on D's constants table: TS2 stage-1 grace 2 s provisional, liveness window 5 s raised to at least 2 × SM-8, TERM to KILL 1 s, reap ceiling 10 s or 5 s under revocation (MD:441–448).

X10's correction is right, and X14's routing is right. J1 r3:192 and the accepted J1 r4:207 both forbid any identity beyond r1:377. r4 is accepted, so the re-citation stays in J1's next revision. r1:377 remains the historical sentence.

Item 1's statement holds. FA-2 adds the optional non-identity token `symbol-census-v1` and one member, `symbolCensus`, on the existing Analyze and Complete payloads. Section 9.8 and the "Within the current majors" record add no frame, phase, terminal, limit member, identity version or major. Protocol major stays 3 and TypeScript major stays 2.

Item 22 joins the proposed carrier. What crosses matches §9.8: under the token, Analyze carries `{enumeratorClosure}` or null, the request commits symbol-kind keys to D∅ before spawn, Complete carries `complete` or `over-bound` and never a truncated census, and BudgetExhausted, Unavailable, Cancelled and ProviderFault carry no census. Admission is D3's clean settlement, atomic with that Analyze's facts and Coverage, in H r1 item 3's order: facts, then the census, then D and Coverage (H1:197–200). The projected inventories are host-derived typed inputs (EXC:259, EXC:265–272). INC-1 and INC-2 bind the current `planId`, `parameterDigest` and `snapshot2`. INC-4 compares census rows like any semantic payload. INC-8 recomputes the census every Run under `host.reuse.disclosed`, with no census-specific event. No accepted interface changes, and this law decides none of FA-2's content.

G10 is a lawful addition to the plan's gate row. `M3-PLAN-r6.md:207` does not list FA-2. This law does not edit that row. It adds G10 as a condition of its own effect, names the rejection of taking effect without a symbol carrier, and routes the recording to the plan's next revision (X9, with H1:715). That is the same pattern as the review rule against `:445` and `:426`.

Item 5's exception is the two producers X-H4 named. E1's syntax stage uses the core provider closure on syntax-universe records only (MC:422–432; ME item 14b). H r1 item 18's inventory derivation produces the file and package inventories and the `file@enumerated` and `package@manifest-declared` facts (NCM:949). In a syntax universe the producer is the core provider closure (MC:424–429). In a TypeScript or Rust universe that leg stays gated until X-H3 is answered (MC:432, MC:453). `TargetAttributionV2` and FA-2's census inventories are projections of an admitted frame. The open-ended substitute, host-produced records in general, stays rejected.

X13 is true on the cited bytes, and leaving it undecided here is right. `subjectsAlgorithm` selects every non-empty `.rs` file and rejects before spawn above `maxSubjectsPerStage` 256 (RPP:106, RPP:226–231). `ProtocolLimitsV3.maxSubjectsPerStage` is const 256 (handshake schema), checked by exact equality in Hello (NE:2929–2941). NE §0 supersedes neither selector. The T2 manifest has 22 entries with a Rust `files` count, and 9 of those counts are over 256, including `rs-medium-axum` at 301 and `rs-medium-tokio` at 808. Both ids are in `counts.rust.medium.devIds`, the seven workloads item 9 uses. The law changes no limit. R12 is the right owner.

X15 is true on the cited bytes. The three inherited selectors give every key of a stage one file-set commitment. NE:1927–1945 requires each key's own scope2, NE:3279 requires the entry to equal the request, and NE:136 makes §4.1a the field's recipe while naming none of the three selectors superseded. FA-2's row C is the resolution, and this law does not decide it.

## Dependence

**O7.** G9 and item 17. No item's protocol text depends on which way O7 is decided. A delta round is needed only if the decision lets a provider execute repository code, needs a new wire signal or member for confinement, or changes item 2 into a resident or pooled helper. Under the lead's recommendation none of those arises.

**S-M.** Item 9 entirely: every `⟨SM-n⟩`, F, T, and every outcome, including (B) and (C) together. Conditionally: O3 on (B), O4 on (C), and both when both outcomes hold; X6 and the D law's liveness floor, sized by SM-8; a TS2 limit question through SM-6, which only a successor can answer; MC's conditional S-R through SM-5 and SM-6. No other item's text depends on the measured values. Items 1 and 2 stay one-shot under every listed outcome.

**FA-2.** G10, and items 1, 13 and 22, which cite the proposed token, the census member, the census-free request commitment, and admission at clean settlement. Item 10's census sentence follows item 22. A delta round is needed if acceptance changes a wire member, the commitment a key carries (including §0 row C), the admission point, or the reuse treatment. Schema layout and vectors need none. Outright rejection leaves item 22 joining nothing, and G10 cannot be met. X13 does not depend on FA-2.

The summary table matches that split, once RF-2 puts row C on the FA-2 delta round. Items 2–8, 11, 12 and 14–21 do not change text under those outcomes. Item 12.4 names SM-8 and states no number.

## Non-blocking observations

**NBO-1.** Item 5 and the ME joins row cite ME:477 for "The crate never mints `fact2`". That sentence is ME:478. ME:477 is the data-document bullet in the same item. The rule is the one ME states.

**NBO-2.** Line 209 says `git diff --name-only e093e90 15c0779` lists none of the product files this law cites. That range includes `design-lock.json`, which line 730 cites as a pin of the register. The other cited product sources (`Cargo.toml`, `providers/rust/src/main.rs`, `crates/contracts/src/generated/protocol.rs`, `schemas/wire/native-carriers-v1.json`, `crates/lifecycle/src/installation.rs`) are unchanged from `e093e90` through current main `cd5958b`. `15c0779..cd5958b` is `design-lock.json` only, the I1-P binding. On the next touch, name that pin base.

**NBO-3.** Item 22.3 invalidates a census on the enumeration class, with configuration and native context. Item 6's other classes include dependency source sets and prepared outputs, and both can change the symbols a worker attests. On the next touch, say the census key covers every class item 6 names, and that per-file dirtiness is never sufficient by itself.
