CODEX2 review: **S18**, the final-output-section contract successor of the host pipeline law M3-J1. You accepted J1 r3, and GROK2 accepted r4. S18 is a passage successor to WS §1's cancellation paragraph (WS:224-231) and to the operability plan's §5.5 phase table (OPP:330-340). It also carries your two non-blocking observations on J1 r3, J1-R3-NB-01 and J1-R3-NB-02, as J1 r3's acceptance note promised. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** with `subjectManifestSha256`, or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-s18-r1`.

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** Run no cargo, no tests, no generator and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** The lead ran the real `tools/verify_design.py` from `cd5958b`, design-only, in the scratch harness (`evidence/verify_scratch.py --rev cd5958b`). The harness writes nothing and holds a synthetic review and assent in memory. You may rerun it. Never edit the product or its lock.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**
- **Product main is `cd5958b`**, read only, with 82 contract successors. **Lock pin:** `design-lock.json@cd5958b` (334,799 bytes, `67a5bb92…`). The record is built and checked against it.

## Subject

The pins are in `hashes.txt`. Every file is untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/host-pipeline-j/s18-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 8 members** are:
  - `s18/successor.json`;
  - `README.md`;
  - `PASSAGES.md`;
  - `operability/PLAN.md`, the complete successor copy of the operability plan;
  - `evidence/copies-report.json`;
  - `evidence/build_s18.py`, `check_s18.py` and `verify_scratch.py`.
- **Not part of the subject:** `s18-unit.json`, the lead's DRAFT-PENDING-REVIEW record.

**Law.**
- `host-pipeline-j/PROPOSAL-r4.md` (`c18c0d3c…`) is GROK2's r4 acceptance. Its passages:
  - the S18 row, J1:772;
  - 5.3, J1:382-396;
  - 8.2's O row, J1:535;
  - 8.4, J1:550-561;
  - J-C14, J-C14b and J-C14c, J1:589-603;
  - S12-O, J1:746.
- `PROPOSAL-r3.md` (`ad887c90…`) is your acceptance. r4 changed nothing S18 touches.
- NB-01 and NB-02 are in `reviews/codex2-host-pipeline-j-r3/review.json`.

**Joins:**
- S-OP-2 r6, `operability/s-op-2/PROPOSAL-r6.md` (`ce8d3a4b…`, Codex ACCEPT-DESIGN-UNIT, not yet bound):
  - ordinary registration, r6:226-230;
  - finalization, r6:652-683;
  - after the freeze, r6:704;
  - `host.signal.received`, r6:871.
- X7 r6 (`9e17faf2…`) and X3D r8 (`5e491b92…`), the M2 accepted snapshots.
- The operability plan's accepted r3 bytes, `operability/PLAN-r3.md` (`b49035f2…`). The live `PLAN.md` adds only the two-line acceptance note after line 1, so OPP:330-340 is r3:328-338.

## What it does

The README has the full tables; `PASSAGES.md` has every text. In brief:

1. **Six line overrides, insert or replace only:** three on WS and the same three on WS's selected effective copy WSE (`source-selection-v2/reference/effective-workflows-and-surfaces.md`). The lock at `cd5958b` binds no entry on any of these lines.
   - **WS:225 and WSE:225.** The *before-settle* definition is narrowed to signals observed no later than the output decision point, where the final output section applies.
   - **WS:231 and WSE:235**, the cancellation paragraph's last line, kept. A new **Final output section** paragraph follows it:
     - the output decision point;
     - the section, for the decided envelope or the interrupted termination output;
     - settlement when the output returns;
     - a *final-output* signal deferred, changing nothing the decision fixed and recorded only operationally, for durable and ephemeral alike;
     - a renderer failure before any byte, routed by committed evidence through §8's required-output law and §9's rows 1376 and 1377, under WS:233-240's aggregate;
     - NB-01's fault owners;
     - a write or flush failure ending exit 4 with no replacement;
     - nothing added.
   - **WS:1393 and WSE:1466.** The SIGINT golden row's detail cell gains the deferral.
2. **A complete successor copy of the operability plan r3.** The plan is not a `verify_design` input, so it cannot be a parent (CR-1's case). The copy is `PLAN-r3.md` with five lines replaced and one inserted:
   - §5.5's lead-in (r3:328);
   - row D (r3:335), which answers r3's open question;
   - a new **row O**, which carries NB-02 and `CancelPhase` `O` by ordinary registration;
   - row E (r3:336);
   - consequentially, §5.2's user-interrupt row (r3:293) and §10's cancellation control row (r3:433).

   The record's `standing` selects the copy, B-S9's form.

## Lead decisions for you to rule on

The README records thirteen, each with the alternatives it rejects:
- **LD-1.** The form: WS and WSE line overrides, and a complete copy of OPP r3 selected by the record.
- **LD-2.** WSE takes WS's overrides (I1-L's LD-L5).
- **LD-3.** Scope: every invocation whose last required step is the `render` step that writes its one required envelope (44 of CINV's 45 commands).
- **LD-4, substantive.** The interrupted termination output is written in a final output section too, and settlement is the decided envelope's output return. A renderer failure of a termination output fails the render step (J1 row 44's "an interrupt with no Run").
- **LD-5.** An O signal enters neither the envelope nor an invocation record it carries. INV5's closed `Cancellation.phase` has no member that fits it.
- **LD-6 and LD-7.** How NB-01 and NB-02 are carried. NB-02's rule is three-way, by S-OP-2 r6's cutoff, reads and freeze. Delayed emission is rejected.
- **LD-8.** Every failed write or flush of the decided envelope is final, byte or no byte, because `write_all` reports no count.
- **LD-9.** S-OP-2's finalization keeps the decided termination's deadline.
- **LD-10.** The copy's scope. Rows A to C, the r3:338 note and §9's S-OP-12 row are left to OPP's next revision under J1's S15.
- **LD-11.** WS:1393 is qualified, and no CINV golden is added.
- **LD-12.** J1 8.3's commit-phase precedence is not restated in WS. It is flagged as a J1 cross-law item.
- **LD-13.** Binding-only, with no materialization.

## Decide

1. **Exactness.**
   - Is every `before` the exact parent line?
   - Is every `after` true and minimal, and are the WS and WSE pairs identical?
   - Is the copy exactly `PLAN-r3.md` plus the stated edits?
2. **Completeness against J1.** Does S18 carry the S18 row (J1:772), with 5.3, 8.2's O row and 8.4, completely, and nothing beyond the lead decisions?
3. **Your observations.**
   - Is NB-01 carried as you recommended? That is: the X3D and X7 fault owners cited directly, §9's return-to-owner, no verdict or closed-Run composition, and the disclosure kept whichever termination is primary.
   - Is NB-02 carried as you recommended? That is: classification and deferral common to all of O, and the event's fate by the actual cutoff and freeze.
4. **The form and scope.** Rule on LD-1, LD-2, LD-3 and LD-10. Is a complete copy of a non-input plan, selected by the record, a sound successor here?
5. **The precisions.** Rule on LD-4, LD-5, LD-8 and LD-9.
6. **Consequential passages.** Does any other accepted passage still read against S18? Candidates:
   - one that says every pre-settlement signal gives `interrupted` 130;
   - one that defines settlement by step terminality alone;
   - one that records a final-output signal as a cancellation phase.

   Look in WS, WSE, the copy, INV5's descriptions, the CINV goldens and WSE's interruption-ledger text (WSE:1389-1395). Rule on LD-11 and LD-12.
7. **Selection.** Is the record well-formed under `verify_design`'s `contract_successor` and `successor_chain` rules? Is anything else wrong?

## Running the evidence (optional)

Use `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`. Neither script needs extra dependencies.

1. **Build check.** `docs/implementation/m3/host-pipeline-j/s18/evidence/build_s18.py --check` rebuilds everything in memory and compares it with the files on disk. It reads the product lock at `cd5958b` through `git show`.
2. **Content checks.** `.../evidence/check_s18.py --rev cd5958b` runs 121 independent checks. They cover:
   - the pins;
   - the lock, and every unbound in-flight record (23);
   - the copy's difflib alignment against `PLAN-r3.md`;
   - J1's S18 row and both observations;
   - no new code or exit;
   - every cited line in WS, WSE, X7, X3D, S-OP-2, OPP r3, J1, RTC, INV5, ENV7 and `bootstrap.rs`.
3. **`verify_design`.** `.../evidence/verify_scratch.py --rev cd5958b` is design-only. It takes the lock from 82 to 83 successors, with six overrides and no supersession, and leaves the inventory (`v134`) and the inheritance (55) unchanged. A probe shows that a later conflicting override of WS:231 is refused.

The lead ran the build twice, with identical bytes, and both other scripts once, all passing.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `s18-subject.json`. The lead's value is `9d184011d659d7cffe154280c3325aa3844f9625f24d20e71463f6ab00904ffc`.
- `"successor"`: `{path, bytes, sha256}` of `s18/successor.json`. The lead's value is 13062 bytes, `5407ce5170cfb7f5ae611c542f13a06297172e3afa36180f603ebcc14064f17f`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. One review maps exactly one subject. If you would change bytes, give the exact replacement text. Do not commit.
