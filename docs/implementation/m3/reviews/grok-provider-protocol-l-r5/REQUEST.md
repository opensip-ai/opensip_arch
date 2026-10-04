Grok review: law **M3-L r5**, the M3 provider-protocol and reuse law. This is a **law and contract-soundness** review, round 5, and still an **early round**: the law's gate is not met. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT**, recorded as "accepted in review" and effective only when the gate is met, or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok-provider-protocol-l-r5.

**Lead note (reviewer change).** Grok reviewed L r2 to r4. **GROK2** reviews r5, because Grok is busy. Grok's r2–r4 reviews are copied in their directories. The directory keeps its name. Write your output under `/tmp/opensip-implementation/reviews/grok-provider-protocol-l-r5`. Don't run cargo.


**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git only read-only.
- No product builds or test runs, and no cargo: a timing-sensitive crash-matrix lead set may be using this machine.
- Never touch the real home (`~/Library/Application Support/OpenSIP`).
- Never read the private 413 UUID fixture.
- Use read-only scratch scripts under your review directory if you need them, at `nice -n 19`.

## Subject

The pins are in `hashes.txt`.
- **The subject:** `docs/implementation/m3/provider-protocol-l/PROPOSAL.md`, the r5 law. It is the subject of `subjectSha256`.
- **Also part of r5:**
  - `provider-protocol-l/evidence/wire_identities.py`, control L-C1, now with R7 and the RUST3-LIM source;
  - `provider-protocol-l/evidence/wire-identities.json`, its report, which records each source's sha256, the key records and the key copies.
- **For diffing:**
  - `provider-protocol-l/PROPOSAL-r4.md` (`261db4b9…`), the exact r4 bytes you reviewed;
  - your r4 review, now in `reviews/grok-provider-protocol-l-r4/` with status REQUIRED-FINDINGS.

  The "r5 changes" table lists what moved.
- **New joins:**
  - **RUST3-LIM**, the Rust3 subject-list-by-reference successor for this law's X13 (R12). **GROK2 accepted it at r1** while r5 was being drafted (`reviews/codex2-rust3-lim-r1`, status ACCEPTED, a directory name kept from its CODEX2 assignment): ACCEPT-DESIGN-UNIT, no required findings, two NBOs, on the subject this law pins (`5dfd3cd9…`). It binds after FA-2. Its package is `docs/implementation/m3/native-successors-fa/rust3-lim/`. **You are not reviewing RUST3-LIM.** Review L's join to it: item 1, item 9's SM-11 to SM-14, item 13's row and condition, L-G11, the fourth trigger, X13 and R12.
  - **FA-2 r2**, still in review with Codex (`reviews/codex-fa-2-r2`).
- **Snapshots only.** Newly accepted: M3-H r3 (`fact-admission-h/PROPOSAL-r3.md`; every H1 citation is re-mapped to H3) and M3-PLAN r9 (`M3-PLAN-r9.md`). Also pinned:
  - J1 r3 and r4;
  - M3-C r6, and r7, which is not cited;
  - M3-D r3.
- **Product:** `/Users/sb/code/opensip-ai/opensip`, read-only. Main is `392499e`, CRC-1's binding after `cd5958b`, which changed only `design-lock.json` (r5 changes row 12). Both locks are pinned.

## What r5 changes

1. **RF-1: rule R7 (lead decision).**
   - **The rule.** Every **required** member of a record that a cited contract defines as an identity key, or as a key's field-for-field copy, is identity-bearing. So is every member a contract requires to equal a key's member.
   - **The records.** The script closes them in `KEY_RECORDS` and `KEY_COPY`, each with its sentence:
     - DLV `CoverageKeyV1` (DLV:804-817);
     - C-2 `coverageKey.key`, with RPP:544-548;
     - the returned `CoverageKeyV2` (NE:3277-3282; NE:1927-1932);
     - `ViewEntryV3`'s `relation` and `resolution` (NE:3529; NEM:1566-1567).
   - **Precedence.** R1 to R6 keep their admissions and labels.
2. **Every other composite key checked.** Item 13 now lists each one with why it is or is not a key: the request key, the returned key and entry, the fact identity, commitment preimages, view and occupancy keys, correlation tuples, and scope summaries.
3. **Derived counts.** r4 derived 51 rows and 235 paths; r5 derives 52 rows and 278 paths (TS2 121, Rust3 157). The +43, with none removed, are 30 R7 paths on existing rows plus the RUST3-LIM row's 13. By rule: R1 200, R2 23, R3 4, R4 15, R5 3, R7 33.
4. **L-G11, RUST3-LIM accepted (lead decision).**
   - L does not take effect on a Rust3 that refuses two of S-M's seven Rust medium workloads.
   - A fourth delta-round trigger names RUST3-LIM's reopening parts exactly.
   - X13 and R12 are closed by pointing at it, and item 1 names it.
   - GROK2 has since accepted it, so L-G11 is **met in review, held on FA-2**. It opens again only if Codex's review changes FA-2's handshake copies, which are RUST3-LIM's parents (change 9 below).
5. **Item 13.** The Rust per-file `subjectId` is on the wire only without `subject-scope-reference-v1`. Under the token, each stage carries `subjectScope.subjectScopeCommitment` instead. This was pending RUST3-LIM's acceptance, which GROK2 has given. It now waits on RUST3-LIM's binding after FA-2, as FA-2's members wait on FA-2.
6. **Item 9.** SM-11 to SM-14, as RUST3-LIM proposes, with the large Rust workloads and S_eff.
7. **Gate rename.** L-G1 to L-G11, because "G10" collided with DR-G10 (M3-PLAN r9 NBO-1). The kept r2 to r4 tables keep the old names.
8. **NBO-1.** The opening paragraph now states the four triggers as the operative text does.
9. **RUST3-LIM accepted (r5 changes row 11).**
   - The fourth trigger, in both statements, now names any later change to RUST3-LIM's accepted bytes, including a rebuild forced through FA-2's handshake copies.
   - The operative trigger maps GROK2's two NBOs. NBO-1 is evidence and needs none. NBO-2 reopens L only if it is closed by editing §9.3a's reading rule.
   - The L-G11 row, item 13's condition and RUST3-LIM row (script labels only; no count moves), the RL short name, the joins row, X13 and the Effect clause all record the acceptance.
10. **Pin base (row 12).** Main moved to `392499e` (CRC-1, M3-C's core role closure successor). CRC-1 overrides nothing this law cites and shares no parent with FA-2 or RUST3-LIM.

## Decide

1. **RF-1.** Is R7's record list complete and exact, with each record's sentence? Is the checked list of other composite keys right? Run L-C1 read-only. Does the derived table now include every constituent of the coverage keys and entries the contracts define, and nothing they do not?
2. **The counts.** Do they match the regenerated report?
3. **RUST3-LIM's join.** Rule on:
   - whether L-G11 is lawful, and whether its state ("met in review, held on FA-2") is right;
   - whether the fourth trigger's map is exact, including its mapping of GROK2's two NBOs;
   - item 13's RUST3-LIM row and the AnalyzeV2 row's condition;
   - whether SM-11 to SM-14 are correctly stated as measured figures and not protocol constants;
   - whether closing X13 and R12 by pointing at RUST3-LIM is right.
4. **The rename.** Is every operative gate reference renamed? Are unit names (F2/G3, F4/G2, "a G2 plan", "bears on G4"), DR-G gates and the REG:342 quote left alone?
5. **NBO-1.** Is it answered?
6. **The re-pins.** Is the H1 to H3 map right, does M3-PLAN r9 record what X9 now says it records, and is the `392499e` pin base (CRC-1) right?
7. **Dependence. State explicitly which parts depend on O7, which on S-M's figures, which on FA-2 and which on RUST3-LIM.**
8. **Anything else** r5 changed that is wrong, or r4 text it left stale.

## Running L-C1 (optional)

`nice -n 19 python3 docs/implementation/m3/provider-protocol-l/evidence/wire_identities.py --check` reads arch documents only and writes nothing. Without `--check` it prints the table.

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`. An ACCEPT is recorded as "accepted in review". The law takes effect only when L-G1, L-G4, L-G5, L-G9 and L-G10 are met, L-G11 still holds, and S-M's delta round is accepted;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256;
- `"gateDependence"`: `{o7, sm, fa2, rust3lim}`.

This is a law review, not a `verify_design` unit. Do not commit.
