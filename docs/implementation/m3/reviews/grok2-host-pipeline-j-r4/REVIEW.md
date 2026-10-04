# GROK2 review: M3-J1 r4, guarded durable host pipeline

**Verdict: ACCEPT.**

Subject: `docs/implementation/m3/host-pipeline-j/PROPOSAL.md`, 120506 bytes, sha256 `c18c0d3c92ec9a1c029456aaa68e2785f0a17840aab93024f265e1789843fa32`. Diff base: `PROPOSAL-r3.md`, 111561 bytes, sha256 `ad887c9015c3a7863a43472b8438a0c5f7c4b0c4fc53b1996584644757bad286`, the r3 bytes without the acceptance note. Source of the amendment: M3-D r3 `supervisor-d/PROPOSAL-r3.md`, 169430 bytes, sha256 `9679dbc4eec3081cce37f4e2333d4f1f6aecc4df19f0540b157439bd158a8771`. Single reviewer. Law review. No product cargo or tests. All 16 pins in `hashes.txt` matched. `~/Library/Application Support/OpenSIP` was absent.

The r3-to-r4 diff is the round header, the r4-changes table, the M3D short name, row R10a and its bullet, J-β, ER10a and the ephemeral-draw bullet, the item 11 record correction, successors S19 and S20, and one forbidden-substitute line.

## Placement

R10a sits between R10 and R11 (PROPOSAL.md:325). R10's fenced first read has yielded the authenticated trust view. R11's handoff and R12's `CommitSession::open` draw have not run, so the fence is still held. A refusal draws and reserves no analysis-attempt ExecutionId, opens no handoff, lease, or session, and does not call `refused()` or `finish`. Step 0 ends on the refusal, and step 1 projects it, which is 5.2's rule that a refusal at any join ends step 0 and step 1's `terminal` gate then projects it (PROPOSAL.md:340, :367).

J1 places the row. M3-D item 24 owns what it admits and refuses (M3D:717-734). The order-table summary matches that item: every component manifest the trust view admits and the analysis step can select; refusals of EE-1, EE-3b, EE-4's manifest part, and EE-5a as `ExcludedForm {class, subject}`. The row ends with that admitted set, which M3-C item 16 row 8 selects from. It does not wait for the Plan, because selection needs discovery after R12 (M3D:718). CH14:433 is the `components/manifest.rs` validator that admits selected component capabilities and manifest shape after authenticated closure association. Item 25 is untouched: R1 stays before any draw (M3D:750, :761). J-β's range is R4–R10a, with M3D item 24 added as owner (PROPOSAL.md:372).

## Ephemeral draw

ER10a is the last bullet of the fenced "I complete" list, after X4T's report-only trust admission and before the sentence that releases the read session (PROPOSAL.md:426, :428). The ephemeral attempt starts, and therefore draws and reserves its ExecutionId, only after ER10a returns (PROPOSAL.md:431). Item 2 still places that draw at the attempt's start (PROPOSAL.md:178, :189). SD-6 requires the ephemeral counterpart before the ephemeral attempt's draw (M3D:720, :1092). That lower bound is enough, and the admission stays under the read session's fence.

With no trust view, ER10a admits nothing and refuses nothing. M3D:720 names E-3. J1 also names E-4. J1's own E-4 row already says an absent F under an ephemeral read session is no trust view, and E-3 covers I absent or F absent (PROPOSAL.md:440-441). The added name applies that join.

## First-use exception and J-C10b

The exception quotes M3D:722 and then restates it (PROPOSAL.md:341). On route 3b, `mint_intent` is step 1, before the creator act ends `Published`, `LostRace`, or `NotPristine` (PROPOSAL.md:233-235). The prelude's reservation is made there, before P0 is staged (PROPOSAL.md:187). It can already be in `ExecutionIdReservations` when R10a runs, for each of those three results. It names the creation act only. Item 2 rejects binding it to the analysis attempt (PROPOSAL.md:199). R10a's no-draw property is about the analysis attempt's ExecutionId.

J-C10b samples the registry when R10a or ER10a returns its refusal, before step 1's render draw (PROPOSAL.md:343-347). The set equals the set at entry: empty on 3a and on the ephemeral path, and the prelude's alone on 3b. That is D4-T1's placement half (M3D:743-746). The render draw is a later host reservation at the render attempt's start (PROPOSAL.md:179, :189), and J-C4b already counts it as distinct from the prelude and the session (PROPOSAL.md:218). On the refusal path R11 and R12 never run, so `x3d.session.execution-draw` is never reached, and the ephemeral attempt never starts. The `firstUse: true` disclosure is asserted only when `created` is `Some`, which is item 9 (PROPOSAL.md:619). `LostRace` and `NotPristine` keep the prelude reservation and carry `firstUse: false`.

The quoted `(J1:161)` is M3-D's citation of the r3 snapshot. In r3 that line is the prelude sentence. r4 restates the same rule by item 2 and S4.

## Route

The internal refusal is `ExcludedForm {class, subject}`. Its public projection is J1's, with existing codes, under M3-D successor SD-5, recorded here as S20 (PROPOSAL.md:339, :774). M3-D recommends request-rejected 2 with `EXTENSION.ADMISSION_REJECTED` (M3D:733). SL:1306 is that admission-family row. No public code is added, and item 10 grows no row in this round.

S20 says that until it lands, item 10 has no row for the internal refusals M3-D assigns to J1's projection, R10a's and ER10a's `ExcludedForm` among them, and J2a's projection of them is incomplete. It gates J2a's projection of those refusals, and J3d's R10a wiring and J2c's ER10a wiring, each with D4. SD-5's content is that whole set: `ExcludedForm`, `MemoryBudgetBelowCeiling`, `ToolOutputBound`, `ToolScratchBound`, and `confinement-refused`, landing with J2 (M3D:1091). Item 10's totality rule, that a detail with no row is a model error, is kept by that gate. The same law already gates output wiring on S18 and the bounded projections on S-B. Leaving the matrix row to S20 is lawful.

## Record correction

The resume-writer recommendation no longer says a `repair recover` command is M5 (PROPOSAL.md:721-722). `repair-recover` is `opensip repair recover REQUEST-ID [--apply-recovery]` (CINV:988-989). WS:1024 is the closed recovery table over the source-repair journal states. SL:673 puts `repair recover --apply-recovery` under S10.2. BP:973 assigns `repair-recover` to `crates/host/src/repair.rs`. That command is source-repair journal recovery. J-RW r1 records the same correction at X-RW-8 and in its record-corrections section. r4 records it and leaves J-C22 with J-RW. The re-commit paragraph is unchanged.

## Scope, and what acceptance covers

S19 matches the companion M3-C r7 text: item 16 row 8 becomes a selection among manifests R10a or ER10a admitted, adds no admission of its own, and leaves M3-C item 9's core role closures unchanged (M3-C PROPOSAL.md:32, :871). M3-C r7 is reviewed separately. The M3C short name still points at accepted r5.

Accepting r4 accepts this amendment: the placement of R10a and ER10a, J-C10b, S19 and S20 as records, and the item 11 correction. J-BS, S18, and units J2a–J3d still need their own reviews. D4's integration still waits on this amendment (M3D:1133).

## Non-blocking

**NBO-1.** PROPOSAL.md:78 says the live `supervisor-d/PROPOSAL.md` is byte-identical to `PROPOSAL-r3.md` on 2026-10-04. Live is 169909 bytes, sha256 `47652e47952bddd3423fda39c94db663864cd1346b52edcbfe2574318c60f202`. It adds the acceptance paragraph and corrects the r1 RF-4 history sentence. The cited item 24, item 25, SD-5, SD-6, F11, and D4-gate text are unchanged, and the short name's hash still names the preserved r3 file. The sentence does not change a rule of this amendment.
