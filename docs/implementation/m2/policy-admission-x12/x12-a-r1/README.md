# X12-A r1 — record amendment to X12's X12d text (corpus target)

2026-11-11. Drafted by a lead-dispatched design author (Claude Opus 5.5, route R2-DEEP, effort medium) from
`LC/x12d-ts/SCOPE-r1.md` §1 and the lead's rulings (`LC/x12d-ts/QUESTIONS.md`, and the coordinator's relays of 2026-11-11).
Status: **PROPOSED, r6.** History: r2 applied rulings on r1's open points; r3 and r5 applied reviews
(`LC/x12d-ts/review-opus-x12a/VERDICT.md`, `VERDICT-r4.md`); r4 took the census `LC/x12d-ts/CENSUS-C0.md`; r6 takes the
coverage map `LC/x12d-ts/COVERAGE-MAP-C1.md` and the lead's rulings on it, and drops disposition (ii). It needs the
cross-vendor review before X12d-TS's C1 freezes (PA1's premise rule, PA1:330-333). It binds nothing and changes no
existing file, registry or lock. Marks: **SETTLED-BY-TEXT** (restates accepted law), **PROPOSED** (needs review).

## Short names

Architecture main `fa6fa0fba`; product main `1bd328f3` (paths without prefix). `LC` = `.opensip-implementation-cache/lead-2026-10-25`.
Lines are those of the accepted bytes; the banner file `PROPOSAL.md` is offset by the number in brackets.

| Name | Document |
|---|---|
| **X12** | `docs/implementation/m2/policy-admission-x12/PROPOSAL-r4.md` (accepted, Grok) [+2] |
| **MC8** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md` (accepted, CODEX2) [+4] |
| **X5** / **I1** | `m2/replay-join-x5/PROPOSAL-r4.md` [+2] / `m3/preview-pack-i1/PROPOSAL-r3.md` [+2] |
| **PA1** / **CEN** / **MAP** | `LC/pa1/PLAN-AMENDMENT-TS1-r3.md` / `LC/x12d-ts/CENSUS-C0.md` / `LC/x12d-ts/COVERAGE-MAP-C1.md` |

FA = host `fact_admission::tests::the_replay_corpus_replays_through_the_join_or_takes_its_row` (`fact_admission_tests.rs:333`);
NO = host `native_owner_tests::independent_run_replay_matches_selected_reference_and_owns_its_closure` (`native_owner_tests.rs:2877`);
COMP = `native_owner_tests::derives_complete_evaluation_candidates_from_retained_inputs` (`:2639`).

**Amended selectors.**
1. X12:266, the units bullet: "regeneration of the synthetic replay corpus onto the bundled test pack, with the M3 Plan
   builder (item 9)". This is the amendment MC8 names: "This is a record amendment to X12 r3's X12d text" (MC8:1101;
   MC8:1152; C4b's edge, MC8:1187).
2. X12 item 9 (X12:214-224) gains one note. Its text stays as X12's own state.
3. MC8:1101 (item 19 part 4), "with an empty `typescript` file population, so the rule evaluates nothing", for the one
   disposition (iii) Run only (A7).

## Clauses

**A1. The corpus target.** *SETTLED-BY-TEXT (MC8:1101):* "onto the bundled test pack" is replaced. After amendment
X12:266 reads: "**X12d (M3), inventory successor.** The Run-closure application of `check_plan_pack` inside replay, and
regeneration of the synthetic replay corpora onto the release preview pack `opensip.preview.typescript.pack:1` under
X12-A's A7, with the M3 Plan builder (item 9; X12-A). Its parts are MC8 item 19. It must land before any analysis
producer can reach X5." *PROPOSED:* A7's dispositions, and "with the M3 Plan builder" read as placement, X12d being
C4's inventory successor (MC8:1097) (O2).

**A2. The reason. SETTLED-BY-TEXT (MC8:1101).** `check_plan_pack` always uses `RELEASE_PACKS`, and the test registry is
`cfg(test)`-private to the evaluator. **Citation correction:** MC8's `policy.rs:1361-1367` is now
`evaluator/src/policy.rs:1410-1416` (:1415), and its `policy.rs:1412` is now `:1461-1463` (`TEST_PACKS`,
`policy_pack_tests.rs:20`).

**A3. Rejected: a test registry reachable downstream. SETTLED-BY-TEXT.** "A feature-gated test registry reachable from
downstream builds. It is a new cfg seam on admission, and needs an X8 and X9 site-list amendment" (MC8:1108). X12:276
forbids "a `cfg(test)` row or test registry reachable from a release build".

**A4. The pins.** *SETTLED-BY-TEXT:* they are "amended, not deleted", and say it is "wired exactly once, in replay"
(MC8:1100; MC8:1114). *PROPOSED:* how they say it.
- The host list `fact_admission_tests.rs:665-681` (`"check_plan_pack"` at :671; MC8's `:661-668`) stays a forbidden list.
  Its comment at :665 is re-cited to X12d.
- `configuration_tests.rs:507` (MC8's `:449-450`) pins the configuration projection. It is unchanged.
- **New evaluator pin** (scope commit C4): `check_plan_pack(` and the detector join each occur exactly once in
  `evaluator/src/replay.rs`, after the seal read (:185-201) and before `derive_evaluation(` (:202).

**A5. Item 9 keeps its text. PROPOSED (form; lead ruling).** Note added after X12:224: "*X12-A:* X12d inserts
`check_plan_pack`, and MC8 item 9's detector join, into `replay_run` after the Plan and seal are read and before
`derive_evaluation` (MC8:1098-1099)."

**A6. Item 10's `check_plan_pack` tests stand. SETTLED-BY-TEXT (X12:245).** They are evaluator unit tests over
`TEST_PACKS`, outside `replay_run`. Their refusal inputs show that X12:288 does not forbid a refusal input (A8).

**A7. The corpora and their dispositions.**
- **Principle. SETTLED-BY-TEXT:** after X12d no replayed Plan names a fixture pack, with no exception (MC8:1098, :1112,
  :1113). *PROPOSED reading:* MC8:1112's "corpus Plan" means a Plan of the replayed corpus (item 19's subject, MC8:1101).
  Fixtures that never reach `replay_run`, and the derive-level tests below, keep their fixture-pack Plans.
- **What the joins meet (CEN §1-2).** Every refusal is `PLAN_POLICY_PACK_NOT_BUNDLED`. All 83 emission rows of the 82
  refused Plans would also fail the detector join: each detector differs from the seal's evaluator closure in more than
  `kind`, and each `contributionId` is `"fixture"`. 63 workspace tests fail, plus 4 in crash-matrix builds only.
  The replayed sources are listed below (CEN §2):
  the host corpus (101 cases, 73 Runs in 51 Plans; FA, plus 2 tests shared with the synthetic); the seal corpus (1 Run,
  `packet-0-original`, also in the host corpus; 19 tests); the evaluator cycle fixture (4 cases in 2 Plans, through its
  test's builder, `atoms.rs:4212-4470`; 1 test); the crash-matrix synthetic builder `run_candidate.rs` (42 + 4 tests).
- **What the host tests assert (MAP §0).**
  - FA asserts three things only: the case replays, a regeneration mismatch, or evidence missing (91, 9 and 1 cases).
  - Verdicts and finding counts are checked by NO, a second host test that reads all 101 cases.
  - No host test turns a replayed Run's verdict into a host outcome row.
  - The only host test that needs a finding is `synthetic_b8_an_altered_claimed_output_never_replays` (`tests/admission_tests.rs:3265`).
- **Dispositions. PROPOSED (lead rulings).** Each case of the three corpora gets exactly one disposition, by the reviewed
  coverage map. **Nothing is deleted or regenerated before the map has been independently reviewed.**
  - **(i) Structure:** regenerated onto the release pack with an empty `typescript` population (MC8:1101). This covers
    the seal-corpus Run, the synthetic's source, the pass base, and cases whose test checks replay, admission, commit,
    bounds or member removal.
  - **(iii) The finding Run:** one fail Run with one `module-import-cycle` finding under the release rule. It is built
    from the cycle fixture's `retained-typescript-self-cycle` case moved onto the release pack (MAP §5), and it also
    serves `synthetic_b8`. The unit first measures that `derive_evaluation` produces the finding on the moved inputs.
    It reaches host tests as a committed fixture, written by the regenerator and drift-checked. Selector 3 amends
    MC8:1101 for this Run only, because a Run that exists to carry a finding cannot carry one with an empty population.
    *Control:* on replay its finding is produced by the release rule over its retained facts, not typed into a fixture.
  - **(iv) Covered elsewhere, strict form:** a case leaves the replayed corpus only when a **named** test asserts its
    evaluation content at the `derive_evaluation` level against the stored outputs, as COMP does. Where that test does
    not exist, the unit writes it before the case leaves. For each such case the unit records what the replay-level walk
    checked that the derive-level test does not (for example the full retained walk over its input shape). Where a (i)
    structure Run with the same input shape keeps that check, the shape is added to (i).
- **Forged cases (X5:157).** The host keeps a forged case for every forging kind the release-pack Runs can express, each
  built by forging one claimed output of a release-pack Run, so the mismatch is the only thing wrong. The kinds the
  rulings name are a forged verdict on the pass Run and on the fail Run, a forged finding on the fail Run, and forged
  deficiencies if an empty-population release Run has any (to be measured). The map lists each of today's 9 forged cases with its new form or why it cannot be expressed. *PROPOSED reading of
  X5:157* ("a tampered output (one byte of a claimed output, the corpus's forged cases) is
  `evidence.regeneration-mismatch`"): one host-replayed case per expressible forging kind. This now yields several
  forged cases, not one.
- **X5 item 8's other host tests each keep a host-replayed case (X5:154-162):** the corpus replays through
  `replay_candidate`; the `missing-blob-…` case and member removal; "a schema or identity failure inside `Input` is
  `EVALUATION.INPUT_REFUSED`"; "the limits test of items 4 and 5e".
- **Boundary.** Every Run passed to `replay_run` (directly or through `replay_candidate` or `finalize`) names the release
  pack, whatever outcome its test expects. The one exemption is a C4-T14 negative (MC8:1117): a regenerated Run with
  exactly one join input re-pointed (pack id, pack count, policy digest, or detector closure), with dependent identities
  re-derived. Every other refusal test asserts its exact diagnostic.
- **Disclosed limit: coverage lost at replay level.** A pass Run with live non-gating findings
  (`selected-nongating-live-findings`) cannot be expressed by the release pack, whose one rule is gating. It is covered
  at the derive level only, and the unit's handoff and the milestone disclosure state this.
- **Fixtures that share these Plans but never reach `replay_run`** (CEN §4; MAP §6) are unchanged. Where a correspondence
  check ties one to the replay corpus (`native-owner-patterns-materialization-r2/runners/check_fixture_correspondence.py`),
  it is kept passing, or amended with the reason stated and reviewed.

**A8. What a corpus Plan must carry. PROPOSED.**
- **A (i) Plan** passes both joins (MC8:1098-1099; MC8:474-476) and whatever `derive_evaluation` requires for the release
  pack with an empty population. That includes the detector being a `semanticClosures` member (`policy.rs:588-597`).
  It need not meet item 18 in full: item 18 binds C4 (MC8:1076), and "a Plan without `typescript.imports` is lawful"
  (MC8:1094). It is a synthetic fixture, not a Plan the product would build.
- **The (iii) Plan** carries item 18's enumeration and `imports` request (MAP §5).
- **Pack provenance. SETTLED-BY-TEXT (X12:288; lead ruling).** X12:288 forbids "a Plan whose `policyPackIds` or
  `policyDigest` did not come from an `AdmittedPack`", with no synthetic exception. So a corpus Plan's pack id, policy
  digest, and committed policy and program come from an `AdmittedPack` produced by the product's real admission over
  `Named("opensip.preview.typescript.pack:1")` (accessors `policy.rs:836-857`). They are never typed and never copied
  from a registry file. A C4-T14 refusal input is lawful as such (X12:245; MC8:1117).

**A9. The generator. PROPOSED (lead ruling: branch (b)).** A drift-checked regenerator in product test support, labelled
synthetic, beside `run_candidate.rs` (:15-19). It re-derives with `derive_evaluation` from today's `*.native-owner-r1*.json`
files. The step that sets a Plan's pack fields and re-derives the dependent identities holds an `AdmittedPack`.
- **Diff control.** Each regenerated Run gets a recorded comparison with its predecessor, under the old-to-new identity
  map. Every differing record must be one the pack or the detector closure reaches: the Plan, the analysis-spec, the
  policy and program, the emission row, the detector closure, `semanticClosures`, the identities derived from them,
  the re-derived outputs and the seal. For the (iii) Run the population is also covered. Nothing else differs, and
  labels are unchanged.
- **Crash-matrix rebinding.** `bound_to` (`run_candidate.rs:279-290`), `bind` (:338; closure map :376-384) and
  `renaming_the_evaluator_closure` (:544) swap in `CommitSession::core_evaluator_closure`. They must also rebind every
  emission row's detector closure to that descriptor with `kind: "detector"`, retained and a `semanticClosures` member,
  before the fixpoint rewrite (MC8:475; lead ruling Q6). This is done with C1. It reaches the F01 row and the lead sets,
  whose changed expectations are re-transcribed under S12 before review.

**A10. Edges and the lead set. SETTLED-BY-TEXT.** "X12d depends on I1-c (the row) and I1-b2 (the op)" (MC8:1102). Both
are integrated (`m3/IMPLEMENTATION-STATUS.md:249`). "A full X9 matrix lead set on X12d's commit (`matrixPass: true`). It
is serialized with every other lead run set" (MC8:1103).

**A11. Row and carrier.** Row **SETTLED-BY-TEXT**: `EVALUATION.INPUT_REFUSED`, X5 item 5's structural row (MC8:1098-1099;
X12:218; X5:77). Carrier **PROPOSED** (lead ruling Q1): `ReplayError::Structure(RetainedWalkError::Policy(e))`
(`replay.rs:20`; `full_walk.rs:40`) for both joins, under `limits.retained.owner` (`replay.rs:171`); no new variant.

## What X12d must do: MC8 item 19 in full, as amended here

- **Parts** (MC8:1098-1103): 1, the pack join "after reading the Plan and before `derive_evaluation`"; 2, "Item 9's join
  is wired at the same point, with the same row" (scope commit C2); 3, the pins (A4); 4, the corpus (A7); 5, the edges;
  6, the serialized X9 lead set (A10).
- **Forbidden** (MC8:1112-1115): "a corpus Plan naming `"fixture"` after X12d"; "a replay path without the join";
  "deleting the pin tests rather than amending them"; "X9 evidence from an earlier commit offered for X12d".
- **Controls** (MC8:1117-1119): "C4-T14: replay refuses an unbundled pack, a wrong digest, and a detector from another
  core"; "C4-T15: the regenerated corpus replays"; "C4-T16: the X9 matrix passes on the X12d commit"; also A4's pin, the
  reviewed coverage map, the (iii) control and A9's diff control.

## Rejected alternatives

- **Disposition (ii), keeping fixture packs behind an evaluator-private replay entry** (MAP §0 item 3; lead ruling). "A
  registry row's `packId` must be `<name>:<version>`", while every corpus Plan names `fixture.file-observed` or
  `fixture.semantic-atom`, "with no version, so no lawful test row can match them". The 50 `fixture.file-observed`
  Plans carry "28 distinct `policyDigest`s", against one row's `policySha256`. "The detector join then refuses every
  row", and fixing it "changes every finding id, because a finding's `ruleClosure` is the emission row's
  `detectorClosure`". So a (ii) Run "can only be replayed after the same identity rewrite and re-derivation that (i)
  needs".
- **The original runner as generator.** The census found it cannot run today and cannot target the release pack, and the
  reference models hardcode the fixture packs (CEN §3; QUESTIONS Q7).
- **All corpora onto an empty population** (r1-r2). This would erase the forged-content negatives and every finding.

## What this record does not do

It adds no law beyond MC8 item 19, except selector 3. It does not cover Rust Plans (X12d-RS; PA1 §1.2: "Must not claim:
X12d complete; the join exercised on a Rust Plan"). It does not settle how the Plan build receives the pack: that is the
provider-request unit's, by a separate lead ruling (the typed `&AdmittedPack`, per X12:208, "only from an
`AdmittedPack`", and X12:288; MC8:923 says "from", not "only from").

## Open points

- **O1. Nothing checks the pack at replay today** (`replay.rs:177-202`); the Plan build checks only caller-supplied
  strings (`host/src/plan.rs:312-340`). No TS1 Run counts as M3-M-TS1 before X12d-TS lands: X12:222, X12:266; MC8:1109,
  :1113; PA1:142.
- **O2. "With the M3 Plan builder" (X12:266; X12:220).** This record reads it as placement (MC8:1097). Read instead as
  "built by the Plan builder", it would require every corpus Plan to meet item 18 in full. Part a's builder is on main
  (QUESTIONS Q3).

## Consequences

X12d-TS works under MC8 item 19 in full, as amended by A1-A11. Until the coverage map is reviewed, only non-destructive
work goes ahead (the regenerator's code, the measurements, the derive-level tests). C1 may be drafted, not frozen,
before this record is accepted.
