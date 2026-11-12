# X12-A r1 — record amendment to X12's X12d text (corpus target)

2026-11-11. Drafted by a lead-dispatched design author (Claude Opus 5.5, route R2-DEEP, effort medium) from
`LC/x12d-ts/SCOPE-r1.md` §1 and the lead's rulings (`LC/x12d-ts/QUESTIONS.md`, and the coordinator's relays of 2026-11-11).
Status: **PROPOSED, r3.** History: r2 applied the lead's rulings on r1's open points. r3 applies the independent review
`LC/x12d-ts/review-opus-x12a/VERDICT.md` (RF-1 to RF-6) under the lead's RF-1 ruling, which replaces the earlier
"all corpora onto an empty population". It needs the cross-vendor review before X12d-TS's C1 freezes (PA1's premise
rule, PA1:330-333). It binds nothing and changes no existing file, registry or lock.
Marks: **SETTLED-BY-TEXT** (restates accepted law), **PROPOSED** (a reading or rule that needs review).

## Short names

Architecture main `fa6fa0fba`; product main `1bd328f3` (paths without prefix). `LC` = `.opensip-implementation-cache/lead-2026-10-25`.
Lines are those of the accepted bytes; the banner file `PROPOSAL.md` is offset by the number in brackets.

| Name | Document |
|---|---|
| **X12** | `docs/implementation/m2/policy-admission-x12/PROPOSAL-r4.md` (accepted, Grok) [+2] |
| **MC8** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md` (accepted, CODEX2) [+4] |
| **X5** / **I1** | `m2/replay-join-x5/PROPOSAL-r4.md` [+2] / `m3/preview-pack-i1/PROPOSAL-r3.md` [+2] |
| **PA1** | `LC/pa1/PLAN-AMENDMENT-TS1-r3.md` |

**Amended selectors.** (1) X12:266, the units bullet: "regeneration of the synthetic replay corpus onto the bundled test
pack, with the M3 Plan builder (item 9)". (2) X12 item 9 (X12:214-224) gains one note; its text stays as X12's own state.
(3) **MC8:1101 (item 19 part 4), "with an empty `typescript` file population, so the rule evaluates nothing", to the
extent it reaches a branch (iii) corpus (A7).** (1) is the amendment MC8 names: "This is a record amendment to X12 r3's
X12d text" (MC8:1101; MC8:1152; C4b's edge, MC8:1187).

## Clauses

**A1. The corpus target.** *SETTLED-BY-TEXT (MC8:1101):* "onto the bundled test pack" is replaced. X12:266 reads, after
amendment: "**X12d (M3), inventory successor.** The Run-closure application of `check_plan_pack` inside replay, and
regeneration of the synthetic replay corpora under X12-A's A7, with the M3 Plan builder (item 9; X12-A). Its parts are
MC8 item 19. It must land before any analysis producer can reach X5." *PROPOSED:* the A7 split (it amends selector (3));
and the reading of "with the M3 Plan builder" as placement, X12d being C4's inventory successor (MC8:1097) (O2).

**A2. The reason. SETTLED-BY-TEXT (MC8:1101).** `check_plan_pack` always uses `RELEASE_PACKS`, and the test registry is
`cfg(test)`-private to the evaluator, so storage, host and crash-matrix builds never see it. **Citation correction:**
MC8:1101's `policy.rs:1361-1367` is now `evaluator/src/policy.rs:1410-1416` (`check_plan_pack_in(&RELEASE_PACKS, …)` at
:1415); its `policy.rs:1412` is now `:1461-1463` (`#[cfg(test)] mod pack_tests`), which holds `TEST_PACKS`
(`policy_pack_tests.rs:20`; one row, `opensip.test.fixture.pack:1`).

**A3. Rejected: a test registry reachable downstream. SETTLED-BY-TEXT (MC8:1108; X12:276).** "A feature-gated test
registry reachable from downstream builds. It is a new cfg seam on admission, and needs an X8 and X9 site-list
amendment" (MC8:1108). Forbidden: "a `cfg(test)` row or test registry reachable from a release build" (X12:276).

**A4. The pins. SETTLED-BY-TEXT:** they are "amended, not deleted" and after X12d say `check_plan_pack` is "wired exactly
once, in replay" (MC8:1100; forbidden "deleting the pin tests rather than amending them", MC8:1114). *PROPOSED,* how the
pins say it, since a host forbidden list cannot express "exactly once, in replay":
- **host** `fact_admission_tests.rs:665-681` (`"check_plan_pack"` at :671; MC8's `:661-668`) stays a forbidden list, so the
  host never wires a second join; its comment at :665 is re-cited from "X12 r3 item 9" to X12d;
- **configuration** `configuration_tests.rs:507` (MC8's `:449-450`) is unchanged: it pins the configuration projection,
  which never calls `check_plan_pack` before or after X12d;
- **new evaluator pin (owed by X12d-TS, scope commit C4):** `check_plan_pack(` and the detector join each occur exactly
  once in `evaluator/src/replay.rs`, after the seal read (`replay.rs:185-192`; the detector join needs `evaluatorClosure`,
  :201) and before `derive_evaluation(` (:202).

**A5. Item 9 keeps its text. PROPOSED (form; lead ruling).** X12:220 ("X12 does not insert `check_plan_pack` into
`replay_run` …") stays as X12's state at r4. Note added after X12:224: "*X12-A:* X12d inserts `check_plan_pack`, and
MC8 item 9's detector join, into `replay_run` after the Plan and seal are read and before `derive_evaluation` (MC8:1098-1099)."

**A6. Item 10's `check_plan_pack` tests stand. SETTLED-BY-TEXT (X12:245).** They are evaluator unit tests over
`TEST_PACKS` and never pass through `replay_run`. Their refusal inputs, "a corpus Plan naming `"fixture"` is refused; … a
test-pack Plan with any other policy digest is refused" (X12:245), show that X12:288 does not forbid a refusal input (A8).

**A7. Which corpus goes where. Principle SETTLED-BY-TEXT; branches PROPOSED (lead ruling on RF-1).**
- **Principle.** After X12d, no Run that reaches replay in any build outside the evaluator crate's own unit tests names a
  non-release pack. It follows from 19.1 ("`replay_run` … calls `check_plan_pack`", MC8:1098), "a replay path without the
  join" (MC8:1113) and "a corpus Plan naming `"fixture"` after X12d" (MC8:1112).
- **(i) Structure corpora** (tests of replay, admission, commit or crash behaviour, not of what a rule finds): regenerated
  onto `opensip.preview.typescript.pack:1` with an empty `typescript` file population, as MC8:1101 says. *Keep:* every
  case label and outcome kind. *Lose:* nothing their tests assert.
- **(ii) Rule-evaluating corpora whose tests live, or can live, in the evaluator crate:** keep their fixture packs, and are
  replayed only through an evaluator-private, `#[cfg(test)]` entry that runs `replay_run`'s own body over the test
  registry, as `check_plan_pack_in` already does for `check_plan_pack` (`policy.rs:1415-1417`). This is not MC8:1108's
  rejected seam: that is "feature-gated" and "reachable from downstream builds"; a `#[cfg(test)]` item is compiled only
  in the evaluator's own unit-test build, never in a dependent's build and never in a release build (X12:276), and the
  `cfg(test)` registry is X12a's accepted scope (X12:252). The entry still runs both joins (no path "without the join",
  MC8:1113), and the `ReplayedRun` is still built only in `replay_run`'s body (X5:188, "A `ReplayedRun` built anywhere but
  `replay_run`", is forbidden). *Condition:* each fixture pack a branch (ii) Plan names is a `cfg(test)` registry row whose
  document hashes to that Plan's `policyDigest`; today `TEST_PACKS` has only `opensip.test.fixture.pack:1`. *Keep:*
  everything. *Lose:* nothing; the evaluation is still that of a fixture pack, not the release rule.
- **(iii) Rule-evaluating corpora whose tests must stay outside the evaluator** (host or storage handling of a Run that
  carries findings): regenerated onto the release preview pack with a **non-empty** `typescript` population that yields
  findings by the release pack's own rule (`module-import-cycle`). *Keep:* case labels, case kinds (value, `mismatch`,
  `unavailable`) and every forged-content negative. *Lose:* the fixture rules' particular findings, counts and verdict mix,
  which become the release rule's. **This amends MC8:1101's "empty population" for these corpora** (selector (3)): a
  corpus whose tests exist to check findings cannot check them with none. Such Plans need item 18's EnumerationPlan and
  `imports` symbol inventories (MC8:1079-1082), or "Every subject would then be indeterminate" (MC8:1089), so A8's relief does not
  reach them.
- **Boundary (RF-2).** Every Run passed to `replay_run`, directly or through `replay_candidate` or `finalize`, whatever
  outcome its test expects, names the release pack (or, in (ii), a test-registry pack). The only exemption is a C4-T14
  negative (MC8:1117): a regenerated Run with exactly one join input re-pointed, the pack id, the pack count, the policy
  digest, or (the detector negative) the detector closure, with dependent identities re-derived so that this input is the
  only thing wrong. A Run a test expects replay to refuse for any other reason (the host corpus's 9 `mismatch` and 1
  `unavailable` cases) names the release pack, and its test asserts the exact diagnostic, not only the row.
- **Corpora. To be confirmed against the census (`LC/x12d-ts/CENSUS-C0.md`, not yet written) before the cross-vendor
  review.** Rows marked `?` are uncertain.

| Corpus | Replayed by | Branch |
|---|---|---|
| `security/tests/fixtures/journal-seal-replay.native-owner-r1.json` (1 Run, `fixture.file-observed`) | `security/src/journal_store.rs:1693` | (i) |
| storage crash-matrix synthetic `storage/src/crash_matrix_support/run_candidate.rs` (from the row above, :2-4) | storage `src/` and `tests/commit_tests.rs`; host `crash_matrix_support.rs:383`, `:591`, `:651` (`finalize`) | (i) |
| `evaluator/tests/fixtures/cycle-representative.native-owner-r1.v1.json` `retainedCases` (4 Runs, `fixture.semantic-atom`; `fail`, `pass`, 2 `indeterminate`) | `evaluator/src/atoms.rs:4467` | (ii) |
| evaluator test-built Runs other than the above | evaluator unit tests | (ii) or (i) `?` |
| `host/tests/fixtures/replay-fixtures.native-owner-r1.json` (101 cases, 73 Runs, 93 findings; 9 `mismatch`, 1 `unavailable`) | `host/src/fact_admission_tests.rs:77`, `finalization_tests.rs:749`, `native_owner_tests.rs:2882`, `tests/admission_tests.rs:2543` | (iii) `?` (whether some of its tests can move to (ii)) |

**A8. What a corpus Plan must carry. PROPOSED.** A (i) corpus Plan must pass the pack join (19.1), the detector join (19.2;
MC8:474-476) and whatever `derive_evaluation` itself requires for the release pack with an empty `typescript` population
(at least `policy.rs:588-597` and `composition.rs:765-778`: a `kind: detector` closure that is a `semanticClosures`
member). It need not meet item 18 (MC8:1075-1094) in full: item 18 binds C4 ("When the selection admits …, C4: …",
MC8:1076), and "a Plan without `typescript.imports` is lawful" (C4-T13, MC8:1094). A (iii) Plan meets what its findings
need (A7). A (ii) Plan passes both joins over the test registry.
- **Pack provenance (SETTLED-BY-TEXT, X12:288; lead ruling).** X12 forbids "a Plan whose `policyPackIds` or
  `policyDigest` did not come from an `AdmittedPack`" (X12:288), with no exception for synthetic corpora. A corpus Plan's
  pack id, policy digest, and the policy bytes and compiled program it commits come from an `AdmittedPack` produced by the
  product's real admission (`admit_pack` over `Named("opensip.preview.typescript.pack:1")`, accessors `policy.rs:836-857`;
  in (ii), the evaluator's admission over the test registry), never typed and never copied from a registry file. A
  C4-T14 refusal input is lawful as a refusal input, as X12:245 and MC8:1117 already require (r2's O3, closed).
- **What a corpus Plan does not show.** It is a synthetic fixture, not a Plan the product would build. An (i) Plan shows
  nothing of item 18's EnumerationPlan, the imports request, the symbol inventories or any rule evaluation; C4-T11,
  C4-T12 and C4-T14's TS leg are the controls that do.

**A9. The generator. PROPOSED.** Pinned records change only by their generators. On both branches, the step that sets
the Plan's pack fields and re-derives the dependent identities is product code that holds an `AdmittedPack` (A8). The
crash-matrix synthetic's fixpoint rewrite (`run_candidate.rs:10-14`) is the model; a design-side runner alone cannot be
the whole generator. X12d-TS's first worker establishes which holds before regenerating anything.
- **(a) The original runner,** if it can be parameterized to target the release pack:
  `docs/implementation/m3/native-publication/native-owner-patterns-materialization-r2/runners/` (product commit
  `a62fbd7c`), changed on a reviewed architecture branch. It rewrites committed predecessors, not from scratch
  (`apply_fixture_companions.py:15-20`). Conditions: it first reproduces today's `*.native-owner-r1*.json` byte for byte
  from the committed `*.current*.json` inputs (`replay-fixtures.current.json`, `journal-seal-replay.current.json`,
  `cycle-representative.current.v1.json`, and the others it names) under the pinned Python 3.12 / Unicode 15.0.0
  toolchain; and its output passes through the product pack step.
- **(b) Otherwise,** a drift-checked generator in product test support, labelled synthetic as `run_candidate.rs` is
  (:15-19), including the product pack step. Its inputs are today's `*.native-owner-r1*.json` files. Condition: the worker
  records exactly why (a) fails.
- **Diff control (RF-5), both branches.** For every regenerated Run, a recorded comparison with its predecessor, under
  the old-to-new identity map, lists every record that differs and shows each is one the pack or the detector closure
  reaches: the Plan, the analysis-spec, the committed policy and program, the emission row, the detector closure,
  `semanticClosures`, the identities derived from them, the re-derived outputs and the seal; in (iii) also the
  `typescript` population and what derives from it. Nothing else differs. Case count and labels are unchanged; in (i) and
  (ii), non-identity expectations are unchanged too.
- **The crash-matrix rebinding (RF-6), a requirement on `run_candidate.rs`.** `bound_to` (:279-290) swaps in
  `CommitSession::core_evaluator_closure`, and `bind` (:338; the closure map at :376-384) and `renaming_the_evaluator_closure`
  (:544) rewrite to it. The detector join compares the Plan's detector closure with *that* descriptor except `kind`
  (MC8:475), so both must also rebind the detector closure to the session's evaluator descriptor with `kind: "detector"`,
  retained and a `semanticClosures` member, before the fixpoint rewrite. Otherwise every crash-matrix candidate fails the join.

**A10. Edges and the lead set. SETTLED-BY-TEXT.** "X12d depends on I1-c (the row) and I1-b2 (the op)" (MC8:1102), both
integrated (`m3/IMPLEMENTATION-STATUS.md:249`). "X12d's evidence includes a full X9 matrix lead set on X12d's commit
(`matrixPass: true`). It is serialized with every other lead run set" (MC8:1103).

**A11. The refusal row and carrier.** Row **SETTLED-BY-TEXT**: X5 item 5's structural row, `EVALUATION.INPUT_REFUSED`
(MC8:1098-1099; X12:218; X5:77). Carrier **PROPOSED** (lead ruling Q1): the existing `ReplayError::Structure(
RetainedWalkError::Policy(e))` (`replay.rs:20`, `full_walk.rs:40`; already searched, `unavailable_evidence.rs:135`) for
both joins, no new variant, under the owner budget `limits.retained.owner` (`replay.rs:171`). The law names no keys for
the detector join; C2 names them.

## What X12d must do: MC8 item 19, all of it, as amended here

- **Parts.** 1, "`replay_run` … calls `check_plan_pack` after reading the Plan and before `derive_evaluation`" (MC8:1098);
  2, "Item 9's join is wired at the same point, with the same row" (:1099), the scope's detector-join commit C2; 3, the
  pins (:1100; A4); 4, the corpus (:1101; A7); 5, the edges (:1102); 6, the serialized X9 lead set (:1103; A10).
- **Forbidden substitutes** (MC8:1112-1115): "a corpus Plan naming `"fixture"` after X12d"; "a replay path without the
  join"; "deleting the pin tests rather than amending them"; "X9 evidence from an earlier commit offered for X12d".
- **Controls** (MC8:1117-1119): "C4-T14: replay refuses an unbundled pack, a wrong digest, and a detector from another
  core"; "C4-T15: the regenerated corpus replays"; "C4-T16: the X9 matrix passes on the X12d commit". Plus A4's new pin
  and A9's diff control.

## What this record does not do

It adds no law beyond MC8 item 19, except the amendment of MC8:1101's empty population for branch (iii) (A7). It does
not cover Rust Plans (X12d-RS; PA1 §1.2, "Must not claim: X12d complete; the join exercised on a Rust Plan"). It does
not settle how the Plan build receives the pack (the provider-request unit's; Consequences).

## Open points

- **O1. Today nothing checks the pack at replay, and the first Run waits for X12d-TS.** `replay_run` reads the Plan
  (`replay.rs:177-180`) and calls `derive_evaluation` (:202) with no pack check between. The Plan build compares the
  Plan's pack fields with caller-supplied strings (`host/src/plan.rs:156-157`, :312-340); its `check_plan_pack` call is
  `#[cfg(test)]` (:968, :1024). No TS1 Run counts as M3-M-TS1 before X12d-TS lands: the join "must land before any
  analysis producer is wired" (X12:222; X12:266); MC8 forbids "a replay path without the join" (MC8:1113) and rejects
  "leaving replay unwired until J" (MC8:1109); J2b-TS consumes X12d-TS (PA1:142).
- **O2. "With the M3 Plan builder" (X12:266; X12:220, "Corpus regeneration belongs with the M3 Plan builder").** This
  record reads it as placement (MC8:1097), and MC8 item 19 does not repeat it. The alternative reading, "built by the Plan
  builder", would cost corpus Plans built by the product's Plan builder: item 18 in full for every corpus Run. Part a's
  builder is on main (`LC/x12d-ts/QUESTIONS.md`, Q3), so it would not wait on C4a-TS-b; branch (iii) already needs most
  of item 18.
- **O3. The census.** A7's table is fixed from `CENSUS-C0.md` before the cross-vendor review.

## Consequences

- **X12d-TS** works under MC8 item 19, all six parts with its forbidden substitutes and controls, as amended by A1-A11.
  Its C1 may be drafted, not frozen, before this record is accepted.
- **The provider-request unit** (and J2b-TS): by a separate lead ruling, its entry takes the owner's typed admitted pack
  (`&AdmittedPack`) instead of strings. The texts: "The future M3 Plan builder takes the policy only from an
  `AdmittedPack`" (X12:208); the forbidden "a Plan whose `policyPackIds` or `policyDigest` did not come from an
  `AdmittedPack`" (X12:288); MC8's Plan table, "`policyPackIds` from the `AdmittedPack` (item 18)" (MC8:923). The "only"
  rests on X12:208 and :288; MC8:923 says "from".
