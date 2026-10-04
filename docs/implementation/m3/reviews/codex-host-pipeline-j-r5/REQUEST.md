Codex review: M3-J1 r5, the guarded durable host pipeline. This is a **law and method-soundness** review, round 5. It is a **record revision** that also carries two lead decisions. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-host-pipeline-j-r5.

**Lead note (product base).** The law and this request were drafted against product main `5214350` (88 contract successors). Main has since moved to `218465f` (91), by binding-only commits: CR-1, SYN-1 and SYN-1F. Nothing J1 cites changed, and WS:226 and WSE:226 are still free in the lock. SYN-1 has since been accepted and bound. r5 records it as pending, matching its cut-off; J1's next revision records it. Don't run cargo.


**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run may be using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- Use read-only scratch scripts under your review directory if you need them.

## Subject

The pins are in `hashes.txt`. Every cited law is pinned at its accepted snapshot (`PROPOSAL-rN.md`), never at a live file, which may move to a new draft during your review.
- **The subject:** `docs/implementation/m3/host-pipeline-j/PROPOSAL.md`, the r5 law. Its sha256 is `subjectSha256`.
- **The diff base:** `docs/implementation/m3/host-pipeline-j/PROPOSAL-r4.md` (`c18c0d3c…`), the r4 bytes GROK2 accepted, without the acceptance note. r5 is built from these bytes. Diff r4 against r5: every change should appear in r5's "r5 changes" table.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `5214350`, read-only, with 88 contract successors and inventory v135. J1 was read at `3e64266`. Between the two, the only product file J1 cites that changed is `crates/security/src/custody/operation_guard.rs`, and only at lines 225-241 (X4-F1). J1 cites its lines 99-106. You can check with `git diff 3e64266 5214350 -- <path>`.
- **One naming note.** GROK2 reviewed S18, but its review directory is `reviews/codex2-s18-r2/`, the name of S18's first assignment.

## What r5 records, and where each item comes from

1. **S20 = SD-5**, accepted by Grok and bound at product `052d3cb` (`supervisor-d/sd-5/README.md`, "Totality for `ExcludedForm`" and X-SD5-J1):
   - row 56 is SD-5's row, word for word;
   - row 27 now reads "not admitted by current trust";
   - J-C20 gains row 56's test;
   - S20's row records the bound route and what stays owed.
2. **S19 = M3-C r7**, accepted in review by CODEX2. Status only.
3. **X-SD5-1** (SD-5's cross-law items). M3-D item 25's request-class `ExcludedForm` at R1 is recorded as routed to M3-D r4, with the row's shape pending. No M3-D r4 exists in arch: `supervisor-d/PROPOSAL.md` is r3 plus its acceptance note.
4. **S18**, accepted by GROK2 at r2 and bound at `5214350`. r5 applies S18's cross-law items 1a to 1d and 1g (`host-pipeline-j/s18/README.md`, "Cross-law items"):
   - NB-02's three-way rule, in 8.2's row O;
   - NB-01's citation fix;
   - the S-OP-2 r6 re-citations;
   - 5.3's settlement wording, per LD-4;
   - item 13's S18 row.
5. **X-FA1-J1.** FA-1 is bound at `f97c02b`. It re-cites row 31's basis.
6. **X14** (M3-L r5) **and X-FA2-J1** (FA-2, bound at `8ca420f`). Item 2's forbidden substitute now cites L r5's item 13.
7. **X10** (M3-L r5; M3-PLAN r9's routing table). M3L is cited by item, never by line.
8. **Moved snapshots:**
   - M3P moves to r9, with a new M3P6 for r6's own words;
   - M3C moves to r7;
   - M3D's sentence about the live file is corrected, per GROK2's NBO-1 on r4;
   - MH is new (H r3);
   - SOP2 moves to r6;
   - X3C is new (X3c r8);
   - M3L moves to L r5.
9. **S17** is recorded as done by M3-PLAN r9. X3c r8's acceptance is recorded in item 11 and in S14.
10. **SYN-1**, in review with CODEX2 and not accepted, is recorded as pending, and no row changes. SYN-1 is **not pinned**, because it is not accepted. The draft is `syntax-e/syn-1/README.md`, with cross-law item X-J1 and observation O-1. Its subject manifest is `syntax-e/syn-1-subject.json`, `4ed2d9ba…` as `syn-1-unit.json` records it.

**Items routed toward J1 that r5 deliberately does not record:**
- **J-RW's RW-S8.** J-RW is in review, and its r3 is being written.
- **M3-H's R-J1**, the reach of row 36. H routes it to J2a, not to J1's text (H r3, "Record corrections"), and M3-PLAN r9's routing table agrees.
- **X3c r8's CL-1.** It is routed to X3d r9, which is J1's S10, and not to J1's text.

## The two lead decisions

- **LD-r5-1** (8.2, the new paragraph after the table; S18 cross-law item 1e).
  - **The case.** A signal is observed after `publish` returns `Refused`, `CommitUndetermined`, or `Committed` with `latchedAfterAdmission`, and before the output decision point.
  - **The decision.** It is labelled by the last phase the operation reached: C if FinalGate admission had succeeded, and B otherwise. The label is read from the state bits of the window close's own sample (8.1).
  - **Rejected:** D; A; a new `CancelPhase` member; no label.
- **LD-r5-2** (8.3, the new paragraph; S18 cross-law item 1f and its LD-12).
  - **The decision.** 8.3's rules 1 and 2 stand against WS:226, on the basis of IE:1680-1681 and SL:551-554.
  - **The WS amendment** is recorded as an owed successor, **S21**, on WS:226 and WSE:226. Both lines are free in the lock at `5214350`. r5 does not make the amendment.
  - **What waits for S21:** J3d's durable signal wiring, J-C14's rule-1 and rule-2 signal cases, J-C15b's phase-C projections, and rows S12-C and S12-U.
  - **Rejected:**
    - WS:226 as written;
    - reading WS:226 as subordinate to WS:233-240;
    - calling the signal after-settle or final-output;
    - amending WS here;
    - no gate;
    - gating J2a, or all of J3b.

## Decide

1. **Fidelity.** Is each recorded item faithful to its source? Does r5 change anything that no source or lead decision calls for? In particular:
   - Is row 56 SD-5's text, word for word? Are row 27's reading and J-C20's test what X-SD5-J1 asks?
   - Do 8.2's row O and J-C14b now say what S18's LD-6 and LD-7 say (NB-01 and NB-02)?
   - Is 5.3's settlement point S18's LD-4? The same applies to the "does not settle the invocation" wording in 5.3 and 8.4, which replaces r4's "does not make step 1 terminal". Were the 8.4 edits needed for consistency with LD-4?
2. **Re-citations.** Does every re-pinned citation resolve to the same fact at the new snapshot?
   - **M3C, r5 → r7.** Every cited line is claimed to be byte-identical, moved by 22 to 49 lines.
   - **SOP2, r4 → r6.** S18's map, plus 710 → 766.
   - **M3P, r6 → r9.** Every fact r9 still holds is re-pinned to r9. M3P6 keeps r6 for r6's own words: item 1's quotation, item 14's r6 sizing, and item 15. Is that split right, or should every M3P citation move to r9?
   - **M3L, r1 lines → L r5 items (X10).** :120 → item 2; :375-382 and :377 → item 13; :442-462 → item 16; :450-457 → item 16c; :548 → X3.
3. **LD-r5-1.**
   - Is "the last phase reached", read from the close's sample, a sound and implementable label?
   - Is `Refused` always a pre-admission return (X3D items 4 to 6)?
   - S18's item 1e names only `Refused` and `CommitUndetermined`. r5 extends the rule to a `Committed` the latch sampled, which also never enters D. Is that extension right?
   - r5 leaves `prepare_commit`'s error returns to row A's existing reading. That includes a refusal at `prepare_commit` step 6, after the attempt row committed (X3D:130-138). Is leaving that unchanged right for a record revision, or is it a gap that must be closed now?
4. **LD-r5-2.**
   - Is the conflict real: WS:224-228 and WS:233-240 against IE:1680-1681 and SL:551-554?
   - Is outcome-first precedence the right resolution?
   - Are S21's content, owner and gate right?
   - Is the gate the right size? J3d's durable signal wiring, J-C14's rule-1 and rule-2 signal cases, J-C15b's phase-C projections, and rows S12-C and S12-U wait. J2a, J3b's other work, S12-B and S12-D proceed.
   - Does item 14 state S21's planning effect correctly, where S21 joins J3d's critical-path conditions?
5. **Pending items.** Are X-SD5-1 (routed to M3-D r4, shape pending) and SYN-1 (pending acceptance, no row change) recorded without deciding anything?
6. **Scope.** Does r5 change anything else in r4?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256, as one string.

This is a law review, not a `verify_design` unit. S21, J-BS and the inventory units J2a to J3d still need their own reviews. Do not commit.
