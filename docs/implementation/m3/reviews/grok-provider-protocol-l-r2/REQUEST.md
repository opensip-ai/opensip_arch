Grok review: law **M3-L r2**, the M3 provider-protocol and reuse law. This is a **law and contract-soundness** review, and an **early round**: the law's gate is not yet met. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT**, recorded as "accepted in review" and effective only when the gate is met, or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok-provider-protocol-l-r2.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs, and no cargo: a timing-sensitive crash-matrix lead set may be using this machine.
- Never touch the real home (`~/Library/Application Support/OpenSIP`).
- Never read the 413 fixture.
- Use read-only scratch scripts under your review directory if you need them.

## Subject

The pins are in `hashes.txt`.
- **The subject:** `docs/implementation/m3/provider-protocol-l/PROPOSAL.md`, the r2 law. It is the subject of `subjectSha256`.
- **For diffing:** `docs/implementation/m3/provider-protocol-l/PROPOSAL-r1.md` (`5e858c05…`), r1's bytes. r1 was drafted on 2026-10-03 and never sent, so **no revision of this law has been reviewed before**. Review the whole law, not only the diff. The subject's "r2 changes" table lists what moved.
- **The plan:** `docs/implementation/m3/M3-PLAN-r6.md`, the accepted r6 bytes (`a6956e88…`). The M3-L row is line 207 there (line 209 of the live `M3-PLAN.md`, which carries a 2-line acceptance note). The subject cites every plan line as `M3-PLAN-r6.md`:n.
- **Accepted laws it joins** (each cited at its accepted snapshot):
  - S-OP-2 r6, the event vocabulary: `operability/s-op-2/PROPOSAL-r6.md`;
  - M3-J1 r3, the host pipeline: `host-pipeline-j/PROPOSAL-r3.md`;
  - M3-C r6, accepted in review: `snapshot-plan-c/PROPOSAL-r6.md`;
  - M3-E1 r3, the syntax law: `syntax-e/PROPOSAL-r3.md`;
  - with minor or no joins: M3-I1 r2, M3-B r2, X12 r4 and X2 r9.
- **A draft and a record:**
  - the D law, `supervisor-d/PROPOSAL.md`: M3-D, a draft under GROK2's review (r3 at this writing), not accepted. The subject cites it **by role, not by line**, because it is changing. Its bytes are pinned so that you can see what was read.
  - CF-P's record, `confinement-cf/CF-P-RECORD.md`.
- **Plans:** AQP r6 (§5.3, lines 383-409), OPP r3 (§3.1, §3.6, §4.1, §5.5, §8, §9), Q0 r13 (§9.4, §11) and its envelope schema. None has changed since r1.
- **Contracts and protocol artifacts**, unchanged since r1:
  - `docs/v2/contracts/product-v1/native-evidence.md` §9 (lines 2781-3313), `identity-and-evidence.md` (lines 179-196, 1288-1301 and 1580-1629), `workflows-and-surfaces.md` §1, `security-and-lifecycle.md` and `admission-and-qualification.md`;
  - `docs/coop/artifacts/{delivery.v2,rust-provider-protocol.v2,rust-provider-protocol.v4,delivery-rust-provider-join.v4,control-protocol-contract.v2}.json`;
  - `docs/coop/completion/{control-completion.contract.v5,distribution-runtime-completion.v2}.md`;
  - `docs/coop/design-corrections/native/{protocol3-transitions.v1,typescript-protocol2-order.v1}.json`;
  - `docs/coop/design-corrections/qualification-gates.applied.v1.json` items[9]; `docs/v2/architecture/implementation-coverage.v1.json` (DR-G10, DR-G14); `docs/v2/architecture/08-decision-and-readiness-register.md:342` and `:355`; `docs/v2/architecture/02-distribution-and-components.md`; `docs/implementation/m3/record-hygiene/PROPOSAL.md` §2.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `e093e90`, read-only. The subject says that no product file it cites changed after r1's `2967905`.
- **Not pinned:** the overnight log, `docs/implementation/OVERNIGHT-2026-10-03.md`. It is live, and the subject cites it by entry.

## What r2 changes

1. **Review and effect (lead decision).**
   - Early review is allowed.
   - An ACCEPT is "accepted in review". The law takes effect only when every gate item, G1 to G9, is met, as M3-C r5 and r6 do.
   - Filling `⟨SM-n⟩` (with item 9's outcome), and any change O7 forces, go through a delta round.
   - Where a dependent names "M3-L accepted", that means L in effect.
   - **Rejected:** waiting for the gate before any review.
2. **The gate.** G2, G3 and G7 are MET. G4 and G5 are owner items (B3). G9 is an owner item (B1), with CF-P cited as evidence only. G1 (S-M) is NOT STARTED. G6 is met on the lead's reading, and G8 is decided in item 11.
3. **A new section, "What depends on O7 and S-M".**
4. **The S-OP-2 event check (item 14).** Each need is named as S-OP-2 r6 registers it.
5. **Joins refreshed:**
   - item 2: syntax universes have no child; a child starts after MC's pre-execution joins (J1's J-ε, J-ζ);
   - item 9: SM-10's unit, `snapshot2`'s bounds in SM-5 and SM-6, workloads from the complete T2 manifest;
   - item 10: `host.reuse.disclosed`, per stage and universe;
   - item 12.1: stderr is counted and never held (lead decision); 12.2: `detailCode` as S-OP-2's empty K3 table;
   - item 13: J1 item 2's reading of where the ExecutionId comes from;
   - item 16b: TypeScript `host-shutdown` is never sent at M3 (lead decision);
   - items 16f and 18: the commit-phase join is J1 item 8; providers are live only in phase A.
6. **Cross-law items** X9 to X12, with X3, X5 and X8 updated; new open questions R10 and R11; a "Joins checked" table.

## Decide

1. **Review and effect.** Is the rule lawful and sound? In particular:
   - Is it right that an ACCEPT in review satisfies no dependent's gate (MC's gate; `M3-PLAN-r6.md:255` and `:378`; the D law's gate note)?
   - X9 routes the conflict with `M3-PLAN-r6.md:445` ("Before L can be sent: S-M, the two sign-offs and O7") and `:426` to M3-PLAN's next revision, and does not rewrite the plan. Is that the right treatment?
2. **The gate table.** Is each row true today, with its evidence? Is G6 met by Q0 §2's catalog draft specs (open question R7)? Is O1 lawfully decided inside this law (G8)? Does G9 cite CF-P only as evidence, never as a decision?
3. **Dependence on O7 and S-M. State explicitly which parts of the law depend on O7's decision and which depend on S-M's figures.** Is the subject's section "What depends on O7 and S-M" complete and correct? Name any item whose text would have to change under some O7 outcome or some S-M outcome that the subject does not list.
4. **Items 1-2: TS2/Rust3 unchanged, and one child per universe.**
   - Does any item add, remove or reinterpret a frame, member, phase, terminal, token, limit or identity version?
   - Are the cardinality, start and end rules exactly DLV's and F02's?
   - Is the syntax-universe scope faithful to ME §G and ME item 16, and to MC item 9?
   - Is the start point right: after MC's row 15 (MC:867), in J1's join J-ζ?
5. **Item 3 and the INC table.** Is "none ships at M3" sound? Is each INC item's classification right?
   - **D5a successor needed:** INC-1, before cross-edit reuse; INC-6, before M5 residency.
   - **Pure law:** INC-2, INC-3, INC-4, INC-5, INC-7 and INC-8.
   - Is it true that no D5a successor is needed for this law to take effect?
6. **Item 4, the central finding.** Check the claim that under IE as written no cache entry can hit across a source edit:
   - `cache2` binds the Plan through `stage-spec.planId` (IE:195, IE:1288-1293);
   - `scopeIds` must be subject-scopes of this snapshot (IE:1617-1618);
   - an edit changes `snapshot2` and `plan2` (IE:179, IE:182).

   Is there any lawful cross-edit reuse route that the subject missed?
7. **Items 5-10, INC-2 to INC-8.** Is each obligation stated faithfully to AQP:389-409? Are the forbidden substitutes complete? For item 9:
   - Are SM-1 to SM-10 the right figures? Do SM-5 and SM-6 now report against `snapshot2`'s bounds (MC item 5, MC X-1)? Is SM-10's unit the one S-OP-2 labels (SOP2:881, SOP2:910)?
   - Are the workloads right: the T2 manifest's medium dev ids per language, plus `mr-rs-medium-serde-json`, with held-out entries excluded?
   - Are the derived F and T sound, and are outcomes (A), (B) and (C) compared only against owner-approved targets (AQP:372-385), with no invented number?

   For item 10: is `host.reuse.disclosed`, per stage and universe, the right carrier, syntax stages included?
8. **Items 11-12: O1(a) and the S-OP-4 record join.**
   - **12.1.** Is counting stderr without holding it lawful against DLV:1133 and OPP:171? Are the 262,144-byte bounds right for both languages?
   - **12.2.** Is `detailCode` as S-OP-2's empty K3 table right? Does a member the G unit adds later stay within item 1?
   - **12.3.** Is progress derived from host-admitted transitions, not from fact admission (DLV:1517)?
   - **12.4.** Liveness through `health`/`healthReport`/`resourceReport`, and the synchronous-compiler exposure (SM-8, X6).
   - **12.5.** Is a record join enough for the SDK alias re-binding from V1 to TS2 (DRC:556-566; R2)?
9. **Item 13: RequestId and phase-lawful identities.**
   - Is it right that no identity beyond `executionId`, `snapshotId`, `planId` and the universe key crosses the wire, that RequestId never reaches a child, and that records use host-held values only?
   - Is the adoption of J1 item 2's reading right: the ExecutionId is reserved at `CommitSession::open` (R12) for a durable attempt, distinct from OPP §5.5's "attempt admitted" (the attempt row)?
10. **Item 14: the S-OP-2 event check.** Check each row of item 14's table against SOP2:864-894.
    - Is every need registered, under the stated name and with the stated fields?
    - Is the reconciliation of OPP:238's `supervision.no_progress` with the registered `supervision.progress.absent` right (X11)?
    - Does the law need any record that S-OP-2 r6 does not register?
11. **Item 15: DR-G14 placement.** Are the handshake identity checks (NE:2824-2834, NE:2973-2984) the right M3 enforcement point, with `installation.rs` at M5?
12. **Item 16: the two-stage cancel.** This is the most contract-sensitive item. Check:
    - (a) the in-band `Cancel` first, then control `cancel {user}`; TypeScript `CancelV1` with `reason: user-interrupt` (DLV:860);
    - (b) in-band `Cancel` only for user interruption (RPP:451; DRJ:1850). DLV:860 admits `host-shutdown`. Is never sending it at M3 lawful, and sound?
    - (c) the per-protocol stage-1 grace: Rust3's `cancellationGraceMilliseconds` 5,000 against the TS2 provisional 2 s. Is reading that member as a wait, not only a ceiling, right (R9)?
    - (d) the forced stage;
    - (e) `interrupted` 130, no facts and no Run (DLV:1122, DLV:1146, DRJ:1036-1051, NE:3421-3426, NE:3837-3843, WS:229; J1 row 46);
    - (f) providers live only in phase A (J1:500), with the commit-phase join deferred to J1 item 8, and r1's "provider part of phase B" withdrawn.

    Is adopting CPC's T-1 split as a lead decision lawful, given that CPC calls T-1 unresolved and is itself `CANDIDATE-NOT-APPLIED` while CC:9 calls it the accepted authority (R1)?
13. **Items 17-18: boundaries.** Does any sentence state a launch rule, which is the D law's, or presume an O7 outcome? Does any sentence decide the commit-phase join, which is J1 item 8's? Is citing the D law by role, not by line, adequate here?
14. **Items 19-21: record corrections.**
    - **DR-G10.** REG:355 against QG items[9] and COV:4656-4681. Is the selector correction exact, and does it change no gate row, threshold or standing?
    - **The stale majors** at F02:220 and F02:259.
    - **NE §14's heading.** Is the evidence that the current NE bytes were in the v45 review's subject sufficient for what item 21 claims, and no more?
    - Is it right that none of the three may be applied in place, because of the design-lock and D-372 pins?
15. **Joins, cross-law findings and open questions.**
    - Is the "Joins checked" table true for each law?
    - Are X1 to X12 real and correctly routed, each naming the record that must change, if any?
    - Does r2 silently rewrite any accepted law anywhere?
    - Is anything missing that needs the owner?
16. **Anything else** wrong or missing.

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`. An ACCEPT is recorded as "accepted in review". The law takes effect only when its gate is met (G1, G4, G5 and G9 are open today) and S-M's delta round is accepted.
- `"subjectSha256"`: PROPOSAL.md's sha256, as pinned in `hashes.txt`;
- `"requiredFindings"`: an array, empty on ACCEPT. Each finding has `id`, `location`, `problem`, `evidence` and `fix`;
- `"nonBlockingObservations"`.

REVIEW.md must have a section **"Dependence on O7 and S-M"** that answers Decide item 3. You may also carry it in review.json as `"gateDependence"`, with `o7` and `sm` arrays of item references.

This is a law (PROPOSAL) review, not a `verify_design` unit, so use the law verdicts above. A contract successor would need `ACCEPT-DESIGN-UNIT` with a single-string `subjectManifestSha256`, and an inventory unit would need `ACCEPT-UNIT`. This subject is neither. Do not commit.
