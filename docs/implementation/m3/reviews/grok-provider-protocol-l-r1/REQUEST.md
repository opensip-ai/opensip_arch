**STATUS: DRAFT REQUEST, NOT SENT.** Send this only once the M3-L acceptance gate permits, that is, when gate items G1-G9 of the subject are met or each is explicitly accepted as pending by the lead. The items are listed in the subject's "Acceptance gate" section and in `docs/implementation/m3/M3-PLAN.md:160`. At drafting (2026-10-03) these were open:
- G1, S-M measured;
- G2, T2b;
- G4, D3 sign-off;
- G5, D13 sign-off;
- G7, S-OP-2 drafted;
- G9, O7 decided by the owner.

**Before sending**, the lead:
1. revises the subject to fill every `⟨SM-n⟩` placeholder from S-M's report, records item 9's outcome, and updates the gate table (the review subject is then r2 or later; preserve r1 as `PROPOSAL-r1.md`);
2. writes `hashes.txt` (sha256, bytes, path) and `status.json` in this directory;
3. updates the subject line below and the product HEAD;
4. commits ("Assign M3-L rN to Grok.");
5. sends this request with `herdr agent prompt w2:p1 …`.

Until then this file is a draft, and no hash or status exists.

---

Grok review: law **M3-L**, the M3 provider-protocol and reuse law (`docs/implementation/m3/provider-protocol-l/PROPOSAL.md`). It is the law that fixes the M3 provider protocol before providers are built. Claude Opus 5.5 leads. You review **facts and law**: every citation, every contract reading, and whether each decision is sound and complete. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/grok-provider-protocol-l-r1`.

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation.
- **This is a law review.** Run no product cargo and no tests. The lead keeps the native lane.
- **Never touch the real home.** Never read the 413 fixture.

**Subject:** `docs/implementation/m3/provider-protocol-l/PROPOSAL.md`, revision rN. Its sha256 and bytes are pinned in `hashes.txt`. Product: `/Users/sb/code/opensip-ai/opensip`, main `<HEAD at send time>` (`2967905` at drafting).

**What it builds on:**
- **The accepted plans:**
  - `docs/implementation/m3/M3-PLAN.md` r4: the M3-L, M3-D, M3-S and M3-J rows, "O7", and "Choices left open";
  - `docs/implementation/m3/analysis-quality/PLAN.md` r6, §5.3 INC-1 to INC-8 (lines 383-409);
  - `docs/implementation/m3/operability/PLAN.md` r3: §3.1, §3.6, §4.1, §5.5, §8 and §9;
  - `docs/implementation/m3/harness/DESIGN.md` r13: §9.4 and §11, and its envelope schema.
- **The contracts:** `docs/v2/contracts/product-v1/native-evidence.md` §9 (lines 2781-3313), `identity-and-evidence.md` (lines 179-196, 1288-1301 and 1580-1629), `workflows-and-surfaces.md` §1, `security-and-lifecycle.md` and `admission-and-qualification.md`.
- **The protocol artifacts the subject cites:**
  - `docs/coop/artifacts/{delivery.v2,rust-provider-protocol.v2,rust-provider-protocol.v4,delivery-rust-provider-join.v4,control-protocol-contract.v2}.json`;
  - `docs/coop/completion/{control-completion.contract.v5,distribution-runtime-completion.v2}.md`;
  - `docs/coop/design-corrections/native/{protocol3-transitions.v1,typescript-protocol2-order.v1}.json`.
- **The gate and records:**
  - `docs/coop/design-corrections/qualification-gates.applied.v1.json` items[9];
  - `docs/v2/architecture/implementation-coverage.v1.json` (DR-G10 and DR-G14);
  - `docs/v2/architecture/08-decision-and-readiness-register.md:342` and `:355`;
  - `docs/v2/architecture/02-distribution-and-components.md`;
  - `docs/implementation/m3/record-hygiene/PROPOSAL.md` §2.

## Decide

1. **The gate table.** Is each gate item's status true at send time, with its evidence? Is G6 met by Q0 §2's catalog draft specs (open question R7)? Is O1 lawfully decided inside this law (G8)?
2. **Items 1-2: TS2/Rust3 unchanged, and one child per universe.** Does any item add, remove or reinterpret a frame, member, phase, terminal, token, limit or identity version? Are the cardinality, start and end rules exactly DLV's and F02's?
3. **Item 3 and the INC table.** Is "none ships at M3" sound? Is each INC item's classification right?
   - **D5a successor needed:** INC-1, before cross-edit reuse; INC-6, before M5 residency.
   - **Pure law:** INC-2, INC-3, INC-4, INC-5, INC-7 and INC-8.
   - Is it true that no D5a successor is needed for M3-L's acceptance?
4. **Item 4, the central finding.** Check the claim that under IE as written no cache entry can hit across a source edit:
   - `cache2` binds the Plan through `stage-spec.planId` (IE:195, IE:1288-1293);
   - `scopeIds` must be subject-scopes of this snapshot (IE:1617-1618);
   - an edit changes `snapshot2` and `plan2` (IE:179, IE:182).

   Is there any lawful cross-edit reuse route that the subject missed?
5. **Items 5-10, INC-2 to INC-8.** Is each obligation stated faithfully to AQP:389-409? Are the forbidden substitutes complete? For item 9:
   - Are the S-M figures SM-1 to SM-10 the right ones?
   - Are the derived F and T sound?
   - Are outcomes (A), (B) and (C) compared only against owner-approved targets (AQP:372-385), with no invented number?
   - If the placeholders are filled, are the values taken from S-M's report and labelled preliminary?
6. **Items 11-12: O1(a) and the S-OP-4 record join.**
   - The stderr and `fault` dispositions: are the 262,144-byte bounds right for both languages?
   - Progress from host-admitted transitions, not fact admission (DLV:1517).
   - Liveness through `health`/`healthReport`/`resourceReport`, and the synchronous-compiler exposure (SM-8, X6).
   - The SDK alias re-binding from V1 to TS2 (DRC:556-566): is a record join enough (R2)?
7. **Item 13: RequestId and phase-lawful identities.** Is it right that no identity beyond `executionId`, `snapshotId`, `planId` and the universe key crosses the wire? That RequestId never reaches a child? That records use host-held values only?
8. **Item 14: the operational record.**
   - Do the span boundaries and fields meet Q0 §9.4 and ENV `operationalRecords` (`carriesReuseDisclosure`, `carriesProcessMaxRss`)?
   - Is the list of events for S-OP-2 complete?
9. **Item 15: DR-G14 placement.** Are the handshake identity checks (NE:2824-2834, NE:2973-2984) the right M3 enforcement point, with `installation.rs` at M5?
10. **Item 16: the two-stage cancel.** This is the most contract-sensitive item. Check:
    - (a) the in-band `Cancel` followed by control `cancel {user}`, and the in-band-first ordering;
    - (b) in-band `Cancel` only for user interruption (RPP:451; DRJ:1850);
    - (c) the per-protocol stage-1 grace: Rust3's `cancellationGraceMilliseconds` 5,000, against OPP's provisional 2 s for TS2. Is the reading of that member as a wait, not only a ceiling, right (R9)?
    - (d) the forced stage;
    - (e) `interrupted` 130, no facts and no Run (DLV:1122, DLV:1146, DRJ:1036-1051, NE:3421-3426, NE:3837-3843, WS:229);
    - (f) the scope boundary to S-OP-12 and M3-J.

    Is adopting CPC's T-1 split as a lead decision lawful, given that CPC calls T-1 unresolved and is itself `CANDIDATE-NOT-APPLIED` while CC:9 calls it the accepted authority (R1)?
11. **Items 17-18: boundaries.** Does any sentence state a launch rule (which is the D law's) or presume an O7 outcome? Does any sentence decide the commit-phase join (which is S-OP-12's)?
12. **Items 19-21: record corrections.**
    - **DR-G10.** REG:355 against QG items[9] and COV:4656-4681. Is the selector correction exact, and does it change no gate row, threshold or standing?
    - **The stale majors** at F02:220 and F02:259.
    - **NE §14's heading.** Is the evidence that the current NE bytes were in the v45 review's subject sufficient for what item 21 claims, and no more?
    - Is it right that none of the three may be applied in place, because of the design-lock and D-372 pins?
13. **The cross-law findings X1-X8 and the open questions.** Are they real and correctly routed? Is anything missing that needs the owner?
14. **Anything else** wrong or missing.

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: an array, empty on ACCEPT. Each finding has `id`, `location`, `problem`, `evidence` and `fix`;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: the subject's sha256 as pinned in `hashes.txt`.

This is a law (PROPOSAL) review, so the `verify_design` unit shapes do not apply. A contract successor would need `ACCEPT-DESIGN-UNIT` with a single-string `subjectManifestSha256` matching its own subject. An inventory unit would need `ACCEPT-UNIT` plus `inventoryCandidateAssessment`. This subject is neither, so use the law verdicts above.

Do not commit.
