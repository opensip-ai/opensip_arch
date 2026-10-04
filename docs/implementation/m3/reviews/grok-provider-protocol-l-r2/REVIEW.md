# M3-L r2 — provider-protocol and reuse law

**Verdict: REQUIRED-FINDINGS.** One finding, RF-1, on item 13’s closed wire-identity list. An ACCEPT would have been “accepted in review” only. The law takes effect only when G1, G4, G5 and G9 are met and S-M’s delta round is accepted. Those four gate items are open.

Subject: `docs/implementation/m3/provider-protocol-l/PROPOSAL.md`, 91126 bytes, sha256 `5bd4025ee5e9c43c4fd1f9543a73bd756352414d7eab682a62c045af91d07fd9`. Whole law read against `PROPOSAL-r1.md` (`5e858c05…`). No cargo, no product build, no test run. The real OpenSIP home is absent.

## RF-1. Item 13’s wire list is shorter than the lines it cites

Item 13 (line 478) says the only identities on the wire are `executionId`, `snapshotId`, `planId` and the universe key, citing NE:3158–3163 and NE:3166–3189.

Those lines define the OpenUniverse payloads:

- `TypeScriptOpenUniverseV2` = `{executionId, snapshotId, planId, planIntentCommitment, providerId, universe, universeKey}` (NE:3166–3177).
- `OpenUniverseV3` = `{executionId, snapshotId, planId, planIntentCommitment, providerId, universe, repositoryResolution}` (NE:3178–3187). `repositoryResolution` carries `dependencySourceSetId`, `preparedOutputSetId`, `authorizationId` and `effects`.
- NE:3159: `executionId` and `planIntentCommitment` keep their owners.

Item 15 requires handshake identity members that are also on the wire: `HelloAckV3`’s five identity members equal `expectedIdentity` (NE:2830–2833), and `TypeScriptHelloAckV2` carries the provider and runtime descriptor digests and identity fields (NE:2973–2981).

`PROPOSAL-r1.md:377` is the same sentence. J1 r3:192 forbids “any identity on a provider’s wire beyond M3L:377’s”. X10 (line 705) says that citation needs no content change.

The rest of item 13 holds. RequestId is absent from both OpenUniverse payloads and never reaches a child. Records use host-held values, and an echo mismatch is `PROVIDER.PROTOCOL_VIOLATION` (NE:2854–2856). The ExecutionId reading matches J1 item 2: for a durable attempt it is reserved at `CommitSession::open` before any provider frame, and that reservation is distinct from OPP §5.5’s attempt row.

**Fix.** Keep the four names as the correlation identities that cross the wire, and name the protocol members the contracts already require beside them: Hello and HelloAck identity members, `planIntentCommitment`, `providerId`, the universe object, and Rust `repositoryResolution`. Keep the prohibition on RequestId, RunId, ProjectId, a log path, and any identity the two protocols do not already carry. In X10, except J1:192: the next J1 revision re-reads that substitute against the corrected inventory. r1:377 stays the historical sentence.

## Dependence on O7 and S-M

The section “What depends on O7 and S-M” (lines 91–110) is complete for the outcomes it names, with the joint-measurement gap in NBO-2.

**S-M.** Item 9 depends on it entirely: every `⟨SM-n⟩`, the derived F and T, and outcome (A), (B) or (C). These depend on it only conditionally:

- O3 arises on (B), and O4 on (C);
- X6, and the D law’s liveness floor, are sized by SM-8;
- SM-6 may raise a TS2 limit question, which only a successor can answer (item 1);
- SM-5 and SM-6 decide whether MC’s conditional S-R is needed.

No other item’s text depends on the measured values. Under every listed outcome, items 1 and 2 keep TS2 and Rust3 one-shot for M3. A D5 staging change from O3 or O4 is the owner’s decision outside this law. This law would need a delta round only to change M3’s protocol, which item 1 forbids without a successor.

The unlisted case is F over 2 s and T over a medium budget together. Item 9 records one outcome. Both (B) and (C) then apply, and both O3 and O4 should be raised. That is a label in the delta round. It does not change the protocol text. See NBO-2.

**O7.** No item’s text depends on which way O7 is decided. O7 decides when this law takes effect (G9) and when a provider may launch (item 17; `M3-PLAN-r6.md:476`). A delta round is needed only if the decision lets a provider execute repository code, needs a new wire signal or member for confinement, or changes item 2 into a resident or pooled helper. Under the lead’s recommendation none of those arises. CF-2’s disclosure carrier sits beside Coverage (`M3-PLAN-r6.md:504`). CF-P is evidence for the owner (G9), and CFP:3 claims nothing as enforced.

## Review and effect

The review rule is sound. Early review is allowed. An ACCEPT is “accepted in review” and satisfies no dependent gate. Dependents’ “M3-L accepted” means L in effect: accepted in review, every gate item met, and every delta round accepted. That reading preserves the sense those dependents were written against, when acceptance itself waited for the gate.

Checked anchors:

- `M3-PLAN-r6.md:255`: “Day 0 is M3-L’s acceptance. Because O7 and S-M are in L’s gate, both are done by then.”
- `M3-PLAN-r6.md:378` is the bullet “L acceptance (about 2, once its gate is met).” Line 377 is X4-F1. The citations at lines 53 and 694 resolve.
- MC’s pinned gate (PROPOSAL-r6.md:88–89): review is allowed now; acceptance requires “M3-L is accepted”; an unchanged draft is not acceptance. The quoted “MC header” sentence is the live recording paragraph. See NBO-1.
- The D law’s gate note (its line 55 and its units line) treats day 0 as L’s acceptance and holds product units until M3-L is accepted. Under this rule that means L in effect.
- The overnight entry “Lead decision: M3-L gets an early review round” is present.

X9’s treatment of `M3-PLAN-r6.md:445` and `:426` is right. Those lines still say L is sent only after S-M, the two sign-offs and O7, and that r2 fills `⟨SM-n⟩` after S-M. This law must not edit the accepted plan. Day 0 stays “after the gate”. The also-stale Seatbelt line at `:524` predates CF-P, and X9 names it.

## Gate

| Row | Judgment |
|---|---|
| G1 | Open. No S-M report. P5-8 at `:593` still places S-M after X4-F1. The overnight log records the X9-6 rerun and F8b bound. |
| G2 | Met. T2b accepted; T2R:24 is 49 repositories, 5 workspaces, 33 families. |
| G3 | Met. Preserved `DESIGN-r13.md` is 151216 bytes, sha256 `37438317…`. The live file is the pinned `1f108399…` and its line 3 records that acceptance and schema `71f682d1…`. |
| G4, G5 | Open owner items. AQP:543 and AQP:554 are still `proposed`. |
| G6 | Met on the stated reading. Q0 §2 (HD:276–300) is the accepted rule-catalog draft, and the M3-Q0 row says the accepted record includes those specs (AQP:175–199). AQP:542 is the placement sign-off, which the gate text does not require. R7 discloses the other reading. |
| G7 | Met. S-OP-2 r6 is the pinned accepted bytes. The plan’s own G7 row at `:441` still says r4 is in review; this law’s row is the current one. |
| G8 | Lawfully decided in item 11. The plan already records that (`:442`, `:463`) and makes it final when L is accepted. Under the review rule, final means at effect. |
| G9 | Open owner decision. CF-P is cited as evidence. CFP:3 claims nothing as enforced. The macOS verdict (CFP:231–264) and the AL2023 desk check (CFP:309–315, kernels 6.1.147, 6.12.40, 6.18 and later) match the summary, including the five profile amendments and the `kern.procargs` denial. |

## Protocols, reuse, records, cancel

Items 1 and 2 add no frame, member, phase, terminal, token, limit or identity version. Cardinality matches DLV:556–567 and F02:222–224 and F02:268–269. Syntax universes have no child (ME:764; MC item 9). A child starts after MC row 15 (MC:867, “before any provider”), in J1’s J-ζ after J-ε. J1’s own pin of that row is the older M3C:836; this law’s MC:867 is the r6 line.

Item 3’s “none ships at M3” matches the accepted plan at `:469`. The INC table matches the requested split: a D5a IE successor before cross-edit reuse (INC-1), protocol-lifetime successors and a DR-G10 acceptance successor before M5 residency (INC-6), and pure law for INC-2, INC-3, INC-4, INC-5, INC-7 and INC-8. No D5a successor is needed for this law to take effect. AQP:387 is the condition the law must be able to satisfy; AQP:546 sends a contract change through D5a when a feature needs one.

Item 4 holds on the lines cited. `cache2` binds the Plan through `stage-spec.planId` (IE:195, IE:1288–1293). Every `scopeIds` member is a subject-scope of this snapshot (IE:1617–1618). A source edit changes `snapshot2` and therefore `plan2` (IE:179, IE:182). Same-Plan regeneration is the hit IE allows (IE:1599–1608). Equal content digests are not authority (IE:1614–1615). Stripping `planId` by host convention is the hidden second recipe IE:1291–1292 forbids. No other lawful cross-edit route is open under IE as written.

Items 5–8 restate AQP:389–407, including INC-3’s seven classes and INC-6’s residency obligations. The 2 s, 30 s and 8 s figures are the owner targets at AQP:385 and AQP:377. SM-1 through SM-10 are the right figures. SM-5 and SM-6 report the MC item 5 bounds (100,000 rows, 4 MiB, about 27,000 rows in 4 MiB, 8 GiB). SM-10’s unit is SOP2:910 (`bytes` on macOS, `kib` on Linux) plus the checked conversion. The workloads match the manifest: `counts.rust.medium.devIds` has 7 entries, `counts.tsjs.medium.devIds` has 6, `poly-medium-napi-rs` is in both, `mr-rs-medium-serde-json` is the extra workspace at T2R:198, and the held-out set at T2R:76 is outside those lists. F and T are the sums item 9 defines. Item 10’s `host.reuse.disclosed`, per stage and universe, is SOP2:873, and the syntax stages are in scope because they have no child.

Items 11 and 12 hold. Counting stderr to EOF and keeping `{bytes, truncated}` is the reduction SOP2:837 and K7 already store; DLV:1133’s host-owned marker is `truncated: true`; both bounds are 262,144 (NE:2967, RPP:117). OPP:171 still says the host holds the text; X11 routes that wording, and the D r1 review’s NBO-1 already called the count lawful. `detailCode` is SOP2:844’s empty K3 table, so a later G-unit member stays a diagnostic label inside item 1. Progress is host-counted validated frames; DLV:1517 admits facts only after Complete, matching commitments, zero-exit and EOF. Liveness is `health` / `healthReport` / `resourceReport` (CC:33–35), and the window stays above SM-8 without embedding SM-8’s number. The SDK names at DRC:556–566 bind V1 payloads; re-binding them to the TS2 payloads is a record-join question (R2), and item 12.5 adds no operation.

Item 14’s table matches SOP2:864–894, including `supervision.progress.absent` for OPP:238’s `supervision.no_progress`, empty `detailCode`, the stderr reduction, and `host.reuse.disclosed`. The law needs no event S-OP-2 r6 does not register. SOP2:1006 is the same native-unit prohibition item 9 forbids.

Item 15’s M3 point is the two handshake checks (NE:2824–2834, NE:2973–2984). `installation.rs` is the first DR-G14 owner (COV:4771–4773) and is listed at M5 (COV:8976). The gate milestone at COV:4770 is M3. Building the module stays at M5, with the plan at `:467`.

Item 16 holds as disclosed lead decisions.

- Stage 1 is in-band `Cancel` with `user-interrupt`, then control `cancel` reason `user` (DLV:860, RPP:451, CC:37). The in-band frame goes first.
- DLV:860 also admits `host-shutdown`, and that string appears only there. Rust `CancelV2.reason` is exactly `user-interrupt`. Never sending `host-shutdown` at M3 is host policy. It removes no protocol member. The two languages stay aligned, and NE:3837–3843 admits nothing from a cancelled child.
- Rust’s 5,000 ms member is a retained limit checked by exact equality (RPP:119, RPP:134, NE:2929–2941). Reading it as the stage-1 wait is the reading J1 8.5 already adopts. v4 line 966 names the member on a guard context path. R9 correctly leaves the guard that consumes it to the Rust protocol owner. TS2 has no grace member; the provisional 2 s is the D law’s constant (OPP:329).
- The forced stage, `interrupted` 130, no facts and no Run match DLV:1122, DLV:1146, DRJ:1036–1051 (`interrupt-before`), NE:3424–3425, NE:3842–3843, WS:229, and J1’s phase-A/B outcome row.
- TypeScript after `Cancelled` goes to EOF (T2O:261–266). Rust goes to zero-exit, then EOF (P3T:342–364). `observedPhase` is unchanged (NE:3296–3302).
- J1:500 places providers in phase A, through `prepare_commit` returning the attempt row, including the whole analysis. r1’s “provider part of phase B” is withdrawn. The commit-phase join stays J1 item 8.
- CPC is `CANDIDATE-NOT-APPLIED` and binds nothing (CPC:7, CPC:10). CC:9 calls it the accepted authority. T-1 (CPC:659–663) is the split this item adopts as its own lead decision, with R1 asking the DR-102 owner. J-1 orders the two carriers (CPC:466–472). J-5 starts teardown with `shutdown` or `cancel` (CPC:489–492). That adoption is disclosed. It does not claim CPC resolved T-1.

Items 17 and 18 state no launch rule and decide no commit-phase join. Citing the D law by role is adequate while its header can still gain an acceptance note (NBO-3). The three requirements in item 17 are cardinality, no launch before O7 and D1, and `workerExecutesRepositoryCode` false (NE:2534–2535).

Items 19–21 match the records and change no standing.

- REG:355 is the historical TS major 1 / Rust major 2 row with harness `harness.DR-G10.provider-conformance.ts-major-1`. QG `items[9]` is DR-G10, acceptance text and harness `harness.DR-G10.product-v1` as item 19 quotes, standing “DESIGN-CONTRACT-ACCEPTED; REQUIRED PRODUCT QUALIFICATION UNPERFORMED”. COV:4659–4661 selects `/items/9` with `valueSha256` `1313c85d…`. Qualification stays M6 (COV:4675). COV:4679 keeps the old claim as `inheritedAcceptance`. REG:342 already says G10 uses TS major 2 and Rust major 3.
- F02:220 says TypeScript major 1, and F02:259 says Rust major 2. The structural rules at F02:222–224, F02:268–269 and F02:271–273 still bind. Current majors are NE:2785 and QG:202.
- NE:4203’s heading still says independent Claude review pending. The current NE bytes (`83b99783…`, 329013 bytes) are in `candidate-subject.v45.json`, and QG:212–215 cites `claude-independent-design.v45` for DR-G10. Item 21 claims that review status for these bytes and leaves §14’s read scope at R6.
- RH:29–48 pins the register through `design-lock.json` and the D-372 manifest, and pins F02 through the manifest. None of the three notes is applied in place. Contract text under `docs/v2/contracts/` stays unedited.

`git diff --name-only 2967905 e093e90` in the product tree does not list `Cargo.toml`, `providers/rust/src/main.rs`, `crates/contracts/src/generated/protocol.rs`, `schemas/wire/native-carriers-v1.json` or `crates/lifecycle/src/installation.rs`.

## Joins and cross-law findings

The joins table is true on the bytes read. S-OP-2 r6 registers every event item 14 names, and SOP2:1041’s R9 is the SM-10 unit item 9 now states. J1 item 2, J-ε, J-ζ, item 8, 8.5, and the fault and signal outcome rows agree with items 5, 13 and 16, apart from RF-1’s closed set. MC item 20’s INC claims are unchanged by r2. X12 r4:244’s pack refusal reaches no provider. X2 r9 supplies the project-admission phase item 13 uses for ProjectId. MB r2 cites r1:494–509, which is item 17. ME §G and item 16’s in-host syntax reason match item 2.

X1 through X12 name a real record and an owner. X3, X5 and X9–X12 ask for later revisions of OPP, the D law’s manifest record, the plan, J1’s re-pin, and the Rust protocol owner’s answer on `maxPreparedOutputEntries` 256 (RPP:102, RPP:385). R10 leaving that question open is right: NE:2934 retains the v2 limit, and this law changes no limit. X8’s citation re-pin is the plan’s row 12 (`:64`) and the M3-L row’s AQP:389–409 cite (`:207`). No accepted law is rewritten in place. X10’s “no content change” needs the J1:192 exception in RF-1.

Nothing else on the decide list needs the owner beyond the questions the law already flags (O1–O4, R1–R11).

## Non-blocking observations

**NBO-1.** Lines 47 and 122 attribute the effect sentence to the MC header. It is the live file’s recording paragraph. The pinned gate at MC:88–89 is the text that supports the rule.

**NBO-2.** Item 9’s single outcome does not name the case where F and T both miss. Record both (B) and (C).

**NBO-3.** GROK2 has accepted the pinned D-law bytes in review. The D file and this law still say draft. Role citation stays the right form until an acceptance note exists.
