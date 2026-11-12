# X12-A r1 — record amendment to X12's X12d text (corpus target)

2026-11-11. Drafted by a lead-dispatched design author (Claude Opus 5.5, route R2-DEEP, effort medium) from
`LC/x12d-ts/SCOPE-r1.md` §1 and the lead's rulings (`LC/x12d-ts/QUESTIONS.md`, and the coordinator's relays of 2026-11-11).
Status: **PROPOSED, r4.** History: r2 applied the lead's rulings on r1's open points. r3 applied the independent review
`LC/x12d-ts/review-opus-x12a/VERDICT.md` (RF-1 to RF-6). r4 fixes the corpus split from the census
`LC/x12d-ts/CENSUS-C0.md` under "Lead rulings 2026-11-12 after the census" (QUESTIONS.md:66-99). It needs the
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
| **PA1** / **CEN** | `LC/pa1/PLAN-AMENDMENT-TS1-r3.md` / `LC/x12d-ts/CENSUS-C0.md` |

**Amended selectors.** (1) X12:266, the units bullet: "regeneration of the synthetic replay corpus onto the bundled test
pack, with the M3 Plan builder (item 9)". (2) X12 item 9 (X12:214-224) gains one note; its text stays as X12's own state.
(3) **MC8:1101 (item 19 part 4), "with an empty `typescript` file population, so the rule evaluates nothing", for
disposition (iii) only (A7).** (1) is the amendment MC8 names: "This is a record amendment to X12 r3's X12d text"
(MC8:1101; MC8:1152; C4b's edge, MC8:1187).

## Clauses

**A1. The corpus target.** *SETTLED-BY-TEXT (MC8:1101):* "onto the bundled test pack" is replaced. X12:266 reads, after
amendment: "**X12d (M3), inventory successor.** The Run-closure application of `check_plan_pack` inside replay, and
regeneration of the synthetic replay corpora under X12-A's A7, with the M3 Plan builder (item 9; X12-A). Its parts are
MC8 item 19. It must land before any analysis producer can reach X5." *PROPOSED:* A7's dispositions (selector (3)), and
"with the M3 Plan builder" read as placement, X12d being C4's inventory successor (MC8:1097) (O2).

**A2. The reason. SETTLED-BY-TEXT (MC8:1101).** `check_plan_pack` always uses `RELEASE_PACKS`, and the test registry is
`cfg(test)`-private to the evaluator. **Citation correction:** MC8's `policy.rs:1361-1367` is now
`evaluator/src/policy.rs:1410-1416` (:1415); its `policy.rs:1412` is now `:1461-1463`, which holds `TEST_PACKS`
(`policy_pack_tests.rs:20`; one row, `opensip.test.fixture.pack:1`).

**A3. Rejected: a test registry reachable downstream. SETTLED-BY-TEXT.** "A feature-gated test registry reachable from
downstream builds. It is a new cfg seam on admission, and needs an X8 and X9 site-list amendment" (MC8:1108); "a
`cfg(test)` row or test registry reachable from a release build" (X12:276).

**A4. The pins.** *SETTLED-BY-TEXT:* "amended, not deleted", "wired exactly once, in replay" (MC8:1100; MC8:1114).
*PROPOSED,* how they say it: the host list `fact_admission_tests.rs:665-681` (`"check_plan_pack"` at :671; MC8's
`:661-668`) stays a forbidden list, its comment at :665 re-cited to X12d; `configuration_tests.rs:507` (MC8's `:449-450`)
is unchanged, since it pins the configuration projection; **a new evaluator pin** (scope commit C4): `check_plan_pack(`
and the detector join each occur exactly once in `evaluator/src/replay.rs`, after the seal read (:185-201) and before
`derive_evaluation(` (:202).

**A5. Item 9 keeps its text. PROPOSED (form; lead ruling).** Note added after X12:224: "*X12-A:* X12d inserts
`check_plan_pack`, and MC8 item 9's detector join, into `replay_run` after the Plan and seal are read and before
`derive_evaluation` (MC8:1098-1099)."

**A6. Item 10's `check_plan_pack` tests stand. SETTLED-BY-TEXT (X12:245).** They are evaluator unit tests over
`TEST_PACKS`, outside `replay_run`. Their refusal inputs show X12:288 does not forbid a refusal input (A8).

**A7. The corpora and their dispositions.**
- **Principle. SETTLED-BY-TEXT.** After X12d, no Run that reaches replay in any build outside the evaluator crate's own
  unit tests names a non-release pack (MC8:1098, :1112, :1113).
- **What the joins meet (CEN §1-2).** Every refusal is `PLAN_POLICY_PACK_NOT_BUNDLED`: no replayed Plan names a bundled
  pack. **All 83 emission rows** of the 82 refused Plans would also fail the detector join: each detector descriptor
  differs from the seal's evaluator closure in more than `kind`, and each `contributionId` is `"fixture"`, not in the
  release row's `["opensip.preview.typescript"]`. So every replayed Run changes its pack, policy, detector and
  contribution, whatever its disposition. **63 workspace tests, plus 4 in crash-matrix builds only (67), fail.**

| Source reaching `replay_run` | Runs / Plans | Failing tests |
|---|---|---|
| host `tests/fixtures/replay-fixtures.native-owner-r1.json` (101 cases) | 73 Runs in 51 Plans (69 `fixture.file-observed`, 4 `fixture.semantic-atom`) | 1 test of its own (`fact_admission::tests::the_replay_corpus_replays_through_the_join_or_takes_its_row`), plus 2 shared with the synthetic (`admission_tests::synthetic_b1_…`, `synthetic_b8_…`) |
| security `tests/fixtures/journal-seal-replay.native-owner-r1.json` | 1 Run, `packet-0-original`, the same Run as in the host corpus (23 objects, 46 blobs) | 19 (security 13, host 5, storage 1) |
| evaluator `tests/fixtures/cycle-representative.native-owner-r1.v1.json` `retainedCases`, through the cycle test's builder (`atoms.rs:4212-4470`) | 4 cases in 2 Plans (`fixture.semantic-atom`) | 1 |
| crash-matrix synthetic builder `storage/src/crash_matrix_support/run_candidate.rs`, from `packet-0-original` | in memory, per session | 42 + 4 crash-matrix only |

- **Dispositions. PROPOSED (lead ruling).** Each case of the three corpora gets exactly one, by a reviewed **coverage
  map**: what the case tests, where the same content is already tested without `replay_run`, and its disposition. The
  map is X12d-TS's deliverable, not this record's. **Nothing is deleted or regenerated before it exists and is reviewed.**
  - **(i) Structure:** regenerated onto `opensip.preview.typescript.pack:1` with an empty `typescript` population
    (MC8:1101): the seal-corpus Run, the synthetic's source, and cases whose test checks replay, admission, commit,
    bounds or member removal.
  - **(ii) Evaluator content:** keeps its fixture pack and is replayed only through an evaluator-private `#[cfg(test)]`
    entry that runs `replay_run`'s own body over the test registry, as `check_plan_pack_in` does for `check_plan_pack`
    (`policy.rs:1415-1417`). Not MC8:1108's seam: a `#[cfg(test)]` item compiles only in the evaluator's own unit-test
    build, never downstream or in a release build (X12:276); the `cfg(test)` registry is X12a's (X12:252). Both joins
    still run (MC8:1113), and the `ReplayedRun` is built only in `replay_run`'s body (X5:188). *Conditions:* a test
    registry row per fixture pack, whose document hashes to the Plan's `policyDigest` (`TEST_PACKS` holds neither
    fixture pack today), and the detector rebound to the evaluator closure (the 83-row finding applies here too).
  - **(iii) A host outcome row that needs findings:** one representative Run per distinct row a host test asserts, on
    the release pack with a **non-empty** population yielding findings by the release rule, built by product fixture
    builders (whether the evidence-capture unit's world builders can serve, and which pack their world names, is the
    map's to establish). **Selector (3) amends MC8:1101 for these Runs only**, because a Run that exists to carry findings
    cannot carry them with none. These Plans need item 18's EnumerationPlan and symbol inventories (MC8:1079-1082), or
    "Every subject would then be indeterminate" (MC8:1089).
  - **(iv) Duplicate:** content fully covered elsewhere at the level it matters; dropped from the replayed corpus, with
    a pointer to the covering test.
  - *Aim:* the host keeps one replayed Run per outcome row it maps and its structure negatives, evaluation content is
    tested where the evaluator owns it, and no coverage disappears without a named replacement. **X5 item 8's host
    tests bound the map:** the corpus replays through `replay_candidate`, "the corpus's forged cases" are
    `evidence.regeneration-mismatch`, the `missing-blob-…` case, and member removal over one corpus case (X5:154-160).
    Each keeps at least one host-replayed case.
- **Boundary.** Every Run passed to `replay_run` (directly or through `replay_candidate` or `finalize`) names the release
  pack, or in (ii) a test-registry pack, whatever outcome its test expects. The only exemption is a C4-T14 negative
  (MC8:1117): a regenerated Run with exactly one join input re-pointed (pack id, pack count, policy digest, or detector
  closure), with the dependent identities re-derived. Every other refusal test asserts its exact diagnostic.
- **Fixtures that share these Plans but never reach `replay_run`** (CEN §4: the `composition-`, `enumeration-join-`,
  `evaluator-parameter-`, `execution-input-`, `full-walk-`, `input-structure-`, `plan-input-` and `reconstruction-`
  fixtures, and `evaluator/tests/fixtures/policy-pack-plan-fixture.json`): unchanged. Where a correspondence check ties
  one to the replay corpus (the architecture's `native-owner-patterns-materialization-r2/runners/check_fixture_correspondence.py`),
  the check is kept passing, or amended with the reason stated and reviewed.

**A8. What a corpus Plan must carry. PROPOSED.** An (i) Plan passes both joins (MC8:1098-1099; MC8:474-476) and what
`derive_evaluation` requires for the release pack with an empty population (at least `policy.rs:588-597`,
`composition.rs:765-778`). It need not meet item 18 in full: item 18 binds C4 (MC8:1076), and "a Plan without
`typescript.imports` is lawful" (MC8:1094). A (iii) Plan meets what its findings need (A7).
- **Pack provenance. SETTLED-BY-TEXT (X12:288; lead ruling).** "A Plan whose `policyPackIds` or `policyDigest` did not
  come from an `AdmittedPack`" is forbidden, with no synthetic exception. A corpus Plan's pack id, policy digest, and
  the committed policy and program come from an `AdmittedPack` from the product's real admission (`admit_pack` over
  `Named("opensip.preview.typescript.pack:1")`, accessors `policy.rs:836-857`; in (ii), the evaluator's admission over
  the test registry). They are never typed and never copied from a registry file. A C4-T14 refusal input is lawful as
  such (X12:245; MC8:1117).
- **What an (i) Plan does not show.** It is a synthetic fixture, not a Plan the product would build, and shows nothing of
  item 18 or of rule evaluation. C4-T11, C4-T12 and C4-T14's TS leg do.

**A9. The generator. PROPOSED (lead ruling: branch (b)).** A drift-checked regenerator in product test support,
labelled synthetic, beside `run_candidate.rs` (:15-19), re-deriving with `derive_evaluation`. Its inputs are today's
`*.native-owner-r1*.json` files. The step that sets a Plan's pack fields and re-derives the dependent identities holds
an `AdmittedPack` (A8). The reference models are not extended in this unit.
- **Diff control.** For every regenerated Run, a recorded comparison with its predecessor under the old-to-new identity
  map. It shows that each differing record is one the pack or the detector closure reaches: the Plan, the analysis-spec,
  the committed policy and program, the emission row, the detector closure, `semanticClosures`, the identities derived
  from them, the re-derived outputs and the seal; in (iii) also the population and what derives from it. Nothing else
  differs. Labels are unchanged, and in (i) and (ii) so are the non-identity expectations.
- **Crash-matrix rebinding.** `bound_to` (`run_candidate.rs:279-290`), `bind` (:338; the closure map at :376-384) and
  `renaming_the_evaluator_closure` (:544) swap in `CommitSession::core_evaluator_closure`. They must also rebind every
  emission row's detector closure to that descriptor with `kind: "detector"`, retained and a `semanticClosures` member,
  before the fixpoint rewrite, or every crash-matrix candidate fails the join (MC8:475; lead ruling Q6). This is done
  with C1. It reaches the F01 row and the lead sets, whose changed expectations are re-transcribed under S12 before review.

**A10. Edges and the lead set. SETTLED-BY-TEXT.** "X12d depends on I1-c (the row) and I1-b2 (the op)" (MC8:1102), both
integrated (`m3/IMPLEMENTATION-STATUS.md:249`). "A full X9 matrix lead set on X12d's commit (`matrixPass: true`). It is
serialized with every other lead run set" (MC8:1103).

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
  core"; "C4-T15: the regenerated corpus replays"; "C4-T16: the X9 matrix passes on the X12d commit"; plus A4's pin, A7's
  coverage map and A9's diff control.

## Rejected alternatives

- **A9 branch (a), the original runner** (CEN §3; QUESTIONS Q7). (1) The located runners are one-shot schema-digest
  migrations, exact string substitution plus rehash, with "expected verdicts not rewritten" as a precondition. A pack
  change rewrites every proof, finding and verdict. (2) They cannot run today: `run_fixture_authoring.py:3` requires
  `OPENSIP_LEAD_HOLDS_LANE_LOCK=1`, and the recipes read a worktree that is gone. (3) The assembler of the 101-case
  pooled corpus was not found. (4) The reference models hardcode `fixture.file-observed` / `fixture.semantic-atom`
  (`evaluator_graph_fixture.v3.py`, `evaluator_semantic_fixture.v3.py:458`), and none implements `cycle-representative`.
- **All corpora onto an empty population** (r1-r2's A7). It would erase the host corpus's 93 findings and forged-content
  negatives and the cycle cases' verdicts.

## What this record does not do

It adds no law beyond MC8 item 19, except selector (3) for (iii). It does not cover Rust Plans (X12d-RS; PA1 §1.2: "Must
not claim: X12d complete; the join exercised on a Rust Plan"), and it does not settle how the Plan build receives the pack.

## Open points

- **O1. Today nothing checks the pack at replay, and the first Run waits for X12d-TS.** `replay_run` reads the Plan
  (`replay.rs:177-180`) and calls `derive_evaluation` (:202) with no pack check. The Plan build compares its pack fields
  with caller-supplied strings (`host/src/plan.rs:156-157`, :312-340), and its `check_plan_pack` call is `#[cfg(test)]`
  (:968, :1024). No TS1 Run counts as M3-M-TS1 before X12d-TS lands: X12:222, X12:266; MC8:1109, :1113; PA1:142.
- **O2. "With the M3 Plan builder" (X12:266; X12:220).** This record reads it as placement (MC8:1097). Read instead as
  "built by the Plan builder", every corpus Plan would meet item 18 in full. Part a's builder is on main (QUESTIONS Q3),
  and (iii) already needs most of item 18.

## Consequences

- **X12d-TS** works under MC8 item 19 in full, as amended by A1-A11. The coverage map precedes C1's regeneration. C1 may
  be drafted, not frozen, before this record is accepted.
- **The provider-request unit** (and J2b-TS): by a separate lead ruling, its entry takes the typed `&AdmittedPack`, not
  strings. "The future M3 Plan builder takes the policy only from an `AdmittedPack`" (X12:208), and X12:288, above.
  MC8's Plan table says "`policyPackIds` from the `AdmittedPack` (item 18)" (MC8:923): "from", not "only from".
