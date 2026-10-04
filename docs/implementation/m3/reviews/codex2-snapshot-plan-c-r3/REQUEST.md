CODEX2 review: M3-C r3, the sealed snapshot and Plan law. This is a **law and contract-soundness** review, round 3. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-snapshot-plan-c-r3.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run may be using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- If you compute digests or schedules, use read-only scratch scripts under your review directory.

## Subject

The pins are in `hashes.txt`.
- **The subject:** `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`, the r3 law. It is the subject of `subjectSha256`.
- **For diffing:** `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r2.md` (`bf44ffe2…`), the r2 bytes you reviewed.
- **Your earlier reviews:** `/tmp/opensip-implementation/reviews/codex2-snapshot-plan-c-r2/` and `…-r1/`.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `30c5db1`, read-only.

**Two dependencies changed under this law since r2:**
- **M3-B r2 was accepted by GROK2** (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`). It assigns C1 its findings F1, F10 and F14, and its successor S4.
- **X12 r4 was drafted from M3-B item 10's successor S2,** and is **pending Grok's review** (`docs/implementation/m2/policy-admission-x12/PROPOSAL.md`; `reviews/grok-pack-admission-x12-r4`). It names row 1 of this law's order table as a dependent to update.

## What r3 changes

The "r3 changes" table at the top of PROPOSAL.md maps each item to its change.

1. **C2-R1 (item 16).** Enumeration admission is split in two:
   - **Step 15: pre-execution structural admission** (C4). Its limited interface has **no inventories argument**. It checks the inventory-free joins (`enumeration-contract.v1.md:100-106`), and a refusal is a host-invariant fault.
   - **The full `admit_enumeration`** (`:164`) runs after execution and before evaluation, in J2 with H, over the actual inventories (IE:1462-1474, IE:1513-1515; COMP:15-17). Its routing depends on origin (`:159-160`), and Run closure re-admits again (`:157-158`).

   C4-T19 adds a non-empty available `imports`-cell symbol population.
2. **C2-R2 (items 1 and 2).**
   - **Two classes of read.** **Source reads** are governed by the one-read rule. **Operational reads** are X2's marker, carrier, Git and recheck reads, and C1's VCS reads. They never supply inventory bytes.
   - **`.opensip/` is excluded.** At the project root and at each D15 member root, `.opensip/` is excluded by an exact discovery anchor (successor SX-1, with B-S1). This also discharges M3-B's F10, and C1 never touches `local.json` in CI.
   - **`opensip.json`** is the one path read both ways. The walk's bytes must match X2's carrier-capture digest, or the snapshot refuses. The handoff is by digest only, and X2's types are unchanged.
   - **The capture session** opens after X2's handoff releases the fence.
   - **Controls:** C1-T24 is revised and C1-T25 is added.
3. **C2-R3 (item 12).**
   - **Protocol counters** are set-wide, exact and logical: packages, regular files and content bytes. Crossing one is a set bound.
   - **Decoder counters D1 to D4** are per archive: a framing allowance derived from the profile, long-name records, compressed input and gzip fields. Crossing one is an archive-profile breach, so the package is recorded missing if activated, with an `undecodable:` reason. It is never a set refusal.
   - **Omissions:** the `missing:` and `undecodable:` omissions are reconciled, and an inactive package does not make the set incomplete.
   - **Controls:** C3-T6b.
4. **X12 r4 (item 16, rows 1 to 4).** The order is:
   1. X2's fenced selection and carrier captures, which are operational and write nothing;
   2. B1's resolution;
   3. pack admission;
   4. X2's registry capture, registration, lease and handoff.

   **The first-use clause:** on the first-use creator route, "before any effect" reads "before any project-scoped effect". X12 r4's acceptance is a gate item and a C4a gate. Control C4-T20 is added.
5. **M3-B r2 obligations:**
   - **F1:** a snapshot ledger, never under the fence (item 2);
   - **S4:** `vcs-observation` schema 3 for D15 workspaces, with HEAD and ref reads for every repository alike (item 4);
   - **F14:** "Units" now expresses the host chain as **b + 23 days** in variant B, where b is the day B2-c finishes. That is 28 at M3P's b = 5, 31 at M3-B's estimate of b = 8, and 33 at b = 10.
6. **C2-N1 and C2-N2.**
   - **C2-N1:** the C2c counterfactual is corrected to 30 days in both variants. F1 and G1a's edges are narrowed to the interfaces they consume, with the full-edge alternative stated.
   - **C2-N2:** a UTF-8 truncation-boundary fixture is added, and R6's evidence becomes C3a's review evidence.

## Decide

1. **C2-R1.** Is step 15's structural admission a lawful pre-execution subset of the enumeration law, and is the full admission placed at its governing point with origin-sensitive routing? Does C4-T19 prove that no inventory is manufactured?
2. **C2-R2.**
   - Is the operational/source boundary exact against `project_admission.rs` (:536-545, :561, :604, :612-615, :797, :818, :872), X2 r9 item 3a (M3-B:608) and M3-B items 2, 3 and 12?
   - Is excluding `.opensip/` by an exact anchor, under successor SX-1, the right disposition of F10?
   - Is the digest-only `opensip.json` rule sound?
3. **C2-R3.** Are the protocol counters now exactly the logical quantities of NE:2876-2878, NE:1663-1664 and NE:2931-2932?
   - Are D1 to D4 correctly derived, with no legitimate Cargo archive inside the protocol bounds breaching them?
   - Is the breach disposition consistent with DS-6 and item 13?
4. **X12 r4.** Do rows 1 to 4 faithfully carry X12 r4 item 8 and its first-use clause? Is citing r4 as pending, with a gate, adequate?
5. **M3-B reconciliation.** Are F1, F10, S4 and F14 discharged consistently with M3-B r2? Is the b + 23 formula right?
6. **Regressions.** Did any r3 edit contradict a decision you accepted in r1 or r2?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. The contract successors (CRC-1, CR-1, NIJ-1, VCS-1, SX-1, S-B, S-R, T2-DEP) need `ACCEPT-DESIGN-UNIT` reviews of their own. X12d and the C code units are inventory units, reviewed with `ACCEPT-UNIT` and `inventoryCandidateAssessment`. Do not commit.
