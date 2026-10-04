# Fact admission — proposal M3-H r3

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Law for unit **M3-H** of the accepted M3 unit plan (M3P:216). It fixes H's scope, its joins, its hand-off to J2 and its code units H1 to H5.

**Draft r3, not accepted. Not code.** This law touches no product file. H's code units wait for P0, for the codec and supervisor units they consume (D2b, D3) and for the gates in item 25.

**History.** r1 (`PROPOSAL-r1.md`, sha256 `69f50bb1…`, 88,004 bytes) was reviewed by Grok (`reviews/grok-fact-admission-h-r1`). The verdict was REQUIRED-FINDINGS, with one required finding (RF-1) and two non-blocking observations (NBO-1 and NBO-2). r2 answers all three.

In r2, while answering RF-1 and NBO-1, the drafter found that item 10's direct call disagreed with the owner it cites. Item 10 was rebuilt on the same owner call as item 14 (see the r2 table).

r2 (`PROPOSAL-r2.md`, sha256 `4ae48f09…`, 106,667 bytes) was reviewed by Grok (`reviews/grok-fact-admission-h-r2`). The verdict was REQUIRED-FINDINGS, with one required finding (RF-1, the internal consistency of the routing) and three non-blocking observations. Grok accepted r2's routing idea. r3 answers all four findings and changes nothing else of substance.

**Standings.** This law pins only accepted snapshots of other laws, never a live `PROPOSAL.md`.
- **Accepted and pinned:**
  - M3-PLAN r6;
  - M3-C r7, accepted in review by CODEX2. It takes effect once M3-L is accepted. r7 narrowed item 16 row 8 and changed nothing H cites; every MC line was re-mapped from r6 to r7 (r3);
  - M3-D r3 (GROK2);
  - M3-J1 r4 (GROK2), which adds R10a;
  - M3-E1 r3, M3-I1 r2, M3-B r2 and X5 r3.
- **M3-L has no accepted snapshot.** r2 received required findings, and r3 is in review (X-H4). FA-2 is drafted as a design unit and is in review with Codex (X-H1). H depends on neither. H takes no rule from M3-L. Each interface r1 cited L for is now cited to the contract text L itself cites. L's own words appear only as the object of X-H1 and X-H4, through r1's frozen bytes (ML1).

**Lead decisions.** Every item marked "lead decision" is dated 2026-10-04. It is made under the owner's standing direction to decide on the lead's recommendation and to block only where no recommendation exists. Each one names the alternatives it rejects, and the owner may reverse any of them. Items marked "law" state what the accepted contracts already require of H, and items marked "record" change nothing. No item needs an owner decision to proceed.

Six cross-law items, X-H1 to X-H6, name the law that must change. None blocks this law's acceptance. Item 25 says which code legs each one gates.

## r3 changes and review responses

| Finding | Change |
|---|---|
| **RF-1** (one route) | **Lead direction: one authority.**<br>- **One table.** Item 14.4's table is now the **only** routing authority for view-join keys. Items 5 (F10), 10, 11, 16 and 22 refer to it and restate none of it. Removed: item 22's producer-claim row, item 10's "row 30 or 32" sentence, and item 22's blanket host-invariant routing of item 11.<br>- **Anchors.** On a provider-return view, the three anchor keys take MJ row 30 only. Row 32 is the Coverage cause and carrier row, not an anchor row.<br>- **Coverage claim keys** on a provider-return view:<br>  - the prerequisite and totality keys take MJ row 32, the row for a Coverage cause, carrier or contradictory completeness (MJ:678);<br>  - `COVERAGE_PRODUCER_ADMISSION` takes row 32 or row 30 by its causes, under 14.4a's tie rule.<br>- **Origin.** Item 11 is retitled. The provider's own terminal Coverage is provider-return origin (item 14.1). Only the pre-Analyze conversion is host-minted. Item 22's host-minted row now names "item 11's pre-Analyze conversion, item 16 and item 18".<br>- **Key matching.** Keys are matched by their prefix token, the text before the first `:`, because the owner appends suffixes (`view_joins.rs:352-357`, `:429-431`, `:526-530`). The catch-all applies only when no listed token matches.<br>- **New control H-C25** tests the router directly: item 11's two cases on their two routes, suffixed keys on their listed rows, and the tie rule. |
| **NBO-1** | F7 and item 14.5 now cite DLV:972-975, the key-construction rule that leaves `FACT_SCOPE_JOIN` reachable only through H's assembly. |
| **NBO-2** | Product main is `cd5958b` (I1-P). Since `3e64266`, its crates differ only in X4-F1's ten `crates/security` trust and custody files (`15c0779`), which this law does not cite. Every pinned product file is byte-identical to `3e64266`. |
| **NBO-3** | 14.4a: row 32 when any row-32 cause is present, otherwise row 30. The two rows share the public termination, so the rule fixes only the recorded condition. |
| Context | - **M3-C r7** was accepted (CODEX2, `a1ee9386…`). MC is now cited by `PROPOSAL-r7.md`, re-mapped line by line from r6. r7 changes only item 16 row 8, which H does not cite.<br>- **The successor** for X-H3 is renamed "M3-C r8 / CRC-2", because r7 did not take X-H3 up. |

## r2 changes and review responses

| Finding | Change |
|---|---|
| **RF-1** (the anchor checks) | **Lead decision: keep the owner and fix the routing.**<br>- **Where the anchor bytes are checked.** `ANCHOR_SOURCE`, `ANCHOR_RANGE` and `ANCHOR_UTF8` now run once, in item 14's call of `inspect_plan_view_joins` over the **provisional view**. That is the view H builds from the return's candidates in a staging overlay, before anything joins the return's admitted set (item 14.2). That function is their only owner, and it reads anchors from a view (`view_joins.rs:212-223`, `:388-407`). No host copy of the anchor law is added (item 5).<br>- **F5** keeps only the anchor count. It is checked inside F4's identity call, which reports `anchor cardinality` (`relations.rs:334-341`).<br>- **F4 and F6** run on `inspect_relation_snapshot`, which calls `inspect_relation_payload` first (`closure.rs:329-338`, `:417-497`). H keeps the owner's `RelationRule` text as the key. r1's `FACT_ANCHOR_CARDINALITY` is withdrawn: it is IE prose (IE:1038), not a runtime key.<br>- **The routing rule (item 14.4).** Every view has one origin.<br>  - A key that judges a producer's claim (the three anchor keys; the Coverage producer, prerequisite and totality keys) takes MJ row 30 or 32 on a provider-return view. On a host-minted view it takes the host-invariant row; host-minted views are E3's syntax stage, item 11's pre-Analyze conversion and item 18's inventory stage.<br>  - A key that judges H's own assembly (`FACT_SOURCE_PRODUCER_JOIN`, `FACT_SCOPE_JOIN`, the partition overlap and the rest) is a host invariant, MJ row 29's codes, whatever the origin.<br>- **F3** now checks the `(relation, rung)` pair, so that F3 and F7 together leave `FACT_SCOPE_JOIN` reachable only through H's assembly.<br>- **Item 5** routes its refusals to MJ row 30 for provider returns only. **Item 16** keeps every refusal of an E3 record host-internal, the anchor keys included.<br>- **New control H-C24** discriminates the three anchor failures on a provider fact (row 30) from the same failures on an E3 syntax fact (host invariant). H-C6, H-C14 and item 22 follow. |
| **Found while answering NBO-1** (item 10's producer call) | r1's item 10 called `inspect_coverage_producer` directly. It used a per-Analyze census and the reference model's `languageVersionBinding.dialect`. The product owner differs on both:<br>- RC-2's census is "the admitted `unresolved-edge` facts of the **view**" (IE:1481; NE:3351, NE:3474). The owner's view join builds exactly that (`view_joins.rs:450-466`).<br>- The product's `universe_dialect` is a `{table}` derived from the retained universe frame (`view_joins.rs:470-479`; `coverage.rs:290-303`). The function that builds it is crate-private to the evaluator (`capability_support.rs:279`).<br>**Lead decision:** item 10 no longer calls the inspector. H builds D and the provisional `coverage2` and names them in the provisional view. The owner's view-join call then runs the producer check, the identity check, the prerequisites and Coverage totality (`view_joins.rs:434-532`). That is the same composition Run closure re-runs. H-C9 and H-C10 become source pins that H passes no census and no dialect. |
| **NBO-1** (the census slice) | Item 10 now states it plainly. `CoverageProducerInput.unresolved` is a caller-supplied slice (`coverage.rs:28-36`), and the inspector cannot prove it complete (`coverage.rs:21-22`). On H's path its only caller is the owner's view join, which builds it from the `unresolved-edge` facts the provisional view names (`view_joins.rs:450-466`). Those are host-held values: facts H admitted at F1 to F9 and put in the view. No census is ever taken from a provider or from a caller of H. The child module is named `fact_admission/coverage.rs` wherever it is meant. |
| **NBO-2** (later drafts) | J1 is now accepted at r4 (GROK2, `c18c0d3c…`).<br>- **MJ** is cited by `host-pipeline-j/PROPOSAL-r4.md` lines: J-η is MJ:377 and J2b is MJ:785. The outcome-matrix row numbers are unchanged.<br>- **Every other law** is now cited by its accepted snapshot, not its live file. M3P, ME, MI, MB, AQP, OPP and X5 lines are re-pinned. Each of those live files differs from its snapshot only by its acceptance note, so the re-pin is mechanical. J1's r3-to-r4 change moved lines, and every MJ citation was re-mapped against r4's bytes. Every re-pinned line was checked to carry the same text it did in r1.<br>- **M3-C** stays on r6. r7's narrowing of row 8 is noted where it could touch H (item 8). |
| Context | - **Product.** Main is `9c11c53` (B-S1), after `0ceb9ad` (I1-L). Neither changes a crate: `git diff --stat 3e64266 9c11c53 -- crates` is empty, so every cited product line is as r1 read it.<br>- **FA-2 and M3-L r3** are being drafted (X-H1, X-H4). This law keeps both items and depends on none of their details.<br>- **M3-L citations** are re-sourced to the contracts L cites (DLV, NE, AQP and OPP). |

## Short names

Lines were checked against the files named here on 2026-10-04. Each sha256 prefix is the first 8 hex of the exact file pinned in this law's review request (`reviews/grok-fact-admission-h-r3/hashes.txt`).

| Name | Document | Standing | sha256 |
|---|---|---|---|
| **M3P** | `docs/implementation/m3/M3-PLAN-r6.md` | M3-PLAN r6, accepted bytes | `a6956e88…` |
| **MC** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r7.md` | M3-C r7 bytes, accepted in review by CODEX2 (`reviews/codex2-snapshot-plan-c-r7`) | `a1ee9386…` |
| **ME** | `docs/implementation/m3/syntax-e/PROPOSAL-r3.md` | M3-E1 r3, accepted bytes | `d71031ff…` |
| **MI / MIU** | `docs/implementation/m3/preview-pack-i1/{PROPOSAL-r2,UNITS-r2}.md` | M3-I1 r2, accepted bytes | `1eb47d1e…` / `0c3c0f44…` |
| **MJ** | `docs/implementation/m3/host-pipeline-j/PROPOSAL-r4.md` | M3-J1 r4, accepted bytes (GROK2, `reviews/grok2-host-pipeline-j-r4`) | `c18c0d3c…` |
| **ML1** | `docs/implementation/m3/provider-protocol-l/PROPOSAL-r1.md` | M3-L r1, frozen and never sent. **Not accepted, and not authority.** M3-L has no accepted snapshot. These bytes are cited only as the object of X-H1 and X-H4 | `5e858c05…` |
| **MB** | `docs/implementation/m3/config-discovery-b/PROPOSAL-r2.md` | M3-B r2, accepted bytes | `92e65825…` |
| **MD** | `docs/implementation/m3/supervisor-d/PROPOSAL-r3.md` | M3-D r3, accepted bytes (GROK2, `reviews/grok2-supervisor-d-r3`) | `9679dbc4…` |
| **AQP** | `docs/implementation/m3/analysis-quality/PLAN-r6.md` | r6, accepted bytes | `8aed6eb8…` |
| **OPP** | `docs/implementation/m3/operability/PLAN-r3.md` | r3, accepted bytes; cited by section and line | `b49035f2…` |
| **X5** | `docs/implementation/m2/replay-join-x5/PROPOSAL-r3.md` | X5 r3, accepted bytes | `d9a101b8…` |
| **REG** | `docs/v2/architecture/08-decision-and-readiness-register.md` | contract | `de21a7e0…` |
| **CH14** | `docs/v2/architecture/14-repository-and-module-layout.md` | contract | `c7b10bf6…` |
| **BP** | `docs/v2/architecture/implementation-boundaries-and-build-plan.md` | contract | `8e6e8bab…` |
| **COV** | `docs/v2/architecture/implementation-coverage.v1.json` | contract | `753f220e…` |
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md` | contract | `83b99783…` |
| **IE** | `docs/v2/contracts/product-v1/identity-and-evidence.md` | contract | `c82404f3…` |
| **ENC** | `docs/coop/design-corrections/foundation/enumeration-contract.v1.md` | incorporated contract | `b7858bc8…` |
| **EXC** | `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md` | incorporated contract | `22ee2507…` |
| **ATOM** | `docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md` | incorporated contract | `8649b8b0…` |
| **FAULT** | `docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md` | incorporated contract | `5731b41d…` |
| **SIS** | `docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json` | schema | `6ab46925…` |
| **IDS** | `docs/coop/design-corrections/foundation/identity-schemas.v3.json` | schema | `a76c9e2f…` |
| **RPS** | `docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json` | schema | `53380a24…` |
| **EPLAN** | `docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json` | schema | `10627cb6…` |
| **NCM** | `docs/coop/design-corrections/native/native-capability-matrix.v2.json` | matrix | `4b1c19b0…` |
| **NEM** | `docs/coop/design-corrections/native/native_evidence_model.v2.py` | reference model | `7d1c0acf…` |
| **PWM** | `docs/coop/design-corrections/native/provider_wire_model.v1.py` | reference model | `a2a8b9d1…` |
| **DLV** | `docs/coop/artifacts/delivery.v2.json` | TS2's inherited base | `47b6cfd1…` |
| **RPP** | `docs/coop/artifacts/rust-provider-protocol.v2.json` | Rust3's inherited base | `6308a98c…` |

Product paths are under `opensip/` at main `cd5958b`. They were read, not run. Since `3e64266`, the crates differ only in X4-F1's ten `crates/security` trust and custody files (`15c0779`), and this law cites none of them. Every cited product file is byte-identical to `3e64266`, so every cited line reads as r1 read it. The pin base is `3e64266`'s bytes, and the files are pinned in `hashes.txt`.

## Acceptance gate

This law may be reviewed and accepted now.
- **It launches nothing and spawns nothing.** H is pure host code over retained records (item 23), so O7 is not a gate item (M3P:474-485).
- **It relies on no draft.** D3's clean-settlement gate is the accepted M3-D r3's (MD:618-633). "TS2 and Rust3 unchanged" is INC-5 (AQP:400) and NE §9 (NE:2781-3316), not an M3-L rule. Item 25 holds each H code unit until what it uses is accepted and integrated.
- **Its cross-law items gate code legs, not acceptance.** X-H1 to X-H6 are routed to the native owner, to M3-C's next revision, to M3-L's next revision and to M3P's next revision. Item 25 and "Cross-law items" say which leg each one holds.
- **M3P:259 assumes the H law is accepted before day 0.** E1 builds E3 against "the accepted H law's syntax-join interface" (ME:712, ME:714). Item 16 is that interface.

## Problem

**What exists at main `cd5958b`** (every file cited below is byte-identical to `3e64266`).
- **`fact_admission.rs` is X5's replay join and nothing else** (`crates/host/src/fact_admission.rs:1-17`, `:93-102`). Its header says "The M3 syntax, context, occupancy and Coverage joins arrive in this module" (`:2-3`).
  - The module is `#[allow(dead_code)]` with one caller, X7a (`crates/host/src/lib.rs:44-47`).
  - X5's source pin forbids a second `opensip_evaluator` import, any `inspect_`, `derive_evaluation`, `check_plan_pack`, `Clone`, `Default` and every I/O name in that file (`fact_admission_tests.rs:651-700`; X5:141).
- **The evaluator already owns the Run-closure halves of most of H's laws.** Each is a pure, local check over retained records:
  - `inspect_coverage_producer` (`crates/evaluator/src/coverage.rs:305-455`) runs NE §4.1a's steps 2 to 6, the RC bijection, the cause-carrier registry and the source-variant guard. It then mints `coverage2`. But it "cannot establish that the observation census is complete or Plan-bound" (`coverage.rs:21-22`), and it takes the scope and the census as arguments. Its product caller is the view join, which supplies the census and the dialect table from the view and its universe frame (`view_joins.rs:450-491`).
  - `inspect_syntax_fact` (`capability_support.rs:219-277`) and `inspect_coverage_prerequisites` (`:376-381`).
  - `inspect_plan_view_joins` (`view_joins.rs:212-223`) checks a view's scopes, facts and anchors (`FACT_SOURCE_PRODUCER_JOIN`, `FACT_SCOPE_JOIN`, `ANCHOR_SOURCE`, `ANCHOR_RANGE`, `ANCHOR_UTF8`; `view_joins.rs:366-407`). It then runs the Coverage producer check, the prerequisites and Coverage totality for every Coverage the view names (`view_joins.rs:434-532`). It is the only owner of the anchor byte checks.
  - The identity crate's `inspect_relation_snapshot` and `inspect_relation_payload` apply the relation payload rules, the anchor count and the `file` snapshot joins, and report `RelationRule` text (`crates/identity/src/closure.rs:329-338`, `:417-497`; `relations.rs:325-391`). The closure walk fixes `fact.producerClosure` to kind `provider` (`closure.rs:164`).
  - `inspect_enumeration_join` (`enumeration_join.rs:1329-1341`) is ENC's join over retained inventories. `derive_evaluation` re-runs it in reconstruction (`composition.rs:1081-1099`; `input_reconstruction.rs:439-459`).
- **No producer-boundary owner exists.** Nothing in the product does any of these:
  - builds the subject-scope descriptor D from the host's own enumeration (NE:1927-1928);
  - decodes a relation payload from deterministic CBOR into `C` (`crates/identity/src/capability_codec.rs:1-2` is "not … relation payload CBOR");
  - mints `fact2`, `coverage2` or `view2` from a provider return;
  - projects `TargetAttributionV2` from `OccupancyCompanionV1`. The evaluator only reads target-attribution refs (`execution_inputs.rs`; `input_reconstruction.rs`).
- **No provider, codec, supervisor or syntax crate exists yet** (M3P:208; MD:1143-1144; ME:5).

**What the accepted record asks of H.**
- **M3P:216.** The syntax, context, occupancy and Coverage joins; relation-registry and Coverage-domain refusals (REG:368); a missing rung is indeterminate (REG:370); framing grants no fact authority (CH14:482). H admits what I1-b2 reads (MI item 8). The full `admit_enumeration` runs in J2's pipeline with H's admission (MC:880, MC:892-896).
- **BP:680-683.** "`host/fact_admission.rs` checks source/context, occupancy, relation-at-rung and Coverage joins before ordinary evaluation."
- **COV** routes DR-G23 (COV:5004) and DR-G25 (COV:5056) to `fact_admission.rs`, with `replay.rs` and `outcomes.rs` respectively. It routes NE §4, "Resolution completeness", which is COV's `native-evidence:5` (COV:7144). It also names `fact_admission.rs` as a co-owner of every one of the 60 non-`inventory` capability cells (COV:2077-4425).
- **G23 and G25 are prepared at M3, not qualified.** Their qualification milestone is M6 (COV:5004, COV:5056; BP:1027, BP:1029).

**Six gaps.**
- **G1. No producer-boundary admission.** DR-G23's required evidence is "FactCandidate relation-registry refusal before fact admission; Coverage-domain mutation refusal; no unknown-to-covered conversion" (REG:368). Nothing implements it.
- **G2. No owner of missing-rung typing at admission** (REG:370; AQP:113).
- **G3. No occupancy capture** (NE:3009-3150).
- **G4. A provider's symbol census has no carrier.** I1's rule cannot pass or fail on a real TypeScript Run without one (item 17; X-H1).
- **G5. Clean non-Complete terminals contradict each other.** NE admits "facts before the terminal". DLV and RPP discard all candidates. MD hands that choice to H (MD:623, MD:1107; item 4; X-H2).
- **G6. No owner and no lawful producer for host-produced inventory records** in TypeScript and Rust universes (item 18; X-H3, X-H5).

## Decisions at a glance

| # | Decision | Rejected |
|---|---|---|
| 1 | **Scope.** H admits provider returns, the in-host syntax stage's outputs, provider symbol censuses, the host's own inventory records and the host's Coverage conversions. It does not own decoding, settlement, D9 projection, candidate envelopes, receipts, the full enumeration call, evaluation or replay. | H projecting D9 terminations; H admitting `clones-near` envelopes |
| 2 | **Layout.** `fact_admission.rs` stays the root and X5's replay join, byte for byte. H's joins are child modules under `fact_admission/`. | a second top-level module; one file; amending X5's pin |
| 3 | **Boundary.** Only D3's clean settlement reaches H. Every coordinate is re-derived from host-held values. Admission is **atomic per Analyze**. | streaming before settlement; per-batch admission; trusting echoes |
| 4 | **Clean `Unavailable` and `BudgetExhausted`.** Every candidate is discarded, and the terminal's exhaustive Coverage is admitted (X-H2, FA-1). | admitting facts before the terminal; failing the terminal operationally |
| 5–8 | **The fact join.** RC-0 and the registry, the requested pair, payload in `C`, the anchor count and `file` joins on the identity owner, universes, the native confidence law and the stage spec's producer. Owner keys are kept verbatim. The anchor bytes are checked in item 14 (r2). | a second copy of an owner's law, including an early anchor byte check; repairing payloads; the wire's `producer` text |
| 9–12 | **The Coverage join.** D is built from host values only, with subjects by the relation's subject kind. The owner's view join is H's `admit_coverage_result_v3`, using the census and dialect it derives from the view itself (r2). H never edits an entry and never mints `complete`. | provider-chosen partitions; a per-Analyze census; a direct inspector call with a host-built dialect |
| 13 | **Closed-world cross-checks** are an H extension, wired after FA-1. | none; host recomputation of `closedWorld` |
| 14 | **Views.** One provisional `view2` per stage, judged once by `inspect_plan_view_joins`. Refusals are routed by what the key judges and by the view's origin (r2, RF-1). | views assembled by J2; one route for every view-join key |
| 15 | **Occupancy.** The buffer checks run at settlement with the buffer step's preconditions, and binding follows J2b's receipt. | binding before the receipt; capturing on refusal |
| 16 | **The syntax join** is the same admission path, and H carries E1's second-integrator legs. | a syntax shortcut |
| 17 | **Provider symbol censuses** get owner admission against SIS. Their carrier is X-H1 (FA-2). | inferring a census from facts or from files |
| 18 | **Host inventory records.** H derives and admits them. Their producer closure is X-H3. | leaving them unowned; minting them under the language provider's closure |
| 19 | **Hand-off.** H returns admitted records with origin tags, and J2b calls the full join. | H calling `inspect_enumeration_join` |
| 21 | **A missing rung is indeterminate.** H fabricates no Coverage and has no path to syntax. | a degraded mode |
| 22 | **Routes** use existing rows only. | any new public code |
| 23 | **Operation.** Pure; bounded by constants on no ledger; cancellation between returns; deterministic. | ledger charging; order-dependent output |
| 25 | **Units H1 to H5.** H5 alone sits on the host chain: 3 days, finishing on day 22. | one unit holding all of H after C4a |

---

## A. Scope, placement and the admission boundary

### 1. What H admits, and what it does not (lead decision)

- **Decision.** H is the host's producer-boundary admission for native evidence (CH14:482; BP:680-683). It admits into `fact2`, `scope2`, `coverage2` and `view2`, and into the host-derived typed inputs (EXC:259, EXC:265-269), every native record that evaluation reads:
  - **TS2 and Rust3 provider returns** (AQP:400; NE:2781-3316):
    - `FactCandidateV1` candidates (NE:2883);
    - `CoverageResultV3` entries in the `Coverage` and `CoverageV3` frames and in the terminals (NE:2884, NE:3270-3292);
    - `OccupancyCompanionV1` companions on negotiated `FactBatchV3` (NE:3009-3150).
  - **The in-host syntax stage's outputs** from E3: its inert candidates, and the Coverage entries E3 maps from per-file outcomes (ME:385, ME:477, ME:578). Item 16.
  - **Provider-attributed symbol inventories,** `SubjectInventoryV1` of kind `symbol` (IE:1466-1470; SIS). Item 17.
  - **Host-produced inventory records,** by lead decision. Item 18.
  - **The host's own Coverage conversions** for a clean terminal and a pre-Analyze `Unavailable` (NE:3227-3268). Item 11.
- **Not H's:**
  - **Wire decoding, framing, the spool and settlement.** These are D2b's and D3's (MD:335, MD:343, MD:618-633). "D2b admits no fact and mints no Coverage" (MD:343).
  - **The public projection of a refusal.** That is J2a's total projection in `outcomes.rs` (MJ item 10; MJ:703). H returns typed refusals with their origin, and never a termination.
  - **The `clones-near` candidate envelope.** E3 builds it and J2 captures it (ME:506-566, ME:718). It is candidate-only and mints no fact (ME:511, ME:550).
  - **Stage receipts and `ExecutionInputsV1`.** These are J2b's host capture (EXC:12-22, EXC:51-53; MJ:785).
  - **The call of the full `admit_enumeration`.** J2b makes it at J-η (MJ:377; MC:880, MC:892-896). H supplies its inputs (item 19).
  - **Evaluation and replay.** `derive_evaluation` with I1-b2 is J2b's (MJ:378; MI:404). X5's replay join is unchanged (X5:23-35).
  - **The Plan, stage specs and enumeration bindings.** These are C4a's (MC:839-917).
- **Basis:**
  - M3P:216;
  - CH14:482: "Own host admission of provider candidates, Coverage and occupancy joins against the selected source/context before evaluation; protocol framing alone grants no fact authority";
  - BP:680-683;
  - COV:5004, COV:5056, COV:7144;
  - `fact_admission.rs:1-3`.
- **Rejected:**
  - **H building the D9 projection.** MJ item 10 gives one total projection with no wildcard arm (MJ:703). A second projection would be a second owner of the outcome matrix.
  - **H admitting the `clones-near` envelope as evidence.** Its only owner is the execution-input join (EXC §6; ME:508-511).

### 2. Where H's code lives (lead decision)

- **Decision.**
  - **The root.** `crates/host/src/fact_admission.rs` stays the module root and X5's replay join, unchanged. It gains only `mod` lines and crate-private re-exports.
  - **The children.** H's joins are crate-private child modules under `crates/host/src/fact_admission/`:
    - `stage.rs`: the entries `admit_stage_return`, `admit_syntax_stage` and `bind_occupancy` (items 3, 15 and 16), and the atomic assembly of one return;
    - `candidates.rs`: items 5 to 8;
    - `coverage.rs`: items 9 to 13;
    - `views.rs`: item 14;
    - `occupancy.rs`: item 15;
    - `inventory.rs`: items 17 to 19.

    Spellings are provisional; H's units fix them.
  - **Tests.** Unit tests sit beside each child. Integration controls go in `crates/host/tests/admission_tests.rs` (CH14:497).
  - **The pins.** X5's source pin stays green and unchanged on the root (`fact_admission_tests.rs:651-700`). The children carry their own pins (H-C20).
- **Basis:**
  - X5:23: "The syntax and Coverage joins arrive with M3 in the same module. **Rejected:** creating a separate `replay_join.rs` module, which would leave `fact_admission.rs` with two owners for one boundary";
  - `fact_admission.rs:1-3`;
  - the X5 pin's forbidden list (`fact_admission_tests.rs:661-697`).
- **Rejected:**
  - **A second top-level module,** such as `host/admission.rs`. X5 item 1 rejects two owners for one boundary.
  - **Everything in the one file.** X5's pin would fail, and five sub-units would contend for one file.
  - **Amending X5's pin.** It is an accepted law's control (X5:141), and it needs no change if the root stays the replay join.
- **Record.** The new paths enter the product inventory through each unit's inventory successor. CH14's next refresh lists them (CH14-H, item 25).

### 3. What reaches H: a clean settlement, atomic per Analyze (law)

- **Decision.**
  - **The input.** H's provider entry takes D3's settled value for one child: one Analyze of one `(ExecutionId, SnapshotId, universe key)` (DLV:556-566; the Rust key is the native semantic-universe identity, NE:3161-3164). D3 releases it only on a clean settlement (MD:621-624; DLV:1138; RPP:588-596):
    - the participant reached its terminal;
    - exit status was zero;
    - EOF was observed;
    - every commitment recomputed.

    That value is constructible only by D3, and H5 pins this. H never receives a frame, a partial stream or the spool of a non-clean settlement (MD:624, MD:632).
  - **Framing grants nothing** (CH14:482; M3P:216). A wire-valid frame is a claim. H re-derives every coordinate it checks from host-held values:
    - the retained Plan;
    - the execution-plan stage spec found through the dispatch binding's `retainedStageOrdinal` (NE:3034-3044);
    - the sealed snapshot;
    - the admitted universes and contexts.

    It never uses a worker echo as a source of truth. The host owns fact validation and admission, and `workerMayMintHostIdentities` is false (DLV:568-574).
  - **Atomic per Analyze.** H admits the candidates, Coverage, companions and census of one Analyze together, or none of them. DLV's atomicity scope is the "entire Analyze across every requested stage" (DLV:1139), and Rust admits "the complete Analyze candidate set and Coverage only after every condition succeeds" (RPP:596).
    - H judges Coverage only after every candidate of that Analyze has passed F1 to F9, because the owner's view join judges each Coverage against the facts its view names (item 10).
    - A refusal anywhere discards the whole return. No `fact2`, `scope2`, `coverage2`, `view2`, attribution or inventory from that child is retained (NE:3837-3843).
  - **The order within one return:**
    1. facts, F1 to F9 (items 5 to 8);
    2. the symbol census (item 17);
    3. D, the scopes and the provisional Coverage, after the bijection and closed-world checks (items 9, 11, 12 and 13);
    4. the provisional views and the owner's view-join call, which runs F10 and item 10's producer boundary (item 14);
    5. the occupancy buffer (item 15).

    Occupancy **binding** follows J2b's stage receipt (item 15).
  - **Where records go.** H writes descriptors and `C` blobs only into the invocation's private temporary custody (MJ:399). It never writes to a store before the attempt row (MJ:411).
  - **INC-2.** Every record H mints binds the current `snapshot2` and `plan2`, and every wire echo of them must equal them (AQP:388; NE:3158-3161). No standing is inherited from an earlier Run.
- **Basis:** DLV:1136-1144 (`factBatchAtomicity`), DLV:1517 (DL-13: "admits facts only after Complete+matching commitments+zero-exit+EOF"); RPP:584-598; MD:618-633; NE:3837-3843.
- **Rejected:**
  - **Admitting candidates before settlement,** for memory or latency. That is partial admission (MD:630).
  - **Per-batch admission.** A batch is not the atomicity unit (DLV:1139), and RC-2 needs the whole Analyze's census.
  - **Taking `stageId`, `producer` or a universe from the frame** as the coordinate itself. Workers may not mint host identities (DLV:572).

### 4. Clean non-Complete terminals: candidates discarded, terminal Coverage admitted (lead decision; X-H2)

MD hands this choice to H: "Which candidates a clean `Unavailable` or `BudgetExhausted` admits is the admission owner's" (MD:623; finding F7, MD:1107).

- **Decision.** On a clean post-Analyze `Unavailable` or a clean `BudgetExhausted` (D3 clean settlement, zero exit and EOF), H:
  - **discards** every fact candidate and every occupancy companion of that Analyze;
  - **admits** the terminal's exhaustive Coverage, one entry per requested key in stage-major/key order (NE:3288-3292), at item 10's producer boundary;
  - **records** the child's owed symbol inventories as host-derived outcomes of the terminal (item 17):
    - `unavailable` with `provider-unavailable` for `Unavailable` (ENC:121);
    - `partial` with `budget-exhausted`, a null cause, no rows and no examined paths for `BudgetExhausted` (ENC:120).

  The stage is `partial` and the Run's route is MJ row 31: indeterminate 3 by the primary deficiency (NE:3849-3855). Only one clause of NE:3849-3850 is not applied: "facts before the terminal are admitted".
- **Basis:**
  - **The candidate dispositions are retained.** DLV's `candidateDisposition: DISCARD_ALL_CANDIDATES` for both terminals (DLV:1140-1141, DLV:1152, DLV:1164) and RPP's `discardAllOn` with "candidates remain discarded" (RPP:597-598) are **not** superseded. NE §0 supersedes those terminals' payload schemas and coverage-payload selectors, and names none of their candidate dispositions (NE:126, NE:129).
  - **Nothing can verify the pre-terminal stream.** Stream integrity is committed only on `Complete`: `factStreamCommitment` exists only on `CompleteV1` (DLV:1138, DLV:1171; RPP:588-596).
  - DLV:1517: facts are admitted only after "Complete+matching commitments+zero-exit+EOF".
  - **The terminal is clean, not a fault.** DLV:1156: "never operational-failed solely for clean Unavailable".
- **Rejected:**
  - **Admitting facts before the terminal,** as NE:3849-3850 reads. It admits facts whose stream integrity nothing verified, against the retained selectors.
  - **Treating the terminal as an operational fault.** That contradicts DLV:1156 and NE:3849.
- **Consequence, disclosed.** If a provider finds a cycle and then exhausts its budget, the Run cannot fail on that cycle. It is indeterminate, `COVERAGE.BUDGET_EXHAUSTED`. This fails closed: indeterminate is never pass (MI item 6).
- **Cross-law X-H2.** The native owner's passage successor **FA-1** reconciles NE:3849-3850 with the retained selectors (see "Cross-law items").

---

## B. The fact join (DR-G23, finding masquerade)

### 5. The candidate join, in order (law; r2, RF-1)

Each candidate of a settled return, and each in-host syntax candidate (item 16), passes these checks in this order. A refusal at any step refuses the whole return (item 3).

| Step | Check | Owner of the law | Refusal key |
|---|---|---|---|
| F0 | **Precondition, not H's check.** The batch correlates with its `DispatchBindingV1` (`stageId`, `analysisOrdinal`, `batchIndex`, contiguous `candidateOrdinal`). D2b checks this at the wire (NE:3039-3044; PWM:278-330). | D2b | `PROVIDER_RETURN_DISPATCH` (NE:3044) |
| F1 | **Registered relation.** `relation` is one of the thirteen registered relations (RPS `x-opensip-relation-registry`; IE:912-916). A record of any other shape, such as a finding, a verdict, a rule identity or a cycle, is not a candidate. This is NT-3's finding masquerade (REG:368). | RPS | `FACT_RELATION_UNREGISTERED` |
| F2 | **RC-0.** `resolution` is a rung of **that relation's** ladder. The rung vocabulary is shared, so schema validity proves nothing (NE:2072-2090). H reads the registry ladder before decoding, and F4's identity call checks it again. | RPS `ladderAuthority` | `FACT_RUNG_NOT_IN_LADDER` |
| F3 | **Requested (r2: the pair).** The `(relation, resolution)` pair is one the attributed stage requested (DLV `FactCandidateV1.relation`: "requested by the attributed stage"; DLV:1144, "relation/rung"). With F7, every fact that passes lies under one of the stage's requested Coverage keys, and so under one of the provisional view's scopes (items 9 and 14). | DLV | `FACT_RELATION_NOT_REQUESTED` |
| F4 | **Payload, under the identity owner.** Decoded under the registered selector, held to every retained restriction and re-encoded to `C` (item 6). Then `inspect_relation_snapshot` runs, which calls `inspect_relation_payload` first (`closure.rs:329-338`, `:417-497`). Those owners re-check the ladder, the per-rung fields, `same-only`, non-negative integers and NFC text (`relations.rs:325-391`). A `clones` fact also goes to the evaluator's `inspect_body_identity` (`body_identity.rs:389-398`). | IE:904-916; identity and evaluator owners | the owner's `RelationRule` text (for example `rung not in ladder`, `forbidden rung field`, `same-only universe`, `non-NFC string`), or the owner's typed error |
| F5 | **Anchor count.** The count is the relation's `anchorLaw` count: at least 1 for `source-text`, 0 for `inventory` (IE:1004-1006). F4's call checks it (`relations.rs:334-341`). **F5 checks no anchor bytes (r2, RF-1).** Whether a source anchor names an inventoried blob, lies inside it and splits no UTF-8 character (IE:164, IE:1426-1429) is checked once, at F10. The only owner of those checks reads them from a view (`view_joins.rs:388-407`). | identity owner | `anchor cardinality` |
| F6 | **Snapshot joins of the payload.** A `file` payload's `path`, `contentSha256` and `byteLength` equal the sealed inventory row, and its anchors name that path (IE:986-990). F4's call checks them (`closure.rs:465-494`). | IE:986-990; identity owner | `path not inventoried`, `file content join`, `file length join`, `anchor foreign path` |
| F7 | **Universes.** `sourceUniverseId` is this child's universe. `targetUniverseId` is that universe or an activated target universe of the stage. `universeRule: same-only` requires them equal (IE:914-916; NE:3162-3164). Requested keys cross universes only for `imports`, `calls` and `references`, and every other relation has exactly one intra-universe key (DLV:972-975; r3, NBO-1). | IE, NE, DLV | `FACT_UNIVERSE_NOT_IN_STAGE` |
| F8 | **Confidence.** `confidenceMillionths` is exactly 1,000,000. That is NE §4.8's provider emission law, which holds over every native relation (NE:2366-2373). | NE §4.8 | `FACT_CONFIDENCE_NOT_NATIVE` |
| F9 | **Syntax universes only.** `inspect_syntax_fact`: every anchor path is read by a selected grammar that bears the `relation@rung`. Inventory relations are exempt (NE:319-336; `capability_support.rs:219-277`). | evaluator | `SYNTAX_CAPABILITY_UNSUPPORTED_FACT` |
| F10 | **View joins, the anchor bytes among them (r2).** Once the provisional view names the facts (item 14), `inspect_plan_view_joins` checks each fact's snapshot and producer (`FACT_SOURCE_PRODUCER_JOIN`) and its scope (`FACT_SCOPE_JOIN`). It then checks each anchor's source blob, range and UTF-8 boundaries (`ANCHOR_SOURCE`, `ANCHOR_RANGE`, `ANCHOR_UTF8`) (`view_joins.rs:366-407`). Item 14.4 routes each key. | evaluator | as named |

- **One implementation per law (lead decision).** Where the identity crate or the evaluator owns a check (F4 to F6, F9 and F10), H puts the record into its staging overlay (item 14.2) and calls that owner, keeping the owner's key verbatim. H implements only what no owner implements: F1 to F3, F7 and F8, D, the payload adapter and atomic discard. So a record H admits is a record Run closure admits, under the same law (ME:772's "single implementation" pattern).
  - The anchor byte law in particular has one owner. H runs it where that owner can run: over the provisional view.
  - r1's F5, which claimed to run those checks before any view existed, is withdrawn (r2, RF-1).
- **Routes (r2, RF-1; r3):**
  - a refusal at F1 to F9 takes MJ row 30 for a provider return, and the host-invariant row for a record E3 hands H (item 16);
  - F10's keys are routed only by item 14.4's table.
- **The keys.** H's own keys (F1 to F3, F7 and F8) are internal diagnostic keys. They are kept in the operational record. They are not `DomainDetailCode` members and add no public code (NE:3546-3555; FAULT:54-55). The owners' keys are kept as the owners spell them. r1's `FACT_ANCHOR_CARDINALITY` is withdrawn: IE uses that name as prose (IE:1038), and no owner returns it.
- **Basis:** REG:368; COV:5018 (G23's method: "Fact2 payload admission"); DLV:1144 (`hostValidation`); IE:904-916, IE:986-1006, IE:1426-1429; NE:2072-2090, NE:2366-2373; `closure.rs:329-338`, `:417-497`; `view_joins.rs:366-407`.
- **Rejected:**
  - **A host copy of RC-0, the payload rules or the anchor law,** including an anchor byte check before any view exists. Two implementations of one law can drift. The identity and evaluator functions are the product's single owners.
  - **Admitting first and leaving refusal to Run closure.** That routes a provider lie through replay as `EVALUATION.INPUT_REFUSED` after evaluation has already run, rather than refusing it at the boundary (NE:1945-1947).
- **Forbidden substitutes:**
  - a record that is not a registered relation admitted as a fact;
  - a rung matched against the flat vocabulary;
  - a `(relation, rung)` pair the stage did not request;
  - a native confidence below 1,000,000;
  - an anchor byte or UTF-8 check outside `inspect_plan_view_joins` (r2);
  - any key added to the public detail registry.

### 6. The payload adapter: deterministic CBOR to `C` (law)

- **Decision.**
  - **Decoding.** D2b's strict deterministic-CBOR reader decodes `FactCandidateV1.canonicalRelationPayload` (MD:335).
  - **Validation.** H validates the decoded value against the registered RPS selector for that relation and rung. It refuses any value that a retained restriction forbids: non-NFC text, a negative integer, a value out of `uint64` range, a field outside the closed set, a value outside an enum, a per-rung required field missing or forbidden field present, or a `universeRule` breach.
  - **Encoding.** H re-encodes to `C`. `payloadDigest` names those `C` bytes, and `payloadSchemaDigest` is the RPS document's own file digest (IE:912-916).
  - **No repair.** The adapter "refuses rather than repairs" (IE:906-909).
  - **Under negotiated `FactBatchV3`,** the wire bytes are the same CBOR. `decodedRelationPayload` is a test-vector observation and never a wire member (NE:3011-3020, NE:3077-3082).
  - **E3's candidates** are produced in the host as RPS payload values (ME:468). They pass the same validation and `C` encoding, with no CBOR step.
- **Basis:** IE:810-828 ("`fact2` payloads are `C`"), IE:904-916; NE:3072-3086.
- **Rejected:**
  - **A second CBOR decoder,** for example a general crate. MD rejects it (MD:347-348).
  - **The identity `capability_codec`.** It is a CVE1 tag format (`capability_codec.rs:1-2`).
  - **Keeping the CBOR bytes as the preimage.** Historical CBOR is never a `fact2` preimage (IE:902-905).

### 7. `unresolved-edge` facts (law)

- **Decision.**
  - **What they are.** `unresolved-edge` facts are product facts that the host mints (NE:2202-2206):
    - relation `unresolved-edge`, rung `observed`, `universeRule same-only`;
    - payload `{referrer, relation ∈ {imports, references, calls, types, reachability}, edgeKind, targetScope, targetModule|null, detail ≤ 512 bytes}`, where `edgeKind` is one of the closed sixteen `UnresolvedEdgeKindV1` values (NE:2189-2200);
    - at least one source-text anchor (IE:1004).

    They pass item 5's join unchanged.
  - **They are item 10's census.** H never drops one. It never synthesizes one: an `unresolved-edge` fact wraps a producer's payload (NE:2202-2206), and RC-2 counts admitted facts only (NE:2113-2117). It never infers one from a Coverage entry's counts.
  - **The per-stage bound.** `maxUnresolvedEdgesPerStage` is 1,000,000 (NE:2184-2185, NE:2933). A `Complete` stage that carries more refuses at H. A conforming provider ends such a stage in `BudgetExhausted` instead (RC-5).
- **Basis:** NE:2113-2122 (RC-2 counts "admitted `unresolved-edge` facts whose relation matches and whose referrer is in the examined set"); NE:2187-2206.
- **Forbidden substitutes:** an unresolved edge inferred from `unresolvedEdgeCount`; one admitted under another relation's ladder; one dropped because its referrer lies outside every scope.

### 8. The producer, the universes and `fact2` (law)

- **Decision.**
  - **The producer.** `fact.producerClosure` is the `producerClosure` of the execution-plan stage spec that the dispatch binding's `retainedStageOrdinal` names (NE:3012, NE:3119-3121). It is never the wire's `producer` text, and never a closure that stage spec does not name. Its kind must be `provider` (IDS:4729-4731; ATOM:48).
    - On a syntax-universe record, it is the core provider closure, and only there (MC:435-443; ME:570-578).
    - On a TypeScript or Rust record, it is that language's provider closure. Host-produced inventory records are X-H3's (item 18).
  - **The identity.** `fact2` = H("fact", {snapshot, relation and rung, universes, producer closure, exact relation payload and its schema digest, anchors, confidence millionths}) (IE:184).
  - **M3-C r7 (accepted; r2, NBO-2; r3).** r7 narrows item 16 row 8, closure admission, to a selection among manifests already admitted at J1 r4's R10a (MJ:325). H does not depend on row 8. It reads producer closures from the retained Plan and stage specs, whichever step admitted them.
- **Basis:** IE:184; IDS:4726-4745 ("enumeration, view production, fact production and stage production are all provider acts under the existing kind"); NE:3115-3126; MC:458 ("the consuming Rust provider's closure as producer: false, since the provider did not produce the record").
- **Forbidden substitutes:** a producer taken from the frame; the core provider closure on a TypeScript or Rust record (MC:464); a language provider's closure on a record that provider did not produce.

---

## C. The Coverage join (DR-G23, Coverage-domain mutation; NE §4)

### 9. The host subject scope D (lead decision; X-H1, X-H6)

- **Decision.** For every Coverage entry it judges, H builds D = `{schemaVersion: 2, snapshotId, sourceUniverse, targetUniverse, relation, resolution, enumeratorClosure, subjects}` (NE:1902-1915; IDS:620-680) from host-held values only. "A provider-supplied commitment is never an input to this step" (NE:1927-1928).
  - **`snapshotId`** is the Plan's.
  - **`relation`, `resolution` and both universes** come from the requested key, which the host derived before spawn (NE:3230-3233, NE:3277-3282).
  - **`enumeratorClosure`** is the binding's Plan-selected enumerator, `enumerator.closureId` (IDS:4729; ENC:106). The enumerator and the stage's producer are separate coordinates (NE:3054-3059).
  - **`subjects`** depend on the relation's subject kind (RPS:15, `subjectKindLaw`). SIS's `InventoryRowV1.nativeSubjectId` is "Scope.subjects spelling: LogicalPath for file; package name for package; SubjectIdV1 for symbol". Scope subjects are inventory rows (ENC:93):
    - **`source-path`** (`file`, `vcs-change`, `clones`): the binding's host-derived extent of that kind. For `clones` that is the body-eligible paths (NE:959-970). It is never a provider list.
    - **`package-name`:** the names of the host-derived package inventory rows (item 18).
    - **`symbol`** (`declares`, `literal`, `control-flow`, `imports`, `references`, `calls`, `types`, `reachability`, `unresolved-edge`): the `nativeSubjectId`s of the binding's admitted symbol census (item 17). That census is the enumerator's trusted attribution (RPS:15; NE:507-515).
      - In a syntax universe, the census is E3's.
      - **In a TS2 or Rust3 universe, the census has no carrier today (X-H1).**
  - **Order.** The subjects are a canonical set, and a duplicate refuses rather than deduplicating (NE:1912-1913; NEM:1500-1523).
- **Bounds (X-H6).** IDS bounds `subjects` at 100,000 entries, and the identity encoder bounds the descriptor at 4 MiB of `C` bytes (IDS:674; IE:117; MC:307-310). H never truncates D and never splits it.
  - A scope that would exceed either bound refuses through S-B's projection: request-rejected 2, `REQUEST.UNSATISFIABLE`, `PROJECT.SCOPE_LIMIT`, subject `subject-scope.subjects:count>100000` or the byte form. This needs S-B to gain the field (X-H6).
  - Until then, H5's large-scope path is gated on S-B, as MJ:402 gates every unit that reaches an S-B route.
- **Basis:** NE:1894-1947; RPS:15; SIS `InventoryRowV1`; ENC:93; IDS:620-680.
- **Rejected:**
  - **D from the provider's `examinedUniverse`.** "A provider that examined a narrower partition than the host enumerated is detected here, and by nothing else" (NE:1936-1937).
  - **Symbol subjects derived from facts, anchors or file paths.** "Inventing symbol-to-path parsing would be fabricated evidence" (RPS:15). It is also I1's forbidden census inference (MI:490-492).
  - **Truncating or sharding a large scope.** NE:4280 forbids truncation and sharding in this family.

### 10. The producer boundary runs in the owner's view join (law; r2)

- **Decision.** For each Coverage entry of a return, after item 12's bijection check, H prepares and the owner judges.
  1. **H prepares,** in the return's staging overlay (item 14.2):
     - D and its `scope2` = H("subject-scope", D) (item 9; NE:1898);
     - the entry's `C` bytes as a blob;
     - a **provisional** `coverage2` = H("coverage", {schemaVersion: 2, scopeId, payloadSchemaDigest, payloadDigest}). Its `payloadSchemaDigest` is the registered NES document's digest and never a caller's (IE:185; NE:1939-1943).

     H names the scope and the provisional `coverage2` in the stage's provisional view (item 14).
  2. **The owner judges,** in item 14's single call of `inspect_plan_view_joins`. For every Coverage the view names, that call (`view_joins.rs:434-532`):
     - requires its scope to be one of the view's (`COVERAGE_SCOPE_JOIN`);
     - builds **the census** from the `unresolved-edge` facts the view names (`view_joins.rs:450-466`). That is RC-2's census: "the admitted `unresolved-edge` facts of the view" (IE:1481; NE:3351, NE:3474);
     - derives the source-variant table from the retained universe frame (`view_joins.rs:470-479`);
     - runs `inspect_coverage_producer` with that census and table (`view_joins.rs:480-491`). The inspector applies NE §4.1a's commitment, key and count joins, the RC bijection, the cause carriers and the source-variant guard (`coverage.rs:305-455`);
     - requires the inspector's `coverage2` to equal H's provisional one (`COVERAGE_ADMITTED_IDENTITY`);
     - runs `inspect_coverage_prerequisites` and the relation's `coverageTotality` (`view_joins.rs:498-532`).
  3. **Admission.** A Coverage entry is admitted only when that call returns without refusal. Until then the provisional `coverage2` is a staging name that nothing outside the overlay sees. So NE's order, every check before any `coverage2` exists (NE:1924-1940), holds for every record that leaves the overlay.
- **This is the product's `admit_coverage_result_v3`** (NE:1924-1947; NEM:1545). It is also the same composition Run closure re-runs over the retained view. H writes no copy of RC-0 to RC-6, the cause-carrier registry or the commitment law. It calls `inspect_coverage_producer` nowhere itself.
- **The census slice (r2, NBO-1).** `CoverageProducerInput.unresolved` is a caller-supplied slice (`coverage.rs:28-36`), and the inspector cannot prove it complete (`coverage.rs:21-22`). On H's path its only caller is the owner's view join, which builds the slice from the facts the provisional view names. Those are host-held values: facts that passed F1 to F9 and that H put in the view (item 14.1). H's child module `fact_admission/coverage.rs` passes no census anywhere, and no census is taken from a provider or from a caller of H (H-C9).
- **What the owner cannot establish, H establishes:**
  - D, from host values (item 9);
  - that the view names every admitted fact of its stage, so the census is the view's whole census (item 14.1);
  - the entry-to-key bijection (item 12);
  - the stage's and the enumerator's Plan binding (items 8 and 9).
- **Routing.** Every key from that call is routed by item 14.4's table, and only by it (r3).
- **Basis:** NE:1924-1947, NE:2083-2122, NE:2135-2181; IE:1481; NE:3351; `view_joins.rs:434-532`; `coverage.rs:305-455`.
- **Rejected:**
  - **r1's direct call of `inspect_coverage_producer`.** It disagreed with the owner on two points:
    - it used a per-Analyze census, where the law counts the view's facts (IE:1481);
    - it passed the reference model's `languageVersionBinding.dialect`, where the product reads a `{table}` derived from the universe frame (`view_joins.rs:470-479`; `coverage.rs:290-303`). The function that builds that table is crate-private to the evaluator (`capability_support.rs:279`).

    Two callers of one law could disagree with each other and with Run closure.
  - **Pre-filtering the census by D's subjects.** The bijection decides membership (NE:2113-2117).
- **Forbidden substitutes:**
  - a census or dialect supplied by H, by a provider or by a caller of H;
  - an admitted Coverage whose view-join call refused;
  - a provisional `coverage2` leaving the overlay before that call.

### 11. Coverage outside a `Coverage` frame: the provider's terminal entries and the host's pre-Analyze conversion (law; r3)

- **Decision.** Two cases bring Coverage to H outside a `Coverage` frame. H admits every entry of both at item 10. The two have different origins (item 14.1), and their refusals are routed by item 14.4 and item 22, never here (r3).
  - **A clean `Unavailable` or `BudgetExhausted` terminal** (item 4). The entries are the provider's own, carried in the terminal's `coverage` array. Entry *k* belongs to the stage whose cumulative requested-key range contains *k* (NE:3288-3292). H writes none of them. Their origin is **provider return**.
  - **A pre-Analyze `Unavailable`** (`native-context-mismatch`; NE:3205-3268). This is the only case in which the host writes Coverage, and its origin is **host-minted**. After DONE, it mints one entry for each requested key of every stage it would have placed:
    - coverage `unknown`;
    - `examinedUniverse` = the host commitment and count;
    - `resolutionCompleteness` = `completeness_from_stage` with `attempted=false`, `stageTerminal=unavailable` and `examinedExhaustive=false`;
    - `closedWorld` = exactly the startup law's fixed value;
    - `derivationKinds` = `[]`;
    - confidence 0;
    - deficiency `provider-unavailable` with a null cause (NE:3234-3264).

    No stage id and no coverage comes from the worker (NE:3267-3268; NEM:4586-4617).
- **H writes no Coverage for:**
  - a faulted or cancelled child (NE:3837-3843);
  - an `UNSUPPORTED-TYPED` cell, an unselected enumerator or a null-universe binding: "no Coverage is fabricated at null U" (ENC:69-77). The execution-input account carries that disclosure (EXC §5; J2b).
- **Symbol keys before any census (X-H1).** The pre-Analyze conversion needs D for symbol-kind keys, and no census exists. Until FA-2 is accepted, H refuses to mint such an entry and the leg is gated. FA-2's recommended content is `subjects: []` with the entry above: nothing examined, `unknown`.
- **Basis:** NE:3205-3268, NE:3288-3292; ENC:69-77.
- **Forbidden substitutes:** a Coverage entry for a child that did not run; any host-minted entry other than `unknown`.

### 12. No Coverage-domain mutation, no unknown-to-covered conversion (law)

- **Decision.**
  - **Bijection with the request.** `entries[i]` answers `requestedCoverageDomain.keys[i]` (NE:3277-3282):
    - relation, resolution and `subjectScopeCommitment` equal the requested key;
    - the universes are the key's universe-id suffixes;
    - the entry count equals the requested key count.

    A missing, extra, reordered or re-keyed entry refuses (`native.coverage-entry-key-mismatch`, NE:3529).
  - **H never edits an entry.** It never changes `coverage`, `deficiency`, `nativeCause`, `resolutionCompleteness`, `closedWorld` or `derivationKinds`, and never turns `unknown` into `complete` (REG:368: "no unknown-to-covered conversion"). The only entries the host writes are item 11's pre-Analyze conversion entries, and they are `unknown`.
  - **A provider's `complete` survives only if the inspector admits it:** RC-2 over the census, RC-6 and the subject count (NE:2113-2122, NE:2135-2181).
- **Basis:** REG:368 (NT-5, Coverage-domain mutation); COV:5018; NE:3277-3282, NE:3529.
- **Forbidden substitutes:** an entry rewritten "to match" its key; a host-chosen partition; a `complete` minted by the host.

### 13. Closed-world cross-checks (lead decision; an H extension, wired after FA-1)

- **Decision.**
  - **Two record laws of NE §4.5.** H checks both over the stage's admitted `unresolved-edge` facts, the same facts its provisional view names (item 14.1):
    - `deadCodeRepairEligible` implies `exportsClosed=closed`, `entryPointsRecognized=all` and `nonliteralLoading=none` (NE:2237-2240);
    - `nonliteralLoading=none` implies that the universe has no admitted `unresolved-edge` fact of class `require-nonliteral`, `dynamic-import-nonliteral`, `reflective-access` or `indirect-eval` (NE:2221-2222).
  - **The route.** A contradiction refuses on NE §10's producer row with the internal key `native.coverage-closed-world-mismatch`. **It is wired only after FA-1** adds that key to NE:3529's producer-boundary row. Before FA-1, H-C13 asserts the two laws over fixtures only.
  - **This is an H extension.** The reference producer boundary recomputes only "the bijection and the RC-2 preconditions" (NE:3005-3007; NEM:1545-1605). COV's G23 method asks for "Coverage3 examined/resolution/closed-world cross-checks" (COV:5018).
- **Rejected:**
  - **No closed-world check.** G23's method names it.
  - **Host recomputation of `closedWorld`.** Ingredients 1 and 4 need manifest and configuration semantics that the producer owns (NE:2216-2224, NE:3005-3007).

---

## D. Views, occupancy and the syntax join

### 14. Views: the provisional view, the owner's view join and its routing (lead decision; r2, RF-1)

- **Decision.**
  - **14.1 One view per stage, and one origin per view.** H mints one `view2` for each (stage, producer closure), over:
    - the stage's scopes;
    - every fact of the stage that passed F1 to F9;
    - the stage's Coverage.

    The view is H("view", {Plan, scopes, facts, Coverage, producer and schema closure}) (IE:186), and its producer is the stage spec's (item 8). One party authored every fact and Coverage entry a view names, so every view has one **origin**:
    - **provider return:** a TS2 or Rust3 stage's view, including a clean terminal's Coverage (item 4);
    - **host-minted:** E3's syntax stage (item 16), item 11's pre-Analyze conversion and item 18's inventory stage.

    The scopes (D) are H's in every view. They are assembly, not a claim.
  - **14.2 The provisional view.** H builds each view in a **staging overlay** of the return's temporary custody (MJ:399), together with its scopes, facts, provisional Coverage and the blobs they name. The overlay joins the return's admitted set only after the view-join call returns without refusal. A refusal discards the overlay with the rest of the return (item 3). Nothing is committed, and nothing is visible outside H, before then.
  - **14.3 One owner call.** H runs `inspect_plan_view_joins` once over each provisional view (`view_joins.rs:212-223`), passing evaluation refs that name exactly that view and its provisional Coverage. That call checks, in this order (`view_joins.rs:276-532`):
    - the view's Plan and producer (`VIEW_PLAN_JOIN`, `UNSELECTED_PRODUCER`);
    - its scopes, their enumerators and their partition (`SCOPE_SOURCE_JOIN`, `UNSELECTED_ENUMERATOR`, `ENUMERATOR_CLOSURE_KIND`, `SUBJECT_SCOPE_PARTITION_OVERLAP`);
    - each fact's snapshot, producer and scope (`FACT_SOURCE_PRODUCER_JOIN`, `FACT_SCOPE_JOIN`);
    - **each anchor's source blob, range and UTF-8 boundaries** (`ANCHOR_SOURCE`, `ANCHOR_RANGE`, `ANCHOR_UTF8`);
    - the Coverage joins and item 10's producer boundary (`VIEW_COVERAGE_JOIN`, `SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER`, `COVERAGE_SCOPE_JOIN`, `COVERAGE_PRODUCER_ADMISSION:<causes>`, `COVERAGE_ADMITTED_IDENTITY`, the prerequisite keys and `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH`).

    This call is the only place H checks anchor bytes (F5, F10), and the only place a Coverage entry is admitted (item 10).

**14.4 The routing rule: the only authority for view-join keys (r2, RF-1; r3).** Every refusal of the view-join call is routed by this table and by nothing else. Items 5 (F10), 10, 11, 16 and 22 refer to it and restate none of it.
- **Matching (r3).** The owner returns a key string, and often appends a suffix after a `:` (`view_joins.rs:352-357`, `:429-431`, `:526-530`; `capability_support.rs:330-370`). H matches a key by its **prefix token**: the text before the first `:`, or the whole key when it has none.
  - A prefix token is matched by equality against the tokens listed below.
  - The catch-all row applies only when no listed token matches.
  - A refusal that carries no key string (a record, limit, owner or selection error) takes the catch-all row.

  For example, `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH:file@enumerated:a.ts` has prefix token `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH`, so it takes that token's row.
- **Origin** is the view's (14.1).

| Prefix token | Provider-return view | Host-minted view |
|---|---|---|
| `ANCHOR_SOURCE`, `ANCHOR_RANGE`, `ANCHOR_UTF8` | MJ row 30 | host invariant |
| `COVERAGE_PRODUCER_ADMISSION` | MJ row 32 or MJ row 30, by 14.4a | host invariant |
| `COVERAGE_DIALECT_PREREQUISITE`, `COVERAGE_DIALECT_PREREQUISITE_UNDISCLOSED`, `COVERAGE_DIALECT_DEFICIENCY_MISMATCH`, `COVERAGE_DIALECT_CAUSE_MISMATCH`, `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`, `SYNTAX_CAPABILITY_DEFICIENCY_MISMATCH`, `SYNTAX_CAPABILITY_CAUSE_MISMATCH`, `COVERAGE_SOURCE_VARIANT_UNSUPPORTED_SCOPE`, `COVERAGE_SOURCE_VARIANT_DEFICIENCY_MISMATCH`, `COVERAGE_SOURCE_VARIANT_CAUSE_MISMATCH`, `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH` | MJ row 32 | host invariant |
| **catch-all, H's assembly:** any other token, or no key. For example `VIEW_PLAN_JOIN`, `UNSELECTED_PRODUCER`, `SCOPE_SOURCE_JOIN`, `UNSELECTED_ENUMERATOR`, `ENUMERATOR_CLOSURE_KIND`, `SUBJECT_SCOPE_PARTITION_OVERLAP`, `FACT_SOURCE_PRODUCER_JOIN`, `FACT_SCOPE_JOIN`, `VIEW_COVERAGE_JOIN`, `SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER`, `COVERAGE_SCOPE_JOIN`, `COVERAGE_ADMITTED_IDENTITY`, `BODY_ELIGIBILITY_UNDECLARED`, `BODY_ELIGIBILITY_FORM` | host invariant | host invariant |

- **The rows** (MJ:675-678):
  - **MJ row 30** (MJ:676; NE:3529) and **MJ row 32** (MJ:678; NE:3538, NE:3541) are both operational-failed 4, `PROVIDER.PROTOCOL_VIOLATION` / provider-protocol, with `domainDetail` absent and the key in the operational record. They differ only in the condition they record.
  - **The host invariant** is MJ row 29's codes (MJ:675; NE:3573): operational-failed 4, `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant, `HOST.INVARIANT_VIOLATED`.
- **Why anchors take row 30 only.** An anchor failure breaks the byte rule (IE:164, IE:1426-1429). It is a producer-boundary protocol violation (NE:3529), not a Coverage cause or carrier.
- **Why the prerequisite and totality keys take row 32 (lead decision).** Each refuses a Coverage entry whose declared completeness, deficiency or cause its own carrier law contradicts:
  - a false `complete`, an undisclosed or wrong deficiency, or a wrong cause (NE:446-453, NE:3772-3779, NE:3802-3806);
  - a `complete` `file@enumerated` that omits an inventoried path (NE:358-363).

  That is row 32's condition: "Producer Coverage cause or carrier refusal; contradictory completeness" (MJ:678). NE assigns these keys no other row.

**14.4a The tie rule for `COVERAGE_PRODUCER_ADMISSION` (r3).** The owner joins every refusal and fault of one inspection into one key (`view_joins.rs:136-148`). Each cause in the key is one of the owner's own spellings, and belongs to one of two classes:
- **Row-32 causes:**
  - a refusal beginning `native.coverage-cause-`: the cause-carrier registry (NE:3541; `coverage.rs:106-157`);
  - a refusal beginning `native.coverage-source-variant-`: the source-variant carrier law (NE:3802-3806; `coverage.rs:389-399`);
  - a bijection fault whose `fault` member begins `RC-6:`: contradictory completeness (NE:3538; `coverage.rs:192`). The key renders it as `'fault': 'RC-6:` (`view_joins.rs:141-146`).
- **Row-30 causes:** every other cause. These are NE §4.1a's key, commitment, count, entry-key and schema-digest refusals, and the bijection faults labelled `RC-0:`, `RC-1:` and `RC-2:` (NE:1945-1947, NE:3529; `coverage.rs:183-260`, `:358-404`).

**The rule:** row 32 when any row-32 cause is present; otherwise row 30.
- Rows 30 and 32 share the public termination, and item 3 discards the return either way. So the rule decides only which condition is recorded (r2 review, NBO-3).
- H matches only the owner's key spellings and rule labels. It reads no free text to choose a route.

**14.5 Why this split.**
- **Claims.** An anchor is the producer's own statement of what it read: its path, blob digest and byte range (IE:164, IE:1426-1429). A Coverage entry is the producer's claim about its partition, and NE makes every producer-boundary refusal of one `PROVIDER.PROTOCOL_VIOLATION` (NE:1945-1947, NE:3529, NE:3538, NE:3541). Reporting a provider's lie as a host bug misroutes it. Reporting the host's own minting error as a provider fault misroutes it the other way.
- **Assembly.** Every other key tests a coordinate H built: the view; its producer, from the stage spec (item 8); its scopes, from the requested keys (item 9); each fact's snapshot and producer (item 8); each Coverage's scope and provisional identity (item 10). F3 and F7 already refuse, at the producer boundary, every provider fact whose relation, rung or universes match no requested key. Requested keys cross universes only for `imports`, `calls` and `references`, with one key per activated universe; every other relation has exactly one intra-universe key (DLV:972-975). So a fact that passes F3 and F7 names a requested four-tuple, and `FACT_SCOPE_JOIN` can only fail through H's own assembly (r3, NBO-1).
- **One origin.** A view never mixes origins (14.1), so the view's origin is the origin of the record whose key fired. The owner returns a key, not a record (`view_joins.rs:388-407`). One origin per view makes the key and the view enough.

**14.6 Overlap.** Run closure decides disjointness (IE:1431-1444). H's requested keys are host-built, so `SUBJECT_SCOPE_PARTITION_OVERLAP` in this call is a host invariant.

**14.7 Receipts.** The view digests H returns become J2b's stage-receipt `outputRefs` (EXC:12, EXC:51-53).

- **Basis:** IE:164, IE:186, IE:1426-1429, IE:1431-1444, IE:1481; NE:1945-1952, NE:3529, NE:3538, NE:3541, NE:3573; `view_joins.rs:212-223`, `:276-532`; MJ:399.
- **Rejected:**
  - **Views assembled by J2b.** The view is the unit `coverage_view_use` is judged against (NE:1949-1952), so its owner is the owner of the parts.
  - **A host copy of the anchor byte law, run before the view.** That was r1's F5 as written, and it would be a second implementation of `view_joins.rs:388-407`.
  - **Every view-join refusal as a host invariant,** as r1's item 14 had it. A provider anchor that misses its blob, overruns it or splits UTF-8 is a producer-boundary lie (NE:3529, NE:3837-3843).
  - **Every view-join refusal as a provider fault.** Most keys test what H built.
- **Forbidden substitutes:**
  - a view that mixes provider and host-minted records;
  - an overlay record that leaves H before its view-join call passes;
  - a claim or assembly key routed against 14.4's table;
  - a second route table anywhere in H (r3).

### 15. The occupancy join (law)

- **Decision.**
  - **The buffer checks.** D3 holds the spool until settlement (MD:621). So `buffer_fact_batch_occupancy`'s checks run on the settled batch at H's admission, with exactly that step's preconditions: the dispatch binding is required, and views and receipts are not (NE:3046-3048). The step's substance is its precondition set. NE's "during ANALYZING" places it before views exist, which the settled spool still satisfies (R7).
  - **Binding.** After H's view and J2b's stage receipt, `capture_occupancy` and `bind_worker_occupancy` join:
    - the dispatch binding;
    - the receipt, with the matching view digest on its `outputRefs`;
    - this batch's mint map `candidateOrdinal → fact2`;
    - the stage spec's producer, with kind `provider` rederived from retained closures;
    - the inventories and the enumeration plan (NE:3099-3113).
  - **The projection** onto `TargetAttributionV2` (NE:3118-3126; ATOM:32-52):
    - `planId` from the retained Plan;
    - `sourceFactId` from the mint;
    - `producerClosure` from the stage spec;
    - `targetUniverse` from the minted fact;
    - the occupancy fields from the companion.
  - **Refusals:**
    - an extra or unknown `candidateOrdinal`;
    - a malformed companion, which refuses the batch's occupancy capture atomically (NE:3137-3138);
    - `PROVIDER_RETURN_UNBOUND_ENVELOPE`;
    - `PROVIDER_RETURN_HOST_AUTHORED`, which captures nothing (NE:3139-3142);
    - `TARGET_ATTRIBUTION_FACT_NOT_IN_PLAN`;
    - `TARGET_ATTRIBUTION_PROVIDER_OCCUPANCY_CONFLICT` over prior and current sidecars (NE:3110-3113; ATOM:50);
    - C15's `TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT` (NE:3144-3146).

    Routes follow FAULT:46-58 (item 22).
  - **Lawful omissions:**
    - the token is absent: occupancy-unknown, and **not** `required-output-pointer-omitted` (NE:3137-3141; FAULT:56-57);
    - syntax-only and clone or candidate stages carry no companion (NE:3134-3135);
    - syntactic rungs must omit (NE:3132).
  - **The output.** On `admitted`, H returns the `{domain: target-attribution, digest}` refs for J2b's `hostDerivedRefs`. On `omitted` or a refusal, it returns none (EXC:279).
- **Basis:** NE:3009-3150; EXC:259, EXC:276-282; ATOM:32-52; FAULT:46-58.
- **Rejected:**
  - **Binding before the receipt exists.** NE:3049-3052 requires the receipt and the view.
  - **Capturing anything from a refused batch.** EXC:279: "A refused batch captures nothing."
- **Forbidden substitutes:** occupancy from specifier text in syntax-only (NE:3134); a `producerClosure` from a caller argument; an attribution for a fact on no selected view.

### 16. The syntax join (law; E1's second-integrator legs)

- **Decision.**
  - **What E3 hands H.** E3 executes the syntax stage in the host (ME:578; MC:917) and hands H:
    - the stage coordinates: the core provider closure's stage;
    - the inert candidates of `parsed` files (ME:466-478);
    - the Coverage entries E3 maps from per-file outcomes (ME:384-415);
    - the symbol census for the syntax relations' symbol scopes (item 17).

    H admits them through items 5 to 14, with no shortcut. The interface is `admit_syntax_stage`, which E3 builds against (ME:712, ME:714).
  - **Syntax-specific joins:**
    - F9's `inspect_syntax_fact`;
    - the inventory exemption (NE:323-336);
    - the core provider closure as producer on syntax-universe records only (MC:435-443, MC:464);
    - no candidate from a non-`parsed` file (ME:410).

    A `backend-fault` reaches H with no Coverage and no envelope: E3 fails the step first (ME:392).
  - **Origin.** The syntax stage's producer is core code (MC:442; BP:676-683), so E3's records are host-minted.
    - A refusal of one at F1 to F9 is a host defect. It takes the host-internal row, as E1's own backend-fault route does (ME:392; item 22).
    - Its view-join keys, the three anchor keys included, are routed by item 14.4, where an E3 view is host-minted (r3).
  - **The syntax cause** `source-parse-error` under `input-closure-incomplete` (ME:390) admits only after SYN-1 and SYN-1F are accepted and E2s has updated the registries the inspector reads (`coverage.rs:317`; ME:709).
  - **The second integrator.** H5 integrates after E3 (M3P:307; ME:714-728). So H's acceptance scope includes:
    - **E3-T3's end-to-end leg:** Coverage per outcome row, including precedence with both kinds of file in one scope (ME:415);
    - **E3-T6's Coverage leg:** a TS unit whose provider is unavailable gives no syntax universe, and its required semantic Coverage is `unknown`/`provider-unavailable` (ME:620).

    H-C16 carries both.
- **Basis:** ME items 10, 13, 14b, 16 and 20 (ME:384-415, ME:466-482, ME:568-593, ME:607-622, ME:703-738); BP:676-683.
- **Rejected:** **a syntax fast path** that mints facts in E3. "The crate never mints `fact2`" (ME:477).
- **Forbidden substitutes:** any H call into `host/syntax.rs` (ME:618); a syntax record admitted into a TypeScript or Rust view.

---

## E. Inventories and the enumeration hand-off

### 17. Provider-attributed symbol inventories (law; X-H1)

- **Decision.** ENC requires that "Caller maps must already be owner-admitted" (ENC:166). H is the owner admission of every `SubjectInventoryV1` of kind `symbol`, before J2b's full join. It checks:
  - **the schema** (SIS), with SIS's 4 MiB `C` ceiling and no truncation (SIS `description`);
  - **the locator.** `(planId, parameterDigest, cellOrdinal, programOrdinal, kind)` equals an expected inventory of the Plan's `EnumerationPlanV1` whose binding is this child's universe and enumerator (ENC:108-109, ENC:115);
  - **completeness of the return.** The child returns exactly one census for each expected `(cellOrdinal, programOrdinal, symbol)` of its bindings (EXC:59). An omission refuses on the provider-return route. J2b's full join stays the authority over the whole expected set (item 19);
  - **the state law** (ENC:119-121):
    - `complete`: `examinedPaths` equals the host-derived symbol extent (ENC:119, ENC:186);
    - `partial`: `examinedPaths` ⊆ extent, with a required deficiency, and its known rows are kept (ENC:120);
    - `unavailable`: only for actual provider unavailability (ENC:121);
  - **the rows:**
    - `kind=symbol`;
    - `path` inside the symbol extent and never external (SIS `InventoryRowV1.path`; `ENUMERATION_INVENTORY_EXTERNAL_PATH`);
    - `nativeSubjectId` unique within the inventory;
    - `projections` naming Plan-selected `kind=detector` closures (ENC:186).

  The host does not recompute symbol extraction. That is the stated trust boundary (SIS `description`; NE:507-515; IE:1469-1470).
- **The carrier gap (X-H1).** The census is provider-attributed (IE:1466-1470; NE:89-91), and the providers produce it (CH14:513, CH14:539; M3P:214, F2's "symbols"). But neither TS2 nor Rust3 can carry it:
  - the candidate frame carries closed `FactCandidateV1` values (NE:2883);
  - the Coverage frame carries only `CoverageResultV3` entries (NE:2884, NE:3270-3276);
  - the terminals carry counts and commitments (DLV `StageResultV1`, `CompleteV1`);
  - EXC forbids a new frame name and makes inventories host-derived inputs, never stage outputs (EXC:259, EXC:265-270);
  - INC-5 keeps both protocols unchanged without a reviewed successor (AQP:400), and M3-L r1's item 1 adds nothing to either (ML1:98-117).

  Symbol-scope subjects are census rows (RPS:15; SIS). So a TS or Rust symbol-kind scope has no lawful D. The pre-Analyze request key also cannot carry a commitment over a census that does not yet exist (NE:3277-3282).
- **Decision within this law.** H3 implements the owner admission against the SIS record. Fixtures and E3's in-host census feed it; E3's census has no transport problem. **H3's provider leg, and every end-to-end TS or Rust symbol-scope control in H5, are gated on FA-2.** FA-2 also gates F2 and G3, which emit the census.
- **Basis:** ENC:115-123, ENC:166, ENC:186; SIS; IE:1462-1474; NE:89-95.
- **Rejected:**
  - **Inferring the census** from `declares` facts, from anchors or from the file population. I1 forbids each (MI:490-492).
  - **Refusing every TS Run** until FA-2. That is what happens anyway if FA-2 is late. The law records it as a gate, not as a behavior.

### 18. Host-produced inventory records (lead decision; X-H3, X-H5)

- **The gap (X-H5).** NCM says the inventory capability is "Produced by host discovery and enumeration, not by a language provider", in every mode (NCM:949). COV routes the six `inventory/*` cells to `discovery.rs` and `snapshot.rs` (COV:4226-4391). MB gives B "the discovery half" and C1 "the inventory bytes" (MB:414). But no law mints any of these:
  - the host-derived file and package `SubjectInventoryV1` outcomes;
  - the `file@enumerated` and `package@manifest-declared` facts, which carry zero anchors (IE:1006);
  - their scopes and Coverage.

  Yet MJ:377 and MC:892 require the host-derived inventories to exist before the full join.
- **Decision.** H3 derives and admits these records. They are facts and inventories, and H is the one owner that mints `fact2` and owner-admits inventories. H3 reads only retained records:
  - the sealed `snapshot2` inventory (C1);
  - `UnitMembershipV1` (B2-c);
  - the scope descriptor and `EnumerationPlanV1`'s extents (C4a).

  It derives extents through the evaluator's pure projections `project_enumeration_extent` and `project_enumeration_packages` (`enumeration.rs:132-135`, `:641`), so the extent law has one implementation (ENC:186).
  - **The file inventory.** Its rows are the binding's file extent (ENC:117, ENC:131).
  - **The package inventory.** One row per named first-party manifest. A parse failure gives `partial` / `source-syntax-invalid`, and every other known named row is kept (ENC:118).
  - Both inventories carry origin host-internal (MC:893).
  - **`file@enumerated` facts.** One per inventoried path, with the payload joined to the snapshot row (IE:986-990), meeting `coverageTotality` (IE:1455-1457). **`package@manifest-declared` facts:** one per package row.
  - **`vcs-change@vcs-reported` is not decided here.** C item 4 gives M3 no change observation (MC:287). What an M3 Run says for that relation is routed with X-H5.
  - **Grammar gating.** Inventory relations are exempt (NE:323-336).
- **The producer (X-H3).** These records need a producer and an enumerator: a Plan-selected `provider` closure that produced them (IDS:4729-4731). MC:458 states the principle: a provider that did not produce a record is not its producer.
  - In a syntax universe, that closure is the core provider closure (MC:435-440).
  - In a TypeScript or Rust universe, MC r7 forbids the core provider closure: "It is never the producer of any TypeScript or Rust record" (MC:443, MC:464). The language provider did not produce the records (NCM:949).

  **So no lawful producer exists.** The recommendation to MC's next revision and to CRC-1 is in X-H3. It gates H3's TS and Rust leg and H5.
- **Rejected:**
  - **Leaving the records unowned.** J2b's full join would then have no host-derived inventories (MC:892).
  - **Minting them under the language provider's closure.** That is false attribution (MC:458).
  - **Putting the derivation in J2b's `analysis.rs`.** It would split the inventory law across two modules, and the facts would still need H's admission.

### 19. The hand-off to J2's full `admit_enumeration` (lead decision)

- **Decision.**
  - **What H returns to J2b.** For each settled child and each E3 stage:
    - the admitted record set: `fact2`, `scope2`, `coverage2` and `view2`, in temporary custody;
    - the target-attribution refs;
    - the admitted symbol inventories, with origin `provider-return` for a provider's census (item 17), and host-internal for E3's census and for item 4's terminal outcomes.

    Once per invocation, H also returns the host-derived file and package inventories with origin host-internal (item 18).
  - **What J2b does.** After every stage return is admitted and before `derive_evaluation`, J2b runs the full `admit_enumeration`. In the product that is `inspect_enumeration_join` over the retained inputs (`enumeration_join.rs:1329-1341`). `derive_evaluation` re-runs it in reconstruction (`input_reconstruction.rs:439-459`) (MJ:377; MC:892-895). The missing-record refusal `ENUMERATION_INVENTORY_MISSING_RECORD` (ENC:111) is J2b's: only the complete expected set shows it.
  - **Origin routing** (MC:893; ENC:159-160; FAULT:46-58, FAULT:82-90):
    - a refusal naming a provider-attributed inventory takes provider-return and `EVALUATION.INPUT_REFUSED`;
    - one naming a host-derived inventory takes host-internal and `HOST.INVARIANT_VIOLATED`.

    H's origin tag is the only input to that choice. "Origin is recorded on the fault observation after refusal; it is not an admit parameter" (FAULT:57-58).
  - **H never calls the full join** (H-C20), as C4 does not (MC:896).
- **Rejected:**
  - **H calling `inspect_enumeration_join` per child.** A per-child call cannot see a whole missing inventory. The full join is one act over the complete set (ENC:111; MC:892).
  - **J2b inferring origin** from the inventory's content.

### 20. What I1-b2 reads (record of MI item 8)

| MI:398 input | Where I1 reads it | H's join | Control | Gate |
|---|---|---|---|---|
| `imports` facts at `resolved-target` | 2.3, edges (MI:110-127) | items 5–8 | H-C4 to H-C7 | FA-2 for provider runs |
| `unresolved-edge` facts with payload relation `imports` | 2.3 (MI:128); 2.6 (MI:188-190) | item 7 | H-C6, H-C9 | — |
| `TargetAttributionV2` occupancy | 2.3, target (MI:116-120) | item 15 | H-C15 | the token negotiated |
| `imports`-cell symbol inventories, with paths | 2.3, source vertex (MI:113); 2.5(b), census (MI:155-160) | item 17 | H-C17 | FA-2 |
| exact (`imports`, `resolved-target`) scopes, with subjects, and their Coverage | 2.5(b) step 3 and (c) (MI:161-174) | items 9–12 | H-C8 to H-C11 | FA-2 |

- **The shapes are fixed by I1-b2's fixtures** (MI:399; MIU:32, MIU:42-80). H-C19 checks that H's admitted records over the QCM projects equal those shapes.
- **Without FA-2,** a real TS Run's importers have no unique inventory row. Every edge is then uncertain and every subject indeterminate (MI:113-115, MI:121-125; MC:998). That fails closed, but the rule can never pass or fail. See the owner note.

---

## F. Indeterminacy, routes and operating rules

### 21. A missing rung is indeterminate (DR-G25) (law)

- **Decision.** H's part of "A missing required TypeScript semantic rung is typed Coverage-indeterminate; silent syntax fallback fails" (REG:370; COV:5056; AQP:113):
  1. **Every requested key gets an entry.** Each requested key of a settled child has exactly one admitted entry, from the provider, the terminal or the pre-Analyze conversion, or the child faulted (items 3 and 12). A missing rung is that entry's typed deficiency, never an absent entry.
  2. **No Coverage for a child that did not run:** an unselected enumerator, a closure not installed, a null universe. The execution-input account discloses those (ENC:69-77; MJ row 27).
  3. **No path from a provider outcome to the syntax stage.** H never calls E3. It admits a syntax record only from E3's stage of a Plan-bound syntax universe (ME:607-622; NE:253-259).
  4. **A syntax fact never discharges a TS or Rust scope.** H admits it only into its own syntax-universe view (item 14). Matching is on relation, rung and both universes (NE:366-370; ME:610).
  5. **Three routes stay distinct** (COV:5070, the method):
     - stale input is C3's pre-Plan request-rejected 2 (NE:3525; MJ row 25);
     - provider-unavailable is indeterminate 3 (MJ rows 27 and 31);
     - an operational fault is 4 (MJ rows 30 and 32).

     H supplies first-hand evidence only for the last two, and never converts one into another.
- **The D9 reduction is J2a's.** `outcomes.rs` is G25's co-owner (BP:1029; MJ item 10).
- **Forbidden substitutes:** a "degraded mode" (ME:617); an absent entry standing for a missing rung; a provider fault reported as unavailability.

### 22. Refusal routes: existing rows only (law)

| Refusal family | Origin | Public row | Basis |
|---|---|---|---|
| Fact join, F1 to F9, on a provider return (items 5–8), including item 7's per-stage bound | producer boundary | MJ row 30 (MJ:676): operational-failed 4, `PROVIDER.PROTOCOL_VIOLATION` / provider-protocol, `domainDetail` absent, key in the operational record | NE:3529; NE:3837-3843; DLV:1169 |
| **Every key of the owner's view-join call** (F10; items 10 and 14), for any record | by the view's origin | **item 14.4's table, the only authority for these keys. This item restates none of it.** | item 14.4 |
| Coverage bijection with the request, on provider-authored entries: a `Coverage` frame or a terminal (item 12) | producer boundary | MJ row 30 | NE:3277-3282, NE:3529 |
| Closed world (item 13), once FA-1 is accepted | producer boundary | MJ row 30 | NE:3529 (FA-1) |
| Occupancy (item 15) | provider-return | operational-failed 4, `PROVIDER.PROTOCOL_VIOLATION` / provider-protocol, `EVALUATION.INPUT_REFUSED` (MJ row 36's codes) | FAULT:46-53; NE:3148-3149 |
| Host-authored occupancy | host-internal | operational-failed 4, `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant, `HOST.INVARIANT_VIOLATED` | FAULT:53-54 |
| Provider symbol inventory (item 17) | provider-return | as occupancy | MC:893; ENC:159-160 |
| A refusal outside the view-join call of a host-minted record: item 11's pre-Analyze conversion, item 16 and item 18 | host-internal | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant, `HOST.INVARIANT_VIOLATED` (MJ row 29's codes, MJ:675) | NE:3573; ME:392 |
| Admission work bound (item 23) | host-internal | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant, `WORK.BUDGET_EXHAUSTED` (MJ rows 11 and 21's codes) | MJ:657, MJ:667 |
| Over-bound subject scope (item 9) | request | request-rejected 2, `REQUEST.UNSATISFIABLE`, `PROJECT.SCOPE_LIMIT`, after S-B (MJ row 22) | MJ:402; X-H6 |
| Clean `Unavailable` / `BudgetExhausted` (item 4) | not a refusal | indeterminate 3 by the primary deficiency (MJ row 31) | NE:3849-3855 |

- **No new public code,** class, exit, fault cause or detail. Internal keys stay diagnostic (NE:3546-3555; FAULT:54-55).
- **Record note R-J1.** MJ row 36 is titled "Replay refusal (X5)". Its codes are also reached from H's provider-return refusals, before any replay. J2a's projection takes that origin with the same row (record correction below).

### 23. Purity, bounds, cancellation and determinism (lead decision)

- **Decision.**
  - **Pure.** H does no I/O and takes no lock or ledger. It imports no security, storage, platform or lifecycle crate and reads no environment. It reads retained records and writes only into the temporary custody maps that J2b hands it. This is X5's purity pattern (`fact_admission_tests.rs:680-697`; MJ:399).
  - **Bounded.** `ADMISSION_LIMITS` are host constants: the traversal budgets for the identity and evaluator owners that H calls. They are sized so that the largest return D3's spool bound and the protocol limits permit is admitted (MD:497, MD:512; NE:2929-2942, NE:2961-2967).
    - They are charged to no operation ledger: replay's precedent (X5:45).
    - A crossing on a return D3 accepted is a host invariant (item 22).
    - H1 fixes the values with an exact-boundary test, X5's pattern (`fact_admission_tests.rs:559-628`).
  - **Cancellation.** H checks the host cancellation source between stage returns. A cancellation observed during admission stops it and retains nothing; the class follows J's phase rules (MJ item 8; NE:3421-3426). A cancelled child never reaches H (MD:624).
  - **Deterministic.** H's output does not depend on child completion order, thread count or batch boundaries. Records are canonical sets, and per-universe maps are in canonical order (AQP:322-325; OPP:275; ME:434).
  - **Observable, not semantic.** H's work is the admission half of OPP's "admission and replay" phase span (OPP:246). Refusal keys go to the operational record (NE:3546-3555). No operational field enters a semantic identity (OPP:247).
- **Rejected:**
  - **Charging admission to the attempt ledger.** Pure semantic work would exhaust caps meant for native custody work (X5:45).
  - **Wall-clock bounds.** They make outcomes nondeterministic (ME:439).

### 24. U-5 and U-6: H's half (record)

MB:406 routes U-5 and U-6 (NE:864-870) to "H and J".
- **H's half.** U-6's cross-unit `external-module-boundary` edges are ordinary `unresolved-edge` facts on the importing side, admitted at item 7. H never narrows a multi-unit scope: it admits per-universe Coverage and aggregates nothing.
- **J's half.** U-5's per-unit predicate evaluation and the `narrowed=false` invariant belong to evaluation (`derive_evaluation`; MJ:378).

---

## G. Controls

Each control has a fixture or a source pin. Synthetic fixtures are labelled and no compiler qualification is claimed, as in X5's tests (`fact_admission_tests.rs:1-5`), and all live in `crates/host/src/fact_admission/*_tests.rs` or `crates/host/tests/admission_tests.rs`.

| ID | Control | Item | Unit |
|---|---|---|---|
| **H-C1** | A fault, a nonzero exit, a missing EOF or a cancellation after some `FactBatch` frames gives H nothing. H's entry type is constructible only by D3. Shares D3-T22 and D3-T23 (MD:633). | 3 | H5 |
| **H-C2** | A refusal in the last stage of a multi-stage Analyze leaves no record of any of its stages in custody. | 3 | H5 |
| **H-C3** | A clean `BudgetExhausted`, and a clean post-Analyze `Unavailable`, after `FactBatch` frames: zero `fact2`, every terminal entry admitted, the stage `partial`, MJ row 31's route. | 4 | H2, H5 |
| **H-C4** | NT-3, finding masquerade. Each refuses before any `fact2`, on MJ row 30: an unregistered relation; another relation's rung (`unresolved-edge@enumerated`); an unrequested relation; an extra payload member (a `finding` or `verdict` field); a foreign universe; confidence 999,999. | 5 | H1 |
| **H-C5** | The payload adapter refuses, and never repairs, non-NFC text, a negative integer, a non-canonical CBOR encoding and a per-rung forbidden field. An admitted fact's `payloadDigest` is the SHA-256 of its `C` bytes, and its `payloadSchemaDigest` is the RPS file digest. | 6 | H1 |
| **H-C6** | Anchor count and `file` joins, on the identity owner's keys (F4 to F6): an inventory fact with an anchor, and a code or `unresolved-edge` fact with none (`anchor cardinality`); a `file` payload whose anchor names another path (`anchor foreign path`); a `file` payload whose digest or length disagrees with the sealed row (`file content join`, `file length join`). | 5, 7 | H1 |
| **H-C7** | The producer. A frame whose `producer` text differs from the stage spec still yields the stage spec's `producerClosure`. A stage spec naming a non-provider closure refuses. The core provider closure on a TypeScript record refuses: C2-T13a's admission leg (MC:471-477). | 8 | H1 |
| **H-C8** | NE §4.1a's cases at the producer boundary, through the owner's view-join call over H's D (NE:1962-1975): a claimant-chosen commitment; a narrower partition; a count mismatch; a key universe outside the scope; `complete` over an admitted unresolved edge; `incomplete` over an exhaustive partition, which admits; a duplicate subject; a caller-chosen schema digest. On a provider-return view each refuses as `COVERAGE_PRODUCER_ADMISSION:<cause>`, on the row item 14.4a gives it. | 9, 10 | H2 |
| **H-C9** | The census (r2). A source pin shows that no child of `fact_admission/` passes a census or a dialect, and that none calls `inspect_coverage_producer`. Fixtures: an `unresolved-edge` fact in the view whose referrer is in D makes a `complete` entry refuse, and the same view without that fact admits. | 10 | H2 |
| **H-C10** | The dialect (r2). The owner derives the source-variant table from the retained universe frame (`view_joins.rs:470-479`). A source-path `clones` scope over an unsupported variant refuses `complete` (CB7-MUST-1) through that call, with no dialect supplied by H. | 10 | H2 |
| **H-C11** | NT-5, Coverage-domain mutation. A missing, extra, reordered or re-keyed entry refuses. A source pin shows that no code path writes a provider entry's `coverage`, `deficiency`, `nativeCause`, `resolutionCompleteness`, `closedWorld` or `derivationKinds`, and that host-minted entries are `unknown` only. | 11, 12 | H2 |
| **H-C12** | The pre-Analyze conversion equals NE:3234-3264 field by field, including the fixed `closedWorld`, and reads no worker stage id or coverage. | 11 | H2 |
| **H-C13** | Closed world: `deadCodeRepairEligible: true` beside an admitted `require-nonliteral` edge refuses. This is wired after FA-1 and test-only before. | 13 | H2 |
| **H-C14** | Views (r2). Each of these refuses: a scope outside the view; a Coverage the view does not name; an overlap; a provisional `coverage2` whose identity disagrees with the inspector's. Each assembly key, forced by a fixture that corrupts H's own assembly, takes the host-invariant row on a provider-return view and on a host-minted view alike. No overlay record survives a refusal. | 14 | H2 |
| **H-C15** | Occupancy, each case of item 15 with its FAULT route: an extra ordinal; a malformed companion; an unbound envelope; a host-authored envelope (captures nothing); a fact not in the Plan; a provider occupancy conflict; C15. The token absent is lawful, and syntax-only has no companion. | 15 | H4 |
| **H-C16** | Syntax: E3-T3's end-to-end leg and E3-T6's Coverage leg (ME:415, ME:620); a Markdown-anchored code fact refuses `SYNTAX_CAPABILITY_UNSUPPORTED_FACT`; the inventory exemption holds; `source-parse-error` admits only under `input-closure-incomplete`, after E2s. | 16 | H5 |
| **H-C17** | Symbol inventory owner admission: a wrong locator; `examinedPaths` outside the extent; an external path; a duplicate `nativeSubjectId`; `complete` with `examinedPaths` ≠ extent; `partial` keeping its known rows; an omitted owed census refusing on provider-return. | 17 | H3 |
| **H-C18** | Host-derived inventories: file totality; a malformed `package.json` beside a named sibling gives `partial` with the sibling kept (ENC:118); origin tags. C4-T19's H leg: an available TS `imports` population reaches J2b's full join with the actual admitted inventories (MC:947-955). | 18, 19 | H3, H5 |
| **H-C19** | I1's shapes: H's admitted records over QCM's `cycle`, `self`, `acyclic`, `unresolved` and `dynamic` projects equal I1-b2's fixture shapes. Fixture-level until FA-2, then provider-produced. | 20 | H5 |
| **H-C20** | Source pins. The root is unchanged and X5's pin stays green. The children: no security, storage, platform or lifecycle import; no `fs::`, `env::`, `Command`, `Mutex`, `static mut` or `unsafe`; no `replay_run`, `ReplayedRun`, `run3:`, verdict, `derive_evaluation` or `inspect_enumeration_join`; no call into `host/syntax.rs`. | 2, 19, 21, 23 | each |
| **H-C21** | DR-G25's three routes, one fixture each, none converted into another: a stale import (2), a provider unavailable (3), a protocol fault (4). A TS provider that is unavailable gives no syntax universe. | 21 | H5 |
| **H-C22** | Shuffled child completion order, and concurrency 1 against N, give byte-identical custody maps. A return at the exact bound admits. A bound crossing takes the host-invariant row. | 23 | H1, H5 |
| **H-C23** | INC-2: an echo of `snapshot2` or `plan2` that differs from the Plan's refuses (NE:3158-3161). | 3 | H5 |
| **H-C24** (r2, RF-1) | Anchor routing, six fixtures.<br>- **On a provider-return view:** an anchor naming a blob outside the sealed inventory, an anchor running past its blob, and an anchor whose start or end splits a UTF-8 character refuse `ANCHOR_SOURCE`, `ANCHOR_RANGE` and `ANCHOR_UTF8` respectively, on MJ row 30.<br>- **On an E3 syntax fact:** the same three failures refuse with the same keys, on the host-invariant row.<br>- **A source pin** shows that no child of `fact_admission/` reads anchor bytes outside `inspect_plan_view_joins`.<br>Item 18's inventory facts carry no anchors (IE:1006), so they have no anchor case. | 5, 14, 16, 22 | H2 (provider leg), H5 (E3 leg) |
| **H-C25** (r3, RF-1) | The 14.4 router is one pure function of (owner key, view origin). Unit tests use the owner's real key spellings:<br>- **Item 11's two origins.** A clean `BudgetExhausted` terminal entry that declares a cause its carrier forbids refuses `COVERAGE_PRODUCER_ADMISSION:native.coverage-cause-must-be-null:…` on MJ row 32. A terminal entry whose commitment mismatches refuses on MJ row 30. The same two failures on a pre-Analyze conversion entry, forced by a fixture that corrupts H's own conversion, take the host-invariant row.<br>- **Suffixed keys.** `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH:file@enumerated:a.ts` on a provider-return view takes row 32 by its listed token, not the catch-all. `SUBJECT_SCOPE_PARTITION_OVERLAP:imports@resolved-target:s` and `SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER:imports@syntactic` take the catch-all.<br>- **The tie rule.** A joined key with only `RC-2:` faults takes row 30. One with an `RC-6:` fault takes row 32. One with both `native.subject-scope-commitment-mismatch` and `native.coverage-cause-required:…` takes row 32.<br>- **One table.** A source pin shows that the code for items 10, 11 and 22 calls the router and holds no second route table. | 11, 14, 22 | H2 |

**Crash matrix.** H adds no durability point and writes no store, so it adds no X9 row. Its units touch no `crates/security`, `crates/storage` or `host/src/finalization.rs` file, so they owe no lead set under the rerun rule MJ:731 states for J's units.

---

## H. Successors

| ID | What | Kind and review | Owner | Needed before |
|---|---|---|---|---|
| **FA-1** | NE §10 fault-law passage, NE:3849-3850. On a clean non-Complete terminal, candidates before the terminal are discarded and its exhaustive terminal Coverage is admitted (item 4; X-H2). It also adds `native.coverage-closed-world-mismatch` to NE:3529's producer-boundary row (item 13). | native passage successor; **ACCEPT-DESIGN-UNIT** | native owner | H2's closed-world wiring. Item 4 needs nothing: it applies the retained selectors. |
| **FA-2** | **The symbol census carrier** (X-H1). Drafted as a design unit and in review with Codex. This law depends on none of its details. Lead recommendation:<br>(a) a capability-token-negotiated payload version on the existing per-stage `Coverage`/`CoverageV3` and terminal frames. It carries each owed `SubjectInventoryV1` symbol census, with no new frame name (the `target-attribution-v2` pattern, NE:3061-3064; EXC:270);<br>(b) for symbol-kind keys, the Analyze request carries the host-derivable **symbol extent** commitment as a request coordinate. The returned key carries the `scope2` commitment over the census, which the host recomputes from the admitted census. This supersedes NE:3279's equality for those keys only;<br>(c) a census-free host scope, `subjects: []`, for the pre-Analyze conversion;<br>(d) F2's and G3's emission duty. | native protocol successor to NE §9.4, §9.6 and §9.7, reviewed with **M3-L's next revision** (AQP:400); **ACCEPT-DESIGN-UNIT** | native owner; protocol owners (DR-G10); M3-L | D2b's payload codec; F2; G3; H3's provider leg; H5's symbol-scope legs; J2's TS and Rust path |
| **M3-C r8 / CRC-2** (X-H3) | A third admitted use of the core provider closure: producer and enumerator of the three inventory relations' records in **every** universe. It is a `semanticClosures` member whenever an inventory cell is requested. C2-T13 and C2-T13a are extended to match, and C4a's `exec-plan2` gains one host inventory stage per universe. | M3-C revision plus identity successor; **ACCEPT-DESIGN-UNIT** for CRC-1 | C's owners; identity | C4a; H3's TS and Rust leg; H5 |
| **S-B field** (X-H6) | The subject-scope `subjects` bound (100,000 entries; the 4 MiB descriptor) as an S-B field reachable after execution, with its subject spelling | C's S-B successor | native owner | H5's large-scope path |
| **ML next** (X-H4) | M3-L's INC-2 item (ML1:206, ML1:210) reads "no admitted provider frame **or Plan-selected in-core producer stage**", so that E3's syntax facts and item 18's inventory facts are lawful. M3-L r3 is being drafted. | M3-L revision | lead | M3-L acceptance |
| **M3P-H** | Planning record: H's units H1 to H5 (item 25); the X-H items; FA-2, C's next revision and CRC-1's widening as pre-day-0 law rounds; H's absorption of host inventory records (X-H5) | planning record | lead | — |
| **CH14-H** | `crates/host/src/fact_admission/` child paths | record, at the next CH14 refresh | — | — |

Not successors:
- **X5.** Its replay join and pin are unchanged (item 2).
- **J1.** Its J-η placement is implemented unchanged (item 19). Row 36's reach is a record correction.
- **I1.** It "adds no admission law" (MI:397).

---

## I. Units (item 25)

**25. Units.**

| Unit | Content | Integration after | Built against, and gates | Review | Size | Days | Finishes |
|---|---|---|---|---|---|---|---|
| **H1** | `fact_admission/candidates.rs`: items 5 to 8. The payload adapter, the registry and ladder checks, anchors, source and universe joins, confidence, `unresolved-edge` facts, the producer and `fact2`. Also `ADMISSION_LIMITS` (item 23). H-C4 to H-C7. | P0; D2b (the CBOR reader and decoded candidates) | identity and evaluator owners; retained-record fixtures | ACCEPT-UNIT | M | 2 | 6 |
| **H4** | `fact_admission/occupancy.rs`: item 15. H-C15. | H1; D2b | ATOM; FAULT | ACCEPT-UNIT | S | 1 | 7 |
| **H2** | `fact_admission/{coverage,views}.rs`: items 9 to 14. D, the provisional scopes, Coverage and views, the staging overlay, the owner's view-join call and its routing (item 14.4), host-minted entries, the bijection, and closed world (unwired until FA-1). H-C3, H-C8 to H-C14, H-C24's provider leg and H-C25. | H1 | **E2s** for the `source-parse-error` leg; **FA-1** for the closed-world wiring | ACCEPT-UNIT | M | 2 | 8 |
| **H3** | `fact_admission/inventory.rs`: items 17 to 19. Symbol-census owner admission; host-derived file and package inventories and inventory facts; origin tags. H-C17, H-C18 (unit leg). | H1 | **FA-2** for the provider leg; **M3-C r8 / CRC-2** (X-H3) for the TypeScript and Rust inventory leg; fixtures and E3's census before | ACCEPT-UNIT | M | 2 | 8 |
| **H5** | `fact_admission/stage.rs` and the root's `mod` lines: the entries, the atomic assembly and the real wiring. That means D3's settled value, C4a's Plan, stage specs and bindings, F1's TS transport fixtures, and E3's stage. Also the end-to-end and second-integrator controls: H-C1, H-C2, H-C16, H-C18 (J2b leg), H-C19, H-C21 to H-C23, and H-C24's E3 leg. | **C4a (19)**, F1 (15), E3 (14), D3 (7), H2, H3, H4 | **FA-2** for the symbol-scope legs; **M3-C r8 / CRC-2** for the inventory leg; **S-B** for the large-scope path; SYN-1 and E2s | ACCEPT-UNIT | L | 3 | **22** |

- **Review.** Every unit is an inventory successor, numbered at launch after a `git ls-files` check (ME:729), and reviewed with `inventoryCandidateAssessment` (MIU:20-21).
- **DAG effect, against M3P r6's table (M3P:282-318):**
  - H1 runs on days 4 to 6, after D2 (M3P:298). H4 finishes on day 7. H2 and H3 finish on day 8. All four are off the host chain.
  - **H5 is M3P's H row:** 3 days after C4a (19) and F1 (15), finishing on **day 22** (M3P:307). M3P's 33-day conditional host chain is unchanged (M3P:320-324). So are J2's day 25 and the zero-slack X12d branch that also reaches J2 on day 22 (M3P:324).
  - E3's 14 days of slack are unchanged. E3 builds against H2's interface and integrates before H5 (ME:714-738).
  - **The figure holds only if the new law rounds land in time.** FA-2 and M3-C r8 / CRC-2 must be accepted before day 0, or at the latest before D2b starts (day 2) for FA-2's codec and before C4a starts (day 16) for X-H3. M3P:257-261's list of pre-day-0 law rounds gains both. If either is late, the first unit that needs it (D2b, F2, G3 or C4a) waits for it day for day, and the path runs through it.
- **Effort.** 10 unit-days in all (2 + 1 + 2 + 2 + 3). M3P counted 3 on the chain, and only H5's 3 are there.

---

## Cross-law items

Each item names the law that must change. None is decided by this law beyond its own lead decisions.

- **X-H1. The provider symbol census has no carrier.** It is for the **native owner (FA-2)**, with **M3-L's next revision**. FA-2 is now drafted as a design unit and is in review with Codex, and M3-L r3 is in review with Grok. This item stands, and this law depends on none of their details.
  - **The obligation.** The census is provider-attributed (IE:1466-1470; NE:89-91; CH14:513, CH14:539), and symbol-scope subjects are its rows (RPS:15; SIS; ENC:93).
  - **No carrier exists.** Neither TS2's nor Rust3's frames carry it (NE:2883-2884, NE:3270-3292; DLV `StageResultV1`, `CompleteV1`). EXC forbids a new frame name (EXC:270). INC-5 keeps both protocols unchanged without a reviewed successor (AQP:400), and M3-L r1's item 1 adds nothing to either (ML1:98-117).
  - **The key cannot be computed in advance.** NE:3279 requires the returned key's commitment to equal the request key's. The request is built before spawn (NE:3230-3233), when no census exists.
  - **The consequence.** Without FA-2:
    - no TS or Rust symbol-kind Coverage can be admitted;
    - F2 and G3 cannot deliver "symbols and Coverage" lawfully (M3P:214-215);
    - I1's rule can never decide on a real Run (item 20).
  - The recommendation is FA-2's row.
- **X-H2. Clean non-Complete terminals.** It is for the **native owner (FA-1)**. NE:3849-3850's "facts before the terminal are admitted" contradicts the retained candidate dispositions (DLV:1140-1141, DLV:1152, DLV:1164; RPP:597-598), which NE §0 does not supersede (NE:126, NE:129). M3 applies the retained selectors (item 4). MD's F7 (MD:623, MD:1107) is answered here. MD's next revision cites item 4.
- **X-H3. No lawful producer for host-produced inventory records in TS and Rust universes.** It is for **M3-C's next revision and CRC-1**.
  - NCM:949 says the host produces inventory records in every mode.
  - MC r7 forbids the core provider closure on any TypeScript or Rust record (MC:443, MC:464).
  - MC:458 forbids attributing a record to a provider that did not produce it.
  - IDS requires a `provider` kind (IDS:4729-4731).

  The recommendation is the M3-C r8 / CRC-2 row. It asks for one bounded exception to MC:443, limited to the three inventory relations.
- **X-H4. L's "no fact without a producing frame".** It is for **M3-L's next revision** (r3, being drafted beside FA-2). M3-L's INC-2 item forbids "host-minted facts without a producing frame" (ML1:206, ML1:210). Grok's review of H r1 records that the sentence stands in L r2 (`reviews/grok-fact-admission-h-r1/REVIEW.md`, "What holds"). This item stands, and this law depends on none of r3's details. Read literally, that forbids E1's in-host syntax facts (ME:477-478; MC:435-440) and item 18's inventory facts (NCM:949). The fix is the "ML next" row's wording.
- **X-H5. Nobody produces the inventory capability's records.** It is for **M3P's next revision (M3P-H)**, and for MC and the native owner on `vcs-change`.
  - B owns the discovery half and C1 the bytes (MB:414). MJ:377 and MC:892 assume the host-derived inventories exist. No unit mints them.
  - H takes them by lead decision (item 18), which M3P-H records.
  - **Still open:** what M3 says for `vcs-change@vcs-reported`, given C item 4's "no Git object reader" (MC:287). That goes to MC's next revision and the native owner. This law makes no claim for it.
- **X-H6. The subject-scope bound after execution.** It is for **C's S-B successor**. IDS bounds `subjects` at 100,000 and the identity encoder bounds the descriptor at 4 MiB (IDS:674; IE:117). C's item 5 found that `snapshot2`'s 4 MiB descriptor holds about 27,000 rows (MC:307-323; M3P:210, "S-R"), and symbol scopes over large T2 repositories will meet the same wall. S-B carries the snapshot and dependency bounds today (MC S-B row; MJ:402). It should gain the scope field, refusing typed and never truncating (NE:4280). Whether a census key may be partitioned across several disjoint scopes (IE:1431-1440) is FA-2's question.

## Record corrections (record only)

- **MC:885 (C r7, unchanged from r6).** "the inventory joins at `:107-111`" should read `:108-111`. ENC:107 is the `nativeContextDigest` join, which step 15's own fourth bullet checks (MC:889). This is for C's next revision.
- **MJ row 36 (R-J1).** Its codes are also reached from H's provider-return refusals before any replay (item 22). The record note is for J2a.
- **MD F7** (MD:623, MD:1107) is answered by item 4.
- **M3P:216.** H's units are item 25's, and the X-H items join the pre-day-0 law list (M3P-H).
- **CH14:482.** The child paths of item 2 (CH14-H).

## Forbidden substitutes

- **Admission before or outside settlement:** a candidate, Coverage entry, companion or census admitted from a non-clean settlement, from a partial stream or per batch (items 3 and 4).
- **Facts that should not exist:** a fact admitted before a clean `Unavailable` or `BudgetExhausted` terminal at M3 (item 4); a fact for an unregistered relation, an off-ladder rung, an unrequested relation, a foreign universe or a confidence below 1,000,000; a repaired payload (items 5 and 6).
- **Coordinates from the wrong source:** a coordinate taken from a worker echo; a producer from the frame; a language provider's closure on a record it did not produce (items 3 and 8).
- **Wrong scopes:** D from a provider's `examinedUniverse`; symbol subjects inferred from facts, anchors or files; a truncated or sharded scope (item 9).
- **A weakened census or dialect:** a census or dialect supplied by H, by a provider or by a caller of H; a direct call of `inspect_coverage_producer` on H's path (item 10).
- **Anchors and staging (r2):** an anchor byte or UTF-8 check outside `inspect_plan_view_joins`; a provider anchor refusal routed as a host invariant, or an E3 one as a provider fault; a record leaving the staging overlay before its view-join call passes (items 5 and 14).
- **Routing (r3):** a second route table for view-join keys outside item 14.4; a key matched by anything but its prefix token; an anchor key on MJ row 32 (item 14.4).
- **Coverage that should not exist:** an edited provider entry; an unknown-to-covered conversion; a host-minted entry other than `unknown`; Coverage for a child that did not run (items 11 and 12).
- **Syntax:** any path from a provider outcome to `host/syntax.rs`; a syntax record in a TypeScript or Rust view (items 16 and 21).
- **Inventories and hand-off:** an inventory admitted without owner admission; an origin guessed from content; H calling the full enumeration join (items 17 to 19).
- **Codes:** a new public code, class, exit, fault cause or detail; a wildcard route (item 22).
- **Operation:** I/O, a lock or a ledger in admission; order-dependent output (item 23).
- **X5:** any edit to X5's replay join or its pin (item 2).

## Consistency with accepted and drafted laws

- **MC (r7, accepted).** H supplies the inputs of the full admission that MC splits from step 15, and never makes that call (MC:885-896). r7 narrows row 8 only, which H does not cite (item 8). It uses the core provider closure exactly as item 9 admits it (MC:433-443), and asks for one more use (X-H3). C4-T19's H leg is H-C18.
- **ME (r3).** H owns admission of the syntax stage's facts and Coverage (ME:477, ME:578). It carries E3-T3's and E3-T6's H legs as the second integrator (ME:714-728). The `clones-near` envelope stays J2's (ME:718).
- **MI (r2).** Item 20 maps each of MI item 8's inputs. "I1 adds no admission law" (MI:397) holds.
- **MJ (r4, accepted).** H is J-η's first half (MJ:377). Refusals project through MJ item 10's existing rows (item 22). Custody is 5.4a's (MJ:399). r4's R10a (MJ:325) moves no sentence H relies on.
- **M3-L.** It has no accepted snapshot, so H takes no rule from it. H adds no wire member (AQP:400). Its census need goes to FA-2 and L's next revision (X-H1), and the fact-construction wording to L's next revision (X-H4).
- **MB (r2).** H takes U-6's admission half (item 24). B's discovery half and C1's bytes feed item 18 unchanged (MB:414).
- **MD (r3, accepted).** H consumes D3's clean settlement (MD:622) and D2b's CBOR reader (MD:335), and answers F7 (item 4).
- **AQP and OPP.** Refusal, not degradation (AQP:112, item 21); the determinism suite (AQP:322-325; OPP:275, item 23); INC-2 (AQP:388); the admission phase span (OPP:246).
- **X5 (r3).** The module is the same, the replay join is unchanged, and the pin stays green (item 2).

## Open questions for the owner

**None without a recommendation.** Every choice above carries the lead's recommendation.

**Flagged for the owner (non-blocking lead decisions the owner may reverse):**
1. **Without FA-2, the preview rule cannot decide on any real TypeScript repository.** Every `module-import-cycle` answer is indeterminate, because no symbol census reaches the host (item 20; X-H1). FA-2 is a protocol successor, so it changes TS2 and Rust3 payloads through a negotiated token. It should join the pre-day-0 law rounds.
2. **A provider that exhausts its budget after finding a cycle cannot fail the Run on that cycle.** The Run is indeterminate (item 4).
3. **H absorbs the host-produced inventory records** that no unit owned (item 18; X-H5). This adds one M unit (H3) off the critical path.
4. **The core provider closure would produce inventory records in every universe** (X-H3). Every core release is then a new inventory producer, as it already is a new syntax producer and detector (MC item 9; ME owner note 4).

## Review questions

R1 to R8 were r1's questions, and Grok's r1 review answers them (`reviews/grok-fact-admission-h-r1/REVIEW.md`). r2 asked R9 to R11, which Grok's r2 review answers (`reviews/grok-fact-admission-h-r2/REVIEW.md`). They are kept below for the record. r3 asks:
- **R12 (RF-1).** Is item 14.4 now the only routing authority, with items 5, 10, 11, 16 and 22 referring to it and restating nothing? Is prefix-token matching exact for every key the owner returns?
- **R13.** Are 14.4a's classes of `COVERAGE_PRODUCER_ADMISSION` causes, and its tie rule, faithful to J1 r4's rows (MJ:676, MJ:678) and to NE:3529, NE:3538 and NE:3541? Is it right to send the prerequisite and totality keys to row 32?

r2's questions:
- **R9 (RF-1).** Does item 14.4 close RF-1? The anchor keys now run once, in the owner's call over the provisional view. They take MJ row 30 on a provider-return view and the host-invariant row on a host-minted view. Every assembly key is a host invariant.
- **R10.** Do F3's pair check and F7 make `FACT_SCOPE_JOIN` unreachable by a lawful provider error, so that routing it as a host invariant is sound?
- **R11 (item 10).** Is moving the producer boundary into the owner's view-join call right, given RC-2's per-view census (IE:1481; NE:3351) and the crate-private dialect table (`capability_support.rs:279`)?
  - A provider could put an `unresolved-edge` fact in the view of a stage that carries no scope of the fact's payload relation. The per-view census law then counts that fact toward no Coverage.
  - Is that lawful, or is it a contract gap for the native owner?

## Not claimed

- **Nothing was run.** No code, build, test or matrix run was done for this law. Product facts come from reading main `cd5958b`. Every cited file there equals `3e64266`'s.
- **No G23 or G25 qualification.** That is M6 (COV:5004, COV:5056). H prepares them.
- **No contract, schema, register row, gate or threshold is changed.** FA-1, FA-2, M3-C r8 / CRC-2, S-B's field and L's next revision carry the changes, under their own reviews.
- **No protocol change.** FA-2 is a recommendation to its owners.
- **No `vcs-change@vcs-reported` answer for M3** (X-H5).
- **No closed-world refusal before FA-1** (item 13).
- **No confinement, sandbox or untrusted-input claim** (as ME:795 states for E).
- **No timing measurement.** Item 25's days are M3P's planning durations.
