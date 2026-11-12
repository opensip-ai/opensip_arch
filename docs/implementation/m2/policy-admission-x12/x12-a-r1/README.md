# X12-A r1 — record amendment to X12's X12d text (corpus target)

2026-11-11. Drafted by a lead-dispatched design author (Claude Opus 5.5, route R2-DEEP, effort medium) from
`LC/x12d-ts/SCOPE-r1.md` §1 and the lead's rulings (`LC/x12d-ts/QUESTIONS.md`, and the coordinator's relays of 2026-11-11).
Status: **PROPOSED, r5.** History: r2 applied rulings on r1's open points; r3 applied review `LC/x12d-ts/review-opus-x12a/VERDICT.md`;
r4 fixed the corpus split from the census `LC/x12d-ts/CENSUS-C0.md` (QUESTIONS.md:66-99); r5 applies the re-check
`VERDICT-r4.md` (R1-R3) and the lead's ruling that disposition (ii) is not the default. It needs the cross-vendor review
before X12d-TS's C1 freezes (PA1's premise rule, PA1:330-333). It binds nothing and changes no existing file, registry
or lock. Marks: **SETTLED-BY-TEXT** (restates accepted law), **PROPOSED** (needs review).

## Short names

Architecture main `fa6fa0fba`; product main `1bd328f3` (paths without prefix). `LC` = `.opensip-implementation-cache/lead-2026-10-25`.
Lines are those of the accepted bytes; the banner file `PROPOSAL.md` is offset by the number in brackets.

| Name | Document |
|---|---|
| **X12** | `docs/implementation/m2/policy-admission-x12/PROPOSAL-r4.md` (accepted, Grok) [+2] |
| **MC8** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md` (accepted, CODEX2) [+4] |
| **X5** / **I1** | `m2/replay-join-x5/PROPOSAL-r4.md` [+2] / `m3/preview-pack-i1/PROPOSAL-r3.md` [+2] |
| **PA1** / **CEN** | `LC/pa1/PLAN-AMENDMENT-TS1-r3.md` / `LC/x12d-ts/CENSUS-C0.md` |

**Amended selectors.**
1. X12:266, the units bullet: "regeneration of the synthetic replay corpus onto the bundled test pack, with the M3 Plan
   builder (item 9)". This is the amendment MC8 names: "This is a record amendment to X12 r3's X12d text" (MC8:1101;
   MC8:1152; C4b's edge, MC8:1187).
2. X12 item 9 (X12:214-224) gains one note; its text stays as X12's own state.
3. MC8:1101 (item 19 part 4), "with an empty `typescript` file population, so the rule evaluates nothing": for
   disposition (iii) only (A7).
4. **Only if disposition (ii) is used (A7):** MC8:1112, "a corpus Plan naming `"fixture"` after X12d", narrowed to
   builds outside the evaluator's own unit tests; and X5:188, "A `ReplayedRun` built anywhere but `replay_run`", read
   as admitting `replay_run`'s own private body shared with one `#[cfg(test)]` entry.

## Clauses

**A1. The corpus target.** *SETTLED-BY-TEXT (MC8:1101):* "onto the bundled test pack" is replaced. X12:266 reads, after
amendment: "**X12d (M3), inventory successor.** The Run-closure application of `check_plan_pack` inside replay, and
regeneration of the synthetic replay corpora under X12-A's A7, with the M3 Plan builder (item 9; X12-A). Its parts are
MC8 item 19. It must land before any analysis producer can reach X5." *PROPOSED:* A7's dispositions, and "with the M3
Plan builder" read as placement, X12d being C4's inventory successor (MC8:1097) (O2).

**A2. The reason. SETTLED-BY-TEXT (MC8:1101).** `check_plan_pack` always uses `RELEASE_PACKS`, and the test registry is
`cfg(test)`-private to the evaluator. **Citation correction:** MC8's `policy.rs:1361-1367` is now
`evaluator/src/policy.rs:1410-1416` (:1415); its `policy.rs:1412` is now `:1461-1463`, which holds `TEST_PACKS`
(`policy_pack_tests.rs:20`; one row, `opensip.test.fixture.pack:1`).

**A3. Rejected: a test registry reachable downstream. SETTLED-BY-TEXT.** "A feature-gated test registry reachable from
downstream builds. It is a new cfg seam on admission, and needs an X8 and X9 site-list amendment" (MC8:1108); "a
`cfg(test)` row or test registry reachable from a release build" (X12:276).

**A4. The pins.** *SETTLED-BY-TEXT:* "amended, not deleted", "wired exactly once, in replay" (MC8:1100; MC8:1114).
*PROPOSED,* how they say it. The host list `fact_admission_tests.rs:665-681` (`"check_plan_pack"` at :671; MC8's
`:661-668`) stays a forbidden list, and its comment at :665 is re-cited to X12d. `configuration_tests.rs:507` (MC8's
`:449-450`) pins the configuration projection and is unchanged. **The new evaluator pin** (scope commit C4) has two forms:
- *without (ii):* `check_plan_pack(` and the detector join each occur exactly once in `evaluator/src/replay.rs`, after
  the seal read (:185-201) and before `derive_evaluation(` (:202);
- *with (ii):* the release `replay_run` calls the shared body exactly once, with `&RELEASE_PACKS`. The body calls the
  registry-taking pack join and the detector join each exactly once, after the seal read and before
  `derive_evaluation(`. The only other caller is one `#[cfg(test)]` entry. No production code can pass another registry:
  the body is private and the test registry is `cfg(test)`, which the compiler enforces and a text scan only confirms.

**A5. Item 9 keeps its text. PROPOSED (form; lead ruling).** Note added after X12:224: "*X12-A:* X12d inserts
`check_plan_pack`, and MC8 item 9's detector join, into `replay_run` after the Plan and seal are read and before
`derive_evaluation` (MC8:1098-1099)."

**A6. Item 10's `check_plan_pack` tests stand. SETTLED-BY-TEXT (X12:245).** They are evaluator unit tests over
`TEST_PACKS`, outside `replay_run`. Their refusal inputs show X12:288 does not forbid a refusal input (A8).

**A7. The corpora and their dispositions.**
- **Principle. SETTLED-BY-TEXT:** after X12d no replayed Plan names a fixture pack (MC8:1098, :1112, :1113). Disposition
  (ii), if used, narrows this to builds outside the evaluator's own unit tests: **PROPOSED**, selector 4.
- **What the joins meet (CEN §1-2).** Every refusal is `PLAN_POLICY_PACK_NOT_BUNDLED`. **All 83 emission rows** of the 82
  refused Plans would also fail the detector join: each detector descriptor differs from the seal's evaluator closure in
  more than `kind`, and each `contributionId` is `"fixture"`, outside `["opensip.preview.typescript"]`. Every replayed
  Run therefore changes its detector, and its pack too in all dispositions but (ii). 63 workspace tests fail, plus 4 in
  crash-matrix builds only.

| Source reaching `replay_run` (CEN §2) | Runs / Plans | Failing tests |
|---|---|---|
| host `tests/fixtures/replay-fixtures.native-owner-r1.json`, 101 cases | 73 / 51 | 1 of its own (`the_replay_corpus_replays_through_the_join_or_takes_its_row`) + 2 shared with the synthetic |
| security `tests/fixtures/journal-seal-replay.native-owner-r1.json` | 1 (`packet-0-original`, also in the host corpus) | 19 |
| evaluator `cycle-representative.native-owner-r1.v1.json`, through its test's builder (`atoms.rs:4212-4470`) | 4 cases / 2 | 1 |
| crash-matrix synthetic builder `storage/src/crash_matrix_support/run_candidate.rs` | in memory, per session | 42 + 4 |

- **Dispositions. PROPOSED (lead rulings).** Each case of the three corpora gets exactly one, by a reviewed **coverage
  map** (X12d-TS's deliverable, not this record's). The map records what the case tests, where the same content is tested
  without `replay_run`, and its disposition. **Nothing is deleted or regenerated before the map exists and is reviewed.**
  **The default set is (i), (iii) and (iv)**, under which no Plan names a fixture pack after X12d, as MC8:1112 says.
  - **(i) Structure:** regenerated onto `opensip.preview.typescript.pack:1` with an empty `typescript` population
    (MC8:1101): the seal-corpus Run, the synthetic's source, and cases whose test checks replay, admission, commit,
    bounds or member removal.
  - **(iii) A host outcome row that needs findings:** one representative Run per distinct row a host test asserts, on the
    release pack with a **non-empty** population. Selector 3 amends MC8:1101 for these Runs only: a Run that exists to
    carry findings cannot carry them with none. Its builder is product fixture builders in host test support; whether
    the evidence-capture unit's world builders serve, and which pack their world names, is the map's to establish. These
    Plans need item 18's EnumerationPlan and symbol inventories (MC8:1079-1082), or "Every subject would then be
    indeterminate" (MC8:1089). **Control:** on replay, each representative Run's findings are produced by the release
    rule over its retained facts, not typed into a fixture, and the map names the findings each Run must yield.
  - **(iv) Duplicate:** the content is fully covered elsewhere at the level it matters. The case is dropped from the
    replayed corpus, with a pointer to the covering test.
  - **(ii) Evaluator content, only by exception:** a case the map lists by name, with the text that requires its coverage
    at replay level, where none of (i), (iii) or (iv) can keep it. It keeps its fixture pack and is replayed only through
    an evaluator-private `#[cfg(test)]` entry running `replay_run`'s own body over the test registry. That is not
    MC8:1108's seam, because a `#[cfg(test)]` item compiles only in the evaluator's own test build (X12:276; X12:252).
    Both joins run (MC8:1113). *Conditions:* a test-registry row per fixture pack, whose document hashes to the Plan's
    `policyDigest` (`TEST_PACKS` holds neither fixture pack); the detector rebound. **If the map lists no (ii) case,
    selector 4, the (ii) form of A4's pin and the evaluator-private entry are all dropped from the unit.**
- **X5 item 8 bounds the map (X5:154-162).** These host tests each keep at least one host-replayed case:
  - the corpus replays through `replay_candidate` (:155);
  - "the corpus's forged cases" are `evidence.regeneration-mismatch` (:157);
  - the `missing-blob-…` case and member removal (:159-160);
  - "a schema or identity failure inside `Input` is `EVALUATION.INPUT_REFUSED`" (:161);
  - "the limits test of items 4 and 5e" (:162).
  
  *PROPOSED reading of X5:157:* "a tampered output (one byte of a claimed output, the corpus's forged cases) is
  `evidence.regeneration-mismatch`" is kept by one host-replayed forged case per host row, and the other forged cases
  go to (iii), (iv) or, by exception, (ii).
- **Boundary.** Every Run passed to `replay_run` (directly or through `replay_candidate` or `finalize`) names the release
  pack, or in (ii) a test-registry pack, whatever outcome its test expects. The only exemption is a C4-T14 negative
  (MC8:1117): a regenerated Run with exactly one join input re-pointed (pack id, pack count, policy digest, or detector
  closure), with the dependent identities re-derived. Every other refusal test asserts its exact diagnostic.
- **Fixtures that share these Plans but never reach `replay_run`** (CEN §4: the composition, enumeration-join,
  evaluator-parameter, execution-input, full-walk, input-structure, plan-input and reconstruction fixtures, and
  `evaluator/tests/fixtures/policy-pack-plan-fixture.json`) are unchanged. Where a correspondence check ties one to the
  replay corpus (`native-owner-patterns-materialization-r2/runners/check_fixture_correspondence.py`), the check is kept
  passing, or amended with the reason stated and reviewed.

**A8. What a corpus Plan must carry. PROPOSED.** An (i) Plan passes both joins (MC8:1098-1099; MC8:474-476) and what
`derive_evaluation` requires for the release pack with an empty population (at least `policy.rs:588-597`,
`composition.rs:765-778`). It need not meet item 18 in full: item 18 binds C4 (MC8:1076), and "a Plan without
`typescript.imports` is lawful" (MC8:1094). An (i) Plan is a synthetic fixture, not a Plan the product would build, and
shows nothing of item 18 or of rule evaluation. C4-T11, C4-T12 and C4-T14's TS leg cover those.
- **Pack provenance. SETTLED-BY-TEXT (X12:288; lead ruling).** X12:288 forbids "a Plan whose `policyPackIds` or
  `policyDigest` did not come from an `AdmittedPack`", with no synthetic exception. A corpus Plan's pack id, policy
  digest, and committed policy and program therefore come from an `AdmittedPack` issued by the product's real admission:
  `admit_pack` over `Named("opensip.preview.typescript.pack:1")` (accessors `policy.rs:836-857`), or in (ii) the
  evaluator's admission over the test registry. They are never typed and never copied from a registry file. A C4-T14
  refusal input is lawful as such (X12:245; MC8:1117).

**A9. The generator. PROPOSED (lead ruling: branch (b)).** A drift-checked regenerator in product test support, labelled
synthetic, beside `run_candidate.rs` (:15-19), re-deriving with `derive_evaluation` from today's `*.native-owner-r1*.json`
files. The step that sets a Plan's pack fields and re-derives the dependent identities holds an `AdmittedPack` (A8). It
covers (i) and (ii); (iii) has its own builder and control (A7).
- **Diff control.** For every regenerated Run, a recorded comparison with its predecessor under the old-to-new identity
  map. Each differing record must be one the pack or the detector closure reaches: the Plan, the analysis-spec, the
  policy and program, the emission row, the detector closure, `semanticClosures`, the identities derived from them, the
  re-derived outputs and the seal. Nothing else may differ; labels and non-identity expectations are unchanged.
- **Crash-matrix rebinding.** `bound_to` (`run_candidate.rs:279-290`), `bind` (:338, with its closure map at :376-384)
  and `renaming_the_evaluator_closure` (:544) swap in `CommitSession::core_evaluator_closure`. Each must also rebind every
  emission row's detector closure to that descriptor with `kind: "detector"`, retained and a `semanticClosures` member,
  before the fixpoint rewrite (MC8:475; lead ruling Q6). This is done with C1. It reaches the F01 row and the lead sets,
  whose changed expectations are re-transcribed under S12 before review.

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
- **Forbidden** (MC8:1112-1115): "a corpus Plan naming `"fixture"` after X12d" (narrowed only by selector 4, if (ii) is
  used); "a replay path without the join"; "deleting the pin tests rather than amending them"; "X9 evidence from an
  earlier commit offered for X12d".
- **Controls** (MC8:1117-1119): "C4-T14: replay refuses an unbundled pack, a wrong digest, and a detector from another
  core"; "C4-T15: the regenerated corpus replays"; "C4-T16: the X9 matrix passes on the X12d commit". Also A4's pin,
  A7's coverage map and (iii) control, and A9's diff control.

## Rejected alternatives

- **The original runner as generator.** The census found it cannot run today and cannot target the release pack, and
  the reference models hardcode the fixture packs (CEN §3; QUESTIONS Q7).
- **All corpora onto an empty population** (r1-r2's A7). It would erase the host corpus's findings and forged-content
  negatives and the cycle cases' verdicts.

## What this record does not do

It adds no law beyond MC8 item 19, except selector 3 and, only if (ii) is used, selector 4. It does not cover Rust
Plans (X12d-RS; PA1 §1.2: "Must not claim: X12d complete; the join exercised on a Rust Plan"). It does not settle how
the Plan build receives the pack. That is the provider-request unit's, by a separate lead ruling: the typed
`&AdmittedPack`, per X12:208 ("only from an `AdmittedPack`") and X12:288. MC8:923 says "from", not "only from".

## Open points

- **O1. Nothing checks the pack at replay today, and the first Run waits for X12d-TS.** `replay_run` has no pack check
  (`replay.rs:177-202`). The Plan build checks only caller-supplied strings (`host/src/plan.rs:312-340`). No TS1 Run counts
  as M3-M-TS1 before X12d-TS lands: X12:222, X12:266; MC8:1109, :1113; PA1:142.
- **O2. "With the M3 Plan builder" (X12:266; X12:220).** This record reads it as placement (MC8:1097). Read as "built by
  the Plan builder", every corpus Plan would meet item 18 in full. Part a's builder is on main (QUESTIONS Q3), and (iii)
  already needs most of item 18.
- **O3. Whether (ii) is used** is the coverage map's finding (A7). The clauses that fall away if it is not are selector 4,
  A4's second form, A7's (ii) bullet, and the (ii) mentions in A7's Principle and Boundary and in A8.

## Consequences

X12d-TS works under MC8 item 19 in full, as amended by A1-A11. The coverage map precedes C1's regeneration. C1 may be
drafted, not frozen, before this record is accepted.
