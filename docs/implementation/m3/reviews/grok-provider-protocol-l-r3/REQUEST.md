Grok review: law **M3-L r3**, the M3 provider-protocol and reuse law. This is a **law and contract-soundness** review, round 3, and still an **early round**: the law's gate is not met. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT**, recorded as "accepted in review" and effective only when the gate is met, or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok-provider-protocol-l-r3.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git only read-only.
- No product builds or test runs, and no cargo: a timing-sensitive crash-matrix lead set may be using this machine.
- Never touch the real home (`~/Library/Application Support/OpenSIP`).
- Never read the private 413 UUID fixture.
- Use read-only scratch scripts under your review directory if you need them, at `nice -n 19`.

## Subject

The pins are in `hashes.txt`.
- **The subject:** `docs/implementation/m3/provider-protocol-l/PROPOSAL.md`, the r3 law. It is the subject of `subjectSha256`.
- **For diffing:** `docs/implementation/m3/provider-protocol-l/PROPOSAL-r2.md` (`5bd4025e…`), the exact r2 bytes you reviewed, and your r2 review (`reviews/grok-provider-protocol-l-r2/REVIEW.md`, `review.json`). The subject's "r3 changes" table lists what moved. Review the diff closely and the rest for consistency.
- **What r3 joins, new this round:**
  - **FA-2**, the native contract successor for M3-H's X-H1, in review with Codex at the same time (`reviews/codex-fa-2-r1`). Its package is `docs/implementation/m3/native-successors-fa/fa-2/`: `README.md` (the design and its lead decisions LD-F1 to LD-F9), `section-9-8.md` (the NE §9.8 text it appends) and `successor.json` (every override). **You are not reviewing FA-2.** Review L's join to it: item 1, item 13's FA-2 entry, item 22, G10, and the third delta-round trigger.
  - **M3-H r1** (`fact-admission-h/PROPOSAL-r1.md`, `69f50bb1…`), which you reviewed. Its X-H1 (H1:724-732) and X-H4 (H1:741) are what r3 answers. H's r2 is being drafted in the live file and is **not** cited; do not review it.
  - **M3-D r3**, now accepted by GROK2 (`supervisor-d/PROPOSAL-r3.md`, `9679dbc4…`), and **M3-J1 r4**, now accepted by GROK2 (`host-pipeline-j/PROPOSAL-r4.md`, `c18c0d3c…`).
  - **I1-L**, accepted by CODEX2 and bound at product `0ceb9ad`.
- **Accepted laws it keeps joining** (each at its accepted snapshot): S-OP-2 r6, M3-J1 r3, M3-C r6 (in review; its gate is MC:88-89), M3-E1 r3, M3-I1 r2, M3-B r2, X12 r4, X2 r9, and M3-PLAN r6.
- **Plans** AQP r6, OPP r3 and Q0 r13 are still cited at their live files, as in r2. Each live file is exactly its snapshot plus a two-line note after line 1 (live n = snapshot n − 2), and both are pinned.
- **Contracts and protocol artifacts:** NE §4.1a and §9 (lines 1876-1998, 2781-3316), IE, DLV, RPP, CPC, CC, the native handshake and startup schemas, NCM, and the foundation ENC, EXC, SIS and RPS. None changed since r2.
- **The product:** `/Users/sb/code/opensip-ai/opensip`, read-only. The assigned base is main `e093e90`. Main is now `15c0779` (the I1-L, B-S1, B-S2 and B-S9 bindings, and X4-F1). `git diff --name-only e093e90 15c0779` lists none of the product files this law cites.

## What r3 changes

1. **RF-1 (item 13).** The four correlation identities stay. Beside them, item 13 now names every identity-bearing member the contracts already put on the wire, per protocol:
   - Hello and HelloAck, including the members item 15 checks;
   - each OpenUniverse payload's members: TS2 `universeKey`; Rust3 `repositoryResolution` with its set ids, `authorizationId` and `effects`;
   - the later echoes;
   - FA-2's two members, under its token.

   The prohibition stays: no RequestId, RunId, ProjectId, log path, or identity the protocols do not carry.
2. **J1:192.** X10 is corrected. **X14** records that J1's next revision re-cites item 13; J1 r4:207 carries the same sentence. It is deliberately **not** folded into J1 r4, which is accepted.
3. **NBO-1.** "Review and effect" cites MC:88-89, the pinned gate.
4. **NBO-2.** Item 9 records every outcome that holds. (B) and (C) together raise both O3 and O4.
5. **NBO-3.** M3-D is accepted at r3, in the short name, item 17 and the joins row, and is still cited by role. R8 is closed.
6. **X-H1 (lead decision).**
   - New **item 22** joins FA-2's carrier as proposed: what crosses the wire, when it is admitted, and how INC treats it.
   - **G10, FA-2 accepted, is added to the gate.**
   - Item 1 names FA-2 as the one protocol change M3 makes. It is a native successor, not this law's.
   - Item 10 covers the census.
7. **X-H4 (item 5).** "No host-minted facts without a producing frame" gains an exact exception: a Plan-selected in-core producer stage. There are exactly two: E1's syntax stage, and H's host inventory derivation, which in a TS or Rust universe still waits for H's X-H3. Host projections of an admitted frame (`TargetAttributionV2`, FA-2's inventories) are stated not to be host-minted.
8. **New cross-law items:**
   - **X13:** Rust3's retained `maxSubjectsPerStage` 256 refuses before spawn any snapshot with more than 256 non-empty `.rs` files. By T2's counts that is 9 of 22 Rust entries, including S-M's `rs-medium-axum` and `rs-medium-tokio`. Routed to the Rust protocol owner (R12) and not decided.
   - **X15:** the inherited key-commitment rules conflict with NE §4.1a for every key. FA-2 closes it.
   - **X16:** FA-2's follow-ups for H, C, D, F, G and the plan.
9. **"What depends on O7, S-M and FA-2"** adds FA-2, the joint case, and a summary table built on your `gateDependence`.

## Decide

1. **RF-1.** Is item 13's inventory now exactly what the contracts put on each protocol's wire (NE:2816-2835, NE:2955-2981, NE:3158-3191; DLV `AnalyzeV1`, `FactCandidateV1`, `CoverageKeyV1`, `CancelV1`; RPP:441-457)? Is anything missing or extra? Does it still keep RequestId, RunId and ProjectId off the wire?
2. **X14.** Is routing J1's re-citation to J1's next revision, outside J1 r4, the right treatment? Is X10's correction right?
3. **NBO-1 to NBO-3.** Are they answered?
4. **The FA-2 join.**
   - Is item 22 a complete and lawful join: what crosses, when it is admitted (at D3's clean settlement, atomically, in H's order), and how INC-1 to INC-4 and INC-8 treat it?
   - Is item 1's statement right that FA-2 changes no frame, phase, terminal, limit, identity version or major?
   - Is G10 a lawful addition to the plan's gate row (`M3-PLAN-r6.md:207`)?
   - Is the third delta-round trigger right?
5. **X-H4.** Is item 5's exception exact, with exactly two named in-core stages, each with a Plan-selected producer, and no wider? Is "host projections of an admitted frame are not host-minted" right?
6. **Dependence. State explicitly which parts depend on O7, which on S-M's figures and which on FA-2.** Is the section, and its summary table, complete and correct?
7. **X13 and X15.** Are the findings true on the cited bytes (RPP:106, RPP:226-231; NE:2929-2941; NE:136; NE:1927-1945; NE:3279; DLV `coverageDomain.keyConstruction`, `RequestedCoverageDomainV1.workerRule`; RPP `coverageDomainAlgorithm`)? Is not deciding X13 here right?
8. **Anything else** r3 changed that is wrong, or any r2 text r3 left stale.

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`. An ACCEPT is recorded as "accepted in review". The law takes effect only when G1, G4, G5, G9 and G10 are met and S-M's delta round is accepted;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256;
- `"gateDependence"`: `{o7, sm, fa2}`, as in your r2 review.

This is a law review, not a `verify_design` unit. FA-2 is reviewed separately by Codex. Do not commit.
