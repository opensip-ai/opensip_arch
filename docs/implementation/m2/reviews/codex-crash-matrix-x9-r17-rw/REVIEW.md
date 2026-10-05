X9 r17 round 3, §RW: **REQUIRED-FINDINGS**, one P2 finding.

Codex is the single reviewer; Grok is the implementation lead. This review judges §RW and NBO-1 under LD-17-1. The subject is docs/implementation/m2/crash-matrix-x9/PROPOSAL.md, 332138 bytes, SHA-256 118a9a9835933da722691d1477a3f574e7ffd9deca73f7c21af7c6217c581aff. The diff base is PROPOSAL-r17-S12.md, 278697 bytes, SHA-256 6b208ccf7d1b0ce5c18ec0329724fbc103de8b18d9abae0b02a6ac0856f397f3. All six supplied pins match, including the accepted J-RW r4 snapshot.

**X9-RW-RF-01 — correct J4a's census delta (P2).**

RW.3, line 2245, says J4a's states add eight census points and eight kill-set points. Its own preceding predictions describe four distinct point names:

- x3c.ledger-create.projects.repair/directory-barrier.before
- x3c.ledger-create.projects.repair/directory-barrier.after
- x3b.floor.directory.repair/directory-barrier.before
- x3b.floor.directory.repair/directory-barrier.after

Each occurs twice. Therefore these states contribute **four census points, eight durability events and eight kill-set points**. The eight RW-K4/RW-K7 rows listed in RW.5 are correct.

This uses the matrix's existing meaning of censusPoints. At pinned product 43ea32a, Census::from_exit groups occurrences by name (crates/platform/src/crash_barrier/driver.rs:552–557); census_json emits one entry per name with its separate occurrences field (crates/security/src/crash_matrix_support/run_record.rs:263–274); and the checker reports len(census.points) (tools/check_crash_matrix.py:407 and :476). For n=2, sampling first/middle/last selects #1 and #2, giving two kill points per name. The accepted J4a diff's two directory barriers under each repair scope agrees with the section's own prediction.

RW.7 makes J4e match RW.3's prediction and stop on a contradiction (lines 2523 and 2532). A correct four-name contribution would contradict the stated eight-name census delta. Correct line 2245 and any dependent count to four new census names, each occurring twice, with eight kill-set points. Keep the eight rows and their expectations. Later units' additional names remain determined by their own censuses. No matrix run is needed to resolve this arithmetic error.

**Requested decisions.**

The row outcomes transcribe accepted J-RW r4 item 10 faithfully. RW-F00 covers the 57 L11 cells, split as 46 registration, six private-creation, two conditional ledger-schema and three trust-leaf cells. RW-D1 explicitly covers the unsampled predecessor-directory occurrence #6. RW-K carries all ten start states, with RW-K6 conditional on J4c's pins. RW-K5 explicitly stays in the census with an empty repair kill set and no row. The composition sentence's “has rows” phrase should be read with that explicit K5 exception. Child 3's completion expectations respect the final-effect boundary; a trust leaf also needs child 3's publication to name it, determined before a run by the existing reference method.

RW-N covers the twelve neighbour families, expanded to 15 rows by the three N-R9 marker variants and two ledger-with-WAL custody variants. Its outcomes retain the accepted custody/contradiction/corruption/incomplete distinctions. Its empty completion report and neighbour preservation score the safety bias while permitting earlier lawful effects. The explicitly excluded SQLite WAL/SHM siblings remain governed by the reader's existing lawful behavior. RW-B uses the existing busy-writer and skipped-sweep outcomes with the registration writer held under the fence.

J4a's six re-transcriptions are exactly the moved cells. I checked the stored rows at indices 141, 147, 153, 159, 165 and 101 at 43ea32a against their case/variant identities and old expected objects. The first five use form B: R2 becomes Committed and gains the existing witness alternatives; R4 becomes unknown-attempt-unobserved; R1, R3 and pre-attempt values stay. The carrier-floors row uses form A, with R1/R4 absent. The existing identities, scripts, labels, units and lack of unit selector stay. No other storage or host row kills one of these 57 points. The 174 F00 rows agree with 083ad5c, and the existing committed forms have the stated 89/22 counts. Storage has 403 rows and host 98 at the pinned base.

NBO-1 is a citation correction only. SOP2 r6:871 registers A–E; J1 r6:588 registers O. The bullet keeps the same A–E/O spelling, order and no-signal value. The complete diff has exactly three hunks: the prior round's acceptance note, this citation, and the reserved RW section's replacement. No other r17 section's row changes.

**Lead decisions.**

| Decision | Assessment |
|---|---|
| LD-RW-1 | Accept F00 for pre-attempt repair/neighbour rows and F30 for contention. |
| LD-RW-2 | Accept unchanged old identities and variants distinguishing repair point and start state. |
| LD-RW-3 | Accept unchanged RW-F00 selection and J4e ownership for new rows, outside check-unit subsets. |
| LD-RW-4 | Accept the scope rule, exact accepted J4a names and nested C-REG step names. |
| LD-RW-5 | Accept explicit #6 kills recorded outside the sampled kill set under the existing full-check rule. |
| LD-RW-6 | Accept each sub-unit integrating its own changed cells and full lead set; J4e adds the typed completion join. |
| LD-RW-7 | Accept scored typed completion codes, final-effect idempotence and the trust-leaf reference condition. |
| LD-RW-8 | Accept one three-child ladder and recovery checks for each killed child that drew an ExecutionId. |
| LD-RW-9 | Accept lawful crash prefixes plus specific mutations and neighbour-object comparison. |
| LD-RW-10 | Accept both ledger-with-WAL variants and the private marker needed to exercise the missing-row case. |
| LD-RW-11 | Accept conservative interim L11 wording with the record follow-up below; the retirement gate remains unchanged. |

These decisions introduce no conflicting application outcome. X9-RW-RF-01 corrects a count outside the decisions themselves. L11 retirement still requires both J4e's complete passing RW lead set, RW-D1/RW-K10 included, and J4c's RW-C5 pins. N-L0 retains the bare-WAL ledger limit; power-loss variants remain L1.

**Nonblocking observations.**

X9-RW-NB-01, RW.3 line 2214: the release-absence explanation overstates what the checker requires. The checker derives scopes from the static registry and requires OPENSIP_X9_ plus those registered owner strings, not every dynamic census scope (check_crash_matrix.py:121–137, :385–387 and :521–524 at 43ea32a). A repair census does not automatically extend releaseAbsence.strings. Correct the explanation to registered-prefix coverage plus the feature-disabled macro's bare-block expansion. Every full repair name contains its registered owner prefix, so the existing prefix byte scan supplies coverage; no release leak was identified. If full dynamic-name scan entries are intended, explicitly assign that extension to J4e.

X9-RW-NB-02, LD-RW-11 at line 2511: deferring L11 reason narrowing until J4e refines J-RW r4:651's interim reason-update sentence. This conservative staging choice is reasonable, with passing RW-F00 records showing actual progress. Record it in the owed J-RW revision alongside LD-RW-6 so this reporting policy is explicit. The two-condition retirement gate is preserved.

**Validation and limits.**

This review used read-only hashes, the full unified diff, accepted-law/source inspection and in-memory JSON/arithmetic checks. Product source was read through git show 43ea32a, the declared drafting base; observed live main had advanced to 2ea15719f8c4c194d47876ec7d0db248bb379523. The accepted J4a diff matched 9c6496aeaca917a489a9ac2bc997c424339f7169942a57559ce717cc0aa60461 and was reconstructed against 1d24900 in memory to inspect the repair blocks. No dirty worktree supplied evidence. Python used 3.14.6 with -I -B at nice -n 19.

Only review.json and REVIEW.md were written under the requested output directory. There were no repository edits, commits, pushes, delegation, Cargo, lane-lock access, crash-matrix executions or build/test lanes. The real OpenSIP home and private 413 UUID fixture were not accessed. Future repair traces, J4b–J4e code, census totals and lead sets remain implementation evidence owed by their units; none was executed here.
