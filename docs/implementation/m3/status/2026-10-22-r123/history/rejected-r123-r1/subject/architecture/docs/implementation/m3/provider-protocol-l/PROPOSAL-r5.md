# The M3 provider-protocol and reuse law — proposal M3-L r5

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. It is the law for unit **M3-L** of the accepted M3 unit plan (`M3-PLAN-r6.md:207`).

**Draft r5, not accepted. Not code. Reviewable now; effective only when its gate is met.** Under the review rule ("Review and effect"), an ACCEPT is recorded as "accepted in review". The law takes effect only when every gate item, L-G1 to L-G11, is met, as M3-C's pinned gate also works (MC:88-89). Four things go through a delta round:
- filling the `⟨SM-n⟩` values;
- any change that O7's decision forces;
- any change Codex's review forces in a part of FA-2 that sets a wire member, the commitment a key carries, the admission point or the reuse treatment. That includes every one of FA-2's NE §0 rows, but not its NE:93 header sentence, schema layout, vectors and evidence, README prose or materialization map ("What depends on O7, S-M, FA-2 and RUST3-LIM");
- **(r5)** the same for RUST3-LIM, which GROK2 has accepted with no change forced: any later change to its accepted bytes in a part that sets a wire member or a commitment, including a rebuild forced by a change to FA-2's handshake copies, its parents.

**History.**
- **r1** (`PROPOSAL-r1.md`, sha256 `5e858c05…`, 59,109 bytes) was drafted on 2026-10-03 and never sent. Its draft request is superseded (`reviews/grok-provider-protocol-l-r1/status.json`, `SUPERSEDED-UNSENT`). r1 cited M3-PLAN r4 and predated T2b's acceptance, S-OP-2, CF-P, M3-C r6, M3-E1 r3 and M3-J1 r3.
- **r2** (`PROPOSAL-r2.md`, sha256 `5bd4025e…`, 91,126 bytes) refreshed those joins and the gate, adopted the review rule, and otherwise kept r1's substance. It was the first revision reviewed. Grok returned **REQUIRED-FINDINGS** (`reviews/grok-provider-protocol-l-r2`): one required finding, RF-1 (item 13's closed list of wire identities), and three non-blocking observations, NBO-1 to NBO-3.
- **r3** (`PROPOSAL-r3.md`, sha256 `6df524a4…`, 121,776 bytes) answered all four. It also joined FA-2, the native successor that answers M3-H's X-H1 (the provider symbol census has no carrier), and answered M3-H's X-H4 (item 5's "no host-minted facts"). Grok returned **REQUIRED-FINDINGS** (`reviews/grok-provider-protocol-l-r3`): RF-1 (item 13's later members and its ceiling still mis-stated the cited payloads), RF-2 (FA-2's §0 row C against the third delta-round trigger), and three non-blocking observations.
- **r4** (`PROPOSAL-r4.md`, sha256 `261db4b9…`, 145,405 bytes) answered all five. Item 13's inventory became **derived mechanically** from the cited schemas, with control L-C1 re-deriving it. The third delta-round trigger named exactly which FA-2 changes reopen this law. Grok returned **REQUIRED-FINDINGS** (`reviews/grok-provider-protocol-l-r4`): RF-1 (the derived ceiling omits required constituents of the coverage keys) and NBO-1 (the opening paragraph's trigger wording).
- **r5** answers both. It adds rule **R7** (identity-key constituents) and re-derives the inventory. It gates on **RUST3-LIM**, the Rust3 subject-list successor, as **L-G11**, closes X13 and R12 with it, and adds SM-11 to SM-14. It renames the gate items **L-G1 to L-G11**, so that "G10" no longer collides with the register's DR-G10 (M3-PLAN r9 NBO-1). Every item, X, R and O number of r1 to r4 is kept.

It is written under:
- the M3-L row (`M3-PLAN-r6.md:207`), the M3-S row (`:205`), the M3-D row (`:211`), the M3-J row (`:217`), "M3-L gate status" (`:429-445`), the "O7" section (`:474-525`) and the critical path (`:253-427`);
- the accepted analysis-quality plan's §5.3, obligations INC-1 to INC-8 (AQP:383-409, r6);
- the accepted operability plan's §3.1, §3.6, §4.1, §5.5, §8 and §9 (OPP, r3);
- the accepted quality-harness design record, where it constrains the protocol (Q0, r13);
- **new in r2:** S-OP-2 r6 (accepted), items 19, 22 and 23; M3-J1 r3 (accepted), items 2, 5 and 8; M3-C r6 (accepted in review), items 5, 9, 16 and 20 and its cross-law findings X-1 and X-3; M3-E1 r3 (accepted), items 14b and 16 and its section G; CF-P's record; and the D law's draft, cited by role;
- **new in r3:**
  - M3-D r3, now accepted by GROK2, still cited by role;
  - M3-J1 r4, now accepted by GROK2 (R10a; no provision this law cites changes);
  - M3-H r1's cross-law items X-H1 and X-H4 (a reviewed draft, not authority);
  - FA-2, the native contract successor for X-H1, in review with Codex;
  - I1-L, the preview pack's accepted policy-language successor, whose cycle atom needs symbol scopes;
- **new in r5:**
  - M3-H r3, now accepted (`fact-admission-h/PROPOSAL-r3.md`, cited as H3; it replaces r3's and r4's H1 citations);
  - M3-PLAN r9, now accepted (`M3-PLAN-r9.md`), which records the review rule, day 0 as "L in effect", and L-G10 (FA-2) in the M3-L row;
  - RUST3-LIM, the Rust3 subject-list successor, accepted by GROK2 at r1 and binding after FA-2;
  - FA-2 r2, in review with Codex;
- the product contracts in `docs/v2/contracts/product-v1/` and the protocol artifacts they select.

## r5 changes

| # | Change | Where | Source |
|---|---|---|---|
| 1 | **r4 is preserved** as `PROPOSAL-r4.md` (`261db4b9…`). | header | — |
| 2 | **RF-1. Rule R7: identity-key constituents (lead decision).** Every **required** member of a record that a cited contract defines as an identity key, or as a key's field-for-field copy, is identity-bearing. So is every member a cited contract requires to equal a key's member. The script names those records in `KEY_RECORDS` and `KEY_COPY`, each with its sentence: DLV `CoverageKeyV1` (DLV:804-817), C-2 `coverageKey.key` (with RPP:544-548), the returned `CoverageKeyV2` (NE:3277-3282; NE:1927-1932), and `ViewEntryV3`'s `relation` and `resolution` (NE:3529 `native.coverage-entry-key-mismatch`; NEM:1566-1567). R1 to R6 keep their admissions and labels; R7 applies only to members they do not admit. L-C1 now covers R7. | item 13; `evidence/wire_identities.py` | `reviews/grok-provider-protocol-l-r4` RF-1; lead direction |
| 3 | **The other composite keys checked.** Item 13 now records each one the walk passes and why it is or is not a key: the request key (R7), the returned key and entry (R7), the fact identity (a host-only record), commitment preimages (content, not keys), view and occupancy keys (only the entry's key-field copies are), correlation tuples (exchange ordinals compared with host records), and scope summaries (counts). | item 13 | lead direction |
| 4 | **The derived counts.** r4: 51 payload rows, 235 identity-bearing member paths (TS2 106, Rust3 129). r5: 52 rows, 278 paths (TS2 121, Rust3 157). The +43, with none removed, are 30 R7 additions to existing rows (15 per language: `relation`, `resolution` and `schemaVersion` on each request key; `relation` and `resolution` on each returned key and entry, in the Coverage, post-Analyze `Unavailable` and `BudgetExhausted` rows), plus the new RUST3-LIM row's 13 paths, of which 3 are R7. By rule: R1 200, R2 23, R3 4, R4 15, R5 3, R7 33. | item 13 | L-C1 report |
| 5 | **Rust3 limit gate: L-G11, RUST3-LIM accepted (lead decision).** This law does not take effect on a Rust3 that refuses two of S-M's seven Rust medium workloads, and nine of T2's 22 Rust entries, before spawn. RUST3-LIM is the native successor that names the subject array by reference under `subject-scope-reference-v1`. **Rejected:** taking effect with X13 open. A fourth delta-round trigger covers later changes to RUST3-LIM's accepted bytes (row 11). X13 and R12 are closed by pointing at it. Item 1 names it beside FA-2. | gate; "Review and effect"; item 1; X13; R12 | RUST3-LIM README (X-RL-L1) |
| 6 | **Item 13: the Rust per-file `subjectId`.** It is on the wire only without `subject-scope-reference-v1`. Under the token each stage carries `analysisDomain.subjectScope.subjectScopeCommitment` instead (a commitment, R1). This is pending RUST3-LIM's acceptance, as FA-2's members are. The derived table gains that row. | item 13 | X-RL-L2 |
| 7 | **Item 9: SM-11 to SM-14**, as RUST3-LIM's README proposes: Rust cost per subject, rebuilding the subject scope, response volume per subject (with FA-2's census), and work-unit tuples, with the large Rust workloads and the S_eff derivation. | item 9 | X-RL-L3 |
| 8 | **Gate rename.** L's gate items are **L-G1 to L-G11** wherever they are operative, because "G10" collided with the register's DR-G10 (M3-PLAN r9 NBO-1). The kept r2 to r4 change tables keep the old names: G1 to G10 there are L-G1 to L-G10. | throughout | M3-PLAN r9 NBO-1 |
| 9 | **NBO-1.** The opening paragraph now states the delta-round triggers as the operative text does. | header | NBO-1 |
| 10 | **Re-pins.** M3-H is cited at its accepted r3 snapshot (H3), not r1; every H1 line is re-mapped. M3-PLAN r9 is accepted and recorded beside r6, whose lines this law keeps citing. The gate row is also cited at `M3-PLAN-r9.md:255`, and X9 is marked done there except for L-G11 and the rename. | short names; gate; X9 | coordinator direction |
| 11 | **RUST3-LIM accepted.** GROK2 accepted RUST3-LIM r1 while r5 was being drafted: ACCEPT-DESIGN-UNIT, no required findings, two non-blocking observations, on subject `5dfd3cd9…` and successor `70f494d9…`, the bytes this law pins. L-G11 is **met in review, held on FA-2**: it opens again if Codex's review changes FA-2's handshake copies, RUST3-LIM's parents. Both statements of the fourth trigger now name later changes to the accepted bytes, and the operative one maps the review's two NBOs. Item 13's condition and RUST3-LIM row, the RL short name, the joins row, X13 and the Effect clause say so. | header; gate; "Review and effect"; item 13; short names; joins; X13; Effect | `reviews/codex2-rust3-lim-r1/review.json` (status `ACCEPTED`) |
| 12 | **Pin base.** Product main moved to `392499e`, which binds CRC-1, M3-C's core role closure successor, as the 83rd contract successor. Only `design-lock.json` changed. CRC-1 overrides no passage this law cites, agrees with items 1 and 5 on the core provider closure, and shares no parent with FA-2 or RUST3-LIM. The register pin is unchanged. | Product paths | `git diff cd5958b 392499e`; `crc-1/successor.json` (`29df5f5e…`) |

Nothing else changes in substance.

## r4 changes (kept for the record; G1 to G10 here are L-G1 to L-G10)

| # | Change | Where | Source |
|---|---|---|---|
| 1 | **r3 is preserved** as `PROPOSAL-r3.md` (`6df524a4…`). | header | — |
| 2 | **RF-1. Item 13's wire inventory is generated, not written (lead decision).** `evidence/wire_identities.py` reads every payload each frame carries from the cited schemas, walks every nested record, and classifies each member by a closed rule set (R1 to R6). Its output is item 13's table, inserted verbatim. The ceiling is "exactly these members". This corrects every point Grok raised: `subjectScopeCommitment` sits on `CoverageKeyV1`, not `FactCandidateV1`; `stageId` is on Analyze stage requests and on the FactBatch and Coverage wrappers; the Rust `subjectId` and anchor `factId` are included; snapshot, dependency-source and prepared frames carry `snapshotId`, `dependencySourceSetId` and `planId` respectively; `analysisOrdinal` and `phase` are listed as non-identity members. It also lists members neither r3 nor the review named, among them `relationSchemaId`, anchor `contentSha256`, `dependsOn`, the request-domain commitments, the prepared `planRow`, and the `target-attribution-v2` companion ids. **Rejected:** another hand-written list, which RF-1 showed drifts from the payloads. | item 13 | `reviews/grok-provider-protocol-l-r3` RF-1; lead direction |
| 3 | **Control L-C1.** `evidence/wire_identities.py --check` re-derives the inventory from the pinned bytes and fails on any difference from item 13's table or from `evidence/wire-identities.json`, which records each source's sha256. | item 13 | lead direction |
| 4 | **FA-2 needs no extra member.** The derived FA-2 rows are exactly §9.8's two members. No cross-law item for FA-2 arises. | item 13 | RF-1 check |
| 5 | **RF-2. The third delta-round trigger is exact.** Any change Codex's review forces in a part of FA-2 that sets a wire member, the commitment a key carries, the admission point or the reuse treatment reopens this law. That includes **every one of FA-2's four §0 rows (A to D)**, because each sets a wire value: A and B the Analyze and Complete payloads, C every key's commitment, D the Hello token arrays. What needs none is named exactly: FA-2's NE:93 header sentence, its schema layout, its vectors and evidence, its README prose and its materialization map. "Review and effect", G10, the dependence section, its summary table and X15 now agree. | "Review and effect"; gate; "What depends"; X15 | RF-2 |
| 6 | **NBO-1.** "The crate never mints `fact2`" is ME:478. | item 5; joins | NBO-1 |
| 7 | **NBO-2. Pin base.** Product main is now `cd5958b`. From `e093e90` to `cd5958b` the product changed `design-lock.json` (the I1-L, B-S1, B-S2, B-S9 and I1-P bindings; 77 to 82 contract successors) and X4-F1's `crates/security` files. Neither is a source this law reads for a rule. The lock's pin of the register (REG, `de21a7e0…`), which items 19-21 rely on, is unchanged. | short names | `git diff --name-only e093e90 cd5958b` |
| 8 | **NBO-3.** Item 22.3: a census's invalidation key covers every class item 6 names, including dependency source sets and prepared outputs. Per-file dirtiness is never sufficient by itself. | item 22.3 | NBO-3 |
| 9 | **Snapshots.** Every law is cited at a snapshot. J1 r4 (`PROPOSAL-r4.md`, `c18c0d3c…`) is re-checked: it changes nothing this law cites. M3-C r7 is in review (`PROPOSAL-r7.md`) and is not cited. M3-H r3 is in review and is not cited; only H r1's snapshot is (H1). | short names | coordinator direction |
| 10 | **FA-2 r2 joined (trigger 3 applied).** Codex's r1 findings forced two scoping changes in FA-2. FA2-R1-01: the NE:1927 insertion, §4.1a step 1's census source, applies only to symbol keys of a TypeScript or Rust universe. FA2-R1-02: X-FA2-C is narrowed to TS and Rust bindings that owe the worker's symbol census. NE:1927 is on trigger 3's reopen list, so this round takes it in: X16 and the M3-C joins row now state the narrowed cascade. Items 1, 13 and 22 and G10 need no change, because item 22 already concerns TS and Rust workers only, and the census schema bytes that L-C1 pins are unchanged. | X16; joins (MC); G10 and the FA2 short name (r2 in review) | `reviews/codex-fa-2-r1`; FA-2 r2 |

Nothing else changes in substance.

## r3 changes (kept for the record; G-numbers are L-G)

| # | Change | Where | Source |
|---|---|---|---|
| 1 | **r2 is preserved** as `PROPOSAL-r2.md` (`5bd4025e…`). Laws that cite r1 by line still resolve in `PROPOSAL-r1.md`. r3 keeps every item, X, R and O number. | header | — |
| 2 | **RF-1. Item 13's wire inventory is restated from NE, per protocol.** The four correlation identities stay. Beside them, item 13 now names every identity-bearing member the contracts already put on the wire: Hello and HelloAck (the members item 15 checks), each OpenUniverse payload's members (TS2 `universeKey`; Rust3 `repositoryResolution` with its set ids, `authorizationId` and `effects`), and the later echoes. It names FA-2's census member, under its token. The prohibition stays: no RequestId, RunId, ProjectId, log path, or identity the protocols do not carry. | item 13 | `reviews/grok-provider-protocol-l-r2` RF-1; NE:2816-2835, NE:2955-2981, NE:3158-3189 |
| 3 | **J1:192's citation of M3L:377** needs a content change after all. It is recorded as **X14**: J1's next revision re-cites item 13. It is **not** folded into J1 r4, which GROK2 has accepted, and whose line 207 carries the same sentence. X10 is corrected. | X10, X14 | RF-1's fix |
| 4 | **NBO-1. The gate citation.** "Review and effect" cites M3-C's pinned gate, MC:88-89, not the live file's recording paragraph. | "Review and effect"; short names | NBO-1 |
| 5 | **NBO-2. Every failed comparison is recorded.** When F > 2 s and T misses a medium budget, the S-M delta round records both (B) and (C) and raises both O3 and O4. | item 9; "What depends on O7, S-M and FA-2"; O3, O4 | NBO-2 |
| 6 | **NBO-3. M3-D is accepted at r3** (GROK2, `9679dbc4…`). The short name, item 17 and the joins row say so. The D law is still cited by role. | short names; item 17; joins | NBO-3; `reviews/grok2-supervisor-d-r3` |
| 7 | **X-H1. The symbol census is joined (lead decision).** New item 22 adopts FA-2's carrier: what crosses the wire, when it is admitted, and how reuse treats it. Item 1 names FA-2 as the one protocol change M3 makes, which is a native successor and not this law's. Item 10 covers the census. **G10, FA-2 accepted, is added to the gate.** **Rejected:** a gate without FA-2; drafting the carrier in this law. | items 1, 10, 22; gate | H1:724-732; FA-2 |
| 8 | **X-H4. In-core producer stages.** Item 5's "the host never constructs a fact that no admitted provider frame produced" gains its exact exception: a Plan-selected in-core producer stage. There are exactly two: E1's syntax stage, and the host inventory derivation H designs, which in a TS or Rust universe still waits for H's X-H3. | item 5 | H1:741; ME:477; MC:422-432; NCM:949 |
| 9 | **The review rule** gains a third delta-round trigger: a change that FA-2's acceptance forces on items 1, 13 or 22. | "Review and effect" | — |
| 10 | **"What depends on O7, S-M and FA-2"** gains FA-2, the joint (B)+(C) case, and a summary table following Grok's dependence list. | that section | `review.json` `gateDependence` |
| 11 | **New cross-law items:** X13, Rust3's 256-subject request cap (R12); X14, J1's re-citation; X15, the inherited key-commitment rules, which FA-2 closes; X16, FA-2's follow-ups for H, C, D, F, G and the plan. | "Cross-law findings"; R12, R13 | FA-2 README F-1, F-2 |
| 12 | **Re-pins.** J1 stays cited at its r3 bytes. J1 r4 is accepted and changes none of the provisions cited; it is pinned beside them. AQP, OPP and Q0 are still cited by their live accepted files, which differ from their snapshots only by a two-line note after line 1. Both are pinned. Product main has moved from `e093e90` to `15c0779`, and no product file this law cites changed. | short names | `git diff --name-only e093e90 15c0779` |
| 13 | **Joins checked**, refreshed: D r3, J1 r4, H, FA-2, I1-L, E1 and C r7. | "Joins checked" | — |

Nothing else changes in substance.

## r2 changes (kept for the record; G-numbers are L-G)

| # | Change | Where | Source |
|---|---|---|---|
| 1 | **r1 is preserved** as `PROPOSAL-r1.md`. Six laws and drafts cite r1 by line. Those lines still resolve there, and r2 keeps every item, X, R and O number they cite (X10). | header | — |
| 2 | **Review rule (lead decision).** Early review is allowed. An ACCEPT is "accepted in review" and takes effect only when every gate item is met. The `⟨SM-n⟩` values and any change O7 forces go through a delta round. A dependent's "M3-L accepted" means L in effect. **Rejected:** waiting for the gate before any review. | "Review and effect" | ON, "Lead decision: M3-L gets an early review round"; MC header |
| 3 | **Gate refreshed.** G2, G3 and G7 are MET, with their records. G4 and G5 are owner items (B3). G9 is an owner item (B1), with CF-P's evidence. G1, S-M, is still NOT STARTED. G6 and G8 are unchanged. | "Acceptance gate" | `reviews/grok2-corpus-t2b-r1`; HD:3; `reviews/codex-s-op-2-r6`; CFP; ON |
| 4 | **Dependence on O7 and S-M** is stated, item by item. | new section | — |
| 5 | **Re-pins.** Every plan citation is now `M3-PLAN-r6.md`:n (the M3-L row is line 207). S-OP-2 is cited at its accepted r6 bytes, J1, MC and ME at theirs. The product is main `e093e90`; no product file this law cites changed after r1's `2967905`. | throughout | `git diff --name-only 2967905 e093e90` |
| 6 | **S-OP-2's event names (item 14).** Each need is named exactly as S-OP-2 r6 registers it, and every one is registered. OPP:238's working name `supervision.no_progress` is registered as `supervision.progress.absent`. | item 14 | SOP2:864-894 |
| 7 | **stderr is counted, never held (item 12.1; lead decision).** The host reads stderr to EOF, counts it and keeps no text. **Rejected:** r1's hold-then-reduce. This closes the D law draft's departure from item 12.1. | item 12.1 | the D law's stderr item; `reviews/grok2-supervisor-d-r1` NBO-1 |
| 8 | **`detailCode` (item 12.2)** is S-OP-2's K3 `RustDetailCode` with an empty table. A member added later is a diagnostic label only. | item 12.2 | SOP2:844, :850-851 |
| 9 | **S-M's figures (item 9).** SM-10's unit is the platform's native unit, labelled, with a checked byte conversion. SM-5 and SM-6 also report `snapshot2`'s bounds. The workloads come from the complete T2 manifest. SM-1, SM-3 and SM-8 also inform the D law's constants. | item 9 | SOP2:910, :915, :1041 (R9); MC X-1; T2R |
| 10 | **Syntax universes have no child (item 2).** The in-host syntax pass is outside item 2's cardinality rules and is never a provider fallback. | item 2 | ME item 16 and §G; MC item 9 |
| 11 | **Where a child starts (items 2 and 13).** After MC's pre-execution joins, with the attempt's ExecutionId already reserved. "Attempt admission" for identities is read as J1 item 2 reads it. | items 2, 13 | J1 items 2 and 5.2; MC row 15 |
| 12 | **TypeScript `CancelV1` (item 16; lead decision).** M3 sends only `reason: user-interrupt`. `host-shutdown` is never sent. | items 16a, 16b | DLV:860 |
| 13 | **The commit-phase join is J1's (items 16f and 18).** Providers are live only in phase A. r1's "the provider part of phase B" is withdrawn. | items 16f, 18 | J1 8.2, 8.5, S15 |
| 14 | **Reuse disclosure per stage and universe (item 10)**, syntax stages included, as `host.reuse.disclosed`. | item 10 | SOP2:873; ME §G |
| 15 | **Cross-law findings.** X3 is answered for S-OP-12 by J1. X5 is addressed by the D law's draft. X8 is resolved by M3-PLAN r5. New: X9 to X12. | "Cross-law findings" | — |
| 16 | **Open questions.** R3, R8 and R9 are updated by the D law's draft. S-OP-2's R9 (SM-10's unit) is answered. New: R10 (Rust prepared entries) and R11 (the review rule). | "Open questions" | — |
| 17 | **Joins checked**, law by law. | new section | — |

Nothing else changes in substance.

**Standing direction.** Lead decisions are made under the owner's standing direction to decide on the lead's recommendation and to block only where no recommendation exists. r1's are dated 2026-10-03. r2's new ones (the review rule, item 12.1 and item 16b), r3's (G10 and item 22, item 5's in-core exception, and the third delta-round trigger) r4's (item 13's derived inventory with L-C1, and the exact scope of the third trigger) and r5's (rule R7, L-G11 with the fourth trigger, and the `L-G` rename) are dated 2026-10-04. Each names the alternatives it rejects. The owner may reverse any of them.

## Review and effect (lead decision, r2)

- **Decision.**
  - **Early review is allowed.** A law and contract-soundness review round may run now, before the gate is met.
  - **What an ACCEPT means.** It is recorded as "accepted in review". The law takes effect only when every gate item, L-G1 to L-G11, is met. M3-C's pinned gate works the same way: "This law may be reviewed now. It can be accepted when: **M3-L is accepted** … An unchanged draft is not acceptance" (MC:88-89). **(r3, NBO-1)** r2 quoted the live MC file's recording paragraph here. MC:88-89 is the pinned text.
  - **What reopens it.** Four things go through a **delta round**, with the same reviewer, on the diff only:
    1. filling every `⟨SM-n⟩` from S-M's report, with every outcome item 9 records, and any owner answer to O3 or O4 that those outcomes trigger;
    2. any change that O7's decision forces (see "What depends on O7, S-M, FA-2 and RUST3-LIM");
    3. **(r3; exact in r4, RF-2)** any change Codex's review forces in a part of FA-2 that sets a wire member, the commitment a key carries, the admission point or the reuse treatment. Such a change reaches items 1, 13 or 22, and item 10's census sentence, which follows item 22. It **includes every change to any of FA-2's four NE §0 rows**: each touches a wire value or commitment (A and B, the Analyze and Complete payloads; C, the commitment every key carries; D, the Hello and HelloAck token arrays). A §0 change confined to rows that touch no wire value or commitment would need no delta round, **but FA-2 has no such row.** The parts of FA-2 whose change needs none are named exactly in "What depends on O7, S-M, FA-2 and RUST3-LIM".
    4. **(r5)** any later change to RUST3-LIM's accepted bytes in a part that sets a wire member or a commitment. GROK2 accepted r1 with no change forced. Such a change can still come from a rebuild forced by a change Codex requires in FA-2's handshake copies, RUST3-LIM's parents, or from a later RUST3-LIM revision. It reaches items 1, 9 and 13 and L-G11. The parts are its token (its NE:2790 override and the handshake copies' `subjectScope` wire-law entry and enum), its NE §0 rows **E** and **F**, its §9.2, §9.6 and §9.3a overrides (NE:2883, NE:3028, NE:3070, NE:2942), and every record and law entry of its subject-scope schema. Its README prose, subject-count evidence, vectors, scratch verify and materialization map need none. **Its review's two NBOs:** NBO-1 corrects two copy-line annotations in its evidence, and needs none. NBO-2 would close a description census in one of two ways. Adding `RustFactBatchV2Vector.stageId` to the reading-rule list edits §9.3a's reading rule, and the schema's copy of it, so it takes this round. Giving that description NE:3070's parenthetical instead edits a handshake-copy description outside the `subjectScope` entry and enum, and needs none.

    The S-M delta round also refreshes the gate rows. A gate item met after that round (a sign-off, or O7 decided as recommended) is recorded as recording text in the live file's header note, unless it forces a change. A forced change takes its own delta round.
  - **What dependents may rely on.** Wherever another law or record names "M3-L accepted" or "L's acceptance" as a gate or as day 0, it means **L in effect**: accepted in review, every gate item met, and every delta round accepted. That covers MC's gate, `M3-PLAN-r6.md:255` and `:378`, and the D law draft's gate note. An ACCEPT in review alone satisfies no dependent's gate.
- **Basis:**
  - the overnight log's record of this lead decision (ON, "Lead decision: M3-L gets an early review round");
  - M3-C's pinned gate (MC:88-89; ON, "M3-C accepted in review at r5", "M3-C r6 accepted in review");
  - `M3-PLAN-r6.md:255`: "Day 0 is M3-L's acceptance. Because O7 and S-M are in L's gate, both are done by then."
- **Rejected:**
  - **Waiting for the gate before any review.** That was r1's rule, and its draft request said "Send this only once the M3-L acceptance gate permits". It serializes the day-0 law behind three owner items (O7, D3, D13) and a lead run set (S-M), and leaves the law's soundness unknown until all four close.
  - **Letting "accepted in review" satisfy dependents' gates.** A delta round under S-M, O7, FA-2 or RUST3-LIM could still change what they rely on, and day 0 would then start before O7 is decided, against `M3-PLAN-r6.md:476`.
  - **A full re-review when S-M lands.** Only the values and the outcome change. A delta round on the diff is enough, as M3-C r6's narrow amendment showed.
- **Consequence.** `M3-PLAN-r6.md:445` ("Before L can be sent: S-M, the two sign-offs and O7") and `:426` (r2 "fills ⟨SM-n⟩ after S-M") no longer describe the order. Cross-law item X9 routed the change to M3-PLAN's next revision. **(r5)** M3-PLAN r9, accepted, has made it: day 0 is "L in effect" (`M3-PLAN-r9.md:385`), and the M3-L row records the review rule and L-G10 (`M3-PLAN-r9.md:255`; P7-1, P7-2).

## Acceptance gate

Status on 2026-10-04. The gate is the M3-L row: "S-M, complete T2 (T2b), Q0, D3, D13 and the D2 draft, S-OP-2 drafted, O1 and **O7 decided**" (`M3-PLAN-r6.md:207`). **(r5)** M3-PLAN r9, accepted, adds "and **FA-2 accepted (G10, P7-2)**" (`M3-PLAN-r9.md:255`), which is L-G10 here. The same row says "The S-OP-4 join is the law's content, not a gate item", so S-OP-4 is item 12, not a gate row. Under "Review and effect", the gate decides when L takes effect, not when it may be reviewed.

**(r5, lead decision) L-G11 is this law's second addition.** L in effect fixes Rust3 for M3. Without RUST3-LIM, Rust3 refuses before spawn every snapshot with more than 256 non-empty `.rs` files: nine of T2's 22 Rust entries, including two of S-M's seven Rust medium workloads, `rs-medium-axum` (301) and `rs-medium-tokio` (808) (X13; RUST3-LIM's own count agrees in 21 of 22 entries). **Rejected:** taking effect with X13 open. That would fix for M3 a Rust protocol that cannot serve the workloads its own spike measures. The plan's next revision records L-G11 (X9).

**(r3, lead decision) L-G10 is this law's addition to the plan's row.** Item 22 joins FA-2's carrier, and L in effect fixes TS2 and Rust3 for M3. Without FA-2, no TypeScript or Rust symbol-kind Coverage can be admitted, which covers nine of the thirteen relations (NE:403), so F2 and G3 could not deliver their symbols lawfully (H3:850-858). **Rejected:** leaving FA-2 out of the gate. L would then take effect on a protocol that cannot carry what its dependents need, and item 22 would join nothing. The plan's next revision records L-G10 (X9).

| # | Gate item | Status | Evidence |
|---|---|---|---|
| L-G1 | **S-M**, the INC-7 spike, measured | **NOT STARTED.** It is a lead run set (`M3-PLAN-r6.md:205`). P5-8's machine order puts it after Grok's rerun on C (done), F8b's cargo steps (done: F8b is bound at product main `e093e90`) and X4-F1's lanes and reruns (`M3-PLAN-r6.md:593`). **(r3)** X4-F1 has since been accepted by GROK2 and integrated at product main `15c0779` (ON, "X4-F1 accepted by GROK2 and integrated"). This law does not record whether P5-8's other reruns after it have run. If O7 is decided while both wait, S-M moves ahead of X4-F1 (`:594`). Its report also waits for the D13 sign-off (L-G5). Its Q6-labelled samples wait for D12 (`:205`). Item 9 lists the figures it must deliver. Every number that depends on it is a placeholder `⟨SM-n⟩`. | `M3-PLAN-r6.md:205`, `:371`, `:435`, `:593`; ON, "Grok's X9-6 rerun on C was accepted" and "F8b accepted and bound"; no S-M report exists |
| L-G2 | **T2 complete (T2b)** | **MET.** GROK2 accepted T2b with no findings. The T2 manifest holds 49 repositories, 5 multi-repo workspaces and 33 independence families. | `reviews/grok2-corpus-t2b-r1/status.json` (`ACCEPTED`); T2R:24; `M3-PLAN-r6.md:203`, `:436`; ON, "M3-T2b accepted by GROK2" |
| L-G3 | **Q0** | **MET.** CODEX2 accepted the harness design record r13 (sha256 `37438317…`; envelope schema `71f682d1…`). | HD:3; `M3-PLAN-r6.md:204`, `:437` |
| L-G4 | **D3**, the T2 selection | **OPEN: an owner item** (blocker B3). It is lead work with owner sign-off, status `proposed` (AQP:543). No sign-off is recorded. The lead recommends approval as reviewed. | AQP:543; ON B3; `M3-PLAN-r6.md:438`, `:534` |
| L-G5 | **D13**, the exploratory envelope | **OPEN: an owner item** (blocker B3). ENV's mechanisms were accepted within Q0 r13 (HD:1141-1158), but the sign-off is open (HD:1245, OI-1; AQP:554). D13 also gates S-M's report (L-G1). D13's second half, the DR-G13 successor, is M6 work and is not in this gate. | AQP:554; HD:1245; ON B3; `M3-PLAN-r6.md:439`, `:534` |
| L-G6 | **D2 drafted** | **MET, on the lead's reading.** The rule-catalog draft specs are Q0 §2 (HD:276-300), accepted in r13. D2's placement decision (a first-party `PolicyDocumentV2` pack through a WS/pack successor) is still `proposed`, with owner sign-off (AQP:542; HD:1259, OI-15). The gate asks for the draft, not the sign-off. A reviewer may read it otherwise (open question R7). | AQP:542; `M3-PLAN-r6.md:440` |
| L-G7 | **S-OP-2 drafted** | **MET, and exceeded.** Codex accepted S-OP-2 at r6, ACCEPT-DESIGN-UNIT with no required findings (`ce8d3a4b…`). Item 14 checks that it registers every event this law needs. It does. | SOP2; `reviews/codex-s-op-2-r6/status.json` (`ACCEPTED`); ON, "S-OP-2 accepted at r6 by Codex" |
| L-G8 | **O1** | **DECIDED IN THIS LAW** (item 11), as a lead decision. Accepted S-OP-2 r6 is written within it (SOP2 item 19), and the plan records it (`M3-PLAN-r6.md:463`). It becomes final when this law takes effect. | `M3-PLAN-r6.md:442`, `:463`; OPP:394 |
| L-G9 | **O7 decided** | **OPEN: an owner decision**, blocker B1. **CF-P has run.** It is evidence for O7, not a decision, and it claims nothing as enforced (CFP:3):<br>- **macOS 27:** programmatic Seatbelt confinement through `sandbox_init_with_parameters` is feasible, provided the profile adds a `kern.procargs` sysctl denial (one of five amendments CF-P asks of the D law's profile draft). Deprecation risk is high, so each macOS major needs its own check (CFP:231-264).<br>- **AL2023, by desk check only:** feasible on kernels 6.1.147, 6.12.40, 6.18 and later. Earlier kernel builds lack Landlock and disclose (CFP:309-315).<br>The lead's recommendation is in ON B1 and `M3-PLAN-r6.md:478-485`. This law neither decides O7 nor assumes its outcome (item 17). | ON B1; CFP:3, CFP:231-264, CFP:309-315; `M3-PLAN-r6.md:476`, `:532` |
| L-G10 | **(r3) FA-2 accepted**: the provider symbol-census carrier, a native contract successor (M3-H X-H1) | **OPEN: in review with Codex.** r1 (`reviews/codex-fa-2-r1`) returned REQUIRED-FINDINGS on two scoping points, and r2 is in review (`reviews/codex-fa-2-r2`; ACCEPT-DESIGN-UNIT wanted). Item 22 joins it as proposed. **(r4)** A change Codex requires to any part of FA-2 that sets a wire member, a key's commitment, the admission point or the reuse treatment, including any of its four §0 rows, takes this law's third delta round ("What depends on O7, S-M, FA-2 and RUST3-LIM"). | FA2 README and §9.8; H3:850-858; item 22 |
| L-G11 | **(r5) RUST3-LIM accepted**: the Rust3 request subject list by reference, a native contract successor (this law's X13; R12) | **MET IN REVIEW, held on FA-2.** GROK2 accepted RUST3-LIM r1 (`reviews/codex2-rust3-lim-r1`, a directory name kept from the CODEX2 assignment; status `ACCEPTED`): ACCEPT-DESIGN-UNIT, no required findings, two non-blocking observations, on subject `5dfd3cd9…` and successor `70f494d9…`, the bytes this law pins. Its unit record (`rust3-lim-unit.json`) is the lead's to complete. Its parents are FA-2 r2's two handshake copies, still in review with Codex. If Codex's review changes them, RUST3-LIM is rebuilt on the new copies, and L-G11 is open again until the rebuild is accepted. It binds in `design-lock.json` only after FA-2 is bound (RL LD-R8). A later change in a part that sets a wire member or a commitment takes this law's fourth delta round. | RUST3-LIM README (X-RL-L1, LD-R8); `rust3-lim/section-9-3a.md`; `reviews/codex2-rust3-lim-r1/review.json`; X13 |

**Before L takes effect:**
- S-M runs (L-G1), and its delta round fills every `⟨SM-n⟩`, records every outcome item 9 names and refreshes these rows;
- the owner signs off D3 and D13 (L-G4, L-G5) and decides O7 (L-G9);
- Codex accepts FA-2 (L-G10);
- **(r5)** RUST3-LIM stays accepted (L-G11). GROK2 has accepted it, and the acceptance holds unless Codex's review changes FA-2's handshake copies;
- any change that O7 or FA-2's acceptance forces, or that a later change to RUST3-LIM's accepted bytes makes, passes its own delta round.

**Not in this gate:**
- CF-P, which gates the D law, not this one (`M3-PLAN-r6.md:211`). It has run, and L-G9 cites it as evidence.
- D12, which gates only S-M's Q6-labelled samples (`M3-PLAN-r6.md:205`).
- Every D5a successor. Item 3's table explains why none is needed for M3.
- The D law, now accepted at r3 (NBO-3). This law cites it by role (item 17). The D law names this law as one of its inputs, not the reverse.
- **(r3)** M3-H. H depends on this law and on FA-2, not the reverse. The H code legs that FA-2 gates are H's (H3 item 25).
- **(r5)** X13 is no longer listed here: r3 and r4 kept it out of the gate, and r5 gates it as L-G11.

## What depends on O7, S-M, FA-2 and RUST3-LIM

r2 stated its own reading here so that the reviewer could test it. Grok's r2 review found it complete for the outcomes it named, apart from the joint case (NBO-2). r3 adds that case and FA-2.

**S-M.**
- **Item 9 depends on it entirely:** every `⟨SM-n⟩`, the derived F and T, and the outcomes (A), (B) and (C).
- **Some things depend on it conditionally:**
  - owner questions O3 and O4 arise only on outcomes (B) and (C). **(r3, NBO-2)** When F > 2 s and T misses a medium budget, both outcomes hold. The delta round records both, and both O3 and O4 arise. Items 1 and 2 stay one-shot under both;
  - X6, liveness against synchronous compiler work, is sized by SM-8, which also sets the D law's liveness floor;
  - SM-6 may raise a TS2 limit question, which only a successor can answer (item 1);
  - SM-5 and SM-6 decide whether MC's conditional S-R is needed (MC item 5).
- **No other item depends on S-M's values.** Under every outcome, items 1 and 2 keep TS2 and Rust3 one-shot for M3 (item 9's outcome text). If the owner's answer to O3 or O4 changes D5's staging, that is the owner's decision, outside this law. This law would then need a delta round only to change M3's protocol, which item 1 forbids without a successor.

**O7.**
- **No item's text depends on O7's outcome.** O7 decides when L takes effect (L-G9) and when a provider may launch (item 17; `M3-PLAN-r6.md:476`).
- **A delta round is needed only if O7 is decided in a way that:**
  - lets a provider execute repository code at M3. That contradicts item 17's third requirement and NE:2534-2535, and would need contract successors as well;
  - needs a wire signal or wire member at the provider boundary for confinement. Item 1 forbids that, and CF-2's disclosure carrier sits "beside Coverage and never inside it" (`M3-PLAN-r6.md:504`);
  - changes item 2's process model, for example with a resident or pooled confined helper.
- **Under the lead's recommendation, none of these arises.** The confinement records are the D law's own registrations (its records item), not needs of item 14.

**FA-2 (r3).**
- **L-G10 depends on it,** and items 1, 13 and 22 cite its proposed content: the token, the census member on Analyze and `Complete`, the census-free request commitment, and admission at clean settlement.
- **A delta round is needed (r4, RF-2)** whenever Codex's review forces a change in a part of FA-2 that sets a wire member, the commitment a key carries, the admission point or the reuse treatment. Item 10's census sentence follows item 22, so a reuse-treatment change that moves it belongs to the same round. Mapped to FA-2's parts (FA2 README, "What changes"):
  - **Reopens this law:**
    - every NE §0 row FA-2 adds (the override of NE:138), because each touches a wire value or commitment:
      - **A** and **B** replace the Analyze and Complete payloads;
      - **C** sets the commitment every key carries, with or without the token (FA2 LD-F7; X15);
      - **D** extends the Hello and HelloAck token arrays;
    - NE:1913 and NE:1927 (§4.1a: a symbol scope's subjects, the input to every symbol key's commitment);
    - NE:2791 and NE:2814 (the token);
    - NE:2884 and NE:2990 (the payload versions);
    - NE:3235, NE:3279 and NE:3292 (the commitments the pre-Analyze, returned and terminal symbol entries carry);
    - NE:3313 (§9.8 itself);
    - NE:4195 (join H-9, the census's ownership and admission law);
    - the three provider-startup pointer overrides (commitments);
    - the handshake copies (the token and the `symbolCensus` wire law);
    - every record and every law entry of the census schema.
  - **Needs none:**
    - FA-2's NE:93 header sentence, while §9.8 is unchanged;
    - a change to the census schema's layout (key order, descriptions, `$defs` names) that leaves every member, bound and law entry unchanged;
    - FA-2's vectors and evidence script;
    - its README prose;
    - its materialization map.

  **No FA-2 §0 row is in the second list.** A §0 change confined to rows that touch no wire value or commitment would need no delta round, but FA-2 has no such row.
- **If FA-2 is rejected outright,** item 22 joins nothing and L-G10 cannot be met. The next revision of this law follows FA-2's successor.
- **X13 does not depend on FA-2,** and FA-2 does not decide it; RUST3-LIM does (below).

**RUST3-LIM (r5).**
- **L-G11 depends on it**, and so do:
  - item 13's RUST3-LIM row, and the AnalyzeV2 row's condition on its `stages[]` members;
  - item 9's SM-11 to SM-14, which it proposes;
  - item 1's naming of it;
  - X13 and R12, which it closes.
- **A delta round is needed** whenever a later change to RUST3-LIM's accepted bytes, including a rebuild forced through FA-2's handshake copies, changes a part that sets a wire member or a commitment. GROK2's r1 acceptance forced none. The full map of reopening parts, and of the parts that need none, is the fourth trigger ("Review and effect").
- **If a rebuild of RUST3-LIM is refused,** which can arise only if FA-2's review changes its parents, L-G11 is open again, X13 reopens, and this law's next revision follows RUST3-LIM's successor.
- **No item's text depends on S-M's figures through RUST3-LIM:** SM-11 to SM-14 set budgets and the effective subject ceiling, not a protocol constant (RUST3-LIM "What S-M must measure").

**Summary (r3; Grok's `gateDependence`, extended; RUST3-LIM row r5).**

| Depends on | What |
|---|---|
| O7 | L-G9; item 17; a delta round only if the outcome lets a provider execute repository code, needs a new wire signal or member for confinement, or makes the provider resident or pooled |
| S-M | item 9: every `⟨SM-n⟩`, F, T, and every outcome; O3; O4; X6, through SM-8; a TS2 limit question that only a successor can answer, through SM-6 (item 1); MC's conditional S-R, through SM-5 and SM-6 |
| FA-2 | L-G10; items 1, 13 and 22, and item 10's census sentence (which follows item 22); a delta round for any forced change to a wire member, a key's commitment (**including every FA-2 §0 row, A to D**), the admission point or the reuse treatment. None for FA-2's NE:93 header sentence, schema layout, vectors, evidence, README prose or materialization map |
| RUST3-LIM | L-G11; items 1 and 13 (its row, and the AnalyzeV2 row's condition); item 9's SM-11 to SM-14; X13 and R12; a delta round for any later change to a part that sets a wire member or a commitment, including a rebuild forced through FA-2's handshake copies (its token, §0 rows E and F, §9.3a and its §9.2 and §9.6 overrides, the subject-scope schema). None for its README prose, evidence, vectors, scratch verify or materialization map |
| No text change under any outcome above | items 2-8, 10-12, 14-16 and 18-21. Item 12.4 names SM-8 but states no number. Item 10's census line follows item 22. |

## Short names

Line numbers are those of the cited files on 2026-10-04. A live plan or design file that carries a two-line acceptance note is 2 lines ahead of its `-rN` snapshot. AQP, OPP, Q0 and ENV have not changed since r1, so r1's lines for them stand.

**(r3) Pinning.** Every other **law** is cited at an accepted snapshot, never at a live `PROPOSAL.md`, because a live file can move to a new draft mid-review. AQP, OPP and Q0 are accepted **plans**, still cited by their live files as r1 and r2 cited them. Each live file is exactly its snapshot (`analysis-quality/PLAN-r6.md`, `operability/PLAN-r3.md`, `harness/DESIGN-r13.md`) plus a two-line note inserted after line 1, checked byte for byte. So live line n ≥ 3 is snapshot line n − 2. The review request pins both.
- **M3P** `docs/implementation/m3/M3-PLAN-r6.md`, the accepted r6 bytes (sha256 `a6956e88…`). The live `M3-PLAN.md` carries the acceptance note and is 2 lines ahead. **Every plan citation here is `M3-PLAN-r6.md`:n**, except where `M3-PLAN-r9.md` is named.
- **M3P9 (r5)** `docs/implementation/m3/M3-PLAN-r9.md`, M3-PLAN r9, **accepted** (`72bc7a13…`; `reviews/grok2-m3-plan-r9`). It records L's review rule, day 0 as "L in effect" (`:385`) and L-G10 in the M3-L row (`:255`; P7-1, P7-2). Its NBO-1 asks for the `L-G` rename, which r5 makes. r6's lines stay this law's general plan citations: r9 changes none of the rows this law relies on except those three records.
- **AQP** `docs/implementation/m3/analysis-quality/PLAN.md` (r6, accepted; live file, sha256 `1611014d…`)
- **OPP** `docs/implementation/m3/operability/PLAN.md` (r3, accepted; live file, sha256 `4eca344b…`; the r3 bytes are `PLAN-r3.md`)
- **Q0, HD** `docs/implementation/m3/harness/DESIGN.md` (r13, accepted; live file, sha256 `1f108399…`)
- **ENV** `docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json`
- **SOP2** `docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`, the S-OP-2 r6 bytes Codex accepted (`ce8d3a4b…`). The live file differs only in recording text.
- **J1** `docs/implementation/m3/host-pipeline-j/PROPOSAL-r3.md`, the M3-J1 r3 bytes CODEX2 accepted (`ad887c90…`)
- **J1r4 (r3)** `docs/implementation/m3/host-pipeline-j/PROPOSAL-r4.md`, the M3-J1 r4 bytes **accepted by GROK2** (`c18c0d3c…`; `reviews/grok2-host-pipeline-j-r4`). r4 adds row R10a and its ephemeral counterpart ER10a, widens J-β to R4-R10a, and adds SD-6's successor rows S19 and S20 and their controls. It changes no provision this law cites: item 2, J-ε, J-ζ, item 8, 8.5, and rows 30 and 46 read the same, at lines shifted by 14 to 32. This law keeps citing r3's bytes, and cites r4 as `J1r4:n` where r4's own line is meant.
- **MC** `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r6.md`, the M3-C r6 bytes CODEX2 accepted in review (`8274bca1…`). Its gate is MC:88-89: it may be accepted once this law is accepted (NBO-1). **(r3)** The live `PROPOSAL.md` now holds the r7 draft, in review with CODEX2. r7 narrows only item 16's row 8, and it is not cited.
- **ME** `docs/implementation/m3/syntax-e/PROPOSAL-r3.md`, the M3-E1 r3 bytes Codex accepted (`d71031ff…`)
- **MB** `docs/implementation/m3/config-discovery-b/PROPOSAL-r2.md` (M3-B r2, accepted by GROK2)
- **I1** `docs/implementation/m3/preview-pack-i1/PROPOSAL-r2.md` (M3-I1 r2, accepted by CODEX2)
- **X12r4, X2r9** `docs/implementation/m2/policy-admission-x12/PROPOSAL-r4.md` and `docs/implementation/m2/project-root-x2/PROPOSAL-r9.md` (accepted by Grok)
- **The D law (MD)** `docs/implementation/m3/supervisor-d/PROPOSAL-r3.md`: M3-D r3, **accepted by GROK2** with no required findings (`9679dbc4…`; `reviews/grok2-supervisor-d-r3`) **(r3, NBO-3)**. The live `PROPOSAL.md` differs only in recording text. **It is still cited by role** ("the D law's stderr item", "its constants table"). Its section F is still an O7 placeholder. r2 pinned exactly these bytes as a draft, so wherever kept r2 text says "the D law's draft", it now means the accepted r3.
- **(r4; r5) Other laws in review, not cited:** M3-C r7 (`snapshot-plan-c/PROPOSAL-r7.md`, `a1ee9386…`, accepted in review with CODEX2; it narrows only item 16's row 8). M3-H r3 is now accepted and is cited (H3, below). **J1 r4 re-checked (r4):** its only changes against r3 are R10a, ER10a, J-β's range, SD-6's rows S19 and S20 and their controls, and the M3D short name. None is a provision this law cites.
- **H3 (r5)** `docs/implementation/m3/fact-admission-h/PROPOSAL-r3.md`, M3-H r3, **accepted** (`7a562720…`). r3 and r4 cited H r1 (`PROPOSAL-r1.md`, `69f50bb1…`) as H1, a reviewed draft. r5 re-maps every H1 citation to H3:
  - X-H1 (H1:724-732) is H3:850-858;
  - X-H4 (H1:741) is H3:867;
  - item 17 (H1:490-519) is H3:613-643;
  - "Without FA-2" (H1:582) is H3:705;
  - the round-timing line (H1:715) is H3:841.

  Item numbers 3, 4, 17, 18 and 25 are unchanged. The kept change tables keep their H1 citations.
- **RL (r5)** `docs/implementation/m3/native-successors-fa/rust3-lim/`: RUST3-LIM, the native contract successor for this law's X13 (R12), accepted by GROK2 at r1 with no required findings (`reviews/codex2-rust3-lim-r1`; subject `rust3-lim-subject.json`, `5dfd3cd9…`; successor `rust3-lim/successor.json`, `70f494d9…`). §9.3a as it proposes it is `rust3-lim/section-9-3a.md`, its subject-scope schema `rust3-lim/design/native/rust-subject-scope.schemas.v1.json` (an L-C1 source), and its design record `rust3-lim/README.md`. **Accepted, not yet bound:** it binds after FA-2 (RL LD-R8; L-G11).
- **FA2 (r3)** `docs/implementation/m3/native-successors-fa/fa-2/`: FA-2, the native contract successor for X-H1, in review with Codex. r1's review (`reviews/codex-fa-2-r1`) is REQUIRED-FINDINGS; **r2** is in review (`reviews/codex-fa-2-r2`, subject `dca02900…`). Its subject manifest is `native-successors-fa/fa-2-subject.json` and its record `fa-2/successor.json`. NE §9.8 as FA-2 proposes it is `fa-2/section-9-8.md`, and its design record is `fa-2/README.md`, cited as "FA-2 LD-Fn". **Proposed, not accepted** (L-G10).
- **I1L (r3)** `docs/implementation/m3/preview-pack-i1/i1-l/`: I1-L, accepted by CODEX2 (ACCEPT-DESIGN-UNIT) and bound at product `0ceb9ad`.
- **ENC / EXC / SIS / RPS (r3)** `docs/coop/design-corrections/foundation/{enumeration-contract.v1.md, execution-inputs-contract.v1.md, subject-inventory.schema.v1.json, relation-payload-schemas.v2.json}`
- **NCM (r3)** `docs/coop/design-corrections/native/native-capability-matrix.v2.json`
- **CFP** `docs/implementation/m3/confinement-cf/CF-P-RECORD.md` (a record, not law)
- **T2R** `docs/implementation/m3/corpus/README.md` (T2a and T2b accepted by GROK2). **T2M** is its manifest, `t2-corpus-manifest.draft.json`.
- **ON** `docs/implementation/OVERNIGHT-2026-10-03.md`, a live log, cited by entry
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

None of the contract, architecture or protocol files above has changed since r1.

Product paths are under `opensip/`, at main `e093e90`. Every product file this law cites is unchanged since r1's `2967905`: `git diff --name-only 2967905 e093e90` lists none of them. They were read, not run. **(r3)** Main has since moved to `15c0779`: the I1-L, B-S1, B-S2 and B-S9 bindings, and X4-F1. **(r4, NBO-2) Pin base.** Main is now `cd5958b` (the I1-P binding, after `15c0779`). `git diff --name-only e093e90 cd5958b` lists `design-lock.json` (the five bindings; 77 to 82 contract successors) and X4-F1's `crates/security` files. **(r5) Pin base.** Main is now `392499e`, CRC-1's binding after `cd5958b`. `git diff --name-only cd5958b 392499e` lists only `design-lock.json`, which appends CRC-1, M3-C's core role closure successor, as the 83rd contract successor. CRC-1 overrides IE:285, IE:1377, WS:308, the evaluator-composition contract's line 9, the effective workflows reference's line 312, three pointers of I1-L's identity schemas and the detector-manifest schema's description. This law cites none of them. Its IE:1377 rule agrees with item 1's syntax-universe sentence and with item 5's forbidden substitute: the core provider closure is a direct `semanticClosures` member exactly when the Plan selects a `native.semantic-universe.syntax.v2` universe, and is never selected otherwise. It shares no parent or overridden passage with FA-2 or RUST3-LIM.
- No source this law reads for a rule changed: `Cargo.toml`, `providers/rust/src/main.rs`, `crates/contracts/src/generated/protocol.rs`, `schemas/wire/native-carriers-v1.json` and `crates/lifecycle/src/installation.rs` are unchanged.
- `design-lock.json` is cited only as the register's pin (items 19-21; RH:29-31). Its input pin of the register (`08-decision-and-readiness-register.md`, `de21a7e0…`) is the same at `e093e90`, `cd5958b` and **(r5)** `392499e`.

## Problem

M3 builds the first real providers and the supervisor around them (BP:887; `M3-PLAN-r6.md:211-215`). Before the provider protocol is fixed, three accepted records require one law to settle the following.

**The quality plan.** Its reuse obligations INC-1 to INC-8 must be "written into the M3 law, plus the INC-7 spike" (AQP:499). They are "the condition that the M3 provider protocol and host law must be able to satisfy, whether or not changed-scope ships at M3" (AQP:387). Any of them that needs a contract change goes through D5a (AQP:546).

**The operability plan.** "Before the M3 provider protocol law" (OPP:380), it needs:
- O1 decided;
- the S-OP-4 record join under O1(a);
- O7 decided;
- S-OP-2 drafted;
- INC-1 to INC-8 in the same law.

It also needs the provider side of two-stage cancellation (OPP:329) and the phase-lawful identity rule (OPP:149-159).

**The unit plan.** It gives this law three more pieces (`M3-PLAN-r6.md:207`, `:467-469`, `:624-628`):
- the DR-G14 placement and changed-scope choices;
- a record correction for DR-G10;
- a record of two other stale texts.

**What exists today.** At product `e093e90`:
- there is no `crates/components` (`git ls-tree e093e90 crates/`; `Cargo.toml:3`);
- the Rust provider exits before reading a request (`providers/rust/src/main.rs:1-14`);
- the generated TS2 and Rust3 carriers (`crates/contracts/src/generated/protocol.rs:5422`, `:6111`) come from an input that is "not a production wire decoder, not semantic admission" (`schemas/wire/native-carriers-v1.json:4`).

So no implementation constrains this law. The accepted contracts, plans and laws do.

## Decisions

Lead decisions are dated 2026-10-03 unless marked r2, r3, r4 or r5 (2026-10-04). They are recorded under the owner's standing direction to decide on the lead's recommendation and to block only where no recommendation exists. The owner may reverse any of them.

### A. Protocols and process lifetime

**1. TS2 and Rust3 are the M3 provider protocols, unchanged (INC-5).**
- **Decision.** M3's providers speak exactly two protocols:
  - `typescript-semantic` major 2;
  - `rust-semantic` major 3.

  Each is as NE §9 defines it (NE:2781-3313), over its inherited base: DLV for TypeScript, and the RPP v2 / v4 merge for Rust (F02:259-269). This law adds nothing to either protocol: no frame, member, phase, terminal kind, capability token, limit, identity version or negotiation choice. Handshakes stay per language: `TypeScriptHelloV2`/`TypeScriptHelloAckV2` and `HelloV3`/`HelloAckV3` (BP:718-719). Both still require exact token-array and identity-version echo (NE:2792-2796, NE:2837-2844).
  - **The optional `target-attribution-v2` token.** Whether a signed capability row carries it stays a matter for that row and for the provider units (F, G). This law changes neither branch of NE:2799-2814.
  - **(r3) FA-2, the one protocol change M3 makes, is not this law's.** FA-2 is a native contract successor reviewed on its own (ACCEPT-DESIGN-UNIT; L-G10). It adds the optional, non-identity token `symbol-census-v1` and, under it, one member, `symbolCensus`, on the existing `Analyze` and `Complete` payloads of both protocols (FA2 §9.8). It adds no frame, phase, terminal kind, limit member, identity version or major, as NE did for `target-attribution-v2` ("Protocol major stays 3 / TypeScript major 2", NE:2811). AQP:402 requires exactly this for a wire change: "a reviewed successor; the protocols are not unselected". Once FA-2 is accepted, "TS2 and Rust3" in this law means NE §9 with FA-2's successor. Item 22 joins it.
  - **(r5) RUST3-LIM, the second, is not this law's either.** It is a native contract successor reviewed on its own (L-G11). It adds the optional, non-identity `rust-semantic` token `subject-scope-reference-v1` and, under it, one stage-record version in the existing Rust `Analyze` `stages` array: `StageRequestV3`, whose analysis domain names the subject array by reference (`RustSubjectScopeV1`) instead of inline (RL §9.3a). It adds no frame, phase, terminal, limit member or value, identity version or major, and `ProtocolLimitsV3` keeps every value. It is accepted, and it binds after FA-2. From then, "TS2 and Rust3" in this law also includes it.
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
  - any extra wire member or frame, for example for progress, diagnostics, correlation or reuse. **(r3; r5)** The members FA-2 and RUST3-LIM add, each reviewed as a native successor, are the only ones M3 adds (items 13 and 22);
  - a negotiated "extension" that changes frame meaning;
  - citing F02:220 ("major is **1**") or F02:259 ("**major 2**") as the current majors (item 20).

**2. One child per universe, one-shot, no reuse.**
- **Decision.** For each `(ExecutionId, SnapshotId, universe key)` of a TypeScript or Rust semantic universe, the host launches exactly one provider process. The universe key is TypeScript's `universeKey` (NE:3166-3177) and, for Rust, the native semantic-universe identity (NE:3161-3163).
  - **TypeScript.** The `workerCardinality` rule applies unchanged (DLV:556-565):
    - one worker per distinct key;
    - shared across the matching TypeScript stages of that key;
    - never multiplexing different keys;
    - never reused across ExecutionIds;
    - never retained after its terminal;
    - never resident.
  - **Rust.** One supervised sidecar per semantic universe, with no reuse (F02:268-269).
  - **Syntax universes have no child (r2).** A `native.semantic-universe.syntax.v2` universe is produced in the host by the core provider closure (MC item 9; ME item 14b), with no provider process. This item's cardinality, start and end rules do not apply to it (ME §G). The in-host syntax pass is never a fallback for a TypeScript or Rust child (the "No in-process fallback" bullet below; ME item 16).
  - **When a child may start.** Only after the host has bound `SnapshotId`, `PlanId` and the complete universe key (DLV:566). **(r2)** Only after MC's pre-execution joins over the built Plan, "before any provider" (MC:867, row 15). And only through NE §9.1's reject-before-disclosure order (NE:2846-2866). In J1's pipeline that is join J-ζ, after J-ε (J1 item 5.2). The attempt's ExecutionId is already reserved by then (item 13; J1 item 2).
  - **How a child ends.** After its terminal it reaches zero-exit, then EOF, and its scratch is destroyed (DLV:567; RPP:582). After `Cancelled`, TypeScript requires only EOF (T2O:261-266).
  - **No restart.** A faulted child is never restarted within its attempt (OPP:273). A new attempt has a fresh ExecutionId (WS:81-82), and so fresh children. M3 retries no attempt in process (J1 item 5.1).
  - **No in-process fallback.** A failed launch or child is never replaced by in-process analysis (OPP:135, F7; AQP:114). M3-E1 relies on this bullet as one of its five reasons why syntax never substitutes for a semantic rung (ME item 16).
  - **The harness.** Its warm runs follow the same rule: each is a new process "with … no reused provider process" (Q0:805).
- **Basis:**
  - F02:222-224: "one child per `(ExecutionId, SnapshotId, TypeScriptSemanticUniverseKey)`, and no reuse remain unchanged. R-1 one-shot/lifetime-neutral constraints also apply";
  - QG:202 ("one-shot");
  - DLV:567: "A child is never retained for a later request";
  - DLV:1517 (DL-13): "never reuses worker state";
  - ME §G: "Syntax is **in the host**, not a provider. L's one-child-per-universe rules do not apply to it."
- **Rejected:**
  - **A pre-spawned or pooled warm worker** to hide start-up cost. It crosses ExecutionIds (DLV:562), and DLV:1197 already rejected a "resident tsserver or language-server daemon".
  - **Multiplexing universes in one Node process** (DLV:561).
  - **Spawning before Plan binding**, even with no bytes sent (DLV:566).
- **Forbidden substitutes:**
  - a worker kept alive between invocations, attempts or Plans under any name ("warm", "cached", "pooled");
  - a host-side store of provider frames replayed to a new child;
  - a provider restarted after a fault within one attempt;
  - in-process analysis after a provider failure;
  - **(r2)** a provider child for a syntax universe.

**3. Changed-scope at M3: none ships (lead decision; `M3-PLAN-r6.md:469`).**
- **Decision.** M3 builds no producer cache and no changed-scope path. Every M3 run is full analysis of its Plan.
  - **What binds later work.** Items 4-10 bind any changed-scope or resident design.
  - **Who decides it.** M4 decides whether changed-scope ships, with S-M's data (AQP:502; `M3-PLAN-r6.md:469`).
  - **Explicit scope is not incremental.** A narrower Plan through the existing scope descriptor (`workspaceRoots`, `pathPrefixes`; NE:4276) is lawful today and needs no successor. But it is a different Plan with its own Coverage, it is not reuse, and it never satisfies INC-4.
- **Basis:** `M3-PLAN-r6.md:469`: "Changed-scope (M3-L). Recommendation: none ships. ML item 4 found that cross-edit reuse needs an IE successor (the INC-1 successor), because `cache2` binds the Plan. It is owned by the identity owner (AQP:546) and decided at M4 with S-M's data (AQP:502)."
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
| INC-7 | 9 | Gate item L-G1. | **Pure law.** |
| INC-8 | 10 | The operational record says `recomputed`, cause `no-reuse-path`. | **Pure law.** The public carrier at M4 is S-OP-6, an operability successor, not D5a. A semantic Coverage successor is forbidden. |

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
  - **For any later reuse.** The INC-1 successor must define how a reused producer candidate is re-admitted under the new snapshot, including anchors and producer attestation. The host must never construct a fact that **neither an admitted provider frame nor a Plan-selected in-core producer stage** produced **(r3, X-H4)**. A faulted or cancelled worker "contributes **no facts, no Coverage entries and no Run**" (NE:3837-3843), and framing grants no fact authority (`M3-PLAN-r6.md:216`).
  - **(r3, M3-H X-H4) The in-core producer stages.** r2's wording, read literally, forbade two lawful M3 producers (H3:867). Exactly two exist at M3. Each is an execution-plan stage whose stage spec names its producer, and H admits its records like any other:
    - **E1's in-host syntax stage.** Its producer is the core provider closure, on syntax-universe records only (ME item 14b; MC:422-432). "The crate never mints `fact2`": H's syntax join admits its candidates (ME:478; r4, NBO-1).
    - **The host inventory derivation that H3 item 18 designs.** It produces the file and package `SubjectInventoryV1` outcomes and the `file@enumerated` and `package@manifest-declared` facts, which are "Produced by host discovery and enumeration, not by a language provider" (NCM:949). In a syntax universe its producer is the core provider closure (MC:424-429). In a TypeScript or Rust universe it has no lawful producer until M3-C r8 and CRC-2 answer H's X-H3 (MC:432, MC:453; H3 routes it there). Until then that leg stays gated, as H holds it.

    Neither is a provider fallback (item 2) or a reuse route. **Host projections of an admitted provider frame are not host-minted:** `TargetAttributionV2` (NE §9.6) and FA-2's census inventories (item 22) are produced by the frame they project.
- **Basis:** AQP:390; **(r3)** H3:867 (X-H4); ME item 14b; MC item 9; NCM:949.
- **Rejected:** carrying forward a standing such as "already admitted" from an earlier Run. **(r3)** Also rejected: an open-ended "host-produced records are lawful". It would admit host fabrication. The two stages are named, and each has a Plan-selected producer.
- **Forbidden substitutes:**
  - host-minted facts with neither a producing frame nor a Plan-selected in-core producer stage **(r3)**;
  - an in-core stage producing a TypeScript or Rust record under the core provider closure before X-H3 is answered (MC:432);
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
  - **For the INC-1 successor.** Its key must cover every one of these classes. A class the key omits is a hidden input. MC keeps each class separately identified, so such a key can cover them (MC item 20).
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

**9. INC-7: the spike first, and what its numbers decide (law; gate item L-G1).**
- **Decision.** This law fixes the protocol (items 1-2) only when it takes effect. That needs S-M's measured report (L-G1), entered through a delta round ("Review and effect"). An ACCEPT in review before S-M fixes nothing. S-M is the M3-S unit's lead run set:
  - it is a throwaway harness outside the product;
  - it runs over public, pinned T2 bytes;
  - it executes no repository code;
  - its samples are labelled preliminary;
  - it makes no production or confinement claim (`M3-PLAN-r6.md:205`).

  Its report must contain at least the figures below. Each is used here only by placeholder. Unless S-M's report fixes it otherwise:
  - **Workloads (r2).** The dev-role medium entries of the figure's language in the accepted T2 manifest: T2M `counts.rust.medium.devIds` (7 entries) and `counts.tsjs.medium.devIds` (6 entries) (T2R:57-67). For the Rust rows, add the workspace `mr-rs-medium-serde-json` (T2R:198). T2b's counting rule counts a polyglot entry per language, at the class of its own lines (T2R:57-59), so `poly-medium-napi-rs` is in both lists. Held-out entries are excluded, so that held-out standing is never put at risk (T2R:76; Q0:256, QD-23).
  - **Statistic.** 3 warmups, then 7 runs; the median, with the maximum also reported (AQ:268-276; AQP:349).
  - **Host.** The lead's macOS host, labelled `preliminary`; not D12 (`M3-PLAN-r6.md:205`).

| ID | Figure | Unit | Value |
|---|---|---|---|
| SM-1 | TS start: a fresh Node process, from the pinned closure path, loads the pinned TypeScript compiler and is ready to read a request | ms | `⟨SM-1⟩` |
| SM-2 | TS analysis: a fresh-process `Program` creation plus a full semantic pass over the repository | ms | `⟨SM-2⟩` |
| SM-3 | Rust start: the `rustc_driver` sidecar is ready for its callbacks (needs S-P to succeed; otherwise `incomplete` with S-P's reason) | ms | `⟨SM-3⟩` |
| SM-4 | Rust analysis: through type checking. No build script or proc-macro runs, so the expansion that depends on them is disclosed as unavailable | ms | `⟨SM-4⟩` |
| SM-5 | Sealing: enumerate the read set, read and SHA-256 every member, and compute the `snapshot2`/`plan2`-equivalent digests. **(r2, MC X-1)** Also report the inventory rows, the total bytes and the canonical descriptor's bytes, against `snapshot2`'s bounds: 100,000 rows, a 4 MiB descriptor (about 27,000 rows) and 8 GiB in total (MC item 5) | ms; rows; bytes; descriptor bytes | `⟨SM-5⟩` |
| SM-6 | TS read-set size, including `node_modules` as T2 pins it (NE:2948-2949). Compare with TS2's `maxSnapshotEntries` 200,000 and `maxSnapshotChunkBytes` 1,048,576 (NE:2963). **(r2, MC X-1)** Also compare with `snapshot2`'s binding bounds of 100,000 rows and a 4 MiB descriptor (MC item 5), and report the descriptor's bytes. If T2 pins no dependency tree, report the repository-only set, labelled. | entries; bytes; descriptor bytes | `⟨SM-6⟩` |
| SM-7 | Transfer: stream the sealed set, plus the Rust dependency-source set, through a pipe in ≤ 1 MiB chunks with framing, once per child | ms per child | `⟨SM-7⟩` |
| SM-8 | The longest single synchronous compiler call inside SM-2 (the event-loop block) | ms | `⟨SM-8⟩` |
| SM-9 | Complete replay, IE:1580-1592, over a fact and finding graph of the size SM-2 and SM-4 imply. Synthetic and labelled. | ms | `⟨SM-9⟩` |
| SM-10 | Per-process `wait4` `ru_maxrss`, information only (AQP:343). **(r2)** In the platform's native unit, labelled as S-OP-2's `rss_unit` labels it (`bytes` on macOS, `kib` on Linux), with the checked conversion to bytes beside it (SOP2:881, SOP2:910; Q0:889) | native unit, labelled; bytes | `⟨SM-10⟩` |
| SM-11 | **(r5; RUST3-LIM)** Rust analysis cost per subject: SM-4's time, SM-10's peak RSS and the worker's peak scratch bytes, each divided by the measured subject count | ms/subject; bytes/subject | `⟨SM-11⟩` |
| SM-12 | **(r5; RUST3-LIM)** Rebuilding the Rust subject scope: time and peak memory to derive the array, `commitments.subjectScope` and `domainCommitment` from the accepted manifest, on the host (both independent derivations) and on the worker | ms; bytes | `⟨SM-12⟩` |
| SM-13 | **(r5; RUST3-LIM)** Response volume per subject, per Rust stage: (a) fact candidates, (b) spool bytes under RPP `candidateSpoolAccounting`, (c) response payload bytes, (d) response frames, (e) FA-2 census rows and census CBOR bytes | count/subject; bytes/subject | `⟨SM-13⟩` |
| SM-14 | **(r5; RUST3-LIM)** Work-unit tuples per run: Σ over the workload's Rust stages of subjects × requested keys | work-units | `⟨SM-14⟩` |

  **SM-11 to SM-14 (r5; RUST3-LIM, X-RL-L3).**
  - **Workloads.** The Rust medium workloads above, with axum (301 non-empty `.rs` files) and tokio (808) now servable under `subject-scope-reference-v1`. Also the large dev Rust entries smithy-rs (1,084), rspack (1,384) and deno (1,052), and sui (3,318) if S-P permits. Held-out entries (tauri, ripgrep, rust-analyzer) are excluded, as above. The counts are RUST3-LIM's (`rust3-lim/evidence/rust-subject-counts.json`).
  - **What they set.** None of them is a protocol constant. The S-M delta round records:
    - the M3 Rust provider's effective subject ceiling, `S_eff = min(snapshot2's admitted rows, ⌊1,000,000 / ⟨SM-13a⟩⌋, ⌊2^30 / ⟨SM-13b⟩⌋, ⌊2^30 / ⟨SM-13c⟩⌋, ⌊1,000,000 / ⟨SM-13d⟩⌋, ⌊2^31 / ⟨SM-11 scratch⟩⌋)`;
    - the Rust stage budget that G's budget profile and C's Plan carry, at or below `⟨SM-14⟩`-derived values, so that a large repository ends in `BudgetExhausted` or the scope-limit route, never in a response safety-bound fault (RUST3-LIM F-4; X-RL-C2, X-RL-G2);
    - whether rebuilding the scope (SM-12) costs anything material, which would be a finding for G and D, not a reason for a cap;
    - where FA-2's census `over-bound` route starts to bind (SM-13e).
  - **No outcome (A) to (C) depends on them.** They feed the D, C and G units' constants. RUST3-LIM is in this law's gate (L-G11), but SM-11 to SM-14 are measured, not decided, here.

  **Derived figures:**
  - the one-shot fixed floor **F** = start (SM-1 or SM-3) + SM-5 + SM-7 + SM-9;
  - the per-run total **T** = F + analysis (SM-2 or SM-4).

  **What the S-M delta round records.** It records F and T per workload and, against the owner-approved targets, **every** outcome that holds, not just one **(r3, NBO-2)**. Those targets are held on the D12 runner (AQP:372), so the comparison here is preliminary:
  - **(A)** F ≤ 2 s, the single-file edit target (AQP:385), and T within the medium budgets (AQP:377): T under Q0 §9.2's cold reset ≤ 30 s, and T under its warm reset ≤ 8 s. Cold and warm are separate fixtures (AQ:279-280), so S-M reports T under each reset it can apply. One-shot stands for M3. M4 decides whether changed-scope can meet the edit target by reducing analysis work.
  - **(B)** F > 2 s. No host-side reuse under one-shot TS2/Rust3 can meet the edit target, because F remains. This law still fixes TS2/Rust3 for M3, since residency is staged to M5. The record names residency (item 8) or a protocol successor as M4's only route to the target, and raises owner question O3.
  - **(C)** T > a medium budget. One-shot full analysis misses an owner budget. This is the trigger AQP:372 names ("to be revisited after the first exploratory measurement"), so it raises owner question O4 before L takes effect.
  - **(B) and (C) together (r3, NBO-2).** When F > 2 s and T misses a medium budget, the round records both outcomes and raises both O3 and O4. Neither masks the other. Items 1 and 2 stay one-shot under both. (A) is recorded only when neither (B) nor (C) holds.

  **Other uses of these figures (r2).** The D law's draft also takes two of them for its own constants (its constants table): SM-1 or SM-3 for the handshake deadline, and SM-8 for the liveness floor. Those constants are the D law's, not this law's.
- **Basis:**
  - AQP:408: "Before the protocol is fixed, measure startup, sealing and replay costs for one-shot analysis on medium T2 workloads. Residency must earn its cost against that measurement";
  - `M3-PLAN-r6.md:638`: "The one-shot design may miss the §5.2 budgets (AQP:376-378). S-M exists to find that out before L."
- **Rejected:**
  - **Taking effect with invented or estimated figures.** An early ACCEPT in review is lawful because it fixes nothing until the delta round records measured values.
  - **Making effect conditional on outcome (A).** The gate is "S-M measured" (`M3-PLAN-r6.md:207`), not "S-M passes". The owner decides budget and staging questions, not this law.
- **Forbidden substitutes:**
  - a number in this law not taken from S-M's report;
  - an S-M figure from a held-out repository;
  - a macOS figure presented as a D12 or Q6 sample;
  - **(r2)** a native `ru_maxrss` value labelled as bytes on a platform whose native unit is not bytes (SOP2:1006).

**10. INC-8: reuse disclosure lives in the operational record, outside semantic Coverage (law).**
- **Decision.** The host's operational record (OPP:249) discloses which results were recomputed and which were reused producer work, **per stage and universe (r2)**. That covers every provider child's stages and the in-host syntax stages, which have no child (item 2; ME §G). The record is:
  - host-owned, typed and nonsemantic;
  - keyed by RequestId and, once the attempt's ExecutionId is reserved, ExecutionId (item 13);
  - outside Run identity, Coverage, PlanId and every digest.

  At M3 every record states that all work was recomputed and none reused, and names the cause: `no-reuse-path` (item 3). **(r2)** The carrier is S-OP-2's `host.reuse.disclosed`, with fields `stage`, `universe`, `state` (`recomputed`) and `cause` (`no-reuse-path`) (SOP2:873). Its header carries the ExecutionId, which exists before the Plan (J1 item 2: R12 precedes J-ε). ME agrees that no parse result crosses invocations (ME §G).

  **(r3)** A provider's symbol census (item 22) is recomputed in every Run, with its universe's Analyze. The per-stage-and-universe record already covers it. No census-specific event, field or cause is added.

  `CoverageResultV3` is unchanged. It has no reuse member (NE:2016-2030), and canonical Coverage describes only the current Plan's examined, resolved and sufficient state (AQP:409). Fully re-admitted reused work may support a complete result. Any obligation not re-established for the current Plan stays a typed incomplete deficiency (AQP:409).
  - **Carriers.** At M3 the record reaches the harness as instrumentation (OPP:250). A public disclosure at M4 needs S-OP-6 (OPP:250, OPP:412). `host.reuse.disclosed` is not an export candidate (SOP2:873).
- **Basis:** AQP:409; OPP:249-250; Q0:946, Q0:953; ENV:660-666, where `carriesReuseDisclosure` is a required member; SOP2:873.
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
  - OPP:232-238; `M3-PLAN-r6.md:463`; OPP:394;
  - **(r2)** accepted S-OP-2 is written within it: component diagnostics under O1(a) reach records only as host-constructed codes and reductions (SOP2 item 19).
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
  1. **stderr: counted, never held (lead decision, r2).** The host reads each provider's stderr continuously to EOF, so that a child never blocks on a full pipe. It counts the bytes, saturating, and records whether the count passed the protocol bound. **It retains no text.** At settlement the count is reduced to `{bytes, truncated}`, S-OP-2's K7 through `Reduced::from_capture` (SOP2:837), and logged as `provider.stderr.reduced` (SOP2:882). There is no digest: a digest of free text is P3 (OPP:171). The bounds are TS2 `maxStderrBytes` 262,144 (NE:2967) and Rust3's retained v2 `maxStderrBytes` 262,144 (RPP:117, retained by NE:2934). stderr is never parsed, logged, exported, admitted or used as a fact, and it never changes a result (DLV:1133).
     - **Why counting is enough.** DLV:1133 has the host capture stderr "up to 256 KiB, then truncated with a host-owned marker". At M3 those bytes have no lawful reader. No S-OP-2 kind accepts P3, and a consented raw capture is O9, "not at M3" (OPP:401; `M3-PLAN-r6.md:541`). Counting serves the capture's only use, K7, and the marker becomes `truncated: true`. GROK2 confirmed this reading as lawful in its D r1 review (`reviews/grok2-supervisor-d-r1/review.json`, NBO-1), and the D law's stderr item adopts it.
     - **Rejected:** r1's "holds it in memory" and reduction at settlement, which follows OPP:171's wording. The lawful output is the same, and holding keeps P3 in host memory, and in any host core image, for no use. Under r1 the D law's draft had to depart from this item; under r2 it follows it.
  2. **Fault detail.**
     - The control `fault` detail (CC:36; ≤ 1,024 bytes, CC:56-58) is reduced to its length. S-OP-2 reduces control `refusal` detail (CC:32) the same way (SOP2:838-839).
     - Rust `ProviderFaultV2.faultKind` is a closed enum (RPP:441-445), so it is loggable as P0 (SOP2:843).
     - **(r2)** Its `detailCode` is "diagnostic only, never D9 authority" (RPP:445). S-OP-2 r6 registers it as K3 `RustDetailCode` with an **empty table**, so every value is `{unrecognized}`: its length and truncation, never its text (SOP2:844). That is this item's reduction. S-OP-2 rejected a closed set now, because it would give an open protocol member a meaning that item 1 forbids (SOP2:851). A member the G unit later adds by ordinary registration (SOP2:226-230) is a diagnostic label only. It never becomes D9 authority, a result, progress or a protocol meaning.

     All of these are logged as `provider.fault.reduced` (SOP2:883).
  3. **Progress.** Progress is derived only by the host, from transitions its own state machine admitted. It counts:
     - frames that passed protocol validation: snapshot chunks acknowledged, and `FactBatch` and `Coverage`/`CoverageV3` frames per universe and stage;
     - stage changes.

     The phrase "admitted stage/counter observations" (DRC:574) is read as these host-counted transitions. Frame acceptance is not fact admission: facts are admitted only after Complete, matching commitments, zero-exit and EOF (DLV:1517). So progress never implies admitted facts. **(r2)** S-OP-2 carries the counts as `fact_frames` and `coverage_frames` on `provider.stage.terminal` (SOP2:880), and their absence as `supervision.progress.absent` (SOP2:886).
  4. **Liveness.**
     - **The signal.** Nonce-matched `health`/`healthReport` (CC:33-34, CC:50-54) and `resourceReport` (CC:35), within the STEADY window (CC:132). A missed health response within the supervisor's window is a liveness fault (OPP:237), logged as `supervision.liveness.missed` (SOP2:885). Nonces are never recorded (SOP2:840).
     - **The window.** It is the D law's constant, provisionally 5 s (OPP:237). **(r2)** The D law's draft raises it to at least 2 × SM-8 unless F and G show the responder is independent of compiler work (its constants table). This law requires only that it be above SM-8, unless the providers show that the responder is independent of compiler work.
     - **What the provider owes.** The component's health responder must not be starved by compiler work. A long synchronous compiler call must not turn a legitimate long phase (OPP:238) into a liveness fault. How it achieves that is F's and G's design, for example a responder outside the compiler's thread.
     - **What S-M owes.** SM-8 measures the exposure.
  5. **The SDK alias rebinding.** DRC:556-566 binds the SDK's `HostRequest`, `ProviderResponse`, `FactBatch`, `Coverage` and `ProviderComplete` aliases to DLV's **V1** payloads. Under TS2 they bind to the successor payloads of NE §9.4 and §9.7 and `provider-startup.schemas.v1.json`. That is a re-binding of existing operations, not a new operation.
     - **Rust3 has no SDK.** DRC:515 selects "a TypeScript provider SDK plus Rust host bindings", so the Rust sidecar implements its component side of common control itself (G1a).
     - **Open.** Whether the DR-125 owners treat this re-binding as a record join or as an SDK successor is open question R2. S-OP-2 adds no SDK operation either (SOP2:806).
- **Basis:** OPP:240 ("Under (a), S-OP-4 is still needed as a record join stating the stderr and fault-detail disposition and the progress derivation"); `M3-PLAN-r6.md:207`; SOP2 item 22 (SOP2:831-851).
- **Rejected:**
  - **A separate S-OP-4 record unit.** The M3-L row places the join in this law (`M3-PLAN-r6.md:207`).
  - **Keeping a stderr digest** for correlation. That is P3 (OPP:171).
  - **(r2)** Holding stderr bytes until settlement (12.1).
- **Forbidden substitutes:**
  - stderr text or `fault` detail in any log, crash ring, bundle or export;
  - **(r2)** stderr bytes kept in any buffer beyond the read that counts them;
  - a progress number a provider supplied;
  - a health window shorter than a measured legitimate synchronous block.

**13. RequestId correlation and phase-lawful identities at the provider boundary (law).**
- **Decision.**
  - **The correlator.** `RequestId` (`req1_` plus 32 hex; WS:78-79; IE:61-63) is the universal correlator of every provider-attributed record (OPP:148). J1 mints one per invocation at ingress (J1 item 2).
  - **It never reaches a provider.** It is not a wire member (neither TS2 nor Rust3 has one, and adding one breaches item 1), not an argv element and not an environment variable. The predecessor's `OPENSIP_RUN_ID` child-environment tag (OPP:121) is not inherited.
  - **What is on the wire (r4, RF-1; lead decision: derived, not hand-written).** r2 said "only" four identities; r3 named more by hand and still mis-stated later payloads (`reviews/grok-provider-protocol-l-r3` RF-1). r4 does not write the list. It is generated from the cited schemas, and control L-C1 re-derives it.
    - **The correlation identities** stay as before: `executionId`, `snapshotId` (`snapshot2` text), `planId` (`plan2` text) and the universe coordinate, the native semantic-universe identity (NE:3158-3164). They are what records correlate on (below). `executionId` and `planIntentCommitment` keep their owners (NE:3159).
    - **The method.** `evidence/wire_identities.py` reads every payload each protocol puts on the wire:
      - **Which payload each frame carries.** NE §9 and §0's supersessions select it; the script's frame map cites the selecting line for each. The sources are the native handshake and startup schemas, `delivery.v2` and `rust-provider-protocol.v2` for the inherited payloads, NE §9.2's table for the dependency-source frames, `fact-batch.schema.v3.json` and the occupancy companion under `target-attribution-v2`, and FA-2's census schema under `symbol-census-v1`.
      - **The walk.** It reads each payload's own members, including optional ones, and descends into every nested record the payload names. Where an inherited record is typed only by its id, a cited map supplies the record: fact candidates and anchors are the fact-plane records `delivery.v2` implements field for field, and Rust stage requests reach C-2's stage and coverage key.
      - **The rules.** It classifies every member by a closed rule set (R7 added in r5). A member is identity-bearing iff:
        - **R1:** its name ends in `Id`, `Ids`, `Key`, `Commitment`, `Sha256`, `Digest`, `Hash`, `MerkleRoot`, `Closure` or `Universe`; or
        - **R2:** a contract's machine-readable identity list names it, on the payload that list governs (the handshake schema's `typescriptDescriptorBinding` and `rustIdentityBinding`); or
        - **R3:** it is the universe descriptor, whose hash is the universe coordinate (NE:3161-3163), or a row copied from that descriptor. R3 members are listed whole and not descended into; or
        - **R4:** its published description names an identity type, or an identity member, as its value or part of it; or
        - **R5:** its description fixes the same constant as an R1 member of the same artifact; or
        - **R6:** it is a JSON Schema string whose pattern requires a digest or a typed identity prefix; or
        - **R7 (r5, RF-1; lead decision):** it is a **required** member of a record that a cited contract defines as an identity key, or as a key's field-for-field copy, or a member a cited contract requires to equal a key's member. R7 applies only where R1 to R6 do not, so their labels are unchanged. The records are closed in the script (`KEY_RECORDS`, `KEY_COPY`), each with its sentence:
          - DLV `CoverageKeyV1`, the requested key: "Field-for-field exact implementation of c2-plan-stage-schema.v3.json#coverageKey.key" (DLV:804-817; "full requested key", DLV:726);
          - C-2 `coverageKey.key` itself (`c2-plan-stage-schema.v3.json`), which RPP's `CoverageKeyV2` takes as its external (RPP:544-548);
          - the returned key `CoverageKeyV2`: `entries[i]` answers `requestedCoverageDomain.keys[i]`, and its relation, resolution and both universes must equal the host's `D` (NE:3277-3282; NE:1927-1932);
          - `ViewEntryV3`'s `relation` and `resolution`, which must equal the key's (`native.coverage-entry-key-mismatch`, NE:3529; NEM:1566-1567).
      - **(r5) Every other composite key the walk passes, checked.** Each is listed with why it is, or is not, an R7 record:
        - **Request keys:** the TS2 `RequestedCoverageDomainV1.keys[]` and the Rust `analysisDomain.requestedCoverageDomain[]` are the C-2 key, so they are R7.
        - **Returned keys and entries:** `CoverageResultV3.key` (R7) and `.entry`'s `relation` and `resolution` (R7 copies) in every Coverage wrapper and terminal coverage array.
        - **The fact identity:** FACT-ID-V1 is a host-only identity over the admitted record ("owner": "Rust host only", fact-plane `factIdContract`; DLV:802 `hostJoin`: the candidate "is never an admitted fact"). The wire candidate is a claim, not a key. Its identity-bearing members are those R1 to R6 admit.
        - **Commitment preimages:** `domainCommitment`'s `{subjectScope, keys}`, the stage, stream and batch commitments over candidates and entries, and `manifestSha256` over manifest entries. A commitment binds content, and its preimage's members are content, not identities, unless a contract names the record a key: the keys inside `requestedCoverageDomain` are R7.
        - **View and occupancy keys:** a view is host-minted and never on the wire. `OccupancyCompanionV1` is "associated by candidateOrdinal in that batch" (its schema), and the projected `TargetAttributionV2` is a host record. Only the entry's key-field copies are R7.
        - **Correlation tuples:** a FactBatch's `stageId`, `analysisOrdinal` and `batchIndex` are compared with the host's `DispatchBindingV1` (NE:3039-3041), a host record not on the wire. `stageOrdinal`, `candidateOrdinal` and entry positions order frames within one exchange. They name nothing outside it, so they are listed as non-identity members (`stageId` is R1).
        - **Scope summaries:** TS2 `SubjectScopeV1`, RUST3-LIM's `RustSubjectScopeV1` and `ExaminedUniverseV1` are not keys. Their commitments are R1. `scopeKind` and `subjectCount` are a label and a count, checked against the host's reconstruction.
      - **What is not enumerated.** Opaque bytes (chunks, `canonicalRelationPayload`) carry no member-level identity. A relation payload's own subject ids are the relation registry's (RPS), are provider-attested, and are not host identities.
    - **(r5) The counts.** r4 derived 51 payload rows and 235 identity-bearing member paths. r5 derives 52 and 278: TS2 21 and 121, Rust3 31 and 157. By rule: R1 200, R2 23, R3 4, R4 15, R5 3, R7 33. The 43 added paths, with none removed, are:
      - **30 R7 paths on existing rows, 15 per language:** `relation`, `resolution` and `schemaVersion` on each Analyze request key, and `relation` and `resolution` on each returned key and each entry, in the Coverage, post-Analyze `Unavailable` and `BudgetExhausted` rows;
      - **the new RUST3-LIM row's 13 paths**, of which 3 are R7.
    - **(r5) Rust's per-file `subjectId`, pending RUST3-LIM's acceptance.** GROK2 has since given it, so the condition now waits on RUST3-LIM's binding after FA-2. `stages[].analysisDomain.subjects[].subjectId` is on the wire only when `subject-scope-reference-v1` is absent (the AnalyzeV2 row's condition). Under the token, each stage is a `StageRequestV3` and carries `analysisDomain.subjectScope.subjectScopeCommitment` instead: a commitment (R1), and no per-file identity (the RUST3-LIM row). That row is on the wire only once RUST3-LIM is bound, after FA-2 (L-G11; RL LD-R8), and its token is negotiated, as FA-2's rows depend on FA-2.
    - **The inventory, exactly.** The table below is the script's output, inserted verbatim. Each row gives the frame, the payload with the source line that defines it, when that payload is on the wire, every identity-bearing member with the rule that admits it, and the top-level members that carry no identity at any depth.

<!-- wire-identities:begin (generated by evidence/wire_identities.py; do not edit) -->

**TS2 (`typescript-semantic` major 2)**

| Frame | Payload (source line) | When | Identity-bearing members (rule) | Top-level members with no identity at any depth |
|---|---|---|---|---|
| Hello (h→w) | `TypeScriptHelloV2` (HS:424) | always | `hostBuildId` (R1); `expectedProviderDescriptorSha256` (R1); `expectedRuntimeDescriptorSha256` (R1) | `limits`, `expectedCapabilities`, `identityVersions` |
| HelloAck (w→h) | `TypeScriptHelloAckV2` (HS:463) | always | `protocolMajor` (R2); `providerBuildId` (R2); `providerDescriptorSha256` (R1); `runtimeDescriptorSha256` (R1); `nodeVersion` (R2); `v8Version` (R2); `modulesAbi` (R2); `typescriptVersion` (R2); `typescriptCompilerSha256` (R2); `typescriptStdlibMerkleRoot` (R2); `defaultWorkBudgetProfileId` (R2); `defaultWorkBudgetProfileSha256` (R2); `platformId` (R2) | `capabilities`, `identityVersions` |
| OpenUniverse (h→w) | `TypeScriptOpenUniverseV2` (ST:332) | always | `executionId` (R1); `snapshotId` (R1); `planId` (R1); `planIntentCommitment` (R1); `providerId` (R1); `universe` (R3); `universeKey` (R1) | — |
| UniverseAccepted (w→h) | `TypeScriptUniverseAcceptedV2` (ST:369) | always | `executionId` (R1); `snapshotId` (R1); `planId` (R1); `universeKey` (R1) | — |
| SnapshotManifest (h→w) | `SnapshotManifestV1` (DLV:850) | always | `snapshotId` (R1); `manifestSha256` (R1); `entries[].contentSha256` (R1) | — |
| SnapshotFileChunk (h→w) | `SnapshotFileChunkV1` (DLV:851) | always | `snapshotId` (R1) | `path`, `chunkIndex`, `byteOffset`, `bytes` |
| SnapshotSeal (h→w) | `SnapshotSealV1` (DLV:852) | always | `snapshotId` (R1); `manifestSha256` (R1) | `entryCount`, `totalFileBytes`, `totalChunkCount` |
| SnapshotAccepted (w→h) | `SnapshotAcceptedV1` (DLV:853) | always | `snapshotId` (R1); `manifestSha256` (R1) | `entryCount`, `totalFileBytes`, `totalChunkCount` |
| NativeContextVerified (w→h) | `NativeContextVerifiedV1` (ST:464) | always | `nativeContextId` (R1); `recomputedNativeContextId` (R1) | `equal` |
| Unavailable (pre-Analyze) (w→h) | `PreAnalyzeUnavailableV1` (ST:485) | always | `executionId` (R1); `snapshotId` (R1); `planId` (R1); `nativeContextId` (R1); `recomputedNativeContextId` (R1) | `reason` |
| Analyze (h→w) | `AnalyzeV1` (DLV:854) | always | `executionId` (R1); `snapshotId` (R1); `planId` (R1); `universeKey` (R1); `stageRequests[].stageId` (R1); `stageRequests[].providerId` (R1); `stageRequests[].dependsOn` (R4); `stageRequests[].requestedCoverageDomain.subjectScope.snapshotId` (R1); `stageRequests[].requestedCoverageDomain.subjectScope.subjectScopeCommitment` (R1); `stageRequests[].requestedCoverageDomain.keys[].relation` (R7); `stageRequests[].requestedCoverageDomain.keys[].resolution` (R7); `stageRequests[].requestedCoverageDomain.keys[].sourceUniverseId` (R1); `stageRequests[].requestedCoverageDomain.keys[].targetUniverseId` (R1); `stageRequests[].requestedCoverageDomain.keys[].subjectScopeCommitment` (R1); `stageRequests[].requestedCoverageDomain.keys[].producer` (R5); `stageRequests[].requestedCoverageDomain.keys[].producerVersion` (R4); `stageRequests[].requestedCoverageDomain.keys[].schemaVersion` (R7); `stageRequests[].requestedCoverageDomain.domainCommitment` (R1) | `analysisOrdinal` |
| Analyze (h→w) | `TypeScriptAnalyzeV2` (FA2:211) | under symbol-census-v1 (FA-2, proposed) | `symbolCensus.enumeratorClosure` (R1) | — |
| FactBatch (w→h) | `FactBatchV1` (DLV:855) | always | `stageId` (R1); `facts[].producer` (R4); `facts[].producerVersion` (R4); `facts[].sourceUniverseId` (R1); `facts[].targetUniverseId` (R1); `facts[].relationSchemaId` (R1); `facts[].anchors[].snapshotId` (R1); `facts[].anchors[].contentSha256` (R1); `facts[].anchors[].factId` (R1); `batchCommitment` (R1) | `analysisOrdinal`, `batchIndex` |
| FactBatch (w→h) | `FactBatchV3` (FB3:1) | under target-attribution-v2 | `stageId` (R1); `candidates[].producer` (R4); `candidates[].producerVersion` (R4); `candidates[].sourceUniverseId` (R1); `candidates[].targetUniverseId` (R1); `candidates[].relationSchemaId` (R1); `candidates[].anchors[].snapshotId` (R1); `candidates[].anchors[].contentSha256` (R1); `candidates[].anchors[].factId` (R1); `occupancyCompanions[].targetUniverseId` (R1); `occupancyCompanions[].targetNativeId` (R1); `occupancyCompanions[].evaluationNativeId` (R1) | `schemaVersion`, `analysisOrdinal`, `batchIndex` |
| Coverage (w→h) | `TypeScriptCoverageV2` (ST:518) | always | `stageId` (R1); `entries[].key.relation` (R7); `entries[].key.resolution` (R7); `entries[].key.sourceUniverse` (R1); `entries[].key.targetUniverse` (R1); `entries[].key.subjectScopeCommitment` (R1); `entries[].entry.relation` (R7); `entries[].entry.resolution` (R7); `entries[].entry.examinedUniverse.subjectScopeCommitment` (R1); `coverageCommitment` (R1) | `analysisOrdinal` |
| Unavailable (post-Analyze) (w→h) | `TypeScriptUnavailableV2` (ST:582) | always | `affectedStageIds` (R1); `coverage[].key.relation` (R7); `coverage[].key.resolution` (R7); `coverage[].key.sourceUniverse` (R1); `coverage[].key.targetUniverse` (R1); `coverage[].key.subjectScopeCommitment` (R1); `coverage[].entry.relation` (R7); `coverage[].entry.resolution` (R7); `coverage[].entry.examinedUniverse.subjectScopeCommitment` (R1); `coverageCommitment` (R1) | `analysisOrdinal`, `reason` |
| BudgetExhausted (w→h) | `TypeScriptBudgetExhaustedV2` (ST:683) | always | `triggerStageId` (R1); `coverage[].key.relation` (R7); `coverage[].key.resolution` (R7); `coverage[].key.sourceUniverse` (R1); `coverage[].key.targetUniverse` (R1); `coverage[].key.subjectScopeCommitment` (R1); `coverage[].entry.relation` (R7); `coverage[].entry.resolution` (R7); `coverage[].entry.examinedUniverse.subjectScopeCommitment` (R1); `coverageCommitment` (R1) | `analysisOrdinal`, `dimension`, `limit`, `observed` |
| Complete (w→h) | `CompleteV1` (DLV:859) | always | `stageResults[].stageId` (R1); `stageResults[].factCommitment` (R1); `stageResults[].coverageCommitment` (R1); `factStreamCommitment` (R1); `coverageStreamCommitment` (R1) | `analysisOrdinal` |
| Complete (w→h) | `TypeScriptCompleteV2` (FA2:377) | under symbol-census-v1 (FA-2, proposed) | `symbolCensus.rows[].nativeSubjectId` (R1) | — |
| Cancel (h→w) | `CancelV1` (DLV:860) | always | `executionId` (R1) | `analysisOrdinal`, `reason` |
| Cancelled (w→h) | `CancelledV1` (DLV:861) | always | `executionId` (R1) | `analysisOrdinal`, `observedPhase` |

**Rust3 (`rust-semantic` major 3)**

| Frame | Payload (source line) | When | Identity-bearing members (rule) | Top-level members with no identity at any depth |
|---|---|---|---|---|
| Hello (h→w) | `HelloV3` (HS:586) | always | `hostBuildId` (R1); `expectedProtocolContractSha256` (R1); `expectedIdentity.protocolMajor` (R2); `expectedIdentity.providerBuildId` (R2); `expectedIdentity.rustCommitHash` (R2); `expectedIdentity.hostTriple` (R2); `expectedIdentity.targetTriple` (R2); `expectedIdentity.sysrootDigest` (R2) | `protocolMajor`, `expectedCapabilities`, `identityVersions`, `limits` |
| HelloAck (w→h) | `HelloAckV3` (HS:630) | always | `protocolMajor` (R2); `providerBuildId` (R2); `rustCommitHash` (R2); `hostTriple` (R2); `targetTriple` (R2); `sysrootDigest` (R2) | `capabilities`, `identityVersions` |
| OpenUniverse (h→w) | `OpenUniverseV3` (ST:394) | always | `executionId` (R1); `snapshotId` (R1); `planId` (R1); `planIntentCommitment` (R1); `providerId` (R1); `universe` (R3); `repositoryResolution.dependencySourceSetId` (R1); `repositoryResolution.preparedOutputSetId` (R1); `repositoryResolution.authorizationId` (R1) | — |
| UniverseAccepted (w→h) | `UniverseAcceptedV3` (ST:431) | always | `executionId` (R1); `snapshotId` (R1); `planId` (R1); `providerId` (R1); `universe` (R3); `repositoryResolution.dependencySourceSetId` (R1); `repositoryResolution.preparedOutputSetId` (R1); `repositoryResolution.authorizationId` (R1) | — |
| SnapshotManifest (h→w) | `SnapshotManifestV2` (RPP:357) | always | `snapshotId` (R1); `manifestSha256` (R1); `entries[].contentSha256` (R1) | — |
| SnapshotFileChunk (h→w) | `SnapshotFileChunkV2` (RPP:363) | always | `snapshotId` (R1) | `path`, `chunkIndex`, `byteOffset`, `bytes` |
| SnapshotSeal (h→w) | `SnapshotSealV2` (RPP:369) | always | `snapshotId` (R1); `manifestSha256` (R1) | `entryCount`, `totalFileBytes`, `totalChunkCount` |
| SnapshotAccepted (w→h) | `SnapshotAcceptedV2` (RPP:375) | always | `snapshotId` (R1); `manifestSha256` (R1) | `entryCount`, `totalFileBytes`, `totalChunkCount` |
| DependencySourceManifest (h→w) | `DependencySourceManifest` (NE:2876) | always | `dependencySourceSetId` (R1); `manifestSha256` (R1); `entries[].packageKey` (R1); `entries[].contentSha256` (R1) | — |
| DependencySourceChunk (h→w) | `DependencySourceChunk` (NE:2877) | always | `dependencySourceSetId` (R1); `packageKey` (R1) | `path`, `chunkIndex`, `byteOffset`, `bytes` |
| DependencySourceSeal (h→w) | `DependencySourceSeal` (NE:2878) | always | `dependencySourceSetId` (R1); `manifestSha256` (R1) | `entryCount`, `totalBytes`, `totalChunkCount` |
| DependencySourceAccepted (w→h) | `DependencySourceAccepted` (NE:2879) | always | `dependencySourceSetId` (R1); `manifestSha256` (R1) | `entryCount`, `totalBytes`, `totalChunkCount` |
| PreparedOutputManifest (h→w) | `PreparedOutputManifestV2` (RPP:381) | always | `planId` (R1); `manifestSha256` (R1); `entries[].planRow` (R3); `entries[].logicalPath` (R4); `entries[].blobSha256` (R1); `entries[].contentSha256` (R1) | — |
| PreparedOutputChunk (h→w) | `PreparedOutputChunkV2` (RPP:387) | always | `planId` (R1) | `outputOrdinal`, `chunkIndex`, `byteOffset`, `bytes` |
| PreparedOutputSeal (h→w) | `PreparedOutputSealV2` (RPP:393) | always | `planId` (R1); `manifestSha256` (R1) | `entryCount`, `totalBlobBytes`, `totalChunkCount` |
| PreparedOutputAccepted (w→h) | `PreparedOutputAcceptedV2` (RPP:399) | always | `planId` (R1); `manifestSha256` (R1) | `entryCount`, `totalBlobBytes`, `totalChunkCount` |
| NativeContextVerified (w→h) | `NativeContextVerifiedV1` (ST:464) | always | `nativeContextId` (R1); `recomputedNativeContextId` (R1) | `equal` |
| Unavailable (pre-Analyze) (w→h) | `PreAnalyzeUnavailableV1` (ST:485) | always | `executionId` (R1); `snapshotId` (R1); `planId` (R1); `nativeContextId` (R1); `recomputedNativeContextId` (R1) | `reason` |
| Analyze (h→w) | `AnalyzeV2` (RPP:405) | always; once RUST3-LIM is bound (after FA-2), its `stages[]` members only without subject-scope-reference-v1 | `executionId` (R1); `snapshotId` (R1); `planId` (R1); `stages[].planStage.stageId` (R1); `stages[].planStage.dependsOn` (R4); `stages[].planStage.providerId` (R1); `stages[].analysisDomain.subjects[].subjectId` (R1); `stages[].analysisDomain.requestedCoverageDomain[].relation` (R7); `stages[].analysisDomain.requestedCoverageDomain[].resolution` (R7); `stages[].analysisDomain.requestedCoverageDomain[].sourceUniverseId` (R1); `stages[].analysisDomain.requestedCoverageDomain[].targetUniverseId` (R1); `stages[].analysisDomain.requestedCoverageDomain[].subjectScopeCommitment` (R1); `stages[].analysisDomain.requestedCoverageDomain[].producer` (R5); `stages[].analysisDomain.requestedCoverageDomain[].producerVersion` (R4); `stages[].analysisDomain.requestedCoverageDomain[].schemaVersion` (R7); `stages[].analysisDomain.domainCommitment` (R1) | `analysisOrdinal` |
| Analyze (h→w) | `StageRequestV3 (each stages[] member of AnalyzeV2 or AnalyzeV3)` (RL:93) | under subject-scope-reference-v1 (RUST3-LIM, accepted; binds after FA-2) | `stages[].planStage.stageId` (R1); `stages[].planStage.dependsOn` (R4); `stages[].planStage.providerId` (R1); `stages[].analysisDomain.subjectScope.subjectScopeCommitment` (R1); `stages[].analysisDomain.requestedCoverageDomain[].relation` (R7); `stages[].analysisDomain.requestedCoverageDomain[].resolution` (R7); `stages[].analysisDomain.requestedCoverageDomain[].sourceUniverseId` (R1); `stages[].analysisDomain.requestedCoverageDomain[].targetUniverseId` (R1); `stages[].analysisDomain.requestedCoverageDomain[].subjectScopeCommitment` (R1); `stages[].analysisDomain.requestedCoverageDomain[].producer` (R5); `stages[].analysisDomain.requestedCoverageDomain[].producerVersion` (R4); `stages[].analysisDomain.requestedCoverageDomain[].schemaVersion` (R7); `stages[].analysisDomain.domainCommitment` (R1) | — |
| Analyze (h→w) | `AnalyzeV3` (FA2:263) | under symbol-census-v1 (FA-2, proposed) | `symbolCensus.enumeratorClosure` (R1) | — |
| FactBatch (w→h) | `FactBatchV2` (RPP:411) | always | `stageId` (R1); `candidates[].producer` (R4); `candidates[].producerVersion` (R4); `candidates[].sourceUniverseId` (R1); `candidates[].targetUniverseId` (R1); `candidates[].relationSchemaId` (R1); `candidates[].anchors[].snapshotId` (R1); `candidates[].anchors[].contentSha256` (R1); `candidates[].anchors[].factId` (R1) | `analysisOrdinal`, `batchIndex` |
| FactBatch (w→h) | `FactBatchV3` (FB3:1) | under target-attribution-v2 | `stageId` (R1); `candidates[].producer` (R4); `candidates[].producerVersion` (R4); `candidates[].sourceUniverseId` (R1); `candidates[].targetUniverseId` (R1); `candidates[].relationSchemaId` (R1); `candidates[].anchors[].snapshotId` (R1); `candidates[].anchors[].contentSha256` (R1); `candidates[].anchors[].factId` (R1); `occupancyCompanions[].targetUniverseId` (R1); `occupancyCompanions[].targetNativeId` (R1); `occupancyCompanions[].evaluationNativeId` (R1) | `schemaVersion`, `analysisOrdinal`, `batchIndex` |
| CoverageV3 (w→h) | `CoverageV3` (ST:550) | always | `stageId` (R1); `entries[].key.relation` (R7); `entries[].key.resolution` (R7); `entries[].key.sourceUniverse` (R1); `entries[].key.targetUniverse` (R1); `entries[].key.subjectScopeCommitment` (R1); `entries[].entry.relation` (R7); `entries[].entry.resolution` (R7); `entries[].entry.examinedUniverse.subjectScopeCommitment` (R1); `coverageCommitment` (R1) | `analysisOrdinal` |
| Unavailable (post-Analyze) (w→h) | `UnavailableV3` (ST:631) | always | `affectedStageIds` (R1); `coverage[].key.relation` (R7); `coverage[].key.resolution` (R7); `coverage[].key.sourceUniverse` (R1); `coverage[].key.targetUniverse` (R1); `coverage[].key.subjectScopeCommitment` (R1); `coverage[].entry.relation` (R7); `coverage[].entry.resolution` (R7); `coverage[].entry.examinedUniverse.subjectScopeCommitment` (R1); `coverageCommitment` (R1) | `analysisOrdinal`, `reason` |
| BudgetExhausted (w→h) | `BudgetExhaustedV3` (ST:734) | always | `triggerStageId` (R1); `coverage[].key.relation` (R7); `coverage[].key.resolution` (R7); `coverage[].key.sourceUniverse` (R1); `coverage[].key.targetUniverse` (R1); `coverage[].key.subjectScopeCommitment` (R1); `coverage[].entry.relation` (R7); `coverage[].entry.resolution` (R7); `coverage[].entry.examinedUniverse.subjectScopeCommitment` (R1); `coverageCommitment` (R1) | `analysisOrdinal`, `unit`, `limit`, `observed` |
| Complete (w→h) | `CompleteV2` (RPP:435) | always | `stageResults[].stageId` (R1); `stageResults[].factCommitment` (R1); `stageResults[].coverageCommitment` (R1); `factStreamCommitment` (R1); `coverageStreamCommitment` (R1) | `analysisOrdinal` |
| Complete (w→h) | `CompleteV3` (FA2:419) | under symbol-census-v1 (FA-2, proposed) | `symbolCensus.rows[].nativeSubjectId` (R1) | — |
| ProviderFault (w→h) | `ProviderFaultV2` (RPP:441) | always | `executionId` (R1) | `analysisOrdinal`, `phase`, `faultKind`, `detailCode` |
| Cancel (h→w) | `CancelV2` (RPP:447) | always | `executionId` (R1) | `analysisOrdinal`, `reason` |
| Cancelled (w→h) | `CancelledV2` (RPP:453) | always | `executionId` (R1) | `analysisOrdinal`, `observedPhase` |

<!-- wire-identities:end -->

    - **The ceiling.** The identity-bearing members on a provider's wire are **exactly** the members listed above, under the condition each row states. No RequestId, RunId, ProjectId, log path, pid or record key is on the wire, and nothing beyond this list. A row marked "FA-2, proposed" is on the wire only once FA-2 is accepted and its token negotiated (L-G10; item 22). **(r5)** A row marked "RUST3-LIM, accepted; binds after FA-2" is on the wire only once RUST3-LIM is bound, after FA-2, and its token is negotiated (L-G11; RL LD-R8). A row marked `target-attribution-v2` is on the wire only when that token is negotiated (NE:2797-2814).
    - **Control L-C1 (r4; covers R7 and the RUST3-LIM source from r5).** `python3 evidence/wire_identities.py --check` re-derives the inventory from the pinned schema bytes. It fails if the table above or `evidence/wire-identities.json` (which records each source's sha256) differs by one member, rule or line. It runs with no product code, build or network. A schema successor that changes a payload changes the derived table, and so needs a delta round of this item.
    - **FA-2 needs no further member (r4 check).** The derived FA-2 rows hold exactly the two members FA-2's §9.8 and this law's item 22 name: `symbolCensus.enumeratorClosure` on Analyze, and the census rows' `nativeSubjectId` on `Complete`. No cross-law item for FA-2 arises from RF-1.
    - **r1:377** is the historical closed sentence that J1 still cites (X14).
  - **Phase (r2: J1's reading).** A provider exists only after its attempt's ExecutionId is reserved and after Plan sealing (item 2). J1 item 2 fixes where that ExecutionId comes from:
    - for a durable attempt, `CommitSession::open` at row R12, reserved in the process's `ExecutionIdReservations` before any provider frame;
    - for an ephemeral attempt, a host draw at the attempt's start (J1:160-174).

    J1 reads that point as OPP §3.1's "attempt admission" for identities (J1:180). It comes before the attempt row, which OPP §5.5 and J1 item 8 call "attempt admitted" (item 16f). The provider frame builders accept only the reserved type, `ReservedExecutionId` (J1:170). Every provider-attributed record carries `requestId`, `projectId`, `planId`, `executionId`, the component role and the universe-key suffix, which are lawful from those phases (OPP:149-157). S-OP-2's provider and supervision events require Project, Plan and Execution, with `role` and `universe` fields (SOP2:857-861).
  - **What is never stringified.**
    - **RunId.** It is never a wire member. It appears in this invocation's provider-attributed records only after a `Committed` publish, and a candidate RunId is never stringified (OPP:157-159).
    - **The emergency case.** When `RequestAuthority::begin` fails, no RequestId exists (OPP:160). No provider is ever spawned in that case, because no attempt has started.
  - **Host-held values only.** Records use the host's own bound values, never worker echoes. Workers may not mint host identities (DLV:572), and an echo that differs is `PROVIDER.PROTOCOL_VIOLATION` before any source byte or after (NE:2854-2856, NE:3216-3226).
- **Basis:**
  - OPP:145-160;
  - J1 item 2 (J1:148-203);
  - DLV:570-574 (host ownership of process fate and identity);
  - CH13:59-62: "no … hidden environment input";
  - Q0:770, which excludes RequestId and ExecutionId from determinism comparison.
- **Rejected:**
  - **Passing RequestId to the child for its own logging.** Providers never get a log path, and the host writes every provider-attributed record (OPP:222).
  - **Keying records by pid.** Pids are reused. The pid is only an attribute, beside `hostReapedMaxRss` (Q0:889).
- **Forbidden substitutes:**
  - any identity in a record before the phase that mints it;
  - a worker echo used as a record key;
  - a RequestId, RunId or log path given to a child;
  - **(r2)** an ExecutionId on a provider's wire that was not reserved first (J1:194);
  - **(r3)** any identity on a provider's wire beyond this item's list.

**14. The operational record at the provider boundary, and the S-OP-2 events it uses (law).**
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
- **The events (r2).** S-OP-2 is accepted (L-G7), and it owns the names, field schemas and allowlists. This law names each need exactly as S-OP-2 r6 registers it. **Every need is registered; there is no gap.**

| Need | S-OP-2 r6 event (line) | Fields this law relies on | Class |
|---|---|---|---|
| provider spawned | `provider.process.spawned` (SOP2:877) | `protocol`, `pid` | P0; `pid` P1 |
| provider ready (end of the start span) | `provider.process.ready` (SOP2:878) | `start`, `transfer` (SOP2:902) | P0 |
| stage changed | `provider.stage.changed` (SOP2:879) | `stage`, `state` | P0 |
| stage terminal | `provider.stage.terminal` (SOP2:880) | `terminal` (NE:2025, `cancelled` included), `fact_frames`, `coverage_frames`, `analysis` | P0 |
| reaped | `provider.process.reaped` (SOP2:881) | `pid`, `max_rss_native` with `rss_unit` (this law's `hostReapedMaxRss`; SOP2:910), `max_rss_bytes`, `cpu`, `teardown` | P0; `pid` P1 |
| cancel stage 1 sent | `supervision.cancel.sent` (SOP2:888) | `inband`, `control_reason` | P0 |
| cancel stage 2 forced | `supervision.cancel.forced` (SOP2:889) | `trigger` (`second-signal`, `grace-expired`), `grace` | P0 |
| liveness missed | `supervision.liveness.missed` (SOP2:885) | `window` | P0 |
| no progress | `supervision.progress.absent` (SOP2:886). OPP:238's working name `supervision.no_progress` is registered under this name. | `stage`, `since` | P0 |
| stderr reduced | `provider.stderr.reduced` (SOP2:882) | `stderr` (K7 `{bytes, truncated}`) | P0 |
| fault reduced | `provider.fault.reduced` (SOP2:883) | `source`, `fault_kind`, `refusal_family`, `detail` (K7), `detail_code` (K3) | P0 |

  Every row also carries `role` (P0) and `universe` (P1), and requires Project, Plan and Execution (SOP2:857-861). Two more registered events serve other items: `supervision.wait.expired` is item 16c's typed expiry of a bounded wait (SOP2:890), and `host.reuse.disclosed` is item 10's disclosure (SOP2:873). S-OP-2 states that it covers every row of r1's needs table and the provider-boundary record (SOP2:914).
  - **Names belong to S-OP-2.** A later rename or retirement is S-OP-2's registration (SOP2 item 2), not an amendment of this law. The D law's draft registers further supervision events of its own (its records item). This law needs none of them.
- **Basis:** OPP:248-251; Q0 §9.4 (Q0:941-953); ENV:654-686; SOP2 items 22 and 23 (SOP2:831-915).
- **Rejected:** spans from provider-reported timestamps. The provider's clock and claims are not admitted observations.
- **Forbidden substitutes:**
  - any field of the record entering a semantic identity or digest;
  - a record synthesized when instrumentation failed (Q0:953);
  - **(r2)** an event name outside S-OP-2's registry.

**15. DR-G14 at M3: closure manifests and no-ambient refusals; installation stays at M5 (lead decision; `M3-PLAN-r6.md:467`).**
- **Decision.**
  - **What M3 does.** It prepares the self-contained closure manifests and the no-ambient-runtime refusals (F4, G2). At the protocol boundary that means two handshake checks, each `PROVIDER.PROTOCOL_VIOLATION` before any source byte on a mismatch:
    - TS2's HelloAck must match the verified signed provider and runtime descriptors, field by field (NE:2973-2984);
    - Rust3's `HelloAckV3` identity members must equal `expectedIdentity`, which is copied from the Plan's universe row and bound to the verified signed release (NE:2824-2834).

    No PATH or system runtime is ever a fallback (BP:715-717; F02:232-241).
  - **What stays at M5.** `crates/lifecycle/src/installation.rs`, the DR-G14 owner module, which COV lists first at M5.
- **Basis:** COV:4770-4776 (gate milestone M3, owner `installation.rs`); COV:8976 (`installation.rs` at M5); BP:1018; `M3-PLAN-r6.md:181`.
- **Rejected:** building `installation.rs` early. It belongs to the M5 lifecycle surface, and M3 needs only the refusal path.
- **Forbidden substitutes:**
  - ambient Node or a system `rustc` admitted for any reason;
  - a closure mismatch downgraded to a warning.

### D. Cancellation

**16. The provider-side two-stage cancel (lead decisions in 16a, 16b, 16c and 16e).**
- **(a) Stage 1, cooperative**, at the first SIGINT, SIGTERM or SIGHUP before finalization (OPP:329; WS:224-229). For each live provider child the host does two things, in this order:
  1. Its provider-side participant writes the in-band `Cancel` exactly once: TypeScript `CancelV1` with `reason: user-interrupt` (DLV:860, DLV:1122), Rust `CancelV2` with `reason: "user-interrupt"` (RPP:447-451). It then closes the request side (RPP:714, T023, which sets `requestClosed`; DLV:1146).
  2. The control plane sends `cancel` with reason `user` (CC:37) as the supervision-scoped announcement that teardown has begun (CPC:375; CPC:489-492, J-5 T-1).

  Both are appended to the host's one merged event order (CPC:466; CPC:469-472, J-1), and `supervision.cancel.sent` is logged (SOP2:888). **Lead decision: the in-band frame goes first,** so the semantic participant sees `Cancel` before any SDK-level abort.
- **(b) Who may cancel in band.** Only user interruption sends the in-band `Cancel`. Rust's `CancelV2.reason` is exactly `user-interrupt` (RPP:451), and an unsolicited `Cancelled` maps to a provider-protocol fault (DRJ:1850). **(r2)** TypeScript's `CancelV1.reason` also admits `host-shutdown` (DLV:860). **Lead decision: M3 never sends it.** A deadline, liveness failure, resource breach, supervisor fault, revocation or host shutdown uses control `cancel` with reason `deadline` or `supervisor-fault` and the teardown ladder (CPC:489-492). It never uses the in-band frame.
  - **Rejected (r2):** TypeScript's `host-shutdown` for non-user teardown. Rust3 has no such value, so the two languages would diverge on fault teardown. And nothing from a faulting or cancelled child is ever admitted (NE:3837-3843), so a cooperative in-band stop buys nothing there. The D law's cancellation item makes the same choice.
- **(c) After stage 1.**
  - **What may follow.** Only `Cancelled`; then zero-exit and EOF for Rust (P3T:342-364), and EOF for TypeScript (T2O:254-266). TypeScript's `observedPhase` rule for the context interval is unchanged (NE:3296-3302).
  - **Late provider octets** are delivered unmodified to the owning participant, which alone gives them meaning (CPC:462).
  - **The stage-1 grace (lead decision).**
    - **Rust3:** the protocol's own `cancellationGraceMilliseconds`, 5,000 (RPP:119). It is retained with an identical value in `ProtocolLimitsV3` and checked by exact equality in Hello (NE:2929-2941).
    - **TS2:** `TypeScriptProtocolLimitsV1` has no grace member (NE:2961-2967), so the host's "bounded cleanup grace" (DLV:1146) applies. It is the D law's operational constant, provisionally 2 s (OPP:329).

    **(r2)** The D law's constants table uses both values and "never substitutes its own". J1 adopts the same reading for S-OP-12's second stage (J1 8.5, J1:533).

    Every bounded wait must exist, be finite, and append a typed event when it expires (CPC:494). The event is `supervision.wait.expired` (SOP2:890).
- **(d) Stage 2, forced.** A second signal, or expiry of the stage-1 grace, forces the kill of the provider's process tree. The provisional escalation from TERM to KILL is 1 s, with a 10 s reaping ceiling (OPP:273). Scratch is removed (DLV:1146; F02:203-204). A second signal forces at once, inside either protocol's grace. `supervision.cancel.forced` is logged with its trigger (SOP2:889).
- **(e) Outcome (law).**
  - **The class.** It stays `interrupted` (130). For TypeScript, "absence of Cancelled after a user signal does not overwrite that class with a provider fault" (DLV:1146; DLV:1122). For Rust, a signal before finalization with fate `USER_INTERRUPTED` or `VERIFIED_CANCELLED` takes the `interrupt-before` template (DRJ:1036-1051). J1's outcome matrix routes a signal in phase A or B to `interrupted` 130 with no runId (J1 item 10, row 46).
  - **The stage.** A cancelled stage mints nothing and keeps its interrupted termination (NE:3421-3426; NE:3842-3843). Its stage terminal is `cancelled` (NE:2025).
  - **The Run.** "an analysis attempt aborts and leaves no Run" (WS:229). Cancellation is never an incomplete-analysis deficiency or a provider fault.
- **(f) Scope (r2: J1 r3).** Providers are live only in OPP §5.5's phase A, as J1 r3 places that phase. Phase A runs "from R0 until `prepare_commit` returns with the attempt row committed", and "includes the durable entry, project admission, the whole analysis and replay". In phase A, "Providers get `cancel`" under this item (J1:500). No provider is live in phase B or later. **r1's "and the provider part of phase B" is withdrawn.**
  - **The commit-phase join** is J1 r3 item 8, which closes S-OP-12 (J1 successor S15). It covers:
    - the cancellation latch, a third source for the operation's FinalGate (J1 8.1);
    - phases A to E, and J1's phase O (J1 8.2);
    - the outcome-first precedence (J1 8.3);
    - the output decision point (J1 8.4).
  - **Its successors.** X3d r9, X4 r8 and X7 r7 (J1 successors S9 to S11) are each reviewed on their own and land with unit J3b. Until then, no signal sets the latch (OPP:340).
  - **This law decides none of it.**
- **Basis:**
  - DLV:860 (`CancelV1.reason`), DLV:1146 (`userCancellation`);
  - DLV:1122 (`cancelTransition`);
  - RPP:307-308 and RPP:447-457;
  - DRJ:1848-1852 (`cancellationTotality`);
  - F02:171-177 (host-owned race precedence);
  - J1 item 8 (J1:457-582);
  - CPC:660-663, tension T-1. CPC records two cancellation carriers for one child and "Scoped control-plane cancel to SUPERVISION level (teardown-announcement) and left in-band Cancel wholly to the host's provider-side participant". CPC reports that tension as unresolved (CPC:657). This item adopts that split as a lead decision for M3. Open question R1 asks the DR-102 owner to confirm it.
- **Rejected:**
  - **Control-plane-only cancel.** The SDK would then have to synthesize a `Cancelled` frame, which is the control plane authoring a semantic frame (F02:168-170). Or the protocol's own cancel path would starve (CPC:662).
  - **In-band-only cancel.** It leaves the control session with no teardown announcement, and the J-5 ladder starts with `shutdown` or `cancel` (CPC:491).
  - **A single 2 s host grace for both languages.** On automatic expiry it would enforce 2 s in place of the 5,000 ms both sides agreed by exact equality in Hello. Every bound "is enforced at its named boundary" (RPP:134), so that changes an accepted limit's meaning (item 1). A second signal is different: it is the user's explicit demand, and user-interruption precedence survives the missing `Cancelled` (DLV:1122; DRJ:1036-1051). R9 asks the Rust protocol owner to confirm this reading.
  - **A single 5 s grace for both.** It lengthens TypeScript cancellation for no protocol reason.
  - **Killing at the first signal.** It loses the clean `Cancelled` path that K7 keeps (OPP:125).
  - **Mapping a missing `Cancelled` to a provider fault** (DLV:1146).
- **Consequence, recorded.** OPP's cancellation goal (p95 ≤ 2 s from the first signal to exit; OPP:342) may be missed by Rust3 without a second signal, by up to the protocol's 5 s grace. It is a goal, not a threshold (OPP:342), and the measurement reports it (`M3-PLAN-r6.md:470`, `:623`).
- **Forbidden substitutes:**
  - an in-band `Cancel` for a non-user reason;
  - **(r2)** a TypeScript `CancelV1` with `reason: host-shutdown` at M3;
  - a second in-band `Cancel`;
  - a `Cancelled` synthesized by the host or SDK;
  - admitting facts from a cancelled child;
  - a grace without a typed expiry event;
  - any reading of the commit phases in this law.

### E. Boundaries this law does not own

**17. Launch rules are the D law's, under O7.**
- **Decision.** This law states no spawn, environment, descriptor, confinement, grant or scratch-placement rule. The D law alone owns launch rules under O7 (`M3-PLAN-r6.md:211`, `:508`; and `:87`: "launch rules have one owner, the D law, and M3-L cites it").
  - **(r3, NBO-3) The D law's state.** M3-D r3 is **accepted** (GROK2, no required findings; `9679dbc4…`). Its confinement section F is still a placeholder, binding only once O7 is decided as recommended (its own header). This law still cites it by role.

  This law requires only three things:
  - item 2's cardinality and binding preconditions;
  - that no provider launches before O7 is decided and D1's primitive exists (`M3-PLAN-r6.md:476`; J1 join J-ζ);
  - that no repository code executes. `workerExecutesRepositoryCode` is the constant `false` (NE:2534-2535), and "Repository execution is disabled by default" (SL:1059).

  This law does not decide O7, and it assumes no outcome of it. **(r2)** CF-P's feasibility findings (CFP:231-264, CFP:309-315) are evidence for the owner's decision. They are not a decision, and CF-P claims nothing as enforced (CFP:3). The confinement disclaimers stand until their successors are accepted (`M3-PLAN-r6.md:487-495`): SL:497, SL:1113, AQ:344, NE:2554 and REG:366.
- **Rejected:** restating the lead's O7 recommendation (`M3-PLAN-r6.md:478-485`), or CF-P's profile, as law here. That would pre-empt the owner and create a second owner of the launch rules.
- **Forbidden substitutes:**
  - a launch rule written in this law or in any M3 provider unit rather than the D law;
  - any confinement claim before CF-1.

**18. The commit-phase cancellation join is J1 r3 item 8 (record).** S-OP-12 is closed there (J1 successor S15), and it lands with J3b through X3d r9, X4 r8 and X7 r7. See item 16f. This law refers to it and does not decide it.

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

**20. F02's stale protocol majors.** F02:220 says the TypeScript selector's major "is **1**", and F02:259 says "The normative Rust contract is **major 2**". The current majors are TS2 and Rust3 (BP:717; NE:2785; QG:202). Those sentences are historical for M3. Their structural rules still bind: one child per key and no reuse (F02:222-224, F02:268-269), and the successor rule (F02:271-273). The plan already forbids the M3 laws to copy the stale majors (`M3-PLAN-r6.md:189`). A note is proposed for the same batch.

**21. NE §14's heading.** NE:4203 reads "Host composition corrections (mixed authorship; independent Claude review pending)".
- **What this record establishes.** The current NE bytes (sha256 `83b99783…`, 329,013 bytes) are a member of `docs/coop/design-corrections/reviews/candidate-subject.v45.json`. That file is the subject of `claude-independent-design.v45`, whose verdict is `ACCEPT`, and QG cites that review for DR-G10 (QG:212-215). So "pending" is not a current fact about these bytes' review status.
- **What it does not establish.** Whether v45's read scope covered §14 in particular (open question R6).
- **No edit.** NE is a frozen contract and is not edited.

### G. The provider symbol census (r3)

**22. FA-2's carrier, joined (lead decision, r3; M3-H X-H1; gate item L-G10).**
- **The obligation.** A TypeScript or Rust provider's symbol census is its "explicit population assertion" (NE:88-91), and symbol-scope subjects are its rows (RPS:15; ENC:93). r2 left it without a carrier. No TS2 or Rust3 frame carries it, EXC forbids a new frame name (EXC:270), and item 1 forbade this law to add one. The request key would also have needed the census before spawn (H3:850-858). Without it, no TS or Rust symbol-kind Coverage is admissible, and I1's cycle rule cannot decide on a real Run (H3:705).
- **Decision.** This law adopts FA-2's carrier **as proposed**. It decides none of FA-2's content. Where they differ, FA-2's accepted bytes govern, and this item takes a delta round ("Review and effect").
  1. **What crosses the wire.** Only under `symbol-census-v1`, which is negotiated by the existing exact echo (FA2 §9.1 paragraph; FA2 LD-F1):
     - **host to worker, on `Analyze`:** `symbolCensus` = `{enumeratorClosure}`, or `null` when no census is owed;
     - **in the request, before spawn:** each `symbol`-kind key commits to the census **rule**, the scope2 of its descriptor with `subjects: []` (D∅; FA2 LD-F2);
     - **worker to host, on `Complete`:** the census, either `complete` `{examinedPaths, rows}` or `over-bound` `{rowCount, examinedPathCount}`, never truncated. Each `symbol`-kind Coverage entry commits to the census **values**, the same descriptor with the census as `subjects`;
     - **nothing** on `BudgetExhausted`, `Unavailable`, `Cancelled` or `ProviderFault`.

     There is no new frame, phase, terminal, limit member, identity version or major. Item 1 holds, and item 13 lists the two members.
  2. **When it is admitted.** Only at D3's clean settlement of `Complete`, atomically with that Analyze's facts and Coverage, in H's order: facts, then the census, then `D` and Coverage (H3 item 3).
     - The host projects the census into `SubjectInventoryV1` records. They are host-derived typed inputs under their admission owners, never stage outputs (EXC:59, EXC:259, EXC:265-272).
     - The host owner-admits them against the Plan's locators and the symbol extent (ENC:115-123, ENC:166), then runs NE §4.1a on each `symbol`-kind entry.
     - A fault, a cancellation or a non-`Complete` terminal admits no census (NE:3837-3843; item 16e). On a clean `BudgetExhausted` or `Unavailable`, the owed inventories are host-derived outcomes (H3 item 4).
     - Frame acceptance is still not admission (item 12.3), and a census is not progress.
  3. **How reuse treats it (INC).**
     - **INC-1 and INC-2 (items 4, 5).** Every projected record names the current `planId` and `parameterDigest`, and every scope built from it binds the current `snapshot2`. A census is never carried across Plans, and no M3 path reuses one (item 3). It is a provider attestation admitted in one Run, never authority beyond it.
     - **INC-3 (item 6).** A census depends on its universe's whole program. **(r4, NBO-3)** Its invalidation key covers **every class item 6 names**: enumeration, incoming references, negative dependencies, configuration and native context, tool and rule closures, dependency source sets, and prepared outputs (AQP:391-399). The last two can change the symbols a worker attests as surely as an edit can. Per-file dirtiness is never sufficient by itself.
     - **INC-4 (item 7).** A paired full and incremental sequence compares census rows, and the scopes built from them, like any semantic payload.
     - **INC-8 (item 10).** The census is recomputed every Run and covered by `host.reuse.disclosed` per stage and universe. No census-specific record exists.
  4. **Records.** No S-OP-2 event is added. Census bytes are semantic evidence, and no operational record carries them (item 14).
- **Basis:** H3:613-643 (item 17), H3:850-858 (X-H1); FA2 LD-F1 to LD-F7 and §9.8; NE:88-96; IE:1462-1470; ENC:115-123; EXC:259, EXC:265-272; RPS:15.
- **Rejected:**
  - **Leaving FA-2 out of this law's gate.** L in effect would fix TS2 and Rust3 for M3 with no lawful symbol Coverage, so F2, G3 and I1 could not deliver.
  - **Drafting the carrier in this law.** Item 1 keeps protocol changes in reviewed native successors; this law only joins them.
- **Forbidden substitutes:**
  - a census on any other frame or payload, or without the token;
  - a census inferred from facts, anchors or files (RPS:15; MI:492);
  - a census admitted before clean settlement, or carried across Plans;
  - a census that is truncated, sharded or partial on `Complete`.

## Joins checked (r2, refreshed in r3)

Every join this law makes to a law accepted since r1 was read on 2026-10-04, as were its joins to the D law, now accepted, and **(r3)** to M3-H and FA-2.

| Law | Join | Result |
|---|---|---|
| **S-OP-2 r6** (accepted) | Items 10, 12, 13 and 14: the record join, the reductions, correlation and the events | **Consistent.** Every event need is registered (item 14). SM-10's unit now follows SOP2:910 (item 9; S-OP-2's R9, SOP2:1041). The `detailCode` row matches item 12.2 (SOP2:844). Counting stderr fits `Reduced::from_capture` (SOP2:837). S-OP-2's two rows beyond r1 (reduced `refusal` detail, unrecorded nonces; SOP2:850) are adopted in items 12.2 and 12.4. |
| **J1 r3** (accepted) | RequestId and ExecutionId phase (J1 item 2); where a child starts (J-ε, J-ζ; J1 item 5.2); the commit-phase join (J1 item 8); the second stage (J1 8.5); outcome rows 30 and 46 | **Consistent, with r1's phase scope corrected.** Item 13 adopts J1 item 2's reading. Item 2 cites J-ε and J-ζ. Item 16f narrows r1's scope to phase A (J1:500) and defers to J1 item 8. J1 8.5 adopts item 16c's grace, which answers X3 for S-OP-12. Row 30 (worker fault: `PROVIDER.PROTOCOL_VIOLATION`, no facts, Coverage or Run) matches item 5. Row 46 (signal in A or B: `interrupted` 130, no runId) matches item 16e. **(r3)** J1 r4 is accepted (GROK2). It changes none of these provisions: it adds R10a, ER10a and SD-6's rows. Its line 207, like r3's line 192, forbids "any identity on a provider's wire beyond M3L:377's". Item 13 now lists those identities exactly, and J1's next revision re-cites item 13 (X14). |
| **MC r6** (accepted in review) | MC item 20's INC consistency; MC's uses of items 2, 13 and 17 (MC:93, MC:642); MC X-1 and X-3 | **Consistent.** MC item 20's claims hold against r3 unchanged. X-1 is taken into SM-5 and SM-6. X-3 is recorded as X12 and R10. MC's gate (MC:88-89), "M3-L is accepted", means L in effect ("Review and effect"). **(r3)** C r7, in review with CODEX2, narrows only item 16's row 8 and has no join here. FA-2's C follow-ups go to C's next revision (X16), as FA-2 r2 narrows them: the enumerator of a TS or Rust binding that owes a symbol inventory (not host-derived inventories, X-H3; not syntax universes); a worker for every TS or Rust universe such an inventory binds; and the Plan-time token need. |
| **ME r3** (accepted) | In-host syntax with no child (ME §G); "no in-process fallback" (ME item 16, reason 5); no producer cache (item 3); **(r3)** the syntax stage as an in-core producer (item 5) | **Consistent.** Item 2 states the syntax scope, and keeps the fallback bullet ME relies on. **(r3)** Item 5's exception names E1's syntax stage exactly as ME item 14b and ME:478 define it (r4, NBO-1). E3's in-host census needs no carrier (item 22). |
| **I1 r2** (accepted), **I1-L** (accepted, bound at `0ceb9ad`) | **(r3)** The cycle atom's census and exact scopes (MI:113, MI:155-165) | **No text join; a delivery join.** I1 cites nothing in this law, and its product chain does not wait for it (`M3-PLAN-r6.md:355`). Its atom decides on a real TS or Rust Run only through retained symbol inventories and symbol scopes. Item 22, with FA-2, H and F2, is what makes those producible. Until then every such answer is indeterminate, which fails closed (H3:705). |
| **M3-H r3** (**accepted**; r5 re-pins from r1) | **(r3)** X-H1, X-H4 | **Answered.** X-H1 is answered by item 22 with FA-2 (L-G10). X-H4 is answered by item 5's in-core exception. H's other cross-law items (X-H2, X-H3, X-H5, X-H6) are other owners'. H depends on this law, not the reverse. |
| **FA-2** (design unit; r2 in review with Codex) | **(r3)** Items 1, 13 and 22; L-G10 | **Joined as proposed.** FA-2 adds no frame, phase, terminal, limit member, identity version or major (FA2 "Within the current majors"). Its wire members are item 13's FA-2 entry. Its admission point is H's clean settlement (item 22.2). Its finding F-1 is X15, and F-2 is X13. |
| **RUST3-LIM** (design unit, accepted by GROK2 at r1; binds after FA-2) | **(r5)** Items 1, 9 and 13; L-G11; X13, R12 | **Joined as accepted.** It adds no frame, phase, terminal, limit member or value, identity version or major (RL "Within the current majors"). Item 13's derived table carries its stage record, and the AnalyzeV2 row's condition. Item 9 carries SM-11 to SM-14. It binds after FA-2, whose handshake copies are its parents (RL LD-R8). Its X-RL-C1, C2, D and G items are its own owners'. |
| **MB r2** (accepted) | Item 17 (MB cites it at r1's lines 494-509) | **Consistent.** Item 17 is kept. |
| **X12 r4** (accepted) | Pack refusals "reach no evaluation, provider, facts, Coverage or custody call" (X12r4:244) | **Consistent** with item 2: a pack refusal precedes the Plan, so it precedes any child. |
| **X2 r9** (accepted) | Project admission, the phase from which ProjectId is lawful (OPP:154) | **Consistent.** Item 13 uses only that phase. |
| **The D law** (M3-D r3, **accepted** by GROK2; r3, NBO-3) | Items 2, 9, 12, 13, 14, 16 and 17; **(r3)** item 22 through D2b | **Consistent.** **(r3)** FA-2's payload versions are D2b's to decode, under D's "one codec per protocol, no translation" (FA2 X-FA2-D). D3's settlement is unchanged, because the census arrives in `Complete`. The D law follows items 12, 13, 14 and 16 (its gate note). Its stderr item departed from r1's item 12.1, and r2 adopts its reading (item 12.1), so the departure closes. Its constants table answers R8 and adopts R9's reading. Its control-codec item proposes X5's tuple. This law defers launch rules to it (item 17). It cites r1 by line (X10). |

## Cross-law findings

These are recorded for their owners. None changes an accepted outcome. Each names the record that must change, if any.
- **X1. `cache2` binds the Plan** (item 4). Any changed-scope design needs a D5a IE successor before it can reuse work across an edit. This is the main finding for D5a and for M4's changed-scope decision. **Owner:** the identity owner (AQP:546).
- **X2. The two cancellation carriers.** CPC's T-1 is reported as unresolved (CPC:657-663). Item 16 adopts CPC's split for M3, and R1 asks the DR-102 owner to confirm it. The D law's cancellation item follows the same split.
- **X3. OPP §5.5's provisional 2 s grace against Rust3's 5,000 ms protocol grace** (RPP:119; NE:2934). Item 16c reconciles them. **r2:** J1 adopts that reading for S-OP-12's second stage (J1 8.5, J1:533), and the D law's constants table adopts it for supervision. **Still to change:** OPP's next revision should cite the protocol member. J1 successor S15 already asks OPP's next revision to cite J1 item 8.
- **X4. The SDK alias bindings name V1 payloads** (DRC:556-566), while TS2 is current. Item 12.5 records the re-binding, and R2 asks how the DR-125 owners classify it.
- **X5. The control `select` tuple for TS2 and Rust3.** CC records only a preview witness, `analyzer`/`typescript`/`1` (CC:199-202). **r2:** the D law's draft proposes the tuple in its control-codec item: `analyzer`, the provider id (`typescript-semantic` or `rust-semantic`) and the protocol major as an integer, 2 or 3. A manifest-owner record confirming it is in the D law's successor list. X5 stays open until that record is accepted (R3). This law requires only that the tuple be the exact pinned selection, with no translation (F02:164, F02:168-170).
- **X6. Liveness against synchronous compiler work** (item 12.4). A single-threaded responder can turn a legitimate long phase into a liveness fault. SM-8 measures the exposure, and F, G and the D law resolve it. The D law's draft sets the floor at 2 × SM-8.
- **X7. Stale record text:** REG:355, F02:220, F02:259 and NE:4203 (items 19-21). **Owner:** the record-hygiene batch (R5).
- **X8. Citation drift. Resolved.** M3-PLAN r5 re-pinned every AQP line (`M3-PLAN-r6.md:64`, row 12), and its M3-L row now cites AQP:389-409 (`:207`).
- **X9 (r2). M3-PLAN's sending order and day 0.** The plan says "**Before L can be sent:** S-M, the two sign-offs and O7" (`M3-PLAN-r6.md:445`), and schedules r2 to fill ⟨SM-n⟩ after S-M (`:426`). r2's review rule sends L before both. The gate is unchanged.
  - **Must change:** M3-PLAN's next revision (a lead record). It should replace `:445` and `:426` with the review rule, and should state that day 0 (`:255`) and "L acceptance" (`:378`) mean L in effect.
  - **Also stale there:** its O7 risk line (`:524`, Seatbelt "unverified") predates CF-P.
  - **(r3) Also to record there:** L-G10 (FA-2 accepted) in the M3-L row; FA-2 among the pre-day-0 law rounds, accepted before D2b starts (H3:841).
  - **(r5) Done in M3-PLAN r9 (accepted),** except two items. r9 replaces `:445` and `:426` with the review rule, states day 0 as "L in effect" (`M3-PLAN-r9.md:385`), and records L-G10 (`:255`; P7-1, P7-2). **Still to record in its next revision:** L-G11 (RUST3-LIM accepted), RUST3-LIM among the pre-day-0 rounds, and the `L-G` rename its own NBO-1 asks for.
  - **Until then,** this law's "Review and effect" governs L's own review, and day 0 is unchanged.
- **X10 (r2). Citations of r1 by line.** These laws and drafts cite r1 by line:
  - MC r6 (`L:n`);
  - J1 r3 (`M3L:n`);
  - S-OP-2 r6 (`M3L:n`);
  - ME r3 (`L:132`);
  - MB r2 (`ML:494-509`);
  - the D law's draft (`ML:n`).

  Each pins r1 (`5e858c05…`), now kept as `PROPOSAL-r1.md`, so every cited line still resolves. r2 and r3 keep every item, X, R and O number, and the substance each of them cites, with one exception. **What changes:** each re-pins by item at its next revision. The D law can now say that its stderr item follows item 12.1 rather than departing from it.
  - **(r3, RF-1) The exception: J1:192.** J1 r3:192, and its accepted r4 successor J1r4:207, forbid "any identity on a provider's wire beyond M3L:377's". r1:377 is item 13's old closed list, which RF-1 found shorter than the contracts. That citation needs a content change, not just a re-pin: X14. r2's "no content change is needed in any of them" was wrong for J1.
- **X11 (r2). OPP wording.** OPP:171 says provider stderr is "held in memory" before reduction. Item 12.1 counts without holding, with the same lawful output, and so does the D law's stderr item. OPP:238 names the no-progress record `supervision.no_progress`, while S-OP-2 registers it as `supervision.progress.absent` (SOP2:886). **May change:** OPP's next revision may align both. No outcome changes. **Owner:** OPP's owner (CLI and operability).
- **X12 (r2; MC X-3). Rust3's prepared-entry bound.** Rust3 retains v2's `maxPreparedOutputEntries` of 256 (RPP:102; RPP:385; NE:2934), beside `maxExpansionRows` and `maxGeneratedFileRows` of 1,000,000 (NE:2933). This law changes no limit (item 1). If 256 governs a prepared manifest's entries, an admitted prepared set of more than 256 entries cannot reach a Rust3 child. That would need a Rust protocol successor, never host-side splitting. At M3 prepared sets are harness-imported (MC O-1), so this bears on G4, not on M3's T2 measurement. **Owner:** the Rust protocol owner (R10, joining MC's R4).
- **X13 (r3; FA-2 F-2). Rust3's 256-subject request cap.**
  - **The rule.** RPP's `planAndDomainProjection.subjectsAlgorithm` puts every non-empty `.rs` file of the sealed snapshot into each Rust stage's `analysisDomain.subjects` (RPP:226-231). It rejects the request "before child spawn" above `maxSubjectsPerStage`, which is 256 (RPP:106). Rust3 retains that limit with an identical value in `ProtocolLimitsV3`, checked by exact equality in Hello (NE:2929-2941; the handshake schema's `ProtocolLimitsV3.maxSubjectsPerStage`, const 256). NE §0 supersedes neither the algorithm nor the limit.
  - **The effect.** The T2 manifest records more than 256 Rust files for 9 of its 22 Rust entries. Two are in S-M's seven Rust medium workloads (item 9): `rs-medium-axum` (301) and `rs-medium-tokio` (808). The lead has not recounted non-empty `.rs` entries. A product Rust provider could not be spawned for those repositories.
  - **What it does not affect.** S-M's throwaway harness is not bound by the request rule, so SM-3 and SM-4 can still be measured.
  - **This law changes no limit (item 1).** A change to the subject list or the limit changes the Hello-checked limits map, which is a Rust protocol successor.
  - **Owner:** the Rust protocol owner (R12).
  - **(r5) Closed by RUST3-LIM, and gated as L-G11.** RUST3-LIM names the subject array by reference under the optional token `subject-scope-reference-v1` (RL §9.3a). Host and worker rebuild the array from the accepted `SnapshotManifest`, the commitment recipes and `ProtocolLimitsV3` are unchanged, and the token is needed exactly when a snapshot has more than 256 subjects. Its own count agrees with T2's in 21 of 22 entries (rust-analyzer has two empty files). axum and tokio become servable, and aws-sdk-rust (242,187 subjects) stays beyond `snapshot2`'s bounds and takes the scope-limit route. GROK2 has accepted it (L-G11). What remains is its binding after FA-2, not X13.
- **X14 (r3; RF-1). J1 re-cites item 13.**
  - **What changes.** J1's next revision replaces "beyond M3L:377's" (J1 r3:192; J1r4:207) with a citation of this law's item 13. It is **not** folded into J1 r4, which GROK2 accepted.
  - **Until then,** J1's forbidden substitute reads against r1's narrower list. Nothing J1 permits is wider than item 13, so no outcome changes in the meantime.
  - **Owner:** J1's author (the lead).
- **X15 (r3; FA-2 F-1). The inherited request-key commitment rules.**
  - **The conflict.** DLV `coverageDomain.keyConstruction.subjectScopeCommitment`, DLV `RequestedCoverageDomainV1.workerRule` and RPP `planAndDomainProjection.coverageDomainAlgorithm[3]` give every key of a stage one file-set commitment. NE §4.1a requires each key's own scope2 (NE:1927-1945), and NE:3279 requires the entry to equal the request. NE §0 names none of the three as superseded, although its C-2 row makes §4.1a the field's recipe (NE:136). So the two rules conflict for **every** key.
  - **The resolution.** FA-2's §0 row C closes it in both languages, with or without the token, keeping the inherited file-set proofs. This law's item 1 reads TS2 and Rust3 with that row once FA-2 is accepted.
  - **(r4, RF-2)** Row C sets a wire value: the commitment every requested key carries. So a change Codex's review forces in row C reopens this law through the third delta-round trigger, like any change to rows A, B or D.
  - **Owner:** the native owner, through FA-2.
- **X16 (r3). FA-2's follow-ups for other laws** (FA2 "Cascade and cross-law items"):
  - **M3-H's next revision:** item 17's provider leg; symbol `D` from the census, or D∅; item 11's pre-Analyze symbol entries; H-C17's new cases.
  - **M3-C's next revision** (as FA-2 r2 narrows it, FA2-R1-02):
    - the enumerator of every available TS or Rust binding **that owes a symbol inventory** is the universe's worker provider closure. Host-derived file and package inventories and the inventory relations are excluded; they are H's X-H3, routed to M3-C r8 and CRC-2. Syntax universes have no child;
    - every TS or Rust universe that an expected symbol inventory binds has a worker;
    - the Plan-time token need.
  - **D2b:** the four payload versions.
  - **F2 and G3:** the emission duty and the signed capability rows.
  - **M3-PLAN (X9):** L-G10 and the pre-day-0 round.

  None of these is decided here.

## Forbidden substitutes

- Any change to a TS2 or Rust3 frame, member, phase, terminal, token, limit or identity version made by this law, a provider unit or the control plane (items 1, 11).
- A provider process reused across ExecutionIds, Plans or universes; retained after its terminal; pooled or pre-spawned; restarted within an attempt; or replaced by in-process analysis. A provider child for a syntax universe (item 2).
- Reuse of an authoritative object, a cache entry consumed under another Plan, or a key match treated as admission (item 4).
- A fact, scope, Coverage entry or view not minted under the current snapshot and Plan; a host-minted fact with neither a producing frame nor a Plan-selected in-core producer stage (item 5).
- An unbounded invalidation treated as bounded, or a full-analysis fallback that is not disclosed (item 6).
- Changed-scope shipped without INC-4's paired equivalence (item 7).
- A resident or long-lived host or provider at M3 (item 8).
- A number in this law not taken from S-M's report, or this law taking effect without S-M (item 9).
- Reuse provenance in any semantic payload, digest or Coverage entry, or a Coverage successor carrying provenance (item 10).
- A new progress, diagnostic or heartbeat message; provider-asserted progress; or parsed stderr (items 11, 12).
- stderr text, a stderr digest, stderr bytes kept in any buffer, or `fault` detail text in any sink (item 12).
- A RequestId, RunId or log path given to a child; an identity in a record before its phase; a worker echo used as a key; an unreserved ExecutionId on the wire; or any wire identity beyond item 13's list (item 13).
- Any operational-record field entering identity; a record synthesized after an instrumentation failure; or an event name outside S-OP-2's registry (item 14).
- Ambient runtimes or tools, or a closure mismatch downgraded (item 15).
- An in-band `Cancel` for a non-user reason, with TypeScript's `host-shutdown`, sent twice, or synthesized as `Cancelled`; facts admitted from a cancelled child; or a bounded wait with no typed expiry (item 16).
- Any launch rule outside the D law, or any confinement claim before CF-1 (item 17).
- Any decision about the commit-phase cancellation join (items 16f, 18).
- Any edit to a frozen contract, the register or a D-372-pinned file to apply items 19-21.
- **(r2)** An ACCEPT in review treated as this law in effect, by this law or by any dependent ("Review and effect").
- **(r3)** A provider symbol census on any carrier but FA-2's, inferred by the host, admitted before clean settlement, carried across Plans, or truncated (item 22).

## Open questions

### For the owner

- **O1. O7, hostile-input confinement.** Gate item L-G9 and blocker B1. The lead's recommendation is in ON B1 and at `M3-PLAN-r6.md:478-485`. **r2:** CF-P's evidence is in, and it is summarized in L-G9. This law is drafted so that it does not depend on the outcome ("What depends on O7, S-M, FA-2 and RUST3-LIM").
- **O2. Sign-off on D3 (the T2 selection) and D13 (the exploratory envelope).** These are gate items L-G4 and L-G5 (AQP:543, AQP:554) and blocker B3. They are lead work that needs the owner's sign-off. D13 also gates S-M's report. D2's placement sign-off (AQP:542) stays `proposed`. It is not a gate item here (L-G6).
- **O3. Conditional on S-M outcome (B).** If the one-shot fixed floor F exceeds the 2 s edit target, M4's changed-scope cannot meet that target under TS2/Rust3. The owner would confirm one of two things:
  - the edit target waits for M5 residency, as D5's staging implies;
  - or D5's staging changes.
- **O4. Conditional on S-M outcome (C).** If one-shot full analysis misses a medium budget (30 s cold or 8 s warm), that is the D4 revisit AQP:372 names. The owner decides whether to revisit the budgets or the staging.
  - **(r3, NBO-2)** O3 and O4 can arise together: under (B) and (C) at once, the owner answers both.
- **Flagged for possible reversal (r2):** r2's three new lead decisions: the review rule, counting stderr without holding it (item 12.1), and never sending TypeScript's `host-shutdown` (item 16b). None blocks.
- **Flagged for possible reversal (r5):** none blocks.
  - L-G11: RUST3-LIM accepted is a condition of this law taking effect.
  - Rule R7, which widens item 13's ceiling to every required member of an identity key.
  - **A consequence worth knowing:** a Rust release without `subject-scope-reference-v1` still serves repositories of 256 subject files or fewer, but never more (RUST3-LIM owner note 1).
- **Flagged for possible reversal (r3):** none blocks.
  - L-G10 and item 22: FA-2 accepted is a condition of this law taking effect.
  - Item 5's in-core exception, limited to exactly two named stages.
  - The third delta-round trigger.
  - **A consequence worth knowing:** TypeScript and Rust semantic analysis needs FA-2's token wherever a symbol census is owed, which is almost every semantic cell. A provider release without it is never spawned for such a Plan (FA2, owner note 1).

### For S-M's data

These are SM-1 to SM-10 (item 9). Each decides or informs the following:
- **F (SM-1 or SM-3, SM-5, SM-7, SM-9)** decides outcome A, B or C, and so O3 and O4.
- **SM-2 and SM-4** give T, and show how much changed-scope could save at M4.
- **SM-5 and SM-6** show whether a medium TypeScript read set with `node_modules` fits TS2's `maxSnapshotEntries` of 200,000 and, more tightly, `snapshot2`'s 100,000 rows and 4 MiB descriptor. A TS2 limit miss is a successor question by item 1, and cannot be fixed by host behaviour. A `snapshot2` miss is MC's S-R (MC item 5).
- **SM-8** sets the floor for the D law's health window, or shows that the providers need an independent responder (X6).
- **SM-1 and SM-3** also inform the D law's handshake deadline.
- **SM-3 and SM-4** depend on S-P. If S-P fails, the Rust rows are `incomplete`. Whether the law can take effect with Rust rows incomplete is a question for the delta round's reviewer. The lead's recommendation is no, unless S-P's failure is itself accepted as a finding with a G2 plan.
- **SM-10** informs OPP §5.2's concurrency ceiling (information only).
- **(r5) SM-11 to SM-14** set the M3 Rust provider's effective subject ceiling (S_eff), the Rust stage budget for G's budget profile and C's Plan, and where FA-2's census `over-bound` route starts to bind. None of them is a protocol constant (item 9; RUST3-LIM).

### For other owners and reviewers

- **R1. DR-102 owner.** Confirm item 16's reading of the T-1 split between control and in-band cancellation (CPC:660-663).
- **R2. DR-125 owners.** Is the SDK alias re-binding from V1 to TS2 payloads (item 12.5) a record join, or does it need an SDK successor?
- **R3. The D law, with the manifest owner.** Fix the control `select` tuple for TS2 and Rust3 (X5). **r2:** the D law's draft proposes it, with a manifest-owner record in its successor list. R3 closes when that record is accepted.
- **R4. Identity owner (D5a).** Is a cache-key domain without `planId` admissible under IE §4's no-hidden-input rule (IE:1296-1298)? What re-admission evidence does a reused candidate need under a new snapshot (items 4 and 5)? This is needed before M4 ships changed-scope, not for M3.
- **R5. The record-hygiene batch.** Add the notes in items 19 and 20 to its re-pinning successor (RH §2).
- **R6. The lead.** Did the read scope of `claude-independent-design.v45` cover NE §14 (item 21)?
- **R7. The reviewer.** Is L-G6 met by Q0 §2's draft specs, or does "the D2 draft" mean a drafted WS/pack successor (AQP:542)?
- **R8. The D law (supervisor).** Fix the TS2 cleanup grace, the health window, and the TERM-to-KILL escalation and reaping ceiling. Items 12.4 and 16c set their constraints. **r2: answered in the D law's draft** (its constants table): the TS2 grace is 2 s, provisional; the liveness window is 5 s, raised to at least 2 × SM-8; TERM to KILL is 1 s; the reap ceiling is 10 s, or 5 s under revocation. R8 closes when the D law is accepted. **(r3) Closed:** M3-D r3 is accepted with that constants table (NBO-3).
- **R9. Rust protocol owner.** Item 16c reads `cancellationGraceMilliseconds` (RPP:119) as the host's stage-1 wait before a forced kill on automatic expiry, not only as a ceiling. The drafting read found the member in the v4 guard context list (`rust-provider-protocol.v4.json:966`) but not the guard that uses it. Confirm the reading. **r2:** the D law's draft and J1 8.5 adopt it, pending this confirmation.
- **R10 (r2). Rust protocol owner.** X12: does `maxPreparedOutputEntries` 256 (RPP:102, RPP:385) govern a prepared manifest's entries in transport, beside NE's 1,000,000-row bounds? This is MC's R4, asked from this law's side.
- **R11 (r2). The reviewer.** Is "Review and effect" lawful: an ACCEPT in review, effect only when the gate is met, delta rounds for S-M and O7, and dependents reading "M3-L accepted" as L in effect? Is "What depends on O7 and S-M" complete? **(r3)** Grok answered yes, apart from the joint case, which r3 adds (NBO-2).
- **R12 (r3). Rust protocol owner.** X13: should Rust3's request subject list stay "every non-empty `.rs` file of the snapshot" under a cap of 256, which refuses two of S-M's seven Rust medium workloads before spawn? Or does a Rust protocol successor replace it, for example with a binding-scoped or uncapped transport list? This law changes no limit. **(r5) Closed:** RUST3-LIM is that successor, by reference under a token, with no limit value changed. Its acceptance is L-G11.
- **R15 (r5). The reviewer.**
  - Is R7's record list complete: every record a cited contract defines as an identity key or as a key's field-for-field copy, and every member required to equal a key's? Is the checked list of other composite keys right in excluding the fact identity, commitment preimages, view and occupancy records, correlation tuples and scope summaries?
  - Do the derived counts and the RUST3-LIM row match the schemas?
  - Is L-G11 a lawful second addition to the plan's gate row, and is the fourth trigger's map of RUST3-LIM's parts exact?
- **R14 (r4). The reviewer.**
  - Is item 13's derived inventory right? In particular: the frame-to-payload map, the record identities and the `CHILD` map in `evidence/wire_identities.py`, and the closed rules R1 to R6, including what R4 and R5 admit.
  - Does control L-C1 re-derive it from the pinned bytes?
  - Is the third trigger's map of FA-2's parts complete and exact?
- **R13 (r3). The reviewer.**
  - Is item 13's inventory now exactly the contracts' (NE:2816-2835, NE:2955-2981, NE:3158-3191, with the later echoes)?
  - Is item 22's join complete and lawful against FA-2: what crosses, when it is admitted, and INC?
  - Is L-G10 a lawful addition to the plan's gate row?
  - Is item 5's in-core exception exactly two stages, and no wider?

## Not claimed

- **Measurement.** Nothing has been measured. Every `⟨SM-n⟩` is a placeholder. The only numbers here are owner-approved targets, protocol constants, schema bounds, and OPP's and the D law's provisional values, each cited.
- **Records.** No contract, schema, gate, threshold, register row or pinned file is changed. Items 19-21 are records, and their notes are proposals.
- **Decisions.** O7 is not decided, and no confinement is claimed; CF-P's findings are cited as evidence only. The commit-phase cancellation join is not decided (J1 item 8). No launch rule is stated (the D law).
- **Shipped features.** No changed-scope path, cache or resident host ships at M3. No D5a successor is drafted.
- **Registration.** This law registers no event and no code table. Item 14 names S-OP-2's events and relies on them.
- **Other laws.** No accepted law is changed by this revision. Cross-law items X3, X5 and X9 to X16 name the records that should change, for their owners. J1's re-citation (X14) is not folded into J1 r4.
- **FA-2.** This law joins FA-2 and decides none of its content. FA-2's protocol change is the native owner's successor, under its own review (L-G10).
- **This revision.** No product code, cargo command, test or lead run set was run for it. Product facts come from reading main `e093e90` with `git show` and `git diff`, re-checked against `cd5958b` and **(r5)** `392499e`. **(r4)** The only script run is control L-C1 (`evidence/wire_identities.py`), which reads arch documents.
- **Effect.** An ACCEPT of this revision is "accepted in review". The law takes effect only when gate items L-G1, L-G4, L-G5, L-G9 and L-G10 are met, L-G11 still holds (it is met in review unless Codex's review changes FA-2's handshake copies), and S-M's delta round is accepted.
- **RUST3-LIM.** This law joins RUST3-LIM and decides none of its content (L-G11).
