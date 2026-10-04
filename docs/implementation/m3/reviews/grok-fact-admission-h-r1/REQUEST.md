GROK review: M3-H r1, the fact admission law. This is a **law and contract-soundness** review, round 1. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok-fact-admission-h-r1.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run may be using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- Use read-only scratch scripts under your review directory if you need them.


**Two pinned files moved after pinning (lead note).** Their live paths now hold new drafts:
- `m3/host-pipeline-j/PROPOSAL.md` is J1 r4, a narrow SD-6 amendment in review with CODEX2;
- `m3/snapshot-plan-c/PROPOSAL.md` is M3-C r7, likewise.

Judge H against the **pinned bytes**:
- J1: `git show 176534ae7:docs/implementation/m3/host-pipeline-j/PROPOSAL.md` (`89c84927…`; r3 plus its acceptance note);
- M3-C: `git show 3590205a9:docs/implementation/m3/snapshot-plan-c/PROPOSAL.md` (`a2f16b7b…`; r6 plus its note).

Run git read-only with a private `HOME`. You may also read the new drafts, J1 r4 (row R10a) and C r7 (row 8 narrowed to manifests admitted at R10a), and say whether either changes anything H relies on.

## Subject

The pins are in `hashes.txt`. The subject file is untracked in arch until acceptance.
- **The subject:** `docs/implementation/m3/fact-admission-h/PROPOSAL.md`, law M3-H r1. It is the subject of `subjectSha256`.
- **The plan row:** `docs/implementation/m3/M3-PLAN.md:218` (M3-PLAN r6, accepted). The H row in its DAG is `:309`.
- **The laws H must join exactly** (all pinned):
  - M3-C r6, by the bytes CODEX2 accepted in review (`snapshot-plan-c/PROPOSAL-r6.md`, `8274bca1…`). Read item 9 (the core provider closure, MC:420-466) and item 16, including the C2-R1 split (MC:869, MC:873-885).
  - M3-E1 r3: items 10, 13, 14a, 14b and 16, and the second-integrator rule (ME:716-730).
  - M3-I1 r2: item 8, what H must admit for I1-b2 (MI:398-401), and items 2.3 and 2.5.
  - M3-J1 r3: J-η (MJ:350), the outcome matrix (MJ item 10) and J2b (MJ:753).
  - M3-B r2: U-5, U-6 and the inventory cells (MB:408, MB:416).
  - M3-D r3, accepted by GROK2 (`supervisor-d/PROPOSAL-r3.md`, `9679dbc4…`): item 20 and finding F7 (MD:618-633, MD:1107), and D2b's CBOR reader (MD:335).
- **One draft, cited for an interface only:** M3-L r2 (`provider-protocol-l/PROPOSAL.md`, `5bd4025e…`), which is in review with you separately. L r2 and D r3 appeared while H was drafted. The law cites their bytes and states that the provisions it relies on read the same in L r1 and D r2, which are pinned for that check.
- **The contracts:**
  - NE §4 (COV's `native-evidence:5`), §9.6, §9.7 and §10;
  - IE §3 and §4;
  - REG:368 and REG:370;
  - CH14:482; BP:680-683; COV's DR-G23 and DR-G25 rows;
  - the incorporated foundation contracts and schemas (ENC, EXC, ATOM, FAULT, SIS, IDS, RPS, EPLAN);
  - NCM, NEM and PWM;
  - the inherited protocol bases DLV and RPP.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `e093e90`, read-only. That is F8b on top of `3e64266`; F8b changed no file under `crates/`, so `3e64266` and `e093e90` agree on every cited line. The product files the law cites are pinned in `hashes.txt` by their bytes at that commit: `fact_admission.rs` and its tests, and the evaluator inspectors H calls.

## What the law decides

1. **Scope and layout** (items 1 and 2). H is the producer-boundary admission for native evidence. Its joins live in child modules under `crates/host/src/fact_admission/`. The root stays X5's replay join, byte for byte, with X5's pin unchanged.
2. **The boundary** (item 3). Only D3's clean settlement reaches H. Admission is atomic per Analyze, and every coordinate is re-derived from host-held values.
3. **Clean non-Complete terminals** (item 4, answering MD's F7). Candidates are discarded and the terminal's exhaustive Coverage is admitted. This applies DLV's and RPP's retained candidate dispositions against NE:3849-3850 (X-H2, FA-1).
4. **The fact join** (items 5 to 8). Relation registry and RC-0, requested relation, the CBOR-to-`C` adapter, anchors, source and universe joins, the native confidence law, and the stage spec's producer. Where an owner already exists, the evaluator's and identity crate's Run-closure keys are reused.
5. **The Coverage join** (items 9 to 13):
   - D is built from host values, with subjects by subject kind.
   - `inspect_coverage_producer` serves as `admit_coverage_result_v3`, with a complete unresolved census and the universe dialect always passed.
   - No entry is edited and nothing becomes `complete` by the host.
   - Closed-world cross-checks are an extension wired after FA-1.
6. **Views, occupancy and the syntax join** (items 14 to 16), including E1's second-integrator legs.
7. **Inventories and the hand-off** (items 17 to 19):
   - symbol-census owner admission;
   - host-produced inventory records absorbed into H (X-H5);
   - origin-tagged hand-off to J2b's full `admit_enumeration`.
8. **Routes** (item 22) use existing rows only. **Units** (item 25): H1 to H5, with only H5 on the host chain (day 22).

**Cross-law items** X-H1 to X-H6 name the law that must change. X-H1 (the provider symbol census has no carrier on TS2 or Rust3) and X-H3 (no lawful producer closure for host inventory records in TS and Rust universes) are the most consequential.

## Decide

1. **Grounding.** Is every claim grounded in a cited line of an accepted document or of the product at `3e64266`? Are the citations accurate?
2. **Joins.** Does the law join the accepted laws exactly: C r6's item 9 and C2-R1 split, E1's second-integrator rule, I1 item 8, J-η, and the B inventory split? Where it says two accepted texts conflict, is the conflict real? Is it recorded rather than papered over, with the right owner named?
3. **R1 to R8** in the law's "Review questions":
   - R1, the X-H1 carrier gap;
   - R2, clean terminals;
   - R3, the completeness of the fact join;
   - R4, D and the census;
   - R5, X-H3;
   - R6, the layout against X5;
   - R7, the occupancy buffer timing;
   - R8, routes.
4. **Gates.** Are the DR-G23 (NT-3, NT-5) and DR-G25 obligations prepared by named controls (H-C1 to H-C23), with no public code added?
5. **Units.** Do item 25's units preserve M3-PLAN r6's 33-day conditional host chain, under the stated condition that FA-2 and C r7 / CRC-1 land before day 0?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. FA-1, FA-2 and CRC-1's widening each need their own `ACCEPT-DESIGN-UNIT`. H's code units need `ACCEPT-UNIT` reviews. Do not commit.
