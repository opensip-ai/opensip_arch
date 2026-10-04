Grok review: law **M3-L r4**, the M3 provider-protocol and reuse law. This is a **law and contract-soundness** review, round 4, and still an **early round**: the law's gate is not met. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT**, recorded as "accepted in review" and effective only when the gate is met, or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok-provider-protocol-l-r4.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git only read-only.
- No product builds or test runs, and no cargo: a timing-sensitive crash-matrix lead set may be using this machine.
- Never touch the real home (`~/Library/Application Support/OpenSIP`).
- Never read the private 413 UUID fixture.
- Use read-only scratch scripts under your review directory if you need them, at `nice -n 19`.

## Subject

The pins are in `hashes.txt`.
- **The subject:** `docs/implementation/m3/provider-protocol-l/PROPOSAL.md`, the r4 law. It is the subject of `subjectSha256`.
- **Also part of r4:**
  - `provider-protocol-l/evidence/wire_identities.py`, the script that derives item 13's inventory (control L-C1);
  - `provider-protocol-l/evidence/wire-identities.json`, its report, which records every source's sha256.
- **For diffing:** `provider-protocol-l/PROPOSAL-r3.md` (`6df524a4…`), the exact r3 bytes you reviewed, and your r3 review, now copied into `reviews/grok-provider-protocol-l-r3/` with status REQUIRED-FINDINGS. The subject's "r4 changes" table lists what moved. Review the diff closely and the rest for consistency.
- **FA-2** is now at **r2**, in review with Codex (`reviews/codex-fa-2-r2`; subject `native-successors-fa/fa-2-subject.json`). Codex's r1 review (`reviews/codex-fa-2-r1`) required two scoping fixes:
  - **FA2-R1-01:** the NE:1927 insertion applies to TypeScript and Rust symbol keys only.
  - **FA2-R1-02:** X-FA2-C is narrowed to TS and Rust bindings that owe the worker's census.

  r4 takes both in through its own third trigger (r4 changes row 10). **You are not reviewing FA-2.** Review L's join to it.
- **Snapshots only:** J1 r4 (`host-pipeline-j/PROPOSAL-r4.md`, accepted; re-checked), M3-C r6 (cited) and r7 (`PROPOSAL-r7.md`, in review, not cited), M3-D r3, M3-H r1 (cited as H1). M3-H r3 is in review and not cited.
- **Product:** `/Users/sb/code/opensip-ai/opensip`, read-only. The assigned base is `e093e90`, and main is now `cd5958b`.

## What r4 changes

1. **RF-1: item 13's inventory is derived, not written (lead decision).**
   - `evidence/wire_identities.py` reads the payload each frame carries from the cited schemas. The sources are the native handshake and startup schemas, `delivery.v2`, `rust-provider-protocol.v2`, NE §9.2's table, fact-plane, C-2, FactBatchV3 with the occupancy companion, and FA-2's census schema.
   - It walks every nested record and classifies every member by a closed rule set, R1 to R6.
   - The generated table is inserted verbatim between markers. The ceiling is "exactly these members".
   - It covers each point of your RF-1. It also lists members neither r3 nor your review named, among them `relationSchemaId`, anchor `contentSha256`, `dependsOn`, the request-domain commitments, the prepared `planRow`, and the `target-attribution-v2` companion ids.
2. **Control L-C1.** `python3 evidence/wire_identities.py --check` re-derives the inventory from the pinned bytes and fails on any difference.
3. **FA-2 needs no extra member:** the derived FA-2 rows are exactly §9.8's two members.
4. **RF-2: the third trigger is exact.**
   - Any forced change to a part of FA-2 that sets a wire member, a key's commitment, the admission point or the reuse treatment reopens L.
   - That includes **every FA-2 §0 row (A to D)**.
   - The parts whose change needs none are named exactly.
   - "Review and effect", G10, the dependence section, its summary table and X15 now agree.
5. **NBO-1:** ME:478. **NBO-2:** the pin base. Main is `cd5958b`; only `design-lock.json` and X4-F1's security crate changed, and the lock's register pin (`de21a7e0…`) is unchanged. **NBO-3:** item 22.3 covers every item-6 class.
6. **FA-2 r2 joined.** X16 and the M3-C joins row state the narrowed cascade. Items 1, 13 and 22 and G10 are unchanged.

## Decide

1. **RF-1.** Is the derived inventory exactly what the cited contracts put on each protocol's wire? Check:
   - the frame-to-payload map and its selecting lines;
   - the record identities (`SAME_RECORD`, `DESC_GROUP`) and the `CHILD` map, each with its quoted basis;
   - rules R1 to R6, especially what R4 and R5 admit and what `SCALAR_START` excludes;
   - whether any member is wrongly in or out.

   Rule on whether a mechanical rule set is the right form for the ceiling.
2. **L-C1.** Run it read-only. Does it re-derive item 13's table and the report from the pinned bytes?
3. **RF-2.** Is the third trigger's map of FA-2's parts complete and exact? Is "every FA-2 §0 row reopens L" right? Do the trigger, G10, the dependence paragraph, the summary table and X15 now agree?
4. **NBO-1 to NBO-3.** Are they answered?
5. **FA-2 r2's join.** Is applying trigger 3 to FA2-R1-01 and FA2-R1-02 within this round right? Do X16 and the joins row now match FA-2 r2's X-FA2-C?
6. **Dependence. State explicitly which parts depend on O7, which on S-M's figures and which on FA-2.**
7. **Anything else** r4 changed that is wrong, or r3 text it left stale.

## Running L-C1 (optional)

`nice -n 19 python3 docs/implementation/m3/provider-protocol-l/evidence/wire_identities.py --check`. It reads arch documents only and writes nothing. Without `--check` it prints the table.

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`. An ACCEPT is recorded as "accepted in review". The law takes effect only when G1, G4, G5, G9 and G10 are met and S-M's delta round is accepted;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256;
- `"gateDependence"`: `{o7, sm, fa2}`.

This is a law review, not a `verify_design` unit. Do not commit.
