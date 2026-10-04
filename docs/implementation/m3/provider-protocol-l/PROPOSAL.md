# The M3 provider-protocol and reuse law — proposal M3-L r1

**DRAFT: acceptance gated.** This is a draft. It may be reviewed once its gate permits, and it cannot be accepted until every gate item below is met. Its gate list is the M3-L row of the accepted M3 unit plan (`M3-PLAN.md:160`). Drafting proceeds in parallel, as that row allows.

2026-10-03. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent, during the overnight autonomous run. It is the law for unit **M3-L** of `docs/implementation/m3/M3-PLAN.md` (r4, accepted). It is written under:
- the M3-L row (`M3-PLAN.md:160`), the M3-D row (`M3-PLAN.md:164`), the M3-S row (`M3-PLAN.md:158`), the M3-J row (`M3-PLAN.md:170`), the "O7" section (`M3-PLAN.md:308-359`) and the critical path (`M3-PLAN.md:187-258`);
- the accepted analysis-quality plan's §5.3, obligations INC-1 to INC-8 (`analysis-quality/PLAN.md:383-409`, r6; the INC text is byte-identical in r4, r5 and r6);
- the accepted operability plan's §3.1, §3.6, §4.1, §5.5, §8 and §9 (`operability/PLAN.md`, r3);
- the accepted quality-harness design record, where it constrains the protocol (`harness/DESIGN.md`, r13);
- the product contracts in `docs/v2/contracts/product-v1/` and the protocol artifacts they select.

## Acceptance gate

Status at drafting (2026-10-03). The gate is `M3-PLAN.md:160`: "S-M, complete T2 (T2b), Q0, D3, D13 and the D2 draft, S-OP-2 drafted, O1 and **O7 decided**". The same row says "The S-OP-4 join is the law's content, not a gate item", so S-OP-4 appears as item 12, not here.

| # | Gate item | Status | Evidence |
|---|---|---|---|
| G1 | **S-M**, the INC-7 spike, measured | **NOT STARTED.** It depends on T2a (met), the Q0 envelope (met) and D13 (G5, open); its Q6-labelled samples also wait for D12 (`M3-PLAN.md:158`). It is a lead run set, so it waits for X9's lead sets (`M3-PLAN.md:270`). Item 9 lists the figures it must deliver. Every number that depends on it is a placeholder `⟨SM-n⟩`. | `M3-PLAN.md:158`, `:245`; no S-M report exists |
| G2 | **T2 complete (T2b)** | **T2a MET; T2b NOT STARTED.** T2a was accepted by GROK2 (arch `be87f45f7`; `reviews/grok2-corpus-t2a-r1/status.json` `ACCEPTED`). T2b's candidates are pinned in the T2a draft manifest but not yet a T2b unit. | `corpus/README.md:11-16` |
| G3 | **Q0** | **MET.** The harness design record r13 was accepted by CODEX2 (arch `925b1ddd2`; sha256 `37438317…`). | `harness/DESIGN.md:3` |
| G4 | **D3**, the T2 selection | **OPEN.** It is lead work with owner sign-off, status `proposed` (`analysis-quality/PLAN.md:543`). No sign-off is recorded. | — |
| G5 | **D13**, the exploratory envelope | **PARTLY SETTLED.** ENV is drafted and its mechanisms were accepted within Q0 r13 (`harness/DESIGN.md:1141-1158`). D13's sign-off is still open (`harness/DESIGN.md:1245`, OI-1; `analysis-quality/PLAN.md:554`). D13's second half, the DR-G13 successor, is M6 work and is not in this gate. | — |
| G6 | **D2 drafted** | **MET, on the lead's reading.** The rule-catalog draft specs are Q0 §2 (`harness/DESIGN.md:276-300`), accepted in r13. D2's placement decision (a first-party `PolicyDocumentV2` pack through a WS/pack successor) is still `proposed`, with owner sign-off (`analysis-quality/PLAN.md:542`; `harness/DESIGN.md:1259`, OI-15). The gate asks for the draft, not the sign-off. A reviewer may read it otherwise (open question R7). | — |
| G7 | **S-OP-2 drafted** | **NOT STARTED.** No S-OP-2 draft exists. Item 14 lists the provider-boundary events this law needs it to register. | `operability/PLAN.md:408` |
| G8 | **O1** | **DECIDED IN THIS LAW** (item 11), as a lead decision subject to this law's review. It becomes final when this law is accepted. | `M3-PLAN.md:298`; `operability/PLAN.md:394` |
| G9 | **O7 decided** | **PENDING. An owner decision**, blocker B1 in `docs/implementation/OVERNIGHT-2026-10-03.md`. This law neither decides O7 nor assumes its outcome (item 17). | `M3-PLAN.md:310`, `:363` |

**Before acceptance**, the next revision must:
- fill every `⟨SM-n⟩` placeholder from S-M's report and record the item 9 outcome;
- update each gate row with its evidence;
- re-pin the citations into any contract text that moved.

**Not in this gate:**
- CF-P, which gates the D law, not this one (`M3-PLAN.md:164`);
- D12, which gates only S-M's Q6-labelled samples (`M3-PLAN.md:158`);
- every D5a successor. Item 3's table explains why none is needed for M3.

## Short names

Line numbers are those of the live files on 2026-10-03. Each live plan or design file carries a two-line acceptance note, so it is 2 lines ahead of its `-rN` snapshot.
- **M3P** `docs/implementation/m3/M3-PLAN.md` (r4, accepted)
- **AQP** `docs/implementation/m3/analysis-quality/PLAN.md` (r6, accepted)
- **OPP** `docs/implementation/m3/operability/PLAN.md` (r3, accepted)
- **Q0** `docs/implementation/m3/harness/DESIGN.md` (r13, accepted)
- **ENV** `docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json`
- **NE / IE / WS / SL / AQ** `docs/v2/contracts/product-v1/{native-evidence,identity-and-evidence,workflows-and-surfaces,security-and-lifecycle,admission-and-qualification}.md`
- **F02** `docs/v2/architecture/02-distribution-and-components.md`
- **REG** `docs/v2/architecture/08-decision-and-readiness-register.md`
- **BP** `docs/v2/architecture/implementation-boundaries-and-build-plan.md`
- **COV** `docs/v2/architecture/implementation-coverage.v1.json`
- **CH13** `docs/v2/architecture/13-evidence-workflows-and-product-contracts.md`
- **QG** `docs/coop/design-corrections/qualification-gates.applied.v1.json`
- **CC** `docs/coop/completion/control-completion.contract.v5.md`
- **CPC** `docs/coop/artifacts/control-protocol-contract.v2.json`. CC:9-11 calls CPC "the accepted authority". CPC's own header says `CANDIDATE-NOT-APPLIED` and `"binds": "NOTHING"` (CPC:7, CPC:10). This law therefore cites CPC's join rules and its tension T-1 as the reading CC adopts. Where it relies on them, it makes its own lead decision.
- **DRC** `docs/coop/completion/distribution-runtime-completion.v2.md`
- **DLV** `docs/coop/artifacts/delivery.v2.json`, the TypeScript base that TS2 succeeds
- **RPP** `docs/coop/artifacts/rust-provider-protocol.v2.json`, the Rust base that Rust3 succeeds through the v4 merge (F02:259-269)
- **DRJ** `docs/coop/artifacts/delivery-rust-provider-join.v4.json`
- **P3T** `docs/coop/design-corrections/native/protocol3-transitions.v1.json`
- **T2O** `docs/coop/design-corrections/native/typescript-protocol2-order.v1.json`
- **RH** `docs/implementation/m3/record-hygiene/PROPOSAL.md`

Product paths are under `opensip/`, at main `2967905`.

## Problem

M3 builds the first real providers and the supervisor around them (BP:887; M3P:164-168). Before the provider protocol is fixed, three accepted records require one law to settle the following.

**The quality plan.** Its reuse obligations INC-1 to INC-8 must be "written into the M3 law, plus the INC-7 spike" (AQP:499). They are "the condition that the M3 provider protocol and host law must be able to satisfy, whether or not changed-scope ships at M3" (AQP:387). Any of them that needs a contract change goes through D5a (AQP:546).

**The operability plan.** "Before the M3 provider protocol law" (OPP:380), it needs:
- O1 decided;
- the S-OP-4 record join under O1(a);
- O7 decided;
- S-OP-2 drafted;
- INC-1 to INC-8 in the same law.

It also needs the provider side of two-stage cancellation (OPP:329) and the phase-lawful identity rule (OPP:149-159).

**The unit plan.** It gives this law three more pieces (M3P:160, M3P:302-304, M3P:381-385):
- the DR-G14 placement and changed-scope choices;
- a record correction for DR-G10;
- a record of two other stale texts.

**What exists today.** At product `2967905`:
- there is no `crates/components` (`ls crates/`);
- the Rust provider exits before reading a request (`providers/rust/src/main.rs:1-14`);
- the generated TS2 and Rust3 carriers (`crates/contracts/src/generated/protocol.rs:5422`, `:6111`) come from an input that is "not a production wire decoder, not semantic admission" (`schemas/wire/native-carriers-v1.json:4`).

So no implementation constrains this law. The accepted contracts and plans do.

## Decisions

Lead decisions are dated 2026-10-03. They are recorded under the owner's standing direction to decide on the lead's recommendation and to block only where no recommendation exists. The owner may reverse any of them.

### A. Protocols and process lifetime

**1. TS2 and Rust3 are the M3 provider protocols, unchanged (INC-5).**
- **Decision.** M3's providers speak exactly two protocols:
  - `typescript-semantic` major 2;
  - `rust-semantic` major 3.

  Each is as NE §9 defines it (NE:2781-3313), over its inherited base: DLV for TypeScript, and the RPP v2 / v4 merge for Rust (F02:259-269). This law adds nothing to either protocol: no frame, member, phase, terminal kind, capability token, limit, identity version or negotiation choice. Handshakes stay per language: `TypeScriptHelloV2`/`TypeScriptHelloAckV2` and `HelloV3`/`HelloAckV3` (BP:718-719). Both still require exact token-array and identity-version echo (NE:2792-2796, NE:2837-2844).
  - **The optional `target-attribution-v2` token.** Whether a signed capability row carries it stays a matter for that row and for the provider units (F, G). This law changes neither branch of NE:2799-2814.
- **Basis:**
  - AQP:402: "Changing an accepted wire contract needs a reviewed successor; the protocols are not unselected";
  - BP:717: "Current worker protocols are TS2/Rust3";
  - QG:202, DR-G10's acceptance: "TS protocol major2 and Rust protocol major3 remain opaque, one-shot, fate-compatible native subprotocols";
  - F02:271-273: "Any semantic frame/fate or lifetime change to either protocol needs an explicit successor … The common control protocol cannot make the change by negotiation";
  - NE:2811: "Protocol major stays 3 / TypeScript major 2".
- **Rejected:**
  - **A TS3/Rust4 successor now, to carry reuse or residency.** S-M has not measured anything (INC-7). D5 stages residency to M5 (AQP:385). INC-5 keeps the protocols selected.
  - **A shared provider SDK that hides the two handshakes.** BP:720 forbids it: "No additional provider SDK is selected merely to hide their distinct protocol obligations."
- **Forbidden substitutes:**
  - any extra wire member or frame, for example for progress, diagnostics, correlation or reuse;
  - a negotiated "extension" that changes frame meaning;
  - citing F02:220 ("major is **1**") or F02:259 ("**major 2**") as the current majors (item 20).

**2. One child per universe, one-shot, no reuse.**
- **Decision.** For each `(ExecutionId, SnapshotId, universe key)` the host launches exactly one provider process. The universe key is TypeScript's `universeKey` (NE:3166-3177) and, for Rust, the native semantic-universe identity (NE:3161-3163).
  - **TypeScript.** The `workerCardinality` rule applies unchanged (DLV:556-565):
    - one worker per distinct key;
    - shared across the matching TypeScript stages of that key;
    - never multiplexing different keys;
    - never reused across ExecutionIds;
    - never retained after its terminal;
    - never resident.
  - **Rust.** One supervised sidecar per semantic universe, with no reuse (F02:268-269).
  - **When a child may start.** Only after the host has bound `SnapshotId`, `PlanId` and the complete universe key (DLV:566), and only through NE §9.1's reject-before-disclosure order (NE:2846-2866).
  - **How a child ends.** After its terminal it reaches zero-exit, then EOF, and its scratch is destroyed (DLV:567; RPP:582). After `Cancelled`, TypeScript requires only EOF (T2O:261-266).
  - **No restart.** A faulted child is never restarted within its attempt (OPP:273). A new attempt has a fresh ExecutionId (WS:81-82), and so fresh children.
  - **No in-process fallback.** A failed launch or child is never replaced by in-process analysis (OPP:135, F7; AQP:114).
  - **The harness.** Its warm runs follow the same rule: each is a new process "with … no reused provider process" (Q0:805).
- **Basis:**
  - F02:222-224: "one child per `(ExecutionId, SnapshotId, TypeScriptSemanticUniverseKey)`, and no reuse remain unchanged. R-1 one-shot/lifetime-neutral constraints also apply";
  - QG:202 ("one-shot");
  - DLV:567: "A child is never retained for a later request";
  - DLV:1517 (DL-13): "never reuses worker state".
- **Rejected:**
  - **A pre-spawned or pooled warm worker** to hide start-up cost. It crosses ExecutionIds (DLV:562), and DLV:1197 already rejected a "resident tsserver or language-server daemon".
  - **Multiplexing universes in one Node process** (DLV:561).
  - **Spawning before Plan binding**, even with no bytes sent (DLV:566).
- **Forbidden substitutes:**
  - a worker kept alive between invocations, attempts or Plans under any name ("warm", "cached", "pooled");
  - a host-side store of provider frames replayed to a new child;
  - a provider restarted after a fault within one attempt;
  - in-process analysis after a provider failure.

**3. Changed-scope at M3: none ships (lead decision; M3P:304).**
- **Decision.** M3 builds no producer cache and no changed-scope path. Every M3 run is full analysis of its Plan.
  - **What binds later work.** Items 4-10 bind any changed-scope or resident design.
  - **Who decides it.** M4 decides whether changed-scope ships, with S-M's data (AQP:502; M3P:304).
  - **Explicit scope is not incremental.** A narrower Plan through the existing scope descriptor (`workspaceRoots`, `pathPrefixes`; NE:4276) is lawful today and needs no successor. But it is a different Plan with its own Coverage, it is not reuse, and it never satisfies INC-4.
- **Basis:** M3P:304: "Changed-scope (M3-L). Recommendation: none ships. The obligations go into the law, and M4 decides with S-M data."
- **Rejected:**
  - **A same-Plan `cache2` consumer at M3.** It helps only identical re-runs (item 4), not edits. It adds a cache-admission surface before any measurement shows that it pays.
  - **Labelling an explicit-scope run "incremental".**
- **Forbidden substitutes:** any M3 path that answers a request from a prior Run's artifacts, or presents a scoped run as a complete one.

**What each INC item needs.** No D5a successor is needed to accept this law, because neither cross-edit reuse nor residency ships at M3. Two such successors are needed before the features they enable.

| INC | Item | At M3 | Contract consequence |
|---|---|---|---|
| INC-1 | 4 | Only same-Plan reuse is admissible, and none is built. | **Needs a D5a successor (IE)** before any cross-edit reuse: a cache key that does not bind `planId`. |
| INC-2 | 5 | Met by construction. | **Pure law.** The INC-1 successor must also define how a reused candidate is re-admitted, so INC-2 rides on it. |
| INC-3 | 6 | Every run is full analysis. | **Pure law.** It constrains what the INC-1 successor's key must cover. |
| INC-4 | 7 | The suite is authored on the determinism base. | **Pure law** (a harness obligation). |
| INC-5 | 1 | TS2 and Rust3 are unchanged. | **Pure law.** Any change is a successor by definition. |
| INC-6 | 8 | Forbidden. | **Needs D5a successors** at M5: protocol-lifetime successors for both languages, and a DR-G10 acceptance successor. |
| INC-7 | 9 | Gate item G1. | **Pure law.** |
| INC-8 | 10 | The operational record says `reuse: none`. | **Pure law.** The public carrier at M4 is S-OP-6, an operability successor, not D5a. A semantic Coverage successor is forbidden. |

### B. The reuse law: INC-1 to INC-8

**4. INC-1: reuse is an optimization, never authority (law).**
- **Decision.**
  - **What may be reused.** Only producer work, and only as a cache hit admitted against exactly the closure the consuming Run requires (IE:1610-1629). "Finding bytes under a matching key is not authority" (IE:1614-1615). A hit "is reusable producer output, never evidence authority, and it never replaces or re-seals a Run" (IE:1625-1626).
  - **What may not.** An old Run's replay is never evidence for a new snapshot: "New source or policy creates a new Plan/Run" (IE:1605-1606).
  - **Admission against a Run.** Cache and storage admission against an authoritative Run inherit complete replay (IE:1591-1592).
- **The binding consequence, found while drafting.** Under IE as written, no cache entry can hit across a source edit:
  - `cache2` binds the Plan (IE:195). Its `stageSpecDigest` is the digest of the `stage-spec` record, which carries `planId` (IE:1288-1293).
  - Every `scopeIds` member must be "a retained `subject-scope` of this snapshot" (IE:1617-1618), and `scope2` binds the snapshot (IE:183).
  - Any source edit changes `snapshot2` (IE:179), and so `plan2` (IE:182).

  So today's `cache2` admits only same-Plan reuse: identical re-runs and regeneration (IE:1599-1608). Cross-edit reuse of producer work needs a **D5a IE successor**: a cache-key and stage-spec domain keyed by the producer-relevant input closure rather than the Plan, with its own admission. It is owned by the identity owner (AQP:546) and is not drafted here.

  The provider protocols add no reuse route either. Every child receives the complete sealed snapshot (NE:2992-2995), and for Rust the complete dependency set (NE:2863-2866). Provider-side reuse would therefore need TS3/Rust4, which item 1 rejects.
- **Basis:** AQP:389; the IE lines above.
- **Rejected:**
  - **Stripping `planId` from the key by host convention.** That is a non-contract key: a hidden recipe beside the published one, which IE:1291-1292 forbids ("there are never two recipes for one spelling").
  - **Treating equal content digests as reuse authority** (IE:1614-1615).
- **Forbidden substitutes:**
  - consuming an entry minted under another Plan;
  - relabelling an old fact, scope or Coverage entry with a new snapshot's identity;
  - treating a key match as admission;
  - resolving a bare `fact-payload`, `coverage-payload` or `import-payload` reference as a root (IE:1622-1625).

**5. INC-2: every result is admitted under the current snapshot and Plan (law).**
- **Decision.** Every scope, fact, Coverage entry and view the new Plan uses is minted and admitted under the new `snapshot2` and `plan2`, with no inherited standing:
  - scope and fact bind the snapshot (IE:183-184);
  - Coverage binds its scope (IE:185);
  - a view binds the Plan (IE:186).

  Provider frames carry the verified Plan's `snapshot2` and `plan2` texts, and every echo must equal them (NE:3158-3161, NE:3216-3219).
  - **At M3** this holds by construction (item 3).
  - **For any later reuse.** The INC-1 successor must define how a reused producer candidate is re-admitted under the new snapshot, including anchors and producer attestation. The host must never construct a fact that no admitted provider frame produced: a faulted or cancelled worker "contributes **no facts, no Coverage entries and no Run**" (NE:3837-3843), and framing grants no fact authority (M3P:169).
- **Basis:** AQP:390.
- **Rejected:** carrying forward a standing such as "already admitted" from an earlier Run.
- **Forbidden substitutes:**
  - host-minted facts without a producing frame;
  - Coverage copied from a prior Run;
  - a view assembled from objects of two snapshots.

**6. INC-3: invalidation (law, binding any later changed-scope design).**
- **Decision.** Any changed-scope design must define invalidation over all seven classes of AQP:391-399:
  - enumeration;
  - incoming references;
  - negative dependencies, since a universal negative depends on its whole universe;
  - configuration and native context. Any field change already changes the PlanId (NE:1276-1277).
  - tool and rule closures;
  - dependency source sets;
  - prepared outputs.

  When the host cannot bound an invalidation, it falls back to full analysis and discloses that (AQP:400) in the operational record (item 10).
  - **At M3** every run is full, so the record says so.
  - **For the INC-1 successor.** Its key must cover every one of these classes. A class the key omits is a hidden input.
- **Rejected:** invalidation by file-level dirtiness alone. It misses incoming references and universal negatives.
- **Forbidden substitutes:**
  - an unbounded invalidation silently treated as bounded;
  - a fallback to full analysis that is not disclosed.

**7. INC-4: equivalence acceptance (law; a harness obligation).**
- **Decision.** Before any changed-scope path ships (M4 at the earliest), paired full and incremental sequences on the same new snapshot and the same current semantic input closure must give equal results:
  - equal semantic payloads and correspondence for findings, facts and Coverage;
  - equal replay outcomes (AQP:401).
  - **Which identities are compared.** Snapshot- and Plan-bound identities are compared within each pair, where they must be byte-equal. They are never compared across Plans (Q0:766-770).
  - **What is excluded.** Reuse provenance and per-invocation identifiers (RequestId, ExecutionId) (Q0:770).
  - **The edit sequences** are AQP:401's, as Q0:792 adopts them.
  - **Authoring.** The suite is authored on Q0 §8's determinism base.
- **Basis:** AQP:401; Q0 §8.
- **Rejected:** a sampled-equivalence check. Q5 determinism is exact (Q0:772).
- **Forbidden substitutes:**
  - shipping changed-scope on a passing determinism suite alone;
  - comparing with provenance included, which fails by construction (AQP:409), or with identities compared across Plans.

**8. INC-6: no resident host at M3; the M5 resident host's obligations are fixed now (law).**
- **Decision.** M3 has no resident host, no persistent provider and no agent server (DLV:564 `residentWorker: false`; AQP:503). The M5 resident host must meet INC-6 (AQP:403-407):
  - every response is bound to an immutable request snapshot;
  - the single writer is the per-project lifecycle lease (IE:1657-1660);
  - the host execution grant stays `RepoExecutionGrantV2`, outside the Plan (IE:467, IE:1387; NE:1273);
  - cancellation, crash and restart, and stale-reply rejection are exercised;
  - persistent RSS and eviction are bounded and measured.
- **Contract consequence (D5a).** A resident or reused worker contradicts:
  - DLV:562-564 (`reuseAcrossExecutionIds: false`, `retainAfterTerminal: false`, `residentWorker: false`);
  - F02:222-224 and F02:268-269 ("no reuse");
  - DR-G10's "one-shot" acceptance (QG:202).

  F02:271-273 requires "an explicit successor from the owning V1 surface" for any lifetime change. M5 residency therefore needs protocol-lifetime successors for both languages and a DR-G10 acceptance successor, before M5's resident host is built.
- **Rejected:** residency at M3, which D5 stages to M5.
- **Forbidden substitutes:** at M3, any long-lived provider or host process that serves more than one request.

**9. INC-7: the spike first, and what its numbers decide (law; gate item G1).**
- **Decision.** This law fixes the protocol (items 1-2) only on acceptance, and acceptance needs S-M's measured report (G1). S-M is the M3-S unit's lead run set:
  - it is a throwaway harness outside the product;
  - it runs over public, pinned T2 bytes;
  - it executes no repository code;
  - its samples are labelled preliminary;
  - it makes no production claim (M3P:158).

  Its report must contain at least the figures below. Each is used here only by placeholder. Unless S-M's report fixes it otherwise:
  - **Workloads.** The dev-role medium T2a repositories of the figure's language, plus `mr-rs-medium-serde-json` for the Rust rows (`corpus/README.md:16-34`). Held-out entries are excluded, so that held-out standing is never put at risk (Q0:256, QD-23).
  - **Statistic.** 3 warmups, then 7 runs; the median, with the maximum also reported (AQ:268-276; AQP:349).
  - **Host.** The lead's macOS host, labelled `preliminary`; not D12 (M3P:158).

| ID | Figure | Unit | Value |
|---|---|---|---|
| SM-1 | TS start: a fresh Node process, from the pinned closure path, loads the pinned TypeScript compiler and is ready to read a request | ms | `⟨SM-1⟩` |
| SM-2 | TS analysis: a fresh-process `Program` creation plus a full semantic pass over the repository | ms | `⟨SM-2⟩` |
| SM-3 | Rust start: the `rustc_driver` sidecar is ready for its callbacks (needs S-P to succeed; otherwise `incomplete` with S-P's reason) | ms | `⟨SM-3⟩` |
| SM-4 | Rust analysis: through type checking. No build script or proc-macro runs, so the expansion that depends on them is disclosed as unavailable | ms | `⟨SM-4⟩` |
| SM-5 | Sealing: enumerate the read set, read and SHA-256 every member, and compute the `snapshot2`/`plan2`-equivalent digests | ms; files; bytes | `⟨SM-5⟩` |
| SM-6 | TS read-set size, including `node_modules` as T2 pins it (NE:2948-2949). Compare with `maxSnapshotEntries` 200,000 and `maxSnapshotChunkBytes` 1,048,576 (NE:2963). If T2 pins no dependency tree, report the repository-only set, labelled. | entries; bytes | `⟨SM-6⟩` |
| SM-7 | Transfer: stream the sealed set, plus the Rust dependency-source set, through a pipe in ≤ 1 MiB chunks with framing, once per child | ms per child | `⟨SM-7⟩` |
| SM-8 | The longest single synchronous compiler call inside SM-2 (the event-loop block) | ms | `⟨SM-8⟩` |
| SM-9 | Complete replay, IE:1580-1592, over a fact and finding graph of the size SM-2 and SM-4 imply. Synthetic and labelled. | ms | `⟨SM-9⟩` |
| SM-10 | Per-process `ru_maxrss`, information only (AQP:343) | bytes | `⟨SM-10⟩` |

  **Derived figures:**
  - the one-shot fixed floor **F** = start (SM-1 or SM-3) + SM-5 + SM-7 + SM-9;
  - the per-run total **T** = F + analysis (SM-2 or SM-4).

  **What the next revision records.** It records F and T per workload, and one outcome against the owner-approved targets. Those targets are held on the D12 runner (AQP:372), so the comparison here is preliminary:
  - **(A)** F ≤ 2 s, the single-file edit target (AQP:385), and T within the medium budgets (AQP:377): T under Q0 §9.2's cold reset ≤ 30 s, and T under its warm reset ≤ 8 s. Cold and warm are separate fixtures (AQ:279-280), so S-M reports T under each reset it can apply. One-shot stands for M3. M4 decides whether changed-scope can meet the edit target by reducing analysis work.
  - **(B)** F > 2 s. No host-side reuse under one-shot TS2/Rust3 can meet the edit target, because F remains. This law still fixes TS2/Rust3 for M3, since residency is staged to M5. The record names residency (item 8) or a protocol successor as M4's only route to the target, and raises owner question O3.
  - **(C)** T > a medium budget. One-shot full analysis misses an owner budget. This is the trigger AQP:372 names ("to be revisited after the first exploratory measurement"), so it raises owner question O4 before acceptance.
- **Basis:**
  - AQP:408: "Before the protocol is fixed, measure startup, sealing and replay costs for one-shot analysis on medium T2 workloads. Residency must earn its cost against that measurement";
  - M3P:388: "The one-shot design may miss the §5.2 budgets … S-M exists to find that out before L".
- **Rejected:**
  - **Accepting the law with invented or estimated figures.**
  - **Making acceptance conditional on outcome (A).** The gate is "S-M measured" (M3P:160), not "S-M passes". The owner decides budget and staging questions, not this law.
- **Forbidden substitutes:**
  - a number in this law not taken from S-M's report;
  - an S-M figure from a held-out repository;
  - a macOS figure presented as a D12 or Q6 sample.

**10. INC-8: reuse disclosure lives in the operational record, outside semantic Coverage (law).**
- **Decision.** The host's operational record (OPP:249) discloses which results were recomputed and which were reused producer work, per provider child and per stage. The record is:
  - host-owned, typed and nonsemantic;
  - keyed by RequestId and, once the attempt is admitted, ExecutionId;
  - outside Run identity, Coverage, PlanId and every digest.

  At M3 every record states that all work was recomputed and none reused, and names the cause: `no-reuse-path` (item 3).

  `CoverageResultV3` is unchanged. It has no reuse member (NE:2016-2030), and canonical Coverage describes only the current Plan's examined, resolved and sufficient state (AQP:409). Fully re-admitted reused work may support a complete result. Any obligation not re-established for the current Plan stays a typed incomplete deficiency (AQP:409).
  - **Carriers.** At M3 the record reaches the harness as instrumentation (OPP:250). A public disclosure at M4 needs S-OP-6 (OPP:250, OPP:412).
- **Basis:** AQP:409; OPP:249-250; Q0:946, Q0:953; ENV:660-666, where `carriesReuseDisclosure` is a required member.
- **Rejected:** a Coverage successor carrying provenance. AQP:409 already rejects it: it "would make INC-4 fail by construction and change `coverage2` identities".
- **Forbidden substitutes:**
  - reuse provenance in any semantic payload, digest, Plan input, finding or Coverage entry;
  - a reuse success that hides an obligation not re-established;
  - a public reuse surface before S-OP-6.

### C. Correlation, diagnostics and liveness

**11. O1 is decided: (a), with no new control message (lead decision).**
- **Decision.** Provider diagnostics, progress and liveness use only what already exists:
  - the closed common-control set (CC:9-11, CC:27-41);
  - the provider subprotocols' own closed responses.

  No progress, diagnostic or heartbeat frame is added to either plane.
- **Basis:**
  - DRC:573-574: "No generic progress frame is introduced; the host derives progress from admitted stage/counter observations";
  - DRC:574-576: diagnostics "may use the existing bounded stderr channel and carry no protocol meaning";
  - OPP:232-238; M3P:298; OPP:394.
- **Rejected:**
  - **O1(b), a typed progress or diagnostic frame.** It needs S-OP-3 (a DR-102 successor), S-OP-4's SDK methods, TS2 and Rust3 joins, and G20/G21 additions (OPP:240), and it would breach item 1.
  - **Progress from stderr.** stderr "never carries facts, Coverage, identity, control, terminal status" (DLV:1133).
  - **Progress from `resourceReport`.** Its figures are provider-asserted resource counts (CC:35), not admitted work.
- **Forbidden substitutes:**
  - provider-asserted counters as progress;
  - parsing stderr;
  - liveness inferred from traffic alone (OPP:136, F8).

**12. The S-OP-4 record join under O1(a) (law content; owning authority DR-125, OPP:410).**
- **Decision.** This law carries the record join. It adds no SDK operation.
  1. **stderr.** The host captures each provider's stderr up to the protocol bound and holds it in memory. At settlement it reduces it to `{bytes, truncated}`, with no digest: a digest of free text is P3 (OPP:171). The bounds are TS2 `maxStderrBytes` 262,144 (NE:2967), and Rust3's retained v2 `maxStderrBytes` 262,144 (RPP:117, retained by NE:2934). stderr is never parsed, logged, exported, admitted or used as a fact, and it never changes a result (DLV:1133).
  2. **Fault detail.**
     - The control `fault` detail (CC:36; ≤ 1,024 bytes, CC:56-58) is reduced to its length.
     - Rust `ProviderFaultV2.faultKind` is a closed enum (RPP:441-445), so it is loggable as P0.
     - Its `detailCode` is "diagnostic only, never D9 authority" (RPP:445). Until S-OP-2 registers it as a closed set, it is treated as free text and reduced to its length.
  3. **Progress.** Progress is derived only by the host, from transitions its own state machine admitted. It counts:
     - frames that passed protocol validation: snapshot chunks acknowledged, and `FactBatch` and `Coverage`/`CoverageV3` frames per universe and stage;
     - stage changes.

     The phrase "admitted stage/counter observations" (DRC:574) is read as these host-counted transitions. Frame acceptance is not fact admission: facts are admitted only after Complete, matching commitments, zero-exit and EOF (DLV:1517). So progress never implies admitted facts.
  4. **Liveness.**
     - **The signal.** Nonce-matched `health`/`healthReport` (CC:33-34, CC:50-54) and `resourceReport` (CC:35), within the STEADY window (CC:132). A missed health response within the supervisor's window is a liveness fault (OPP:237). The window's value is D3's, provisionally 5 s (OPP:237).
     - **What the provider owes.** The component's health responder must not be starved by compiler work. A long synchronous compiler call must not turn a legitimate long phase (OPP:238) into a liveness fault. How it achieves that is F's and G's design, for example a responder outside the compiler's thread.
     - **What S-M owes.** SM-8 measures the exposure. D3 must set the window above SM-8, or the providers must show that the responder is independent of compiler work.
  5. **The SDK alias rebinding.** DRC:556-566 binds the SDK's `HostRequest`, `ProviderResponse`, `FactBatch`, `Coverage` and `ProviderComplete` aliases to DLV's **V1** payloads. Under TS2 they bind to the successor payloads of NE §9.4 and §9.7 and `provider-startup.schemas.v1.json`. That is a re-binding of existing operations, not a new operation.
     - **Rust3 has no SDK.** DRC:515 selects "a TypeScript provider SDK plus Rust host bindings", so the Rust sidecar implements its component side of common control itself (G1a).
     - **Open.** Whether the DR-125 owners treat this re-binding as a record join or as an SDK successor is open question R2.
- **Basis:** OPP:240 ("Under (a), S-OP-4 is still needed as a record join stating the stderr and fault-detail disposition and the progress derivation"); M3P:160.
- **Rejected:**
  - **A separate S-OP-4 record unit.** M3P:160 places the join in this law.
  - **Keeping a stderr digest** for correlation. That is P3 (OPP:171).
- **Forbidden substitutes:**
  - stderr text or `fault` detail in any log, crash ring, bundle or export;
  - a progress number a provider supplied;
  - a health window shorter than a measured legitimate synchronous block.

**13. RequestId correlation and phase-lawful identities at the provider boundary (law).**
- **Decision.**
  - **The correlator.** `RequestId` (`req1_` plus 32 hex; WS:78-79; IE:61-63) is the universal correlator of every provider-attributed record (OPP:148).
  - **It never reaches a provider.** It is not a wire member (neither TS2 nor Rust3 has one, and adding one breaches item 1), not an argv element and not an environment variable. The predecessor's `OPENSIP_RUN_ID` child-environment tag (OPP:121) is not inherited.
  - **What is on the wire.** Only the identities already bound before spawn: `executionId`, `snapshotId` (`snapshot2`), `planId` (`plan2`) and the universe key (NE:3158-3163, NE:3166-3189). Rust's `CancelV2`, `CancelledV2` and `ProviderFaultV2` also echo `executionId` (RPP:441-457).
  - **Phase.** A provider therefore exists only after attempt admission and Plan sealing (item 2). Every provider-attributed record carries `requestId`, `projectId`, `planId`, `executionId`, the component role and the universe-key suffix, which are lawful from those phases (OPP:149-157).
  - **What is never stringified.**
    - **RunId.** It is never a wire member. It appears in this invocation's provider-attributed records only after a `Committed` publish, and a candidate RunId is never stringified (OPP:157-159).
    - **The emergency case.** When `RequestAuthority::begin` fails, no RequestId exists (OPP:160). No provider is ever spawned in that case, because admission has not happened.
  - **Host-held values only.** Records use the host's own bound values, never worker echoes. Workers may not mint host identities (DLV:572), and an echo that differs is `PROVIDER.PROTOCOL_VIOLATION` before any source byte or after (NE:2854-2856, NE:3216-3226).
- **Basis:**
  - OPP:145-160;
  - DLV:570-574 (host ownership of process fate and identity);
  - CH13:59-62: "no … hidden environment input";
  - Q0:770, which excludes RequestId and ExecutionId from determinism comparison.
- **Rejected:**
  - **Passing RequestId to the child for its own logging.** Providers never get a log path, and the host writes every provider-attributed record (OPP:222).
  - **Keying records by pid.** Pids are reused. The pid is only an attribute, beside `hostReapedMaxRss` (Q0:889).
- **Forbidden substitutes:**
  - any identity in a record before the phase that mints it;
  - a worker echo used as a record key;
  - a RequestId, RunId or log path given to a child.

**14. The operational record at the provider boundary, and the events S-OP-2 must register (law).**
- **Decision.** For each supervised provider child, the host records:
  - **Role.** The protocol name and the universe-key suffix (P1).
  - **Spans**, on a monotonic clock (OPP:251), using these boundaries, which are a lead decision because each is an admitted transition:
    - **start:** spawn → `NativeContextVerified`, or the pre-Analyze `Unavailable`. This includes Hello and HelloAck, OpenUniverse, and snapshot, dependency and prepared custody, with a separate **transfer** sub-span, so that SM-7 has a product counterpart.
    - **analysis:** `Analyze` sent → the stage terminal.
    - **teardown:** the terminal → reap and scratch removal (OPP:248; Q0:944).
  - **Terminal kind**, including `cancelled` (NE:2025).
  - **Cancellation edges**, if any: when the first stage was sent, when the second stage forced the kill, and the cause (item 16).
  - **`hostReapedMaxRss`**, with pid and role: `wait4` `ru_maxrss` in the platform's native unit, labelled. It is information only (Q0:889; AQP:343).
  - **CPU time** from the same rusage.
  - **The reuse disclosure** (item 10).

  The record exists for every invocation that spawns a provider, so the harness can set `carriesReuseDisclosure` and `carriesProcessMaxRss` (ENV:660-666). A missing record is the harness's `record-missing` (Q0:994).
- **What S-OP-2 must register** (G7). S-OP-2 owns the names, field schemas and allowlists. These are the needs, with the privacy class of their fields:

| Need | Privacy class |
|---|---|
| provider spawned, ready, stage changed, terminal, reaped | P0/P1 |
| cancel stage 1 sent, cancel stage 2 forced | P0/P1 |
| liveness missed | P0/P1 |
| no progress (`supervision.no_progress`, OPP:238) | P0/P1 |
| stderr reduced (`{bytes, truncated}`) | P0 |
| fault reduced (length; `faultKind`) | P0 |

- **Basis:** OPP:248-251; Q0 §9.4 (Q0:941-953); ENV:654-686.
- **Rejected:** spans from provider-reported timestamps. The provider's clock and claims are not admitted observations.
- **Forbidden substitutes:**
  - any field of the record entering a semantic identity or digest;
  - a record synthesized when instrumentation failed (Q0:953).

**15. DR-G14 at M3: closure manifests and no-ambient refusals; installation stays at M5 (lead decision; M3P:302).**
- **Decision.**
  - **What M3 does.** It prepares the self-contained closure manifests and the no-ambient-runtime refusals (F4, G2). At the protocol boundary that means two handshake checks, each `PROVIDER.PROTOCOL_VIOLATION` before any source byte on a mismatch:
    - TS2's HelloAck must match the verified signed provider and runtime descriptors, field by field (NE:2973-2984);
    - Rust3's `HelloAckV3` identity members must equal `expectedIdentity`, which is copied from the Plan's universe row and bound to the verified signed release (NE:2824-2834).

    No PATH or system runtime is ever a fallback (BP:715-717; F02:232-241).
  - **What stays at M5.** `crates/lifecycle/src/installation.rs`, the DR-G14 owner module, which COV lists first at M5.
- **Basis:** COV:4770-4776 (gate milestone M3, owner `installation.rs`); COV:8976 (`installation.rs` at M5); BP:1018.
- **Rejected:** building `installation.rs` early. It belongs to the M5 lifecycle surface, and M3 needs only the refusal path.
- **Forbidden substitutes:**
  - ambient Node or a system `rustc` admitted for any reason;
  - a closure mismatch downgraded to a warning.

### D. Cancellation

**16. The provider-side two-stage cancel (lead decisions in 16a, 16c and 16e).**
- **(a) Stage 1, cooperative**, at the first SIGINT, SIGTERM or SIGHUP before finalization (OPP:329; WS:224-229). For each live provider child the host does two things, in this order:
  1. Its provider-side participant writes the in-band `Cancel` exactly once: TypeScript `CancelV1` (DLV:1122), Rust `CancelV2` with `reason: "user-interrupt"` (RPP:447-451). It then closes the request side (RPP:714, T023, which sets `requestClosed`; DLV:1146).
  2. The control plane sends `cancel` with reason `user` (CC:37) as the supervision-scoped announcement that teardown has begun (CPC:375; CPC:489-492, J-5 T-1).

  Both are appended to the host's one merged event order (CPC:466; CPC:469-472, J-1). **Lead decision: the in-band frame goes first,** so the semantic participant sees `Cancel` before any SDK-level abort.
- **(b) Who may cancel in band.** Only user interruption sends the in-band `Cancel`. Rust's `CancelV2.reason` is exactly `user-interrupt` (RPP:451), and an unsolicited `Cancelled` maps to a provider-protocol fault (DRJ:1850). A deadline, liveness failure, resource breach or supervisor fault uses control `cancel` with reason `deadline` or `supervisor-fault` and the teardown ladder (CPC:489-492). It never uses the in-band frame.
- **(c) After stage 1.**
  - **What may follow.** Only `Cancelled`; then zero-exit and EOF for Rust (P3T:342-364), and EOF for TypeScript (T2O:254-266). TypeScript's `observedPhase` rule for the context interval is unchanged (NE:3296-3302).
  - **Late provider octets** are delivered unmodified to the owning participant, which alone gives them meaning (CPC:462).
  - **The stage-1 grace (lead decision).**
    - **Rust3:** the protocol's own `cancellationGraceMilliseconds`, 5,000 (RPP:119). It is retained with an identical value in `ProtocolLimitsV3` and checked by exact equality in Hello (NE:2929-2941).
    - **TS2:** `TypeScriptProtocolLimitsV1` has no grace member (NE:2961-2967), so the host's "bounded cleanup grace" (DLV:1146) applies. It is D3's operational constant, provisionally 2 s (OPP:329).

    Every bounded wait must exist, be finite, and append a typed event when it expires (CPC:494).
- **(d) Stage 2, forced.** A second signal, or expiry of the stage-1 grace, forces the kill of the provider's process tree. The provisional escalation from TERM to KILL is 1 s, with a 10 s reaping ceiling (OPP:273). Scratch is removed (DLV:1146; F02:203-204). A second signal forces at once, inside either protocol's grace.
- **(e) Outcome (law).**
  - **The class.** It stays `interrupted` (130). For TypeScript, "absence of Cancelled after a user signal does not overwrite that class with a provider fault" (DLV:1146; DLV:1122). For Rust, a signal before finalization with fate `USER_INTERRUPTED` or `VERIFIED_CANCELLED` takes the `interrupt-before` template (DRJ:1036-1051).
  - **The stage.** A cancelled stage mints nothing and keeps its interrupted termination (NE:3421-3426; NE:3842-3843). Its stage terminal is `cancelled` (NE:2025).
  - **The Run.** "an analysis attempt aborts and leaves no Run" (WS:229). Cancellation is never an incomplete-analysis deficiency or a provider fault.
- **(f) Scope.** Providers run before the commit. This item therefore covers OPP §5.5 phase A and the provider part of phase B (OPP:334-335). The **commit-phase join** belongs to S-OP-12, owned with the X3D and X7 owners (OPP:417), and is landed by M3-J's J1 law (M3P:170). It covers:
  - the signal as a FinalGate latch observer;
  - phases C to E;
  - X7's latched and CommitUndetermined rows.

  This law decides none of that. Until S-OP-12 is accepted, no signal sets the latch (OPP:340).
- **Basis:**
  - DLV:1146 (`userCancellation`);
  - DLV:1122 (`cancelTransition`);
  - RPP:307-308 and RPP:447-457;
  - DRJ:1848-1852 (`cancellationTotality`);
  - F02:171-177 (host-owned race precedence);
  - CPC:660-663, tension T-1. CPC records two cancellation carriers for one child and "Scoped control-plane cancel to SUPERVISION level (teardown-announcement) and left in-band Cancel wholly to the host's provider-side participant". CPC reports that tension as unresolved (CPC:657). This item adopts that split as a lead decision for M3. Open question R1 asks the DR-102 owner to confirm it.
- **Rejected:**
  - **Control-plane-only cancel.** The SDK would then have to synthesize a `Cancelled` frame, which is the control plane authoring a semantic frame (F02:168-170). Or the protocol's own cancel path would starve (CPC:662).
  - **In-band-only cancel.** It leaves the control session with no teardown announcement, and the J-5 ladder starts with `shutdown` or `cancel` (CPC:491).
  - **A single 2 s host grace for both languages.** On automatic expiry it would enforce 2 s in place of the 5,000 ms both sides agreed by exact equality in Hello. Every bound "is enforced at its named boundary" (RPP:134), so that changes an accepted limit's meaning (item 1). A second signal is different: it is the user's explicit demand, and user-interruption precedence survives the missing `Cancelled` (DLV:1122; DRJ:1036-1051). R9 asks the Rust protocol owner to confirm this reading.
  - **A single 5 s grace for both.** It lengthens TypeScript cancellation for no protocol reason.
  - **Killing at the first signal.** It loses the clean `Cancelled` path that K7 keeps (OPP:125).
  - **Mapping a missing `Cancelled` to a provider fault** (DLV:1146).
- **Consequence, recorded.** OPP's cancellation goal (p95 ≤ 2 s from the first signal to exit; OPP:342) may be missed by Rust3 without a second signal, by up to the protocol's 5 s grace. It is a goal, not a threshold (OPP:342), and the measurement reports it.
- **Forbidden substitutes:**
  - an in-band `Cancel` for a non-user reason;
  - a second in-band `Cancel`;
  - a `Cancelled` synthesized by the host or SDK;
  - admitting facts from a cancelled child;
  - a grace without a typed expiry event;
  - any reading of the commit phases in this law.

### E. Boundaries this law does not own

**17. Launch rules are the D law's, under O7.**
- **Decision.** This law states no spawn, environment, descriptor, confinement, grant or scratch-placement rule. The M3-D law alone owns launch rules under O7. It is not yet drafted (M3P:164, M3P:343; and M3P:27: "launch rules have one owner, the D law, and M3-L cites it").

  This law requires only three things:
  - item 2's cardinality and binding preconditions;
  - that no provider launches before O7 is decided and D1's primitive exists (M3P:310);
  - that no repository code executes. `workerExecutesRepositoryCode` is the constant `false` (NE:2534-2535), and "Repository execution is disabled by default" (SL:1059).

  This law does not decide O7, and it assumes no outcome of it. The confinement disclaimers stand until their successors are accepted (M3P:321-329): SL:497, SL:1113, AQ:344, NE:2554 and REG:366.
- **Rejected:** restating the lead's O7 recommendation (M3P:314-319) as law here. That would pre-empt the owner and create a second owner of the launch rules.
- **Forbidden substitutes:**
  - a launch rule written in any M3 provider unit rather than the D law;
  - any confinement claim before CF-1.

**18. The commit-phase cancellation join is S-OP-12's, landed by M3-J (record).** See item 16f. This law refers to it and does not decide it.

### F. Record corrections

The record corrections are items 19-21. None edits a frozen or pinned file:
- **Contract text** under `docs/v2/contracts/` is never edited.
- **The register** is pinned by the product's `design-lock.json` and by the D-372 application manifest (RH:29-31, RH:41-45).
- **F02** is pinned by the application manifest (RH:33, RH:46-48).

Each correction below is recorded here as current law for M3 and later units. Its in-place note is proposed for the record-hygiene batch's re-pinning successor (RH §2), and is not applied here.

**19. DR-G10's selector (REG:355 against COV:4671).**
- **The stale row.** REG:355 still reads:
  - "TS major 1 and Rust merged major 2 remain opaque, one-shot, fate-compatible subprotocols";
  - harness `harness.DR-G10.provider-conformance.ts-major-1`;
  - status "HARD-BLOCKED pending selector refresh".
- **The current account.** The current applied account of the same gate is:
  - QG:197-215: acceptance "TS protocol major2 and Rust protocol major3 remain opaque, one-shot, fate-compatible native subprotocols with explicit source/fact/Coverage negotiation", harness `harness.DR-G10.product-v1`, current contract NE, and standing "DESIGN-CONTRACT-ACCEPTED; REQUIRED PRODUCT QUALIFICATION UNPERFORMED";
  - COV:4656-4681: selector `/items/9` with `valueSha256` `1313c85d…` (COV:4659-4661), method COV:4671, gate milestone M3, qualification M6. COV:4679 keeps the old claim, labelled `inheritedAcceptance`.

  REG:342 already says that "G10 uses TS protocol major2/Rust major3" and that the detailed rows "preserve historical claims/harness names".
- **The correction.** For M3 and every later unit, DR-G10's current selector is QG `items[9]`, by way of COV:4656-4681.
  - **Historical text.** REG:355's claim, harness name and "pending selector refresh" status are historical. They are never cited as the current gate, and the refresh they wait for has been made in QG and COV.
  - **What is unchanged.** No gate row, threshold or standing changes. DR-G10 stays unqualified, prepared at M3 and qualified at M6 (COV:4675).
- **Proposed note** (after the REG:344-377 table, naming its row):

  > **Current applicability (2026-10-03) — D-372:** the DR-G10 row records the historical TS major 1 / Rust merged major 2 claim and harness. The current selector is QG `items[9]` (TS major 2, Rust major 3, `harness.DR-G10.product-v1`; COV DR-G10); its "pending selector refresh" is discharged there.

**20. F02's stale protocol majors.** F02:220 says the TypeScript selector's major "is **1**", and F02:259 says "The normative Rust contract is **major 2**". The current majors are TS2 and Rust3 (BP:717; NE:2785; QG:202). Those sentences are historical for M3. Their structural rules still bind: one child per key and no reuse (F02:222-224, F02:268-269), and the successor rule (F02:271-273). M3P:142 already forbids the M3 laws to copy the stale majors. A note is proposed for the same batch.

**21. NE §14's heading.** NE:4203 reads "Host composition corrections (mixed authorship; independent Claude review pending)".
- **What this record establishes.** The current NE bytes (sha256 `83b99783…`, 329,013 bytes) are a member of `docs/coop/design-corrections/reviews/candidate-subject.v45.json`. That file is the subject of `claude-independent-design.v45`, whose verdict is `ACCEPT`, and QG cites that review for DR-G10 (QG:212-215). So "pending" is not a current fact about these bytes' review status.
- **What it does not establish.** Whether v45's read scope covered §14 in particular (open question R6).
- **No edit.** NE is a frozen contract and is not edited.

## Cross-law findings found while drafting

These are recorded for their owners. None changes an accepted outcome.
- **X1. `cache2` binds the Plan** (item 4). Any changed-scope design needs a D5a IE successor before it can reuse work across an edit. This is the main finding for D5a and for M4's changed-scope decision.
- **X2. The two cancellation carriers.** CPC's T-1 is reported as unresolved (CPC:657-663). Item 16 adopts CPC's split for M3, and R1 asks the DR-102 owner to confirm it.
- **X3. OPP §5.5's provisional 2 s grace against Rust3's 5,000 ms protocol grace** (RPP:119; NE:2934). Item 16c reconciles them. OPP's next revision, or S-OP-12, should cite the protocol member.
- **X4. The SDK alias bindings name V1 payloads** (DRC:556-566), while TS2 is current. Item 12.5 records the re-binding, and R2 asks how the DR-125 owners classify it.
- **X5. The control `select` tuple for TS2 and Rust3 is unfixed.** CC records only a preview witness, `analyzer`/`typescript`/`1` (CC:199-202), and no accepted text binds a `roleSubprotocol` and `subprotocolVersion` for TS2 or Rust3. D2 must fix them with the manifest owner (R3). This law requires only that the tuple be the exact pinned selection, with no translation (F02:164, F02:168-170).
- **X6. Liveness against synchronous compiler work** (item 12.4). A single-threaded responder can turn a legitimate long phase into a liveness fault. SM-8 measures the exposure, and F, G and D3 resolve it.
- **X7. Stale record text:** REG:355, F02:220, F02:259 and NE:4203 (items 19-21).
- **X8. Citation drift.** M3P cites AQP by r4 line numbers, for example "AQP:370-390" for INC-1 to INC-8 (M3P:160). In the live r6 file those obligations are AQP:389-409. This law cites live r6 lines. M3P's next revision may re-pin them.

## Forbidden substitutes

- Any change to a TS2 or Rust3 frame, member, phase, terminal, token, limit or identity version made by this law, a provider unit or the control plane (items 1, 11).
- A provider process reused across ExecutionIds, Plans or universes; retained after its terminal; pooled or pre-spawned; restarted within an attempt; or replaced by in-process analysis (item 2).
- Reuse of an authoritative object, a cache entry consumed under another Plan, or a key match treated as admission (item 4).
- A fact, scope, Coverage entry or view not minted under the current snapshot and Plan (item 5).
- An unbounded invalidation treated as bounded, or a full-analysis fallback that is not disclosed (item 6).
- Changed-scope shipped without INC-4's paired equivalence (item 7).
- A resident or long-lived host or provider at M3 (item 8).
- A number in this law not taken from S-M's report, or acceptance without S-M (item 9).
- Reuse provenance in any semantic payload, digest or Coverage entry, or a Coverage successor carrying provenance (item 10).
- A new progress, diagnostic or heartbeat message; provider-asserted progress; or parsed stderr (items 11, 12).
- stderr text, a stderr digest or `fault` detail text in any sink (item 12).
- A RequestId, RunId or log path given to a child; an identity in a record before its phase; or a worker echo used as a key (item 13).
- Any operational-record field entering identity, or a record synthesized after an instrumentation failure (item 14).
- Ambient runtimes or tools, or a closure mismatch downgraded (item 15).
- An in-band `Cancel` for a non-user reason, sent twice, or synthesized as `Cancelled`; facts admitted from a cancelled child; or a bounded wait with no typed expiry (item 16).
- Any launch rule outside the D law, or any confinement claim before CF-1 (item 17).
- Any decision about the commit-phase cancellation join (item 18).
- Any edit to a frozen contract, the register or a D-372-pinned file to apply items 19-21.

## Open questions

### For the owner

- **O1. O7, hostile-input confinement.** Gate item G9 and blocker B1. The lead's recommendation is at M3P:312-319. This law is drafted so that it does not depend on the outcome.
- **O2. Sign-off on D3 (the T2 selection) and D13 (the exploratory envelope).** These are gate items G4 and G5 (AQP:543, AQP:554). They are lead work that needs the owner's sign-off.
- **O3. Conditional on S-M outcome (B).** If the one-shot fixed floor F exceeds the 2 s edit target, M4's changed-scope cannot meet that target under TS2/Rust3. The owner would confirm one of two things:
  - the edit target waits for M5 residency, as D5's staging implies;
  - or D5's staging changes.
- **O4. Conditional on S-M outcome (C).** If one-shot full analysis misses a medium budget (30 s cold or 8 s warm), that is the D4 revisit AQP:372 names. The owner decides whether to revisit the budgets or the staging.

### For S-M's data

These are SM-1 to SM-10 (item 9). Each decides or informs the following:
- **F (SM-1 or SM-3, SM-5, SM-7, SM-9)** decides outcome A, B or C, and so O3 and O4.
- **SM-2 and SM-4** give T, and show how much changed-scope could save at M4.
- **SM-6** shows whether a medium TypeScript read set with `node_modules` fits `maxSnapshotEntries` 200,000. If it does not, that is a TS2 limit question, which needs a successor by item 1. It cannot be fixed by host behaviour.
- **SM-8** sets the floor for D3's health window, or shows that the providers need an independent responder (X6).
- **SM-3 and SM-4** depend on S-P. If S-P fails, the Rust rows are `incomplete`. Whether the law can be accepted with Rust rows incomplete is a question for the reviewer at that point. The lead's recommendation is no, unless S-P's failure is itself accepted as a finding with a G2 plan.
- **SM-10** informs OPP §5.2's concurrency ceiling (information only).

### For other owners and reviewers

- **R1. DR-102 owner.** Confirm item 16's reading of the T-1 split between control and in-band cancellation (CPC:660-663).
- **R2. DR-125 owners.** Is the SDK alias re-binding from V1 to TS2 payloads (item 12.5) a record join, or does it need an SDK successor?
- **R3. D2 with the manifest owner.** Fix the control `select` tuple for TS2 and Rust3 (X5).
- **R4. Identity owner (D5a).** Is a cache-key domain without `planId` admissible under IE §4's no-hidden-input rule (IE:1296-1298)? What re-admission evidence does a reused candidate need under a new snapshot (items 4 and 5)? This is needed before M4 ships changed-scope, not for M3.
- **R5. The record-hygiene batch.** Add the notes in items 19 and 20 to its re-pinning successor (RH §2).
- **R6. The lead.** Did the read scope of `claude-independent-design.v45` cover NE §14 (item 21)?
- **R7. The reviewer.** Is G6 met by Q0 §2's draft specs, or does "the D2 draft" mean a drafted WS/pack successor (AQP:542)?
- **R8. D3 (supervisor).** Fix the TS2 cleanup grace (provisionally 2 s), the health window, and the TERM-to-KILL escalation and reaping ceiling. Items 12.4 and 16c set their constraints.
- **R9. Rust protocol owner.** Item 16c reads `cancellationGraceMilliseconds` (RPP:119) as the host's stage-1 wait before a forced kill on automatic expiry, not only as a ceiling. The drafting read found the member in the v4 guard context list (`rust-provider-protocol.v4.json:966`) but not the guard that uses it. Confirm the reading.

## Not claimed

- **Measurement.** Nothing has been measured. Every `⟨SM-n⟩` is a placeholder. The only numbers here are owner-approved targets, protocol constants and OPP's provisional values, each cited.
- **Records.** No contract, schema, gate, threshold, register row or pinned file is changed. Items 19-21 are records, and their notes are proposals.
- **Decisions.** O7 is not decided, and no confinement is claimed. The commit-phase cancellation join is not decided (S-OP-12, M3-J). No launch rule is stated (M3-D).
- **Shipped features.** No changed-scope path, cache or resident host ships at M3. No D5a successor is drafted.
- **S-OP drafts.** S-OP-2 is not drafted. Item 14 lists only what this law needs from it.
- **This revision.** No product code, cargo command, test or lead run set was run for it. Product facts come from reading main `2967905`.
- **Acceptance.** This law is a draft and cannot be accepted until gate items G1, G2, G4, G5, G7 and G9 are met.
